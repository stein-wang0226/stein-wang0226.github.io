"""Refresh learning-review receipts; never rewrite either retention baseline."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "docs/blog-learning-page-review-20261115.md"
LEDGER = ROOT / "docs/organization-changes-20261115.json"
RECEIPTS = ROOT / "docs/content-changes.json"
SYMBOL_REVIEW = ROOT / "docs/blog-symbol-review-20261115.json"
STRUCTURE_REVIEW = ROOT / "docs/blog-structure-review-20261115.json"
CURRICULUM_REVIEW = ROOT / "docs/blog-curriculum-review-20261115.json"
FORWARD_REVIEW = ROOT / "docs/blog-forward-integration-20261115.json"
EXAMPLE_REVIEW = ROOT / "docs/blog-worked-example-review-20261115.json"


def derive():
    catalog = json.loads((ROOT / "content/catalog.json").read_text())["entries"]
    entries = [e for e in catalog if e["origin"] == "local"]
    rows = []
    for line in REVIEW.read_text().splitlines():
        if not line.startswith("| "):
            continue
        cells = [c.strip() for c in line.strip("|").strip().split(" | ")]
        if len(cells) == 4 and cells[0] not in {"唯一源", "---"}:
            rows.append(cells)
    reasons = {}
    for label, judgment, mechanism, retention in rows:
        found = [e for e in entries if label == e["id"] or
                 e["source"].removesuffix(".html").removesuffix(".md").endswith("/" + label)]
        if len(found) != 1:
            raise ValueError(f"review row {label!r}: expected one source, found {len(found)}")
        entry = found[0]
        if entry["id"] in reasons:
            raise ValueError(f"duplicate review row: {entry['id']}")
        reasons[entry["id"]] = f"逐页审阅：{judgment}。原理与算例：{mechanism}。精简与证据：{retention}。"
    if set(reasons) != {e["id"] for e in entries}:
        raise ValueError(f"missing review rows: {sorted({e['id'] for e in entries} - set(reasons))}")
    # Later reviews supplement the frozen learning-rework evidence; they do not
    # relabel its browser results as validation of newly edited content.
    if SYMBOL_REVIEW.exists():
        pages = json.loads(SYMBOL_REVIEW.read_text())["pages"]
        if len(pages) != len(entries) or {p["id"] for p in pages} != set(reasons):
            raise ValueError("symbol review must cover each local source exactly once")
        sources = {e["id"]: e["source"] for e in entries}
        for page in pages:
            if page["source"] != sources[page["id"]]:
                raise ValueError(f"symbol review source mismatch: {page['id']}")
            if page["changed"]:
                reasons[page["id"]] += f" 符号补充审阅：{page['reason']}。"
    if STRUCTURE_REVIEW.exists():
        sources = {e["id"]: e["source"] for e in entries}
        seen = set()
        for page in json.loads(STRUCTURE_REVIEW.read_text())["pages"]:
            identifier = page["id"]
            if identifier in seen or sources.get(identifier) != page["source"]:
                raise ValueError(f"structure review duplicate or source mismatch: {identifier}")
            seen.add(identifier)
            reasons[identifier] += f" 结构补充审阅：{page['reason']}。"
    if CURRICULUM_REVIEW.exists():
        sources = {e["id"]: e["source"] for e in entries}
        pages = json.loads(CURRICULUM_REVIEW.read_text())["pages"]
        if len(pages) != len(entries) or {p["id"] for p in pages} != set(sources):
            raise ValueError("curriculum review must cover each local source exactly once")
        for page in pages:
            if sources[page["id"]] != page["source"]:
                raise ValueError(f"curriculum review source mismatch: {page['id']}")
            if page["changed"]:
                reasons[page["id"]] += f" 分类与课程复查：{page['reason']}。"
    if FORWARD_REVIEW.exists():
        sources = {e["id"]: e["source"] for e in entries}
        seen = set()
        for page in json.loads(FORWARD_REVIEW.read_text())["pages"]:
            identifier = page["id"]
            if identifier in seen or sources.get(identifier) != page["source"]:
                raise ValueError(f"forward review duplicate or source mismatch: {identifier}")
            seen.add(identifier)
            reasons[identifier] += f" 完整算例与主题整合：{page['reason']}。"
    if EXAMPLE_REVIEW.exists():
        sources = {e["id"]: e["source"] for e in entries}
        pages = json.loads(EXAMPLE_REVIEW.read_text())["pages"]
        if len(pages) != len(entries) or {p["id"] for p in pages} != set(sources):
            raise ValueError("worked-example review must cover each local source exactly once")
        for page in pages:
            if sources[page["id"]] != page["source"]:
                raise ValueError(f"worked-example review source mismatch: {page['id']}")
            if page["changed"]:
                reasons[page["id"]] += f" 计算链路补充审阅：{page['reason']}。"
    return entries, reasons


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["refresh", "check"])
    args = parser.parse_args()
    entries, reasons = derive()
    ledger = json.loads(LEDGER.read_text())
    receipts = json.loads(RECEIPTS.read_text())
    by_id = {p["id"]: p for p in ledger["pages"]}
    by_source = {p["source"]: p for p in receipts["changes"]}
    errors = []
    for entry in entries:
        identifier, source = entry["id"], entry["source"]
        digest = hashlib.sha256((ROOT / source).read_bytes()).hexdigest()
        page = by_id[identifier]
        if args.command == "refresh":
            page["reason"] = reasons[identifier]
            receipt = by_source.get(source)
            if receipt is None:
                receipt = {"source": source}
                receipts["changes"].append(receipt)
            elif receipt.get("reason") != reasons[identifier]:
                receipt.setdefault("prior_reason", receipt.get("reason", ""))
            receipt.update(sha256=digest, reason=reasons[identifier])
        else:
            if page["reason"] != reasons[identifier]:
                errors.append(f"{identifier}: stale ledger review reason")
            receipt = by_source.get(source, {})
            if receipt.get("sha256") != digest or receipt.get("reason") != reasons[identifier]:
                errors.append(f"{identifier}: stale receipt SHA/reason")
    shared = "assets/site/catalog.js"
    shared_sha = hashlib.sha256((ROOT / shared).read_bytes()).hexdigest()
    shared_reason = "Approved learning rework and taxonomy integration: preserve assembled reading destinations, filter by chapter and secondary topics, and map legacy training categories; preserve immutable migration baseline."
    if args.command == "refresh":
        receipt = by_source[shared]
        receipt.setdefault("prior_reason", receipt.get("reason", ""))
        receipt.update(sha256=shared_sha, reason=shared_reason)
    elif by_source[shared]["sha256"] != shared_sha:
        errors.append(f"{shared}: stale shared navigation receipt")
    if args.command == "refresh":
        LEDGER.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n")
        RECEIPTS.write_text(json.dumps(receipts, ensure_ascii=False, indent=2) + "\n")
    print("\n".join(errors) if errors else
          f"PASS: {len(entries)} unique reviewed sources; exact current SHA/reasons; baselines untouched")
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
