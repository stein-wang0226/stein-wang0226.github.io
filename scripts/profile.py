"""Read-only local/remote checks and GitHub-rendered Profile preview."""
import argparse
import base64
from datetime import datetime, timezone
import hashlib
from html import escape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urlsplit

from catalog import load_content
from render import ROOT, load_md, md, route_path


class ProfileHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids, self.tags = [], set(), []
        self.images = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append(tag)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])
        if tag == "img":
            self.images.append(attrs)


def parse_html(text):
    parser = ProfileHTML()
    parser.feed(text)
    return parser


def profile_assets(root=ROOT):
    directory = Path(root) / "docs/github-profile/assets"
    manifest = directory / "manifest.json"
    if not manifest.is_file():
        return []
    records = json.loads(manifest.read_text())["assets"]
    for record in records:
        filename = record["file"]
        if Path(filename).name != filename or Path(filename).suffix != ".jpg":
            raise ValueError(f"Invalid Profile asset filename: {filename}")
    return records


def blob_sha(payload):
    return hashlib.sha1(f"blob {len(payload)}\0".encode() + payload).hexdigest()


def local_check(root=ROOT):
    root = Path(root).resolve()
    site, entries, publications, redirects = load_content(root)
    text = (root / "docs/github-profile/README.md").read_text(encoding="utf-8")
    parser = parse_html(md(text))
    errors = []
    if len(re.findall(r"^# ", text, re.M)) != 1:
        errors.append("Profile must have one top-level name heading")
    if any(tag in parser.tags for tag in ("script", "style", "iframe")):
        errors.append("Profile contains tags GitHub does not support for this layout")
    if re.search(r"\bstyle\s*=", text, re.I):
        errors.append("Profile cannot depend on inline CSS")
    if re.search(r"Terminal-Bench Science fork|my fork of", text, re.I):
        errors.append("Remove the ordinary fork from curated Profile work")
    if "TEMPLATE:EMPTY" in text:
        errors.append("Profile contains an empty template")

    records = profile_assets(root)
    if len({record["sha256"] for record in records}) != len(records):
        errors.append("Profile research images must not be duplicated pending responses")
    assets = {f"./assets/{record['file']}": record for record in records}
    image_sources = [image.get("src") for image in parser.images]
    if set(image_sources) != set(assets):
        errors.append("Profile images must exactly match the local asset manifest")
    for image in parser.images:
        source = image.get("src")
        if not image.get("alt", "").strip():
            errors.append(f"Profile image needs useful alternative text: {source}")
        if image.get("height"):
            errors.append(f"Profile image must preserve its aspect ratio: {source}")
        if source not in assets:
            continue
        record = assets[source]
        path = root / "docs/github-profile/assets" / record["file"]
        if not path.is_file():
            errors.append(f"Missing Profile image: {path}")
        elif hashlib.sha256(path.read_bytes()).hexdigest() != record["sha256"]:
            errors.append(f"Profile image differs from its manifest: {source}")

    pages = {route_path("/"): None, route_path("/blog/"): None,
             route_path("/publications/"): None}
    for entry in entries:
        if entry["origin"] == "local" and entry["status"] != "draft":
            pages[route_path(entry["url"])] = root / entry["source"]
    for page in site["pages"]:
        pages[route_path(page["url"])] = root / page["source"]
    for paper in publications:
        pages[route_path(paper["url"])] = None
    for asset in site["assets"]:
        pages[route_path(asset["url"])] = None
    for redirect in redirects["redirects"]:
        pages[route_path(redirect["from"])] = None
    for copy in redirects.get("copies", []):
        pages[route_path(copy["from"])] = None

    host = urlsplit(site["url"]).netloc
    internal = 0
    for link in parser.links:
        parsed = urlsplit(link)
        if parsed.scheme == "mailto":
            continue
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            errors.append(f"Profile links must be absolute URLs: {link}")
            continue
        if parsed.netloc != host:
            continue
        internal += 1
        route = route_path(parsed.path)
        if route not in pages:
            errors.append(f"Profile site link has no published route: {link}")
        elif parsed.fragment and pages[route] is not None:
            source = pages[route]
            if source.suffix == ".md":
                _, body = load_md(source)
                content = md(body)
            else:
                content = source.read_text(encoding="utf-8")
            if unquote(parsed.fragment) not in parse_html(content).ids:
                errors.append(f"Profile link has no source anchor: {link}")
    settings = json.loads((root / "docs/github-profile/settings.json").read_text())
    if set(settings) != {"name", "bio", "blog"} or not all(
            isinstance(value, str) and value.strip() for value in settings.values()):
        errors.append("Profile settings must contain nonempty name, bio and blog")
    if settings.get("blog") != site["url"].rstrip("/") + "/":
        errors.append("Profile website must use the canonical root site")
    if len(settings.get("bio", "")) > 160:
        errors.append("GitHub bio exceeds 160 characters")
    return {"ok": not errors, "errors": errors,
            "links": len(parser.links), "site_links": internal,
            "images": len(parser.images),
            "image_bytes": sum(record["bytes"] for record in records),
            "local_sha256": hashlib.sha256(text.encode()).hexdigest()}


def gh_api(gh, endpoint, payload=None):
    command = [gh, "api", endpoint]
    data = None
    if payload is not None:
        command += ["--input", "-"]
        data = json.dumps(payload)
    result = subprocess.run(command, input=data, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or f"gh api failed for {endpoint}")
    return result.stdout


def remote_status(gh, root=ROOT):
    root = Path(root).resolve()
    expected = json.loads((root / "docs/github-profile/settings.json").read_text())
    local = (root / "docs/github-profile/README.md").read_bytes()
    remote = json.loads(gh_api(gh, "repos/stein-wang0226/stein-wang0226/readme"))
    remote_bytes = base64.b64decode(remote["content"])
    account = json.loads(gh_api(gh, "users/stein-wang0226"))
    pinned_data = json.loads(gh_api(gh, "graphql", {
        "query": '{ user(login:"stein-wang0226") { pinnedItems(first:6, types:REPOSITORY) '
                 '{ nodes { ... on Repository { nameWithOwner description isFork url } } } } }'
    }))
    if pinned_data.get("errors"):
        raise RuntimeError("GitHub did not return pinned repositories")
    pins = pinned_data["data"]["user"]["pinnedItems"]["nodes"]
    pin_names = [p["nameWithOwner"].split("/")[-1] for p in pins]
    field_status = {key: {"actual": account.get(key), "expected": value,
                          "synced": account.get(key) == value}
                    for key, value in expected.items()}
    tree = json.loads(gh_api(
        gh, "repos/stein-wang0226/stein-wang0226/git/trees/main?recursive=1"))
    remote_blobs = {item["path"]: item["sha"] for item in tree["tree"]
                    if item["type"] == "blob"}
    assets = []
    for record in profile_assets(root):
        filename = record["file"]
        payload = (root / "docs/github-profile/assets" / filename).read_bytes()
        actual = remote_blobs.get(f"assets/{filename}")
        assets.append({"file": filename, "synced": actual == blob_sha(payload),
                       "remote_blob_sha": actual,
                       "local_sha256": hashlib.sha256(payload).hexdigest()})
    return {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "read_only": True,
        "readme": {"synced": local == remote_bytes, "remote_blob_sha": remote["sha"],
                   "local_sha256": hashlib.sha256(local).hexdigest(),
                   "remote_sha256": hashlib.sha256(remote_bytes).hexdigest()},
        "assets": {"synced": all(asset["synced"] for asset in assets),
                   "files": assets},
        "account": field_status,
        "pinned": pins,
        "recommendations": {
            "preferred_order": ["stein-wang0226.github.io", "trainable-masked-diffusion", "STM"],
            "main_site_is_pinned": "stein-wang0226.github.io" in pin_names,
            "low_priority_pins": [name for name in pin_names
                                  if name in {"stein-wang0226", "algorithms"}],
        },
        "note": "README, account fields and pins are independent; account updates need user scope.",
    }


PREVIEW_CSS = """
:root{color-scheme:light dark;--bg:#fff;--fg:#1f2328;--muted:#59636e;--line:#d1d9e0;--link:#0969da;--tint:#f6f8fa}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans","PingFang SC",sans-serif}
aside{padding:12px 24px;border-bottom:1px solid var(--line);background:var(--tint);color:var(--muted);font-size:13px}
main{max-width:900px;margin:32px auto;padding:32px;border:1px solid var(--line);border-radius:6px}
article{overflow-wrap:break-word}h1,h2{padding-bottom:.3em;border-bottom:1px solid var(--line);line-height:1.25;margin:24px 0 16px}
h1{font-size:2em;margin-top:0}h2{font-size:1.5em}h3{font-size:1.12em;margin:12px 0}
p,blockquote,table,ul,details{margin:0 0 16px}a{color:var(--link);text-decoration:none}a:hover{text-decoration:underline}
img{max-width:100%;height:auto;vertical-align:middle}
blockquote{border-left:.25em solid var(--line);color:var(--muted);padding:0 1em}blockquote p:last-child{margin-bottom:0}
table{border-collapse:collapse;display:block;width:max-content;max-width:100%;overflow:auto}td,th{padding:10px 13px;border:1px solid var(--line);text-align:left}
tr:nth-child(2n){background:var(--tint)}td p:last-child{margin-bottom:2px}td h3{margin-top:12px}
details{padding:8px 0}summary{cursor:pointer;margin-bottom:12px}li{margin:6px 0}a:focus-visible,summary:focus-visible{outline:2px solid var(--link);outline-offset:4px}
.anchor{display:none}@media(prefers-color-scheme:dark){:root{--bg:#0d1117;--fg:#f0f6fc;--muted:#9198a1;--line:#3d444d;--link:#4493f8;--tint:#151b23}}
@media(max-width:600px){main{margin:12px;padding:20px 16px}h1{font-size:1.65em}td,th{padding:8px 10px}aside{padding:10px 12px}}
"""


def render_preview(gh, output, root=ROOT):
    """Use GitHub's sanitizer; only the external preview gets simulated CSS."""
    output = Path(output).expanduser().resolve()
    if output == ROOT or output.is_relative_to(Path(root).resolve()):
        raise ValueError("Preview output must be outside the source repository")
    if output.suffix != ".html" or not output.parent.is_dir():
        raise ValueError("Preview requires an HTML filename in an existing directory")
    text = (Path(root) / "docs/github-profile/README.md").read_text(encoding="utf-8")
    rendered = gh_api(gh, "markdown", {
        "text": text, "mode": "gfm", "context": "stein-wang0226/stein-wang0226",
    })
    # Show the candidate images before publication, independent of remote assets.
    image_data = {}
    for record in profile_assets(root):
        path = Path(root) / "docs/github-profile/assets" / record["file"]
        image_data[record["file"]] = (
            "data:image/jpeg;base64," + base64.b64encode(path.read_bytes()).decode())

    def embed_image(match):
        filename = Path(unquote(urlsplit(match.group(2)).path)).name
        if filename not in image_data:
            return match.group(0)
        return match.group(1) + escape(image_data[filename], quote=True) + match.group(3)

    rendered = re.sub(r'(\bsrc=")([^"]+)(")', embed_image, rendered)
    output.write_text(
        '<!doctype html><html lang="en"><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>Yuxiang Wang · GitHub Profile preview</title>'
        f'<style>{PREVIEW_CSS}</style><body>'
        '<aside>Local preview · GitHub-rendered Markdown with simulated platform styles. '
        'This version has not been published.</aside>'
        f'<main><article class="markdown-body">{rendered}</article></main></body></html>',
        encoding="utf-8")
    return {"output": str(output), "rendered_by": "GitHub Markdown API",
            "embedded_images": len(image_data), "published": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check")
    check.add_argument("--root", type=Path, default=ROOT,
                       help="Content snapshot to use as the link-validation baseline")
    status = sub.add_parser("status")
    status.add_argument("--gh", default="gh")
    preview = sub.add_parser("preview")
    preview.add_argument("--gh", default="gh")
    preview.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = (local_check(args.root) if args.command == "check"
                  else remote_status(args.gh) if args.command == "status"
                  else render_preview(args.gh, args.output))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return int(result.get("ok") is False)
    except (OSError, RuntimeError, ValueError, KeyError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
