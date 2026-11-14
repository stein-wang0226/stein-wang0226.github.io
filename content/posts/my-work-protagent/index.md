---
title: ProtAgent：蛋白工具智能体与逐步强化学习
---

<p><a href="../">My Work 目录</a> · <a href="full-report.html">完整技术报告：奖励、实验与配置</a> · <a href="https://arxiv.org/abs/2610.33746">论文</a></p>

## 研究问题与方法路线

ProtAgent 研究紧凑蛋白领域智能体能否学习调用真实生物信息工具，并把观察整合成任务答案。主要变量是工具交互的步骤级信用分配：SFT 学习工具调用和输出接口，在线 RL 优化工具选择、停止与证据整合，最后以冻结 checkpoint 在固定评测协议下比较。[1](#ref-1)[2](#ref-2)

```text
protein + question + skill policy
  → real tool call → observation → next action / final answer
  → trajectory admission + task audit
  → assistant-only SFT
  → on-policy rollout + step return + actor update
  → frozen-checkpoint evaluation
```

项目负责领域数据、工具、skills、reward 与评分；ROLL 承担分布式训练与 rollout 运行时。真实工具观察、teacher 示范和 gold annotation 是不同资产，不能让模型生成的“工具样文本”替代程序执行。[2](#ref-2)

## 工具、轨迹和监督怎样组织

输入通常含 `sample_id`、`instruction`、`sequence`、任务类型和 metadata。策略根据历史 `h_t=(x,q,a_1,o_1,…,a_{t−1},o_{t−1})` 输出动作，环境执行对应工具并返回观察。skill policy 约束可见工具、必要证据、答案形状和不应出现的注释部分。[1](#ref-1)[2](#ref-2)

| 任务 | 工具或证据重点 | 主要合同 |
| --- | --- | --- |
| enzyme | EC 预测、序列同源与功能证据 | 催化功能和反应描述有来源 |
| domain | Pfam/HMMER 等结构域信息 | 家族、坐标与结构域架构一致 |
| GO/IPR | QuickGO 等注释核验 | 对提出的条目逐项验证 |
| signal | SignalP | presence/type/cleavage/confidence/group 五项 |
| disorder | DisProt、序列与无序预测证据 | 区间坐标及真实证据覆盖 |

表中概括领域合同，不表示论文每个样本使用全部工具。可注册工具、启发式 fallback 和论文 actual-tool 实验有不同证据等级。程序、权重与数据库版本都属于可复现单元；训练与测试序列隔离不能证明工具数据库中不存在测试蛋白或其同源项。[1](#ref-1)

论文闭环 SFT 使用 987 train / 64 val，训练部分包括 567 action、120 evidence-to-answer 和 300 multi-turn 示例。系统、用户和工具消息作为上下文，只有 assistant 的动作与最终回答进入预测目标：

```text
L_SFT = − Σ_(u in assistant tokens) log πθ(y_u | context, y_<u)
```

这要求 tokenizer、chat template、loss mask 和 next-token label shift 对齐。论文配方为 Qwen3-8B-Instruct、1 epoch、LR `1e−6`、cosine、weight decay `0.01`、长度 8192、bf16；Megatron 使用 TP2/PP2/CP2。局部 batch 和梯度累积为 1×1，不能据此猜测全局 batch。[1](#ref-1)[3](#ref-3)

## 逐步回报怎样进入策略梯度

每个 prompt 采样 K=4 条 on-policy 轨迹。相关工具首次成功、重复调用、格式错误、截断和终止答案分别产生局部奖励。主方法是无 critic 的 REINFORCE，按同一轨迹从后向前累加：[1](#ref-1)[3](#ref-3)

```text
G_t = r_t + γ G_(t+1)                 # 主配方 γ=1
L = − E[A_(t,u) log πθ(y_(t,u)|h_(t,u))] + β KL(πθ || πref)
```

源码先按 `traj_id` 分组并按 step 排序，计算 `r_t + gamma × step_lambd × running_return`，随后恢复原样本顺序。主配方 step λ=1；支持 λ 分支不代表主实验使用了所有扩展。return 经配置选择的 normalization 进入 response/token 奖励与 mask，再做 advantage whitening 和 clipping。[4](#ref-4)

identity return normalization 只表示该层不做组相对变换。后续仍可 whiten 优势并裁剪到 ±0.2；这里的 advantage clip 与 PPO 的概率比 clip 不是一回事。episode 方法把整条轨迹的 return 赋给各动作，step 方法保留当前位置之后的回报，因此不会让后续重复动作继承此前已获得的局部奖励。

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

复現需绑定模型、数据 split、工具数据库、代码/patch、prompt、模板、解码、checkpoint 和 scorer。补充包不含完整模型权重、全部原始 rollout 与大型工具数据库；“代码能 smoke”不能证明全部主表已经重现。reward hygiene 的旧 on/off 实验也不能与后来的四臂重跑直接求差。[1](#ref-1)[5](#ref-5)

本次对照了报告、论文附录、return 实现和当前状态文件，未重新运行训练或 OOD 评测。优先扩展方向是固定输出的独立生物专家与证据蕴含评审，以及固定起点、预算的跨模型/工具机制实验。

## 来源与固定版本

仓库固定到 `d66fa7c287d196d5c26ec23e53c02327c5bbc6a8`，源码访问需要权限。

1. <span id="ref-1"></span>[完整技术报告](https://github.com/stein-wang0226/ProtAgent/blob/d66fa7c287d196d5c26ec23e53c02327c5bbc6a8/docs/assets/reports/ProtAgent_Technical_Report_202611.html)。
2. <span id="ref-2"></span>[README 与领域运行链](https://github.com/stein-wang0226/ProtAgent/blob/d66fa7c287d196d5c26ec23e53c02327c5bbc6a8/README.md)。
3. <span id="ref-3"></span>[arXiv 稿件附录](https://github.com/stein-wang0226/ProtAgent/blob/d66fa7c287d196d5c26ec23e53c02327c5bbc6a8/docs/paper/arxiv2026/appendix.tex)：四臂、阶段、参数与分母。
4. <span id="ref-4"></span>[ROLL agentic/utils.py](https://github.com/stein-wang0226/ProtAgent/blob/d66fa7c287d196d5c26ec23e53c02327c5bbc6a8/supplementary/code_data/third_party/roll/roll/pipeline/agentic/utils.py#L62-L108)：按轨迹累积 return；L467–541 优势处理。
5. <span id="ref-5"></span>[训练状态](https://github.com/stein-wang0226/ProtAgent/blob/d66fa7c287d196d5c26ec23e53c02327c5bbc6a8/docs/plans/TRAINING_PIPELINE_STATUS.md)与[论文证据矩阵](https://github.com/stein-wang0226/ProtAgent/blob/d66fa7c287d196d5c26ec23e53c02327c5bbc6a8/docs/paper/PAPER_EVIDENCE_MATRIX.md)：历史与当前证据区分。
