"""Build from authoritative inputs into a new, manifest-allowlisted artifact."""
from pathlib import Path
import hashlib
import html
import json
import os
import subprocess
import tempfile

from catalog import load_content
from render import BuildContext, DEFAULT_OUTPUT, FAVICON_LINK, ROOT, external_output, input_digest, load_md, mark_cjk_runs, md, publication_date, route_path


def git_metadata(root):
    def git(*args):
        result = subprocess.run(["git", "-C", str(root), *args], check=True,
                                capture_output=True, text=True)
        return result.stdout.strip()
    try:
        return {"commit": git("rev-parse", "HEAD"),
                "dirty": bool(git("status", "--porcelain", "--untracked-files=all"))}
    except (subprocess.CalledProcessError, OSError) as exc:
        raise ValueError("Cannot read actual Git HEAD/dirty state from source repository") from exc


def render_academic(ctx):
    dated_cards, manuscript_cards = [], []
    for paper in ctx.publications:
        meta, body, url = paper["meta"], paper["body"], paper["url"]
        link = (f'<p><a href="{html.escape(meta["paperurl"], quote=True)}">Read the paper ↗</a></p>'
                if meta.get("paperurl") else "")
        citation = f'<h2 id="citation">Citation</h2>{md(meta["citation"])}' if meta.get("citation") else ""
        ctx.page(url, meta["title"], '<p class="eyebrow">Publication</p>'
                 f'<h1>{html.escape(meta["title"])}</h1>'
                 f'<p class="paper-meta">{html.escape(publication_date(meta))} · '
                 f'{html.escape(meta["venue"])}</p>{link}'
                 f'<article class="prose">{md(body)}{citation}</article>', meta["excerpt"], lang="en",
                 script="/assets/site/scroll-region.js")
        cards = dated_cards if meta["date"] else manuscript_cards
        cards.append('<article class="publication-card">'
                     f'<p class="paper-meta">{html.escape(publication_date(meta))} · '
                     f'{html.escape(meta["venue"])}</p>'
                     f'<h2><a href="{ctx.rel("/publications/", url)}">{html.escape(meta["title"])}</a></h2>'
                     f'<p>{html.escape(meta["excerpt"])}</p></article>')
    ctx.page("/publications/", "Publications", '<p class="eyebrow">Research</p><h1>Publications</h1>'
             '<p class="intro">Agent post-training, computer-use recovery, diffusion language models, '
             'and dynamic graph learning. Status follows the latest author-supplied resume; '
             'individual records distinguish it from public preprint metadata. '
             '<a href="https://scholar.google.com/citations?hl=zh-CN&amp;user=PCoqb3wAAAAJ">'
             'Google Scholar ↗</a></p>'
             + ('<section><h2>Manuscripts under review</h2>' + "".join(manuscript_cards) + '</section>'
                if manuscript_cards else "")
             + '<section><h2>Publications &amp; Preprints</h2>' + "".join(dated_cards) + '</section>',
             lang="en")
    for record in ctx.site["pages"]:
        meta, body = load_md(ctx.root / record["source"])
        if record["id"] == "my-work":
            from views import render_my_work
            render_my_work(ctx, record, meta, body)
            continue
        addition = ""
        if record["id"] == "cv":
            addition = '<h2 id="publications">Publications</h2><ul>' + "".join(
                f'<li><a href="{ctx.rel(record["url"], paper["url"])}">'
                f'{html.escape(paper["meta"]["title"])}</a> · '
                f'{html.escape(paper["meta"]["venue"])}</li>' for paper in ctx.publications
            ) + "</ul>"
        elif record["id"] == "about":
            addition = '<h2 id="selected-publications">Selected Publications</h2><ul>' + "".join(
                f'<li><a href="{ctx.rel(record["url"], paper["url"])}">'
                f'{html.escape(paper["meta"]["title"])}</a> · '
                f'{html.escape(paper["meta"]["venue"])}</li>' for paper in ctx.publications
                if paper["slug"] in ctx.site["publications"]["featured"]
            ) + '</ul><h2 id="research-and-notes">Research &amp; Notes</h2>' \
                       '<p><a href="' + ctx.rel(record["url"], "/publications/") + \
                       '">Publications</a> · <a href="' + ctx.rel(record["url"], "/blog/") + \
                       '">博客与笔记</a></p>'
        title = record["title"]
        article = mark_cjk_runs(f'<article class="prose">{md(body)}{addition}</article>')
        ctx.page(record["url"], title, f'<p class="eyebrow">{html.escape(title)}</p>'
                 f'<h1>{html.escape(meta.get("title", title))}</h1>'
                 f'{article}', lang="en",
                 styles=("/assets/site/profile.css",))
    ctx.page("404.html", "Page not found", '<p class="eyebrow">404</p><h1>Page not found</h1>'
             '<p>Browse the <a href="/blog/">blog</a> or return to '
             '<a href="/">the homepage</a>.</p>', lang="en")


def render_artifact(ctx):
    # These modules own presentation only; source loading and output writes stay here.
    from reading import decorate
    from views import render_blog, render_home
    from citations import render_citations
    from course import parent_of, compatibility, decorate_course, relocated_directory
    from mathematics import decorate_math

    for asset in ctx.site["assets"]:
        ctx.copy(ctx.root / asset["source"], asset["url"])
    # Shared presentation assets are a confined public namespace, not a repo scan.
    explicit_assets = {route_path(asset["url"]) for asset in ctx.site["assets"]}
    for asset in sorted((ctx.root / "assets/site").rglob("*")):
        relative = asset.relative_to(ctx.root).as_posix()
        if asset.is_file() and asset.suffix.lower() in {".css", ".js", ".woff", ".woff2", ".txt"}:
            if relative not in explicit_assets:
                ctx.copy(asset, relative)
    render_academic(ctx)
    archive_record = ctx.root / "docs/organization-changes-20261115.json"
    if archive_record.is_file():
        history = json.loads(archive_record.read_text())
        links = []
        for row in history["pages"]:
            ctx.copy(ctx.root / row["archive"], row["archive"])
            entry = ctx.by_id[row["id"]]
            links.append(f'<li><a download href="{ctx.rel("/blog/history/", "/" + row["archive"])}">'
                         f'{html.escape(entry["title"])}：重编前原稿</a></li>')
        ctx.page("/blog/history/", "重编前的原稿", '<h1>重编前的原稿</h1>'
                 '<p>2026年11月15日重编前的源稿逐字保留为文本下载。当前学习内容请从'
                 '<a href="../#learning-paths">完整学习主线</a>进入。</p><ul>' +
                 "".join(links) + '</ul>')
    for record in ctx.entries:
        if record["origin"] != "local" or record["status"] == "draft":
            continue
        if parent_of(record, ctx.by_id):
            compatibility(ctx, record)
            continue
        source = ctx.root / record["source"]
        text = source.read_text(encoding="utf-8")
        if source.suffix == ".md":
            _, body = load_md(source)
            # Ordinary Markdown uses the same reading callback as legacy full HTML.
            text = ('<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">'
                    '<meta name="viewport" content="width=device-width,initial-scale=1">'
                    f'<title>{html.escape(record["title"])}</title></head>'
                    '<body class="site-body">'
                    f'<main class="site-page reading-markdown"><article class="prose">{md(body)}'
                    '</article></main></body></html>')
        text = relocated_directory(ctx, record, text)
        text = (decorate_course(ctx, record, text) if record.get("reading_mode") == "longform"
                else decorate(ctx, record, text))
        text = decorate_math(ctx, record, text)
        if not isinstance(text, str):
            raise ValueError(f"reading.decorate must return HTML text for {record['id']}")
        ctx.write(record["url"], text)
        # Post-owned non-HTML resources retain URL-relative locations.
        if record["kind"] == "post" and record["status"] != "archived":
            for asset in sorted(source.parent.rglob("*")):
                if asset.is_file() and asset.suffix.lower() in {
                    ".css", ".js", ".svg", ".png", ".jpg", ".jpeg", ".gif", ".webp",
                    ".avif", ".ico", ".pdf", ".woff", ".woff2",
                }:
                    relative = asset.relative_to(source.parent).as_posix()
                    target = (Path(route_path(record["url"])).parent / relative).as_posix()
                    ctx.copy(asset, target)
    render_home(ctx)
    render_blog(ctx)
    render_citations(ctx)
    defaults = ctx.redirects.get("defaults", {})
    for item in ctx.redirects["redirects"]:
        ctx.redirect(item["from"], item["to"],
                     item.get("preserve_query", defaults.get("preserve_query", True)),
                     item.get("preserve_fragment", defaults.get("preserve_fragment", True)))
    for item in ctx.redirects.get("copies", []):
        source = ctx.output / route_path(item["to"])
        ctx.write(item["from"], source.read_text(encoding="utf-8")) if source.suffix in {
            ".html", ".css", ".js", ".json", ".txt", ".xml", ".svg"
        } else copy_artifact_asset(ctx, source, item["from"])
    redirect_paths = {route_path(item["from"]) for item in ctx.redirects["redirects"]}
    redirect_paths.update(route_path(e["url"]) for e in ctx.entries if parent_of(e, ctx.by_id))
    urls = sorted({ctx.canonical(path) for path in ctx.generated
                   if path.endswith(".html") and path != "404.html" and path not in redirect_paths
                   and not path.startswith(("wyx0226.github.io/", "legacy/"))})
    ctx.write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n'
              '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
              "\n".join(f"<url><loc>{html.escape(url)}</loc></url>" for url in urls) +
              "\n</urlset>\n")
    ctx.write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {ctx.site['url']}/sitemap.xml\n")
    ctx.write(".nojekyll", "")
    # Pages that own their head still share the icon and canonical URL; the catalog
    # supplies an authored description where the template has none.
    by_route = {route_path(entry["url"]): entry for entry in ctx.entries
                if entry.get("origin") == "local"}
    for path in ctx.generated:
        if not path.endswith(".html"):
            continue
        target = ctx.output / path
        text = target.read_text(encoding="utf-8")
        additions = []
        if 'rel="icon"' not in text:
            additions.append(FAVICON_LINK)
        if 'rel="canonical"' not in text:
            additions.append(f'<link rel="canonical" href="{ctx.canonical(path)}">')
        entry = by_route.get(path)
        if 'name="description"' not in text and entry and entry.get("summary"):
            additions.append('<meta name="description" content="'
                             + html.escape(entry["summary"], quote=True) + '">')
        # Archived pages cannot be edited at the source; the catalog title distinguishes
        # the historical copy from the current manual in the browser tab.
        title_changed = False
        if entry and entry.get("status") == "archived":
            start = text.find("<title>")
            end = text.find("</title>", start + 7) if start != -1 else -1
            if start != -1 and end != -1:
                title = html.escape(entry["title"])
                title_changed = text[start + 7:end] != title
                text = text[:start + 7] + title + text[end:]
        if additions or title_changed:
            if additions:
                text = text.replace("</head>", "".join(additions) + "</head>", 1)
            target.write_text(text, encoding="utf-8")
    files = {path: hashlib.sha256((ctx.output / path).read_bytes()).hexdigest()
             for path in sorted(ctx.generated)}
    ctx.write("build-info.json", json.dumps(
        {"schema_version": 1, **ctx.metadata, "files": files}, ensure_ascii=False,
        indent=2, sort_keys=True) + "\n")


def copy_artifact_asset(ctx, source, target):
    target = route_path(target)
    if target in ctx.generated:
        raise ValueError(f"Output route collision: {target}")
    path = ctx.output / target
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(source.read_bytes())
    ctx.generated.add(target)


def build(output=DEFAULT_OUTPUT, root=ROOT):
    root = Path(root).resolve()
    output = external_output(output, root)
    content = load_content(root)
    metadata = git_metadata(root)
    metadata["input_digest"] = input_digest(root)
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists() and (not output.is_dir() or
                            (any(output.iterdir()) and not (output / "build-info.json").is_file())):
        raise ValueError(f"Refusing to replace a non-owned output directory: {output}")
    with tempfile.TemporaryDirectory(prefix=output.name + "-stage-", dir=output.parent) as temporary:
        stage = Path(temporary)
        ctx = BuildContext(root, stage, *content[:3], metadata, content[3])
        render_artifact(ctx)
        from check import validate
        errors, count = validate(stage, root, content)
        if errors:
            raise ValueError("Build artifact validation failed:\n" + "\n".join(errors))
        # Keep the previous successful artifact intact until the fresh one passes.
        if output.exists():
            backup = stage / "_previous"
            os.replace(output, backup)
            try:
                os.replace(stage, output)
            except OSError:
                os.replace(backup, output)
                raise
            # The old tree moved along with stage; remove only that owned tree.
            import shutil
            shutil.rmtree(output / "_previous")
        else:
            os.replace(stage, output)
    return count, len(ctx.generated)
