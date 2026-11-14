#!/usr/bin/env python3
"""Derive a version-aware bibliography from HTML citations and source registries."""
import argparse
from collections import defaultdict
import hashlib
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import unquote, urljoin, urlsplit, urlunsplit
from catalog import load_content
from render import ROOT, route_path


def source_identity(url):
    parsed = urlsplit(url)
    path = unquote(parsed.path).rstrip("/")
    arxiv = re.search(r"(?:abs|html|pdf)/(\d{4}\.\d{4,5})(v\d+)?", path)
    if parsed.netloc.endswith("arxiv.org") and arxiv:
        version = arxiv[2] or "unspecified"
        return f"arxiv:{arxiv[1]}@{version}", version, "论文"
    if parsed.netloc in {"doi.org", "dx.doi.org"}:
        return "doi:" + path.lstrip("/").casefold(), "unspecified", "论文"
    if parsed.netloc == "github.com":
        parts = path.lstrip("/").split("/")
        if len(parts) >= 4 and parts[2] in {"blob", "tree", "commit"}:
            version = parts[3] if re.fullmatch(r"[0-9a-f]{40}", parts[3]) else "unspecified"
            return f"github:{'/'.join(parts[:2])}@{parts[3]}/{'/'.join(parts[4:])}", version, "代码"
        return "github:" + path.lstrip("/"), "unspecified", "代码"
    if parsed.netloc == "huggingface.co":
        parts = path.lstrip("/").split("/")
        if len(parts) >= 4 and parts[2] in {"blob", "resolve"}:
            version = parts[3] if re.fullmatch(r"[0-9a-f]{40}", parts[3]) else "unspecified"
            return f"hf:{'/'.join(parts[:2])}@{parts[3]}/{'/'.join(parts[4:])}", version, "模型与文档"
    clean = urlunsplit((parsed.scheme, parsed.netloc.casefold(), path, parsed.query, ""))
    return "url:" + clean, "unspecified", "文档与项目"


class Links(HTMLParser):
    def __init__(self, entry):
        super().__init__()
        self.entry, self.stack, self.links, self.current = entry, [], [], None
        self.text_refs = defaultdict(list)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag not in {"meta", "link", "img", "input", "br", "hr", "source", "wbr", "path", "circle", "rect", "line", "polygon", "polyline", "ellipse", "use"}:
            self.stack.append((tag, attrs))
        if tag != "a" or not attrs.get("href"):
            return
        ref = next((a["id"] for _, a in reversed(self.stack)
                    if re.fullmatch(r"ref-[\w-]+", a.get("id", ""))), None)
        section = next((a["id"] for t, a in reversed(self.stack)
                        if t in {"section", "article", "h2", "h3"} and a.get("id")), None)
        historical = any("data-reading-history" in a for _, a in self.stack)
        self.current = {
            "url": urljoin("https://notes.local" + self.entry["url"], attrs["href"]),
            "ref": ref, "anchor": section,
            "role": "historical" if historical else "current", "text": [],
        }

    handle_startendtag = handle_starttag

    def handle_data(self, data):
        ref = next((a["id"] for _, a in reversed(self.stack)
                    if re.fullmatch(r"ref-[\w-]+", a.get("id", ""))), None)
        if ref:
            self.text_refs[ref].append(data)
        if self.current:
            self.current["text"].append(data)

    def handle_endtag(self, tag):
        if tag == "a" and self.current:
            self.current["title"] = " ".join("".join(self.current.pop("text")).split())
            self.links.append(self.current)
            self.current = None
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                self.stack = self.stack[:index]
                break


def derive(root=ROOT, content=None):
    site, entries, _, _ = content or load_content(root)
    records, references, pending, errors = {}, defaultdict(set), [], []

    def record(url, title):
        key, version, kind = source_identity(url)
        if key not in records:
            records[key] = {"source_key": key, "title": title or url, "version": version,
                            "kind": kind, "urls": [], "local_references": [],
                            "used_in": [], "archive_metadata": []}
        value = records[key]
        if url not in value["urls"]:
            value["urls"].append(url)
        return value

    for entry in entries:
        if entry["origin"] != "local" or entry["status"] == "draft":
            continue
        parser = Links(entry)
        parser.feed((root / entry["source"]).read_text(encoding="utf-8"))
        for link in parser.links:
            url = urlsplit(link["url"])
            if url.netloc == "notes.local":
                if url.fragment.startswith("ref-"):
                    local = url.path.removesuffix("index.html") if url.path.endswith("/index.html") else url.path
                    pending.append((local + "#" + url.fragment, entry, link))
                continue
            if url.scheme not in {"https", "http"} or url.netloc == urlsplit(site["url"]).netloc:
                continue
            value = record(link["url"], link["title"])
            location = entry["url"] + ("#" + link["anchor"] if link["anchor"] else "")
            if link["ref"]:
                ref_url = entry["url"] + "#" + link["ref"]
                references[ref_url].add(value["source_key"])
                ref = {"url": ref_url, "label": f'{entry["title"]} [{link["ref"].removeprefix("ref-")}]'}
                if ref not in value["local_references"]:
                    value["local_references"].append(ref)
            else:
                usage = {"url": location, "entry": entry["id"], "title": entry["title"],
                         "role": link["role"], "citation": "直接链接"}
                if usage not in value["used_in"]:
                    value["used_in"].append(usage)
        for anchor, parts in parser.text_refs.items():
            target = entry["url"] + "#" + anchor
            if references.get(target):
                continue
            key = "local:" + target
            title = " ".join("".join(parts).split())
            records[key] = {
                "source_key": key, "title": title, "version": "unspecified",
                "kind": "原文元数据", "urls": [], "archive_metadata": [], "used_in": [],
                "local_references": [{"url": target, "label": f'{entry["title"]} [{anchor.removeprefix("ref-")}]'}],
            }
            references[target].add(key)
    for target, entry, link in pending:
        if target not in references:
            errors.append(f"citation: {entry['id']} unresolved bibliography {target}")
            continue
        for key in references[target]:
            usage = {"url": entry["url"] + ("#" + link["anchor"] if link["anchor"] else ""),
                     "entry": entry["id"], "title": entry["title"],
                     "role": link["role"], "citation": target}
            if usage not in records[key]["used_in"]:
                records[key]["used_in"].append(usage)
    registries = [
        ("assets/research/agent-data-benchmarks/sources.json", "/agent-data-benchmarks/"),
        ("assets/research/posttraining-20261114/sources.json", "/llm-posttraining/"),
        ("assets/research/2026-11-14/sources.json", "/llm-research-map-2026/"),
    ]
    for name, index in registries:
        data = json.loads((root / name).read_text())
        for metadata in data["sources"]:
            url = metadata.get("canonical_url") or metadata.get("url")
            value = record(url, metadata["title"])
            number = metadata.get("number", metadata.get("id"))
            target = index + "#ref-" + str(number)
            if value["source_key"] not in references.get(target, set()):
                errors.append(f"citation registry: {name} [{number}] URL differs from HTML bibliography")
            arxiv = re.search(r"\d{4}\.\d{4,5}(v\d+)", str(metadata.get("version", "")))
            if arxiv and arxiv[1] != value["version"]:
                errors.append(f"citation registry: {name} [{number}] version conflict")
            if metadata.get("usage_as_of"):
                for field, role in (("used_in", "current"), ("historical_used_in", "historical")):
                    expected = sorted({u["url"] for u in value["used_in"] if u["role"] == role})
                    if metadata.get(field) != expected:
                        errors.append(f"citation registry: {name} [{number}] stale {field}")
            # Preserve every field; current/historical uses are derived independently.
            value["archive_metadata"].append({"registry_url": "/" + name, **metadata})
            if metadata.get("local_asset"):
                local = root / route_path(metadata["local_asset"])
                if not local.is_file():
                    errors.append(f"citation archive missing: {metadata['local_asset']}")
                elif metadata.get("sha256") and hashlib.sha256(local.read_bytes()).hexdigest() != metadata["sha256"]:
                    errors.append(f"citation archive SHA mismatch: {metadata['local_asset']}")
                elif metadata.get("bytes") is not None and local.stat().st_size != metadata["bytes"]:
                    errors.append(f"citation archive length mismatch: {metadata['local_asset']}")
    for value in records.values():
        value["used_in"].sort(key=lambda u: (u["role"], u["url"], u["citation"]))
        value["urls"].sort()
        value["local_references"].sort(key=lambda u: u["url"])
    return {"schema_version": 1, "as_of": "2026-11-14",
            "note": "Derived from original HTML and three versioned source registries. Local citation numbers remain page-scoped; unspecified means the source did not pin a version. Current and frozen-original usage are separate.",
            "sources": sorted(records.values(), key=lambda s: (s["kind"], s["title"].casefold(), s["source_key"]))}, errors


def render_citations(ctx):
    data, errors = derive(ctx.root, (ctx.site, ctx.entries, ctx.publications, ctx.redirects))
    if errors:
        raise ValueError("\n".join(errors))
    ctx.write("/blog/references.json", json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    esc = html.escape
    rows = []
    for index, source in enumerate(data["sources"]):
        search = " ".join([source["title"], source["source_key"], *source["urls"],
                           *(u["title"] for u in source["used_in"])]).casefold()
        uses = []
        for role, label in (("current", "当前使用"), ("historical", "冻结原文")):
            locations = {(u["url"], u["title"]) for u in source["used_in"] if u["role"] == role}
            if locations:
                uses.append(label + "：" + "；".join(
                    f'<a href="{ctx.rel("/blog/references/", url.split("#")[0])}'
                    f'{"#" + esc(url.split("#", 1)[1]) if "#" in url else ""}">{esc(title)}</a>'
                    for url, title in sorted(locations)))
        refs = "；".join(f'<a href="{ctx.rel("/blog/references/", ref["url"].split("#")[0])}'
                        f'#{esc(ref["url"].split("#")[1])}">{esc(ref["label"])}</a>'
                        for ref in source["local_references"])
        originals = " · ".join(f'<a href="{esc(url, quote=True)}">原始来源</a>' for url in source["urls"])
        archives = " · ".join(
            f'<a href="{ctx.rel("/blog/references/", m["local_asset"])}">固定版本原件</a>'
            for m in source["archive_metadata"] if m.get("local_asset"))
        rows.append(f'<li id="source-{index + 1}" data-search="{esc(search, quote=True)}" '
                    f'data-kind="{esc(source["kind"])}" data-version="{esc(source["version"])}">'
                    f'<h2>{esc(source["title"])}</h2><small>{esc(source["kind"])} · 版本：'
                    f'{esc(source["version"])}</small><p>{originals} {archives}</p>'
                    f'<p>{refs or "直接链接：没有补造文献编号"}</p>'
                    + "".join(f'<p>{u}</p>' for u in uses) + "</li>")
    kinds = "".join(f'<option>{esc(k)}</option>' for k in sorted({s["kind"] for s in data["sources"]}))
    body = ('<p><a href="../">博客与笔记</a> / 文献查阅</p><h1>文献与原始来源</h1>'
            '<p>按题目、版本、使用章节查阅。同一论文的不同版本分别保留；引用编号属于原页面。'
            '“unspecified”表示未固定版本，冻结原文与当前主讲证据分别标注。</p>'
            '<p><a href="../references.json" download>下载完整引用数据</a></p>'
            '<form class="reference-controls" id="reference-form">'
            '<label>关键词<input name="q" type="search" placeholder="OPD、Harbor、论文或章节"></label>'
            f'<label>来源类型<select name="kind"><option value="">全部</option>{kinds}</select></label>'
            '<label>版本<input name="version" placeholder="v1、提交号或unspecified"></label>'
            '<button type="reset">清除条件</button></form>'
            f'<p id="reference-count" role="status">{len(rows)} 项来源</p>'
            '<noscript><p>以下完整静态列表可直接阅读；筛选需启用JavaScript。</p></noscript>'
            '<ul class="reference-list">' + "".join(rows) + "</ul>")
    ctx.page("/blog/references/", "文献与原始来源", body,
             "版本化文献、原始来源、章节引用与冻结原文使用位置。", script="/assets/site/citations.js")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["check"])
    args = parser.parse_args()
    data, errors = derive()
    print("\n".join(errors) if errors else f"PASS: {len(data['sources'])} source/version records; local citations, registries and archive SHA/length")
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
