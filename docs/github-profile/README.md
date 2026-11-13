# Yuxiang Wang · 王煜祥

**Agentic RL · Scientific Task Synthesis · GUI Agents · Diffusion Language Models · AI4S**

I am a Master's student in Artificial Intelligence at **Fudan University** (2025–2028, expected), advised by [Baojian Zhou](https://baojian.github.io/) at the Knowledge Works Lab. I am currently a **GUI Agent Data Algorithm Intern at ByteDance Seed / AI Data**, following a Research Internship at Alibaba's Platform Technology / AIR Program.

My work connects **reproducible tasks → tool-use trajectories → SFT → reinforcement learning → evaluation**, with an emphasis on scientific agents and long-horizon computer use.

[Academic homepage](https://stein-wang0226.github.io/about/) · [Online CV](https://stein-wang0226.github.io/cv/) · [English resume PDF](https://stein-wang0226.github.io/assets/Curriculum_Vitae.pdf) · [中文简历 PDF](https://stein-wang0226.github.io/assets/Yuxiang-Wang-Resume-zh.pdf) · [Study notes](https://stein-wang0226.github.io/blog/) · [Email](mailto:25210980109@m.fudan.edu.cn)

## Selected Work

- **AutoResearch — scientific Harbor task synthesis.** Delivered **2,000+ task packages** for Qwen post-training. Built expert-protocol conversion, data audit, task generation, calibration, rollout, refinement, evaluation, and SFT validation with solver / verifier separation. Related Terminal-Bench Sci tasks passed one review round. [Details](https://stein-wang0226.github.io/cv/#autoresearch)
- **ProtAgent — step-level Agentic RL.** Trained a **Qwen3-8B ReAct agent** with Tool-Trajectory SFT and Batched Step-Level REINFORCE across five protein annotation tasks. Balanced OOD-1000 annotation-coverage success: **14.1% Base → 40.2% SFT → 61.0% RL** (**+20.8 percentage points** over SFT). [Paper](https://arxiv.org/abs/2610.33746) · [Details](https://stein-wang0226.github.io/cv/#protagent)
- **GUI Agent data & environments.** Built Setup → GUI Rollout → Verify → Reset workflows, independent oracle checks, and reproducible failure replay for professional software. Reviewed **9,641 trace events** and reconstructed real failure cases as RL tasks. [Details](https://stein-wang0226.github.io/cv/#gui-agent)
- **Holon / ProtText-Eval — Protein ↔ Text models.** Contributed to protein pretraining, multimodal CPT, scientific SFT, and evaluation from **0.6B to 8B**. In 0.6B SFT experiments, mixed general / scientific data improved IFEval by **29.02 percentage points** over scientific-only training. [Details](https://stein-wang0226.github.io/cv/#holon)

Project scales follow my November 2026 resumes; the ProtAgent paper describes its closed-loop protocol. Annotation coverage does not alone establish biological correctness; delivered task counts and a review round do not imply public release or benchmark acceptance.

## Research

- [Semantic DLM+](https://arxiv.org/abs/2606.15327) — **NeurIPS 2026 Main Conference — Accepted**.
- [On the Trainability of Masked Diffusion Language Models via Blockwise Locality](https://arxiv.org/abs/2604.24832) — **ACL 2027 under review**, first author.
- [ProtAgent: Post-Training Compact Protein Tool Agents with Interaction-Level Credit Assignment](https://arxiv.org/abs/2610.33746) — **ARR under review**, first author.
- [CUA-Recovery: Benchmarking Error Recovery in Long-Horizon Computer-Use Agents](https://stein-wang0226.github.io/publication/cua-recovery/) — **ICLR 2027 under review**.
- [STM: A Spatio-Temporal Model for Dynamic Graph Fraud Detection](https://doi.org/10.1007/978-981-95-3906-2_3) — **DASFAA 2025**, first author.

[All research records and source notes](https://stein-wang0226.github.io/publications/)

## Public Code

- [Blockwise diffusion trainability](https://github.com/stein-wang0226/trainable-masked-diffusion) — structured-task experiments comparing autoregressive and masked diffusion models.
- [STM](https://github.com/stein-wang0226/STM) — dynamic-graph fraud-detection experiments.
- [Terminal-Bench Science fork](https://github.com/stein-wang0226/terminal-bench-science) — my fork of the [Harbor framework benchmark repository](https://github.com/harbor-framework/terminal-bench-science).

## Open Study Notes

I maintain [Stein's Notes](https://stein-wang0226.github.io/blog/) on LLMs, agents, diffusion models, multimodal learning, and training systems.

- [Pretraining → CPT / Midtraining → SFT / RFT → RL](https://stein-wang0226.github.io/llm-training-lifecycle/)
- [Agentic RL](https://stein-wang0226.github.io/agentic-rl-guide.html)
- [Agent harnesses](https://stein-wang0226.github.io/agent-harness-guide.html)
- [Diffusion language models](https://stein-wang0226.github.io/dlm-survey/)

*Profile content updated from November 2026 research resumes.*
