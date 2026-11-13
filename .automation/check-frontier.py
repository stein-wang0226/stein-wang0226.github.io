#!/usr/bin/env python3
"""Fail closed on dirty files, lost insertion markers, or incoherent source dates."""
import argparse
from collections import Counter
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
import subprocess
import sys

SOURCE = "content/posts/llm-frontier-2026/index.html"
TOPICS = (
    "models", "frontier", "arch", "optimizer", "agent", "rl", "opd",
    "training", "bench", "protein", "changelog",
)
SECTIONS = (*TOPICS, "overview", "rumor", "sources")
VOID = {
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
    "meta", "param", "source", "track", "wbr",
}


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args])


def worktree(repo, phase):
    repo = repo.resolve()
    source = repo / SOURCE
    if source.is_symlink() or not source.is_file():
        raise ValueError(f"Missing regular authoritative source: {SOURCE}")
    if not source.resolve().is_relative_to(repo):
        raise ValueError(f"Authoritative source escapes repository: {SOURCE}")
    git(repo, "ls-files", "--error-unmatch", "--", SOURCE)
    records = git(repo, "status", "--porcelain=v1", "-z",
                  "--untracked-files=all", "--ignore-submodules=none").split(b"\0")
    blocked = []
    index = 0
    while index < len(records):
        record = records[index]
        index += 1
        if not record:
            continue
        status = record[:2].decode("ascii")
        path = record[3:].decode("utf-8", errors="surrogateescape")
        if phase != "updated" or status != " M" or path != SOURCE:
            blocked.append(f"{status} {path!r}")
        if "R" in status or "C" in status:
            # Porcelain -z gives the destination first, then the original path.
            if index < len(records):
                blocked.append(f"rename/copy from {records[index]!r}")
                index += 1
    if blocked:
        raise ValueError("Dirty worktree/index blocks automation:\n" + "\n".join(blocked))


def valid_date(value):
    parsed = date.fromisoformat(value)
    if parsed.isoformat() != value:
        raise ValueError(f"Expected YYYY-MM-DD, found {value!r}")
    return value


class Frontier(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.ids = Counter()
        self.markers = Counter()
        self.dates = []
        self.hero = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids[attrs["id"]] += 1
        section = attrs.get("id") if tag == "section" else None
        inherited = self.stack[-1]["section"] if self.stack else None
        entry_date = "entry-date" in attrs.get("class", "").split()
        frame = {
            "tag": tag, "section": section or inherited,
            "date": entry_date or attrs.get("id") == "last-updated",
            "hero": attrs.get("id") == "last-updated",
            "datetime": attrs.get("datetime"), "text": "",
        }
        if tag not in VOID:
            self.stack.append(frame)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_data(self, data):
        for frame in self.stack:
            if frame["date"]:
                frame["text"] += data

    def handle_comment(self, data):
        if data.strip().startswith("AUTO:INSERT:"):
            self.markers[data.strip()] += 1

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index]["tag"] == tag:
                frames = self.stack[index:]
                del self.stack[index:]
                for frame in frames:
                    if not frame["date"]:
                        continue
                    text = frame["text"].strip()
                    value = valid_date(frame["datetime"] or text)
                    if text != value:
                        raise ValueError(f"Visible date {text!r} differs from datetime {value!r}")
                    if frame["hero"]:
                        if frame["tag"] != "time" or not frame["datetime"]:
                            raise ValueError("last-updated must be a time with datetime")
                        self.hero.append(value)
                    else:
                        self.dates.append((frame["section"], value))
                break


def document(source, baseline=None):
    doc = Frontier()
    doc.feed(source.read_text(encoding="utf-8"))
    doc.close()
    required = Counter(f"AUTO:INSERT:{topic}" for topic in TOPICS)
    if any(doc.markers[marker] != count for marker, count in required.items()):
        raise ValueError("Missing or repeated required AUTO:INSERT:* marker")
    duplicates = [name for name, count in doc.ids.items() if count != 1]
    if duplicates:
        raise ValueError(f"Duplicate HTML ids: {duplicates}")
    if any(doc.ids[section] != 1 for section in SECTIONS):
        raise ValueError("Missing frontier section/anchor")
    if len(doc.hero) != 1:
        raise ValueError("Expected exactly one valid last-updated date")
    changelog = [value for section, value in doc.dates if section == "changelog"]
    if not changelog or changelog != sorted(changelog, reverse=True):
        raise ValueError("Changelog dates must be present and newest first")
    updated = doc.hero[0]
    if updated != changelog[0]:
        raise ValueError("last-updated and latest changelog date disagree")
    if any(value > updated for _, value in doc.dates):
        raise ValueError("Entry date is later than last-updated")
    if baseline:
        old = document(baseline)
        if doc.markers != old.markers:
            raise ValueError("AUTO:INSERT:* markers changed")
        if updated < old.hero[0]:
            raise ValueError("Content update date moved backwards")
    return doc


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    tree = commands.add_parser("worktree")
    tree.add_argument("--repo", type=Path, required=True)
    tree.add_argument("--phase", choices=("clean", "updated"), required=True)
    page = commands.add_parser("document")
    page.add_argument("--source", type=Path, required=True)
    page.add_argument("--baseline", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "worktree":
            worktree(args.repo, args.phase)
        else:
            print(document(args.source, args.baseline).hero[0])
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print(f"BLOCKED: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
