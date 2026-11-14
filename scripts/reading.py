"""Add a reading shell without serializing or rewriting legacy scientific HTML."""
import html
import json
import re
from urllib.parse import urljoin, urlsplit
from render import route_path

GROUPS = {"main": "主线", "extension": "研究扩展",
          "prerequisite": "按需先修与完整推导", "reference": "行业参考"}


def chapter_directory(ctx, entry, chapters):
    def title(row):
        return html.escape(re.sub(r"^\d+\s*·\s*", "", row["title"]))
    groups = []
    for group in GROUPS:
        rows = [e for e in chapters if e.get("chapter_group", "main") == group]
        if not rows:
            continue
        groups.append(f'<section class="reading-chapter-group"><h3>{GROUPS[group]}</h3><ol>' + "".join(
            f'<li data-chapter="{html.escape(e["id"])}"><span class="chapter-number">{e["order"]:02}</span>'
            f'<div><a href="{ctx.rel(entry["url"], e["url"])}">{title(e)}</a>'
            f'<p>{html.escape(e["summary"])}</p></div></li>' for e in rows) + "</ol></section>")
    return '<section class="reading-chapters" id="series-chapters"><h2>章节目录</h2>' + "".join(groups) + "</section>"


def decorate(ctx, entry, text):
    path = entry["url"]
    esc = lambda value: html.escape(str(value), quote=True)
    # Replace only the previous generated navigation, not article controls.
    text = re.sub(r"<!-- SITE:NAV:START -->.*?<!-- SITE:NAV:END -->", "", text, flags=re.S)
    text = re.sub(r'<link\b[^>]*href=["\'][^"\']*assets/site/site\.css["\'][^>]*>', "", text)
    text = re.sub(r'<footer\b[^>]*class=["\']site-footer["\'][^>]*>.*?</footer>',
                  "", text, flags=re.S)
    topic = next(t["label"] for t in ctx.site["topics"] if t["id"] == entry["topic"])
    form = next(t["label"] for t in ctx.site["types"] if t["id"] == entry["type"])
    review = {"unreviewed": "科研事实尚未全面复核", "needs-review": "含待补齐或待核实项",
              "reviewed": "已按内容检查记录复核"}[entry["review_status"]]
    intro_id = "reading-intro" if re.search(r'\bid=["\']site-main["\']', text) else "site-main"
    intro = (f'<section class="reading-intro" id="{intro_id}" tabindex="-1">'
             f'<p class="reading-path"><a href="{ctx.rel(path, "/blog/")}">博客与笔记</a> / '
             f'<a href="{ctx.rel(path, "/blog/")}?topic={esc(entry["topic"])}">{esc(topic)}</a></p>'
             f'<h1>{esc(entry["title"])}</h1><p>{esc(entry["summary"])}</p>'
             f'<p class="reading-meta">{esc(topic)} · {esc(form)} · '
             f'{esc(entry["updated"] or "更新时间待确认")} · {review}</p>')
    if entry.get("prerequisites"):
        intro += '<div class="reading-prerequisites"><strong>先修与按需复习</strong><ul>' + "".join(
            f'<li><a href="{ctx.rel(path, ctx.by_id[p["entry"]]["url"])}'
            f'{"#" + esc(p["anchor"]) if p.get("anchor") else ""}">'
            f'{esc(ctx.by_id[p["entry"]]["title"])}</a>：{esc(p["reason"])}</li>'
            for p in entry["prerequisites"]) + "</ul></div>"
    owner = [o for o in ctx.site.get("concept_owners", []) if o["entry"] == entry["id"]]
    if owner:
        intro += '<p class="reading-owner">本页主讲：' + "、".join(esc(o["label"]) for o in owner) + "</p>"
    if entry.get("reading_role") == "reference":
        intro += f'<p>作为推导、代码或复习参考，可从<a href="{ctx.rel(path, "/blog/")}#learning-paths">完整学习主线</a>按需返回。</p>'
    chapters = sorted((e for e in ctx.entries if e["series"] == (entry["series"] or entry["id"])
                       and e["status"] == "published"), key=lambda e: e["order"])
    end = ""
    if entry["status"] == "archived":
        intro += '<p class="reading-warning">此页为历史版本，保留供查证。请阅读' \
                 f'<a href="{ctx.rel(path, ctx.by_id["rl-interview-guide"]["url"])}">现行 RL 手册</a>。</p>'
    if chapters:
        parent = ctx.by_id[entry["series"]] if entry["series"] else entry
        series_link = ctx.rel(path, parent["url"])
        if entry["kind"] == "chapter":
            position = next(i for i, e in enumerate(chapters) if e["id"] == entry["id"])
            links = [f'<a href="{series_link}">系列目录</a>']
            if position:
                prev = chapters[position - 1]
                links.insert(0, f'<a rel="prev" href="{ctx.rel(path, prev["url"])}">← {esc(prev["title"])}</a>')
            if position + 1 < len(chapters):
                nxt = chapters[position + 1]
                links.append(f'<a rel="next" href="{ctx.rel(path, nxt["url"])}">{esc(nxt["title"])} →</a>')
                if entry.get("chapter_group", "main") != nxt.get("chapter_group", "main"):
                    end += f'<p class="reading-transition">下一页进入{GROUPS[nxt.get("chapter_group", "main")]}。主线已读完时，可回到系列目录按需选择。</p>'
            end += f'<nav class="reading-series" aria-label="章节导航">{"".join(links)}</nav>'
            intro += f'<p>系列位置：{position + 1} / {len(chapters)} · <a href="{series_link}">查看系列目录</a></p>'
    # Existing TOCs are reused. Only add a compact directory when there is none.
    has_toc = bool(re.search(r'<(?:nav|aside|div)[^>]*(?:class|id)=["\'][^"\']*(?:toc|sidebar)', text))
    body_match = re.search(r'(<body\b[^>]*>)(.*)(</body>)', text, re.S | re.I)
    if not body_match:
        raise ValueError(f"{entry['id']}: missing complete HTML body")
    body = body_match[2]
    if entry["kind"] == "chapter":
        # Legacy chapter bars/footers are presentation copies. Replace them from
        # the same order used by the shared directory; source research stays intact.
        compact = '<nav class="reading-chapter-bar" aria-label="系列章节"><a href="' + series_link + '">系列目录</a>' + "".join(
            f'<a href="{ctx.rel(path, e["url"])}"'
            f'{" aria-current=page" if e["id"] == entry["id"] else ""}>'
            f'{e["order"]:02}</a>' for e in chapters) + "</nav>"
        body = re.sub(r'<nav\b[^>]*class=["\']nav-bar["\'][^>]*>.*?</nav>', compact, body, flags=re.S)
        body = re.sub(r'<div\b[^>]*class=["\']page-nav["\'][^>]*>.*?</div>', "", body, flags=re.S)
        def link_label(match):
            attrs, inner = match[1], match[2]
            href = re.search(r'href=["\']([^"\']+)', attrs)
            if not href:
                return match[0]
            url = urlsplit(urljoin("https://notes.local" + path, href[1]))
            if url.netloc != "notes.local":
                return match[0]
            target = next((e for e in ctx.entries if e["kind"] == "chapter"
                           and route_path(e["url"]) == route_path(url.path)), None)
            if not target:
                return match[0]
            if re.fullmatch(r"\d{2}", inner):
                inner = f'{target["order"]:02}'
            else:
                inner = re.sub(r"^(?:第)?\d{2}(?=\s|章|[ ·])", f'{target["order"]:02}', inner)
            return "<a" + attrs + ">" + inner + "</a>"
        body = re.sub(r"<a([^>]*)>(.*?)</a>", link_label, body, flags=re.S)
    if chapters and entry["kind"] == "series":
        directory = chapter_directory(ctx, entry, chapters)
        if "<!-- READING:CHAPTERS -->" in body:
            body = body.replace("<!-- READING:CHAPTERS -->", directory, 1)
        else:
            intro += directory
    # A visible native fallback keeps the original mobile directory reachable
    # when its toggle script cannot run.
    body = re.sub(r'(<button\b[^>]*class=["\']menu-btn["\'][^>]*>.*?</button>)',
                  r'\1<noscript><style>.reading-content .menu-btn{display:none!important}'
                  r'.reading-content .menu-btn ~ .sidebar{display:block!important}</style></noscript>',
                  body, flags=re.S)
    if re.search(r'\bid=["\']math-loading["\']', body):
        body = '<noscript><style>.reading-content #math-loading{display:none}</style>' \
               '<p>当前未启用 JavaScript，公式以 TeX 原文显示，目录与正文仍可阅读。</p></noscript>' + body
    def source_links(match):
        inner = re.sub(r'\b(\d{4}\.\d{4,5}(?:v\d+)?)\b',
                       lambda m: f'<a href="https://arxiv.org/abs/{m[1]}">{m[1]}</a>',
                       match[2])
        return match[1] + inner + match[3]
    body = re.sub(r'(<span\b[^>]*class=["\'][^"\']*\barxiv\b[^"\']*["\'][^>]*>)(.*?)(</span>)',
                  source_links, body, flags=re.S)
    links = []
    ids = set(re.findall(r'\bid=["\']([^"\']+)', body))
    audit_path = ctx.root / "docs/organization-audit-20261114.json"
    if not hasattr(ctx, "organization_headings"):
        ctx.organization_headings = json.loads(audit_path.read_text())["pages"] if audit_path.is_file() else []
    old = next((p for p in ctx.organization_headings if p["id"] == entry["id"]), {})
    legacy = {}
    for item in old.get("generated_headings", []):
        legacy.setdefault(item["label"], []).append(item["anchor"])
    reserved = {item["anchor"] for item in old.get("generated_headings", [])}
    dlm_heading = re.search(r'<h2[^>]*class="section-title"[^>]*>.*?<span class="num">(\d+)</span>', body, re.S)
    dlm_original_number = int(dlm_heading[1]) if dlm_heading else None
    def display_label(label):
        if entry.get("series") != "dlm-survey" or dlm_original_number is None:
            return label
        label = re.sub(r"^" + str(dlm_original_number) + r"(?=\.\d+)",
                       str(entry["order"]), label)
        return re.sub(r"^" + f"{dlm_original_number:02}" + r"(?=\s)",
                      f'{entry["order"]:02}', label)
    def decorate_headings(fragment, historical=False):
        def heading(match):
            level, attrs, inner = match[1], match[2], match[3]
            found = re.search(r'\bid=["\']([^"\']+)', attrs)
            label = re.sub(r'<[^>]+>', '', inner).strip()
            prior = legacy.get(label, [])
            compatible = prior.pop(0) if prior else None
            identifier = found[1] if found else compatible or "reading-topic-" + str(len(ids) + 1)
            while not found and not compatible and (identifier in ids or identifier in reserved):
                identifier += "-new"
            ids.add(identifier)
            if not historical:
                links.append(f'<li><a href="#{esc(identifier)}">{display_label(label)}</a></li>')
            alias = f'<span id="{compatible}" class="reading-anchor"></span>' if compatible and compatible != identifier and compatible not in ids else ""
            if alias:
                ids.add(compatible)
            return (match[0].replace(">", ">" + alias, 1) if found else
                    f'<h{level}{attrs} id="{identifier}">{inner}</h{level}>')
        return re.sub(r'<h([23])([^>]*)>(.*?)</h\1>', heading, fragment, flags=re.S | re.I)
    fragments = re.split(r'(<!-- READING:HISTORY:START -->.*?<!-- READING:HISTORY:END -->)', body, flags=re.S)
    body = "".join(decorate_headings(f, f.startswith("<!-- READING:HISTORY:START -->")) for f in fragments)
    if entry["kind"] == "chapter":
        text = re.sub(r"<title>.*?</title>", f'<title>{esc(entry["title"])}</title>', text, count=1, flags=re.S)
        if entry["series"] == "dlm-survey":
            root_heading = re.search(r'(<h2[^>]*class="section-title"[^>]*>.*?<span class="num">)(\d+)(</span>)', body, re.S)
            if root_heading:
                original_number = int(root_heading[2])
                body = body[:root_heading.start(2)] + f'{entry["order"]:02}' + body[root_heading.end(2):]
                body = re.sub(r'(<h3[^>]*>)' + str(original_number) + r'(\.\d+)',
                              lambda m: m[1] + str(entry["order"]) + m[2], body)
        body = re.sub(r'(<p[^>]*class="eyebrow"[^>]*>[^<]*Chapter\s*)\d+',
                      lambda m: m[1] + f'{entry["order"]:02}', body, count=1)
    history_ids = set()
    for fragment in re.findall(r'<!-- READING:HISTORY:START -->(.*?)<!-- READING:HISTORY:END -->', body, flags=re.S):
        history_ids.update(re.findall(r'\bid=["\']([^"\']+)', fragment))
    def current_toc(match):
        text = match[0]
        return re.sub(r'<li\b[^>]*>\s*<a\b[^>]*href=["\']#([^"\']+)["\'][^>]*>.*?</a>\s*</li>',
                      lambda m: "" if m[1] in history_ids else m[0], text, flags=re.S)
    body = re.sub(r'<(aside|nav|div)\b[^>]*(?:class|id)=["\'][^"\']*(?:toc|sidebar)[^"\']*["\'][^>]*>.*?</\1>',
                  current_toc, body, flags=re.S)
    if not has_toc and links and entry["kind"] != "series":
        intro += '<details class="reading-toc"><summary>本文目录</summary><ol>' + "".join(links) + "</ol></details>"
    intro += "</section>"
    # Tables scroll in their own containers. Inline diagrams retain aspect ratio.
    body = re.sub(r'(<table\b.*?</table>)', r'<div class="reading-table">\1</div>', body, flags=re.S | re.I)
    related = []
    candidates = [ctx.by_id[i] for i in entry.get("related", [])]
    candidates += sorted((e for e in ctx.entries if e["id"] != entry["id"]
                           and e["status"] == "published" and e["kind"] != "chapter"
                           and (e["topic"] == entry["topic"] or set(e["tags"]) & set(entry["tags"]))),
                          key=lambda e: e["id"])
    seen = set()
    for row in candidates:
        if row["id"] in seen or row["status"] == "draft":
            continue
        seen.add(row["id"])
        target = row["url"] if row["origin"] == "external" else ctx.rel(path, row["url"])
        related.append(f'<li><a href="{esc(target)}">{esc(row["title"])}</a></li>')
        if len(related) == 4:
            break
    end += '<aside class="reading-related" aria-label="关联阅读"><h2>关联阅读</h2><ul>' + "".join(related) + "</ul></aside>"
    body = ctx.navigation(path) + intro + '<div class="reading-content">' + body + "</div>" + end + ctx.footer(path)
    # Title changes can shift offsets; locate the body again before splicing.
    body_match = re.search(r'(<body\b[^>]*>)(.*)(</body>)', text, re.S | re.I)
    text = text[:body_match.start(2)] + body + text[body_match.end(2):]
    text = text.replace("</head>", f'<link rel="stylesheet" href="{ctx.asset(path, "/assets/site/site.css")}">\n'
                        f'<link rel="stylesheet" href="{ctx.asset(path, "/assets/site/reading.css")}">\n'
                        f'<script defer src="{ctx.asset(path, "/assets/site/reading.js")}"></script>\n</head>', 1)
    return text
