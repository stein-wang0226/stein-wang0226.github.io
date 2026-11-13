#!/usr/bin/env python3
"""Isolated regression: real fixture index/status, mocked updater/build/publication.

No commits, pushes, network access, real Codex, or scheduled jobs are executed.
The unborn fixture index represents the clean baseline, without creating a commit.
Build/date tests use a synthetic adapter, not the still-pending T2 implementation.
"""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

AUTOMATION = Path(__file__).resolve().parent
SOURCE = "content/posts/llm-frontier-2026/index.html"
GIT = shutil.which("git")
TOPICS = (
    "models", "frontier", "arch", "optimizer", "agent", "rl", "opd",
    "training", "bench", "protein", "changelog",
)


def page():
    sections = []
    for topic in (*TOPICS, "overview", "rumor", "sources"):
        marker = f"<!-- AUTO:INSERT:{topic} -->" if topic in TOPICS else ""
        entry = (
            '<div class="update-entry"><time class="entry-date" '
            'datetime="2026-11-10">2026-11-10</time><p>Fixture baseline.</p></div>'
            if topic == "changelog" else ""
        )
        sections.append(f'<section id="{topic}">{marker}{entry}</section>')
    return (
        '<!doctype html><html><head><title>Synthetic fixture</title></head><body>'
        '<time id="last-updated" datetime="2026-11-10">2026-11-10</time>'
        + "".join(sections) + "</body></html>"
    )


MOCK_GIT = r'''#!/usr/bin/env python3
import json
import os
from pathlib import Path
import subprocess
import sys

args = sys.argv[1:]
repo = Path(args[1]) if args[:1] == ["-C"] else Path.cwd()
command = args[2:] if args[:1] == ["-C"] else args
tools = Path(os.environ["FIXTURE_TOOLS"])
baseline_file = tools / "baseline.json"
baseline = json.loads(baseline_file.read_text())
real = os.environ["FIXTURE_REAL_GIT"]
source = "content/posts/llm-frontier-2026/index.html"

def actual(*arguments):
    return subprocess.check_output([real, "-C", str(repo), *arguments])

def entries():
    result = {}
    for entry in actual("ls-files", "--stage", "-z").split(b"\0"):
        if entry:
            meta, path = entry.split(b"\t", 1)
            result[os.fsdecode(path)] = meta.decode()
    return result

if command[:1] == ["status"]:
    indexed = entries()
    output = []
    # Real porcelain detects staged, unstaged, deleted, renamed and untracked paths.
    for entry in actual("status", "--porcelain=v1", "-z", "--untracked-files=all").split(b"\0"):
        if not entry:
            continue
        status, path = entry[:2].decode(), os.fsdecode(entry[3:])
        if status[0] == "A" and path in baseline:
            status = (" " if indexed.get(path) == baseline[path] else "M") + status[1]
        if status != "  ":
            output.append(status.encode() + b" " + os.fsencode(path) + b"\0")
    sys.stdout.buffer.write(b"".join(output))
elif command[:1] == ["symbolic-ref"]:
    print("main")
elif command[:1] in (["pull"], ["add"], ["commit"], ["push"]):
    with (tools / "events.jsonl").open("a") as log:
        log.write(json.dumps(command) + "\n")
    if command[0] == "commit":
        # Emulate a clean post-commit index WITHOUT executing git commit.
        actual("update-index", "--add", "--", source)
        baseline[source] = entries()[source]
        baseline_file.write_text(json.dumps(baseline))
elif command == ["rev-parse", "HEAD"]:
    print("fixture-no-real-commit")
else:
    sys.stdout.buffer.write(actual(*command))
'''

MOCK_UPDATER = r'''#!/usr/bin/env python3
import os
from pathlib import Path
import subprocess
import sys

args = sys.argv[1:]
repo = Path(args[args.index("-C") + 1])
result = Path(args[args.index("--output-last-message") + 1])
source = repo / "content/posts/llm-frontier-2026/index.html"
tools = Path(os.environ["FIXTURE_TOOLS"])
(tools / "updater-called").touch()
assert "--sandbox" in args and args[args.index("--sandbox") + 1] == "workspace-write"
assert "--dangerously-bypass-approvals-and-sandbox" not in args
mode = os.environ.get("FIXTURE_MODE", "increment")
if mode == "error":
    sys.exit(1)
if mode == "blocked":
    result.write_text("FRONTIER_RESULT: BLOCKED\nSynthetic research blocker.\n")
    sys.exit(0)
if mode == "no_change":
    result.write_text("FRONTIER_RESULT: NO_CHANGE\nNo substantive fixture change.\n")
    sys.exit(0)
text = source.read_text()
text = text.replace(
    'id="last-updated" datetime="2026-11-10">2026-11-10',
    'id="last-updated" datetime="2026-11-14">2026-11-14',
)
entry = (
    '<div class="update-entry"><time class="entry-date" '
    'datetime="2026-11-14">2026-11-14</time><p>Synthetic fixture addition; '
    '<a href="https://example.org/fixture">fixture source</a>.</p></div>'
)
for topic in ("models", "changelog"):
    marker = f"<!-- AUTO:INSERT:{topic} -->"
    text = text.replace(marker, marker + entry)
if mode == "bad_date":
    text = text.replace('id="last-updated" datetime="2026-11-14">2026-11-14',
                        'id="last-updated" datetime="2026-11-13">2026-11-13')
if mode == "visible_date":
    text = text.replace('id="last-updated" datetime="2026-11-14">2026-11-14',
                        'id="last-updated" datetime="2026-11-14">2026-11-13')
if mode == "missing_marker":
    text = text.replace("<!-- AUTO:INSERT:models -->", "")
source.write_text(text)
if mode in ("dirty_after", "staged_after"):
    unrelated = repo / "unrelated.txt"
    unrelated.write_text("Concurrent unrelated edit.\n")
    if mode == "staged_after":
        subprocess.check_call([os.environ["FIXTURE_REAL_GIT"], "-C", str(repo),
                               "update-index", "--add", "--", "unrelated.txt"])
result.write_text("FRONTIER_RESULT: UPDATED\nTwo synthetic entries, not real research.\n")
'''

MOCK_VALIDATOR = r'''#!/usr/bin/env python3
import os
from html.parser import HTMLParser
from pathlib import Path
import sys

repo, source = Path(sys.argv[1]), sys.argv[2]
tools = Path(os.environ["FIXTURE_TOOLS"])
(tools / "validator-called").touch()
mode = os.environ.get("FIXTURE_VALIDATOR_MODE", "success")
if mode == "failure":
    sys.exit(1)
if mode == "dirty":
    (repo / "unrelated.txt").write_text("Build wrote an unrelated file.\n")
if mode == "source_write":
    with (repo / source).open("a") as page:
        page.write("<!-- Build must not write source. -->")
class Dates(HTMLParser):
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id") == "last-updated":
            self.updated = attrs["datetime"]
text = (repo / source).read_text()
dates = Dates()
dates.feed(text)
output = tools / "public"
output.mkdir()
(output / "llm-frontier-2026.html").write_text(text)
(output / "blog").mkdir()
(output / "blog/index.html").write_text(
    f'<a href="/llm-frontier-2026.html">Fixture</a>'
    f'<time datetime="{dates.updated}">{dates.updated}</time>'
)
'''


class AutomationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="frontier-regression-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        self.tools = self.root / "tools"
        self.repo.mkdir()
        self.tools.mkdir()
        self.real_git("init", "-q")
        automation = self.repo / ".automation"
        automation.mkdir()
        for name in ("run-frontier-update.sh", "check-frontier.py", "update-frontier.md"):
            shutil.copy2(AUTOMATION / name, automation / name)
        for name in ("state", "backup", "logs"):
            directory = automation / name
            directory.mkdir()
            (directory / ".gitignore").write_text("*\n!.gitignore\n")
        self.source = self.repo / SOURCE
        self.source.parent.mkdir(parents=True)
        self.original = page()
        self.source.write_text(self.original)
        (self.repo / "unrelated.txt").write_text("Baseline unrelated fixture.\n")
        files = [str(path.relative_to(self.repo)) for path in self.repo.rglob("*")
                 if path.is_file() and ".git" not in path.parts]
        self.real_git("update-index", "--add", "--", *files)
        baseline = {}
        for entry in self.real_git("ls-files", "--stage", "-z").split(b"\0"):
            if entry:
                meta, path = entry.split(b"\t", 1)
                baseline[os.fsdecode(path)] = meta.decode()
        (self.tools / "baseline.json").write_text(json.dumps(baseline))
        for name, text in (("git", MOCK_GIT), ("updater", MOCK_UPDATER),
                           ("validator", MOCK_VALIDATOR)):
            executable = self.tools / name
            executable.write_text(text)
            executable.chmod(0o755)
        self.env = {
            **os.environ,
            "PATH": f"{self.tools}{os.pathsep}{os.environ['PATH']}",
            "FIXTURE_REAL_GIT": GIT,
            "FIXTURE_TOOLS": str(self.tools),
            "FRONTIER_UPDATER": str(self.tools / "updater"),
            "FRONTIER_VALIDATOR": str(self.tools / "validator"),
            "PYTHONDONTWRITEBYTECODE": "1",
        }
        self.state = automation / "state"

    def real_git(self, *args):
        return subprocess.check_output([GIT, "-C", str(self.repo), *args])

    def run_update(self, publish=False, **env):
        args = ["bash", str(self.repo / ".automation/run-frontier-update.sh")]
        if publish:
            args.append("--publish")
        return subprocess.run(args, cwd=self.repo, env={**self.env, **env},
                              capture_output=True, text=True, timeout=30)

    def events(self):
        path = self.tools / "events.jsonl"
        return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []

    def assert_blocked(self, result, expected):
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(expected, (self.state / "last-result.md").read_text())
        self.assertFalse((self.state / "last-successful-scheduled-run").exists())
        self.assertFalse(any(event[0] in {"add", "commit", "push"} for event in self.events()))

    def test_increment_preserves_markers_backup_and_output_date(self):
        result = self.run_update()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.events(), [])
        self.assertFalse((self.state / "last-successful-scheduled-run").exists())
        backups = list((self.repo / ".automation/backup").glob("llm-frontier-2026.*.html"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(), self.original)
        updated = self.source.read_text()
        for topic in TOPICS:
            self.assertEqual(updated.count(f"<!-- AUTO:INSERT:{topic} -->"), 1)
        self.assertEqual(updated.count('class="update-entry"'), 3)
        output = self.tools / "public"
        self.assertEqual((output / "llm-frontier-2026.html").read_text(), updated)
        self.assertIn('datetime="2026-11-14">2026-11-14',
                      (output / "blog/index.html").read_text())
        self.assertEqual(len(list(output.rglob("*"))), 3)
        self.assertIn("local preparation only", (self.state / "last-result.md").read_text())

    def test_unstaged_unrelated_edit_blocks_before_updater(self):
        (self.repo / "unrelated.txt").write_text("Existing manual edit.\n")
        result = self.run_update(publish=True)
        self.assert_blocked(result, "unrelated.txt")
        self.assertFalse((self.tools / "updater-called").exists())
        self.assertEqual(self.events(), [])
        self.assertEqual(self.source.read_text(), self.original)

    def test_staged_unrelated_edit_blocks_before_updater(self):
        (self.repo / "unrelated.txt").write_text("Existing staged edit.\n")
        self.real_git("update-index", "--add", "--", "unrelated.txt")
        self.assert_blocked(self.run_update(publish=True), "unrelated.txt")
        self.assertFalse((self.tools / "updater-called").exists())
        self.assertEqual(self.events(), [])

    def test_untracked_unrelated_file_blocks_before_updater(self):
        (self.repo / "untracked name.txt").write_text("Not authorized.\n")
        self.assert_blocked(self.run_update(publish=True), "untracked name.txt")
        self.assertEqual(self.events(), [])

    def test_dirty_source_is_not_overwritten(self):
        self.source.write_text(self.original + "<!-- Manual edit. -->")
        self.assert_blocked(self.run_update(), SOURCE)
        self.assertFalse((self.tools / "updater-called").exists())
        self.assertIn("Manual edit", self.source.read_text())

    def test_unrelated_edit_introduced_by_updater_blocks_publication(self):
        result = self.run_update(publish=True, FIXTURE_MODE="dirty_after")
        self.assert_blocked(result, "unrelated.txt")
        self.assertFalse((self.tools / "validator-called").exists())
        self.assertIn("Concurrent unrelated", (self.repo / "unrelated.txt").read_text())

    def test_staged_edit_introduced_by_updater_blocks_publication(self):
        self.assert_blocked(self.run_update(publish=True, FIXTURE_MODE="staged_after"),
                            "unrelated.txt")

    def test_mismatched_dates_block_before_build(self):
        self.assert_blocked(self.run_update(FIXTURE_MODE="bad_date"), "disagree")
        self.assertFalse((self.tools / "validator-called").exists())

    def test_visible_and_machine_dates_must_agree(self):
        self.assert_blocked(self.run_update(FIXTURE_MODE="visible_date"), "differs")

    def test_missing_marker_blocks_before_build(self):
        self.assert_blocked(self.run_update(FIXTURE_MODE="missing_marker"), "marker")

    def test_failed_build_cannot_publish_or_stamp_success(self):
        self.assert_blocked(self.run_update(publish=True, FIXTURE_VALIDATOR_MODE="failure"),
                            "validator failed")

    def test_build_cannot_write_unrelated_files(self):
        self.assert_blocked(self.run_update(publish=True, FIXTURE_VALIDATOR_MODE="dirty"),
                            "unrelated.txt")

    def test_build_cannot_write_source(self):
        self.assert_blocked(self.run_update(publish=True, FIXTURE_VALIDATOR_MODE="source_write"),
                            "modified the authoritative source")

    def test_updater_blocked_report_cannot_stamp_success(self):
        self.assert_blocked(self.run_update(FIXTURE_MODE="blocked"), "did not report success")

    def test_updater_failure_cannot_stamp_success(self):
        self.assert_blocked(self.run_update(FIXTURE_MODE="error"), "Updater failed")

    def test_missing_build_contract_blocks_before_updater(self):
        result = self.run_update(FRONTIER_VALIDATOR=str(self.tools / "missing-validator"))
        self.assert_blocked(result, "Build/check interface is required")
        self.assertFalse((self.tools / "updater-called").exists())

    def test_no_change_skips_build_and_publication_and_keeps_cadence(self):
        result = self.run_update(FIXTURE_MODE="no_change")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.state / "last-successful-scheduled-run").exists())
        self.assertFalse((self.tools / "validator-called").exists())
        self.assertEqual(self.events(), [])
        (self.tools / "updater-called").unlink()
        repeated = self.run_update()
        self.assertEqual(repeated.returncode, 0, repeated.stderr)
        self.assertIn("less than 72 hours", repeated.stdout)
        self.assertFalse((self.tools / "updater-called").exists())

    def test_mock_publication_arguments_are_source_only(self):
        result = self.run_update(publish=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.events(), [
            ["pull", "--ff-only", "origin", "main"],
            ["add", "--", SOURCE],
            ["commit", "--only", "-m", "docs(frontier): update 2026-11-14", "--", SOURCE],
            ["push", "origin", "HEAD:main"],
        ])
        self.assertTrue((self.state / "last-successful-scheduled-run").exists())
        # The fixture still has an unborn HEAD: no real commit was created.
        head = subprocess.run([GIT, "-C", str(self.repo), "rev-parse", "--verify", "HEAD"],
                              capture_output=True)
        self.assertNotEqual(head.returncode, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
