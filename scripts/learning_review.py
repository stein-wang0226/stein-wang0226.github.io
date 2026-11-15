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
CHAIN_REVIEW = ROOT / "docs/blog-update-state-review-20261115.json"
DIAGRAM_REVIEW = ROOT / "docs/blog-diagram-review-20261115.json"
DIAGRAM_BASE_COMMIT = "d1bfb5b82776e1787510003e5dd6a87643cb1a22"


def diagram_pages(entries):
    if not DIAGRAM_REVIEW.exists():
        return {}
    review = json.loads(DIAGRAM_REVIEW.read_text())
    if review["base_commit"] != DIAGRAM_BASE_COMMIT:
        raise ValueError("diagram review base commit mismatch")
    sources = {e["id"]: e["source"] for e in entries}
    topics = {e["id"]: e["topic"] for e in entries}
    pages, seen_sources = {}, set()
    for page in review["pages"]:
        identifier, source = page["id"], page["source"]
        if identifier in pages or source in seen_sources:
            raise ValueError(f"diagram review duplicate ID/source: {identifier}")
        if sources.get(identifier) != source:
            raise ValueError(f"diagram review source mismatch: {identifier}")
        topic = topics[identifier]
        module = ("architecture-inference" if topic in {"llm-foundations", "inference"}
                  else "training-data" if topic in {"training", "data"}
                  else "agent-multimodal-diffusion")
        if page["module"] != module:
            raise ValueError(f"diagram review module mismatch: {identifier}")
        before, after = page["sha256_before"], page["sha256_after"]
        for digest in (before, after):
            if not isinstance(digest, str) or len(digest) != 64 or any(
                    c not in "0123456789abcdef" for c in digest):
                raise ValueError(f"diagram review invalid SHA: {identifier}")
        if type(page["changed"]) is not bool or page["changed"] != (before != after):
            raise ValueError(f"diagram review changed/SHA mismatch: {identifier}")
        if not page["reason"] or not page["examined"]:
            raise ValueError(f"diagram review missing scoped judgment: {identifier}")
        pages[identifier] = page
        seen_sources.add(source)
    if set(pages) != set(sources):
        raise ValueError("diagram review must cover each local source exactly once")
    return pages


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
    if CHAIN_REVIEW.exists():
        sources = {e["id"]: e["source"] for e in entries}
        seen = set()
        for page in json.loads(CHAIN_REVIEW.read_text())["pages"]:
            identifier = page["id"]
            if identifier in seen or sources.get(identifier) != page["source"]:
                raise ValueError(f"update/state review duplicate or source mismatch: {identifier}")
            seen.add(identifier)
            if page["changed"]:
                reasons[identifier] += f" 更新与状态链路复查：{page['reason']}。"
    for identifier, page in diagram_pages(entries).items():
        if page["changed"]:
            reasons[identifier] += f" 图示补充审阅：{page['reason']}。"
    return entries, reasons


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["refresh", "check"])
    args = parser.parse_args()
    entries, reasons = derive()
    ledger = json.loads(LEDGER.read_text())
    receipts = json.loads(RECEIPTS.read_text())
    diagrams = diagram_pages(entries)
    by_id = {p["id"]: p for p in ledger["pages"]}
    by_source = {p["source"]: p for p in receipts["changes"]}
    errors = []
    if diagrams:
        if len(by_id) != len(ledger["pages"]) or len(by_source) != len(receipts["changes"]):
            raise ValueError("duplicate ledger/receipt ID or source")
        # A diagram refresh is not permission to absorb unrelated stale changes.
        for entry in entries:
            identifier, source = entry["id"], entry["source"]
            review = diagrams[identifier]
            digest = hashlib.sha256((ROOT / source).read_bytes()).hexdigest()
            if digest != review["sha256_after"]:
                errors.append(f"{identifier}: diagram review current SHA mismatch")
            expected = reasons[identifier]
            historical = (expected.removesuffix(f" 图示补充审阅：{review['reason']}。")
                          if review["changed"] else expected)
            allowed_reasons = {expected, historical} if args.command == "refresh" else {expected}
            page, receipt = by_id.get(identifier, {}), by_source.get(source, {})
            if page.get("source") != source or page.get("reason") not in allowed_reasons:
                errors.append(f"{identifier}: unexpected ledger source/reason")
            allowed_shas = ({review["sha256_before"], digest}
                            if args.command == "refresh" else {digest})
            if receipt.get("sha256") not in allowed_shas or receipt.get("reason") not in allowed_reasons:
                errors.append(f"{identifier}: unexpected receipt SHA/reason")
        for shared in ("assets/site/catalog.js", "assets/site/reading.css"):
            digest = hashlib.sha256((ROOT / shared).read_bytes()).hexdigest()
            if by_source.get(shared, {}).get("sha256") != digest:
                errors.append(f"{shared}: stale shared receipt; diagram refresh will not repair it")
        if errors:
            print("\n".join(errors))
            return True
    for entry in entries:
        identifier, source = entry["id"], entry["source"]
        digest = hashlib.sha256((ROOT / source).read_bytes()).hexdigest()
        page = by_id[identifier]
        if args.command == "refresh":
            if diagrams and not diagrams[identifier]["changed"]:
                continue
            page["reason"] = reasons[identifier]
            receipt = by_source.get(source)
            if receipt is None:
                receipt = {"source": source}
                receipts["changes"].append(receipt)
            elif not diagrams and receipt.get("reason") != reasons[identifier]:
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
    if args.command == "refresh" and not diagrams:
        receipt = by_source[shared]
        receipt.setdefault("prior_reason", receipt.get("reason", ""))
        receipt.update(sha256=shared_sha, reason=shared_reason)
    elif by_source[shared]["sha256"] != shared_sha:
        errors.append(f"{shared}: stale shared navigation receipt")
    if args.command == "refresh":
        for path, value in ((LEDGER, ledger), (RECEIPTS, receipts)):
            text = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
            if path.read_text() != text:
                path.write_text(text)
    print("\n".join(errors) if errors else
          f"PASS: {len(entries)} unique reviewed sources; exact current SHA/reasons; baselines untouched")
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
