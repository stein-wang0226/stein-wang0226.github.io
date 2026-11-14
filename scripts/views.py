"""Catalog-driven home and blog views; no duplicate content records."""
import html
import json
import re
from datetime import date
from html.parser import HTMLParser
from string import Template

from render import load_md, md, publication_date


def esc(value):
    return html.escape(str(value), quote=True)


def ordered(entries):
    return sorted(entries, key=lambda e: (not bool(e["updated"]),
                                         -date.fromisoformat(e["updated"]).toordinal() if e["updated"] else 0,
                                         e["title"], e["id"]))


class Headings(HTMLParser):
    def __init__(self):
        super().__init__()
        self.level, self.text, self.items = None, [], []
        self.history = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "details" and (self.history or "data-reading-history" in attrs):
            self.history += 1
        if self.history:
            return
        if tag in {"h2", "h3"}:
            self.level, self.text = tag, []

    def handle_data(self, data):
        if self.level:
            self.text.append(data)

    def handle_endtag(self, tag):
        if tag == "details" and self.history:
            self.history -= 1
            return
        if tag == self.level:
            self.items.append(" ".join("".join(self.text).split()))
            self.level = None


def public_entries(ctx):
    result = []
    for entry in ctx.entries:
        if entry["status"] == "draft":
            continue
        row = {key: entry[key] for key in (
            "id", "kind", "title", "summary", "url", "topic", "type", "tags",
            "origin", "status", "updated", "series", "order", "reading_role", "chapter_group"
        )}
        headings = Headings()
        if entry["origin"] == "local":
            headings.feed((ctx.root / entry["source"]).read_text(encoding="utf-8"))
        row["headings"] = headings.items
        row["search"] = " ".join([row["title"], row["summary"], *row["tags"],
                                  *headings.items]).casefold()
        result.append(row)
    return result


def route_stages(ctx, route):
    items = []
    for node in route["stages"]:
        entry = ctx.by_id[node["entry"]]
        url = ctx.rel("/blog/", entry["url"]) + ("#" + node["anchor"] if node.get("anchor") else "")
        text = f'<a href="{esc(url)}">{esc(entry["title"])}</a>'
        if node.get("question"):
            text += f'<p>{esc(node["question"])}</p><small>阅读产物：{esc(node["output"])}</small>'
        if entry.get("prerequisites") and node.get("question"):
            text += '<small>按需先修：' + "、".join(
                f'<a href="{ctx.rel("/blog/", ctx.by_id[p["entry"]]["url"])}'
                f'{"#" + esc(p["anchor"]) if p.get("anchor") else ""}">'
                f'{esc(ctx.by_id[p["entry"]]["title"])}</a>' for p in entry["prerequisites"]) + "</small>"
        items.append("<li>" + text + "</li>")
    return '<ol class="route-stages">' + "".join(items) + "</ol>"


def learning_routes(ctx):
    routes = ctx.site.get("learning_paths", [])
    if not routes:
        return ""
    main, *branches = routes
    body = '<section id="learning-paths" class="learning-paths"><div class="section-heading"><h2>完整学习主线</h2>' \
           '<a href="references/">文献查阅</a></div>' \
           f'<p>{esc(main["summary"])}</p>{route_stages(ctx, main)}'
    body += '<p>生成模型研究分支：<a href="../dlm-survey/">扩散语言模型</a>。基础推导、完整代码和自测题可在后部参考入口按需查阅。</p>'
    body += '<div class="route-branches">' + "".join(
        f'<details><summary>{esc(route["label"])}</summary><p>{esc(route["summary"])}</p>'
        f'{route_stages(ctx, route)}</details>' for route in branches) + "</div></section>"
    body += '<section id="research-focus" class="research-focus"><h2>重点研究路径</h2><div class="research-paths">'
    for route in ctx.site.get("research_paths", []):
        links = []
        if route.get("cv_url"):
            links.append(f'<a href="{ctx.rel("/blog/", route["cv_url"].split("#")[0])}#{esc(route["cv_url"].split("#")[1])}">研究经历</a>')
        for slug in route.get("publication_ids", []):
            paper = next(p for p in ctx.publications if p["slug"] == slug)
            links.append(f'<a href="{ctx.rel("/blog/", paper["url"])}">{esc(paper["meta"]["title"])}</a>')
        body += f'<article id="research-{esc(route["id"])}"><h3>{esc(route["label"])}</h3><p>{esc(route["summary"])}</p>' \
                + route_stages(ctx, route) + '<p class="research-records">' + " · ".join(links) + "</p></article>"
    body += "</div></section><details class=\"concept-index\"><summary>按核心概念查主讲位置</summary><ul>"
    for owner in ctx.site.get("concept_owners", []):
        entry = ctx.by_id[owner["entry"]]
        url = ctx.rel("/blog/", entry["url"]) + ("#" + owner["anchor"] if owner.get("anchor") else "")
        body += f'<li><a href="{esc(url)}">{esc(owner["label"])}</a>：{esc(entry["title"])}</li>'
    return body + "</ul></details>"


def grouped_catalog(ctx, rows):
    groups = []
    for topic in ctx.site["topics"]:
        entries = [e for e in rows if e["topic"] == topic["id"] and e["reading_role"] == "core"]
        if entries:
            groups.append(f'<section class="catalog-group"><h3>{esc(topic["label"])}</h3><div class="note-grid">'
                          + "".join(card(ctx, e, chapters=True) for e in entries) + "</div></section>")
    for role, label in (("reference", "推导、代码与自测参考"), ("tracker", "滚动追踪")):
        entries = [e for e in rows if e["reading_role"] == role]
        if entries:
            groups.append(f'<section class="catalog-group"><h3>{label}</h3><div class="note-grid">'
                          + "".join(card(ctx, e, chapters=True) for e in entries) + "</div></section>")
    return "".join(groups)


def card(ctx, row, path="/blog/", chapters=False):
    topic = next(t["label"] for t in ctx.site["topics"] if t["id"] == row["topic"])
    form = next(t["label"] for t in ctx.site["types"] if t["id"] == row["type"])
    label = row["updated"] or "更新时间待确认"
    suffix = " · 系列章节" if row["kind"] == "chapter" else ""
    link = row["url"] if row["origin"] == "external" else ctx.rel(path, row["url"])
    series_class = " series-card" if row["kind"] == "series" else ""
    body = (f'<article class="note-card{series_class}" data-entry="{esc(row["id"])}">'
            f'<div class="tag"><span>{esc(topic)}</span>'
            f'<span class="note-type">{esc(form)}{suffix}</span></div>'
            f'<h2><a href="{esc(link)}">{esc(row["title"])}</a></h2>'
            f'<p>{esc(row["summary"])}</p><div class="card-bottom">'
            f'<span class="note-date">{esc(label)}</span>'
            f'<a class="card-open" href="{esc(link)}" aria-label="阅读{esc(row["title"])}">'
            f'{"浏览系列" if row["kind"] == "series" else "阅读笔记"}{open_icon()}</a></div>')
    if chapters and row["kind"] == "series":
        children = sorted((e for e in ctx.entries if e["series"] == row["id"]
                           and e["status"] == "published"), key=lambda e: e["order"])
        body += '<details><summary>查看系列章节</summary><ol>' + "".join(
            f'<li><a href="{ctx.rel(path, e["url"])}">{esc(e["title"])}</a></li>'
            for e in children) + "</ol></details>"
    return body + "</article>"


def open_icon():
    return ('<svg viewBox="0 0 24 24" fill="none" aria-hidden="true">'
            '<path d="M5 12h14m-6-6 6 6-6 6" stroke="currentColor" '
            'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def featured_series(ctx, row, path="/blog/"):
    children = sorted((e for e in ctx.entries if e["series"] == row["id"]
                       and e["status"] == "published"), key=lambda e: e["order"])
    topic = next(t["label"] for t in ctx.site["topics"] if t["id"] == row["topic"])
    link = ctx.rel(path, row["url"])
    def chapter_title(entry):
        return esc(re.sub(r"^\d+\s*·\s*", "", entry["title"]))
    chapters = "".join(
        f'<li><a href="{ctx.rel(path, e["url"])}">'
        f'<span class="chapter-number">{e["order"]:02}</span>'
        f'<span>{chapter_title(e)}</span></a></li>'
        for e in children)
    return (f'<article class="note-card featured-card" data-entry="{esc(row["id"])}">'
            '<div class="featured-main"><div class="featured-label">推荐系列</div>'
            f'<div class="tag"><span>{esc(topic)}</span>'
            f'<span class="note-type">{len(children)} 个章节</span></div>'
            f'<h2><a href="{esc(link)}">{esc(row["title"])}</a></h2>'
            f'<p>{esc(row["summary"])}</p><div class="card-bottom">'
            f'<span class="note-date">{esc(row["updated"] or "更新时间待确认")}</span>'
            f'<a class="card-open" href="{esc(link)}" aria-label="浏览{esc(row["title"])}">'
            f'浏览系列{open_icon()}</a></div></div>'
            '<div class="featured-chapters"><h3>按章节阅读</h3>'
            f'<ol class="chapter-list">{chapters}</ol></div></article>')


def render_home(ctx):
    _, about = load_md(ctx.root / "content/pages/about.md")
    bio = md(about.split("## ", 1)[0].strip())
    selected = re.search(r"(?ms)^## Selected Work\s*\n(.*?)(?=^## |\Z)", about)
    work = md(selected.group(1).strip()) if selected else ""
    rows = ordered([e for e in ctx.entries if e["origin"] == "local"
                    and e["status"] == "published" and e["kind"] != "chapter"])
    topics = "".join(
        f'<a class="topic-link" href="blog/?topic={esc(t["id"])}">{esc(t["label"])}</a>'
        for t in ctx.site["topics"])
    papers = "".join(
        '<article class="publication-card"><p class="paper-meta">'
        f'{esc(publication_date(p["meta"]))} · {esc(p["meta"]["venue"])}</p>'
        f'<h2><a href="{ctx.rel("/", p["url"])}">{esc(p["meta"]["title"])}</a></h2>'
        f'<p>{esc(p["meta"]["excerpt"])}</p></article>'
        for slug in ctx.site["publications"]["featured"]
        for p in ctx.publications if p["slug"] == slug)
    recommendations = [ctx.by_id[i] for i in ctx.site.get("home_recommendations", [])]
    recent = "".join(
        f'<article class="recent-note"><span class="note-date">{esc(e["updated"])}</span>'
        f'<h3><a href="{ctx.rel("/", e["url"])}">{esc(e["title"])}</a></h3></article>'
        for e in [r for r in rows if r["updated"]][:6])
    template = Template((ctx.root / "templates/home.html").read_text(encoding="utf-8"))
    body = template.substitute(bio=bio, work=work, topics=topics, papers=papers,
                               count=len(rows),
                               recent=recent,
                               featured="".join(card(ctx, e, "/") for e in recommendations))
    ctx.page("/", "Yuxiang Wang · Research & Notes", body,
             "Yuxiang Wang at Fudan and ByteDance Seed: scientific Harbor tasks, Agentic RL, "
             "GUI agent environments, and diffusion language models.",
             styles=("/assets/site/profile.css",))


def render_blog(ctx):
    rows = public_entries(ctx)
    local = ordered([e for e in rows if e["origin"] == "local"
                     and e["status"] == "published" and e["kind"] != "chapter"])
    external = [e for e in rows if e["origin"] == "external"]
    archived = [e for e in rows if e["status"] == "archived"]
    def select(name, label, options):
        return (f'<label class="catalog-field"><span class="catalog-label">{label}</span>'
                f'<select name="{name}" id="filter-{name}"><option value="">全部</option>' +
                "".join(f'<option value="{esc(o["id"])}">{esc(o["label"])}</option>'
                        for o in options) + "</select></label>")
    chips = ('<button type="button" class="topic-chip" data-topic="" aria-pressed="true">'
             '全部</button>' + "".join(
                 f'<button type="button" class="topic-chip" data-topic="{esc(t["id"])}" '
                 f'aria-pressed="false">{esc(t["label"])}</button>' for t in ctx.site["topics"]))
    body = ('<header class="catalog-hero"><div>'
            '<p class="eyebrow">Research &amp; study notes</p>'
            '<h1 class="catalog-wordmark">Stein’s<span>Notes.</span></h1></div>'
            '<div class="catalog-intro"><h2>博客与研究笔记</h2>'
            '<p>从原理推导到训练工程，记录 LLM、Agent 与扩散模型的学习和实践。'
            '选一个主题，或从感兴趣的问题开始。</p>'
            '<p><a href="#learning-paths">完整学习主线</a> · '
            '<a href="#research-focus">重点研究路径</a> · <a href="references/">文献查阅</a></p>'
            f'<div class="catalog-stats"><span><strong>{len(local)}</strong>笔记集合</span>'
            f'<span><strong>{sum(e["kind"] == "chapter" and e["status"] == "published" for e in rows)}</strong>章节</span>'
            f'<span><strong>{len(ctx.site["topics"])}</strong>主题</span></div></div></header>'
            '<form id="catalog-form" class="catalog-controls" action="/blog/" method="get" '
            f'data-catalog-version="{esc(ctx.metadata["input_digest"][:16])}">'
            '<div class="catalog-toolbar"><div class="catalog-search"><label class="search-field">'
            '<span class="visually-hidden">关键词</span>'
            '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
            '<circle cx="10.5" cy="10.5" r="6.5" stroke="currentColor" stroke-width="1.5"/>'
            '<path d="m16 16 4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>'
            '<input id="filter-q" type="search" name="q" autocomplete="off" '
            'placeholder="搜索笔记、章节或关键词"></label>'
            '<button class="search-submit" type="submit">搜索</button></div>'
            '<div class="catalog-secondary">' +
            select("type", "类型", ctx.site["types"]) +
            '<label class="catalog-field"><span class="catalog-label">排序</span>'
            '<select name="sort" id="filter-sort"><option value="updated-desc">最近更新</option>'
            '<option value="title">标题</option></select></label>'
            '<button type="button" id="clear-filters" hidden>清除条件</button>'
            '</div></div><div id="topic-fallback" class="catalog-topic-fallback">' +
            select("topic", "技术主题", ctx.site["topics"]) + '</div>'
            f'<div id="topic-chips" class="topic-chips" role="group" aria-label="技术主题" hidden>{chips}</div>'
            '</form><p id="catalog-notice" role="status"></p>'
            '<noscript><p>当前未启用 JavaScript。以下列出全部文章；'
            '系列卡片内可直接浏览章节，筛选需启用 JavaScript。</p></noscript>'
            + learning_routes(ctx) +
            '<section aria-label="本地文章" id="all-notes"><div class="catalog-heading"><h2>按主题浏览笔记</h2>'
            f'<p id="result-count" aria-live="polite">{len(local)} 个笔记集合</p></div>'
            '<div id="catalog-results" class="catalog-groups">' + grouped_catalog(ctx, local) +
            '</div><p id="no-results" class="no-results" hidden>没有匹配内容。'
            '<a href="/blog/">清除条件，查看全部文章</a></p></section>'
            '<section id="external" class="supplemental"><h2>独立子站</h2><p>课程笔记与面试复习材料。</p>'
            '<div class="note-grid">' + "".join(card(ctx, e) for e in external) +
            '</div></section><section id="archive" class="supplemental"><h2>历史版本</h2>'
            '<p>保留原始内容与旧链接，便于对照阅读。</p><div class="note-grid">' +
            "".join(card(ctx, e) for e in archived) + "</div></section>"
            '<p class="catalog-footnote">日期表示内容更新时间，未知日期保留为待确认。'
            '科研材料的逐项事实复核仍在进行。</p>'
            )
    data = {"entries": rows, "topics": ctx.site["topics"], "types": ctx.site["types"],
            "compatibility": ctx.redirects.get("query_compatibility", {}).get("blog", {}),
            "concept_owners": ctx.site.get("concept_owners", [])}
    ctx.write("/blog/catalog.json", json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    ctx.page("/blog/", "博客与笔记", body, "分类目录、关键词搜索与系列章节。",
             script="/assets/site/catalog.js")
