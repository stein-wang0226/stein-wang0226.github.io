#!/usr/bin/env python3
"""Create an ordinary Markdown article and a draft catalog record without overwriting."""
import sys
sys.dont_write_bytecode = True
import argparse
import json
from pathlib import Path
import re
from string import Template

from catalog import load_content
from render import ROOT


def create(identifier, title, topic, kind="principles", root=ROOT):
    root = Path(root).resolve()
    site, entries, _, _ = load_content(root)
    if not isinstance(title, str) or not title.strip():
        raise ValueError("title must be nonempty")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", identifier):
        raise ValueError("id must be a lowercase slug")
    folder = root / "content/posts" / identifier
    if any(e["id"] == identifier for e in entries) or folder.exists():
        raise ValueError(f"ID or directory already exists: {identifier}; nothing overwritten")
    if topic not in {t["id"] for t in site["topics"]}:
        raise ValueError(f"Unknown topic: {topic}")
    if kind not in {t["id"] for t in site["types"]}:
        raise ValueError(f"Unknown type: {kind}")
    url = f"/{identifier}.html"
    if any(e["url"] == url for e in entries):
        raise ValueError(f"Output URL already exists: {url}")
    catalog_path = root / "content/catalog.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    source = f"content/posts/{identifier}/index.md"
    catalog["entries"].append({
        "id": identifier, "kind": "post", "title": title, "summary": "待补充摘要",
        "source": source, "url": url, "topic": topic, "type": kind, "tags": [],
        "origin": "local", "status": "draft", "review_status": "unreviewed",
        "updated": None, "updated_source": None, "series": None, "order": None,
        "featured": False, "related": [],
    })
    # Use JSON quoting inside YAML so titles containing quotes/newlines remain safe.
    title_yaml = json.dumps(title, ensure_ascii=False)[1:-1]
    body = Template((root / "templates/post.md").read_text(encoding="utf-8")).substitute(title=title_yaml)
    folder.mkdir()
    (root / source).write_text(body, encoding="utf-8")
    catalog_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return source


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("id")
    parser.add_argument("--title", required=True)
    parser.add_argument("--topic", required=True)
    parser.add_argument("--type", default="principles")
    args = parser.parse_args()
    try:
        print("Created draft: " + create(args.id, args.title, args.topic, args.type))
    except (ValueError, OSError) as exc:
        print(f"FAILED: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
