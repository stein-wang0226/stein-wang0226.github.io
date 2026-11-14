"""Check local management contracts and report catalog scale without writes."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

import yaml

from catalog import load_content
from profile import local_check
from render import ROOT


def inventory(root=ROOT):
    site, entries, publications, _ = load_content(root)
    assets = [p for p in (root / "assets").rglob("*") if p.is_file()]
    return {
        "entries": len(entries),
        "kind": dict(Counter(e["kind"] for e in entries)),
        "status": dict(Counter(e["status"] for e in entries)),
        "topic": dict(Counter(e["topic"] for e in entries)),
        "publications": len(publications),
        "assets_bytes": sum(p.stat().st_size for p in assets),
        "largest_assets": [{"path": p.relative_to(root).as_posix(), "bytes": p.stat().st_size}
                           for p in sorted(assets, key=lambda p: p.stat().st_size,
                                           reverse=True)[:5]],
        "configured_topics": [t["id"] for t in site["topics"]],
    }


def check(root=ROOT):
    errors, checked = [], []
    required = ["AGENTS.md", "docs/project-management.md",
                "docs/content-contract.md", "docs/design-system.md"]
    for name in required:
        if not (root / name).is_file():
            errors.append(f"Missing management document: {name}")
    skills = sorted((root / ".trae/skills").glob("*/SKILL.md"))
    manager = root / ".trae/skills/blog-project-manager/SKILL.md"
    if manager not in skills:
        errors.append("Missing project manager skill")
    for path in skills:
        text = path.read_text(encoding="utf-8")
        match = re.match(r"\A---\n(.*?)\n---\n(.+)\Z", text, re.S)
        if not match:
            errors.append(f"{path}: invalid front matter or empty body")
            continue
        meta = yaml.safe_load(match[1])
        if not isinstance(meta, dict):
            errors.append(f"{path}: front matter must be a mapping")
            continue
        if meta.get("name") != path.parent.name or not re.fullmatch(
                r"[a-z0-9]+(?:-[a-z0-9]+)*", str(meta.get("name", ""))):
            errors.append(f"{path}: name must match the folder")
        if not isinstance(meta.get("description"), str) or not meta["description"].strip():
            errors.append(f"{path}: missing description")
        if path == manager:
            for key in ("name", "description"):
                raw = next((line.split(": ", 1)[1] for line in match[1].splitlines()
                            if line.startswith(key + ": ")), "")
                if not raw or raw.startswith(("'", '"')) or ": " in raw or "<" in raw or ">" in raw:
                    errors.append(f"{path}: invalid unquoted {key}")
            if len(text.splitlines()) >= 500:
                errors.append(f"{path}: move long rules into documents")
        checked.append(path)
        checked.extend(path.parent.glob("references/*.md"))
    checked.extend(root / name for name in required)
    checked += [root / "README.md", root / "docs/maintenance.md",
                root / "docs/github-profile/DEPLOYMENT.md"]
    for path in checked:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for value in re.findall(r"\[[^\]]*\]\(([^)\n]+)\)", text):
            parsed = urlsplit(value)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            target = (path.parent / unquote(parsed.path)).resolve()
            if not target.exists():
                errors.append(f"{path.relative_to(root)}: missing reference {value}")
    profile = local_check(root)
    errors.extend(profile["errors"])
    return {"ok": not errors, "errors": errors, "checked_documents": len(set(checked)),
            "profile": profile, "inventory": inventory(root)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", action="store_true")
    args = parser.parse_args()
    try:
        result = inventory() if args.inventory else check()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return int(result.get("ok") is False)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
