#!/usr/bin/env python3
"""Validate one external build artifact, its content contract and public links."""
import sys
sys.dont_write_bytecode = True

import argparse
import hashlib
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import importlib.util
from urllib.parse import unquote, urlsplit

from catalog import load_content
from render import DEFAULT_OUTPUT, ROOT, external_output, input_digest, public_file, route_path

FRONTIER_TOPICS = ("models", "frontier", "arch", "optimizer", "agent", "rl", "opd",
                   "training", "bench", "protein", "changelog")


class Document(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path, self.ids, self.links, self.errors = path, set(), [], []
        self.nav, self.title, self.base = 0, 0, None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            if attrs["id"] in self.ids:
                self.errors.append(f"duplicate id #{attrs['id']}")
            self.ids.add(attrs["id"])
        if tag == "a" and attrs.get("name"):
            self.ids.add(attrs["name"])
        self.title += tag == "title"
        self.nav += tag == "nav" and attrs.get("aria-label") == "主导航"
        if tag == "base":
            self.base = attrs.get("href")
        for key in ("href", "src", "poster"):
            if attrs.get(key):
                self.links.append(attrs[key])
        if tag == "object" and attrs.get("data"):
            self.links.append(attrs["data"])
        if attrs.get("srcset"):
            self.links.extend(part.strip().split()[0] for part in attrs["srcset"].split(",")
                              if part.strip())

    handle_startendtag = handle_starttag


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(output=DEFAULT_OUTPUT, root=ROOT, content=None):
    root = Path(root).resolve()
    output = external_output(output, root)
    site, entries, publications, redirects = content or load_content(root)
    errors = []
    if not output.is_dir():
        raise ValueError(f"Build artifact missing: {output}; run scripts/build.py first")
    info_path = output / "build-info.json"
    if not info_path.is_file():
        raise ValueError(f"Missing artifact manifest: {info_path}")
    try:
        info = json.loads(info_path.read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        raise ValueError(f"Invalid artifact manifest: {exc}") from exc
    if (info.get("schema_version") != 1 or not isinstance(info.get("dirty"), bool)
            or not re.fullmatch(r"[0-9a-f]{40,64}", str(info.get("commit", "")))):
        errors.append("build-info.json: invalid commit/dirty/schema metadata")
    if info.get("input_digest") != input_digest(root):
        errors.append("build-info.json: artifact is stale for current authoritative inputs; rebuild")
    files = info.get("files")
    if not isinstance(files, dict):
        raise ValueError("build-info.json: missing files manifest")
    actual = set()
    for path in sorted(output.rglob("*")):
        relative = path.relative_to(output).as_posix()
        if path.is_symlink():
            errors.append(f"{relative}: symbolic links are not publishable")
        elif path.is_file():
            actual.add(relative)
            if not public_file(relative):
                errors.append(f"{relative}: private/source/cache or non-allowlisted file")
    expected = set(files) | {"build-info.json"}
    for path in sorted(actual - expected):
        errors.append(f"{path}: unregistered/stale output file")
    for path in sorted(expected - actual):
        errors.append(f"{path}: missing manifest file")
    for relative, expected_hash in files.items():
        if not public_file(relative) or route_path(relative) != relative:
            errors.append(f"build-info.json: unsafe manifest path {relative}")
            continue
        path = output / relative
        if path.is_file() and not path.is_symlink() and digest(path) != expected_hash:
            errors.append(f"{relative}: content differs from artifact manifest")

    docs = {}
    redirect_paths = {route_path(item["from"]) for item in redirects["redirects"]}
    for path in sorted(output.rglob("*.html")):
        relative = path.relative_to(output).as_posix()
        doc = Document(path)
        text = path.read_text(encoding="utf-8")
        doc.feed(text)
        docs[path.resolve()] = doc
        errors.extend(f"{relative}: {error}" for error in doc.errors)
        if doc.title != 1:
            errors.append(f"{relative}: expected exactly one title")
        if relative in redirect_paths:
            if "location.replace(" not in text:
                errors.append(f"{relative}: missing redirect behavior")
        elif doc.nav != 1:
            errors.append(f"{relative}: expected one shared navigation")
        if re.search(r"\{%\s*(include|for|if)\b|\{\{[^}]+\}\}", text):
            errors.append(f"{relative}: unrendered template/Jekyll markup")

    def check_link(path, link, base=None):
        url = urlsplit(link)
        if url.scheme or url.netloc:
            return
        local = unquote(url.path)
        if base and not local.startswith("/"):
            base_url = urlsplit(base)
            if base_url.scheme or base_url.netloc:
                return
            parent = output / base_url.path.lstrip("/")
        else:
            parent = path.parent
        target = ((output / local.lstrip("/") if local.startswith("/") else parent / local)
                  if local else path)
        if target.is_dir() or (not target.exists() and not target.suffix):
            target /= "index.html"
        target = target.resolve()
        label = path.relative_to(output).as_posix()
        if not target.is_relative_to(output):
            errors.append(f"{label}: path escapes site: {link}")
        elif not target.is_file():
            errors.append(f"{label}: missing target {link}")
        elif url.fragment and target in docs and unquote(url.fragment) not in docs[target].ids:
            errors.append(f"{label}: missing anchor {link}")
        elif url.fragment and target.suffix == ".html" and target not in docs:
            errors.append(f"{label}: target HTML was not parsed: {link}")

    for path, doc in docs.items():
        for link in doc.links:
            check_link(path, link, doc.base)
    for path in sorted(output.rglob("*.css")):
        for match in re.finditer(r"url\(\s*(['\"]?)(.*?)\1\s*\)", path.read_text(encoding="utf-8")):
            check_link(path, match[2])
    for entry in entries:
        if entry["origin"] != "local":
            continue
        target = output / route_path(entry["url"])
        if entry["status"] == "draft":
            if target.exists():
                errors.append(f"Draft leaked into artifact: {entry['id']}")
        elif not target.is_file():
            errors.append(f"Missing catalog output: {entry['id']} ({entry['url']})")
    for publication in publications:
        if not (output / route_path(publication["url"])).is_file():
            errors.append(f"Missing publication: {publication['slug']}")
    for item in site["navigation"]:
        check_link(output / "index.html", item["url"])
    for item in redirects["redirects"]:
        check_link(output / route_path(item["from"]), item["to"])
        if route_path(urlsplit(item["to"]).path) in redirect_paths:
            errors.append(f"Redirect {item['from']}: target must be a final public route, not another redirect")
    for item in redirects.get("copies", []):
        original, alias = output / route_path(item["to"]), output / route_path(item["from"])
        if not original.is_file() or not alias.is_file() or digest(original) != digest(alias):
            errors.append(f"Compatibility asset copy differs: {item['from']}")
    frontier_entry = next((e for e in entries if e["id"] == "llm-frontier-2026"), None)
    if frontier_entry and frontier_entry["status"] != "draft":
        frontier_path = output / route_path(frontier_entry["url"])
        if frontier_path.is_file():
            frontier = frontier_path.read_text(encoding="utf-8")
            for topic in FRONTIER_TOPICS:
                if frontier.count(f"<!-- AUTO:INSERT:{topic} -->") != 1:
                    errors.append(f"Frontier: missing or repeated update marker {topic}")
            if not re.search(r'\bid=["\']last-updated["\']', frontier):
                errors.append("Frontier: missing last-updated")
            try:
                guard_path = root / ".automation/check-frontier.py"
                spec = importlib.util.spec_from_file_location("frontier_guard", guard_path)
                guard = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(guard)
                guard.document(frontier_path)
            except (ValueError, OSError) as exc:
                errors.append(f"Frontier: incoherent source/entry/changelog dates or markers: {exc}")

    def check_data(value, path):
        if isinstance(value, dict):
            for key, child in value.items():
                if key in {"url", "href"} and isinstance(child, str):
                    check_link(path, child)
                elif key == "source" and isinstance(child, str) and child.startswith("content/"):
                    errors.append(f"{path.relative_to(output)}: private content source in public data")
                else:
                    check_data(child, path)
        elif isinstance(value, list):
            for child in value:
                check_data(child, path)
    for path in sorted(output.rglob("*.json")):
        if path == info_path:
            continue
        try:
            check_data(json.loads(path.read_text(encoding="utf-8")), path)
        except ValueError as exc:
            errors.append(f"{path.relative_to(output)}: invalid JSON: {exc}")
    return errors, len(docs)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", "--site", type=Path, default=DEFAULT_OUTPUT,
                        help="Existing external artifact (default: /tmp/my-blogs-site-build)")
    args = parser.parse_args(argv)
    try:
        errors, count = validate(args.output)
    except (ValueError, OSError) as exc:
        print(f"FAILED: {exc}", file=sys.stderr)
        return 1
    if errors:
        print("\n".join(errors), file=sys.stderr)
        print(f"FAILED: {len(errors)} issues across {count} pages.", file=sys.stderr)
        return 1
    print(f"PASS: {count} HTML pages; catalog, links, anchors, navigation, publications, "
          "frontier markers and artifact allowlist.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
