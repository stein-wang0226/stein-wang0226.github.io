---
title: Trainable DLLM：生成顺序与块局部性
---

<p><a href="../">My Work 目录</a> · <a href="full-report.html">完整技术报告：理论、原图与结果</a></p>

## 研究问题：生成顺序也是训练变量

这项工作研究相同预测任务在不同生成顺序下的训练动力学。AR 为每个输出建立稳定的左到右条件，masked diffusion 在随机缺失状态中恢复 token；Scatter 和 Jigsaw 进一步改变块间调度、块内访问和提交时机。目标是定位依赖结构与学习难度的关系，而不是仅比较最终生成速度。[1](#ref-1)

方法路线是：**匹配规模与预算的受控模型 → ICL/路径搜索/Sudoku 依赖任务 → attention 与监督区间消融 → LM1B 语言建模 → 原始图表与运行日志对账**。不同任务偏好不同条件可见性，没有一个生成顺序在本报告的所有实验中统一占优。

## 目标函数与条件可见性

```text
AR:  pθ(x_1:L) = ∏_i pθ(x_i | x_<i)
MDM: x_(τ,i) = [MASK] with probability τ, otherwise x_i
L_MDM = E[ (1/τ) Σ_i 1[x_(τ,i)=[MASK]] · −log pθ(x_i | x_τ) ]
Block-Diff: pθ(x) = ∏_k pθ(block_k | earlier clean blocks)
```

AR 的 teacher forcing 与因果 mask 为每个位置规定固定预测上下文。MDM 共享模型处理许多随机掩码状态，双向上下文允许从后向前恢复答案，但某些训练状态会缺少关键局部绑定信息。Block-Diff 在块间保持因果顺序、块内去噪，让局部双向建模与前缀提交结合。[1](#ref-1)

这里的吸收式目标是概括形式，实际 noise schedule、SUBS 参数化、loss normalization 和 sampler 需要结合相应实现。不能从公式推断所有分支的计算成本一致。

## Scatter 与 Jigsaw 的路线

Scatter 把序列分成块，以块内 offset 为推进轴：先处理每块 offset 0，再处理 offset 1，直至完成所有层。较早提交的 offset 为后续层提供条件，跨块同 offset 可在一次前向中计算。Jigsaw 先 probe 未提交块的平均预测熵，选择最低熵块，块内保持因果生成，再提交并重复。[1](#ref-1)

| 方法 | 调度与局部可见性 | 需要检查的条件 |
| --- | --- | --- |
| AR | 整体左到右 | 首个决策是否需要未来信息 |
| 标准 MDM | 随机缺失、双向恢复 | 训练 mask 中是否保留关键绑定 |
| Block-Diff | 块间左到右、块内去噪 | 逆向依赖能否跨越未提交块 |
| Scatter | 按 offset 推进 | 所用 backbone 对同 offset 的具体 attention |
| Jigsaw | 熵选择块、块内因果提交 | probe 与提交可见范围、监督密度和训推匹配 |

**本次源码复核补充：LM1B 的同 offset 可见性。** `experiments/lm1b/models/scatdit.py` 的 `scatdiff_mask` 使用
`(pos_q == pos_kv) & (x0_flag_q == x0_flag_kv)`；这一条件不检查 block id，因此同一侧、相同 offset 的跨块 token 存在 attention 边。原报告中的“同层不同块没有 attention 边”概念描述不能直接套用于这个 LM1B backbone。结构化实验与 LM1B 使用不同实现，比较时必须绑定各自模型路径。[2](#ref-2)

LM1B 训练还可能将 `[x_t || x_0]` 拼接为两个分支；允许访问哪些干净位置由 mask 控制，同目标位置的 gold 不能直接可见。`sample_mode` 切换推理条件，输出裁剪、SUBS 和监督 mask 有各自作用。不能仅因输入含 x0 判定泄漏，也不能因为未掩位置 loss 为零就认为潜在 attention 泄漏无害。[2](#ref-2)[3](#ref-3)

## Jigsaw 的训练变体与监督密度

LM1B 的 `jigsaw_prefix` 选择一个 frontier target block：之前的块可见，target 与后面的块被 mask，但只有 target block 进入 loss。它使用 `cross_attn:false`、`attention_mode:causal_unmasked`、`training_mask_mode:prefix_target`，与默认随机 mask 全序列的监督密度不同。[4](#ref-4)

`jigsaw_fixed` 对随机 mask 的多个块监督；`jigsaw_multi` 从同一 x0 产生 K 个不同 target 的前缀视图。multi 可以增加监督视图，但不等于增加 K 倍独立数据。生成顺序、监督数量和条件强度同时变化时，性能差异不能全部归因给“熵选择策略”。[3](#ref-3)[4](#ref-4)

```text
prefix_target:
  blocks before target → visible context
  target block         → hidden + supervised
  later blocks         → hidden + excluded from loss

multi_target_prefix:
  same x0 → K distinct frontier views → expanded batch
```

## 三类受控实验怎样解释局部性

| 任务 | 输入 → 输出 | 检验机制 | 指标 |
| --- | --- | --- | --- |
| ICL 线性回归 | 同一潜在 w 生成演示与查询 → 查询标签 | 算子估计与 query/label 局部绑定 | Respond MSE、阈值步数、FLOPs |
| 星图 Pathfinding | 置乱边列表、start/goal → 完整路径 | 第一跳需利用反向依赖 | 节点准确率与整条路径匹配 |
| Sudoku | 9×9 题面 → 全部棋格答案 | 行/列/宫的全局约束 | 空格 cell accuracy 与整盘准确率 |

ICL 每个序列共用一个潜在向量 `w`。在高斯噪声模型下，演示后验均值可写作
`μ=(X_PᵀX_P+σ²I)⁻¹X_Pᵀy_P`，查询的平方误差最优预测是 `X_R μ`。不同顺序仍可表达相同 Bayes 目标；实验研究的是如何通过训练学到该目标，而不是证明 AR 与扩散有不同统计最优解。[1](#ref-1)

ICL 主要设置 P=20、R=20、d∈{10,15,20}；AR 最稳定，Jigsaw 缩小高维差距，随机 mask 与 Scatter 的部分设置保留更高残差。有限数据 E1/E10 对照需区分 seen-sample 次数与独立任务数，重复训练样本不能被当作新增数据。[1](#ref-1)

星图只有一条分支通往指定终点，输出从起点前进但可以先从终点反向解析；AR 在决定第一跳时可能还没利用后面的路径信息。MDM 成功 seed 可以从 goal 反向解掩码，也存在失败 seed。Sudoku 则允许通过行、列、宫同时约束空格；row/column/box 坐标消融用于区分序列位置和二维拓扑。[1](#ref-1)

这些是任务特定观察，不能据此推出“扩散总更善于推理”或“AR 总更可训练”。模型大小、block size、初始化、seed、坐标和推理预算都影响对照。

## LM1B：似然、生成质量与计算口径

ARR 报告主要使用约 110M 的 backbone、长度 128、BERT-base-uncased tokenizer。语言模型模板默认长度可能为 1024，复跑时须显式固定 `model.length=128`。Test-PPL 测量留出似然估计，Gen-PPL 由外部 GPT-2 Large 为生成文本评分；两者不是同一困惑度。[1](#ref-1)

| 方法 | ARR Test-PPL | ARR Gen-PPL，T=1024 | 证据边界 |
| --- | ---: | ---: | --- |
| MDLM | 29.00 | 55.28 | 原稿值 |
| BD3-LMs，最佳块长4 | 28.16 | 45.43 | 单元格绑定 top-p 与采样文件 |
| Jigsaw control，最佳块长4 | 117.50 | 137.82 | 主表对应 prefix 运行 |
| Scatter，最佳块长16 | 26.35 | 36.16 | T sweep 混有不同 top-p，不能作为纯步数消融 |
| SEDD uniform | 43.31 | 48.63 | 留存 25 样本文件复算为 50.69，差异待对账 |

表中数字保留 ARR 口径。本次没有重新采样或复算 Test-PPL。仓库 audit 记录 32 个 Gen-PPL cell 中 27 个与论文精度一致，4 个 D3PM cell 缺逐样本证据，uniform SEDD T=1024 存在上述差异。完整 Test-PPL 独立评估日志仍未补齐。[5](#ref-5)[6](#ref-6)

Gen-PPL 比较必须记录 checkpoint、top-p、requested T、first-hitting、真实 NFE、样本数和外部 evaluator。某些历史 first-hitting 运行会跳过空步骤，相同 T 未必代表相同有效计算。NFE 相同也可能对应不同输入长度、缓存收益和前向 FLOPs，不能直接称为相同延迟。[1](#ref-1)

## 代码框架与复现状态

结构化实验通过 YAML 选择任务、采样器、骨干、loss 和解码；Accelerate 包装训练。checkpoint 保存模型、optimizer 和 step，验证 JSONL 保存任务指标。LM1B 用 Hydra 选择算法/模型/数据，Lightning 管理训练与重载；推理时要核对 EMA、精度和 attention 后端。[1](#ref-1)[6](#ref-6)

```text
structured: YAML → sampler → serializer/mask → model/loss
            → optimizer + checkpoint → held-out task metrics
LM1B: Hydra → tokenizer/packing → diffusion backbone
      → train/checkpoint → Test-PPL / sampling + external Gen-PPL
```

仓库记录 CPU 与单卡 Nebula MI308X smoke 通过结构化三任务及 LM1B Scatter/Jigsaw，含 optimizer-state reload 和有限指标。它们是小模型、小 fixture 的运行检查，不是论文质量重现。已恢复 ICL/Sudoku 曲线和部分 Pathfinding 运行，但 D5/P5 主图、ICL 的部分种子选择以及 task-affinity 的逐点 profiling 仍有缺口。[6](#ref-6)

下一轮方法实验应分别固定条件可见性、监督密度和计算预算，再扫 block size 或块选择策略。若优先核验既有论文结论，则先恢复缺失运行并对账，不能用新 smoke 替代历史证据。

## 来源与固定版本

仓库固定到 `28ed9621c93951f6032ce8a2ae28c115779ee918`；以下源码需要权限。

1. <span id="ref-1"></span>[ARR 技术报告](https://github.com/stein-wang0226/trainable-dllm-overview/blob/28ed9621c93951f6032ce8a2ae28c115779ee918/docs/reports/trainable-dllm-technical-report.html)：原理、原图、受控实验及语言实验。
2. <span id="ref-2"></span>[LM1B scatdit mask](https://github.com/stein-wang0226/trainable-dllm-overview/blob/28ed9621c93951f6032ce8a2ae28c115779ee918/experiments/lm1b/models/scatdit.py#L31-L60)：同 offset attention 的实际规则。
3. <span id="ref-3"></span>[Scatter diffusion](https://github.com/stein-wang0226/trainable-dllm-overview/blob/28ed9621c93951f6032ce8a2ae28c115779ee918/experiments/lm1b/diffusers/scatter_diffusion.py)与[Jigsaw diffusion](https://github.com/stein-wang0226/trainable-dllm-overview/blob/28ed9621c93951f6032ce8a2ae28c115779ee918/experiments/lm1b/diffusers/jigsaw_diffusion.py)：输入、监督与采样。
4. <span id="ref-4"></span>[Jigsaw prefix 配置](https://github.com/stein-wang0226/trainable-dllm-overview/blob/28ed9621c93951f6032ce8a2ae28c115779ee918/experiments/lm1b/configs/algo/jigsaw_prefix.yaml)。
5. <span id="ref-5"></span>[Gen-PPL 逐格审计](https://github.com/stein-wang0226/trainable-dllm-overview/blob/28ed9621c93951f6032ce8a2ae28c115779ee918/results/arr/lm1b_gen_ppl.csv)。
6. <span id="ref-6"></span>[Verification record](https://github.com/stein-wang0226/trainable-dllm-overview/blob/28ed9621c93951f6032ce8a2ae28c115779ee918/docs/verification.md)与[复现指南](https://github.com/stein-wang0226/trainable-dllm-overview/blob/28ed9621c93951f6032ce8a2ae28c115779ee918/docs/reproduction.md)：已验证范围、差异与缺失证据。
