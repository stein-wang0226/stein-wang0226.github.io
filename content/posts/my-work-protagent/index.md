---
title: ProtAgent：蛋白工具智能体与逐步强化学习
---

<p><a href="../">My Work 目录</a> · <a href="full-report.html">完整技术报告：奖励、实验与配置</a> · <a href="https://arxiv.org/abs/2610.33746">论文</a></p>

## 先记住：真实工具、逐步信用、独立评价

ProtAgent 研究紧凑蛋白领域智能体能否学习调用真实生物信息工具，并把观察整合成任务答案。主要变量是工具交互的步骤级信用分配：SFT 学习工具调用和输出接口，在线 RL 优化工具选择、停止与证据整合，最后以冻结 checkpoint 在固定评测协议下比较。[1](#ref-1)[2](#ref-2)

**训练链：真实工具轨迹 → assistant-only SFT → 当前策略 rollout → step return → actor 更新 → 冻结评测。** 下图展示工具交互与反馈的附着位置。

项目负责领域数据、工具、skills、reward 与评分；ROLL 承担分布式训练与 rollout 运行时。真实工具观察、teacher 示范和 gold annotation 是不同资产，不能让模型生成的“工具样文本”替代程序执行。[2](#ref-2)

<!-- WORK:KNOWLEDGE:START -->
## 知识讲解：工具轨迹、SFT 与在线 RL {#work-knowledge}

**工具智能体** 的一个动作可以包含多个文本 token；程序执行结束后产生的 observation 是环境返回值。训练序列里出现工具名并不等于真实调用成功。**SFT** 使模型模仿已收集的有效动作和答案；**on-policy RL** 则用当前模型重新采样轨迹，比较其实际结果并更新策略。这两者的数据分布和优化目标不同。

这里没有学习 value critic 的主方法使用 REINFORCE。它通过“奖励高的已采样动作提高概率、奖励低的降低概率”优化期望回报；baseline、normalization、whitening 和 KL 用来控制更新，但不能为缺失的生物事实提供真值。**信用分配** 问的是一次成功或失败应影响哪些早先动作。[1](#ref-1)

<figure class="work-mechanism">
<svg viewBox="0 0 840 200" role="img" aria-labelledby="protagent-loop-title protagent-loop-desc" xmlns="http://www.w3.org/2000/svg">
<title id="protagent-loop-title">ProtAgent 的真实工具闭环与训练信号</title><desc id="protagent-loop-desc">策略产生动作，工具执行返回观察，观察加入历史；局部动作奖励和终止答案奖励组成逐步回报用于更新策略。</desc>
<g fill="#f7f5f0" stroke="#a9cec7"><rect x="5" y="15" width="175" height="65" rx="6"/><rect x="225" y="15" width="175" height="65" rx="6"/><rect x="445" y="15" width="175" height="65" rx="6"/><rect x="665" y="15" width="170" height="65" rx="6"/><rect x="225" y="130" width="395" height="55" rx="6"/></g>
<g stroke="#0f766e" stroke-width="2" fill="none"><path d="M180 48H225M400 48H445M620 48H665M750 80V105H92V80M312 80V130M750 105V157H620"/></g>
<g fill="#172d35" text-anchor="middle" font-family="system-ui,sans-serif" font-size="17"><text x="92" y="43">策略与历史</text><text x="92" y="65" font-size="13">蛋白、问题、观察</text><text x="312" y="43">assistant 动作</text><text x="312" y="65" font-size="13">有效调用或最终答案</text><text x="532" y="43">真实工具执行</text><text x="532" y="65" font-size="13">结果、失败与版本</text><text x="750" y="43">新 observation</text><text x="750" y="65" font-size="13">返回历史继续决策</text><text x="422" y="165">局部 reward → 逐步 return → actor 更新</text></g>
</svg>
<figcaption>动作和最终答案是策略输出；工具观察作为条件进入下一步，不能对其做 assistant 模仿监督。<a href="#ref-1">1</a><a href="#ref-3">3</a></figcaption>
</figure>
<!-- WORK:KNOWLEDGE:END -->

## 工具、轨迹和监督怎样组织

输入含 `sample_id`、instruction、sequence、任务类型与 metadata。历史由初始输入、已执行动作和真实观察组成；skill policy 约束可见工具、必要证据及答案形状。[1](#ref-1)[2](#ref-2)

<div class="reading-math">\[
\begin{aligned}
h_t&=(x,q,a_1,o_1,\ldots,a_{t-1},o_{t-1})\\
a_t&\sim\pi_\theta(\cdot\mid h_t)
\end{aligned}
\]</div>

| 任务 | 工具或证据重点 | 主要合同 |
| --- | --- | --- |
| enzyme | EC 预测、序列同源与功能证据 | 催化功能和反应描述有来源 |
| domain | Pfam/HMMER 等结构域信息 | 家族、坐标与结构域架构一致 |
| GO/IPR | QuickGO 等注释核验 | 对提出的条目逐项验证 |
| signal | SignalP | presence/type/cleavage/confidence/group 五项 |
| disorder | DisProt、序列与无序预测证据 | 区间坐标及真实证据覆盖 |

表中概括领域合同，不表示论文每个样本使用全部工具。可注册工具、启发式 fallback 和论文 actual-tool 实验有不同证据等级。程序、权重与数据库版本都属于可复现单元；训练与测试序列隔离不能证明工具数据库中不存在测试蛋白或其同源项。[1](#ref-1)

论文闭环 SFT 使用 987 train / 64 val，训练部分包括 567 action、120 evidence-to-answer 和 300 multi-turn 示例。系统、用户和工具消息作为上下文，只有 assistant 的动作与最终回答进入预测目标：

<div class="reading-math">\[
\mathcal L_{\rm SFT}
=-\sum_{u\in S_{\rm assistant}}
\log\pi_\theta(y_u\mid c,y_{\lt u})
\]</div>

这要求 tokenizer、chat template、loss mask 和 next-token label shift 对齐。论文配方为 Qwen3-8B-Instruct、1 epoch、LR `1e−6`、cosine、weight decay `0.01`、长度 8192、bf16；Megatron 使用 TP2/PP2/CP2。局部 batch 和梯度累积为 1×1，不能据此猜测全局 batch。[1](#ref-1)[3](#ref-3)

## 逐步回报怎样进入策略梯度

每个 prompt 采样 K=4 条 on-policy 轨迹。相关工具首次成功、重复调用、格式错误、截断和终止答案分别产生局部奖励。主方法是无 critic 的 REINFORCE，按同一轨迹从后向前累加：[1](#ref-1)[3](#ref-3)

<div class="reading-math">\[
\begin{aligned}
G_t&=r_t+\gamma G_{t+1},\quad G_{H+1}=0\\
\gamma&=1\quad\text{（主配方）}
\end{aligned}
\]</div>

源码先按 `traj_id` 分组并按 step 排序，计算 `r_t + gamma × step_lambd × running_return`，随后恢复原样本顺序。主配方 step λ=1；支持 λ 分支不代表主实验使用了所有扩展。return 经配置选择的 normalization 进入 response/token 奖励与 mask，再做 advantage whitening 和 clipping。[4](#ref-4)

identity return normalization 只表示该层不做组相对变换。后续仍可 whiten 优势并裁剪到 ±0.2；这里的 advantage clip 与 PPO 的概率比 clip 不是一回事。episode 方法把整条轨迹的 return 赋给各动作，step 方法保留当前位置之后的回报，因此不会让后续重复动作继承此前已获得的局部奖励。

<!-- WORK:EXAMPLE:START -->
### 一个有重复调用的轨迹怎样计算信用 {#work-example}

用论文附录的实际局部权重作算式示例；以下是教学轨迹，不是新增 rollout 实测。第一次正确相关工具调用得 `+0.25`，下一次重复调用得 `−0.30`，第三步回答的终止奖励记为 R，γ=λ=1。[3](#ref-3)

| 动作 | 局部 reward | Step return | 同轨迹 Episode return |
| --- | --- | --- | --- |
| 首次有效相关调用 | +0.25 | R−0.05 | R−0.05 |
| 重复调用 | −0.30 | R−0.30 | R−0.05 |
| 最终答案 | R | R | R−0.05 |

Step return 不再把第一步的 `+0.25` 分给第二步；它仍保留终止答案对早先证据采集动作的影响。真实更新还经过 normalization、token/response mask 和 clipping，因此该表解释的是原始 return，不能直接当成最终 advantage。

无 critic 的 REINFORCE 用 score-function 估计；完整轨迹目标的恒等式与实际局部 surrogate 要分开：

<div class="reading-math">\[
\begin{aligned}
\nabla_\theta\mathbb E_{\tau\sim\pi_\theta}[R(\tau)]
&=\mathbb E[R(\tau)\nabla_\theta\log p_\theta(\tau)]\\
\log p_\theta(\tau)
&=\sum_{t,u\in\text{policy}}\log\pi_\theta(y_{t,u}\mid h_{t,u})\\
L_{\rm pg}
&=-\frac{\sum_{t,u}m_{t,u}A_{t,u}
\log\pi_\theta(y_{t,u}\mid h_{t,u})}{Z}\\
L_{\rm actor}&=L_{\rm pg}
+\beta D_{\rm KL}(\pi_\theta\Vert\pi_{\rm ref})
\end{aligned}
\]</div>

环境转移不依赖策略参数时，工具观察不贡献动作 log probability，但影响后续动作条件。Z 是实现的 reduction 分母；advantage 处理后的 surrogate 不应被宣称为未经变换的无偏梯度。

mask 排除非策略与 padding token；**token mean 与 trajectory mean 不等价**。组相对 return 先减组均值、再除组标准差；组和统计轴以配置为准。Identity 后仍可 whitening；**优势裁剪 ±0.2、概率比 clip、KL anchor 控制不同对象**。[4](#ref-4)
<!-- WORK:EXAMPLE:END -->

### Reward 的正确性为什么仍需要独立评价

终止 reward 包括注释覆盖、工具覆盖、格式、效率与 same-rollout fidelity 等项。论文中的完成工具 guard `−0.45×1[m=0]` 用于抵消纯 schema 增量：`0.45=2×0.15+0.5×0.30`。首次相关调用、重复/无关/malformed 调用及截断在不同 attachment point 计分，不能把终止 reward 复制到每一个原始动作上。[3](#ref-3)

Same-rollout fidelity 检查回答与该次工具结果是否一致；它不能证明工具数据库是真实无误、测试信息未进入数据库，或答案已得到独立生物专家认可。训练优化“可获得的反馈”，评价则需要独立定义目标和分母。

工具与答案 reward 是训练信号。最终评测从 `<answer>` 提取文本，以参考 annotation token recall **严格大于 0.5** 判成功，不能用含格式 bonus 的训练 reward 直接替代评测成功率。[1](#ref-1)[3](#ref-3)

## 四臂实验说明了什么

四臂共享起点、问题、采样计划、seed、环境、reward、预算和评测集，on-policy 轨迹由各 arm 独立生成。回报粒度和 return normalization 是两个比较因素。[1](#ref-1)[3](#ref-3)

| 回报粒度 | Identity | Group-relative |
| --- | --- | --- |
| Step | REINFORCE：61.40 ± 2.10% | Step GRPO：58.20 ± 1.70% |
| Episode | REINFORCE：42.70 ± 1.60% | Episode GRPO：36.50 ± 1.70% |

表中为 seeds 42/43/44 的 OOD-1000 均值与样本 SD。step 相对 episode 在两种 normalization 下高 18.70 / 21.70 个百分点，支持该训练设置下的步骤级信用分配。它不是所有工具任务都必然受益的定理，也不能证明每个 reward 组件的因果贡献。[3](#ref-3)

本项目的 Step GRPO 指组相对逐步 return 与 vanilla policy gradient 的组合，应连同实际实现阅读；不能仅凭名称与任意框架的 episode GRPO 等同。完整报告保留逐 seed 表、局部 γ/λ 消融和阈值敏感性。

## 主模型结果与独立协议

| 模型或条件 | OOD-1000 全样本成功率 | 解释 |
| --- | --- | --- |
| Qwen3-8B base | 14.10% | 未做本项目后训练 |
| SFT | 40.20% | 工具轨迹监督 |
| Full，指定 checkpoint | 61.00% | 主表闭环模型 |
| 同一 Full checkpoint，禁用工具 | 25.50% | 工具观察可用性对照 |

分母固定为 1000；未回答或不可解析样本计失败。full 的 61.00% 是指定模型结果，不能写成四臂表的 61.40% 三种子均值。这个指标反映注释 token 覆盖，不直接测量生物学正确性或证据蕴含。[1](#ref-1)[3](#ref-3)

API 主表行温度为 0、本地 Qwen3 为 1.0；相同工具和 prompt 不代表完全相同的解码控制。Signal 子任务从 SFT 78.50% 降到 full 73.50%，说明总指标改善并不保证每一类别改善。[3](#ref-3)

PFUA 使用独立 Swiss-Prot 数据、reward、checkpoint 和 ROUGE recall。其 60.15 / 41.62 是 ROUGE-1 / ROUGE-L 百分数，与闭环 61.00% 不可合并。README 中 780→631 候选、567/64 SFT split 和超低 smoke loss 属于历史开发链，不应当作论文当前主训练配置；当前训练状态与论文 evidence matrix 另有明确版本区分。[1](#ref-1)[2](#ref-2)[5](#ref-5)

## 训练系统与复现边界

SFT 使用 Megatron；论文 RL actor 使用 FSDP2，rollout 使用 vLLM 并同步 actor 权重。三阶段各 50 updates，学习率 `5e−7 → 5e−8 → 5e−8`，每阶段继承模型权重、重置 optimizer 并更新 reference anchor；并非一个 optimizer state 连续训练 150 步。[1](#ref-1)[3](#ref-3)

复现绑定模型、split、工具数据库、代码/patch、prompt、模板、解码、checkpoint 与 scorer。补充包缺完整权重、原始 rollout 与大数据库；smoke 只证明有限路径运行。旧 reward on/off 与四臂重跑的条件不同，不能直接求因果差。[1](#ref-1)[5](#ref-5)

本次对照了报告、论文附录、return 实现和当前状态文件，未重新运行训练或 OOD 评测。优先扩展方向是固定输出的独立生物专家与证据蕴含评审，以及固定起点、预算的跨模型/工具机制实验。

<!-- WORK:REVIEW:START -->
## 工作总结与复现检查顺序 {#work-review}

| 产物 | 方法价值 | 尚不能推出的结论 |
| --- | --- | --- |
| 有效工具轨迹与 assistant-only SFT | 模型学会执行接口及观察到答案的转化 | 所有工具数据库都与测试同源隔离 |
| Step return 与四臂三种子对照 | 区分回报粒度与 normalization 的影响 | 单个 reward 项的因果贡献 |
| 全样本 OOD-1000 与禁用工具对照 | 指定协议中后训练和工具可用性相关的收益 | 生物学正确率或跨领域必然收益 |
| 阶段配置、checkpoint 与证据矩阵 | 划清论文配方和早期开发记录 | 完整权重、轨迹及大数据库已经公开齐全 |

复现先固定输入、模板和 loss mask，再检查真实工具执行及 `traj_id/step`，随后验证 return 附着位置、advantage 和 actor 权重同步，最后冻结 scorer 与模型。评价应同时报告答题率、全样本成功率、有效工具覆盖和独立证据正确性；只对已回答样本求成功率会掩盖拒答或解析失败。

## 按需补充基础知识

[SFT、RFT 与偏好优化](../../llm-posttraining/s01_supervision_preference.html)解释监督来源；[策略梯度与 RL 算法](../../llm-posttraining/s02_rl_algorithms.html)解释优化目标；[环境奖励与多步信用分配](../../llm-posttraining/s04_environment_reward_credit.html)和[异步后训练系统](../../llm-posttraining/s05_frameworks_async.html)分别连接 return 与分布式执行。
<!-- WORK:REVIEW:END -->

## 五道项目面试追问

1. **为什么不监督 observation？** 它是环境返回的条件；只监督 assistant 动作与答案，避免模型学会伪造工具输出。
2. **Step return 给重复调用什么信用？** 保留其局部负奖与后续终止奖，不继承此前首次调用的正奖；数值例还要经过优势处理。
3. **Identity 是否等于不归一化？** 只在 return 这一层保持原值，后续 masked whitening 与优势裁剪仍可启用。
4. **61.00 与 61.40 为什么都出现？** 前者是指定 checkpoint；后者是四臂主实验三 seed 均值，不能混为一个终点。
5. **成功率能否称作生物正确率？** 这里成功要求 annotation token recall 严格大于 0.5；独立证据蕴含、专家正确性另评。

## 来源与固定版本

仓库固定到 `d66fa7c287d196d5c26ec23e53c02327c5bbc6a8`，源码访问需要权限。

1. <a id="ref-1" href="https://github.com/stein-wang0226/ProtAgent/blob/d66fa7c287d196d5c26ec23e53c02327c5bbc6a8/docs/assets/reports/ProtAgent_Technical_Report_202611.html">完整技术报告</a>。
2. <a id="ref-2" href="https://github.com/stein-wang0226/ProtAgent/blob/d66fa7c287d196d5c26ec23e53c02327c5bbc6a8/README.md">README 与领域运行链</a>。
3. <a id="ref-3" href="https://github.com/stein-wang0226/ProtAgent/blob/d66fa7c287d196d5c26ec23e53c02327c5bbc6a8/docs/paper/arxiv2026/appendix.tex">arXiv 稿件附录</a>：四臂、阶段、参数与分母。
4. <a id="ref-4" href="https://github.com/stein-wang0226/ProtAgent/blob/d66fa7c287d196d5c26ec23e53c02327c5bbc6a8/supplementary/code_data/third_party/roll/roll/pipeline/agentic/utils.py#L62-L108">ROLL agentic/utils.py</a>：按轨迹累积 return；L467–541 优势处理。
5. <a id="ref-5" href="https://github.com/stein-wang0226/ProtAgent/blob/d66fa7c287d196d5c26ec23e53c02327c5bbc6a8/docs/plans/TRAINING_PIPELINE_STATUS.md">训练状态</a>与<a id="ref-5-matrix" href="https://github.com/stein-wang0226/ProtAgent/blob/d66fa7c287d196d5c26ec23e53c02327c5bbc6a8/docs/paper/PAPER_EVIDENCE_MATRIX.md">论文证据矩阵</a>：历史与当前证据区分。
