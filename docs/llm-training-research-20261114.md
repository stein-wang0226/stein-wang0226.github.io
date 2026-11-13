# LLM 训练全链路：来源与原文复核记录

调研截止：2026-11-14。范围为公开原论文、团队技术报告与官方文档；并非全部商业模型的内部训练流程。
数字来自作者报告，未在本地复现训练。本文采用版本固定的论文链接，避免后续修订改变引用口径。
来源编号与 `content/series/llm-training-lifecycle/` 中的 `[1]`–`[27]` 对应。

## 原始材料

用户提供 `agent-base-mid-training-20261114.html`，19,556 字节。
SHA-256：`9be90744e1db851023a2a2e26d02d53df2d43ec20eb814314bcdca0df92a5061`。
原件已逐字节保存至 `content/archive/agent-base-mid-training-20261114.original.html`，用于来源追溯；
不登记为历史 RL 页面，也不加入发布清单。原文六个内容块及有用示例纳入第二章与第四章。
原文锚点 `recipe/results/landscape/data/harbor/sources` 在第二章保留，Harbor 的完整扩展方案放第四章。

## 原始资料登记

| 编号 | 来源与固定版本 | 核对位置 / 用途 |
|---|---|---|
| 1 | [Singhal et al., Priming Base Models for Agentic Post-Training, 2610.22019v1](https://arxiv.org/html/2610.22019v1) | §3–6、表1–3、表9、附录B/D；2026-10-15 的公开 midtraining 配方与受控证据 |
| 2 | [Qwen3-Coder-Next Technical Report, 2603.00729v1](https://arxiv.org/html/2603.00729v1) | §2–4、图3/5、附录A.3；仓库、轨迹、BFP、专家蒸馏及跨框架迁移 |
| 3 | [GLM-5, 2602.15763v1](https://arxiv.org/html/2602.15763v1) | §2.3、3.1–3.5、4.1；上下文课程、错误动作 mask、异步 RL 和跨阶段蒸馏 |
| 4 | [Olmo 3, 2512.13961v2](https://arxiv.org/html/2512.13961v2) | §2.1、3.5–3.6、表5/11；Dolmino、Longmino 与可分叉 model flow |
| 5 | [MidTool, 2608.20314v1](https://arxiv.org/html/2608.20314v1) | §2、3.1–3.3、表2–6；通用工具 midtraining、来源 / 合成占比与负消融 |
| 6 | [PRISM, 2603.17074v3](https://arxiv.org/html/2603.17074v3) | §6、8.1、9、表4/7；混合数据、分项回归与 RL 初始化 |
| 7 | [SPT, 2608.26563v1](https://arxiv.org/html/2608.26563v1) | Skill Pre-Training / Multi-File Skill Assembly；技能包作为语料、Reference Insert |
| 8 | [Function-Aware FIM, 2607.12463v3](https://arxiv.org/html/2607.12463v3) | §2.2–2.4、3.1–3.4、表1/2；函数依赖选择、教师 rationale / body、起始 Instruct 权重 |
| 9 | [Midtraining Bridges Pretraining and Posttraining Distributions, 2510.14865v2](https://arxiv.org/html/2510.14865v2) | 混合分布、引入时间与比例的受控实验；不能将机制假说推广为普适定律 |
| 10 | [DeepSeek-V4, 2606.19348v1](https://arxiv.org/html/2606.19348v1) | §4.1–4.2、5.1.1–5.1.2；训练量、4K→1M、专家 SFT/RL→完整词表 OPD |
| 11 | [Nemotron 3 Ultra, 2606.15007v1](https://arxiv.org/html/2606.15007v1) | §2、3.1–3.3、表5、§3.3.5；20T 预训练、统一 RLVR→MOPD、采样 token 消融 |
| 12 | [Qwen3 Technical Report, 2505.09388v1](https://arxiv.org/html/2505.09388v1) | §3.2、4.1–4.5；三段预训练、cold start→RL→fusion SFT→general RL |
| 13 | [DeepSeek-R1, 2501.12948v1](https://arxiv.org/html/2501.12948v1) | §2；R1-Zero 分支、cold start、推理 RL、拒绝采样 SFT 与第二轮 RL / 小模型蒸馏 |
| 14 | [Training Compute-Optimal Large Language Models, 2203.15556v1](https://arxiv.org/html/2203.15556v1) | compute-optimal 的固定算力假设；参数与 token 扩展，不照搬固定 token/parameter 比例 |
| 15 | [Efficient Training of Language Models to Fill in the Middle, 2207.14255v1](https://arxiv.org/html/2207.14255v1) | FIM prefix/suffix/middle 重排；自回归 decoder 也能学习编辑条件分布 |
| 16 | [The Llama 3 Herd of Models, 2407.21783v1](https://arxiv.org/html/2407.21783v1) | 预训练数据治理、annealing / 长上下文、SFT / DPO 和拒绝采样 |
| 17 | [DPO, 2305.18290v1](https://arxiv.org/html/2305.18290v1) | 固定 chosen/rejected 对上的偏好目标；标准离线 DPO 不等于在线 rollout RL |
| 18 | [PPO, 1707.06347v2](https://arxiv.org/abs/1707.06347v2) | 摘要与原始优化形式；policy ratio、clip、采样→更新；不依据旧 v1 的无正文 HTML |
| 19 | [InstructGPT, 2203.02155v1](https://arxiv.org/html/2203.02155v1) | SFT→偏好 reward model→PPO；人类反馈与参考策略正则 |
| 20 | [DeepSeekMath, 2402.03300v1](https://arxiv.org/html/2402.03300v1) | 原 GRPO，组相对 advantage；去掉独立 critic，不等于省去采样或 reward |
| 21 | [DAPO, 2503.14476v1](https://arxiv.org/html/2503.14476v1) | 非对称 clipping、动态采样、token-level loss 与超长样本处理 |
| 22 | [Understanding R1-Zero-Like Training, 2503.20783v1](https://arxiv.org/html/2503.20783v1) | Dr. GRPO；长度 / 难度归一化偏差及 base 先验的影响 |
| 23 | [GSPO, 2507.18071v1](https://arxiv.org/html/2507.18071v1) | §4.1；序列平均 log-ratio 后取 exp，序列层面 clipping；并非原始概率比的无修改估计 |
| 24 | [Scaling Relationship on Learning Mathematical Reasoning, 2308.01825v2](https://arxiv.org/abs/2308.01825v2) | 作者明确命名 Rejection sampling Fine-Tuning，采样正确推理路径后继续监督训练 |
| 25 | [OpenAI Reinforcement fine-tuning](https://developers.openai.com/api/docs/guides/reinforcement-fine-tuning) | 官方文档定义另一种 RFT：自定义 grader + policy gradient。只用于术语，不提供过期模型 API 操作教程 |
| 26 | [DeepSeek 官方 V4-Pro 模型卡](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro) | 与报告交叉核对 32T+、专家 SFT/GRPO→OPD、1M 与 Pro/Flash 规格 |
| 27 | [Ai2 官方 Olmo 3 model flow](https://allenai.org/blog/olmo3) | 官方发布 2025-11-20，后有 3.1 更新；Base / Instruct / Think / RL-Zero 分支 |

24 篇论文 + 3 份官方网页 / 文档。多数 2026 技术报告为作者自报或预印本；
未标记为独立第三方复现。报告中“最新”指截至上述日期可查且与训练链路直接相关的公开方案。
论文编号与首次发布日期不能机械互推；DeepSeek-V4 元数据日期与编号月份不同，因此正文不推断其发布日。
Olmo 3 官方发布与报告提交分开记录；桥接论文使用 2026-02 修订的 v2，而非沿用“2025 原版”。

## 原文数字核对与必要修订

| 原文项 | 核对结论 / 正文处理 |
|---|---|
| Nemotron 数据桶比例 | 表1：40.8/20/10/3/1.2/20/5%，和为100%；按输入训练 token 分配。39.4B 是唯一轨迹 token，50.3B 是约500B运行见到的轨迹 token |
| Lightning 500B | 表3：Verified 60.7→64.5、Multilingual 55.8→62.8、Pro 32.0→35.5、TB2.0 22.6→23.6。起点 Lightning-LC；均接100B full SFT |
| Super 280B | §4.4：DeepSWE 11.7→15.7、Verified 72.9→74.3；同 full SFT。不得与 Lightning-8K 或 short SFT 横向拼接 |
| 100B trace 置换 | 表2 Lightning-8K full SFT：no traces 60.5/18.5，with traces 63.5/25.1；直接SFT 59.7/22.9（Verified/TB2.0） |
| 工具返回 mask | 表9：27.5→37.8 pass@1，41.6→53.0 pass@3；100B midtraining接“较早版本SFT配方”，不是33B short SFT的通用结果 |
| Nemotron 设置 | 附录B：256K、GBS64、Adam、BF16、文档间隔离注意力；Lightning/Super LR5e−5/1e−5，warmup后恒定。保留MTP，权重0.1/0.3 |
| Nemotron 评测限制 | SWE pass@1 在每题3次 rollout上平均，TB在8次平均；论文“single run”指训练比较，不能写成每题只采样一次。没有等总算力对照；RL只有Lightning-8K短、单种子实验 |
| Qwen 数据与目标 | 600B仓库token、370语言、万亿级midtraining、262144context属实。完整混合比和逐角色loss未公开，不能类推成Nemotron assistant-only配方 |
| GLM 数据口径 | 32K/128K/200K为1T/500B/50B实际训练；160B为issue–PR唯一token池。包含自然与合成agent轨迹 |
| Olmo 长上下文 | 必须改为7B50B、32B100B训练；Dolmino pool2.19T→99.95B mix；Longmino池639B、样本比例约34%长数据+66%midtraining回放 |
| MidTool 合成比例 | 表2 Web42%/PDF23%/Code26%桶各含raw+augmentation，原生轨迹9%。不能把其余91%称为纯自然数据 |
| MidTool 主结果 | 表3 4B BFCL39.73→50.25；表4 τ²8.54→12.23；同100K TOUCAN SFT。RL可继续提升overall，但并非每个分项都会提升 |
| PRISM “保留通用能力” | 表4 Granite3.3-8B MCS：LB-V1平均66.15→66.48，HellaSwag83.46→78.12。表7 Math+Code模型RULER128K59.09→6.46；平均不降不代表无遗忘 |
| SPT | 38040包、218277文件、Reference Insert后约347.8M token，4096块；固定预算混合，比例需扫，不作通用默认值 |
| Function-aware FIM | 968 Python仓库、约400K样本、2.6B token。不能写成纯天然自监督：§2.4 Gemini3Flash生成rationale+candidate body，ground truth只作judge过滤。起始有Qwen2.5-Coder-Instruct；Qwen3-8B的对照同时改变后训练pipeline |
| Function-aware结果 | 表1固定R2E-Gym：7B15.0→17.8、14B26.2→29.2 Verified；Qwen3+SWE-Lego31.8→35.0。不能与“officially reported”基线求差；评测3种子不是训练3种子 |
| OPD | V4 §5.1.2用完整词表reverse KL，认为采样估计方差高；Ultra §3.3.5实验反而倾向sampled-token。协议、教师支持范围与预算不同，不作普适优劣判断 |

## 跨来源结论及边界

1. **阶段与目标是两个维度。** CPT 描述从已有权重继续训练，midtraining 描述 pipeline 中的能力准备阶段；
   可包含文档 LM、FIM、QA 和 masked trace。依据1/2/3/4，不能仅以 assistant-only loss 判定是否属于 SFT 阶段。
2. **重点从单文件 / 静态文本扩展到结构与交互。** repo/PR/CI、参考技能包、函数依赖、API workflow 的具体形态各异。
   依据1/2/5/7/8，不能断言“更多合成轨迹”必然更好。
3. **评估 midtraining 必须经过固定下游训练与能力回归。** 依据1/4/6；
   代理损失有帮助，但可靠性因模型和任务而异，不一概否定 perplexity。固定SFT解释初始化增量，等总算力解释预算价值。
4. **后训练是可循环、可分叉的图。** 依据12/13/27：RL之后可返回拒绝采样SFT，Base可以走RL-Zero；
   依据2/3/10/11：专家或历史阶段checkpoint可作为教师再汇总到单模型。
5. **RFT 必须写全名。** 24是拒绝采样后SFT，25是grader驱动RL，17的标准DPO是固定偏好对优化。
   与SFT、RL并列时不能把两种RFT混为同一个阶段。
6. **OPD不是权重平均，也不等于教师生成静态SFT。** 10/11/3在学生采样的状态上评分；
   teacher指导有偏差与支持范围限制，不能代替独立最终verifier。

## 实践方案的证据性质

CSV schema、mask 伪代码、checkpoint 清单和 Harbor A/B/C/D/E 设计为教学与建议，未执行训练。
A=直接固定SFT；B=等输入预算通用CPT→同SFT；C=领域+回放CPT→同SFT；
D=从C置换部分token为assistant-only轨迹→同SFT；E=额外预算用于SFT。
B/C/D匹配输入token、长度分布等，并实际报告FLOPs/GPU小时；
不能因输入token相等就宣称总算力完全相等，也不能因mask不同但输入相同就忽略有效目标token权重。
评测按任务族/仓库/环境留出，记录harness、模板、工具、verifier、模型与环境版本，
报告配对bootstrap置信区间、训练种子和环境失败分母，未提供虚构Harbor结果或预期提升。

## 内容集成与验收

系列入口和四章的源文件位于 `content/series/llm-training-lifecycle/`，
通过 `content/catalog.json` 登记标题、标签、分类、日期、前后章及关联阅读。
范围仅是新增系列和专用CSS；既有科研正文与迁移基线不需变更。
页面构建、链接、浏览器及原件保留的真实验收结果见 `docs/validation.md` 的本次增量记录。
