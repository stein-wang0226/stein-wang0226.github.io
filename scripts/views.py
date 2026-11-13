"""Catalog-driven home and blog views; no duplicate content records."""
import html
import json
import re
from datetime import date
from html.parser import HTMLParser
from string import Template

from render import load_md, md


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

    def handle_starttag(self, tag, attrs):
        if tag in {"h2", "h3"}:
            self.level, self.text = tag, []

    def handle_data(self, data):
        if self.level:
            self.text.append(data)

    def handle_endtag(self, tag):
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
            "origin", "status", "updated", "series", "order"
        )}
        headings = Headings()
        if entry["origin"] == "local":
            headings.feed((ctx.root / entry["source"]).read_text(encoding="utf-8"))
        row["headings"] = headings.items
        row["search"] = " ".join([row["title"], row["summary"], *row["tags"],
                                  *headings.items]).casefold()
        result.append(row)
    return result


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
    bio = md(about.split("## Research Interests")[0].strip())
    rows = ordered([e for e in ctx.entries if e["origin"] == "local"
                    and e["status"] == "published" and e["kind"] != "chapter"])
    topics = "".join(
        f'<a class="topic-link" href="blog/?topic={esc(t["id"])}">{esc(t["label"])}</a>'
        for t in ctx.site["topics"])
    papers = "".join(
        '<article class="publication-card"><p class="paper-meta">'
        f'{esc(p["meta"]["date"])} · {esc(p["meta"]["venue"])}</p>'
        f'<h2><a href="{ctx.rel("/", p["url"])}">{esc(p["meta"]["title"])}</a></h2>'
        f'<p>{esc(p["meta"]["excerpt"])}</p></article>'
        for p in ctx.publications if p["slug"] in ctx.site["publications"]["featured"])
    feature = next((e for e in rows if e.get("featured") and e["kind"] == "series"), None)
    recommendations = [e for e in rows if e.get("featured") and e != feature][:2]
    recent = "".join(
        f'<article class="recent-note"><span class="note-date">{esc(e["updated"])}</span>'
        f'<h3><a href="{ctx.rel("/", e["url"])}">{esc(e["title"])}</a></h3></article>'
        for e in rows if e["updated"])
    template = Template((ctx.root / "templates/home.html").read_text(encoding="utf-8"))
    body = template.substitute(bio=bio, topics=topics, papers=papers,
                               count=len(rows),
                               recent=recent,
                               featured=(featured_series(ctx, feature, "/") if feature else "") +
                               "".join(card(ctx, e, "/") for e in recommendations))
    ctx.page("/", "Yuxiang Wang · Research & Notes", body,
             "Research profile, publications, and study notes on LLMs, agents and diffusion models.")


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
    feature = next((e for e in local if ctx.by_id[e["id"]].get("featured")
                    and e["kind"] == "series"), None)
    feature_html = featured_series(ctx, feature) if feature else ""
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
            f'<div class="catalog-stats"><span><strong>{len(local)}</strong>笔记集合</span>'
            f'<span><strong>{sum(e["kind"] == "chapter" and e["status"] == "published" for e in rows)}</strong>章节</span>'
            f'<span><strong>{len(ctx.site["topics"])}</strong>主题</span></div></div></header>'
            '<form id="catalog-form" class="catalog-controls" action="/blog/" method="get">'
            '<div class="catalog-search"><label class="search-field">'
            '<span class="visually-hidden">关键词</span>'
            '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
            '<circle cx="10.5" cy="10.5" r="6.5" stroke="currentColor" stroke-width="1.5"/>'
            '<path d="m16 16 4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>'
            '<input id="filter-q" type="search" name="q" autocomplete="off" '
            'placeholder="搜索文章与章节：ELBO、PPO…"></label>'
            '<button class="search-submit" type="submit">搜索</button></div>'
            '<div id="topic-fallback" class="catalog-topic-fallback">' +
            select("topic", "技术主题", ctx.site["topics"]) + '</div>'
            f'<div id="topic-chips" class="topic-chips" role="group" aria-label="技术主题" hidden>{chips}</div>'
            '<div class="catalog-secondary">' +
            select("type", "内容类型", ctx.site["types"]) +
            '<label class="catalog-field"><span class="catalog-label">排序</span>'
            '<select name="sort" id="filter-sort"><option value="updated-desc">最近更新</option>'
            '<option value="title">标题</option></select></label>'
            '<button type="button" id="clear-filters" hidden>清除条件</button>'
            '</div></form><p id="catalog-notice" role="status"></p>'
            '<noscript><p>当前未启用 JavaScript。以下列出全部文章；'
            '系列卡片内可直接浏览章节，筛选需启用 JavaScript。</p></noscript>'
            '<section aria-label="本地文章"><div class="catalog-heading"><h2>全部笔记</h2>'
            f'<p id="result-count" aria-live="polite">{len(local)} 个笔记集合</p></div>'
            '<div id="catalog-results" class="note-grid">' +
            "".join(feature_html if e == feature else card(ctx, e, chapters=True) for e in local) +
            '</div><p id="no-results" class="no-results" hidden>没有匹配内容。'
            '<a href="/blog/">清除条件，查看全部文章</a></p></section>'
            '<section id="external" class="supplemental"><h2>独立子站</h2><p>课程笔记与面试复习材料。</p>'
            '<div class="note-grid">' + "".join(card(ctx, e) for e in external) +
            '</div></section><section id="archive" class="supplemental"><h2>历史版本</h2>'
            '<p>保留原始内容与旧链接，便于对照阅读。</p><div class="note-grid">' +
            "".join(card(ctx, e) for e in archived) + "</div></section>"
            '<p class="catalog-footnote">日期表示内容更新时间，未知日期保留为待确认。'
            '科研材料的逐项事实复核仍在进行。</p>'
            f'<template id="catalog-feature">{feature_html}</template>')
    data = {"entries": rows, "topics": ctx.site["topics"], "types": ctx.site["types"],
            "compatibility": ctx.redirects.get("query_compatibility", {}).get("blog", {}),
            "featured_id": feature["id"] if feature else None}
    ctx.write("/blog/catalog.json", json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    ctx.page("/blog/", "博客与笔记", body, "分类目录、关键词搜索与系列章节。",
             script="/assets/site/catalog.js")
