"""Build from authoritative inputs into a new, manifest-allowlisted artifact."""
from pathlib import Path
import hashlib
import html
import json
import os
import subprocess
import tempfile

from catalog import load_content
from render import BuildContext, DEFAULT_OUTPUT, ROOT, external_output, input_digest, load_md, md, publication_date, route_path


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
                 f'<article class="prose">{md(body)}{citation}</article>', meta["excerpt"], lang="en")
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
        ctx.page(record["url"], title, f'<p class="eyebrow">{html.escape(title)}</p>'
                 f'<h1>{html.escape(meta.get("title", title))}</h1>'
                 f'<article class="prose">{md(body)}{addition}</article>', lang="en",
                 styles=("/assets/site/profile.css",))
    ctx.page("404.html", "Page not found", '<p class="eyebrow">404</p><h1>Page not found</h1>'
             '<p>Browse the <a href="/blog/">blog</a> or return to '
             '<a href="/">the homepage</a>.</p>', lang="en")


def render_artifact(ctx):
    # These modules own presentation only; source loading and output writes stay here.
    from reading import decorate
    from views import render_blog, render_home
    from citations import render_citations

    for asset in ctx.site["assets"]:
        ctx.copy(ctx.root / asset["source"], asset["url"])
    # Shared presentation assets are a confined public namespace, not a repo scan.
    explicit_assets = {route_path(asset["url"]) for asset in ctx.site["assets"]}
    for asset in sorted((ctx.root / "assets/site").rglob("*")):
        relative = asset.relative_to(ctx.root).as_posix()
        if asset.is_file() and asset.suffix.lower() in {".css", ".js", ".woff", ".woff2"}:
            if relative not in explicit_assets:
                ctx.copy(asset, relative)
    render_academic(ctx)
    for record in ctx.entries:
        if record["origin"] != "local" or record["status"] == "draft":
            continue
        source = ctx.root / record["source"]
        text = source.read_text(encoding="utf-8")
        if source.suffix == ".md":
            _, body = load_md(source)
            # Ordinary Markdown uses the same reading callback as legacy full HTML.
            text = ('<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">'
                    '<meta name="viewport" content="width=device-width,initial-scale=1">'
                    f'<title>{html.escape(record["title"])}</title></head><body>'
                    f'<article class="prose">{md(body)}</article></body></html>')
        text = decorate(ctx, record, text)
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
    urls = sorted({ctx.canonical(path) for path in ctx.generated
                   if path.endswith(".html") and path != "404.html" and path not in redirect_paths
                   and not path.startswith(("wyx0226.github.io/", "legacy/"))})
    ctx.write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n'
              '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
              "\n".join(f"<url><loc>{html.escape(url)}</loc></url>" for url in urls) +
              "\n</urlset>\n")
    ctx.write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {ctx.site['url']}/sitemap.xml\n")
    ctx.write(".nojekyll", "")
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
