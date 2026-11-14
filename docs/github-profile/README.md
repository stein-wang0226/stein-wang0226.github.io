<a href="https://stein-wang0226.github.io/about/"><img src="./assets/header.jpg" alt="Yuxiang Wang · Research and notes" width="1280"></a>

# Yuxiang Wang / 王煜祥

> I study how agents learn from interaction, and how to evaluate what they can actually do.

**Fudan University · M.S. in Artificial Intelligence**<br>
GUI Agent Data Algorithm Intern at **ByteDance Seed / AI Data**. Previously at **Alibaba AIR**. Advised by [Baojian Zhou](https://baojian.github.io/).

**[Homepage](https://stein-wang0226.github.io/about/)** &nbsp; / &nbsp; **[CV](https://stein-wang0226.github.io/cv/)** &nbsp; / &nbsp; **[Stein’s Notes](https://stein-wang0226.github.io/blog/)** &nbsp; / &nbsp; [Scholar](https://scholar.google.com/citations?hl=en&user=PCoqb3wAAAAJ) &nbsp; / &nbsp; [Email](mailto:25210980109@m.fudan.edu.cn)

## Research in practice

<table width="100%">
<tr>
<td valign="top" width="50%">
<h3>Scientific task synthesis</h3>
<p><strong>AutoResearch</strong><br>Expert protocols into executable Harbor tasks, with independent verification and difficulty calibration. Delivered <strong>2,000+ task packages</strong> for Qwen post-training.</p>
<p><a href="https://stein-wang0226.github.io/cv/#autoresearch">Methods &amp; delivery</a></p>
</td>
<td valign="top" width="50%">
<h3>Learning from tool use</h3>
<p><strong>ProtAgent</strong><br>Tool-Trajectory SFT and step-level RL for protein agents. OOD-1000 annotation-coverage success: <strong>40.2% SFT → 61.0% RL</strong>.</p>
<p><a href="https://arxiv.org/abs/2610.33746">Paper</a> / <a href="https://stein-wang0226.github.io/cv/#protagent">Training &amp; evaluation</a></p>
</td>
</tr>
<tr>
<td valign="top">
<h3>Reliable computer use</h3>
<p><strong>GUI agents</strong><br>Reproducible environments, independent oracles and failure replay. Turn real execution failures into verifiable tasks for SFT and RL.</p>
<p><a href="https://stein-wang0226.github.io/cv/#gui-agent">Environments &amp; data</a></p>
</td>
<td valign="top">
<h3>Models for science</h3>
<p><strong>Holon / ProtText-Eval</strong><br>Protein–Text pretraining, CPT and scientific SFT across <strong>0.6B–8B</strong> models, connecting instruction alignment to scientific evaluation.</p>
<p><a href="https://stein-wang0226.github.io/cv/#holon">Training &amp; evaluation</a></p>
</td>
</tr>
</table>

## Selected papers

| Work | Focus | Status |
| --- | --- | --- |
| [Semantic DLM+](https://arxiv.org/abs/2606.15327) | Semantic diffusion | **NeurIPS 2026 · Accepted** |
| [Trainability of masked diffusion LMs](https://arxiv.org/abs/2604.24832) | Blockwise locality | First author · ACL 2027 under review |
| [ProtAgent](https://arxiv.org/abs/2610.33746) | Interaction-level credit assignment | First author · ARR under review |

<details>
<summary>More research &amp; evaluation context</summary>

- [CUA-Recovery](https://stein-wang0226.github.io/publication/cua-recovery/) studies error recovery in long-horizon computer-use agents. ICLR 2027 under review.
- [STM](https://doi.org/10.1007/978-981-95-3906-2_3) studies dynamic-graph fraud detection. DASFAA 2025; first author.

[All publications](https://stein-wang0226.github.io/publications/) / [English resume](https://stein-wang0226.github.io/assets/Curriculum_Vitae.pdf) / [中文简历](https://stein-wang0226.github.io/assets/Yuxiang-Wang-Resume-zh.pdf)

</details>

## Code & notes

**Public research code**<br>
[Masked diffusion trainability](https://github.com/stein-wang0226/trainable-masked-diffusion) — structured-task experiments on autoregressive and diffusion models.<br>
[STM](https://github.com/stein-wang0226/STM) — spatio-temporal modeling for dynamic-graph fraud detection.

**[Stein’s Notes](https://stein-wang0226.github.io/blog/)** connects principles, implementations and experiments:

| Start with | Read about |
| --- | --- |
| [LLM training lifecycle](https://stein-wang0226.github.io/llm-training-lifecycle/) | Pretraining, CPT, SFT and RL |
| [Agent tasks & benchmarks](https://stein-wang0226.github.io/agent-data-benchmarks/) | Executable task synthesis and reliable evaluation |
| [Agent harnesses](https://stein-wang0226.github.io/agent-harness-guide.html) | Tool execution, context management and memory |
| [Diffusion language models](https://stein-wang0226.github.io/dlm-survey/) | Training, generation and model design |
