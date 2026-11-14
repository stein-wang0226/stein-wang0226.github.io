#!/usr/bin/env python3
"""Integration checks in isolated copies; never commit, push or edit real sources."""
import sys
sys.dont_write_bytecode = True
import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from datetime import date, timedelta

from catalog import load_content
from citations import derive, source_identity
from check import validate
from new_post import create
from pipeline import build
from render import ROOT, input_digest


def tree(path):
    return {p.relative_to(path).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in path.rglob("*") if p.is_file() and ".git" not in p.relative_to(path).parts}


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="blog-integration-")
        self.base = Path(self.tmp.name)
        self.root = self.base / "source"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns(
            ".DS_Store", "__pycache__", "*.pyc", "run.lock"))
        self.output = self.base / "artifact"

    def tearDown(self):
        self.tmp.cleanup()

    def catalog(self, mutate):
        path = self.root / "content/catalog.json"
        data = json.loads(path.read_text())
        mutate(data["entries"])
        path.write_text(json.dumps(data, ensure_ascii=False))

    def test_contract_failures_name_record_and_field(self):
        original = (self.root / "content/catalog.json").read_bytes()
        cases = [
            (lambda e: e.append(copy.deepcopy(e[0])), "duplicate ID"),
            (lambda e: e[1].update(url=e[0]["url"]), "duplicate output URL"),
            (lambda e: e[0].update(source="content/missing.html"), "source"),
            (lambda e: e[0].update(topic="unknown"), "topic"),
            (lambda e: e[0].update(type="unknown"), "type"),
            (lambda e: e[-1].update(series="no-series"), "series"),
            (lambda e: e[-1].update(order=e[-2]["order"]), "order"),
            (lambda e: e[0].update(updated="2026-02-30"), "updated"),
        ]
        for mutation, message in cases:
            with self.subTest(message=message):
                (self.root / "content/catalog.json").write_bytes(original)
                self.catalog(mutation)
                with self.assertRaisesRegex(ValueError, message):
                    load_content(self.root)

    def test_rebuild_is_deterministic_read_only_and_manifest_only(self):
        before = tree(self.root)
        status = subprocess.check_output(["git", "-C", str(self.root), "status", "--porcelain"])
        build(self.output, self.root)
        first = tree(self.output)
        build(self.output, self.root)
        self.assertEqual(first, tree(self.output))
        self.assertEqual(before, tree(self.root))
        self.assertEqual(status, subprocess.check_output(
            ["git", "-C", str(self.root), "status", "--porcelain"]))
        info = json.loads((self.output / "build-info.json").read_text())
        self.assertEqual(set(first), set(info["files"]) | {"build-info.json"})
        self.assertEqual(bool(status.strip()), info["dirty"])
        self.assertEqual(info["input_digest"], input_digest(self.root))
        self.assertFalse(any(Path(p).parts[0] in {
            "content", "scripts", "templates", "docs", ".automation", ".git"
        } for p in first))
        (self.output / "stale.html").write_text("stale")
        errors, _ = validate(self.output, self.root)
        self.assertTrue(any("stale" in e for e in errors))
        build(self.output, self.root)
        self.assertFalse((self.output / "stale.html").exists())

    def test_failed_build_preserves_previous_success_and_source(self):
        build(self.output, self.root)
        before = tree(self.output)
        self.catalog(lambda e: e[0].update(topic="invalid"))
        sources = tree(self.root)
        with self.assertRaises(ValueError):
            build(self.output, self.root)
        self.assertEqual(before, tree(self.output))
        self.assertEqual(sources, tree(self.root))

    def test_reading_routes_reject_missing_anchors_and_prerequisite_cycles(self):
        path = self.root / "content/site.json"
        original = path.read_bytes()
        site = json.loads(original)
        site["learning_paths"][0]["stages"][0]["anchor"] = "fixture-missing-anchor"
        path.write_text(json.dumps(site, ensure_ascii=False))
        with self.assertRaisesRegex(ValueError, "learning_paths.*missing #fixture"):
            load_content(self.root)
        path.write_bytes(original)
        def cycle(entries):
            a, b = entries[:2]
            a["prerequisites"] = [{"entry": b["id"], "reason": "Fixture"}]
            b["prerequisites"] = [{"entry": a["id"], "reason": "Fixture"}]
        self.catalog(cycle)
        with self.assertRaisesRegex(ValueError, "required reading cycle"):
            load_content(self.root)

    def test_citations_keep_multiple_papers_versions_and_historical_usage(self):
        source = self.root / "content/posts/agentic-rl-guide/index.html"
        fixture = (
            '<section id="fixture-current"><a href="#ref-fixture">[fixture]</a></section>'
            '<details data-reading-history><summary>Fixture</summary>'
            '<section id="fixture-history"><a href="#ref-fixture">[fixture]</a></section></details>'
            '<ol><li id="ref-fixture">'
            '<a href="https://arxiv.org/abs/9901.12345v1">Fixture A</a>'
            '<a href="https://arxiv.org/html/9901.12346v2">Fixture B</a></li></ol>')
        source.write_text(source.read_text().replace("</body>", fixture + "</body>"))
        before = tree(self.root)
        data, errors = derive(self.root)
        self.assertEqual([], errors)
        self.assertEqual(before, tree(self.root))
        for key in ("arxiv:9901.12345@v1", "arxiv:9901.12346@v2"):
            row = next(s for s in data["sources"] if s["source_key"] == key)
            self.assertEqual({"current", "historical"}, {u["role"] for u in row["used_in"]})
            self.assertTrue(row["local_references"][0]["url"].endswith("#ref-fixture"))
        self.assertEqual(source_identity("https://arxiv.org/abs/9901.12345v1")[0],
                         source_identity("https://arxiv.org/pdf/9901.12345v1")[0])
        self.assertNotEqual(source_identity("https://arxiv.org/abs/9901.12345v1")[0],
                            source_identity("https://arxiv.org/abs/9901.12345v2")[0])

    def test_dangling_citation_fails_without_replacing_previous_artifact(self):
        build(self.output, self.root)
        artifact = tree(self.output)
        source = self.root / "content/posts/agentic-rl-guide/index.html"
        source.write_text(source.read_text().replace("</body>",
                          '<a href="#ref-fixture-missing">[missing]</a></body>'))
        before = tree(self.root)
        with self.assertRaisesRegex(ValueError, "unresolved bibliography"):
            build(self.output, self.root)
        self.assertEqual(artifact, tree(self.output))
        self.assertEqual(before, tree(self.root))

    def test_source_registry_usage_and_version_conflicts_are_reported(self):
        path = self.root / "assets/research/posttraining-20261114/sources.json"
        original = path.read_bytes()
        data = json.loads(original)
        data["sources"][0]["used_in"] = ["/fixture-stale-usage.html"]
        path.write_text(json.dumps(data, ensure_ascii=False))
        _, errors = derive(self.root)
        self.assertTrue(any("stale used_in" in error for error in errors))
        data = json.loads(original)
        data["sources"][0]["version"] = "1707.06347v999"
        path.write_text(json.dumps(data, ensure_ascii=False))
        before = tree(self.root)
        _, errors = derive(self.root)
        self.assertTrue(any("version conflict" in error for error in errors))
        self.assertEqual(before, tree(self.root))

    def test_registered_csv_and_embedded_chart_targets_are_checked(self):
        build(self.output, self.root)
        asset = "assets/research/agent-data-benchmarks/global-kv-bytes.csv"
        self.assertEqual((self.root / asset).read_bytes(), (self.output / asset).read_bytes())
        source = self.root / "content/series/agent-data-benchmarks/s01_task_synthesis.html"
        source.write_text(source.read_text().replace(
            "task-synthesis-flow.svg", "missing-chart.svg"))
        with self.assertRaisesRegex(ValueError, "missing target.*missing-chart.svg"):
            build(self.output, self.root)

    def test_draft_scaffold_collision_and_empty_template(self):
        create("fixture-post", 'A "quoted" title', "agent", root=self.root)
        record = next(e for e in load_content(self.root)[1] if e["id"] == "fixture-post")
        self.assertEqual("draft", record["status"])
        before = tree(self.root)
        with self.assertRaisesRegex(ValueError, "already exists"):
            create("fixture-post", "replace", "agent", root=self.root)
        self.assertEqual(before, tree(self.root))
        build(self.output, self.root)
        self.assertFalse((self.output / "fixture-post.html").exists())
        self.assertNotIn("fixture-post", (self.output / "blog/catalog.json").read_text())
        self.catalog(lambda e: e[-1].update(status="published"))
        with self.assertRaisesRegex(ValueError, "template"):
            build(self.output, self.root)
        self.catalog(lambda e: e[-1].update(status="published", summary="Real summary"))
        (self.root / record["source"]).write_text('---\ntitle: "A quoted title"\n---\n## Example\nConcrete content.')
        build(self.output, self.root)
        self.assertTrue((self.output / "fixture-post.html").exists())
        (self.root / record["source"]).write_text('---\ntitle: "A quoted title"\n---\n## Example\nChanged.')
        errors, _ = validate(self.output, self.root)
        self.assertTrue(any("stale" in e for e in errors))
        self.catalog(lambda e: e.pop())
        build(self.output, self.root)
        self.assertFalse((self.output / "fixture-post.html").exists())

    def test_real_frontier_increment_and_catalog_date(self):
        path = self.root / "content/posts/llm-frontier-2026/index.html"
        before = path.read_text()
        old_date = next(e["updated"] for e in load_content(self.root)[1] if e["id"] == "llm-frontier-2026")
        new_date = (date.fromisoformat(old_date) + timedelta(days=1)).isoformat()
        text = before.replace(f'datetime="{old_date}">{old_date}', f'datetime="{new_date}">{new_date}', 1)
        entry = (f'<div class="entry"><span class="entry-date">{new_date}</span>'
                 '<p>Isolated fixture: linked source retained; no real factual addition.</p></div>')
        text = text.replace("<!-- AUTO:INSERT:changelog -->", "<!-- AUTO:INSERT:changelog -->" + entry)
        path.write_text(text)
        build(self.output, self.root)
        rows = json.loads((self.output / "blog/catalog.json").read_text())["entries"]
        frontier = next(e for e in rows if e["id"] == "llm-frontier-2026")
        self.assertEqual(new_date, frontier["updated"])
        self.assertIn(entry, (self.output / "llm-frontier-2026.html").read_text())
        self.assertEqual(text, path.read_text())

    def test_output_must_be_external_and_owned(self):
        with self.assertRaisesRegex(ValueError, "outside"):
            build(self.root / "dist", self.root)
        self.output.mkdir()
        (self.output / "keep.txt").write_text("unrelated")
        with self.assertRaisesRegex(ValueError, "non-owned"):
            build(self.output, self.root)
        self.assertEqual("unrelated", (self.output / "keep.txt").read_text())

    def test_manuscript_date_unknown_requires_label_and_renders_without_fabrication(self):
        paper = self.root / "content/publications/cua-recovery.md"
        original = paper.read_text()
        build(self.output, self.root)
        page = (self.output / "publication/cua-recovery/index.html").read_text()
        self.assertIn("Submission date not disclosed", page)
        self.assertNotIn(">None", page)
        self.assertNotIn(">null", page)
        paper.write_text(original.replace("date_label: 'Submission date not disclosed'\n", ""))
        with self.assertRaisesRegex(ValueError, "unknown date requires"):
            load_content(self.root)
        paper.write_text(original.replace("date: null", "date: '2026-02-30'"))
        with self.assertRaisesRegex(ValueError, "date"):
            load_content(self.root)


if __name__ == "__main__":
    unittest.main(verbosity=2)
