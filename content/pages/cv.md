---
layout: archive
title: "Curriculum Vitae"
permalink: /cv/
author_profile: true
redirect_from:
  - /resume
---

**Yuxiang Wang · 王煜祥**<br />
Agentic RL · Scientific Task Synthesis · GUI Agent Data · Diffusion Language Models · AI4S

[Email](mailto:25210980109@m.fudan.edu.cn) · [GitHub](https://github.com/stein-wang0226) · [Google Scholar](https://scholar.google.com/citations?hl=en&user=PCoqb3wAAAAJ)

<div class="profile-downloads">
<a href="/assets/Curriculum_Vitae.pdf" download="Yuxiang-Wang-Resume-en.pdf">English resume · PDF · 3 pages</a>
<a href="/assets/Yuxiang-Wang-Resume-zh.pdf" download="Yuxiang-Wang-Resume-zh.pdf">中文研究简历 · PDF · 2 页</a>
</div>

Updated from my November 2026 research resumes. The PDFs are original author-supplied snapshots; this online CV adds research links and preserves historical experience.

<nav class="profile-jump-links" aria-label="CV sections">
<a href="#education">Education</a>
<a href="#industry-experience">Experience</a>
<a href="#selected-projects">Projects</a>
<a href="#research-experience">Research</a>
<a href="#publications">Publications</a>
<a href="#skills">Skills</a>
</nav>

## Education

**M.S. in Artificial Intelligence · Fudan University** · 2025.09–2028.06 (expected)

- School of Data Science, Knowledge Works Lab; advisor: [Prof. Baojian Zhou](https://baojian.github.io/).
- Admitted via recommendation (推免).
- Courses include NLP & LLMs, Multimodal LLMs, Optimization, High-Dimensional Statistical Inference, Deep Learning & Spatial Intelligence, and Frontier AI Algorithms.

**B.Eng. in Computer Science · Hangzhou Dianzi University, Zhuoyue Honor College** · 2021.09–2025.06

- Honors / science and engineering experimental class; **GPA 4.59/5.0, top 1%**.
- Outstanding Graduate; HDU ACM Training Team.
- Foundation in algorithms, operating systems, compilers, computer architecture, and mathematics.

## Industry Experience

### ByteDance · Seed / AI Data

**GUI Agent Data Algorithm Intern** · 2026.09–Present

- Build reproducible professional-software environments, validate independent oracles, and audit GUI execution evidence for SFT / RL data admission.
- Diagnose trace failures and reconstruct real cases as RL tasks with frozen initial conditions and clean-VM replay.
- Detailed scope: [GUI Agent data & environments](#gui-agent).

### Alibaba · Platform Technology / AIR Program

**Research Intern · AI4S / Multimodal LLMs / Agents** · 2025.12–2026.09

- Scientific Harbor task synthesis for Qwen post-training; [AutoResearch](#autoresearch).
- Protein tool-use agents and step-level reinforcement learning; [ProtAgent](#protagent).
- Protein–Text multimodal pretraining, CPT, SFT, and unified evaluation; [Holon / ProtText-Eval](#holon).

### Tianyi Transportation Tech · VLA Department

**Algorithm Engineer Intern · Intelligent Driving** · 2025.04–2025.07

- Designed and delivered an automated 4D pre-labeling pipeline integrating road prediction, 3D detection, semantic generation, and occupancy prediction.
- Resolved I/O, inference, and result-alignment incompatibilities across open-source algorithms for large-scale data production.
- Stack: PyTorch, CUDA, Linux, Docker, OpenPCDet, MMDetection3D, OpenCV.

## Selected Projects

<h3 id="autoresearch">AutoResearch · Scientific Harbor Task Synthesis</h3>

*Alibaba · Harbor tasks for Qwen post-training*

- **Expert protocol → executable task.** Engineered expert Skill / Protocol into data audit, task generation, calibration, rollout, refinement, evaluation, and SFT validation.
- **Quality and difficulty.** Used recursive task revision, rollout feedback, and Rubric Judge scoring. Solver / Verifier separation, multi-path calibration, and cross-model judging help distinguish evaluation defects, reasoning errors, and reward hacking.
- **Production system.** Built multi-agent batch generation with concurrency, resumable execution, and version tracking; **delivered 2,000+ Harbor task packages**.
- **Training connection.** Data was validated with **Qwen3.8-27B SFT** and delivered to the Qwen post-training team. My resume reports improvement on Terminal-Bench and related evaluations, without a numerical improvement claim. Related tasks submitted to Terminal-Bench Sci passed one review round.

<h3 id="protagent">ProtAgent · Protein Tool Use &amp; Step-Level RL</h3>

*Alibaba · Qwen3-8B ReAct agent · First-authored manuscript under ARR review*

- **SFT → on-policy RL.** Built a tool-interaction agent for five protein annotation tasks. Tool-Trajectory SFT teaches tool selection, call format, and answer generation; RL improves behavior through real tool execution.
- **Step-level credit assignment.** Designed **Batched Step-Level REINFORCE** with intermediate tool rewards, repeated-call penalties, execution checks, and final-answer rewards. Compute reward-to-go per interaction step and update the corresponding response tokens.
- **Project evaluation.** On five equally represented tasks in **OOD-1000**, annotation-coverage success rates were **Base 14.1%, SFT 40.2%, RL 61.0%**; SFT → RL improves by **20.8 percentage points**.
- **Published ablation.** The arXiv paper reports three-seed mean success of **42.70% episode-level → 61.40% step-level** under identity return normalization. This is a separate comparison from the 61.00% main result. Annotation coverage measures recovery of reference annotations under the fixed tool protocol; it does not alone establish biological correctness.
- [arXiv paper](https://arxiv.org/abs/2610.33746) · [Research record](/publication/protagent/) · [Agentic RL study notes](/agentic-rl-guide.html).

<h3 id="gui-agent">GUI Agent Data &amp; Reproducible RL Environments</h3>

*ByteDance Seed / AI Data · Professional software and computer-use agents*

- **Environment validation.** Reimplemented professional desktop-app behavior in reproducible mock environments. Built **Setup → GUI Rollout → Verify → Reset**, trace replay, and artifact auditing. Checked independent oracles with positive and negative cases for reward judgment and regression validation.
- **Quality and failure analysis.** Validated prompts, attachments, checklists, and execution results for CAD, Blender, and SketchUp tasks. Applied different SFT / RL admission rules and reviewed **9,641 trace events**, analyzing end-state constraints, GUI perception, long-horizon execution, retries, time, and token cost.
- **Real failures → RL tasks.** Reconstructed dependencies, assets, and prerequisite software states from failure traces. Froze initial conditions, replayed critical actions in clean VMs, and checked both assets and state transitions to provide traceable environment packages.
- **Error attribution.** Distinguish application defects, agent execution failures, and environment issues before assigning training signals.

<h3 id="holon">Holon · Protein–Text Models &amp; ProtText-Eval</h3>

*Alibaba · Qwen3 / MoT · Protein understanding and generation*

- **Training lifecycle.** Participated in protein pretraining, multimodal CPT, and scientific SFT for bidirectional **Protein ↔ Text** modeling, T2P / P2T generation, and sequence–structure joint learning.
- **Data and scaling.** Mixed UniRef sequences with text–protein pairs; ran token-ratio, Muon optimizer, compute-budget, and scaling experiments from **0.6B to 8B**. Used fitness and paired-data controls to study capability retention and conditional modeling.
- **Instruction tuning.** In six SFT settings for the 0.6B model, mixing general and scientific data improved **IFEval by 29.02 percentage points** over scientific-only training.
- **Unified evaluation.** Built ProtText-Eval for text-guided generation, editing, and understanding, covering instruction alignment, sequence / structure quality, and downstream effects with multiple model baselines.
- [Training lifecycle study series](/llm-training-lifecycle/).

## Research Experience

### Blockwise Locality in Diffusion Language Models

*First author · Research period: 2025.10–2026.03 · ACL 2027 under review*

- [On the Trainability of Masked Diffusion Language Models via Blockwise Locality](https://arxiv.org/abs/2604.24832).
- Studied masked diffusion versus autoregressive trainability through in-context linear regression, star-graph path-finding, and Sudoku.
- Proposed Scatter and Jigsaw blockwise architectures, connecting local ordering to global iterative refinement.
- Research dates above describe the project; the public preprint was first posted on **2026-04-27**.

### Semantic Diffusion Language Models

- [Semantic DLM+](https://arxiv.org/abs/2606.15327) studies transition kernels through bias–variance trade-offs, exposure bias, and diversity. **NeurIPS 2026 Main Conference — Accepted.**
- The earlier [Semantic Diffusion Language Modeling](/publication/2026-semantic-diffusion-lm/) research record is preserved separately: semantic-neighborhood diffusion, shared refresh, frequency-prior correction, and **27.19 test PPL on LM1B**.
- Public citation metadata is maintained in the shared paper records.

### Dynamic-Graph Fraud Detection

*First author · Research period: 2023.04–2024.08 · DASFAA 2025*

- [STM: A Spatio-Temporal Model for Dynamic Graph Fraud Detection](https://link.springer.com/chapter/10.1007/978-981-95-3906-2_3).
- Graph condensation, distance-aware intra-frame aggregation, and difference-aware inter-frame aggregation capture spatial structure and temporal behavior.
- Project outcomes reported in the earlier CV include leading a national-level student innovation project and a granted invention patent. The chapter was published online on **2026-01-02**.

## Honors & Awards

- National Scholarship; Provincial Government Scholarship.
- Outstanding Graduate of HDU; lead PI of a National-level College Student Innovation Project.
- CUMCM: National Second Prize & Provincial First Prize.
- MCM / ICM: Meritorious Winner; Huawei Software Elite Challenge: Third Prize.
- HDU ACM Training Team; additional competition awards documented in the historical CV.
- Internal AI-coding recognition and talks, documented in the historical CV.

## Skills

- **Training & inference:** PyTorch, Transformers, Accelerate, DeepSpeed (ZeRO-2/3), FSDP2, distributed training, memory optimization, vLLM, FlashAttention-2.
- **Post-training & agents:** Tool-Trajectory SFT, step-level REINFORCE, DPO, PPO, GRPO, RLHF, reward design, preference data, LLM-as-a-Judge, ReAct tool use.
- **Systems:** Docker, Linux, Git, W&B, Slurm, GPU clusters; training scripts, experiment tracking, batch scheduling, and failure diagnosis.
- **Programming:** C++, Python, MATLAB, Java.

## Resume Downloads & History

The English research resume is **3 pages (78 KB)**; the Chinese research resume is **2 pages (259 KB)**. Both preserve the supplied files byte for byte.

- [English research resume](/assets/Curriculum_Vitae.pdf).
- [中文研究简历](/assets/Yuxiang-Wang-Resume-zh.pdf).
- [Historical CV PDF, before this update](/assets/archive/Curriculum_Vitae-before-20261114.pdf).

Project metrics come from the supplied resumes. Publication status is distinguished from public preprint metadata in each record below. The publication list is generated from shared records.
