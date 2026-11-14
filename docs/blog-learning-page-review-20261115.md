# 逐页学习重编记录

本记录对应获批方案，不将静态检查写成浏览器验收或论文复现。
全部74本地条目的逐页编辑判断汇总于下表；最终浏览器与集成验收已完成，
逐源结果见 `blog-learning-validation-20261115.json`，汇总见本文件末尾。
组织 ledger 记录各源的精确原件、教学去向与本表对应理由。

## 前批主线与参考：26源

| 唯一源 | 逐节编辑判断 | 展开 / 算例 | 精简与证据 |
| --- | --- | --- | --- |
| llm-posttraining | 七主题中的反馈与更新入口、六章装配、掌握清单 | 原理→变体→配方→诊断 | 父页只装配唯一片段，删除第二目录与分散阅读路线 |
| posttraining-supervision | SFT、模板/packing、恢复、拒绝采样、偏好、反馈与准入全部审阅 | mask 梯度；KL 正则最优策略→DPO 分类目标 | 方法结论分点，保留KTO/恢复训练来源与退化，偏好细讲唯一主讲 |
| posttraining-algorithms | PG、baseline、GAE/PPO、RLOO/GRPO、各变体、六论文配方、追问与诊断全部审阅 | score-function、reward-to-go、baseline 零均值；GAE/terminal；PPO 分段；组优势 | 修 GiGPO 跨 prompt、固定G/epochs、clip+KL绝对化；六原SVG作带边界的教学图，12追问与论文数值保留 |
| posttraining-opd | 学生轨迹、局部KL、采样梯度、教师接口、多教师、自蒸馏、引导、遗忘全部审阅 | reverse-KL 局部导数；数值估计与梯度估计区别 | 教师接口/成本和监控分点，保工业路线与退化，OPD原理集中本章 |
| posttraining-rewards | 状态机、反馈、过程监督、PURE/Cliff、多步信用、MiMo/RLDS与案例全部审阅 | 重复正确步骤漏洞；局部优势与credit粒度 | 保GraphGPO/ReBel/EFCA/MileGPO等区别与因果边界；经验、奖励漏洞与追问分点 |
| posttraining-frameworks | 框架、配置映射、同步/异步、版本偏移、部分轨迹、Lightning/slime与成本全部审阅 | 策略/数值/完成顺序三偏移；旧KV跨权重边界 | 次要配置按需；固定源码与12类框架口径保留，三种偏差不混成token ratio |
| posttraining-cases | 代码、科学、GUI三任务、反馈、轨迹、实验、诊断与交付全部审阅 | 输入→动作→产物→反馈→训练目标 | GRPO/OPD重复全文归主讲；保独立验收、环境状态、特权信息和未执行实验边界 |
| llm-architecture | 架构入口、六章装配、状态/计算关系与掌握清单 | 表示→选择→更新→恢复 | 删除旧重复目录；源稿分章维护，正文连续阅读 |
| architecture-transformer | 条件预测、张量路径、mask、block、teacher forcing、状态成本与不变量全部审阅 | NLL/softmax导数；4token causal mask；标签shift | 机制展开、结论短卡；修AR训练串行等混淆，原来源和旧定位保留 |
| architecture-attention | 历史访问、MHA/MQA/GQA、cache、RoPE、稀疏、Flash/Paged与对照全部审阅 | 点积方差缩放；二维旋转与相对位移；缓存字节算例 | 型号/框架次表按需；长式分行，原图与共同预算条件保留 |
| architecture-moe | FFN、router、容量、参数/通信、latent专家、EP与消融全部审阅 | 两/三矩阵计数；top-k门控；容量和负载 | 规格名录折叠，不能用总参数替代激活参数或真实吞吐 |
| architecture-residual | 梯度、Norm、初始化/QK/长上下文、AttnRes/mHC与故障全部审阅 | Pre/Post-Norm链式法则；LN/RMS算例 | 修免warmup绝对化；新残差增量归研究地图，基础与诊断集中本章 |
| architecture-hybrid | 外积、衰减/delta、Mamba/SSD、混合层、分支恢复与对照全部审阅 | 状态外积；遗忘与定向覆盖反例；SSM标量状态 | 经验精炼，有限状态压缩边界保留，cache与恢复不自动等价 |
| architecture-comparison | 六比较轴、家族、架构/训练/服务、MTP/drafter、科学设计与证据全部审阅 | 参数、状态、预算、质量独立比较 | 型号名录按需，删除跨设备排名和重复原理长讲 |
| llm-training-lifecycle | 预训练→CPT→SFT→RL/验收→训练方法五章装配 | 阶段产物与监督接口交接 | 入口只保一条主线，训练阶段不再重复后训练全文 |
| llm-training-pretraining | 数据、CLM/FIM、预算、长上下文、恢复、阶段准入全部审阅 | packing边界；6NT前向/反向来由 | 保真实token/重复/预算区别，工程结论分点、共同预算证据保留 |
| llm-training-midtraining | 阶段、工业配方、受控结果、数据/伪代码、配比回放与科学交接全部审阅 | CSV四视角；输入比例与目标比例反例 | 长论文路线表按需；保能力下降与混杂条件，CPT不由名称决定目标 |
| llm-training-sft-rft | 协议策略、角色mask、轨迹准入、拒绝采样、偏好/教师与RL交接全部审阅 | mask的直接梯度与条件反传；筛选偏移 | DPO/OPD/PPO重复推导归后训练；结论按准入条件与失败信号精简 |
| llm-training-rl-evaluation | 闭环、CSV、批次、训练/交付指标、预算、症状与模型合同全部审阅 | 产物独立验收；初始化/额外投入两对照 | 删除重复算法全文，诊断表替代原则长段，实验计划不冒充执行结果 |
| training-methods-systems | LoRA、AdamW/Muon、超参/算例、优化器证据、分片、batch、规划全部审阅 | SGD→Momentum→Adam→AdamW；偏差修正；LoRA首步；polar反例；ZeRO/batch账本 | 论文效果与显存/FLOPs/带宽/通信分开；工业规划按需，未运行GPU配置明确标记 |
| rl-interview-guide | 符号、算法卡、数值卡、参数影响、诊断、短答与历史入口全部审阅 | 关键目标与作用；完整推导定位后训练 | 修G/KL方向/显存/epochs矛盾；合并重复长讲，现代RLVR/Agentic/OPD覆盖保留 |
| agentic-rl-guide | 问题、改动位置、局部信用、任务差异、研究证据与限制全部审阅 | 局部优势与重复状态例 | GRPO与配置重复归主讲；修同名SAPO、跨prompt归一与规则不可hack等断言 |
| agent-harness-guide | runtime、工具、权限、并发恢复、context/换窗、memory与交接全部审阅 | 两固定源码图；压缩/reset/history与V1/V2流程 | 修pruning归属/非通用预算；六原模板与用户原稿下载保留；训练配方与无来源性能移出 |
| transformer-decoder-flow | 公式/形状、cache/mask、参数账本与完整小模型全部审阅 | NLL/attention；整段/逐token/多token缓存等价 | 修Llama3头型、SwiGLU计数、双shift、初始化/cache/device/mask；PyTorch2.8 CPU实现运行通过，非性能实验 |
| distributed-training-guide | DeepSpeed/FSDP/Accelerate/MCore、LoRA、状态/通信与诊断全部审阅 | 固定进程组；分片/完整配置与恢复 | 删除无出处倍数排名；GPU示例未执行，框架代际与版本保留 |
| rl-interview-guide-legacy | 冻结历史正文，只提供查证入口与统一数学加载 | 原六张SVG与原推导保留 | 源正文未重编；现代讲解用带纠错注释的适配图，历史错误不升为现行知识 |

## 检索、规划与权限：4源合入1主题

| 唯一源 | 逐节编辑判断 | 原理 / 算例 | 减法与保留 |
| --- | --- | --- | --- |
| agent-systems/index | 三职责引入、科学关联、掌握清单 | 证据/决策/执行约束关系 | 去旧目录与重复路线；父页只装配不复制正文 |
| s01_rag_retrieval | 对象、索引、检索、Agentic、分层评测、论文结果、追问、来源全部审阅 | BM25饱和/长度项；单位向量与cosine；两路RRF；Recall/MRR | 删除第二幅同义总流程；索引经验分点；保留Faiss固定提交与未运行状态、PROGRESS退化/成本边界 |
| s02_planning_compute | 策略、搜索、验证、环境、预算、对照、论文结果、来源全部审阅 | 独立失败概率→BoN；selector条件成功；UCT两分支；净收益教学例 | 去重复总流程和pass@k组合长讲；分支状态与副作用图、停止表替代原则段；保留Search-R1++下降项 |
| s03_trust_safety | 威胁模型、隔离、科学边界、评测、CaMeL、追问与来源全部审阅 | clean/attacked utility、全部/条件ASR分母例 | 六模式表按需；科学约束分点；保留参数门控/TOCTOU边界和论文条件，不提升为部署安全保证 |

## 任务生产与独立评测：5源合入1主题

| 唯一源 | 逐节编辑判断 | 原理 / 算例 | 减法与保留 |
| --- | --- | --- | --- |
| agent-data-benchmarks/index | 生命周期引入、对象职责、正文装配、掌握清单、原始来源 | 来源/环境/任务/verifier/多轨迹/留出关系 | 去旧四章目录与第二路线；52引用编号不改、清单按需 |
| s01_task_synthesis | 对象、12路线、合同、科学检查、工业生成、准入、履历、EvoSyn、实验全部审阅 | 绝对+相对容差两尺度例；相对repair reward例 | 路线按缺口分组、长表按需；移除GRPO重复长讲；保留原SVG可放大、规模分母、负控制、履历证据边界 |
| s03_scientific_task_family | 来源冲突、任务族、统计、输出、verifier、切分、轨迹、追问、来源全部审阅 | NB均值/方差；offset；8×5配对design；contrast消供体项；raw比4而log2FC=1；BH四检验 | 去第二同义总图；来源树改有分支的机制图；科学schema、许可与方法差异保留；未下载/未执行/容差未冻结状态不变 |
| s04_cluster_training_evaluation | 实验、异质信号、长度、角色、测量、失败、门槛、来源全部审阅 | 配对胜负→差分→标准误/区间；研究组bootstrap步骤；设备小时例 | 双A–E改6独立比较轴，下载JSON同步；步骤信用/采样拆组；GRPO与KV长算归唯一主讲；集群长配置按需 |
| s02_benchmark_map | 测量对象、版本、各领域、指标、SkillsBench、选择全部审阅 | pass@k/pass^k独立式；不放回失败组合→有限样本估计；n5/c2/k2=0.7 | 指标先讲，完整版本/领域名录按需；成功成本只短回顾；保留原表、未复现说明和费用子集分母 |

## 推理服务与成本：4源合入1主题

| 唯一源 | 逐节编辑判断 | 原理 / 算例 | 减法与保留 |
| --- | --- | --- | --- |
| llm-serving/index | 调度/加速/成本三问题、装配、掌握清单、固定实现 | 请求计算与状态交接 | 去旧三章目录与重复研究路线；实现版本说明保留 |
| s01_runtime_scheduling | 阶段、分页、prefix、实现、混合状态、对照、来源全部审阅 | 连续批处理三轮；35token/16槽分页；逻辑→物理映射；两请求共享32prefix例 | 去第二同义总图；prefix条件分点、瓶颈诊断表；固定vLLM/SGLang源码与未运行范围保留 |
| s02_parallel_quantization | 并行、PD、量化、投机、规划、来源全部审阅 | GiB/GB传输下界；舍入/饱和误差；接受min(p,q)→残差→p；三词表质量；提交长度/真实加速例 | 工业规划按需；MTP、贪心/采样和量化target边界保留；原论文收益不当本地测量 |
| s03_capacity_cost | 账本、70B例、指标、rollout、成本、协议、来源全部审阅 | 唯一物理槽/本地head账本；70B/TP4/32K逐维；TTFT/ITL/TPOT时间例；Little稳定条件；全部尝试资源/成功 | 去第二总图；资源不能跨单位直接相加、费用避免重复；CSV/JSON规划不冒充实测 |

本批数值已用Python标准库复算；投机接受/残差用有理数验证最终质量等于target。
BH adjusted p为0.012、0.04、0.053333、0.2；
配对标准误0.0447665；这些均为教学算例，不是模型或科学实验。

构建检查：107 HTML / 303公开文件通过，引用1099 source/version项通过。
本批Chrome三主题×三屏9项通过，全部details展开、外CDN阻断；
数学输出40/33/37，0错误/未渲染/伪公式/整页溢出/内部坏链。
10旧章深链与4无JSfallback通过，两项扩展集成测试48.052s通过。
手机截图实际查看后，dense/contrast公式已拆行；容量公式专项通过：
公式259.89px、可用314px、0错误，新截图已查看。

## 研究地图：8源合入1连续主题

| 唯一源 | 逐节编辑判断 | 展开 / 算例 | 减法与保留 |
| --- | --- | --- | --- |
| llm-research-map-2026/index | 研究问题、证据层次、先修、七节装配、选题、归档与来源全部审阅 | 机制→对照→边界；掌握检查 | 移除旧覆盖表、三路线和七章重复目录；71原编号、15原件、SHA/许可说明保留；长来源/选题按需 |
| s01_agent_data_bench | 资产、四路线、Harbor交接、迁移、榜单审计、实验、定量入口全部审阅 | SQLite临时状态未交接反例；父span/请求0.05与0.10计费例 | 通用对象/合同表归任务主讲；四路线只讲生成空间区别，长实验按需；82/6627困难切片、19/20修复分歧及未重放状态保留 |
| s02_agentic_rl | 四维目标、三算法、信用五路线、异质性、异步、追踪、消融、证据全部审阅 | 等派发但有效组99.2/7.7→中等域92.8%例 | GRPO/GSPO/CISPO重复公式及有效组概率长推导归后训练；保留RLDS/KnowGPO/GiGPO/SAPO/SAMPO具体差别、反思/因果边界、三种异步偏差 |
| s06_architecture_landscape | 比较轴、九家族、状态、Qwen/Kimi/Nemotron/GLM/MiniMax/MiMo/Step/Gemma、闭源、实验全部审阅 | GDN标量→KDA通道gate；AD≠DA矩阵例；实际层数与独立服务测量 | 大规格表/实验按需；模型要点分点；NVFP4失稳切BF16无效、Step迭代精度反例、GLM随机token负载及型号例外保留 |
| s03_base_architecture | 版本、CED、CSA2、FP4/890B、replay、Engram、mHC/MoE、家族与负载全部审阅 | C/Z张量来源；百万历史首次扫描与16384候选；entry→2.5entry/token→890B逐项 | 重复memory分类/episode总时间式移出；原4SVG及放大保留；encoder/decoder replay近似、HBM/host不同口径不相乘；短轮成本列表 |
| s07_architecture_training | 残差、latent专家、工业Muon、精度、深度、Agent对齐、独立实验、来源全部审阅 | AttnRes得分→权重→原表示读取及(0.5,3)例；双随机凸组合范数推导与差异缩半；16→4MiB同分派；递归状态1/1.5/1.75 | 基础Muon与LatentMoE公式归训练/架构；新机制必要过程默认展开；完整工业参数分工、矩阵切片边界、Single-Pass20d→10d限制及原SVG保留 |
| s04_inference_diffusion | 四成本目标、三drafter、采样合同、准入、OPD角色、两论文表与实验全部审阅 | 周期90ms/5token=18ms与AR15ms反例；丢弃B后q=p仍全部A的调度反例 | 标准投机校正与成功成本长式归服务；并发1→128退化保留；温度/块长/τ/加速分开，独立trainer成本及未知硬件不省略 |
| s05_agent_frontiers | GUI、科学三层、Skills版本、适配、并行/多教师、实验全部审阅 | 时间t→冻结→新任务→旧回归图；测试标签泄漏反例；20s串行/13s并行但资源20s例 | 删除第二幅同义总流程；运行memory定义归Harness，研究干预要点分点；所有版本、预算、公开履历与待执行边界保留 |

核验：构建107 HTML/303文件通过，引用1099 source/version项通过；
扩展长章/精确归档两项集成测试48.493s通过。
Chrome390/768/1440，全部details展开、外CDN阻断；每屏30个数学输出，
0pageerror/TeX错误/直接显示式缺失/裸露TeX/伪公式/整体溢出/坏链接。
7旧子章fragment正确定位且展开，2无JS正文/fallback通过。
报告`/tmp/my-blogs-browser-tests/learning-research.json`，源码runner同名js。
手机AttnRes与GDN/KDA实际截图已查看，公式完整可读、图可打开原SVG。

此次截图发现原检查“容器有任意后代数学节点”会漏掉HTML吞入后续段落的坏公式：
求和`j<l`与深度`j<K`中的裸`<`被HTML解释为标签。
已改为TeX `\lt`，验收改为直接display节点＋非数学/代码区域裸TeX扫描；
首次报告28个输出的通过结果作废，修正后30个输出才是本批最终结果。
F全站检查必须沿用这一更严格的实际验收，早批次仍需按此复验。

## DLM：15源合入1连续主题

| 唯一源 | 逐节审阅与编辑判断 | 展开 / 算例 | 减法与保留 |
| --- | --- | --- | --- |
| dlm-survey/index | 范围、分类、路径、先修、原稿、装配、掌握清单 | 训练/生成两支路 | 移除旧目录、重复路线与厂商速度结论；14节正文在同页，先修/扩展折叠 |
| s01_overview | 动机、五分类轴、四token路径、现代路线、追问、来源 | AR位置依赖与扩散状态依赖 | 修正“AR训练串行”“双向保证规划/无reversal”；删除第二课程路径与跨厂商排名 |
| s05_paradigms | 连续三目标、score、SEDD、DFM、对照、追问全部审阅 | VP旋转/逆变换数值例；MSE时间权重；score条件期望；ratio散度导数；两状态master例 | 修正epsilon低噪声归零、VP-v=FM、SEDD缺r项/比率softmax；DFM纠错后ID保留；旧错误冻结全文移到原稿 |
| s02_discrete | D3PM、贝叶斯、VLB、MDLM、LLaDA、Dream/Seed/适配、SEDD、对偶全部审阅 | 行向量Bayes；吸收揭示0.6/0.4；SUBS后验KL→CE→连续权重；t0.25/0.75；对称argmax边际 | 线性weight修正1/t；可见token梯度、remasking/carry-over与GQA/cache分开；LLaDA原论文配方保留；无条件历史数字与错误CART/CTMC公式移出当前正文 |
| s03_block | 因子化、插值、训练、cache、SSD-LM、适配、SFT/BlockGen、drafter、混合模式、Fast-dLLM全部审阅 | 4token两块mask；clean/noisy泄漏；128token/16块/4轮与32块/8轮 | 删除伪单调定理、虚构simplex Gaussian、重复DFlash数值；精确因子化不等于块边际精确；保留现代路线与cache充分条件 |
| s04_continuous | 三接口、Diffusion-LM、COLA、CADD、ELF、CCDD、LangFlow、TextLDM、Plaid全部审阅 | −1→3路径t0.25；两token embedding均值与CE反例；重建/生成/任务三检查 | 删除一般MSE=CE、任意RAE稳定、全域20x；时间符号统一，型号仅保留研究接口/需核对字段 |
| s08_elbo_rl | 原14节的界、SPG/GDSD、d1、偏好/轨迹/方差、uniform迁移全部审阅 | denoiser/path/marginal；Jensen gap；三误差；SPG正负例；指数倾斜0.7311；冻结centered-score目标 | 保留SPG v1四任务数据；删除与现代修订冲突的重复SPG公式、无条件梯度方差倍率、Gaussian投影精确文本概率、uniform迁移保证；未核实命名/题号明确仅线索 |
| s06_scaling | scaling、过拟合、熵调度、四数据研究、噪声核、Beyond、对照全部审阅 | U/D/E/C独立变量；compute约束导数→最优幂；1B×100复用 | 修正N∝sqrt(D)、宽浅推断与过拟合有益；去513/32通用上限与无来源贡献百分比；原研究入口保留 |
| s07_speculative | 基础、DFlash/MTP、接受率、发散、训练、时间线、轨迹/自身加速全部审阅 | 尾和期望；a0.8/b4→2.3616；8+25+2ms/5→7ms/token | 标准精确校正归服务；原KL/概率乘积/速度上界错误移除；DFlash/DSpark/AdaFlash长结果唯一维护在研究地图 |
| s10_comparison | 全方法、RL、理论对比、未来四方向全部审阅 | 五路线收益/成本；五项共同合同；四单轴研究设计；六问短答 | 删除第三套SPG/GDSD、1/TV速度上界、连续全域更强与跨论文RL百分比；方法细节回同页已有解释 |
| s11_loop_transformer | 原10节直觉/理论/复杂度/扩散类比/Ouro/CCDD/latent/现代架构/索引/启示全部审阅 | kP/krF；共享theta梯度和Jacobian乘积；0.5h+1稳定/2h+1发散；8元素结合组合 | 移除无条件复杂度严格分离、答案变化证明忠实、所有循环上限4–8；路线/失败与研究问题保留，未核实大表回精确原稿 |
| s00a_ddpm | 模型→Jensen→裂项→后验→noise loss→采样全部审阅 | 前向方差递推；t≥2裂项；精度α/β、A14/variance1/14/mean0.89443；固定方差MSE | 修正漏α、连续q(x0|x0)=1、有限逆边缘精确Gaussian、simple=ELBO、末步投影数据流形；必要五步推导保留 |
| s00b_flow_sde | 时间、ODE/SDE、路径、条件/边际、score、PF、OT、DDPM连接、训练、求解器与原附录A–F全部审阅 | 条件速度；方差分解证明；test-function连续性；Ito/FP；score抵消；VP极限与逆SDE | 删除独立配对自动OT、一/少步必然、所有loss/网络等价；明确生成/前向时间、理想边际vs路径、空间无关g条件 |
| s12_vae | ELBO、三失败、发展/18变体、VQ/RQ/FSQ/LFQ、层级、现代系统、ACT、联合训练全部审阅 | KL0.81815；重参数梯度；VQ0.8→1两职责；RQ1.3→1.25；25/2^d组合；512图像→latent1/48 | 修正VQ无法绕过、无码本无退化、RQ同token数、LlamaGen/RQ/Sora/Parti归属和ACT prior均值保证；连续/层级家族表与来源保留 |
| s09_commercial | 厂商、Gemini/DiffusionGemma、Mercury、吞吐/成本、Pareto、部署指标全部审阅 | 200ms提交100token：500tok/s但首字200ms | 产品研究/服务版本分开；去1008/1196/1479/2146跨设备排名、当前商业/授权全称保证与永久速度护城河 |

核心定义重新查看MDLM v2、LLaDA v2与BD3-LM v1原论文；
LLaDA v2式3确认1/t，§2.2确认8B配方；BD3-LM明确block1期望目标等价但估计方差仍有差距。
新增/原算例用标准库复算DDPM posterior、VAE KL和接受长度；不代表模型训练。

最终构建107 HTML/303公开文件通过，引用1103 source/version项通过。
DLM的15个ledger理由已逐项更新，SHA/基线单元未重建。
Chrome390/768/1440全部details展开、外部CDN阻断，每屏131个数学输出；
0pageerror/TeX错误/直接display缺失/裸TeX/伪式/整体溢出/实际数学SVG超宽/坏链接。
14旧子章deep link均定位并展开目标；2无JS正文/手动fallback通过。
报告与runner：`/tmp/my-blogs-browser-tests/learning-dlm.json`、同名js。
手机SUBS/加权MLM与DDPM精度/后验新截图已实际查看，分行完整可读。

本轮另一验收漏洞：display mjx自身overflow容器使reading-math.scrollWidth不变，
实际SVG仍可更宽而右端裁切。新增SVG实际bounding width与可用容器宽度比较。
最初128/129数学输出报告不作为最终通过；分行与DLM阅读边距修正后131输出复验有效。
F需对前批同样检查实际公式图形宽度，不能仅看整页或reading-math宽度。

## 综合题库与VLM：2源逐节重编

| 唯一源 | 逐节编辑判断 | 展开 / 实现 | 减法与保留 |
| --- | --- | --- | --- |
| llm-interview-bank/index | 470问的11领域全部审阅：LLM、偏好、RL、Agentic、VLM、Agent、RAG、服务、代码、评测、开放题；155旧答核对口径 | 90卡全部附短答与追问；KL/DPO关键式，SFT/GQA/Norm/RoPE/LoRA/DPO/PPO/GAE/group/采样完整教学代码，online-softmax与经典算法不变量 | 合并同义问、删除无来源频率/公司排名；全470原问及旧答逐字归档，旧公开锚点保留；完整PG/GAE/GRPO推导与六论文数值配方归唯一主讲 |
| vlm-knowledge-interview/index | 六部分全部审阅：核心表示与目标、前沿路线、11问、3组代码、来源、掌握清单 | patch/MLP/query形状与参数；CLIP/SigLIP梯度和两对算例；视觉条件反传；tiling/merge/视频预算；crop坐标；VCD、ColPali MaxSim；完整patch/projector/resampler/mask/tiling | 删除跨论文榜单/无出处倍数，代表路线按需；修正336/14=576、SigLIP负例通信/O(N)、MLP最优/统一四阶段、M-RoPE三等分、VCD无图对比、不同图像不可互看及max12却15tiles；精确原稿和全部原链接继续保留 |

代码验证：PyTorch2.8.0 CPU，SFT shift与mask梯度、GQA/SDPA等价及未来value隔离、
RoPE范数、LoRA首步A/B梯度、GAE terminal、全同奖励组、DPO梯度符号、
Top-P首跨阈值、K1/K3精确期望、三长宽比tiling/预算、块mask、patch/query形状、
20,979,712参数、CLIP score导数及双塔梯度，共8组检查通过。
报告与runner为`/tmp/my-blogs-browser-tests/learning-bank-vlm-code.json`和同名py。
未依赖NumPy、未运行GPU或模型性能/科学实验。

最终构建107HTML/303files与引用1103项通过。
Chrome两页×390/768/1440，全部details展开、外CDN阻断：
题库2、VLM10数学输出，0error/TeX错误/直接display缺失/rawTeX/伪式/
整页溢出/实际SVG超宽/页内坏链；RoPE筛选命中4/90卡，展开/收起通过。
2无JS原生答案展开与正文可读通过；手机CLIP与题库实际截图已查看。
报告`/tmp/my-blogs-browser-tests/learning-bank-vlm.json`；同名js为runner。
手机长式分行后最终通过，早期含wideMath结果均不作为验收通过。
两页ledger真实理由及迁移精确SHA已更新，没有重建baseline或原稿SHA。

## 前沿追踪与Harbor：2源逐节重编

| 唯一源 | 逐节编辑判断 | 展开 / 验收 | 减法与保留 |
| --- | --- | --- | --- |
| llm-frontier-2026/index | 14节含模型、架构、优化器、Agent、RL、OPD、训练、评测、蛋白、证据与日志全部审阅 | 改动位置→比较条件；五个判断追问；polar有限近似、Clip-Higher与行为校正、教师接口边界 | 型号/许可证快照与原维护日志按需；收敛Muon/RL/OPD主讲，旧TB排名改历史；移除无共同条件榜单、领域CoT普遍结论，修正百万碱基单位。AUTO标记、原日期、last-updated与原稿逐字归档保持 |
| harbor-framework-guide/index | 13节与scalingX17集全部审阅；版本、计数、源码、canary与未运行状态核对 | observed/native/ambient/corrected counts→移除比例/归一误差→oracle gap；误收/误拒净值与分母；reward_valid均值；五个机制追问 | 删除重复目录与两次同义总结，长版本表按需；科学数学从代码框移到默认正文；Index筛选改机制图；三原执行图默认可见，600px限宽不变形且可放大；真实案例与计数/去重边界保留 |

make check107HTML/303files通过。两页×390/768/1440，全部details展开、外CDN阻断：
数学输出5/17，0error/TeX错误/直接display缺失/rawTeX/伪式/整页溢出/实际SVG超宽/坏链。
两项无JS正文和原生details通过；Harbor三屏图放大/ESC关闭通过。
手机scientific counts/oracle gap与有效奖励截图已查看；公式分行完整可读。
报告与runner：`/tmp/my-blogs-browser-tests/learning-frontier-harbor.json`与同名js。
首次390px A校正式323.42px超过314px结果不算通过，增加污染中间量后复验通过。
构建发现旧reading-intro别名与真实入口冲突，reading.py已排除生成入口ID；全测试留待F。
尚余MyWork8源与F，不将本批通过写成全站或科学实验通过。

## My Work：四导读与两完整报告

| 唯一源 | 逐节编辑判断 | 展开 / 算例 | 精简与证据 |
| --- | --- | --- | --- |
| my-work-holon/index | 表示→MoT→数据/监督→token校准→预算→Ladder→工作复盘全部审阅 | routed Q/attention、CE分母反例、产出校准与两流例、C/M、DiD | 修正 margin 为 mismatch−match，保 checkpoint/CI/单seed/OOD边界；五追问，机制图可放大 |
| my-work-protagent/index | 工具→SFT→return→reward→四臂→主模型→训练全部审阅 | assistant mask、轨迹score-function、token surrogate、重复调用信用 | 区分原始无偏梯度与处理后advantage；保四臂61.4与指定61.0、PFUA独立、recall>0.5；五追问 |
| my-work-harbor/index | 来源→合同→oracle→门禁→refinement→历史规模全部审阅 | A=(1,10)/B=(2,20)混拼反例、完整路径集合、pass@k补事件 | 剪重复链路，用短要点说明接受门；v4反事实与accepted=0保留，历史库存不除作匹配率；五追问 |
| my-work-dllm/index | 目标→mask→Jigsaw→任务→LM1B→复现全部审阅 | AR/MDM/block目标、熵与ICL终点 | 保 side/offset具体规则和监督密度、top-p混合与缺日志；五追问 |
| my-work-protagent/full-report | 13节全部审阅 | 对数导数→去过去奖→step return→策略token，reward guard与全样本分母 | 四臂/配方同义表合并；原3SVG保持比，可放大；逐seed/阈值/γλ/PFUA表及来源保留；不再克隆导读三节 |
| my-work-dllm/full-report | 全章节审阅 | AR/吸收/块目标；ICL二次型配方、rank风险例；三OR mask；熵与affinity | 修概念mask套用LM1B的错误；CLI按需，原3图保持比可放大；ARR表/SEDD差异/smoke范围保留 |

六页×三屏，全部details展开、断外CDN：数学6/4/2/4/7/10，0error/rawTeX/
直接display缺失/伪式/实际公式SVG超宽/整体溢出/坏链接/机制图超宽。
30项机制/研究图放大与ESC、6项无JS正文检查通过；
手机ICL、PG与Holon交互效应截图已查看。
首次dLLM两式411.81/407.28px超358px不算通过，分行后有效复验；
新增机制图检查发现旧840px最小宽及ProtAgent680px最小宽造成内裁切，
已按原比例缩放并提供放大，不能仅用整体overflow判断图是否完整。
报告与runner为`/tmp/my-blogs-browser-tests/learning-my-work.json`与同名js。
以上批次记录覆盖当时72源；下述两报告完成后，全74源已有逐页判断。全站F验收仍须单独通过。

## My Work：两份方法报告

| 唯一源 | 逐节编辑判断 | 展开 / 算例 | 精简与证据 |
| --- | --- | --- | --- |
| my-work-holon-full | 21节正文审阅：MoT/参数、配置/packing/loss、数据、配比、scaling、优化器、CPT、scoring、基准、完整结果、Ladder、C30、WT/FIM、SFT、结构、生成、探索、复盘、源码与来源 | token/modality reducer 2:8例；mask后监督与长度权重；拒绝采样分布；fetch/预算/coverage；polar反例；DiD逐步相减 | 核心学习定位与五追问；修PSC跨tier/绝对margin混淆与残留强调标记，分点复盘；原图保持比例可放大，手机图min-width裁切修正。保固定7de0f4版本、完整原表、源文档/样例与逐字原件；长源表未逐格复算、无GPU/科学实验 |
| my-work-harbor-full | 原方法、角色、rubric、早评、八类失败、路径判分、包目录、CRISPR例、历史规模、对比、工程选择、成本与追问全部审阅 | 完整路径联合接受与混拼反例；批次分母；全部尝试成本；固定c/p算例与85.7% | 合并三处重复总结/两规模表/第二链路；原对比与费用按需，历史79%与固定成本85.7%分开；原流程图可放大。保0efe0d版本、77,441×10案例、角色与原库存，不推断因果；refinement drop=0/accepted=0边界保留，无任务生成/盲测执行 |

## 全74源最终验收

本表的74份逐页判断与 `organization-changes-20261115.json`、
`content-changes.json` 的当前精确SHA/理由一致。两个基线未重建，原件字节未修改。
`blog-learning-validation-20261115.json` 按每个catalog ID记录知识编辑、
当前主讲位置、三屏公式/图表/链接、源片段、旧fragment、无JS、精确原件和复核状态。

最终覆盖26实际阅读页及48装配片段：390/768/1440共222源检查，
144旧fragment、74无JS、63图放大/ESC和全部17隔离集成用例通过。
八共享入口的24三屏检查、关键词去重/首次点击/返回前进、目录失败降级、
数学本地加载/失败重试和键盘导航通过。九份完整手机公式截图已实际查看。

严格验收发现的超宽公式已逐式重排；PG/OPD短符号、loss目标数、
KV/LoRA维度、FFN/Jacobian、AdamW/Muon/显存、配对SE与RoPE均保留完整关系。
结论与经验继续按重点、比较、故障信号和短答组织。首次搜索点击与details
自目标展开问题也已修复；早期失败结果不计入最终通过。

完整证据、复现命令与验证边界见 `blog-learning-rework-checkpoint-20261115.md`
末尾“F最终验收”。内容阅读验收不等同于科学实验或论文性能复现。
