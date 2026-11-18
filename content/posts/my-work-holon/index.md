---
title: Holon：蛋白质、文本与结构的统一建模
---

<p><a href="../">My Work 目录</a> · <a href="full-report.html">完整研究报告：21 节方法与实验</a></p>

## 先记住：统一接口，分轴验收

Holon 的目标是在同一模型接口中连接蛋白质序列、自然语言与离散结构表示。它以 Qwen2/Qwen3 的文本能力为起点，采用蛋白 tokenizer 和按模态分配参数的 Mixture-of-Transformers（MoT），逐步学习序列先验、蛋白与文本的条件关系及科学任务的输出行为。仓库还保留 dense ProteinQwen3 和 MoE 对照，因此“Holon”应理解为模型、数据、训练和评测组成的研究体系。[1](#ref-1)[2](#ref-2)

**学习链：模态参数分工 → 序列先验 → 双向 CPT → 科学 SFT → 分轴评测。** 快速复习时先抓住三点：[1](#ref-1)

- **MoT 分开投影、共享交互**：参数按模态或任务路由，样本内 attention 仍能跨模态。
- **配方必须落到实际 token**：记录采样比例、输入比例、监督比例与 loss 权重各自登记。
- **科学能力分开验收**：序列 NLL、正确配对敏感性、结构几何与生物功能不能互相替代。

<!-- WORK:KNOWLEDGE:START -->
## 知识讲解：先区分表示、条件与监督 {#work-knowledge}

阅读本项目需要理解三个概念。**Tokenizer** 把氨基酸或文本变成离散编号；它决定序列长度和词表，不能用氨基酸个数直接代替 token 数。**条件建模** 学习“给定描述时哪些蛋白序列更可能”；它不同于把文本和序列各自训练得更流畅。**监督区间** 决定哪些位置产生 loss；一个 token 即使只作上下文，也可能通过注意力影响被监督位置。

P2T 从蛋白预测文本，T2P 从文本预测蛋白，protein-only 学习无文本序列先验：
<p class="math-notation"><strong>符号：</strong>\(p\) 为蛋白序列，\(t\) 为文本，\(p_\theta(\cdot)\) 为参数 \(\theta\) 定义的概率分布；字母 \(p\) 作序列变量与作概率函数时靠位置区分。这里 \(t\) 不是训练时间。</p>

<div class="reading-math">\[
\begin{aligned}
\mathrm{P2T}:&\ p_\theta(t\mid p)\\
\mathrm{T2P}:&\ p_\theta(p\mid t)\\
\mathrm{protein\ only}:&\ p_\theta(p)
\end{aligned}
\]</div>

双向训练不是确定性求逆：一个功能可以对应多个序列，一个序列也可以有多种描述。结构 codec 的离散 token、氨基酸残基与三维坐标同样要分层理解。[1](#ref-1)

<figure class="work-mechanism">
<svg viewBox="0 0 840 210" role="img" aria-labelledby="holon-route-title holon-route-desc" xmlns="http://www.w3.org/2000/svg">
<title id="holon-route-title">Holon 的表示、路由与监督</title><desc id="holon-route-desc">文本和蛋白 token 经各自参数投影，恢复序列顺序后共同参与注意力，再按目标模态计算交叉熵。</desc>
<g fill="#f7f5f0" stroke="#a9cec7"><rect x="5" y="25" width="190" height="65" rx="6"/><rect x="5" y="120" width="190" height="65" rx="6"/><rect x="240" y="25" width="175" height="65" rx="6"/><rect x="240" y="120" width="175" height="65" rx="6"/><rect x="460" y="65" width="175" height="80" rx="6"/><rect x="680" y="65" width="155" height="80" rx="6"/></g>
<g stroke="#0f766e" fill="none" stroke-width="2"><path d="M195 57H240M195 152H240M415 57H437V105H460M415 152H437V105M635 105H680"/></g>
<g fill="#172d35" text-anchor="middle" font-family="system-ui,sans-serif" font-size="17"><text x="100" y="52">文本 token</text><text x="100" y="75" font-size="13">上下文或预测目标</text><text x="100" y="147">蛋白 token</text><text x="100" y="170" font-size="13">独立词表与序列边界</text><text x="327" y="52">理解侧投影</text><text x="327" y="75" font-size="13">Q / K / V</text><text x="327" y="147">生成侧投影</text><text x="327" y="170" font-size="13">Q / K / V gen</text><text x="547" y="96">恢复原位置</text><text x="547" y="122" font-size="14">注意力与位置编码</text><text x="757" y="96">目标头与 CE</text><text x="757" y="122" font-size="14">按监督位置计算</text></g>
</svg>
<figcaption>机制图依据投影装配实现；具体 token 被分到哪一侧由任务布局和索引决定，不能简单把所有蛋白 token 等同于生成侧。<a href="#ref-3">3</a></figcaption>
</figure>
<!-- WORK:KNOWLEDGE:END -->

## 模型如何连接不同模态

### 同一个残基从字母到向量

文本侧的 Qwen tokenizer 按 BPE 合并规则切分子词，一个 token 可以覆盖多个字符。蛋白侧使用 ESM 词表，普通序列中每个残基占一个 token。例如蛋白片段 `IN` 会得到异亮氨酸 `I` 和天冬酰胺 `N` 两个 token，对应整数 ID 12 和 17。Holon 把蛋白起止标记登记在文本词表中，只有中间的残基去查蛋白表。[ESM 词表](https://huggingface.co/facebook/esm2_t33_650M_UR50D/blob/main/vocab.txt) · [Qwen 合并规则](https://huggingface.co/Qwen/Qwen3-0.6B/blob/main/merges.txt)

```text
位置        0                  1                2                3
token       <|protein_start|>  I                N                <|protein_end|>
取向量      Qwen 表[起始 ID]   蛋白表[12]       蛋白表[17]       Qwen 表[结束 ID]
输出        h₀                 h₁               h₂               h₃  → MoT
```

Tokenizer 输出整数。Embedding 层持有形状为「词表大小 × 隐藏维度」的浮点矩阵，每个 ID 选出其中一行。Holon 前向代码用下面两行完成蛋白侧查表和位置还原。[forward 源码](https://github.com/stein-wang0226/Holon/blob/7de0f4d67f9d18d166e715f6e4e200de22cb21ea/modeling/holon/holon.py#L238-L239)

```python
packed_prot_embedding = self.prot_embed_tokens(packed_prot_ids)
packed_sequence[packed_prot_indexes] = packed_prot_embedding
```

**预训练决定向量的起点，冻结策略决定它之后还会不会变。** 文本表从 Qwen checkpoint 载入。蛋白侧沿用 ESM 的编号规则，向量由 Holon 的蛋白表提供。比如从纯序列 checkpoint 扩展到结构阶段，已有氨基酸行继承训练结果，新结构行单独初始化。训练时 tokenizer 的编号规则保持固定；允许求梯度并纳入优化器的 embedding 权重会随 loss 更新，冻结的表则保留载入值。[模型接口与初始化记录](full-report.html)

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

### 从张量看 MoT 为什么能跨模态交互
<p class="math-notation">\(H\) 是 token hidden 表示；\(I_{\rm und/gen}\) 为两类模态路由的行索引，\(W\) 为对应投影参数。单头 \(Q,K\) 为 \(T\times d_h\)、\(V\) 为 \(T\times d_v\)，\(P\) 为 \(T\times T\) 注意力权重，\(O\) 为 \(T\times d_v\) 输出；\({}^\top\) 是转置，softmax 沿 key 位置归一。不同头型在计算前对齐共享关系。</p>

设 packed 表示有 T 行、每行 d 维；两类索引分别选出理解侧与生成侧。各路径计算投影，再 scatter 回原序列；K/V 同理。按单个注意力头写成：

<div class="reading-math">\[
\begin{aligned}
H&\in\mathbb R^{T\times d}\\
Q_{\rm und}&=H[I_{\rm und}]W_{Q,\rm und}\\
Q_{\rm gen}&=H[I_{\rm gen}]W_{Q,\rm gen}\\
P&=\operatorname{softmax}
\left(\frac{QK^\top}{\sqrt{d_h}}+M\right)\\
O&=PV
\end{aligned}
\]</div>

`M` 表示因果与 packed 样本边界等约束。**参数路径分开，不意味着 attention 矩阵按模态彻底断开。** 在合同允许的上下文范围内，蛋白目标仍能使用文本的 K/V。相反，两个不同样本即使拼在同一 batch，也不能因为物理相邻而相互读答案。GQA 的 Q 与 K/V 头数可能不同，上式是每个注意力头的概括，不声称三个矩阵的最后一维完全一致。

冻结策略也分两层：参数 `requires_grad=False` 与中间表示 `detach` 对梯度路径的影响不同；实际 `freeze_und` 必须与实现、optimizer 参数组和 checkpoint 一起核对。packed 的训练及评测 loss 路径与 KV-cache 生成路径同样不同，调用 `.eval()` 本身不会自动把 packed 输入改成生成接口。[2](#ref-2)[3](#ref-3)

## 数据与训练阶段

| 阶段 | 输入与监督 | 学习目标 | 需要保留的交接物 |
| --- | --- | --- | --- |
| 蛋白预训练 | UniRef 等序列、多序列 packing | 蛋白 token 的自回归 CE，建立序列分布先验 | tokenizer、边界布局、checkpoint、训练 token 账本 |
| 双向 CPT | P2T、T2P、protein-only；P1/P2/P3 等条件视图 | 生成方向与条件接口；按配方优化 text/protein CE | 方向标签、冻结策略、resolved data YAML、实际配比 |
| 科学 SFT | 蛋白及任务指令；分类、生成式分类和结构任务 | 任务输出行为与有监督的答案接口 | 监督区间、标签空间、split、目标头与解码 |
| 结构扩展 | 氨基酸序列与离散 structure token | sequence/structure 建模、正折叠与逆折叠 | codec 版本、有效残基、配对和结构质量筛查 |

阶段总结依据统一报告与仓库入口；不同实验分支不必顺序执行表中所有阶段。科学 SFT 的计划稿、参考论文设想和已实现分类路径应分别呈现，结构路线也不能由“存在 codec”推断全部端到端实验已完成。[1](#ref-1)[2](#ref-2)

一个 T2P 样本可以将文本条件放在上下文中，以蛋白 token 为主要预测目标；对应 P2T 视图从序列预测描述。双向样本的“配对正确”必须由 accession、序列和清洗规则确认。训练与 C30/Temporal 评测还需要在聚类、来源比例和视图构造上避免泄漏；精确序列不重复并不充分保证同源分布隔离。[1](#ref-1)

### 一个样本怎样从输入走到 loss
<p class="math-notation">监督式中 \(S\) 为有效目标位置集合，\(|S|\) 为位置数，\(y_i,c_i\) 为第 \(i\) 位目标/条件历史，\(\mathcal L_S\) 为平均 NLL。预算式的 \(C,M,D\) 分别为总 FLOPs、每 token FLOPs 和训练 token 数，\(M\) 与 Attention mask 的 \(M\) 含义不同。</p>

下面是布局讲解，模态标记为描述性占位符，不是仓库 tokenizer 的字面 special token：

```text
T2P: [方向/边界] [功能文本] [蛋白起始] [序列 tokens] [终止]
     └──────── 条件区 ────────┘ └── 主要监督区 ──┘
P2T: [方向/边界] [序列 tokens] [文本起始] [功能文本] [终止]
     └──────── 条件区 ────────┘ └── 主要监督区 ──┘
```

组装顺序是配对 → tokenizer → 方向/边界 → packing → 模态索引与 label shift → CE。对监督位置集合 S：

<div class="reading-math">\[
\mathcal L_S=-\frac{1}{|S|}
\sum_{i\in S}\log p_\theta(y_i\mid c_i)
\]</div>

若分别平均 text/protein CE 再加权，两类目标的贡献可能与全 token 平均不同。例如文本监督 10 tokens、蛋白监督 100 tokens：各模态等权时，两个平均 loss 各占一半；全 token 平均时，文本只占 10/110。**输入比例、监督比例、loss 权重分别核对。**[1](#ref-1)[4](#ref-4)

## 从目标 token 比例到可执行采样

canonical mixed CPT 声明 `P2T:T2P:protein-only = 1:1:98`。这是目标 token 暴露比例。`PackedDataset` 在记录级选择数据组，再按实际输入长度 packing，因此记录采样权重需要考虑有效样本率和每条样本的 token 产出。[2](#ref-2)[4](#ref-4)

令有效率为 a、有效记录均长为 μ、目标份额为 s；单次 fetch 的有效产出为 e。记录采样概率 w 所产生的 token 份额为：

<div class="reading-math">\[
\begin{aligned}
e_i&=a_i\mu_i\\
\widehat s_i&=\frac{w_ie_i}{\sum_jw_je_j}\\
w_i&=\frac{s_i/e_i}{\sum_js_j/e_j}\\
w_i'&\propto w_i\frac{s_i}{\widehat s_i}
\end{aligned}
\]</div>

最后一行是反馈校准后重新归一化；未观测到某流时先查分片、拒收与抽样，不能除以零。若两流均长为 600/300、目标各半，记录权重应为 1/3 与 2/3；直接各半抽样会产生 2/3 与 1/3 的 token 暴露。

可复现的数据配比包含三层：声明比例的 source YAML、可执行 `weight` 的 resolved YAML、跨 rank 汇总的 `token_mix_observed.json`。零 token 和过长样本被拒绝时会重新抽组，所以它们必须进入产出率估计。序列–结构路线还应区分 `packed_input_tokens` 与真正进入蛋白 CE 的 `supervised_prot_tokens`。[4](#ref-4)

这条方法路线的实际贡献是把“配方比例”变成可测量、可修正的暴露量。若比较 8:0:92 与 4:4:92，应同时审查实际 token share、重复暴露和有效数据来源，而不是只比较 YAML 中三个数字。

## Scaling 与优化怎样迁移到 CPT

### 固定算力时，模型该多大、数据该喂多少？

把总预算记作 **C**，每个输入 token 的训练计算量记作 **M**，累计输入 token 数记作 **D**。在同一预算下，按照图中各自的 FLOPs 口径，有 **D ≈ C/M**。沿左图一条同色曲线向右走，就是把更多算力花在每个 token 上，同时减少能训练的 token 数。纵轴是验证交叉熵，越低越好。圆点是训练端点，曲线是预算内的二次拟合，星号是拟合最低点，可以落在两个实测配置之间。

<figure><a href="protein-isoflop.png"><img src="protein-isoflop.png" alt="氨基酸序列的八档算力预算。左图各预算的验证交叉熵呈谷形，右图拟合最优模型计算量与数据量。" style="max-width:100%;height:auto"></a><figcaption>蛋白序列，原图 Figure 2。左图 M 按非 embedding FLOPs/token 计。右图蓝点取各星号的横坐标 M，红点由 D ≈ C/M 得到。八档预算中的拟合为 Mₒₚₜ ≈ 0.0755 C^0.533，Dₒₚₜ ≈ 13.2 C^0.467。</figcaption></figure>

以蛋白序列图为例，预算增加 10 倍时，拟合给出的每 token 计算量增加约 **3.41 倍**，训练 token 数增加约 **2.93 倍**。两者相乘约为 10。蓝线的斜率描述每 token 计算量随预算变化的速度，换成具体参数量还需要所选架构的 FLOPs 公式。

<figure><a href="structure-isoflop.png"><img src="structure-isoflop.png" alt="AFDB-24M 离散结构 token 的七档预算。右图最优 token 数随预算增长的斜率高于每 token 计算量。" style="max-width:100%;height:auto"></a><figcaption>AFDB-24M 结构 token，原图 Figure 5。左图圆点是各配置最终 checkpoint 的验证交叉熵。七档预算给出 Mₒₚₜ ≈ 5.5023 C^0.4550，Dₒₚₜ ≈ 0.18174 C^0.5450；D 按累计输入 token 计。</figcaption></figure>

同样把预算增加 10 倍，结构图给出的分配约为 **2.85 倍每 token 计算量、3.51 倍输入 token 数**。两组实验的指数反映各自数据、目标词表和观测预算内的趋势。跨图可比较算力分配随预算变化的方向；验证交叉熵衡量的是各自词表上的预测任务，绝对值不宜横向排名。

仓库用 iso-FLOPs 实验研究模型规模、训练数据、batch 和学习率，并保留 Muon / AdamW、冻结与全参训练、ZeRO 和 checkpoint 的工程记录。预算迁移需要按当前激活的模型路径重新计算每 token FLOPs，再由算力预算解析训练 token 数。总参数与 active 参数是两个量，不能直接互换。[1](#ref-1)[5](#ref-5)

当前 C1e20 Muon v3 profile：active 参数 **440,401,920**，每 token **2,837,839,872 FLOPs**，global batch **479,232 tokens**。[2](#ref-2)[5](#ref-5)

<div class="reading-math">\[
\begin{aligned}
D&\simeq C/M\\
&=10^{20}/2.83784{\times}10^9\\
&\simeq35.2{\times}10^9\ \text{tokens}
\end{aligned}
\]</div>

这是特定 decoder path 的预算。总参数不能代替 active path 的计算量；历史有效长度 284 仍需由 packed telemetry 校准。

## 如何证明模型使用了文本条件

单看 protein loss 或某个 fitness 分数无法确认模型在利用文本。统一报告将几种证据分开：[1](#ref-1)

- **序列能力**：无文本条件的 CE/NLL、ProteinGym 等 rank correlation，描述蛋白分布适应。
- **条件利用**：正确文本、错配文本、空条件和不同描述层级之间的对照，检查配对敏感性。
- **泛化范围**：C30、Temporal、OOD-safe 等 split 与来源审计，约束可解释的人群。
- **结构与科学输出**：结构任务、生成与编辑评测、分类任务，分别采用相应目标和指标。

Negative Ladder v2 的注册终点是两 checkpoint 从 L0 到 L3 的变化之差；结果在下面算例中展开。**PS8 的绝对 margin 更高，PSC 的下降较小**，两者回答不同问题。[6](#ref-6)

每种 recipe 只有一个训练 seed，实际 token share 尚无独立审计，expanded pool 也不是 strict protein-OOD。因此支持的是冻结样本上的 checkpoint-level 结论，不支持配方因果效应、多种子稳健性或细粒度生物学理解。完整报告保留这个边界与未执行的 replication 设计。[6](#ref-6)

<!-- WORK:EXAMPLE:START -->
### 用真实结果解释交互效应 {#work-example}
<p class="math-notation">\(c\) 索引 checkpoint 配方，\(m_{c,L0/L3}\) 是该配方在两种条件阶梯上的 margin NLL；\(\Delta_c\) 是阶梯差，DiD 是 PSC 与 PS8 两个差的差，单位仍为 NLL。这里 \(m\) 表示指标值，与训练的监督 mask 不同。</p>

Negative Ladder 的 margin 是 **mismatch NLL − matched NLL**；null 条件用于进一步分解信息增益与干扰，不是 margin 的另一端。正 margin 表示该协议下更偏好正确配对，不是生物功能正确率。[6](#ref-6)

| Checkpoint | L0 margin NLL | L3 margin NLL | L3−L0 |
| --- | ---: | ---: | ---: |
| PS8，8:0:92 | 0.0981195 | 0.0871261 | −0.0109934 |
| PSC，4:4:92 | 0.0380793 | 0.0322274 | −0.0058518 |

<div class="reading-math">\[
\begin{aligned}
\Delta_c&=m_{c,L3}-m_{c,L0}\\
\mathrm{DiD}&=\Delta_{\rm PSC}-\Delta_{\rm PS8}\\
&=-0.0058518-(-0.0109934)\\
&=+0.0051416\ \mathrm{NLL}
\end{aligned}
\]</div>

95% CI **[0.0037273, 0.0066557]** 来自 union-component block bootstrap。它覆盖冻结样本的相关性，不覆盖重新训练 seed 的变化；每配方单 seed、token share 未独立审计、expanded pool 非 strict protein-OOD 的边界继续保留。

**复算精度：**表中的端点已经舍入，直接计算 PSC 的 `0.0322274−0.0380793` 得 −0.0058519，再与 PS8 的差相减得 +0.0051415；上式保留原逐样本完整精度聚合的 −0.0058518 与 +0.0051416。不能用显示表的七位小数重建原 bootstrap 或据此判断结果矛盾；独立重算 CI 还需要逐 anchor 结果、依赖组件划分和重采样配置。[6](#ref-6)
<!-- WORK:EXAMPLE:END -->

<!-- WORK:REVIEW:START -->
## 工作总结与尚未闭合的研究问题 {#work-review}

| 工作产物 | 已能说明什么 | 下一步要补什么 |
| --- | --- | --- |
| 模态路由与训练/推理接口 | 有可定位的实现、索引与参数分工 | 同数据预算 dense/MoT 消融，冻结与缓存一致性 |
| 混合 CPT 配方及校准工具 | 声明比例能转换为记录采样并观测暴露 | 实际监督暴露、重复率及跨 rank 汇总审计 |
| Scaling → CPT 预算映射 | 特定 active path 的算力可换算成训练 tokens | 用当前 telemetry 校准 FLOPs 与有效步数 |
| Negative Ladder 与分层评测 | 可区分配对敏感性、绝对分数和 tier 交互 | 新训练 seed、strict protein-OOD 与独立生物评审 |

由此可提炼的研究贡献是统一表示接口、可测量的数据配方和有边界的条件利用评测。SFT 与结构路线的完整实验闭合仍要逐条看台账，不能把计划、实现和实测合并成一个“全部完成”的结论。

## 按需补充基础知识

建议先复习 [Attention 与 KV cache](../../llm-architecture/s02_attention_position_cache.html)，再读 [SFT 与监督 mask](../../llm-posttraining/s01_supervision_preference.html)；训练资源问题可接着看 [优化器与训练系统](../../llm-training-lifecycle/s05_training_methods_systems.html)。这些是通用知识讲解，本页的项目事实仍以固定版本来源为准。
<!-- WORK:REVIEW:END -->

## 五道项目面试追问

1. **MoT 与 MoE 的区别？** MoT 按模态/任务位置选参数；MoE 通常由学习 router 选专家。参数分工不取消样本内跨模态 attention。
2. **1:1:98 为什么不能直接作记录权重？** 不同流每次 fetch 的有效 token 产出不同；按目标份额除以有效产出，再归一化。
3. **protein loss 下降能证明理解文本吗？** 不能；用 matched/null/mismatch、SeqOnly 和独立 split 区分先验、条件收益及干扰。
4. **PSC 的 DiD 为正为何绝对 margin 更低？** DiD 比较下降幅度，绝对 margin 比较端点；两个量可以给出不同排序。
5. **结构 codec 重建更好，fold 模型一定更好吗？** 不一定；几何重建与 token 可学习性分轴验收。完整报告保留五臂实验与非劣门限。

## 实现入口与复核范围

阅读源码可按 `modeling/holon/ → data/ → train/ → eval/` 顺序：先确认参数路由，再确认输入、loss mask、实际 sampling，最后确认 checkpoint 与 scorer 的布局是否一致。长代码、完整实验总表、结构路线和 ProtText-Eval 的细节在[完整报告](full-report.html)中保留。

本页复核范围是项目定位、MoT 投影路由、token-mixture 校准、当前 CPT 预算与 Negative Ladder 结论解释。没有在本次整理中重新运行训练或对全部实验表独立复算。

## 来源与固定版本

所有仓库链接固定到 `7de0f4d67f9d18d166e715f6e4e200de22cb21ea`，需要私有仓库访问权限。

1. <a id="ref-1" href="https://github.com/stein-wang0226/Holon/blob/7de0f4d67f9d18d166e715f6e4e200de22cb21ea/docs/reports/Holon_Unified_Report_202611.html">统一研究报告</a>：2026-11-11 深入研究版。
2. <a id="ref-2" href="https://github.com/stein-wang0226/Holon/blob/7de0f4d67f9d18d166e715f6e4e200de22cb21ea/README.md">README：模型、配置与训练入口</a>。
3. <a id="ref-3" href="https://github.com/stein-wang0226/Holon/blob/7de0f4d67f9d18d166e715f6e4e200de22cb21ea/modeling/holon/qwen3_navit.py#L294-L360">qwen3_navit.py</a>：模态索引与投影装配。
4. <a id="ref-4" href="https://github.com/stein-wang0226/Holon/blob/7de0f4d67f9d18d166e715f6e4e200de22cb21ea/docs/data/token_mix_calibration.md">CPT token mixture calibration</a>：比例、产出率、实测与反馈。
5. <a id="ref-5" href="https://github.com/stein-wang0226/Holon/blob/7de0f4d67f9d18d166e715f6e4e200de22cb21ea/docs/scaling/cpt_scaling_transfer.md">Scaling → CPT transfer</a>：active FLOPs 与预算。
6. <a id="ref-6" href="https://github.com/stein-wang0226/Holon/blob/7de0f4d67f9d18d166e715f6e4e200de22cb21ea/docs/benchmark/PROTEIN_TEXT_NEGATIVE_LADDER_V2_PS8_PSC_RESULT.md">Negative Ladder PS8→PSC 结果</a>：注册终点、CI 与 claim scope。
