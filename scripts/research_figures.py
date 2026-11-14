"""Regenerate sourced research SVGs: python3 scripts/research_figures.py.

Requires matplotlib in the invoking Python, independent of the site builder.
No model measurements: all numerical values are report specifications or
explicit arithmetic. Labels remain text in exported SVGs.
"""
import csv
import json
import re
from html.parser import HTMLParser
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets/research/agent-data-benchmarks"
INK, GREEN, PAPER, GOLD, BLUE = "#172d35", "#0f766e", "#fcfbf7", "#b37b29", "#477d9b"
plt.rcParams.update({"font.family": "DejaVu Sans", "svg.fonttype": "none", "svg.hashsalt": "stein-notes-research-20261114",
                     "font.size": 11, "text.color": INK, "axes.labelcolor": INK})


def canvas(w, h):
    fig, ax = plt.subplots(figsize=(w, h), facecolor=PAPER)
    ax.set_facecolor(PAPER)
    return fig, ax


def save(fig, name):
    target = OUT / name
    fig.savefig(target, format="svg", facecolor=PAPER,
                metadata={"Date": None, "Creator": "Stein's Notes / research_figures.py"})
    target.write_text("\n".join(line.rstrip() for line in target.read_text().splitlines()) + "\n")
    plt.close(fig)


def box(ax, x, y, w, h, title, body, color=GREEN):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.015",
                               edgecolor=color, facecolor="white", linewidth=1.5))
    ax.text(x + w / 2, y + h * .72, title, ha="center", va="center",
            fontweight="bold", color=color, fontsize=12)
    ax.text(x + w / 2, y + h * .36, body, ha="center", va="center", fontsize=10, linespacing=1.65)


def arrow(ax, start, end, color=GREEN):
    ax.annotate("", xy=end, xytext=start,
                arrowprops={"arrowstyle": "->", "color": color, "lw": 1.6})


def ced():
    fig, ax = canvas(12, 5)
    ax.set(xlim=(0, 12), ylim=(0, 5)); ax.axis("off")
    ax.text(.2, 4.55, "CED: global cache and local state follow different paths", fontsize=17, fontweight="bold")
    box(ax, .2, 2.25, 2.1, 1.6, "Prompt tokens", "Causal history\nLong-prefix prefill")
    box(ax, 3, 2.25, 2.5, 1.6, "Encoder x20", "H_20 -> global projections\n3 cache groups, m=2")
    box(ax, 6.2, 2.25, 2.5, 1.6, "Decoder global", "C = H_20 W^KV\nZ = H_20 W^Z; m=1")
    box(ax, 9.4, 2.25, 2.3, 1.6, "Token decode", "Encoder + decoder\nRead shared global KV")
    arrow(ax, (2.3, 3.05), (3, 3.05)); arrow(ax, (5.5, 3.05), (6.2, 3.05))
    arrow(ax, (8.7, 3.05), (9.4, 3.05))
    box(ax, 3, .35, 5.7, 1.15, "Local SWA and per-layer queries", "Decoder tail replay: W=128; Q and SWA remain layer-specific", BLUE)
    arrow(ax, (4.25, 2.25), (4.25, 1.5), BLUE)
    arrow(ax, (8.7, .95), (10.55, 2.25), BLUE)
    ax.text(.2, .02, "Source: DeepSeek V4.1 v1, sections 2.2-2.3 / 3.2. Conceptual ownership, not a kernel schedule.", fontsize=9)
    save(fig, "ced-path.svg")


def layers():
    fig, ax = canvas(12, 5.1)
    palette = {"SWA": "#becac8", "Full": GREEN, "Reindex": GOLD, "Reuse": "#8fbfb3"}
    encoder = ["SWA"] * 2 + (["Full"] + ["Reuse"] * 5) * 3
    decoder = ["Full"] + ["Reuse"] * 3 + (["Reindex"] + ["Reuse"] * 3) * 4
    ax.set(xlim=(0, 21), ylim=(-.6, 3.7)); ax.axis("off")
    ax.text(0, 3.35, "CSA2: the actual 20 + 20 layer plan", fontsize=17, fontweight="bold")
    for y, row, offset in [(2.3, encoder, 1), (.9, decoder, 21)]:
        for i, mode in enumerate(row):
            ax.add_patch(Rectangle((i + .12, y), .83, .65, facecolor=palette[mode], edgecolor="white"))
            ax.text(i + .535, y + .32, {"SWA": "S", "Full": "F", "Reindex": "I", "Reuse": "R"}[mode],
                    ha="center", va="center", color="white" if mode == "Full" else INK, fontweight="bold")
            ax.text(i + .535, y - .2, str(i + offset), ha="center", fontsize=8)
    ax.text(0, 1.78, "Encoder: first 2 SWA-only; 3 groups x 6 layers, m=2", fontsize=11)
    ax.text(0, .37, "Decoder: 5 groups x 4 layers; one shared cache, m=1; each reindex refines its own top-k", fontsize=11)
    for i, (label, color) in enumerate(palette.items()):
        x = i * 4.5
        ax.add_patch(Rectangle((x, -.25), .35, .25, facecolor=color))
        ax.text(x + .5, -.14, label, va="center", fontsize=10)
    ax.text(0, 3.05, "F: create cache + index / I: reuse cache, rerank / R: reuse cache + selected positions", fontsize=10)
    save(fig, "csa2-layer-plan.svg")


def bytes_chart():
    rows = [
        {"group": "Encoder group 1", "entries_per_token": .5},
        {"group": "Encoder group 2", "entries_per_token": .5},
        {"group": "Encoder group 3", "entries_per_token": .5},
        {"group": "Decoder shared", "entries_per_token": 1.0},
    ]
    parts = [("Main E2M1 values", 256, GREEN), ("Main E4M3 scales", 32, "#8fbfb3"),
             ("Indexer E2M1 values", 64, BLUE), ("Indexer E8M0 scales", 4, GOLD)]
    fig, ax = canvas(12, 5)
    for i, row in enumerate(rows):
        left = 0
        for label, per_entry, color in parts:
            value = per_entry * row["entries_per_token"]
            ax.barh(i, value, left=left, color=color, height=.6, label=label if i == 0 else None)
            row[label] = value
            left += value
        row["bytes_per_token"] = left
        ax.text(left + 7, i, f"{left:g} B/token", va="center")
    ax.set_yticks(range(4), [r["group"] for r in rows]); ax.invert_yaxis()
    ax.set_xlim(0, 440); ax.set_xlabel("Global KV bytes per input token (specification-derived)")
    ax.set_title("890 B/token = 178 + 178 + 178 + 356", loc="left", fontsize=17, fontweight="bold", pad=20)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.legend(loc="upper left", bbox_to_anchor=(0, -.22), ncol=2, frameon=False, fontsize=10)
    fig.subplots_adjust(left=.20, right=.96, top=.82, bottom=.30)
    fig.text(.20, .025, "DeepSeek V4.1 v1 + OCP MX v1.0. Excludes SWA, weights, allocator, alignment, workspace and replication.", fontsize=9)
    save(fig, "global-kv-bytes.svg")
    with (OUT / "global-kv-bytes.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)
    (OUT / "figure-data.json").write_text(json.dumps({
        "as_of": "2026-11-14", "measurement": False,
        "source": "https://arxiv.org/html/2609.19969v1",
        "specification": {"main_channels": 512, "main_scale_block": 16,
                          "indexer_channels": 128, "indexer_scale_block": 32,
                          "value_bits": 4, "scale_bits": 8},
        "groups": rows, "total_global_bytes_per_token": sum(r["bytes_per_token"] for r in rows),
        "excludes": ["SWA", "weights", "Engram", "workspace", "padding/alignment",
                     "allocator", "shard replication", "partial tail blocks"],
    }, ensure_ascii=False, indent=2) + "\n")


def replay():
    fig, ax = canvas(12, 4.7)
    ax.set(xlim=(0, 12), ylim=(0, 4.7)); ax.axis("off")
    ax.text(.2, 4.25, "Bounded replay: keep global cache, rebuild local SWA", fontsize=17, fontweight="bold")
    for y, name, middle, end in [
        (2.3, "Encoder: global hit", "SWA miss -> replay last 128\nKeep existing global cache", "New suffix writes\nGlobal + SWA"),
        (.45, "Decoder: every prefill", "Replay last 128 encoder outputs\nThrough decoder layers", "SWA used for decode\nNever a prefix cache"),
    ]:
        box(ax, .2, y, 2.7, 1.35, name, "Global state already available")
        box(ax, 3.6, y, 4.2, 1.35, "Recompute local state", middle, BLUE)
        box(ax, 8.5, y, 3.2, 1.35, "Continue generation", end)
        arrow(ax, (2.9, y + .68), (3.6, y + .68))
        arrow(ax, (7.8, y + .68), (8.5, y + .68))
    ax.text(.2, .05, "Both replay only W tokens: approximate state recovery, not bit-exact L x W dependency reconstruction.", fontsize=10)
    save(fig, "bounded-replay.svg")


def synthesis():
    fig, ax = canvas(12, 5.1)
    ax.set(xlim=(0, 12), ylim=(0, 5.1)); ax.axis("off")
    ax.text(.2, 4.65, "From source material to a trainable, executable task", fontsize=17, fontweight="bold")
    items = [
        ("Source + protocol", "Issue / requirements / paper\nLicense + held-out split"),
        ("Environment + task", "Pinned build / data / state\nSolver-visible contract"),
        ("Independent checks", "Oracle + bad controls\nClean-sandbox handoff"),
        ("Calibrated episodes", "Fixed policy + budget\nFailures + artifact audit"),
    ]
    for i, (title, body) in enumerate(items):
        x = .2 + i * 3
        box(ax, x, 2.35, 2.6, 1.65, title, body)
        if i < 3: arrow(ax, (x + 2.6, 3.18), (x + 3, 3.18))
    box(ax, .2, .5, 5.6, 1.15, "Admit by training objective", "CPT: text/masks / SFT: verified actions / RL: repeatable reward", BLUE)
    box(ax, 6.2, .5, 5.6, 1.15, "Keep evaluation independent", "Family/repo/time hold-out; version + trials + cost + attribution", GOLD)
    arrow(ax, (10.5, 2.35), (9, 1.65))
    arrow(ax, (10.5, 2.35), (3, 1.65), BLUE)
    ax.text(.2, .08, "Editorial synthesis of SWE-Gym / R2E-Gym / ScienceIDE / Harbor; this workflow has not been run here.", fontsize=9)
    save(fig, "task-synthesis-flow.svg")


class SourceIndex(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows, self.current, self.in_title = [], None, False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "li" and re.fullmatch(r"ref-\d+", attrs.get("id", "")):
            self.current = {"id": int(attrs["id"][4:]), "title": "", "url": None}
        if tag == "a" and self.current is not None and self.current["url"] is None:
            self.current["url"] = attrs["href"]
            self.in_title = True

    def handle_data(self, data):
        if self.in_title:
            self.current["title"] += data

    def handle_endtag(self, tag):
        if tag == "a":
            self.in_title = False
        if tag == "li" and self.current:
            self.rows.append(self.current); self.current = None


def sources():
    series = ROOT / "content/series/agent-data-benchmarks"
    parser = SourceIndex()
    parser.feed((series / "index.html").read_text())
    if [s["id"] for s in parser.rows] != list(range(1, 53)):
        raise ValueError("Expected the reviewed 52-reference index")
    for source in parser.rows:
        source["kind"] = "paper" if "arxiv.org/" in source["url"] else "project_documentation"
        source["accessed"] = "2026-11-14"
        source["used_in"] = [
            "/agent-data-benchmarks/" + name for name in
            ("s01_task_synthesis.html", "s02_benchmark_map.html")
            if f'index.html#ref-{source["id"]}"' in (series / name).read_text()
        ]
    (OUT / "sources.json").write_text(json.dumps({
        "schema_version": 1, "as_of": "2026-11-14",
        "index": "/agent-data-benchmarks/#sources",
        "note": "Paper/team-reported claims; no local training or benchmark reproduction. "
                "Author-provided CV metrics are a separate provenance category. "
                "Generated from the authoritative HTML reference index.",
        "sources": parser.rows,
    }, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    if not OUT.is_dir():
        raise SystemExit(f"Create the designated asset directory first: {OUT}")
    ced(); layers(); bytes_chart(); replay(); synthesis(); sources()
    print("Generated 5 SVG figures + CSV + specification JSON + 52-source manifest")
