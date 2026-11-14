"""Generate architecture review figures from cited specifications.

Run with Python + matplotlib; independent of site build dependencies.
No performance measurements or synthetic benchmark values.
"""
import csv
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets/research/architecture-20261114"
INK, GREEN, BLUE, GOLD, PAPER = "#172d35", "#0f766e", "#477d9b", "#b37b29", "#fcfbf7"
plt.rcParams.update({"font.family": "DejaVu Sans", "svg.fonttype": "none",
                     "svg.hashsalt": "stein-notes-architecture-20261114",
                     "font.size": 11, "text.color": INK, "axes.labelcolor": INK})
LAYERS = [
    {"model": "Qwen3.8-Flash-Next", "local_type": "GDN", "local_count": 36,
     "global_type": "QSA", "global_count": 12, "sources": "45;46"},
    {"model": "Kimi K3.1 Pro", "local_type": "KDA", "local_count": 69,
     "global_type": "Gated DSA", "global_count": 24, "sources": "47"},
    {"model": "GLM-5.3-Flash", "local_type": "KDA", "local_count": 34,
     "global_type": "DSA/MLA", "global_count": 11, "sources": "53"},
    {"model": "MiMo-V2.6 Pro", "local_type": "SWA", "local_count": 60,
     "global_type": "GA", "global_count": 10, "sources": "56"},
    {"model": "MiMo-V2.6 Flash", "local_type": "SWA", "local_count": 39,
     "global_type": "GA", "global_count": 9, "sources": "56"},
]
EXPERTS = [
    {"model": "Nemotron 3 Ultra", "hidden": 8192, "latent": 2048,
     "routed_experts": 512, "top_k": 22, "dimension_ratio": .25, "sources": "33;50;51"},
    {"model": "Kimi K3 / K3.1", "hidden": 7168, "latent": 3584,
     "routed_experts": 896, "top_k": 16, "dimension_ratio": .5, "sources": "5;47"},
]


def canvas(height):
    fig, ax = plt.subplots(figsize=(12, height), facecolor=PAPER)
    ax.set_facecolor(PAPER)
    return fig, ax


def save(fig, name):
    target = OUT / name
    fig.savefig(target, format="svg", facecolor=PAPER,
                metadata={"Date": None, "Creator": "Stein's Notes / architecture_figures.py"})
    target.write_text("\n".join(line.rstrip() for line in target.read_text().splitlines()) + "\n")
    plt.close(fig)


def box(ax, x, y, w, h, title, body, color=GREEN):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.015",
                               edgecolor=color, facecolor="white", linewidth=1.4))
    ax.text(x + w / 2, y + h * .72, title, ha="center", va="center",
            fontweight="bold", color=color, fontsize=11)
    ax.text(x + w / 2, y + h * .32, body, ha="center", va="center",
            fontsize=10, linespacing=1.5)


def arrow(ax, start, end, color=GREEN):
    ax.annotate("", xy=end, xytext=start,
                arrowprops={"arrowstyle": "->", "color": color, "lw": 1.6})


def history():
    fig, ax = canvas(5)
    ax.set(xlim=(0, 12), ylim=(0, 5)); ax.axis("off")
    ax.text(.15, 4.6, "History representation and access are separate design choices", fontsize=16, fontweight="bold")
    rows = [
        ("Token KV / MLA", "History -> per-token entries", "Query reads historical KV", "KV grows with N; MLA narrows each entry"),
        ("GDN / KDA / Mamba", "History -> recurrent state", "Query reads finite state", "Recurrent decode state need not grow with N"),
        ("QSA / DSA / MSA", "History -> searchable entries", "Select candidates -> attention", "Selector + gather + attention all have costs"),
        ("SWA + global", "Recent window + global layers", "Local and global paths coexist", "A window does not replace the full history path"),
    ]
    for i, (label, left, right, note) in enumerate(rows):
        y = 3.38 - i * 1.03
        ax.text(.15, y + .5, label, fontsize=11, fontweight="bold", color=GREEN)
        box(ax, 2.2, y + .05, 3.2, .78, "Write / retain", left)
        box(ax, 6.05, y + .05, 3.5, .78, "Read", right, BLUE)
        arrow(ax, (5.4, y + .44), (6.05, y + .44))
        ax.text(2.2, y - .18, note, fontsize=9, color=INK)
    fig.subplots_adjust(left=.025, right=.995, bottom=.025, top=.97)
    save(fig, "history-paths.svg")


def layers():
    fig, ax = canvas(5.1)
    for i, row in enumerate(LAYERS):
        local, glob = row["local_count"], row["global_count"]
        ax.barh(i, local, color=GREEN, height=.58)
        ax.barh(i, glob, left=local, color=BLUE, height=.58)
        ax.text(local / 2, i, f'{local} {row["local_type"]}', ha="center", va="center", color="white", fontsize=10)
        ax.text(local + glob + 1.6, i, f'{glob} {row["global_type"]}  |  total {local + glob}', va="center", fontsize=10)
    ax.set_yticks(range(len(LAYERS)), [r["model"] for r in LAYERS]); ax.invert_yaxis()
    ax.set_xlim(0, 128)
    ax.set_xlabel("Transformer blocks: composition only, not layer order / FLOPs / speed")
    ax.set_title("Hybrid layer counts from reports and pinned configs", loc="left", fontsize=16, fontweight="bold", pad=18)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    fig.subplots_adjust(left=.21, right=.985, top=.83, bottom=.22)
    fig.text(.21, .035, "Sources [45-47], [53], [56]. Nemotron submodule counts are excluded: they use a different counting unit.", fontsize=9)
    save(fig, "hybrid-layer-counts.svg")


def latent():
    fig, ax = canvas(5)
    ax.set(xlim=(0, 12), ylim=(0, 5)); ax.axis("off")
    ax.text(.2, 4.55, "LatentMoE: route narrower representations, then project back", fontsize=16, fontweight="bold")
    for i, row in enumerate(EXPERTS):
        y = 2.58 - i * 1.8
        ax.text(.2, y + 1.3, row["model"], fontsize=12, fontweight="bold", color=GREEN)
        box(ax, .2, y, 2.2, 1.03, "Hidden input", f'd = {row["hidden"]}')
        box(ax, 3, y, 2.25, 1.03, "Down projection", f'r = {row["latent"]}', BLUE)
        box(ax, 5.85, y, 3.05, 1.03, "Routed experts", f'{row["routed_experts"]} experts / top {row["top_k"]}')
        box(ax, 9.5, y, 2.2, 1.03, "Up projection", f'back to d = {row["hidden"]}', BLUE)
        for start, end in [((2.4, y + .52), (3, y + .52)),
                           ((5.25, y + .52), (5.85, y + .52)),
                           ((8.9, y + .52), (9.5, y + .52))]:
            arrow(ax, start, end)
        ax.text(3, y - .22, f'Width ratio r/d = {row["dimension_ratio"]:g}; payload ratio only under fixed assignment / precision', fontsize=9)
    ax.text(.2, .09, "Sources: Nemotron [33, 50-51], Kimi [5, 47]. Shared paths, normalization and additional gates omitted.", fontsize=9)
    fig.subplots_adjust(left=.025, right=.985, bottom=.025, top=.97)
    save(fig, "latent-moe-paths.svg")


def residual():
    fig, ax = canvas(5.1)
    ax.set(xlim=(0, 12), ylim=(0, 5.1)); ax.axis("off")
    ax.text(.15, 4.7, "Residual designs change which representations a layer reads", fontsize=16, fontweight="bold")
    rows = [
        ("Standard residual", "Current stream x", "x + F(Norm(x))", "Fixed additive path"),
        ("Attention Residuals", "Earlier layer / block states", "Softmax over depth", "Select previous representations"),
        ("mHC", "n parallel residual streams", "Constrained mixing + F", "Doubly stochastic residual mixing"),
        ("Gated Residual", "4 residual branches", "Elementwise gate read", "Qwen GR: channel-wise reading"),
    ]
    for i, (label, left, right, note) in enumerate(rows):
        y = 3.48 - i * 1.04
        ax.text(.15, y + .48, label, fontsize=11, fontweight="bold", color=GREEN)
        box(ax, 2.4, y, 3.35, .85, "Available state", left)
        box(ax, 6.5, y, 3.8, .85, "Operation", right, BLUE)
        arrow(ax, (5.75, y + .43), (6.5, y + .43))
        ax.text(2.4, y - .17, note, fontsize=9)
    fig.subplots_adjust(left=.025, right=.985, bottom=.025, top=.97)
    save(fig, "residual-designs.svg")


def export_data():
    for name, rows in [("hybrid-layer-counts.csv", LAYERS), ("latent-moe-specs.csv", EXPERTS)]:
        with (OUT / name).open("w", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
            writer.writeheader(); writer.writerows(rows)
    registry = json.loads((ROOT / "assets/research/2026-11-14/sources.json").read_text())
    nums = {int(n) for row in LAYERS + EXPERTS for n in row["sources"].split(";")}
    (OUT / "figure-data.json").write_text(json.dumps({
        "as_of": "2026-11-14", "measurement": False,
        "layer_counts": LAYERS, "latent_moe": EXPERTS,
        "layer_scope": "Transformer block composition, not sequential layer plan, FLOPs or performance",
        "payload_derivation": "r/d only when token assignment and bytes per value are fixed",
        "payload_excludes": ["metadata", "shared experts", "projections", "padding",
                             "replication", "network protocol", "load imbalance"],
        "sources": [{k: s[k] for k in ("number", "title", "version", "canonical_url")}
                    for s in registry["sources"] if s["number"] in nums],
    }, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    history(); layers(); latent(); residual(); export_data()
    print("Generated 4 SVGs, 2 CSVs and source-linked specification JSON.")
