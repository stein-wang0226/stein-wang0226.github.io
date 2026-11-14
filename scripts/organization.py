#!/usr/bin/env python3
"""Record an immutable content baseline and verify retained research units."""
import argparse
from collections import Counter
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from render import ROOT, route_path


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


class Evidence(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.ids, self.links, self.markers, self.units = [], [], [], []
        self.active = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.append(attrs["id"])
        for key in ("href", "src", "data"):
            value = attrs.get(key, "")
            if value.startswith(("https://", "http://", "/assets/")):
                self.links.append(value)
        if tag in {"p", "li", "pre", "svg"} or "math" in attrs.get("class", "").split():
            self.active.append([tag, [], 1])
        for unit in self.active:
            if tag == unit[0] and unit[1]:
                unit[2] += 1
            unit[1].append(self.get_starttag_text())

    handle_startendtag = handle_starttag

    def handle_data(self, value):
        for unit in self.active:
            unit[1].append(value)

    def handle_entityref(self, value):
        self.handle_data("&" + value + ";")

    def handle_charref(self, value):
        self.handle_data("&#" + value + ";")

    def handle_comment(self, value):
        if "AUTO:INSERT:" in value:
            self.markers.append(value.strip())

    def handle_endtag(self, tag):
        for unit in self.active[:]:
            unit[1].append("</" + tag + ">")
            if tag != unit[0]:
                continue
            unit[2] -= 1
            if unit[2]:
                continue
            raw = "".join(unit[1])
            value = re.sub(r"\s+", " ", re.sub(r"<[^>]*>", "", raw)).strip()
            if unit[0] in {"pre", "svg"}:
                value = re.sub(r"\s+", " ", raw).strip()
            if len(value) >= 55 or unit[0] in {"pre", "svg"}:
                self.units.append({"tag": unit[0], "sha256": sha(value), "preview": value[:100]})
            self.active.remove(unit)


def evidence(path):
    parser = Evidence()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def snapshot(root, output):
    catalog = json.loads((root / "content/catalog.json").read_text())
    pages = []
    for entry in catalog["entries"]:
        if entry["origin"] != "local" or entry["status"] == "draft":
            continue
        source = root / entry["source"]
        doc = evidence(source)
        public = evidence(output / route_path(entry["url"]))
        pages.append({
            "id": entry["id"], "url": entry["url"], "source": entry["source"],
            "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "source_anchors": sorted(set(doc.ids)), "public_anchors": sorted(set(public.ids)),
            "source_links": sorted(set(doc.links)), "markers": sorted(doc.markers),
            "units": doc.units,
            "generated_headings": [
                {"anchor": match[1], "label": re.sub(r"<[^>]+>", "", match[2]).strip()}
                for match in re.finditer(
                    r'<h[23][^>]*id="(reading-section-[^"]+)"[^>]*>(.*?)</h[23]>',
                    (output / route_path(entry["url"])).read_text(), re.S)
            ],
        })
    return {"schema_version": 1, "as_of": "2026-11-14",
            "baseline_commit": json.loads((output / "build-info.json").read_text())["commit"],
            "note": "Immutable pre-integration evidence. Unit hashes cover paragraphs, references, code and diagrams. Titles and generated directory labels may be renumbered; scientific text is retained in place or frozen originals.",
            "pages": pages, "exceptions": []}


def check(root, output=None):
    manifest = root / "docs/organization-audit-20261114.json"
    if not manifest.is_file():
        return []
    audit = json.loads(manifest.read_text())
    errors = []
    exceptions = {(e["id"], e["sha256"]) for e in audit.get("exceptions", [])}
    for page in audit["pages"]:
        path = root / page["source"]
        if not path.is_file():
            errors.append(f"organization: missing source {page['source']}")
            continue
        doc = evidence(path)
        for anchor in set(page["source_anchors"]) - set(doc.ids):
            errors.append(f"organization: {page['id']} lost source anchor #{anchor}")
        for link in set(page["source_links"]) - set(doc.links):
            errors.append(f"organization: {page['id']} lost source URL {link}")
        if Counter(page["markers"]) != Counter(doc.markers):
            errors.append(f"organization: {page['id']} AUTO markers changed")
        retained = Counter(u["sha256"] for u in doc.units)
        baseline = Counter(u["sha256"] for u in page["units"])
        for value in baseline:
            if retained[value] < baseline[value] and (page["id"], value) not in exceptions:
                errors.append(f"organization: {page['id']} missing research unit {value}")
        if output:
            public = evidence(output / route_path(page["url"]))
            for anchor in set(page["public_anchors"]) - set(public.ids):
                errors.append(f"organization: {page['id']} lost public anchor #{anchor}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["snapshot", "check"])
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.command == "snapshot":
        target = args.root / "docs/organization-audit-20261114.json"
        if target.exists():
            raise ValueError("Refusing to overwrite an existing immutable organization baseline")
        target.write_text(json.dumps(snapshot(args.root, args.output), ensure_ascii=False, indent=2) + "\n")
        print(f"Saved baseline: {target}")
    else:
        errors = check(args.root, args.output)
        print("\n".join(errors) if errors else "PASS: organization source units, anchors, sources and markers retained")
        return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
