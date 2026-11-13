"""Load and validate the explicit version-1 content contract."""
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
import copy
import json
import re
from urllib.parse import urlsplit

from render import load_md, public_file, route_path


def read_json(path):
    def unique_keys(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"{path}: duplicate JSON key {key}")
            result[key] = value
        return result
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_keys)


def source_path(root, value):
    if not isinstance(value, str) or not value.startswith(("content/", "assets/")):
        raise ValueError(f"source must be a repository-relative content/ or assets/ path: {value}")
    path = (root / value).resolve()
    if not path.is_relative_to(root) or not path.is_file():
        raise ValueError(f"source does not exist or escapes repository: {value}")
    if any(part.startswith(".") or part == "__pycache__" for part in Path(value).parts):
        raise ValueError(f"source must not reference private/cache files: {value}")
    return path


def content_date(value, label):
    if value is None or value == "":
        return None
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise ValueError(f"{label}: expected an ISO content date or null")
    try:
        return date.fromisoformat(value).isoformat()
    except ValueError as exc:
        raise ValueError(f"{label}: invalid content date {value}") from exc


class UpdatedElement(HTMLParser):
    def __init__(self, element_id, attribute):
        super().__init__()
        self.element_id, self.attribute, self.values = element_id, attribute, []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id") == self.element_id:
            self.values.append(attrs.get(self.attribute))


def load_content(root):
    root = Path(root).resolve()
    site = read_json(root / "content/site.json")
    catalog = read_json(root / "content/catalog.json")
    redirects = read_json(root / "content/redirects.json")
    for label, value in (("site", site), ("catalog", catalog), ("redirects", redirects)):
        if not isinstance(value, dict) or value.get("schema_version") != 1:
            raise ValueError(f"{label}.schema_version: expected 1")
    errors = []
    routes, sources = {}, {}

    def claim(url, owner):
        try:
            path = route_path(url)
            if not public_file(path):
                raise ValueError("not a public file")
            if path in routes:
                raise ValueError(f"duplicate output URL {url}; conflicts with {routes[path]}")
            routes[path] = owner
        except (ValueError, TypeError) as exc:
            errors.append(f"{owner}.url: {exc}")

    def source(value, owner, unique=False):
        try:
            path = source_path(root, value)
            if unique and path in sources:
                raise ValueError(f"duplicate source {value}; conflicts with {sources[path]}")
            if unique:
                sources[path] = owner
            return path
        except (ValueError, TypeError) as exc:
            errors.append(f"{owner}.source: {exc}")
            return None

    def definitions(field):
        values = site.get(field)
        if not isinstance(values, list) or not values:
            errors.append(f"site.{field}: expected a nonempty list")
            return set()
        ids = set()
        for value in values:
            if not isinstance(value, dict) or not value.get("id") or not value.get("label"):
                errors.append(f"site.{field}: expected objects with id and label")
            elif value["id"] in ids:
                errors.append(f"site.{field}: duplicate id {value['id']}")
            else:
                ids.add(value["id"])
        return ids

    topics, types = definitions("topics"), definitions("types")
    if urlsplit(site.get("url", "")).scheme not in {"http", "https"}:
        errors.append("site.url: expected an absolute HTTP(S) URL")
    navigation = site.get("navigation")
    if not isinstance(navigation, list) or not navigation:
        errors.append("site.navigation: expected a nonempty list")
    else:
        for item in navigation:
            if not isinstance(item, dict) or not item.get("label") or not item.get("url"):
                errors.append("site.navigation: expected label/url")
            else:
                try:
                    route_path(item["url"])
                except ValueError as exc:
                    errors.append(f"site.navigation: {exc}")

    for path in ("/", "/blog/", "/publications/", "/404.html",
                 "/build-info.json", "/sitemap.xml", "/robots.txt", ".nojekyll"):
        claim(path, "generated:" + path)
    entries = copy.deepcopy(catalog.get("entries"))
    if not isinstance(entries, list):
        raise ValueError("catalog.entries: expected a list")
    by_id = {}
    for index, entry in enumerate(entries):
        label = f"catalog.entries[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{label}: expected an object")
            continue
        identifier = entry.get("id")
        label = f"catalog[{identifier or index}]"
        if not isinstance(identifier, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", identifier):
            errors.append(f"{label}.id: expected a stable lowercase slug")
        elif identifier in by_id:
            errors.append(f"{label}.id: duplicate ID")
        else:
            by_id[identifier] = entry
        for field in ("title", "summary", "url"):
            if not isinstance(entry.get(field), str) or not entry[field].strip():
                errors.append(f"{label}.{field}: required nonempty string")
        for field, allowed in (("topic", topics), ("type", types),
                               ("kind", {"post", "series", "chapter", "external"}),
                               ("origin", {"local", "external"}),
                               ("status", {"published", "draft", "archived"}),
                               ("review_status", {"unreviewed", "needs-review", "reviewed"})):
            if entry.get(field) not in allowed:
                errors.append(f"{label}.{field}: invalid value {entry.get(field)!r}")
        for field in ("tags", "related"):
            values = entry.get(field, [])
            if (not isinstance(values, list) or not all(isinstance(v, str) for v in values)
                    or len(values) != len(set(values))):
                errors.append(f"{label}.{field}: expected unique strings")
        if "featured" in entry and not isinstance(entry["featured"], bool):
            errors.append(f"{label}.featured: expected boolean")
        path = None
        if entry.get("origin") == "local":
            path = source(entry.get("source"), label, unique=True)
            claim(entry.get("url", ""), label)
            if entry.get("kind") == "external":
                errors.append(f"{label}.kind: external kind requires external origin")
            if path and path.suffix.lower() not in {".html", ".md"}:
                errors.append(f"{label}.source: expected HTML or Markdown")
            if path and entry.get("status") == "published":
                if "TEMPLATE:EMPTY" in path.read_text(encoding="utf-8") or entry.get("summary") == "待补充摘要":
                    errors.append(f"{label}.source/summary: remove empty template placeholders before publication")
        elif entry.get("origin") == "external":
            if entry.get("source") is not None:
                errors.append(f"{label}.source: external entries must not have a source")
            if entry.get("kind") != "external":
                errors.append(f"{label}.kind: external origin requires external kind")
            if urlsplit(entry.get("url", "")).scheme not in {"http", "https"}:
                errors.append(f"{label}.url: external entries require an absolute HTTP(S) URL")
        try:
            entry["updated"] = content_date(entry.get("updated"), label + ".updated")
            rule = entry.get("updated_source")
            if rule:
                if not isinstance(rule, dict) or rule.get("kind") != "html-element":
                    raise ValueError(f"{label}.updated_source: unsupported date extraction rule")
                if not rule.get("id") or not rule.get("attribute"):
                    raise ValueError(f"{label}.updated_source: id and attribute are required")
                if path:
                    parser = UpdatedElement(rule["id"], rule["attribute"])
                    parser.feed(path.read_text(encoding="utf-8"))
                    if len(parser.values) != 1 or not parser.values[0]:
                        raise ValueError(f"{label}.updated_source: expected one valid {rule['id']} element")
                    entry["updated"] = content_date(parser.values[0], label + ".updated_source")
        except ValueError as exc:
            errors.append(str(exc))

    series_orders = {}
    external_urls = set()
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        label = f"catalog[{entry.get('id')}]"
        if entry.get("origin") == "external":
            if entry.get("url") in external_urls:
                errors.append(f"{label}.url: duplicate external URL")
            external_urls.add(entry.get("url"))
        for related in entry.get("related", []) if isinstance(entry.get("related", []), list) else []:
            if related not in by_id or related == entry.get("id"):
                errors.append(f"{label}.related: invalid ID {related}")
        if entry.get("kind") == "chapter":
            parent = by_id.get(entry.get("series"))
            order = entry.get("order")
            if not parent or parent.get("kind") != "series" or parent.get("origin") != "local":
                errors.append(f"{label}.series: expected a local series ID")
            elif parent.get("status") == "draft" and entry.get("status") != "draft":
                errors.append(f"{label}.series: public chapter belongs to a draft series")
            if not isinstance(order, int) or isinstance(order, bool) or order < 1:
                errors.append(f"{label}.order: expected a positive integer")
            else:
                orders = series_orders.setdefault(entry.get("series"), set())
                if order in orders:
                    errors.append(f"{label}.order: duplicate order {order}")
                orders.add(order)
        elif entry.get("series") is not None or entry.get("order") is not None:
            errors.append(f"{label}.series/order: only chapters may have a series/order")

    for page in site.get("pages", []):
        claim(page["url"], "page:" + page["id"])
        source(page["source"], "page:" + page["id"], unique=True)
    publications = []
    config = site.get("publications", {})
    if config.get("source_glob") != "content/publications/*.md":
        errors.append("site.publications.source_glob: expected content/publications/*.md")
    prefix = config.get("url_prefix", "/publication/")
    for path in sorted((root / "content/publications").glob("*.md")):
        try:
            source(path.relative_to(root).as_posix(), "publication:" + path.stem, unique=True)
            meta, body = load_md(path)
            for field in ("title", "venue", "excerpt"):
                if not isinstance(meta.get(field), str) or not meta[field].strip():
                    raise ValueError(f"required field {field}")
            if "date" not in meta:
                raise ValueError("required field date (use null when unknown)")
            meta["date"] = content_date(
                str(meta["date"]) if meta["date"] is not None else None,
                "publication:" + path.stem + ".date")
            if meta["date"] is None and (
                    not isinstance(meta.get("date_label"), str) or not meta["date_label"].strip()):
                raise ValueError("unknown date requires a nonempty date_label")
            url = prefix.rstrip("/") + "/" + path.stem + "/"
            if meta.get("permalink") and route_path(meta["permalink"]) != route_path(url):
                raise ValueError("permalink conflicts with registered publication route")
            claim(url, "publication:" + path.stem)
            publications.append({"meta": meta, "body": body, "slug": path.stem, "url": url})
        except ValueError as exc:
            errors.append(f"publication:{path.stem}: {exc}")
    publications.sort(key=lambda p: (p["meta"]["date"] is not None,
                                     p["meta"]["date"] or "", p["slug"]), reverse=True)
    for slug in config.get("featured", []):
        if slug not in {paper["slug"] for paper in publications}:
            errors.append(f"site.publications.featured: missing publication {slug}")
    for asset in site.get("assets", []):
        claim(asset["url"], "asset:" + asset["source"])
        source(asset["source"], "asset:" + asset["url"])
    for section in ("redirects", "copies"):
        values = redirects.get(section, [])
        if not isinstance(values, list):
            errors.append(f"redirects.{section}: expected a list")
            continue
        for item in values:
            if not isinstance(item, dict) or not item.get("from") or not item.get("to"):
                errors.append(f"redirects.{section}: from/to are required")
                continue
            claim(item["from"], section + ":" + item["from"])
            try:
                route_path(urlsplit(item["to"]).path)
                if urlsplit(item["to"]).scheme or urlsplit(item["to"]).netloc:
                    raise ValueError("target must be local")
            except ValueError as exc:
                errors.append(f"redirects:{item['from']}.to: {exc}")
    for section in ("redirects", "copies"):
        for item in redirects.get(section, []):
            if not isinstance(item, dict) or not item.get("to"):
                continue
            try:
                target = route_path(urlsplit(item["to"]).path)
                if target not in routes:
                    errors.append(f"redirects:{item.get('from')}.to: missing registered target {item['to']}")
            except ValueError:
                pass
    if errors:
        raise ValueError("Invalid content contract:\n" + "\n".join(errors))
    return site, entries, publications, redirects
