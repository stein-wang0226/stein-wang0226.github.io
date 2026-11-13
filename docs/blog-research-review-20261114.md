# 博客知识体系增补：2026-11-14 来源复核与编辑依据

调研截止：2026-11-14。范围：当前博客覆盖、公开基模架构、Agent 数据与评测、长程 Agent RL、推理与扩散模型，以及 GUI、科学 Agent 和持续学习。本文记录编辑依据；原论文结果均未在本地复现。

## 执行摘要

当前登记有 10 个公开本地笔记集合、18 个系列章节，另有独立子站和历史版本。训练全链路已覆盖 pretraining、CPT/midtraining、SFT/RFT、RL/OPD；Agentic RL、Harness、分布式训练、Transformer、扩散模型和 VLM 也已有基础材料。前沿滚动页已经记录 DeepSeek V4.1-Flash、1017、Kimi K3/K3.1 等版本。主要缺口是从快讯和算法名录走向可检查的机制、证据边界与实验对照。

建议形成“数据与评测 → 优化与信用分配 → 模型与推理成本 → 场景迁移”的专题链。最高优先级是 Agent 数据与 benchmark 的区别、Harbor 任务质量及迁移一致性、长程信用分配、异质数据、异步采样和 rollout–trainer 不一致。V4.1 的架构、Agent 数据生产和基础设施适合作为贯通案例；扩散 drafter 与 DSpark 连接已有 DLM 研究。GUI 和科学 Agent 应从面试题库中的子主题提升为正式专题，结合作者公开项目说明方法，但不加入未经授权公开的内部数据或数字。

这些优先级是基于当前覆盖及作者研究方向的编辑判断，不是论文验证过的“领域价值排序”。

## 当前覆盖与增补位置

| 现有材料 | 已覆盖 | 需要增补 | 优先级 |
|---|---|---|---|
| `llm-training-lifecycle` | 训练阶段、数据目标、工业配方、Harbor A–E 对照建议 | 与新数据、RL、架构专题交叉引用，不再重复整套训练链路 | P0 |
| `llm-frontier-2026` | 模型版本、Muon、架构信号、RL 和 OPD 快讯 | 接入专题；明确快讯标签不等于独立复现，保留自动插入标记 | P0 |
| `agent-harness-guide` | 工具、sandbox、reward、异步 rollout | 独立 verifier、artifact 合同、失败归因、adapter parity、计费去重 | P0 |
| `agentic-rl-guide` / RL 手册 | PPO/DPO/GRPO、GSPO/GiGPO/OPD | loss 的四个设计维度、RLDS/KnowGPO/SAMPO、同名 SAPO、异质数据与版本 lag | P0 |
| `transformer-decoder-flow` | dense decoder、RoPE、Attention、KV | CED/CSA2/FP4/SWA replay、KDA/LatentMoE、Engram 与 agent memory 的区别 | P1 |
| `distributed-training-guide` | 并行和训练框架 | prefill/decode、缓存和 IO、routing replay、异步训练有效样本率 | P1 |
| `dlm-survey` | 14 章扩散原理、解码、Scaling 和 RL | DFlash → DSpark → AdaFlash、精确验证条件、批量吞吐与单请求延迟 | P1 |
| VLM / 面试题库 | 编码器、对齐、Agent/RAG 题目 | GUI 长程恢复、OSWorld 2.0、科学 Agent、SkillsBench 1.1 与持续学习 | P1 |
| Muon / loop / 优化器快讯 | 概念与出处 | 独立公式和 kernel 消融专题；保持为后续选题，不宣称本次已完整完成 | P2 |

## 来源方法与证据分层

机器可读来源清单位于 `assets/research/2026-11-14/sources.json`，登记固定版本、原始标题、来源 URL、访问日期、使用位置、原论文许可，以及本地 PDF 的来源、字节数与 SHA-256。公开引用编号由该清单固定；不要把另一个训练系列的编号混用。

- 原论文定义、机制与作者报告结果：采用固定 arXiv 版本。
- 官方发布 / 模型卡 / benchmark 文档：记录访问口径；固定可用的仓库 revision。
- 同一团队的论文、博客和模型卡可以核对一致性，但不是三份独立实验。
- 数据合成方向由 DeepSeek V4.1、NexForge、EvoSyn 等不同团队相互支持；长程信用分配由 GiGPO、RLDS、KnowGPO 和 ARLArena 提供不同方法与限制；架构成本由 DeepSeek、Kimi、Nemotron 提供独立工业例子。
- “某算法普遍最好”“某架构一律更快”“自主持续学习已经产生复利”没有得到这些材料的支持。

## 关键事实与可引用位置

### Agent 数据、环境与 benchmark

1. [DeepSeek V4.1-Flash，2609.19969v1](https://arxiv.org/html/2609.19969v1)：§5.1 明言沿用 SFT → RL → OPD，不引入新后训练算法。主要投资在任务与环境生产；任务定义为 problem / environment / verification system，评估难度和正确性。§5.1.1 的 coding 流程包含可构建性筛选、起始 commit、fail-to-pass / pass-to-pass、隔离环境构建、移除泄漏、多 agent 试解、独立检查和修复。
2. [SWE-smith，2504.21798v1](https://arxiv.org/html/2504.21798v1)：仓库与测试驱动合成的软件任务。是历史基础，不把 2025 方法标成 2026 新发布。
3. [NexForge，2607.14186v6](https://arxiv.org/html/2607.14186v6)：从能力需求、真实场景和 task profile 出发，编译可执行任务并补齐文件、依赖和运行环境。§5 明确 TB2/GDPval 用于下游评测；引用外部 baseline 可能有不同 scaffold。报告的 headline 增益不能作为严格同 harness 算法比较。
4. [EvoSyn，2610.12593v1](https://arxiv.org/html/2610.12593v1)：§4 区分在已有合成空间内重新分配预算，以及扩展新的可控交互因素。Designer、Planner、Generator、Verifier、Reflector 将学习反馈转成合成决策。13.3 points 为作者在 τ²/CAR-Bench 中的报告，本次不迁移为 Harbor 的预期收益。
5. [ProgramGym，2610.13395v1](https://arxiv.org/html/2610.13395v1)：Program-Env 与 Program-Agent 分别处理程序复现环境和执行系统。应区分生成“问题”、生成“可运行环境”和获得“训练轨迹”。
6. [Harbor Adapters / Harbor-Index，2609.04298v1](https://arxiv.org/html/2609.04298v1)：§2 统一适配和 parity；§3 比较 harness、成本和失败；§4 82 个困难任务，来自 54 benchmarks 的 6,627 候选，最终涉及 29 benchmarks。它是困难前沿切片，不是通用能力量尺。
7. [Harbor-Index 官方介绍](https://harbor-index.org/)：难度过滤 → AI 审计 → 人工审计 → audit/fix/re-run；difficulty 和 correctness 分开。动态网站的当前评测不等于论文固定 v1 的同一快照，不混用榜单数字。
8. [Harbor task format](https://www.harborframework.com/docs/task-format)、[独立 verifier](https://www.harborframework.com/news/separate-verifier-sandboxes)：任务由 instruction / environment / tests / solution 组成；reward 输出到 `/logs/verifier/reward.txt` 或 JSON。separate sandbox 只接收显式 artifacts，不能访问未复制的进程状态。公开示例应原样采用 `artifacts` 与 `verifier.environment_mode`，不能造未知参数。
9. [Terminal-Bench 4.0 官方说明](https://www.tbench.ai/news/terminal-bench-4-0)：资源校准、移除 8 个任务，major version 是 breaking change，需要重跑。官方正文说 19 个任务修复；[项目合作方页面](https://snorkel.ai/leaderboard/terminal-bench-4-0/) 说 20 revised、66 tasks。保留 19/20 的来源分歧，不自行归因，数字以 release 逐项清单为最终复核对象。
10. [Silent Instrument Errors，2611.04399v1](https://arxiv.org/html/2611.04399v1)：作者对 HAL/τ 系列归档报告 nested spans 双重计费、未进入 grader、gold replay 混入动作日志及 evaluator 版本重评分问题。维护者确认等情况均为该作者报告；本地没有重放验证。用于提出检查模式，不泛称所有 leaderboard 不可信。
11. [AgentProofBench，2610.34634v1](https://arxiv.org/html/2610.34634v1)：可重用 verifier 的 reuse / rebuild、决策重放与 deployment-state panels。只支持其特定任务族结论。

### RL 目标、信用与系统

1. [GRPO 基础在现有系列中](../content/series/llm-training-lifecycle/s04_rl_evaluation.html)；新文应采用四维比较：advantage、importance ratio/clipping、loss aggregation、sampling/filtering。不要只列算法时间线。
2. [DAPO，2503.14476v1](https://arxiv.org/html/2503.14476v1)：Clip-Higher、动态采样、token-level loss、超长处理。[Dr. GRPO，2503.20783v1](https://arxiv.org/html/2503.20783v1)：长度和 reward std 归一化偏差；不应误称所有按 token 聚合方案权重一样。
3. [GSPO，2507.18071v1](https://arxiv.org/html/2507.18071v1)：`s = exp(mean_token(log πθ − log πold))`。是长度归一的序列比例，不等于完整轨迹 likelihood product。多轮实现还要说明比例按 response/turn/episode 计算。
4. [MiniMax-M1，2506.13585v1](https://arxiv.org/html/2506.13585v1)：CISPO 原始出处；clipped IS weight 配 stop-gradient 与 log-prob 梯度，区别 PPO clipped surrogate，不能归为 Kimi K2 发明。
5. [GiGPO，2505.10978v3](https://arxiv.org/html/2505.10978v3)：episode + anchor state group advantage；要求状态可比和复现，网页搜索场景容易碎片化。
6. [ARLArena，2602.21534v3](https://arxiv.org/html/2602.21534v3)：四设计维度、干净 testbed；SAMPO 组合 sequence clipping、细粒度 advantage 与动态过滤。其结果限于论文任务与配方；不推成“GSPO 永远最好”。
7. **SAPO 同名需拆开**：ARLArena 附录 A.2.3 的 Soft Adaptive Policy Optimization 是 soft clipping 方案；[2608.19842v1 的 SAPO](https://arxiv.org/html/2608.19842v1) 是 Single-Rollout Autoregressive Policy Optimization，单 causal LM 同时生成动作和值、turn-level GAE 与 SARSA，无单独 critic、仍有 value learning。另有 2606.08755 的 skill SAPO，本次不展开。每次写缩写需全名与版本。
8. [RLDS，2609.27035v1](https://arxiv.org/html/2609.27035v1)：固定 subtask taxonomy、reflection 对每轴判分及 pivot step、SDAE 计算每子任务 group advantage，再把 credit 分配到 pivot 附近 token。是诊断驱动信用方案，不是直接把自然语言反思文本当 reward；没有证明反思就是 causal truth。
9. [KnowGPO，2610.22331v1](https://arxiv.org/html/2610.22331v1)：构建 query-specific knowledge conditions，按已满足条件集合分组，增量知识作 process reward。训练条件构造使用 reference answer，外部 verifier 仍需校准；不能称 oracle-free 或完全不需要评估模型。
10. [AReaL，2505.24298v1](https://arxiv.org/html/2505.24298v1)：异步 rollout–trainer 分离与可控 staleness，是基础系统论文。[T1，2609.11042v1](https://arxiv.org/html/2609.11042v1)：terminal 长程训练与 routing replay。[Macaron，2608.09819v1](https://arxiv.org/html/2608.09819v1) §4.3：R³、DSA alignment、IcePop-style residual filtering。
11. DeepSeek V4.1 §5.2.2 **明确分开两个问题**：短轨迹先返回的样本分布偏置由 per-dataset concurrency / 早期短样本处理控制；过时策略样本由 dispatch/waiting 限制及 stale token loss mask 处理。重要性比率不是两者通用修复。§5.2.1/5.2.3 还记录分段 routing、token 中断和跨 checkpoint 的状态处理，这是作者特定系统做法，不能推荐无条件复用所有旧 KV。
12. [CARM，2610.02039v1](https://arxiv.org/html/2610.02039v1)：取消平均 log-ratio 中正负抵消的 mask 诊断。作为待比较新方向，不宣称单凭它能保证 off-policy 正确。
13. 异质 GRPO：同题独立 Bernoulli outcome 假设下，有非零组方差的概率 `1 − p^G − (1−p)^G`；是解析推导，不是测量或模拟数据。组内 std 不平衡学习机会，还可能产生隐式任务权重。建议域/难度分层、零方差组、有效目标 token、verifier disagreement、长度、梯度贡献及真实失败归因。
14. [MOPD，2606.30406v1](https://arxiv.org/html/2606.30406v1)：多教师整合。[Nemotron Ultra，2606.15007v1](https://arxiv.org/html/2606.15007v1) 和 V4 的蒸馏配方可和已有训练系列对接，不能合并不同老师、logits 范围和 mask 的实验结论。

### 基模与推理：DeepSeek V4.1 主线

1. [官方 09-10 发布](https://api-docs.deepseek.com/news/news260910/) 与 arXiv v1 日期 09-17 区分；[1017 更新](https://api-docs.deepseek.com/news/news261017) 为 self-feedback RL 的端到端项目开发增强，不能套用 1017 分数假称 v1 架构消融。
2. v1 §2.1：552B backbone **另有** 196B Engram；40 layers = 20 causal encoder + 20 decoder；prefill 8B active、decode 16B active，1M context，45T 多模态预训练。
3. §2.2 CED：decoder global KV 由 encoder 末层 hidden state 通过 projection 得到；长 prompt 主计算在下半模型。decoder SWA 仍依赖各层状态，需要尾部 bounded replay，不能画成 prefill 完全不走 decoder。
4. §2.3 CSA2：Full 产生 KV/indexer K 和 top-k；Reindex 共享 KV/K、重算 top-k；Reuse 共享 KV/K/top-k；各层仍有自己的 Q 和 SWA KV。decoder hierarchical index 后层只扫描首层候选池，**第一层仍扫描全文**；不宣称所有 indexing 变 O(1)。
5. §2.4 FP4 主 KV；摘要的 890 **bytes/token** 是 global KV 在 HBM 的口径，约 V4-Flash 的 1/4，不是总显存 / 模型参数 / SWA 缓存。persistent cache 约 1/8 是 SSD/host 口径，不是额外乘成 HBM 1/32。
6. §3.2.2 bounded replay 是近似重建局部状态的 storage–compute trade-off；作者实验称影响小，不能泛称 bit-exact。prefix 命中、短轮工具返回、输入输出比、cache IO 与排队是端到端的必要分析变量。
7. [Engram，2601.07372v1](https://arxiv.org/html/2601.07372v1)：N-gram hashing 和 context-aware gating，是条件参数记忆；区别于 KV、RAG、episodic memory 和 skill files。
8. [Kimi K3，2607.24653v1](https://arxiv.org/html/2607.24653v1)：2.8T/104B、KDA、Attention Residuals、Stable LatentMoE，896 routed experts 中激活16；与 V4.1 是不同架构路线，K3 不替代前沿页的 K3.1 当前快讯。不要跨模型比较未经同硬件复现的 speedup。

### 扩散、投机与场景扩展

1. [DFlash，2602.06036v1](https://arxiv.org/html/2602.06036v1)：block diffusion parallel drafter，target AR model 验证；不是证明 standalone DLM 全面替代 AR。
2. [DSpark，2607.05147v1](https://arxiv.org/html/2607.05147v1)：parallel heavy backbone + lightweight sequential head 恢复块内依赖；confidence 与硬件 profile 控制验证长度。§3.2.2 和附录 A 指出 retrospective 看未来 token 选择验证长度可能产生 selection bias；精确保分布需要 non-anticipating admission。
3. [AdaFlash，2607.19223v1](https://arxiv.org/html/2607.19223v1)：利用 target 对 drafter 实际 rollout 的 feedback 作 reverse-KL OPD 与长度预测；domain adaptation 有作者实验，不能把 acceptance 提升当作所有并发条件 throughput 提升。
4. [OSWorld 2.0 项目合作方介绍](https://snorkel.ai/leaderboard/os-world-2-0/)：108 long-horizon tasks、31 self-hosted sites、150/300/500 step budgets，binary 与 partial score 必须同预算比较；评价最终状态而非唯一点击序列。合作方数字未本地复现。
5. [AIRS-Bench，2602.06855v3](https://arxiv.org/html/2602.06855v3)：20 research tasks，problem / dataset / metric，valid submission、normalized performance 与多种 scaffold；科学 Agent 评价不能只检查文件存在或文章流畅。
6. [SkillsBench 初版，2602.12670v1](https://arxiv.org/html/2602.12670v1) 的 86 tasks/11 domains/7 configurations 与 [1.1 官方发布](https://www.skillsbench.ai/blogs/skillsbench-1-1) 的 87/8/18 不可混用；后者还区分 paper aggregate 与动态 leaderboard。curated skills 的正效应不代表 self-generated skill 必然有效。
7. [Macaron-V1，2608.09819v1](https://arxiv.org/html/2608.09819v1)：冻结 base、per-turn LoRA routing、模型–harness 版本链、memory/context/parameters 的不同更新层。报告明确长期 compounding continual learning / collective intelligence 仍为 open question。
8. [Kimi K2.5，2602.02276v1](https://arxiv.org/html/2602.02276v1)：PARL 和 Agent Swarm；比较并行策略必须同时报告 critical-path wall time 与 total tokens / GPU / tools，不能只报子 agent 数量。

## 正文交付设计

新系列 ID `llm-research-map-2026`，公开入口 `/llm-research-map-2026/`，复用现有纸色 / 青绿色文章阅读样式，正文已写入以下唯一源文件：

- 入口：覆盖矩阵、P0/P1/P2 编辑判断、已有文章分工、五章路径、来源索引和本地报告下载。
- `s01_agent_data_bench.html`：数据资产分类、四种合成路线、Harbor 格式与隔离、parity、污染/失败/成本记录、任务验收建议。
- `s02_agentic_rl.html`：四维 loss 地图、GRPO/GSPO/CISPO 数学、GiGPO/RLDS/KnowGPO/SAMPO、SAPO 同名、异质数据、异步两类偏差、同预算消融。
- `s03_base_architecture.html`：V4→V4.1→1017 的引用边界、CED 可视流程、CSA2 模式表、global/persistent/SWA/weight 口径、Engram 与 Kimi 对照、与 Agent 生命周期相连。
- `s04_inference_diffusion.html`：prefill/decode/cache 成本、DFlash/DSpark/AdaFlash、验证精确性、低/高并发与质量预算、已有 DLM 系列交叉引用。
- `s05_agent_frontiers.html`：GUI 与科学任务、skills/memory/continual model 更新、PARL/专家整合、公开项目关联及后续专题验收条件。

每章必须有机制、限制、来源和建议实验。建议实验明确未执行；不生成或展示假训练曲线、fake benchmark rows 或预测收益。

## 报告归档与许可

DeepSeek 报告从官方 Hugging Face 仓库 revision `314113f8a7dadb388215396ba5fbee2c610a04d6` 获取；官方 README 明确 repository and model weights 为 MIT，LICENSE 包含 associated documentation。保留原始 PDF 和完整 MIT notice。论文总结引用固定 arXiv v1；本地 HF 文件称为该 revision 的官方快照，不未经比对宣称与 arXiv 字节相同。

其他本地原件只选择核对为 CC BY 4.0 的论文：Engram、DSpark、DFlash、EvoSyn、ProgramGym、RLDS、Single-Rollout SAPO、ARLArena、SWE-smith。原件不裁切、不改字节，作者与题名页完整保留；同时提供 canonical URL、固定 version 和 CC BY 链接。其他论文提供来源链接；不能把 arXiv perpetual non-exclusive license 当作普通转载授权。

## 验收范围与限制

后续编辑在唯一源入口完成，并接入 catalog、首页推荐、关联阅读和系列顺序。检查新产物的链接、锚点、source 数量、PDF 字节/hash、许可 notice，以及移动与桌面排版。已有迁移基线正文若加交叉引用，只登记该文件的准确新 SHA 和理由，不重建原始基线。

本次不声称所有旧文章科研断言已重新复核，不替未知的商用架构补参数，也不将版本榜单作为算法因果证据。待执行实验、缺少独立复现和来源分歧在正文保留。

## 集成与后续维护

六个入口在 `content/catalog.json` 登记，五章按order 1–5生成前后章导航，并跨Agent、RL、LLM基础与扩散分类参与章节搜索。首页与博客推荐使用目录数据生成；相关旧文通过目录related接入新专题，既有正文、URL、科研公式与AUTO标记未修改。原迁移基线及差异清单未重建。

13项公开归档资源在 `content/site.json` 显式登记：10份PDF、来源JSON、许可说明TXT及完整MIT notice。公开署名与转载说明见 `assets/research/2026-11-14/NOTICE.txt`，按原文校正归档论文的完整作者姓名，去除机构编号和脚注。校验及发布状态另记 `docs/validation.md`，只采用本轮实际结果。
