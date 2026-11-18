# 后训练专题：来源、推导与验收

调研截止：2026-11-14。公开入口 `/llm-posttraining/`，六章。
本次研究与正文审阅覆盖该新专题；不将旧文全部科研结论标记为已复现。
本站没有执行 GPU 后训练，三类任务是教学设计，实验矩阵是待执行方案。

## 内容职责

| 章节 | 核心贡献 | 主要来源编号 |
| --- | --- | --- |
| 01 监督与偏好 | mask、两种RFT、恢复、DPO/SimPO/ORPO/KTO、工业训练图 | 12–23、27、49 |
| 02 RL目标 | PPO/GAE/RLOO/GRPO、分母、GSPO/CISPO/SAPO/SAO、论文级recipe、参数背诵表与追问卡 | 1–11、44、50、58、73–79 |
| 03 OPD | fixed-prefix梯度、full/sample/top-k、多教师、自蒸馏、参数、覆盖与遗忘 | 24–36、55、60、66 |
| 04 环境与信用 | Harbor隔离、PRM/value、图/信念/环境反馈信用、子任务与GAR | 27、37–44、53–54、67–70 |
| 05 系统 | 十二类框架、配置映射、三策略、completion bias、partial KV、固定slime代码 | 25、27、45–65、71–72 |
| 06 案例 | code/科学/GUI输入到终评、轨迹契约、单轴消融与成本 | 16、27、30、34、41、53–54 |

编号、原始URL、版本/commit、位置与使用章节见公开
`assets/research/posttraining-20261114/sources.json`，共79项。
该索引从正文参考列表生成。动态文档记录访问日期，不宣称与仓库SHA同步。
不归档整个外部仓库或新大文件；沿用既有V4.1、Ultra、RLDS、ARLArena原件。

## 关键核对与证据边界

1. RFT区分Rejection sampling Fine-Tuning与Reinforcement Fine-Tuning。
   OpenAI使用成功访问的Cookbook案例；API文档重定向页面不作为完整操作核验。
2. ReTerm 2610.18484v1 §3.1只监督教师恢复token；§3.2另有GRPO分支。
   失败上下文与失败动作监督不同，不说所有失败token应统一屏蔽。
3. GRPO全同reward组仅task PG为零，其他KL/OPD/entropy项可非零。
   `1-p^G-(1-p)^G`仅独立二值采样解析，非实测训练数据。
4. GSPO的序列ratio是平均log-ratio的exp，非完整trajectory IS乘积。
   CISPO裁剪IS系数并detach；Soft SAPO的f(r)保留advantage与符号温度。
5. 两种SAPO区分：2511.20347v1软门控；2608.19842v1单rollout共享policy/value。
   SAO 2607.07508v1的strict IS mask不等于PPO的min-clipping。
6. 完整词表reverse-KL局部logits梯度为
   `p_v[(log p_v-log q_v)-D]`；固定sample上的裸log-ratio反传不等价。
   fixed-prefix identity不包含整个状态分布对参数的导数。
7. DeepSeek V4 §5.1.2与V4.1 §5.2.4使用full-vocabulary；
   Ultra §3.3.5的sampled-token偏好是特定Agent实验，off-support解释为作者假说。
8. MiMo 2610.11959v1 §5.6的MOPD2含standard/teacher-prefix/SFT-prefix OPD：
   prefix可来自示范，学生新生成一回合；不称整episode纯on-policy。
   MOPD 2606.30406v1与MOPD2另列，不把两个名字混用。
9. OPSD 2601.18734v2为同模型不同context的特权解法蒸馏；
   SDPO使用环境文本或成功sibling；SDPG另外组合outcome PG、gate/schedule与UKL。
10. Guided-OPD 2606.15912v2学生回合reverse、教师回合forward KL；
    TISD 2609.30878v1干预后重采后缀。科学Avg@128 equal-step/time与代码Avg@4分开。
11. OPDArena 2610.25651v1实际OPD是student-weighted Top-16；
    full-vocab用于部分分布测量。OOD分布变化与遗忘是关联，非因果证明。
12. PRM步骤正确性、MC continuation成功、value、advantage不同。
    PURE最差步骤目标与Cliff首错后信用不能直接迁移到可恢复Agent。
13. Harbor当前overview/verifier文档已访问；separate环境不继承全部工作区，
    artifacts是TOML顶层键；reward.txt/json并存时JSON优先。历史shared任务单独核对。
14. slime SHA `79aa41a884ab0bf65222c94418f6357d3c31192b`：
    `loss.py`715–719行原始短摘录；829–836应用OPD，839之后可normalize。
    `on_policy_distillation.py`与同SHA文档对照；摘录依Apache-2.0标注。
15. verl `staleness_threshold`为backlog比例而非checkpoint lag个数；
    三策略概率、同版本kernel/template/routing误差与完成顺序偏移分别处理。
16. Agent Lightning v1.0 2608.17528v1已重写，保存真实API调用与exact token前缀；
    不将2025 v0.x LightningRL图当作当前实现。
17. 框架固定README支持与特殊branch/recipe边界保留，ROLL部分async仍在实现。
    AReaL新后端、SkyRL两package、NeMo跨tokenizer均不泛化为全组合支持。
18. 2026 Agentic RL信用趋势新增GraphGPO、ReBel、EFCA与MileGPO：
    分别复用状态转移图、结构化belief、环境反馈多时间尺度和里程碑/分支证据。
    主要实验环境集中在ALFWorld/WebShop等，不外推为开放代码、GUI和科学任务的通用增益。
19. TorchForge固定README `b32f06b` 明确开发暂停并向TorchTitan汇总，
    因而仅保留架构参考，不列为活跃首选。ART固定README `534620a` 作为
    既有多步Agent接入GRPO的客户端/训练后端路线，不与底层分布式框架按star排名。
20. 配方审计以语义字段为准：模型/模板、prompt batch、每题生成数、生成参数、
    verifier、advantage、ratio/clip/分母、优化器、并行与异步版本均需记录。
    没有跨模型通用依据的learning rate、group size或batch不写成标准答案。
21. DeepSeekMath v3 §4.2明确披露G=64、training batch=1024、max=1024、
    policy LR=1e-6、KL β=0.04和每次exploration后单次更新；原文未进一步定义
    batch的prompt/trajectory单位，因此正文不自行用1024/64反推prompt数。
22. DeepSeek-R1 v2新增R1-Zero数值：G=16、每次update为32 prompts/512 trajectories、
    外层8192 outputs拆16 mini-batches、LR=3e-6、β=0.001、T=1、32K→64K、
    single inner epoch及reference每400步刷新。第一RL阶段另写clip ε=10；
    该异常量级按版本原文保留，不提升为通用默认。
23. DAPO论文与固定复现脚本分开：论文warmup为20 rollout steps，commit `4f80e4`
    脚本为10；两者均使用512 prompts、G=16、LR=1e-6、clip 0.20/0.28、
    KL=0及20,480最大生成长度。差异明确并列，不静默选一个。
24. Dr.GRPO论文表给G=8、T/top-p=1、max=3000、LR=1e-6、clip=0.2、
    KL=0、inner epoch=1、AdamW betas(0.9,0.95)、WD=0、grad clip=1；
    global batch未在论文表披露。OAT README中的batch=128仅列作官方命令参数。
25. GSPO原论文披露Qwen3-30B-A3B、4 mini-batches和sequence clip
    3e-4/4e-4，对照GRPO 0.20/0.27；未公开G/LR/global batch等完整配方。
    ROLL数值只标“文档示例”。MiniMax报告未给CISPO最终clip/LR/G；
    NeMo的[0,6] clamp只标固定验证配置，不能冒充MiniMax原始recipe。

## 面试覆盖审计结论

| 维度 | 当前覆盖 | 结论 |
| --- | --- | --- |
| RLVR算法 | PPO/GAE、RLOO/GRPO、DAPO/Dr.GRPO、GSPO/CISPO、两种SAPO、SAO | 主线完整；已补配方和诊断 |
| Agentic RL | 多轮环境、verifier、GiGPO/RLDS/KnowGPO、图/belief/环境反馈信用、单轨迹value | 主流与2026趋势已形成方法簇，不逐篇堆名 |
| OPD | full/top-k/sampled、MOPD/MOPD2、OPSD/SDPO/SDPG、Guided-OPD/TISD、遗忘 | 主线完整；已补教师接口、混合目标和监控 |
| 框架 | TRL、verl、slime、AReaL、OpenRLHF、NeMo RL、ROLL、RLinf、SkyRL、Agent Lightning、ART、TorchForge | 按角色和维护状态覆盖；不做star速度榜 |
| 参数与训练细节 | DeepSeekMath/R1、DAPO、Dr.GRPO论文原值；GSPO/CISPO披露边界；TRL/ROLL/NeMo固定配置；参数联动与12道追问 | 达到可背诵实验卡层；论文值、框架默认与文档示例严格分栏 |
| 旁支谱系 | Offline RL、Decision Transformer、AlphaZero/MuZero、MARL、Distributional/Model-based RL | 在面试手册略写完整，不与RLVR主线等篇幅 |

## 图与教学资源

| 文件 | 口径 |
| --- | --- |
| group-signal.csv / .svg | G=8独立Bernoulli解析概率，9个p值；图显示1%/50%/99% |
| mimo-compute.csv / .svg | MiMo-V2.6 Pro §4.1 Figure3：43.8/43.5/12.7%；非美元占比 |
| figure-data.json | 轴/来源/公式与数据文件对应 |
| case-contracts.json | 三案例、空轨迹契约，design_only，无虚构reward或cost |
| experiment-matrix.csv | E0–E6单轴对照、固定条件和成本分母，均待执行 |

图以inline SVG呈现并保留viewBox，下载原始SVG与CSV。
flow/目标mask/公式/原始短代码共同讲机制，不引入外部图片或运行依赖。

## 已执行的数学核验

临时脚本 `/tmp/my-blogs-posttraining-artifacts.py`：
四组概率分布×三个logit，有限差分对照reverse-KL解析梯度，误差<1e-8；
三个Soft SAPO温度对照ratio=1的导数为1；
两个GRPO有效组解析值、未cap GAR正优势质量守恒及MiMo比例求和。
共19项通过。这些检查是数学/数据核验，不能称模型训练或论文复现。

构建、浏览器与上线验收另记 `docs/validation.md`。

## 2026-11-18：RL 逐步推导与来源续接

本轮在第 02 章补齐问题定义、分层符号表、交互闭环与训练角色分支，
再展开 REINFORCE、reward-to-go、baseline、critic MSE、方差、有限片段
GAE、PPO 动作换测度与 RLOO/GRPO 组关系。主讲位置仍唯一；
系列入口只补导读与学习深链接，不复制推导或历史手册正文。
原配方、诊断、六幅修订教学图、GAE 边界例与 GRPO 完整组算例继续保留。

原 79 项调研及 2026-11-14 截止日期、旧来源版本和访问/使用日期保留。
本轮仅在尾部新增以下 2 项数学来源，现共 81 项；不表示旧来源重新访问、
模型报告重新验证或历史验收适用于新正文。

| 编号 | 来源与版本口径 | 本轮使用与限制 |
| --- | --- | --- |
| 80 | [OpenAI Spinning Up · Intro to Policy Optimization](https://spinningup.openai.com/en/latest/spinningup/rl_intro3.html)，2026-11-18 访问，教程网页未固定版本 | 轨迹概率、score lemma、reward-to-go、baseline、采样 loss；教程基础目标是有限时域无折扣，本站初态折扣目标保留外层 `gamma^t` |
| 81 | [Greensmith、Bartlett、Baxter：Variance Reduction Techniques for Gradient Estimates in Reinforcement Learning](https://jmlr.org/papers/v5/greensmith04a.html)，JMLR 5（2004），2026-11-18 访问 | 最优 baseline 与真实 value 不必相同；本站固定历史、单步向量 score 的协方差迹最小化单独推导，不宣称最小化完整多步梯度协方差 |

GAE 继续使用 [2] `1506.02438v6`，PPO 使用 [1] `1707.06347v2`，
RLOO 使用 [4] `2402.14740v2`，原 GRPO 版本与编号不变。
实际使用位置由 `scripts/citations.py` 的 `derive()` 取得：
装配改写位置时优先取 `original_url`，使用最近的
`section/article/h2/h3`，不把 h4 或 details 的 ID 猜作引用位置。
新增来源的冻结历史使用与组织前使用均为空；旧条目只在实际引用位置变化时
精确更新其使用字段和本轮使用日期，不批量刷新其他来源登记。

### 正文与凭据边界

- T1/T2 交付的第 02 章 SHA-256：
  `3272afc3ec57839306ceb01e05f08f65fab4f867a8388f6c26e58dd05016e9ee`。
  T3 不再编辑该章。问题/符号/图与 PG 在第 16–171 行，baseline/MSE/方差
  在第 172–301 行，GAE/PPO 在第 302–465 行，组证明与图交接在第 466–557 行；
  `normalization` 起至文末不属本轮正文增补。
- T3 写集成仅涉及系列入口导读/参考、两条 catalog 的 `summary/updated`、
  后训练来源登记、本记录及连续性/组织/内容三份精确凭据。
  连续性保留固定 base `80148053b623c4b6e1fc5a1a062f1113e5039443`、
  原 `sha256_before` 和旧审阅，追加本轮说明；两账本各自的 `prior_reason`、
  archive、baseline、保留单位与 destination 不改。
- 两份不可变基线、冻结原件、旧轮审阅及既有共享脚本/无关审计文档保留。
  当前 `assets/site/scroll-region.js` 的既有用户改动不归为本轮工作。
- 本轮证据仅为 T1/T2 源码交付与 T3 局部集成自检。
  上文“已执行的数学核验”和旧轮构建/浏览器记录均为原范围的历史事实；
  不作为本轮新推导的独立数学、当前构建或界面通过证据。
  独立数学 T4 与当前产物/浏览器 T5 另做，本轮不运行训练、构建或浏览器。

### T3 已执行的集成自检

2026-11-18 复用仓库已有虚拟环境 `~/.cache/stein-notes/venv`：
`python3 scripts/learning_review.py check --verify-git-base` 通过，核对 74 个源的
实际 Git 基线、冻结/当前 SHA 链及精确凭据；`python3 scripts/citations.py check`
通过，核对 1122 条来源/版本记录、引用、登记与归档 SHA/长度。
另通过局部 JSON 逐字段边界检查及源 ID 定位：s02 的 48 个 ID 唯一，
入口 13 条算法学习链接均对应现存源 ID，ref-1 至 ref-81 连续有序；
原 79 项登记和两账本各自的 `prior_reason` 保留。以上均非构建或浏览器验收。
