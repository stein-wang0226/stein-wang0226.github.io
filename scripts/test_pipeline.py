#!/usr/bin/env python3
"""Integration checks in isolated copies; never commit, push or edit real sources."""
import sys
sys.dont_write_bytecode = True
import copy
import hashlib
import json
import re
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from datetime import date, timedelta

from catalog import load_content
from citations import derive, source_identity
from check import Document, validate
from new_post import create
from pipeline import build
from render import ROOT, input_digest
from course import Fragment, render_fragment, public_target
from organization import check as check_organization
from mathematics import reflow_formula
from views import source_headings


def tree(path):
    return {p.relative_to(path).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in path.rglob("*") if p.is_file() and ".git" not in p.relative_to(path).parts}


class PipelineTests(unittest.TestCase):
    def test_catalog_headings_render_markdown_and_exclude_code_and_history(self):
        markdown = self.root / "content/fixture-search.md"
        markdown.write_text('---\ntitle: Fixture\n---\n'
                            '## 同一个残基从字母到向量\n'
                            '### **输入**与 `embedding`\n'
                            '```html\n<h2>代码中的假标题</h2>\n```\n'
                            '<details data-reading-history><summary>原稿</summary>'
                            '<h2>历史标题</h2></details>\n')
        html = self.root / "content/fixture-search.html"
        html.write_text('<h2>同一个残基从字母到向量</h2>'
                        '<h3><strong>输入</strong>与 <code>embedding</code></h3>'
                        '<details data-reading-history><summary>原稿</summary>'
                        '<h2>历史标题</h2></details>')
        expected = ["同一个残基从字母到向量", "输入与 embedding"]
        self.assertEqual(expected, source_headings(markdown))
        self.assertEqual(expected, source_headings(html))

    def test_formula_reflow_preserves_matrix_rows_and_function_arguments(self):
        pattern = r'(<div class="reading-math">\\\[)(.*?)(\\\]</div>)'
        matrix = r"\begin{pmatrix}1&2\\3&4\end{pmatrix}"
        source = '<div class="reading-math">\\[A=' + matrix + r',\quad B=\frac{x+y}{z}\]</div>'
        result = re.sub(pattern, reflow_formula, source, flags=re.S)
        self.assertIn(matrix, result)
        self.assertIn(r"B=\frac{x+y}{z}", result)
        self.assertIn(r"\begin{aligned}", result)
        inside = r'<div class="reading-math">\[f(x,\quad y)=\frac{a,\quad b}{c}\]</div>'
        self.assertEqual(inside, re.sub(pattern, reflow_formula, inside, flags=re.S))
        continuation = (r'<div class="reading-math">\[\begin{aligned}'
                        r'A&=x+y\\&\quad+z\end{aligned}\]</div>')
        self.assertEqual(continuation, re.sub(pattern, reflow_formula, continuation, flags=re.S))
        self.assertEqual(result, re.sub(pattern, reflow_formula, result, flags=re.S))

    def test_course_namespaces_resources_and_accessible_svg_references(self):
        entry = {"id": "fixture", "source": "content/fixture.html", "url": "/course/old.html",
                 "title": "01 · Fixture", "order": 1, "origin": "local", "series": "parent"}
        parent = {"id": "parent", "url": "/course/", "reading_mode": "longform",
                  "origin": "local"}
        path = self.root / entry["source"]
        path.write_text('<!-- READING:FRAGMENT:START -->'
                        '<h2 id="topic">Topic</h2><label for="control">Control</label>'
                        '<input id="control" aria-describedby="topic">'
                        '<svg aria-labelledby="diagram"><title id="diagram">Diagram</title>'
                        '<defs><clipPath id="clip"><rect width="2" height="2"/></clipPath></defs>'
                        '<g clip-path="url(#clip)"><use href="#diagram"/></g></svg>'
                        '<a href="old.html#topic">Old link</a>'
                        '<img src="media/example.png" alt="Example">'
                        '<!-- READING:FRAGMENT:END -->')
        before = path.read_bytes()
        result = render_fragment(self.root, entry, parent["url"],
                                 {"fixture": entry, "parent": parent})
        doc = Document(Path("fixture.html"))
        doc.feed(result)
        self.assertEqual([], doc.errors)
        self.assertIn('aria-labelledby="fixture--diagram"', result)
        self.assertIn('for="fixture--control"', result)
        self.assertIn('clip-path="url(#fixture--clip)"', result)
        self.assertIn('href="#fixture--diagram"', result)
        self.assertIn('href="index.html#fixture--topic"', result)
        self.assertIn('src="media/example.png"', result)
        self.assertIn('<h3 id="fixture--topic">', result)
        self.assertEqual(before, path.read_bytes())
        self.assertEqual(("/course/", "fixture--topic"),
                         public_target(entry, "topic", {"parent": parent}))

    def test_longform_output_has_one_source_and_resolves_old_fragments(self):
        build(self.output, self.root)
        parent = (self.output / "llm-posttraining/index.html").read_text()
        self.assertEqual(1, parent.count('class="course-toc"'))
        self.assertEqual(7, parent.count('class="course-chapter"'))
        self.assertEqual(7, parent.count('class="course-focus"'))
        self.assertIn('href="#posttraining-algorithms--interview-cards"', parent)
        self.assertIn('href="#posttraining-algorithms--baseline-proof"', parent)
        self.assertIn('id="posttraining-algorithms--baseline-proof"', parent)
        old = (self.output / "llm-posttraining/s02_rl_algorithms.html").read_text()
        self.assertIn('location.replace(target.href)', old)
        self.assertIn('target.search=location.search', old)
        self.assertIn('"policy-gradient": "posttraining-algorithms--policy-gradient"', old)
        self.assertNotIn("REINFORCE逐步推导", old)
        catalog = json.loads((self.output / "blog/catalog.json").read_text())
        holon = next(e for e in catalog["entries"] if e["id"] == "my-work-holon")
        self.assertIn("同一个残基从字母到向量", holon["headings"])
        self.assertIn("同一个残基", holon["search"])
        self.assertFalse(any(e["id"] == "posttraining-algorithms" for e in catalog["entries"]))
        course = next(e for e in catalog["entries"] if e["id"] == "llm-posttraining")
        self.assertEqual(7, len(course["sections"]))
        self.assertTrue(any("grpo" in s["search"] for s in course["sections"]))
        self.assertEqual("principles", next(s["type"] for s in course["sections"]
                                           if s["id"] == "posttraining-algorithms"))
        self.assertEqual(6, parent.count('class="teaching-diagram"'))
        self.assertNotIn("K = 3~10", parent)
        architecture = (self.output / "llm-architecture/index.html").read_text()
        self.assertEqual(10, architecture.count('class="course-chapter"'))
        self.assertIn('id="transformer-decoder-flow--numerical-forward"', architecture)
        self.assertIn('id="research-architecture-landscape--families"', architecture)
        old_map = (self.output / "llm-research-map-2026/index.html").read_text()
        self.assertNotIn('class="course-chapter"', old_map)
        self.assertIn('"research-architecture-landscape--families": "../llm-architecture/index.html#research-architecture-landscape--families"', old_map)
        self.assertIn('target.search=location.search', old_map)
        self.assertIn('id="research-architecture-landscape--families"', old_map)
        decoder = (self.output / "transformer-decoder-flow.html").read_text()
        self.assertIn('"code": "transformer-decoder-flow--code"', decoder)
        self.assertIn('location.replace(target.href)', decoder)
        self.assertIn('id="architecture-attention--attention-scaling"', architecture)
        self.assertNotIn('class="equation"', architecture)
        training = (self.output / "llm-training-lifecycle/index.html").read_text()
        self.assertEqual(5, training.count('class="course-chapter"'))
        self.assertIn('id="training-methods-systems--state-sharding"', training)
        self.assertNotIn('class="equation"', training)
        self.assertNotIn('data-reading-history', training)
        legacy = (self.output / "llm-training-lifecycle/s05_training_methods_systems.html").read_text()
        self.assertIn('"adamw-example": "training-methods-systems--adamw-example"', legacy)
        harness = (self.output / "agent-harness-guide.html").read_text()
        self.assertIn('id="codex-memory-phase1"', harness)
        self.assertIn('id="codex-prompt-f"', harness)
        self.assertNotIn('data-reading-history', harness)
        for slug, count, anchor in (
                ("agent-systems", 4, "agent-rag--retrieval"),
                ("agent-data-benchmarks", 5, "scientific-task-family--statistics"),
                ("llm-serving", 4, "serving-parallel--speculation")):
            text = (self.output / slug / "index.html").read_text()
            self.assertEqual(count, text.count('class="course-chapter"'))
            self.assertEqual(1, text.count('class="course-toc"'))
            self.assertIn(f'id="{anchor}"', text)
            self.assertNotIn('class="equation"', text)
            self.assertNotIn('data-reading-history', text)
        scientific = (self.output / "agent-data-benchmarks/s03_scientific_task_family.html").read_text()
        self.assertIn('"statistics": "scientific-task-family--statistics"', scientific)
        self.assertNotIn("从count到均值", scientific)

    def test_frozen_original_is_required_and_tampering_is_rejected(self):
        ledger = json.loads((self.root / "docs/organization-changes-20261115.json").read_text())
        row = next(p for p in ledger["pages"] if p["id"] == "rl-interview-guide")
        original = self.root / row["archive"]
        original_bytes = original.read_bytes()
        original.unlink()
        self.assertTrue(any("missing or unsafe archive" in e for e in check_organization(self.root)))
        original.write_bytes(original_bytes + b"\nchanged\n")
        self.assertTrue(any("altered archive or baseline evidence" in e for e in check_organization(self.root)))
        original.write_bytes(original_bytes)
        self.assertEqual([], check_organization(self.root))
        sources, errors = derive(self.root)
        self.assertEqual([], errors)
        reinforce = next(s for s in sources["sources"] if s["source_key"] == "doi:10.1007/bf00992696")
        self.assertTrue(any(u["role"] == "current" for u in reinforce["used_in"]))
        self.assertTrue(any(u["role"] == "historical" and u["url"] == "/" + row["archive"]
                            for u in reinforce["used_in"]))

    def test_document_title_and_accessible_svg_titles(self):
        doc = Document(Path("report.html"))
        doc.feed('<html><head><title>Report</title></head><body>'
                 '<svg><title>Scientific diagram</title><svg><title>Inset</title></svg></svg>'
                 '<svg/><a href="#evidence">Evidence</a><div id="evidence"></div></body></html>')
        self.assertEqual(doc.title, 1)
        self.assertEqual(doc.svg_depth, 0)
        self.assertIn("evidence", doc.ids)
        self.assertIn("#evidence", doc.links)
        doc.feed("<title>Duplicate document title</title>")
        self.assertEqual(doc.title, 2)

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="blog-integration-")
        self.base = Path(self.tmp.name)
        self.root = self.base / "source"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns(
            ".git", ".DS_Store", "__pycache__", "*.pyc", "run.lock"))
        # A copied worktree .git file points back to the live source repository.
        # Give the fixture its own refs/index; shared immutable objects stay read-only.
        metadata = self.base / "metadata"
        subprocess.run(["git", "clone", "--shared", "--no-checkout", str(ROOT), str(metadata)],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        shutil.move(str(metadata / ".git"), str(self.root / ".git"))
        subprocess.run(["git", "-C", str(self.root), "read-tree", "HEAD"], check=True)
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
        # Markdown must inherit site typography, not just a styled introduction.
        for slug in ("holon", "protagent", "harbor-task-sync", "trainable-dllm"):
            page = (self.output / f"my-work/{slug}/index.html").read_text()
            self.assertIn('<body class="site-body">', page)
            self.assertIn('<main class="site-page reading-markdown">', page)
            self.assertIn('<article class="prose">', page)
        # Existing scientific HTML remains outside the Markdown typography scope.
        original = (self.output / "my-work/holon/full-report.html").read_text()
        self.assertNotIn('class="site-page reading-markdown"', original)
        self.assertIn('id="work-study-guide"', original)
        self.assertIn('class="site-page work-reading-link"', original)
        self.assertIn('href="index.html"', original)
        self.assertNotIn('class="site-page work-learning"', original)
        bibliography = json.loads((self.output / "blog/references.json").read_text())
        cited_entries = {u["entry"] for s in bibliography["sources"] for u in s["used_in"]
                         if "#ref-" in u["citation"]}
        for project in ("holon", "protagent", "harbor", "dllm"):
            self.assertIn(f"my-work-{project}", cited_entries)
        for slug in ("holon", "protagent", "harbor-task-sync", "trainable-dllm"):
            page = (self.output / f"my-work/{slug}/full-report.html").read_text()
            for anchor in ("work-study-guide", "work-report-start"):
                self.assertIn(f'id="{anchor}"', page)
            self.assertNotIn('class="site-page work-learning"', page)
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
        catalog_path = self.root / "content/catalog.json"
        catalog_original = catalog_path.read_bytes()
        def invalid_history(entries):
            entry = next(e for e in entries if e.get("relocated_from"))
            entry["relocated_from"] = entry["id"]
        self.catalog(invalid_history)
        with self.assertRaisesRegex(ValueError, "relocated_from"):
            load_content(self.root)
        catalog_path.write_bytes(catalog_original)
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
            '<a href="https://arxiv.org/html/9901.12346v2">Fixture B</a></li></ol>'
            '<p><a href="#cite-fixture">[fixture alternate format]</a></p>'
            '<ol><li id="cite-fixture"><a href="https://arxiv.org/pdf/9901.12345v1">'
            'Fixture A</a></li></ol>')
        source.write_text(source.read_text().replace("</body>", fixture + "</body>"))
        before = tree(self.root)
        data, errors = derive(self.root)
        self.assertEqual([], errors)
        self.assertEqual(before, tree(self.root))
        for key in ("arxiv:9901.12345@v1", "arxiv:9901.12346@v2"):
            row = next(s for s in data["sources"] if s["source_key"] == key)
            self.assertEqual({"current", "historical"}, {u["role"] for u in row["used_in"]})
            self.assertTrue(any(r["url"].endswith("#ref-fixture") for r in row["local_references"]))
        row = next(s for s in data["sources"] if s["source_key"] == "arxiv:9901.12345@v1")
        self.assertTrue(any(r["url"].endswith("#cite-fixture") for r in row["local_references"]))
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
