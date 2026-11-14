"""Refresh learning-review receipts; never rewrite either retention baseline."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "docs/blog-learning-page-review-20261115.md"
LEDGER = ROOT / "docs/organization-changes-20261115.json"
RECEIPTS = ROOT / "docs/content-changes.json"


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
    shared_reason = "Approved learning rework: catalog search and reading destinations follow unique assembled topics; preserve immutable migration baseline."
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
