"""Shared rendering API. All writes are confined to an external artifact."""
from pathlib import Path, PurePosixPath
import html
import json
import posixpath
import re
import hashlib
from urllib.parse import urlsplit

import markdown
import yaml

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = Path("/tmp/my-blogs-site-build")
START, END = "<!-- SITE:NAV:START -->", "<!-- SITE:NAV:END -->"
PUBLIC_EXTENSIONS = {
    ".html", ".css", ".js", ".pdf", ".svg", ".ico", ".woff", ".woff2",
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif", ".json", ".xml", ".txt",
}
PRIVATE_PARTS = {
    "content", "templates", "scripts", "docs", "licenses", "drafts",
    "__pycache__", "node_modules", ".automation", ".github", ".git", ".venv",
}


def input_digest(root):
    """Fingerprint authoritative build inputs, without Git/cache/runtime files."""
    root = Path(root)
    paths = [p for folder in ("content", "assets", "templates", "scripts")
             for p in (root / folder).rglob("*")
             if p.is_file() and not any(part.startswith(".") or part == "__pycache__"
                                       for part in p.relative_to(root).parts)
             and p.suffix != ".pyc"]
    paths.append(root / "requirements.txt")
    paths.append(root / ".automation/check-frontier.py")
    digest = hashlib.sha256()
    for path in sorted(paths):
        digest.update(path.relative_to(root).as_posix().encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def external_output(output, root=ROOT):
    output, root = Path(output).resolve(), Path(root).resolve()
    if output == root or output.is_relative_to(root) or root.is_relative_to(output):
        raise ValueError("Output must be outside the source repository")
    if output == Path(output.anchor) or output in {Path("/tmp"), Path("/private/tmp")}:
        raise ValueError("Output must be a dedicated artifact directory")
    return output


def route_path(url):
    """Convert a local public URL or artifact path into a relative file path."""
    parsed = urlsplit(str(url))
    if parsed.scheme or parsed.netloc or parsed.query or parsed.fragment:
        raise ValueError(f"Expected a local route without query/fragment: {url}")
    path = parsed.path.lstrip("/")
    if path == ".nojekyll":
        return path
    parts = PurePosixPath(path).parts
    if ".." in parts or "\\" in path or any(p.startswith(".") for p in parts):
        if path != ".nojekyll":
            raise ValueError(f"Unsafe public route: {url}")
    if not path or path.endswith("/"):
        path += "index.html"
    elif not PurePosixPath(path).suffix:
        path += "/index.html"
    return path


def public_file(path):
    parts = PurePosixPath(path).parts
    return bool(parts) and (path == ".nojekyll" or PurePosixPath(path).suffix.lower() in PUBLIC_EXTENSIONS) and not any(
        p in PRIVATE_PARTS or (p.startswith(".") and p != ".nojekyll") for p in parts
    ) and (path == ".nojekyll" or PurePosixPath(path).suffix in PUBLIC_EXTENSIONS)


def rel(path, target):
    parsed = urlsplit(str(target))
    if parsed.scheme or parsed.netloc:
        return str(target)
    target_path = route_path(parsed.path)
    result = posixpath.relpath(target_path, posixpath.dirname(route_path(path)) or ".")
    if parsed.query:
        result += "?" + parsed.query
    if parsed.fragment:
        result += "#" + parsed.fragment
    return result


def load_md(path):
    text = Path(path).read_text(encoding="utf-8")
    match = re.match(r"\A---\s*\n(.*?)\n---(?:\s*\n|$)(.*)\Z", text, re.S)
    if not match:
        raise ValueError(f"Missing YAML front matter: {path}")
    metadata = yaml.safe_load(match[1])
    if not isinstance(metadata, dict):
        raise ValueError(f"Invalid YAML front matter: {path}")
    return metadata, match[2].strip()


def md(text):
    if "{%" in text or "{{" in text:
        raise ValueError("Unconverted Jekyll markup")
    return markdown.markdown(text, extensions=["extra", "sane_lists", "toc"])


class BuildContext:
    def __init__(self, root, output, site, entries, publications, metadata, redirects):
        self.root, self.output = Path(root).resolve(), external_output(output, root)
        self.site, self.entries = site, entries
        self.catalog = entries
        self.by_id = {entry["id"]: entry for entry in entries}
        self.publications, self.metadata, self.redirects = publications, metadata, redirects
        self.generated = set()
        self.rel, self.md, self.load_md = rel, md, load_md

    def write(self, path, text):
        path = route_path(path)
        if not public_file(path):
            raise ValueError(f"File is not allowlisted for publication: {path}")
        if path in self.generated:
            raise ValueError(f"Output route collision: {path}")
        destination = self.output / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(text, encoding="utf-8")
        self.generated.add(path)

    def copy(self, source, path):
        path = route_path(path)
        source = Path(source).resolve()
        if not source.is_relative_to(self.root) or not source.is_file():
            raise ValueError(f"Asset source escapes repository or is missing: {source}")
        if not public_file(path):
            raise ValueError(f"File is not allowlisted for publication: {path}")
        if path in self.generated:
            raise ValueError(f"Output route collision: {path}")
        destination = self.output / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(source.read_bytes())
        self.generated.add(path)

    def canonical(self, path):
        path = route_path(path)
        if path.endswith("index.html"):
            path = path[:-10]
        return self.site["url"].rstrip("/") + "/" + path

    def navigation(self, path):
        path = route_path(path)
        links = []
        for item in self.site["navigation"]:
            target = route_path(item["url"])
            active = path == target or (
                target == "blog/index.html" and any(
                    entry["origin"] == "local" and route_path(entry["url"]) == path
                    for entry in self.entries
                )
            )
            current = ' aria-current="page"' if active else ""
            links.append(f'<a href="{html.escape(rel(path, item["url"]), quote=True)}"{current}>'
                         f'{html.escape(item["label"])}</a>')
        return (f'{START}\n<a class="site-skip" href="#site-main">跳转到正文</a>'
                '<nav class="site-nav" aria-label="主导航">'
                f'<a class="site-brand" href="{rel(path, "/")}">'
                '<span class="site-monogram" aria-hidden="true">S.</span>Stein\'s Notes</a>'
                f'<div class="site-links">{"".join(links)}</div></nav>\n{END}')

    def footer(self, path):
        commit = self.metadata["commit"]
        label = (commit[:12] if commit else "unavailable") + (
            " + local changes" if self.metadata["dirty"] else ""
        )
        source = self.site.get("repository", "https://github.com/stein-wang0226/stein-wang0226.github.io")
        return ('<footer class="site-footer"><span>Yuxiang Wang · Research &amp; Notes</span>'
                f'<a href="{html.escape(source, quote=True)}">GitHub · Source</a>'
                f'<a class="site-build" href="{rel(path, "build-info.json")}">Build {html.escape(label)}</a></footer>')

    def page(self, path, title, body, description="", script="", lang="zh-CN"):
        script_tag = (f'<script defer src="{rel(path, script)}"></script>' if script else "")
        base = '<base href="/"><meta name="robots" content="noindex">' if route_path(path) == "404.html" else ""
        self.write(path, f'''<!DOCTYPE html>
<html lang="{html.escape(lang, quote=True)}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} — Yuxiang Wang</title>{base}
<meta name="description" content="{html.escape(description or title, quote=True)}">
<link rel="canonical" href="{self.canonical(path)}">
<link rel="stylesheet" href="{rel(path, "assets/site/site.css")}">{script_tag}
</head><body class="site-body">
{self.navigation(path)}
<main class="site-page" id="site-main" tabindex="-1">{body}</main>
{self.footer(path)}
</body></html>
''')

    def redirect(self, path, target, preserve_query=True, preserve_fragment=True):
        destination = rel(path, target)
        query = "location.search" if preserve_query else '""'
        fragment = "location.hash" if preserve_fragment else '""'
        # Fixed target queries/fragments win; otherwise preserve the old URL.
        self.write(path, f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Page moved — Yuxiang Wang</title>
<link rel="canonical" href="{html.escape(self.canonical(urlsplit(target).path), quote=True)}">
</head><body><p>This page has moved.
<a href="{html.escape(destination, quote=True)}">Continue reading</a>.</p>
<script>const target = new URL({json.dumps(destination)}, location.href);
if (!target.search) target.search = {query};
if (!target.hash) target.hash = {fragment};
location.replace(target.href);</script>
</body></html>
''')
