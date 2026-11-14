---
title: Holon：蛋白质、文本与结构的统一建模
---

<p><a href="../">My Work 目录</a> · <a href="full-report.html">完整研究报告：21 节方法与实验</a></p>

## 研究问题与主要结论

Holon 的目标是在同一模型接口中连接蛋白质序列、自然语言与离散结构表示。它以 Qwen2/Qwen3 的文本能力为起点，采用蛋白 tokenizer 和按模态分配参数的 Mixture-of-Transformers（MoT），逐步学习序列先验、蛋白与文本的条件关系及科学任务的输出行为。仓库还保留 dense ProteinQwen3 和 MoE 对照，因此“Holon”应理解为模型、数据、训练和评测组成的研究体系。[1](#ref-1)[2](#ref-2)

项目最有价值的方法链是：**模态参数分工 → 蛋白序列预训练 → 双向继续预训练 → 科学指令微调 → 分层验证条件利用**。序列 loss 降低、文本匹配敏感性增加、结构预测改善分别回答不同问题，不能由其中一个数字替代整体科学能力。[1](#ref-1)

## 模型如何连接不同模态

文本使用 Qwen 的词表与初始化；蛋白质序列通过蛋白 tokenizer 进入专门的嵌入和输出接口。MoT 在共享序列中根据 token 所属路由选择参数路径，让不同模态使用各自的投影、归一化和 FFN，再将表示恢复到原来的序列顺序参与注意力。这个路由依据模态或任务标记，不应与学习型 top-k MoE router 混为一谈。[2](#ref-2)[3](#ref-3)

实际 `forward_train` 把 understanding 和 generation token 分别送到两套 Q/K/V 投影，再按原索引拼回。`freeze_und` 控制文本侧是否冻结，具体哪些参数和激活停止梯度须读实现。下面是源码流程的精简表达，不是可直接替换的实现：

```text
packed sequence + modality indexes
  → understanding tokens → Q/K/V
  → generation tokens    → Q/K/V_moe_gen
  → restore original indexes
  → position encoding + packed attention
  → modality-specific output path
```

这使跨模态交互和参数隔离可以同时存在，但也引入模态边界、tied head、checkpoint shape 和冻结策略的一致性要求。dense 路线用于检查专门路由的收益与额外成本，MoE 路线则另外研究稀疏容量及优化稳定性。[1](#ref-1)[3](#ref-3)

## 数据与训练阶段

| 阶段 | 输入与监督 | 学习目标 | 需要保留的交接物 |
| --- | --- | --- | --- |
| 蛋白预训练 | UniRef 等序列、多序列 packing | 蛋白 token 的自回归 CE，建立序列分布先验 | tokenizer、边界布局、checkpoint、训练 token 账本 |
| 双向 CPT | P2T、T2P、protein-only；P1/P2/P3 等条件视图 | 生成方向与条件接口；按配方优化 text/protein CE | 方向标签、冻结策略、resolved data YAML、实际配比 |
| 科学 SFT | 蛋白及任务指令；分类、生成式分类和结构任务 | 任务输出行为与有监督的答案接口 | 监督区间、标签空间、split、目标头与解码 |
| 结构扩展 | 氨基酸序列与离散 structure token | sequence/structure 建模、正折叠与逆折叠 | codec 版本、有效残基、配对和结构质量筛查 |

阶段总结依据统一报告与仓库入口；不同实验分支不必顺序执行表中所有阶段。科学 SFT 的计划稿、参考论文设想和已实现分类路径应分别呈现，结构路线也不能由“存在 codec”推断全部端到端实验已完成。[1](#ref-1)[2](#ref-2)

一个 T2P 样本可以将文本条件放在上下文中，以蛋白 token 为主要预测目标；对应 P2T 视图从序列预测描述。双向样本的“配对正确”必须由 accession、序列和清洗规则确认。训练与 C30/Temporal 评测还需要在聚类、来源比例和视图构造上避免泄漏；精确序列不重复并不充分保证同源分布隔离。[1](#ref-1)

## 从目标 token 比例到可执行采样

canonical mixed CPT 声明 `P2T:T2P:protein-only = 1:1:98`。这是目标 token 暴露比例。`PackedDataset` 在记录级选择数据组，再按实际输入长度 packing，因此记录采样权重需要考虑有效样本率和每条样本的 token 产出。[2](#ref-2)[4](#ref-4)

```text
yield_i = valid_rate_i × mean_valid_packed_length_i
weight_i ∝ target_token_share_i / yield_i
corrected_weight_i = old_weight_i × target_share_i / observed_share_i
```

可复现的数据配比包含三层：声明比例的 source YAML、可执行 `weight` 的 resolved YAML、跨 rank 汇总的 `token_mix_observed.json`。零 token 和过长样本被拒绝时会重新抽组，所以它们必须进入产出率估计。序列–结构路线还应区分 `packed_input_tokens` 与真正进入蛋白 CE 的 `supervised_prot_tokens`。[4](#ref-4)

这条方法路线的实际贡献是把“配方比例”变成可测量、可修正的暴露量。若比较 8:0:92 与 4:4:92，应同时审查实际 token share、重复暴露和有效数据来源，而不是只比较 YAML 中三个数字。

## Scaling 与优化怎样迁移到 CPT

仓库用 iso-FLOPs 实验研究模型规模、训练数据、batch 和学习率，并保留 Muon / AdamW、冻结与全参训练、ZeRO 和 checkpoint 的工程记录。预算迁移需要按当前激活的模型路径重新计算每 token FLOPs，再由算力预算解析训练 token 数。总参数与 active 参数是两个量，不能直接互换。[1](#ref-1)[5](#ref-5)

当前 README 的架构感知 C1e20 Muon v3 profile 记录 `N_active=440,401,920`、`M=2,837,839,872 FLOPs/token`、global batch `479,232 tokens`，由 `round(C/M)` 得到约 35.2B 训练 tokens。它是特定 decoder path 的预算解析，不能推广为所有 Holon 规模的通用常数。历史 `S_eff=284` 仍是暂用参考，后续应以 packed telemetry 重新校准。[2](#ref-2)[5](#ref-5)

## 如何证明模型使用了文本条件

单看 protein loss 或某个 fitness 分数无法确认模型在利用文本。统一报告将几种证据分开：[1](#ref-1)

- **序列能力**：无文本条件的 CE/NLL、ProteinGym 等 rank correlation，描述蛋白分布适应。
- **条件利用**：正确文本、错配文本、空条件和不同描述层级之间的对照，检查配对敏感性。
- **泛化范围**：C30、Temporal、OOD-safe 等 split 与来源审计，约束可解释的人群。
- **结构与科学输出**：结构任务、生成与编辑评测、分类任务，分别采用相应目标和指标。

Negative Ladder v2 的正式 checkpoint×tier 终点为
`(PSC_L3 − PS8_L3) − (PSC_L0 − PS8_L0)`，报告 `+0.0051416 NLL`，95% CI `[0.0037273, 0.0066557]`，采用 union-component block bootstrap。PS8 的绝对 margin 在 L0、L3 均更高；PSC 的优势是从 L0 到 L3 的敏感性下降较小。这个交互效应不能改写成“PSC 绝对对齐更强”。[6](#ref-6)

每种 recipe 只有一个训练 seed，实际 token share 尚无独立审计，expanded pool 也不是 strict protein-OOD。因此支持的是冻结样本上的 checkpoint-level 结论，不支持配方因果效应、多种子稳健性或细粒度生物学理解。完整报告保留这个边界与未执行的 replication 设计。[6](#ref-6)

## 实现入口与复核范围

阅读源码可按 `modeling/holon/ → data/ → train/ → eval/` 顺序：先确认参数路由，再确认输入、loss mask、实际 sampling，最后确认 checkpoint 与 scorer 的布局是否一致。长代码、完整实验总表、结构路线和 ProtText-Eval 的细节在[完整报告](full-report.html)中保留。

本页复核范围是项目定位、MoT 投影路由、token-mixture 校准、当前 CPT 预算与 Negative Ladder 结论解释。没有在本次整理中重新运行训练或对全部实验表独立复算。

## 来源与固定版本

所有仓库链接固定到 `7de0f4d67f9d18d166e715f6e4e200de22cb21ea`，需要私有仓库访问权限。

1. <span id="ref-1"></span>[统一研究报告](https://github.com/stein-wang0226/Holon/blob/7de0f4d67f9d18d166e715f6e4e200de22cb21ea/docs/reports/Holon_Unified_Report_202611.html)：2026-11-11 深入研究版。
2. <span id="ref-2"></span>[README：模型、配置与训练入口](https://github.com/stein-wang0226/Holon/blob/7de0f4d67f9d18d166e715f6e4e200de22cb21ea/README.md)。
3. <span id="ref-3"></span>[qwen3_navit.py](https://github.com/stein-wang0226/Holon/blob/7de0f4d67f9d18d166e715f6e4e200de22cb21ea/modeling/holon/qwen3_navit.py#L294-L360)：模态索引与投影装配。
4. <span id="ref-4"></span>[CPT token mixture calibration](https://github.com/stein-wang0226/Holon/blob/7de0f4d67f9d18d166e715f6e4e200de22cb21ea/docs/data/token_mix_calibration.md)：比例、产出率、实测与反馈。
5. <span id="ref-5"></span>[Scaling → CPT transfer](https://github.com/stein-wang0226/Holon/blob/7de0f4d67f9d18d166e715f6e4e200de22cb21ea/docs/scaling/cpt_scaling_transfer.md)：active FLOPs 与预算。
6. <span id="ref-6"></span>[Negative Ladder PS8→PSC 结果](https://github.com/stein-wang0226/Holon/blob/7de0f4d67f9d18d166e715f6e4e200de22cb21ea/docs/benchmark/PROTEIN_TEXT_NEGATIVE_LADDER_V2_PS8_PSC_RESULT.md)：注册终点、CI 与 claim scope。
