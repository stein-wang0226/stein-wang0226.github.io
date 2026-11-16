"""Refresh learning-review receipts; never rewrite either retention baseline."""
import argparse
from copy import deepcopy
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess

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
CONTINUITY_REVIEW = ROOT / "docs/blog-continuity-review-20261116.json"
CONTINUITY_BASE_COMMIT = "80148053b623c4b6e1fc5a1a062f1113e5039443"
IMMUTABLE_BASELINES = {
    "docs/content-migration-manifest.json":
        "11361df792389fc3c516eebbdbe874911a72f9660c29c630fb7b6442cd01258a",
    "docs/organization-audit-20261114.json":
        "2b80203ef8ae46a7e3b9bf8ed40b3766d6359caa1c67663050834985f0012407",
}


def module_for(topic):
    return ("architecture-inference" if topic in {"llm-foundations", "inference"}
            else "training-data" if topic in {"training", "data"}
            else "agent-multimodal-diffusion")


def git_bytes(commit, source):
    result = subprocess.run(
        ["git", "show", f"{commit}:{source}"], cwd=ROOT, capture_output=True)
    if result.returncode:
        raise ValueError(f"cannot read git base bytes: {commit}:{source}")
    return result.stdout


def git_base_available():
    result = subprocess.run(
        ["git", "cat-file", "-e", f"{CONTINUITY_BASE_COMMIT}^{{commit}}"],
        cwd=ROOT, capture_output=True)
    if result.returncode == 0:
        return True
    shallow = subprocess.run(
        ["git", "rev-parse", "--is-shallow-repository"], cwd=ROOT, capture_output=True)
    if shallow.returncode == 0 and shallow.stdout.strip() == b"true":
        return False
    raise ValueError("continuity Git base unavailable outside a shallow clone")


def sha256(value):
    return hashlib.sha256(value).hexdigest()


def scoped_text(value, label):
    generic = {"reviewed", "unchanged", "no change", "pass",
               "已审阅", "无需修改", "未修改", "检查通过"}
    if not isinstance(value, str) or not value.strip() or value.strip().lower() in generic:
        raise ValueError(f"continuity review missing specific {label}")


class SourceAnchors(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.heading_tag = None
        self.heading_parts = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "a" and attrs.get("name"):
            self.ids.add(attrs["name"])
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.heading_tag = tag
            self.heading_parts = []

    def handle_data(self, data):
        if self.heading_tag is not None:
            self.heading_parts.append(data)

    def handle_endtag(self, tag):
        if tag == self.heading_tag:
            heading = " ".join("".join(self.heading_parts).split())
            if heading:
                self.ids.add("heading:" + heading)
            self.heading_tag = None
            self.heading_parts = []

    handle_startendtag = handle_starttag


def source_anchors(raw, source):
    text = raw.decode("utf-8")
    if source.endswith(".md"):
        from render import md
        front_matter = re.match(r"\A---\s*\n(.*?)\n---(?:\s*\n|$)(.*)\Z", text, re.S)
        text = md(front_matter[2].strip() if front_matter else text)
    parser = SourceAnchors()
    parser.feed(text)
    return parser.ids


def has_source_anchor(value, anchors):
    return isinstance(value, str) and value.removeprefix("#") in anchors


def continuity_pages(entries, diagrams, verify_git=True):
    if not CONTINUITY_REVIEW.exists():
        return {}
    review = json.loads(CONTINUITY_REVIEW.read_text())
    base = review.get("base_commit")
    if base != CONTINUITY_BASE_COMMIT:
        raise ValueError("continuity review base commit mismatch")
    for source, expected in review.get("frozen_files", {}).items():
        raw = (ROOT / source).read_bytes()
        if sha256(raw) != expected or (verify_git and raw != git_bytes(base, source)):
            raise ValueError(f"continuity review frozen file SHA mismatch: {source}")
    # Historical judgments are frozen, not reinterpreted against current prose.
    history = (REVIEW, SYMBOL_REVIEW, STRUCTURE_REVIEW, CURRICULUM_REVIEW,
               FORWARD_REVIEW, EXAMPLE_REVIEW, CHAIN_REVIEW, DIAGRAM_REVIEW)
    for path in history:
        source = path.relative_to(ROOT).as_posix()
        raw = path.read_bytes()
        recorded = review.get("frozen_files", {}).get(source)
        if recorded is not None and recorded != sha256(raw):
            raise ValueError(f"continuity review frozen file SHA mismatch: {source}")
        if verify_git and raw != git_bytes(base, source):
            raise ValueError(f"continuity review changed frozen history: {source}")
        if not verify_git and recorded is None:
            raise ValueError(f"continuity shallow check missing frozen file SHA: {source}")
    for source, expected in IMMUTABLE_BASELINES.items():
        if sha256((ROOT / source).read_bytes()) != expected or (verify_git and sha256(
                git_bytes(base, source)) != expected):
            raise ValueError(f"continuity review immutable baseline mismatch: {source}")
    base_entries = entries
    if verify_git:
        baseline = json.loads(git_bytes(base, "content/catalog.json"))["entries"]
        base_entries = [e for e in baseline if e["origin"] == "local"]
    sources = {e["id"]: e["source"] for e in entries}
    if (len(entries) != 74 or len(sources) != len(entries)
            or len(set(sources.values())) != len(entries)
            or sources != {e["id"]: e["source"] for e in base_entries}
            or set(diagrams) != set(sources)):
        raise ValueError("continuity review requires the 74 unique base local sources")
    base_topics = {e["id"]: e["topic"] for e in base_entries}
    if any(e["topic"] != base_topics[e["id"]] for e in entries):
        raise ValueError("continuity review catalog topic differs from base")
    pages, seen_sources = {}, set()
    if not isinstance(review.get("pages"), list):
        raise ValueError("continuity review pages must be a list")
    for page in review["pages"]:
        identifier, source = page["id"], page["source"]
        if identifier in pages or source in seen_sources:
            raise ValueError(f"continuity review duplicate ID/source: {identifier}")
        if sources.get(identifier) != source:
            raise ValueError(f"continuity review source mismatch: {identifier}")
        if page.get("module") != module_for(base_topics[identifier]):
            raise ValueError(f"continuity review module mismatch: {identifier}")
        before, after = page["sha256_before"], page["sha256_after"]
        if any(not isinstance(s, str) or not re.fullmatch(r"[0-9a-f]{64}", s)
               for s in (before, after)):
            raise ValueError(f"continuity review invalid SHA: {identifier}")
        current_raw = (ROOT / source).read_bytes()
        if (before != diagrams[identifier]["sha256_after"]
                or (verify_git and before != sha256(git_bytes(base, source)))):
            raise ValueError(f"{identifier}: frozen diagram/base/continuity before SHA mismatch")
        if after != sha256(current_raw):
            raise ValueError(f"{identifier}: continuity review current SHA mismatch")
        if type(page["changed"]) is not bool or page["changed"] != (before != after):
            raise ValueError(f"continuity review changed/SHA mismatch: {identifier}")
        scoped_text(page.get("reason"), f"reason: {identifier}")
        scoped_text(page.get("evidence_boundary"), f"evidence boundary: {identifier}")
        anchors = source_anchors(current_raw, source)
        if not isinstance(page.get("examined"), list) or not page["examined"]:
            raise ValueError(f"continuity review missing examined positions: {identifier}")
        for item in page["examined"]:
            if not isinstance(item, dict) or not has_source_anchor(item.get("anchor"), anchors):
                raise ValueError(f"continuity review examined anchor missing: {identifier}")
            scoped_text(item.get("judgment"), f"examined judgment: {identifier}")
        changes = page.get("changes")
        if not isinstance(changes, list) or bool(changes) != page["changed"]:
            raise ValueError(f"continuity review changed/changes mismatch: {identifier}")
        for change in changes:
            if not isinstance(change, dict) or not has_source_anchor(change.get("anchor"), anchors):
                raise ValueError(f"continuity review change anchor missing: {identifier}")
            for key in ("kind", "summary"):
                scoped_text(change.get(key), f"change {key}: {identifier}")
            assumptions = change.get("assumptions")
            if isinstance(assumptions, list):
                if not assumptions:
                    raise ValueError(f"continuity review missing assumptions: {identifier}")
                for assumption in assumptions:
                    scoped_text(assumption, f"assumption: {identifier}")
            else:
                scoped_text(assumptions, f"assumptions: {identifier}")
            if not isinstance(change.get("checks"), list):
                raise ValueError(f"continuity review checks must be a list: {identifier}")
        pages[identifier] = page
        seen_sources.add(source)
    if set(pages) != set(sources):
        raise ValueError("continuity review must cover each local source exactly once")
    return pages


def continuity_receipts(entries, reasons, pages, ledger, receipts, command, verify_git=True):
    if not verify_git:
        if command != "check":
            raise ValueError("continuity refresh requires actual Git base bytes")
        review = json.loads(CONTINUITY_REVIEW.read_text())
        files = review.get("integrated_files", {})
        for path in (LEDGER, RECEIPTS, ROOT / "content/catalog.json"):
            source = path.relative_to(ROOT).as_posix()
            if files.get(source) != sha256(path.read_bytes()):
                raise ValueError(f"continuity shallow check integrated file SHA mismatch: {source}")
        by_id = {p["id"]: p for p in ledger["pages"]}
        by_source = {p["source"]: p for p in receipts["changes"]}
        if (len(by_id) != len(ledger["pages"]) or set(by_id) != set(pages)
                or len(by_source) != len(receipts["changes"])):
            raise ValueError("continuity shallow check duplicate/missing ledger/receipt")
        for entry in entries:
            identifier, source = entry["id"], entry["source"]
            review_page = pages[identifier]
            reason = reasons[identifier]
            if review_page["changed"]:
                reason += f" 讲解连贯性续轮审阅：{review_page['reason']}"
            page, receipt = by_id[identifier], by_source.get(source, {})
            if (page.get("source") != source or page.get("reason") != reason
                    or receipt.get("reason") != reason
                    or receipt.get("sha256") != review_page["sha256_after"]):
                raise ValueError(f"{identifier}: continuity shallow check stale SHA/reason")
        local_sources = {e["source"] for e in entries}
        for receipt in receipts["changes"]:
            source = receipt["source"]
            if source not in local_sources and sha256(
                    (ROOT / source).read_bytes()) != receipt["sha256"]:
                raise ValueError(f"{source}: stale unrelated receipt; continuity will not repair it")
        return ledger, receipts
    base = CONTINUITY_BASE_COMMIT
    base_ledger = json.loads(git_bytes(base, LEDGER.relative_to(ROOT).as_posix()))
    base_receipts = json.loads(git_bytes(base, RECEIPTS.relative_to(ROOT).as_posix()))
    expected_ledger, expected_receipts = deepcopy(base_ledger), deepcopy(base_receipts)
    by_id = {p["id"]: p for p in expected_ledger["pages"]}
    by_source = {p["source"]: p for p in expected_receipts["changes"]}
    if (len(by_id) != len(expected_ledger["pages"])
            or len(by_source) != len(expected_receipts["changes"])
            or set(by_id) != set(pages)):
        raise ValueError("continuity review duplicate or missing base ledger/receipt")
    for entry in entries:
        identifier, source = entry["id"], entry["source"]
        page, receipt = by_id[identifier], by_source.get(source, {})
        review = pages[identifier]
        if (page["source"] != source or page["reason"] != reasons[identifier]
                or receipt.get("reason") != reasons[identifier]
                or receipt.get("sha256") != review["sha256_before"]):
            raise ValueError(f"{identifier}: continuity base ledger/receipt mismatch")
        if review["changed"]:
            reason = reasons[identifier] + f" 讲解连贯性续轮审阅：{review['reason']}"
            page.setdefault("prior_reason", page["reason"])
            receipt.setdefault("prior_reason", receipt["reason"])
            page["reason"] = receipt["reason"] = reason
            receipt["sha256"] = review["sha256_after"]
    # Only exact old/new records are allowed. In particular, refresh cannot
    # repair unrelated receipts or alter retention units and prior reasons.
    for actual, old, expected, key in (
            (ledger, base_ledger, expected_ledger, "pages"),
            (receipts, base_receipts, expected_receipts, "changes")):
        if ({k: v for k, v in actual.items() if k != key}
                != {k: v for k, v in old.items() if k != key}
                or len(actual[key]) != len(old[key])):
            raise ValueError(f"continuity review unexpected {key} metadata/coverage")
        for current, previous, updated in zip(actual[key], old[key], expected[key]):
            if current != updated and (command != "refresh" or current != previous):
                raise ValueError(f"continuity review unexpected {key} record: "
                                 f"{previous.get('id', previous.get('source'))}")
    local_sources = {e["source"] for e in entries}
    for receipt in base_receipts["changes"]:
        source = receipt["source"]
        if source not in local_sources and sha256(
                (ROOT / source).read_bytes()) != receipt["sha256"]:
            raise ValueError(f"{source}: stale unrelated receipt; continuity will not repair it")
    catalog = json.loads((ROOT / "content/catalog.json").read_text())
    base_catalog = json.loads(git_bytes(base, "content/catalog.json"))
    permitted_catalog = deepcopy(base_catalog)
    current_entries = {e["id"]: e for e in catalog["entries"]}
    for entry in permitted_catalog["entries"]:
        if pages.get(entry["id"], {}).get("changed"):
            for key in ("summary", "updated"):
                if key in current_entries[entry["id"]]:
                    entry[key] = current_entries[entry["id"]][key]
    if catalog != permitted_catalog:
        raise ValueError("continuity review unrelated catalog change")
    return expected_ledger, expected_receipts


def receipt_bytes(path, value):
    raw = path.read_bytes()
    original = json.loads(raw)
    if original == value:
        return raw
    key = "pages" if path == LEDGER else "changes"
    if ({k: v for k, v in original.items() if k != key}
            != {k: v for k, v in value.items() if k != key}
            or len(original[key]) != len(value[key])):
        raise ValueError("continuity receipt serialization requires scoped record updates")
    text, decoder = raw.decode("utf-8"), json.JSONDecoder()

    def skip_space(index):
        while index < len(text) and text[index].isspace():
            index += 1
        return index

    # Decode top-level values to locate the record array without rewriting
    # surrounding metadata, separators or unchanged record bytes.
    cursor = skip_space(text.index("{") + 1)
    while True:
        field, cursor = decoder.raw_decode(text, cursor)
        cursor = skip_space(cursor)
        if text[cursor] != ":":
            raise ValueError("invalid receipt object separator")
        cursor = skip_space(cursor + 1)
        if field == key:
            if text[cursor] != "[":
                raise ValueError("invalid receipt record array")
            cursor += 1
            break
        _, cursor = decoder.raw_decode(text, cursor)
        cursor = skip_space(cursor)
        if text[cursor] != ",":
            raise ValueError("missing receipt record array")
        cursor = skip_space(cursor + 1)
    replacements = []
    for previous, current in zip(original[key], value[key]):
        start = skip_space(cursor)
        record, cursor = decoder.raw_decode(text, start)
        if record != previous:
            raise ValueError("receipt record order mismatch")
        if previous != current:
            indent = start - text.rfind("\n", 0, start) - 1
            rendered = json.dumps(current, ensure_ascii=False, indent=2)
            replacements.append((start, cursor, rendered.replace("\n", "\n" + " " * indent)))
        end = skip_space(cursor)
        cursor = end + 1 if text[end] == "," else end
    for start, end, rendered in reversed(replacements):
        text = text[:start] + rendered + text[end:]
    if json.loads(text) != value:
        raise ValueError("receipt serialization changed unrelated values")
    return text.encode("utf-8")


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
        module = module_for(topic)
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
    parser.add_argument("--verify-git-base", action="store_true",
                        help="require actual continuity base Git bytes, even in shallow clones")
    args = parser.parse_args()
    entries, reasons = derive()
    ledger = json.loads(LEDGER.read_text())
    receipts = json.loads(RECEIPTS.read_text())
    diagrams = diagram_pages(entries)
    verify_git = True
    if CONTINUITY_REVIEW.exists():
        verify_git = git_base_available()
        if not verify_git and (args.command == "refresh" or args.verify_git_base):
            raise ValueError("continuity integration/refresh requires actual Git base bytes")
    continuity = continuity_pages(entries, diagrams, verify_git)
    if continuity:
        ledger, receipts = continuity_receipts(
            entries, reasons, continuity, ledger, receipts, args.command, verify_git)
        integrated = json.loads(CONTINUITY_REVIEW.read_text()).get("integrated_files", {})
        for path, value in ((LEDGER, ledger), (RECEIPTS, receipts)):
            source = path.relative_to(ROOT).as_posix()
            raw = receipt_bytes(path, value)
            if source in integrated and integrated[source] != sha256(raw):
                raise ValueError(f"continuity integrated receipt SHA mismatch: {source}")
        catalog_source = "content/catalog.json"
        if catalog_source in integrated and integrated[catalog_source] != sha256(
                (ROOT / catalog_source).read_bytes()):
            raise ValueError("continuity integrated catalog SHA mismatch")
        if args.command == "refresh":
            for path, value in ((LEDGER, ledger), (RECEIPTS, receipts)):
                raw = receipt_bytes(path, value)
                if path.read_bytes() != raw:
                    path.write_bytes(raw)
        print(f"PASS: {len(entries)} unique continuity sources; frozen diagram/base/current "
              f"SHA chain ({'actual Git bytes' if verify_git else 'shallow frozen fingerprints'}); "
              "exact scoped receipts; no browser or build validation")
        return False
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
