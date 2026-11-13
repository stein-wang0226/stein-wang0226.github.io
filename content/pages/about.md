---
permalink: /
title: "Yuxiang Wang"
author_profile: true
redirect_from:
  - /about/
  - /about.html
---

I am **Yuxiang Wang (王煜祥)**, a Master's student in Artificial Intelligence at the [School of Data Science](https://sds.fudan.edu.cn/), [Fudan University](https://www.fudan.edu.cn/) (2025–2028, expected), advised by [Prof. Baojian Zhou](https://baojian.github.io/) at the [Knowledge Works Lab](http://kw.fudan.edu.cn/).

I work on **Agentic RL, scientific task synthesis, and reliable agent evaluation**: turning expert protocols and real execution failures into reproducible tasks, then connecting tool-use trajectories, SFT, reinforcement learning, and evaluation.

I am currently a **GUI Agent Data Algorithm Intern at ByteDance Seed / AI Data** (since September 2026). Previously, I was a Research Intern at **Alibaba, Platform Technology / AIR Program** (December 2025–September 2026), working on Harbor tasks for Qwen post-training, protein agents, and Protein–Text foundation models.

[Email](mailto:25210980109@m.fudan.edu.cn) · [GitHub](https://github.com/stein-wang0226) · [Google Scholar](https://scholar.google.com/citations?hl=en&user=PCoqb3wAAAAJ)

## Selected Work

<div class="profile-work-grid" markdown="1">

<article class="profile-work" markdown="1">

<p class="profile-work-label">01 · Scientific task synthesis</p>

### AutoResearch · Harbor tasks

**2,000+ task packages delivered** for Qwen post-training. I built the path from expert Skill / Protocol to data audit, task generation, calibration, rollout, refinement, evaluation, and SFT validation.

Solver / Verifier separation, multi-path calibration, and cross-model Rubric Judge feedback help identify evaluation defects, reasoning failures, and reward hacking. Related Terminal-Bench Sci tasks passed one review round.

[Methods and delivery scope →](/cv/#autoresearch)

</article>

<article class="profile-work" markdown="1">

<p class="profile-work-label">02 · Agentic reinforcement learning</p>

### ProtAgent · Step-level RL

**Tool-Trajectory SFT → On-Policy RL** for a Qwen3-8B ReAct agent across five protein annotation tasks. Batched Step-Level REINFORCE assigns reward-to-go to each interaction step and its response tokens.

On the balanced **OOD-1000** project evaluation, annotation-coverage success rates were **14.1% Base → 40.2% SFT → 61.0% RL**: a **20.8 percentage-point** improvement over SFT.

[Training and evaluation →](/cv/#protagent) · [Paper →](https://arxiv.org/abs/2610.33746)

</article>

<article class="profile-work" markdown="1">

<p class="profile-work-label">03 · GUI agent data &amp; environments</p>

### Reproducible computer-use tasks

I build **Setup → GUI Rollout → Verify → Reset** workflows with trace replay, artifact auditing, and independently checked oracles for professional software.

Reviewed **9,641 trace events** to distinguish application defects, agent failures, and environment issues. Reconstructed real failure cases as RL tasks using frozen initial states, clean-VM replay, and checks on both assets and actions.

[Environment and data work →](/cv/#gui-agent)

</article>

<article class="profile-work" markdown="1">

<p class="profile-work-label">04 · AI4S multimodal training</p>

### Holon · Protein ↔ Text

Protein pretraining → multimodal CPT → scientific SFT on Qwen3 / MoT models, with model scaling from **0.6B to 8B**, token-mixture experiments, and Muon optimization.

In six SFT settings for the 0.6B model, mixing general and scientific data improved **IFEval by 29.02 percentage points** over scientific-only training. ProtText-Eval connects instruction alignment, sequence / structure quality, and downstream evaluation.

[Training and evaluation work →](/cv/#holon)

</article>

</div>

<p class="profile-evidence">Project scales follow my November 2026 research resumes; ProtAgent's evaluation protocol is described in arXiv:2610.33746. Annotation coverage does not alone establish biological correctness. Task delivery and one review round do not imply public release or benchmark acceptance.</p>

## Research Interests

- **Agent post-training** — tool-use SFT, step-level credit assignment, on-policy RL, long-horizon reasoning and recovery.
- **Agentic data & evaluation** — scientific task synthesis, executable verification, difficulty calibration, environment reproducibility.
- **Diffusion language models** — blockwise locality, transition kernels, training stability, and structured generation.
- **AI for Science & multimodal models** — protein agents, Protein–Text understanding / generation, CPT and evaluation.
- **Graph learning** — spatio-temporal reasoning and dynamic-graph fraud detection.

## News

- **November 2026** — **Semantic DLM+ accepted at the NeurIPS 2026 Main Conference.** [ProtAgent](https://arxiv.org/abs/2610.33746) is publicly available on arXiv and under ARR review; CUA-Recovery is under ICLR 2027 review. Details are maintained in the [publication records](/publications/).
- **2026.09** — Joined ByteDance Seed / AI Data to work on GUI Agent data and RL training environments.
- **2026.04** — First-authored [On the Trainability of Masked Diffusion Language Models via Blockwise Locality](https://arxiv.org/abs/2604.24832); currently under ACL 2027 review.
- **2025.12** — Joined Alibaba's AIR Program as a Research Intern.
- **2025.09** — Started my Master's at Fudan University, Knowledge Works Lab.
- **2025.06** — Graduated from HDU as an Outstanding Graduate; admitted to Fudan via recommendation.

## Background & Resume

I received my B.Eng. in Computer Science from the [Zhuoyue Honor College](https://zhuoyue.hdu.edu.cn/), [Hangzhou Dianzi University](https://www.hdu.edu.cn/), in June 2025, where I worked with [Prof. Wang](https://wyxlss.github.io/). My undergraduate GPA was **4.59/5.0 (top 1%)**.

<div class="profile-downloads">
<a href="/cv/">Online CV</a>
<a href="/assets/Curriculum_Vitae.pdf" download="Yuxiang-Wang-Resume-en.pdf">English resume · PDF · 3 pages</a>
<a href="/assets/Yuxiang-Wang-Resume-zh.pdf" download="Yuxiang-Wang-Resume-zh.pdf">中文研究简历 · PDF · 2 页</a>
</div>

The downloads preserve the author-supplied PDFs. The online CV also includes links to research records and historical experience.

## Open Study Notes

I share notes on LLMs, agents, multimodal learning, RL alignment, diffusion models, and training systems. Browse [博客与笔记](/blog/), including the [pretraining → CPT / midtraining → SFT / RFT → RL series](/llm-training-lifecycle/).
