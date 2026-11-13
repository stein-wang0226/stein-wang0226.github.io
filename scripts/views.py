"""Catalog-driven home and blog views; no duplicate content records."""
import html
import json
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
    body = (f'<article class="note-card" data-entry="{esc(row["id"])}">'
            f'<span class="tag">{esc(topic)} · {esc(form)}{suffix}</span>'
            f'<h2><a href="{esc(link)}">{esc(row["title"])}</a></h2>'
            f'<p>{esc(row["summary"])}</p><p class="paper-meta">{esc(label)}</p>')
    if chapters and row["kind"] == "series":
        children = sorted((e for e in ctx.entries if e["series"] == row["id"]
                           and e["status"] == "published"), key=lambda e: e["order"])
        body += '<details><summary>查看系列章节</summary><ol>' + "".join(
            f'<li><a href="{ctx.rel(path, e["url"])}">{esc(e["title"])}</a></li>'
            for e in children) + "</ol></details>"
    return body + "</article>"


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
    template = Template((ctx.root / "templates/home.html").read_text(encoding="utf-8"))
    body = template.substitute(bio=bio, topics=topics, papers=papers,
                               count=len(rows),
                               recent="".join(card(ctx, e, "/") for e in rows[:4]),
                               featured="".join(card(ctx, e, "/") for e in rows
                                                if e.get("featured")))
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
    body = ('<p class="eyebrow">Research &amp; Study Notes</p><h1>博客与笔记</h1>'
            '<p class="intro">按主题阅读，或搜索文章与系列章节。日期表示内容更新时间；'
            '无依据的日期保留为待确认。科研材料的逐项事实复核仍在进行。</p>'
            '<form id="catalog-form" class="catalog-controls" action="/blog/" method="get">'
            '<label class="catalog-field"><span class="catalog-label">关键词</span>'
            '<input id="filter-q" type="search" name="q" placeholder="试试 ELBO、PPO 或 KV Cache"></label>' +
            select("topic", "技术主题", ctx.site["topics"]) +
            select("type", "内容类型", ctx.site["types"]) +
            '<label class="catalog-field"><span class="catalog-label">排序</span>'
            '<select name="sort" id="filter-sort"><option value="updated-desc">最近更新</option>'
            '<option value="title">标题</option></select></label>'
            '<button type="submit">查找</button><button type="button" id="clear-filters">清除条件</button>'
            '</form><p id="catalog-notice" role="status"></p>'
            '<p id="result-count" aria-live="polite"></p>'
            '<noscript><p>当前未启用 JavaScript。以下列出全部文章；'
            '系列卡片内可直接浏览章节，筛选需启用 JavaScript。</p></noscript>'
            '<section aria-label="本地文章"><div id="catalog-results" class="note-grid">' +
            "".join(card(ctx, e, chapters=True) for e in local) +
            '</div><p id="no-results" class="no-results" hidden>没有匹配内容。'
            '<a href="/blog/">清除条件，查看全部文章</a></p></section>'
            '<section id="external"><h2>独立子站</h2><p>这些资源由独立仓库维护。</p>'
            '<div class="note-grid">' + "".join(card(ctx, e) for e in external) +
            '</div></section><section id="archive"><h2>历史版本</h2><div class="note-grid">' +
            "".join(card(ctx, e) for e in archived) + "</div></section>")
    data = {"entries": rows, "topics": ctx.site["topics"], "types": ctx.site["types"],
            "compatibility": ctx.redirects.get("query_compatibility", {}).get("blog", {})}
    ctx.write("/blog/catalog.json", json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    ctx.page("/blog/", "博客与笔记", body, "分类目录、关键词搜索与系列章节。",
             script="/assets/site/catalog.js")
