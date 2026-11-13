#!/usr/bin/env python3
"""Snapshot T1 inputs once, then verify preservation without rewriting the baseline."""
import argparse
from collections import Counter
from datetime import date
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path, PurePosixPath
import re
import sys
from urllib.parse import unquote, urljoin, urlsplit


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs/content-migration-manifest.json"
PUBLIC_DIRS = {
    "about", "assets", "cv", "dlm-survey", "legacy", "notes", "publication",
    "publications", "resume", "wyx0226.github.io", "year-archive",
}
PUBLIC_EXTENSIONS = {".html", ".css", ".js", ".pdf", ".svg", ".ico", ".woff", ".woff2"}
HELPER_MOVES = {
    "dlm-survey/generate.py": "content/series/dlm-survey/generate.py",
    "dlm-survey/s12_vae_summary.md": "content/series/dlm-survey/s12_vae_summary.md",
    "dlm-survey/shared.css": "content/series/dlm-survey/shared.css",
    "dlm-survey/style.css": "content/series/dlm-survey/style.css",
    "content/notes.json": "content/archive/notes-before-migration.json",
}
GENERATED_ROOT = {"index.html", "about.html", "404.html", "robots.txt", "sitemap.xml"}


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(data):
    return hashlib.sha256(data).hexdigest()


def route(path):
    return "/" + (path[:-10] if path.endswith("index.html") else path)


def normalize_url(value):
    parsed = urlsplit(value)
    path = unquote(parsed.path)
    if path.endswith("/index.html"):
        path = path[:-10]
    return path or "/"


class Document(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.anchors = []
        self.links = []
        self.markers = []
        self.headings = []
        self.updated = []
        self._heading = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        anchor = attrs.get("id") or (attrs.get("name") if tag == "a" else None)
        if anchor:
            self.anchors.append(anchor)
        for key in ("href", "src", "poster"):
            if attrs.get(key):
                self.links.append(attrs[key])
        if tag in {"h1", "h2", "h3"}:
            self._heading = {"level": int(tag[1]), "anchor": attrs.get("id"), "text": ""}
        if attrs.get("id") == "last-updated":
            self.updated.append(attrs.get("datetime"))

    def handle_endtag(self, tag):
        if self._heading is not None and tag == f"h{self._heading['level']}":
            self._heading["text"] = " ".join(self._heading["text"].split())
            self.headings.append(self._heading)
            self._heading = None

    def handle_data(self, value):
        if self._heading is not None:
            self._heading["text"] += value

    def handle_comment(self, value):
        if "AUTO:INSERT:" in value or "SITE:NAV:" in value:
            self.markers.append(value.strip())


def document(data):
    doc = Document()
    doc.feed(data.decode("utf-8"))
    return doc


def public_file(path):
    parts = path.parts
    if any(p.startswith(".") and p != ".nojekyll" for p in parts):
        return False
    return (len(parts) == 1 and (path.suffix == ".html" or path.name in {
        ".nojekyll", "robots.txt", "sitemap.xml"})) or (
        parts[0] in PUBLIC_DIRS and path.suffix in PUBLIC_EXTENSIONS)


def mappings(catalog, site):
    result = dict(HELPER_MOVES)
    for entry in catalog["entries"]:
        if entry["origin"] != "local":
            continue
        source = entry["source"]
        if entry["kind"] == "chapter":
            old = "dlm-survey/" + PurePosixPath(source).name
        elif entry["kind"] == "series":
            old = "dlm-survey/index.html"
        elif entry["status"] == "archived":
            old = "legacy/rl-interview-guide.html"
        else:
            old = entry["id"] + ".html"
        result[old] = source
    for page in site["pages"]:
        result[f"content/{page['id']}.md"] = page["source"]
    return result


def snapshot():
    if MANIFEST.exists():
        raise ValueError("Baseline exists; refusing to overwrite pre-migration evidence")
    catalog = read_json(ROOT / "content/catalog.json")
    site = read_json(ROOT / "content/site.json")
    moved = mappings(catalog, site)
    public = sorted(
        p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*")
        if p.is_file() and public_file(p.relative_to(ROOT))
    )
    publications = sorted(p.relative_to(ROOT).as_posix()
                          for p in (ROOT / "content/publications").glob("*.md"))
    paths = sorted(set(public) | set(moved) | set(publications) |
                   {"licenses/academic-pages-MIT.txt", "templates/home.html"})
    records = []
    for old in paths:
        data = (ROOT / old).read_bytes()
        generated = (old in public and old not in moved and old != ".nojekyll" and
                     (old in GENERATED_ROOT or old.split("/")[0] not in {"assets", "dlm-survey"}))
        record = {
            "before": old,
            "after": None if generated else moved.get(old, old),
            "action": "remove-generated" if generated else ("move" if old in moved else "retain"),
            "sha256": sha(data),
            "bytes": len(data),
            "public_url": route(old) if old in public else None,
            "anchors": [],
        }
        if old.endswith(".html"):
            doc = document(data)
            record.update({
                "anchors": sorted(set(doc.anchors)),
                "headings": doc.headings,
                "links": doc.links,
                "markers": doc.markers,
                "last_updated": doc.updated,
            })
        records.append(record)
    baseline = {
        "schema_version": 1,
        "phase": "pre-migration",
        "hash_algorithm": "sha256",
        "baseline_note": "Current uncommitted consolidation, not HEAD; never regenerate after source edits.",
        "counts": {"local_collections": 9, "root_posts": 8, "series": 1, "chapters": 14,
                   "publications": 4, "external_links": 2},
        "external_links": [{"id": e["id"], "url": e["url"]} for e in catalog["entries"]
                           if e["origin"] == "external"],
        "files": records,
    }
    # This is generated evidence, not an editable source or a build input.
    MANIFEST.write_text(json.dumps(baseline, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"SNAPSHOT: {len(records)} files, {len(public)} public files; immutable baseline {MANIFEST.name}")


def validate_contract(catalog, site, redirects, baseline):
    errors = []
    entries = catalog["entries"]
    ids, urls, sources = set(), set(), set()
    topics = {row["id"] for row in site["topics"]}
    types = {row["id"] for row in site["types"]}
    by_id = {e["id"]: e for e in entries}
    for e in entries:
        name = e["id"]
        for key in ("title", "summary"):
            if not isinstance(e.get(key), str) or not e[key].strip():
                errors.append(f"{name}: {key} must be nonempty")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            errors.append(f"{name}: invalid id")
        if name in ids:
            errors.append(f"{name}: duplicate id")
        ids.add(name)
        if e["url"] in urls or (e["origin"] == "local" and normalize_url(e["url"]) in urls):
            errors.append(f"{name}: duplicate url")
        urls.add(e["url"])
        if e["origin"] == "local":
            urls.add(normalize_url(e["url"]))
        for key, allowed in (("topic", topics), ("type", types), ("kind", site["kinds"]),
                             ("status", site["statuses"]), ("origin", site["origins"]),
                             ("review_status", site["review_statuses"])):
            if e.get(key) not in allowed:
                errors.append(f"{name}: illegal {key}={e.get(key)!r}")
        if not isinstance(e.get("tags"), list) or not all(isinstance(t, str) and t for t in e["tags"]):
            errors.append(f"{name}: tags must be nonempty strings")
        if not isinstance(e.get("featured"), bool):
            errors.append(f"{name}: featured must be boolean")
        if len(e["related"]) != len(set(e["related"])) or any(
                other not in by_id or other == name for other in e["related"]):
            errors.append(f"{name}: invalid related IDs")
        if e["origin"] == "external":
            if e["source"] is not None or e["kind"] != "external" or urlsplit(e["url"]).scheme not in {"http", "https"}:
                errors.append(f"{name}: external source/url/kind contract violated")
        else:
            source = e["source"]
            if not isinstance(source, str) or not source.startswith("content/") or ".." in PurePosixPath(source).parts:
                errors.append(f"{name}: source must be a relative content path")
            elif not (ROOT / source).is_file():
                errors.append(f"{name}: missing source {source}")
            if source in sources:
                errors.append(f"{name}: duplicate source")
            sources.add(source)
            parsed = urlsplit(e["url"])
            if not e["url"].startswith("/") or parsed.scheme or parsed.netloc or parsed.query or parsed.fragment:
                errors.append(f"{name}: local url must be a root-relative route")
        if e["updated"] is not None:
            try:
                if date.fromisoformat(e["updated"]).isoformat() != e["updated"]:
                    raise ValueError("not ISO")
            except (ValueError, TypeError):
                errors.append(f"{name}: invalid updated date")
        if e["updated_source"] is not None:
            expected = {"kind": "html-element", "id": "last-updated", "attribute": "datetime"}
            if e["updated_source"] != expected or e["updated"] is not None or e["origin"] != "local":
                errors.append(f"{name}: invalid derived date contract")
            elif (ROOT / e["source"]).is_file():
                values = document((ROOT / e["source"]).read_bytes()).updated
                try:
                    if len(values) != 1 or date.fromisoformat(values[0]).isoformat() != values[0]:
                        raise ValueError("missing or duplicate date")
                except (TypeError, ValueError):
                    errors.append(f"{name}: invalid body last-updated date")
        if e["kind"] == "chapter":
            parent = by_id.get(e["series"])
            if not parent or parent["kind"] != "series":
                errors.append(f"{name}: invalid series parent")
            if type(e["order"]) is not int or e["order"] < 1:
                errors.append(f"{name}: invalid chapter order")
        elif e["series"] is not None or e["order"] is not None:
            errors.append(f"{name}: only chapters may set series/order")
    for parent in (e for e in entries if e["kind"] == "series"):
        children = [e for e in entries if e["series"] == parent["id"]]
        orders = [e["order"] for e in children]
        if not children or sorted(orders) != list(range(1, len(children) + 1)):
            errors.append(f"{parent['id']}: chapter order must be unique and contiguous")
    baseline_sources = {r["after"] for r in baseline["files"] if r["after"]}
    baseline_entries = [e for e in entries if e["source"] in baseline_sources]
    local = [e for e in baseline_entries if e["origin"] == "local" and
             e["status"] == "published" and e["kind"] != "chapter"]
    if (len(local) != baseline["counts"]["local_collections"] or
            sum(e["kind"] == "chapter" for e in baseline_entries) != baseline["counts"]["chapters"]):
        errors.append("original collection/chapter coverage differs from the immutable baseline")
    if len([e for e in entries if e["origin"] == "external"]) != 2:
        errors.append("baseline external coverage differs from 2")
    publication_ids = {p.stem for p in (ROOT / "content/publications").glob("*.md")}
    baseline_publications = {
        Path(r["after"]).stem for r in baseline["files"]
        if r["after"] and r["after"].startswith("content/publications/")
    }
    if not baseline_publications <= publication_ids or not set(site["publications"]["featured"]) <= publication_ids:
        errors.append("publication coverage or featured ID invalid")
    for row in site["pages"] + site["assets"]:
        if not (ROOT / row["source"]).is_file():
            errors.append(f"site: missing source {row['source']}")
    targets = set(urls) | {"/", "/blog/", "/publications/", "/404.html", "/robots.txt", "/sitemap.xml", "/.nojekyll"}
    for row in site["pages"] + site["assets"]:
        normalized = normalize_url(row["url"])
        if normalized in targets:
            errors.append(f"site: conflicting route {row['url']}")
        targets.add(normalized)
    targets |= {f"/publication/{p}/" for p in publication_ids}
    seen = set()
    for row in redirects["redirects"] + redirects["copies"]:
        old, new = normalize_url(row["from"]), normalize_url(row["to"])
        if old in seen or old in targets:
            errors.append(f"redirects: conflicting from {row['from']}")
        seen.add(old)
        if new not in targets:
            errors.append(f"redirects: missing target {row['to']}")
        if row.get("query_policy") not in {None, "blog"}:
            errors.append(f"redirects: invalid query_policy {row['from']}")
    return errors, targets | seen


def verify(allow_content_changes=False, require_clean=False):
    baseline = read_json(MANIFEST)
    receipts_path = ROOT / "docs/content-changes.json"
    receipts = {r["source"]: r for r in read_json(receipts_path)["changes"]} if receipts_path.exists() else {}
    catalog = read_json(ROOT / "content/catalog.json")
    site = read_json(ROOT / "content/site.json")
    redirects = read_json(ROOT / "content/redirects.json")
    errors, routes = validate_contract(catalog, site, redirects, baseline)
    verified, changed, anchors, markers = 0, [], 0, 0
    content_sources = {e["source"] for e in catalog["entries"] if e["origin"] == "local"}
    source_urls = {e["source"]: e["url"] for e in catalog["entries"] if e["origin"] == "local"}
    moved = {r["before"]: r["after"] for r in baseline["files"] if r["action"] == "move"}
    for record in baseline["files"]:
        old, new = record["before"], record["after"]
        if record["public_url"] and normalize_url(record["public_url"]) not in routes:
            errors.append(f"{old}: baseline public route not covered")
        if new is None:
            if require_clean and (ROOT / old).exists():
                errors.append(f"{old}: obsolete generated output remains")
            continue
        if old != new and require_clean and (ROOT / old).exists():
            errors.append(f"{old}: duplicate old source remains")
        dest = ROOT / new
        if not dest.is_file():
            errors.append(f"{old}: missing migrated file {new}")
            continue
        data = dest.read_bytes()
        current = sha(data)
        if current != record["sha256"]:
            receipt = receipts.get(new)
            if receipt and current == receipt["sha256"] and receipt.get("reason"):
                changed.append({"source": new, "baseline_sha256": record["sha256"],
                                "current_sha256": current, "reason": receipt["reason"]})
            elif allow_content_changes and new in content_sources:
                changed.append({"source": new, "baseline_sha256": record["sha256"], "current_sha256": current})
            else:
                errors.append(f"{new}: SHA mismatch {record['sha256']} -> {current}")
        else:
            verified += 1
        if new.endswith(".html"):
            doc = document(data)
            missing = set(record["anchors"]) - set(doc.anchors)
            if missing:
                errors.append(f"{new}: lost anchors {sorted(missing)}")
            if Counter(record.get("markers", [])) != Counter(doc.markers):
                errors.append(f"{new}: changed automation/navigation markers")
            anchors += len(record["anchors"])
            markers += len(record.get("markers", []))
            # Resolve relative HTML URLs against the public URL, not the source directory.
            public_url = source_urls.get(new)
            if public_url:
                for link in doc.links:
                    parsed = urlsplit(link)
                    if parsed.scheme or parsed.netloc:
                        continue
                    target = normalize_url(urljoin(public_url, link))
                    if target not in routes:
                        errors.append(f"{new}: unregistered local target {link} ({target})")
                    if parsed.fragment:
                        candidate = next((r for r in baseline["files"] if r["public_url"] and
                                          normalize_url(r["public_url"]) == target), None)
                        if candidate and candidate["after"] and candidate["after"].endswith(".html"):
                            path = ROOT / candidate["after"]
                            if path.is_file() and unquote(parsed.fragment) not in document(path.read_bytes()).anchors:
                                errors.append(f"{new}: missing linked anchor {link}")
    for e in baseline["external_links"]:
        if not any(row["id"] == e["id"] and row["url"] == e["url"] for row in catalog["entries"]):
            errors.append(f"{e['id']}: external URL changed or absent")
    for row in redirects["copies"]:
        old = next((r for r in baseline["files"] if r["public_url"] == row["from"]), None)
        target = next((r for r in baseline["files"] if r["public_url"] == row["to"]), None)
        # New aliases have no historical source. Historical aliases must continue
        # to share their original target; the target's exact update has a receipt.
        if old and (not target or old["sha256"] != target["sha256"]):
            errors.append(f"{row['from']}: compatibility copy is not byte-identical")
    if errors:
        print("\n".join(errors))
        print(f"FAIL: {len(errors)} migration/contract issues")
        return 1
    if changed:
        print("LATER CONTENT CHANGES (not a claim of byte-identical preservation):")
        print(json.dumps(changed, indent=2))
    print(f"PASS: {verified} exact SHA matches; {len(changed)} documented later changes; "
          f"{anchors} original source anchors; {markers} original markers; "
          f"{len(routes)} registered public routes")
    entries = catalog["entries"]
    collections = sum(e["origin"] == "local" and e["status"] == "published" and
                      e["kind"] != "chapter" for e in entries)
    chapters = sum(e["kind"] == "chapter" for e in entries)
    print(f"Original coverage retained: {baseline['counts']['local_collections']} collections, "
          f"{baseline['counts']['chapters']} chapters")
    print(f"Current coverage: {collections} local collections, {chapters} chapters, "
          f"{len(list((ROOT / 'content/publications').glob('*.md')))} publications, 2 external links")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", action="store_true", help="Capture once before any moves")
    parser.add_argument("--allow-content-changes", action="store_true",
                        help="Report later catalog HTML body SHA changes; still require original anchors/markers")
    parser.add_argument("--require-clean", action="store_true", help="Reject obsolete source/output copies")
    args = parser.parse_args()
    try:
        if args.snapshot:
            snapshot()
            return 0
        return verify(args.allow_content_changes, args.require_clean)
    except (KeyError, ValueError, TypeError, OSError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
