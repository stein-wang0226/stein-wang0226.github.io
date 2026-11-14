---
title: Trainable DLLM：生成顺序与块局部性
---

<p><a href="../">My Work 目录</a> · <a href="full-report.html">完整技术报告：理论、原图与结果</a></p>

## 先记住：调度、可见性、监督分开控制

这项工作研究相同预测任务在不同生成顺序下的训练动力学。AR 为每个输出建立稳定的左到右条件，masked diffusion 在随机缺失状态中恢复 token；Scatter 和 Jigsaw 进一步改变块间调度、块内访问和提交时机。目标是定位依赖结构与学习难度的关系，而不是仅比较最终生成速度。[1](#ref-1)

方法路线是：**匹配规模与预算的受控模型 → ICL/路径搜索/Sudoku 依赖任务 → attention 与监督区间消融 → LM1B 语言建模 → 原始图表与运行日志对账**。不同任务偏好不同条件可见性，没有一个生成顺序在本报告的所有实验中统一占优。

<!-- WORK:KNOWLEDGE:START -->
## 知识讲解：生成顺序、可见性与可训练性 {#work-knowledge}

**AR（自回归）** 按固定顺序预测下一 token；训练时使用正确前缀，即 teacher forcing。**Masked diffusion** 从部分缺失的序列预测被遮蔽位置，推理时反复选择、恢复或提交 token。一次 forward 内可并行输出多个位置，不代表它们之间已经建立自回归依赖。

**Block** 是序列分组；**attention mask** 决定当前位置能读哪些 key/value；**loss mask** 决定哪些预测被监督。这三个概念不能混为一谈。可训练性关注固定预算下的收敛、稳定性与样本效率，可表达性关注是否存在能表示目标的参数；两种顺序能表示同一函数，也可能训练得很不一样。[1](#ref-1)

<figure class="work-mechanism">
<svg viewBox="0 0 840 220" role="img" aria-labelledby="dllm-order-title dllm-order-desc" xmlns="http://www.w3.org/2000/svg">
<title id="dllm-order-title">三种调度方式的块与位置关系</title><desc id="dllm-order-desc">自回归按序列位置推进，Scatter 按块内 offset 跨块推进，Jigsaw 按低熵选择块并在块内因果提交。调度不等于具体 attention mask。</desc>
<g fill="#f7f5f0" stroke="#a9cec7"><rect x="5" y="20" width="255" height="170" rx="6"/><rect x="292" y="20" width="255" height="170" rx="6"/><rect x="579" y="20" width="255" height="170" rx="6"/></g>
<g fill="#172d35" text-anchor="middle" font-family="system-ui,sans-serif" font-size="18"><text x="132" y="51">AR</text><text x="419" y="51">Scatter</text><text x="706" y="51">Jigsaw</text><text x="132" y="95" font-size="16">block 0 → block 1 → …</text><text x="132" y="125" font-size="15">固定左到右位置</text><text x="132" y="162" font-size="13">每次提交下一个 token</text><text x="419" y="95" font-size="16">offset 0 → offset 1 → …</text><text x="419" y="125" font-size="15">同 offset 跨块处理</text><text x="419" y="162" font-size="13">mask 取决于实际实现</text><text x="706" y="95" font-size="16">probe → 选低熵块</text><text x="706" y="125" font-size="15">块内因果生成 → 提交</text><text x="706" y="162" font-size="13">重复选择剩余未提交块</text></g>
</svg>
<figcaption>概念调度图，不能替代某个 backbone 的可见性矩阵。LM1B Scatter 的同 offset 跨块边在下面单独核对。<a href="#ref-1">1</a><a href="#ref-2">2</a></figcaption>
</figure>
<!-- WORK:KNOWLEDGE:END -->

## 目标函数与条件可见性

<div class="reading-math">\[
p_\theta(x_{1:L})=\prod_i p_\theta(x_i\mid x_{\lt i})
\]</div>

线性吸收噪声在时间 τ 以概率 τ 掩码，否则保留原 token。只在 masked 位置计算带时间权重的 CE：

<div class="reading-math">\[
\begin{aligned}
\ell_i&=-\log p_\theta(x_i\mid x_\tau)\\
L_{\rm MDM}
&=\mathbb E\left[
\frac1\tau\sum_i
\mathbf1\{x_{\tau,i}=m\}\ell_i\right]\\
p_\theta(x)
&=\prod_k p_\theta(x^{(k)}\mid x^{(\lt k)})
\end{aligned}
\]</div>

AR 的 teacher forcing 与因果 mask 为每个位置规定固定预测上下文。MDM 共享模型处理许多随机掩码状态，双向上下文允许从后向前恢复答案，但某些训练状态会缺少关键局部绑定信息。Block-Diff 在块间保持因果顺序、块内去噪，让局部双向建模与前缀提交结合。[1](#ref-1)

这里的吸收式目标是概括形式，实际 noise schedule、SUBS 参数化、loss normalization 和 sampler 需要结合相应实现。不能从公式推断所有分支的计算成本一致。

### 从公式看一次训练更新

对干净序列 x0 采样噪声时间 τ，按该 schedule 将部分 token 替换为 `[MASK]` 得到 xτ。模型输出每个位置的词表分布，但只在监督集合 S 上累积目标 CE。`1/τ` 对不同遮蔽程度作时间权重；其数值稳定性、τ 的范围和实际平均方式应读实现，不能把 τ=0 直接代入。

AR 的目标位置在给定正确前缀下训练；MDM 的目标在不同随机缺失上下文下训练。后者既能利用后面的可见信息，也必须面对缺失关键邻居的状态。Block-Diff 的因式分解是外层块顺序，块内条件分布仍要通过去噪或相应 sampler 得到，不能把它当成一遍 softmax 直接输出整个联合分布。

```text
clean x0 → sample mask/noise state → visible xτ
         → attention decides readable context
         → model distributions → loss mask selects supervised positions
         → weighted CE → optimizer update
```

训练输入中含 x0 分支不必然泄漏：要检查目标 query 是否能通过任何允许的 attention 路径读到自己的 gold。只检查 loss mask 排除了某些位置是不够的，因为被排除位置仍可能向目标传递信息。[2](#ref-2)[3](#ref-3)

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

<!-- WORK:EXAMPLE:START -->
### 用两块序列区分调度和 attention {#work-example}

以下为索引讲解，非新的实验数据。令序列是 `[a0,a1,a2 | b0,b1,b2]`，字母表示块，数字表示 offset。Scatter 的推进轴是 `[a0,b0] → [a1,b1] → [a2,b2]`。但“a1 与 b1 是否互相可见”由模型 mask 决定，不能从推进顺序直接得出。

在读取的 LM1B `scatdiff_mask` 中，xt 的 a1 query：

| key 位置或分支 | 该 mask 是否允许 | 原因 |
| --- | --- | --- |
| xt 的 a1 或 b1 | 允许 | 同 side、同 offset；不检查块号 |
| xt 的 a0 或 b0 | 不由这些规则允许 | xt→xt 规则仅同 offset |
| x0 的 a0 或 b0 | 允许 | xt query 的 offset 严格大于 x0 key |
| x0 的 a1 或 b1 | 不允许 | offset 必须严格小于，避免直接读取同层 gold |

这是这一函数的边集合，不是对所有实现的统一描述；后续层的多跳信息流、packing 和 sample mode 仍要结合完整 forward 检查。尤其应区分训练的 x0 侧可见性与推理时实际已经提交的条件。[2](#ref-2)[3](#ref-3)
<!-- WORK:EXAMPLE:END -->

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

### 熵选块为什么不等于选出正确块

给未提交块 b 的位置分布 p，先计算每个位置的熵，再取块内均值并选最小：

<div class="reading-math">\[
\begin{aligned}
H_b&=-\frac1{|b|}\sum_{i\in b}\sum_v p_{i,v}\log p_{i,v}\\
b^*&=\arg\min_{b\in U}H_b
\end{aligned}
\]</div>

U 是未提交块集合。**低熵表示确信，未必正确**；错误块提交后会影响后续条件。probe 与正式提交都计入计算预算。

因此一个充分的消融应固定 backbone、attention、supervised token 数及实际 forward 预算，再比较固定块顺序与熵选择。prefix/fixed/multi 的监督密度不同，只有同时记录 loss 分母、target block 数和重复视图才能解释其差异。[3](#ref-3)[4](#ref-4)

## 三类受控实验怎样解释局部性

| 任务 | 输入 → 输出 | 检验机制 | 指标 |
| --- | --- | --- | --- |
| ICL 线性回归 | 同一潜在 w 生成演示与查询 → 查询标签 | 算子估计与 query/label 局部绑定 | Respond MSE、阈值步数、FLOPs |
| 星图 Pathfinding | 置乱边列表、start/goal → 完整路径 | 第一跳需利用反向依赖 | 节点准确率与整条路径匹配 |
| Sudoku | 9×9 题面 → 全部棋格答案 | 行/列/宫的全局约束 | 空格 cell accuracy 与整盘准确率 |

ICL 每个序列共用潜在向量 w，先由演示估计 w，再预测查询。标准高斯先验与噪声下：

<div class="reading-math">\[
\begin{aligned}
\mu&=(X_P^\top X_P+\sigma^2I)^{-1}X_P^\top y_P\\
\widehat y_R&=X_R\mu
\end{aligned}
\]</div>

完整报告展开平方项配方与不可识别子空间。不同顺序可以表达同一 Bayes 目标；实验比较**训练是否学得到**。[1](#ref-1)

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

### 三种常见指标不能互相替代

**PPL=exp(平均 NLL)**，须固定 tokenizer、目标 token 与估计器。Test-PPL 测留出建模，Gen-PPL 由外部模型评生成；两者不能直接排序。扩散留出似然可能通过上界或估计得到，不能默认等同 AR 精确 NLL。

Sudoku 的 cell accuracy 统计棋格正确比例，整盘准确率要求所有目标空格和约束通过；高 cell accuracy 仍可能有大量无效棋盘。Pathfinding 的节点准确率与完整路径匹配也有相同差别。NFE 则只是网络前向次数：不同序列长度、probe、缓存和硬件条件下，每次 forward 的成本不同。

<!-- WORK:REVIEW:START -->
## 工作总结与未完成的证据闭合 {#work-review}

| 研究产物 | 已有价值 | 优先补齐 |
| --- | --- | --- |
| AR/MDM/Scatter/Jigsaw 的受控框架 | 将生成顺序与依赖任务连接 | 固定可见性、监督密度和计算的机制消融 |
| ICL/Pathfinding/Sudoku 记录 | 可定位的曲线与任务特定失败模式 | 缺失主图运行、seed 选择与逐点 profiling |
| LM1B 配置、采样和逐格表 | 区分 Test-PPL、Gen-PPL、top-p 与 T | 缺逐样本的 D3PM cell、SEDD 差异及留出评估日志 |
| CPU/单卡 smoke 与 reload | 小模型路径可运行、状态可恢复 | 按主表预算复现质量，不以 smoke 代替主实验 |

最稳妥的贡献表述是：研究块局部性与条件依赖如何影响训练，并提供可复核实现和任务分解。当前证据不足以把某条顺序推广为所有任务的最优策略，或把采样参数混合的 T sweep 解释成纯计算缩放规律。

## 按需补充基础知识

先读 [离散扩散目标](../../dlm-survey/s02_discrete.html)和[块扩散](../../dlm-survey/s03_block.html)，再看 [扩散方法比较](../../dlm-survey/s10_comparison.html)。注意力实现可接着复习 [Attention、位置编码与 KV cache](../../llm-architecture/s02_attention_position_cache.html)。通用理论和本项目实验记录应分别阅读。
<!-- WORK:REVIEW:END -->

## 五道项目面试追问

1. **同一生成顺序能确定 attention 吗？** 不能；调度决定提交先后，mask 决定可见性，loss mask 决定监督，分别查代码。
2. **输入含 x0 就泄漏吗？** 看目标能否沿允许的 attention 路径读到自己的 gold；loss 为零不阻止上下文传播。
3. **Jigsaw multi 增加 K 个视图是 K 倍数据吗？** 是同一 x0 的重复条件视图；独立数据与监督量分开计。
4. **Scatter T sweep 能解释算力规律吗？** 先固定 top-p、first-hitting、checkpoint 和真实 NFE；主表混有不同 top-p。
5. **较低训练 loss 能证明推理更强吗？** 用留出任务、整路径/整盘成功、预算与 seed 检查；不把 smoke 当主实验复现。

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

1. <a id="ref-1" href="https://github.com/stein-wang0226/trainable-dllm-overview/blob/28ed9621c93951f6032ce8a2ae28c115779ee918/docs/reports/trainable-dllm-technical-report.html">ARR 技术报告</a>：原理、原图、受控实验及语言实验。
2. <a id="ref-2" href="https://github.com/stein-wang0226/trainable-dllm-overview/blob/28ed9621c93951f6032ce8a2ae28c115779ee918/experiments/lm1b/models/scatdit.py#L31-L60">LM1B scatdit mask</a>：同 offset attention 的实际规则。
3. <a id="ref-3" href="https://github.com/stein-wang0226/trainable-dllm-overview/blob/28ed9621c93951f6032ce8a2ae28c115779ee918/experiments/lm1b/diffusers/scatter_diffusion.py">Scatter diffusion</a>与<a id="ref-3-jigsaw" href="https://github.com/stein-wang0226/trainable-dllm-overview/blob/28ed9621c93951f6032ce8a2ae28c115779ee918/experiments/lm1b/diffusers/jigsaw_diffusion.py">Jigsaw diffusion</a>：输入、监督与采样。
4. <a id="ref-4" href="https://github.com/stein-wang0226/trainable-dllm-overview/blob/28ed9621c93951f6032ce8a2ae28c115779ee918/experiments/lm1b/configs/algo/jigsaw_prefix.yaml">Jigsaw prefix 配置</a>。
5. <a id="ref-5" href="https://github.com/stein-wang0226/trainable-dllm-overview/blob/28ed9621c93951f6032ce8a2ae28c115779ee918/results/arr/lm1b_gen_ppl.csv">Gen-PPL 逐格审计</a>。
6. <a id="ref-6" href="https://github.com/stein-wang0226/trainable-dllm-overview/blob/28ed9621c93951f6032ce8a2ae28c115779ee918/docs/verification.md">Verification record</a>与<a id="ref-6-reproduction" href="https://github.com/stein-wang0226/trainable-dllm-overview/blob/28ed9621c93951f6032ce8a2ae28c115779ee918/docs/reproduction.md">复现指南</a>：已验证范围、差异与缺失证据。
