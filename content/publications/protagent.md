---
title: "ProtAgent: Post-Training Compact Protein Tool Agents with Interaction-Level Credit Assignment"
collection: publications
permalink: /publication/protagent/
excerpt: 'A compact protein tool agent trained with SFT and on-policy REINFORCE. Step-level returns improve interaction-level credit assignment; ProtAgent-8B reaches 61.00% annotation-coverage success under a fixed closed-loop tool protocol.'
date: 2026-10-24
venue: 'ARR · Under review · First author'
paperurl: 'https://arxiv.org/abs/2610.33746'
citation: 'Yuxiang Wang, Baojian Zhou, Qifang Zhao, Keyue Jiang, Yanghua Xiao, Xiaoxiao Xu. "ProtAgent: Post-Training Compact Protein Tool Agents with Interaction-Level Credit Assignment." <i>arXiv:2610.33746</i>, 2026.'
---

## Status & Sources

The official title, author order, abstract, and public preprint date (**2026-10-24**) follow [arXiv:2610.33746v1](https://arxiv.org/abs/2610.33746v1). Yuxiang Wang is the first author. ARR review status follows my November 2026 resume; the arXiv posting date is not the ARR submission date.

## Training

- **Qwen3-8B ReAct agent** for five protein annotation tasks.
- **Tool-Trajectory SFT → On-Policy RL**, learning tool selection, call syntax, and answer generation before optimizing real tool interactions.
- **Batched Step-Level REINFORCE**, with intermediate tool rewards, repeated-call penalties, execution checks, and a final-answer reward.
- Reward-to-go is computed per interaction step and assigned to the corresponding response tokens.

## Project Evaluation

On the five-task balanced **OOD-1000**, the resumes report:

| Stage | Success rate |
|---|---:|
| Base | 14.1% |
| Tool-Trajectory SFT | 40.2% |
| SFT + Step-Level RL | 61.0% |

The RL stage improves over SFT by **20.8 percentage points**. The public paper reports **61.00% annotation-coverage success** for ProtAgent-8B under a fixed closed-loop protocol with real bioinformatics tools. This metric measures recovery of reference annotations under that protocol; it does not by itself establish biological correctness or complete evidence grounding.

## Credit-Assignment Ablation

The public abstract additionally reports a **three-seed** comparison of episode-level and step-level returns:

| Return normalization | Episode-level mean success | Step-level mean success |
|---|---:|---:|
| Identity | 42.70% | 61.40% |
| Group-relative | 36.50% | 58.20% |

The **61.40% three-seed mean** is a separate comparison from the **61.00% main reported result**. Episode-level returns assign one episode return to every action; step-level returns assign action and terminal rewards to the responses that produced them and to preceding actions. Both use on-policy REINFORCE.

[Project and industry context](/cv/#protagent).
