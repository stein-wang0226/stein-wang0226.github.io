"""Add a reading shell without serializing or rewriting legacy scientific HTML."""
import html
import re


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
            end = f'<nav class="reading-series" aria-label="章节导航">{"".join(links)}</nav>'
            intro += f'<p>系列位置：{position + 1} / {len(chapters)} · <a href="{series_link}">查看系列目录</a></p>'
        else:
            intro += '<details class="reading-series-list"><summary>按顺序阅读全部章节</summary><ol>' + "".join(
                f'<li><a href="{ctx.rel(path, e["url"])}">{esc(e["title"])}</a></li>'
                for e in chapters) + "</ol></details>"
    # Existing TOCs are reused. Only add a compact directory when there is none.
    has_toc = bool(re.search(r'<(?:nav|aside|div)[^>]*(?:class|id)=["\'][^"\']*(?:toc|sidebar)', text))
    body_match = re.search(r'(<body\b[^>]*>)(.*)(</body>)', text, re.S | re.I)
    if not body_match:
        raise ValueError(f"{entry['id']}: missing complete HTML body")
    body = body_match[2]
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
    if not has_toc:
        links = []
        ids = set(re.findall(r'\bid=["\']([^"\']+)', body))
        def heading(match):
            level, attrs, inner = match[1], match[2], match[3]
            found = re.search(r'\bid=["\']([^"\']+)', attrs)
            identifier = found[1] if found else "reading-section-" + str(len(links) + 1)
            while not found and identifier in ids:
                identifier += "-new"
            ids.add(identifier)
            label = re.sub(r'<[^>]+>', '', inner)
            links.append(f'<li><a href="#{esc(identifier)}">{label}</a></li>')
            return match[0] if found else f'<h{level}{attrs} id="{identifier}">{inner}</h{level}>'
        body = re.sub(r'<h([23])([^>]*)>(.*?)</h\1>', heading, body, flags=re.S | re.I)
        if links:
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
    text = text[:body_match.start(2)] + body + text[body_match.end(2):]
    text = text.replace("</head>", f'<link rel="stylesheet" href="{ctx.rel(path, "/assets/site/site.css")}">\n'
                        f'<link rel="stylesheet" href="{ctx.rel(path, "/assets/site/reading.css")}">\n</head>', 1)
    return text
