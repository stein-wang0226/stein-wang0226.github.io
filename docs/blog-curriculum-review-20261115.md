# 分类与学习内容复查 · 2026-11-15

基于 `7392b5c51784230aef0d8809bebabef02219cb15`，承接同日结构补充。
本轮复查全部74份唯一内容源的主题归属、章节顺序、主讲边界、机制图与例子入口；
对下表标为“修改”的正文逐段核对新内容与来源。保留既有原稿及74源原审阅记录，
不把此前的浏览器结果作为本轮发布验收。未修改页不声称重新核验了每条历史外部资料。

## 本轮组织结果

- 一级主题按模型架构、训练、推理、数据排列，Agent、多模态和扩散作为专门方向。
- 训练阶段是纵轴；算法、预算、优化器、框架与执行是横轴。四类知识目录与长章共用内容源。
- 主讲、题库、实现参考、研究增量各有职责；筛选同时检查子章节与次主题，
  避免研究地图中的架构内容、训练页中的数据内容在分类后消失。
- 旧训练分类保留别名；旧章节链接继续定位长章锚点。未复制正文创建新的主题页面。

## 逐源判断

| 唯一源 | 处理 | 本轮判断与复查对象 |
| --- | --- | --- |
| my-work-holon | 保留 | MoT→数据目标→条件利用→评测；项目结果与通用训练原理有清晰分工，保留配对干预算例 |
| my-work-protagent | 保留 | 工具轨迹→监督→逐步信用→独立评价；保留真实工具、奖励分母和四臂实验边界 |
| my-work-harbor | 保留 | 合同→多路径oracle→盲测→失败归因；分类迁至数据，科学要求与历史生产量分开 |
| my-work-dllm | 保留 | 调度、attention与loss分别讲解；两块算例和训练可见性符合项目主线 |
| my-work-holon-full | 保留 | 长研究报告保留证据与历史材料；学习摘要承担快速入口，不复制实验结论到通用教材 |
| my-work-protagent-full | 保留 | 保留配置、原始seed与逐步回报细节；与摘要按深度分工，不改实验分母 |
| my-work-harbor-full | 保留 | 保留原稿方法汇报、合同和历史记录；成本仍标估算与未刷新价格 |
| my-work-dllm-full | 保留 | 保留ICL、ARR、路径与LM1B机制；已明确概念层与具体backbone的attention差别 |
| agent-systems | 保留 | 检索、规划、权限三章连续阅读；与Harness运行循环边界清楚 |
| agent-rag | 保留 | BM25→dense→RRF→Agentic检索；有推导、数例与分层评测，不补重复模型列表 |
| agent-planning | 保留 | 候选存在性、选择器、UCT与状态分支依次展开；保留Search-R1++分项退化 |
| agent-trust | 保留 | 控制面、数据面、权限和隔离有机制图；保留CaMeL攻击集分母及效用未知项 |
| llm-serving | 保留 | 调度→精度/并行→容量/成本主线明确；一级分类由训练推理合并项拆为推理 |
| serving-runtime | 修改 | 增补Kimi K3.1索引→候选→潜在KV读取图、每层流量公式及GB300单请求TTFT；区别读取与容量 |
| serving-parallel | 保留 | PD传输下界、量化舍入/饱和、投机精确性与速度算例完整；不用架构活跃参数代替部署容量 |
| serving-capacity | 保留 | 70B容量、延迟分母、Little定律及成功成本连贯；规划表保持无实测状态 |
| llm-posttraining | 修改 | 修正过时来源数量说明，登记11月OPD补充；保留原理→变体→配方→诊断顺序 |
| posttraining-supervision | 保留 | SFT mask、轨迹恢复、拒绝采样、DPO推导集中；训练阶段页只负责交接 |
| posttraining-algorithms | 保留 | PG/GAE/PPO/GRPO推导、六论文数值配方与追问完整；保留mini-batch和epochs区别 |
| posttraining-opd | 修改 | 在多教师/自蒸馏原节加入Agentic-OPD与ECOS；核对top-k、验证切分、命令监督、遗忘与额外成本 |
| posttraining-rewards | 保留 | 环境→反馈类型→过程监督→多步信用；PURE反例与2026信用分配已有独立机制和证据 |
| posttraining-frameworks | 保留 | 同步/异步及三类偏移、固定源码和12类框架保持；TorchForge迁入TorchTitan状态已有说明 |
| posttraining-cases | 保留 | 代码、科学、GUI三条完整轨迹连接目标和验证；待执行对照不写成已测结果 |
| training-methods-systems | 修改 | 完整保留AdamW/Muon推导；补四层训练架构、TorchTitan/MaxText固定源码、框架验收、roofline和nGPT整套配方证据 |
| scientific-task-family | 保留 | 来源→统计单位→NB/contrast/BH→verifier→切分；算例与数据角色已清晰 |
| cluster-training-evaluation | 保留 | 算法、预算、集群和配对统计分开；增加数据次主题归属，规划仍不声称运行 |
| llm-architecture | 保留 | 张量→Attention→FFN/MoE→残差→混合状态→比较；保留单一连续目录 |
| architecture-transformer | 保留 | token至logits、causal mask、shift与四种状态对应；基础张量链路已有图 |
| architecture-attention | 保留 | 缩放、GQA、KV字节、RoPE、Flash/Paged职责分开；Kimi Linear同预算数据保留反例 |
| architecture-moe | 保留 | FFN账本、router、容量、通信与LatentMoE串联；不能由激活参数比例推速度 |
| architecture-residual | 保留 | Pre/Post Norm梯度、RMSNorm算例与mHC受控结果清楚；不复制优化器推导 |
| architecture-hybrid | 保留 | 外积→遗忘→delta→Mamba/SSD→混合层与恢复；矩阵转置约定已解释 |
| architecture-comparison | 保留 | 六条比较轴与共同实验协议汇总；将型号细节留在研究家族表 |
| agent-data-benchmarks | 保留 | 数据生产、任务、轨迹、独立benchmark的关系有图；归入数据主题 |
| agent-task-synthesis | 保留 | 12条合成路线→合同→数值容差→轨迹准入；跨阶段数据用途已展开 |
| agent-benchmark-map | 保留 | pass@k组合推导、版本、领域与成本分母齐全；不把滚动榜单抄入各章 |
| llm-research-map-2026 | 保留 | 七章按研究问题维护新机制；通过子章节主题筛选可从架构/训练/推理/数据找到相关部分 |
| research-agent-data | 保留 | 合成空间、环境迁移和验证重放是增量主题；与任务合成主讲分工明确 |
| research-agentic-rl | 保留 | 更新对象、信用、异质数据、异步偏移四维组织；完整算法推导仍归后训练 |
| research-base-architecture | 保留 | V4.1版本→CED→CSA2→字节→replay；保留890B/token口径和查表参数分拆 |
| research-inference-diffusion | 保留 | DFlash/DSpark/AdaFlash分别改变候选、训练和调度；保留选择偏差反例及并发对照 |
| research-agent-frontiers | 保留 | GUI/科学/skills/memory与持续适配分层；保留时间切分和并行资源算例 |
| research-architecture-landscape | 修改 | 增补经典→前沿学习图和四类目录关系；Kimi连接新服务字节/TTFT证据，九家族固定版本规格保持 |
| research-architecture-training | 保留 | 残差、LatentMoE、Muon、精度、递归计算分对象讲解；增加模型架构次主题，不复制更新公式 |
| llm-training-lifecycle | 修改 | 增加阶段×目标/数据×预算×执行交叉表；连接Scaling、优化器与框架主讲，引用CS336及Smol课程组织 |
| llm-training-pretraining | 修改 | 补固定算力最优解、IsoFLOP/scaling ladder、μP/WSD机制与图；新增混合token、重复倍数与目标占比算例 |
| llm-training-midtraining | 保留 | 阶段定义、固定SFT受控证据、CSV视角、回放与目标权重完整；数据次主题与训练入口共用正文 |
| llm-training-sft-rft | 保留 | 保留角色mask、筛选与交接；DPO和OPD推导指向唯一主讲，避免重复 |
| llm-training-rl-evaluation | 保留 | CSV误删0反例、策略版本、训练/交付指标及预算对照清晰 |
| llm-frontier-2026 | 修改 | 精简旧MiniMax混合性能概括并转主讲证据；跨主题可检索，动态追踪与基础教材分工保持 |
| agentic-rl-guide | 保留 | 按五个研究问题比较方法，保留局部信用例；基础推导不回填到速览 |
| dlm-survey | 保留 | 概览→目标→离散/块→连续→ELBO/RL→Scaling/解码；先修与商业分支按需展开 |
| transformer-decoder-flow | 保留 | 公式、代码对象与缓存等价性对应；作为实现参考，不复制为第二架构长章 |
| rl-interview-guide | 保留 | 短答、参数、诊断与追问卡；详细推导及修订六图在主讲，历史原稿入口保持 |
| agent-harness-guide | 保留 | 执行→状态→上下文→记忆→恢复链路完整；Codex原稿和六模板保持 |
| distributed-training-guide | 保留 | DeepSpeed/FSDP/Megatron接口与诊断定位；状态推导归训练主讲 |
| llm-interview-bank | 修改 | 补Scaling ladder/μP/WSD短答与边界并链接推导；增相关次主题，避免只在架构分类找到综合题库 |
| vlm-knowledge-interview | 保留 | CLIP/SigLIP→connector→mask→视觉预算→评测；未闭合历史型号断言仍不作结论 |
| rl-interview-guide-legacy | 保留 | 历史原稿明确归档，只验入口和渲染；旧算法口径不冒充当前教材结论 |
| dlm-ddpm | 保留 | ELBO裂项、高斯后验与噪声重加权推导完整；先修不挡住主线 |
| dlm-flow-sde | 保留 | 条件到边际场、概率守恒、SDE/ODE按假设推进；保留端点与OT边界 |
| dlm-overview | 保留 | 四token例先解释生成状态，再介绍路线；适合作为DLM入口 |
| dlm-discrete | 保留 | Bayes→吸收核→KL到CE→LLaDA；1/t权重算例明确 |
| dlm-block | 保留 | 块间/块内循环、训练可见性和缓存充分条件分开；没有把mask名字当实现证明 |
| dlm-continuous | 保留 | 连续接口、路径方向、MSE/CE反例与三层误差；不恢复无来源统一倍数 |
| dlm-paradigms | 保留 | 预测坐标换算、时间权重、score与离散质量流；符号与对象齐全 |
| dlm-scaling | 保留 | 数据受限U/D/E与crossover为本节重点；保留短幂律推导，完整实验阶梯由训练主讲承担 |
| dlm-speculative | 保留 | AR drafter与DLM自身提速分开；尾和期望、周期时间和联合分布边界完整 |
| dlm-elbo-rl | 保留 | 边际/路径/下界分开，SPG符号与GDSD倾斜例清楚；不把ELBO差写成精确ratio |
| dlm-commercial | 保留 | 只解释产品证据与burst时延算例；定价与开放状态不冒充当日实测 |
| dlm-comparison | 保留 | 机制表、统一合同与六道复述题收束主线；避免堆历史无共同分母表 |
| dlm-loop-transformer | 保留 | hidden循环与噪声去除区分，参数复用不等于免费计算；理论条件明确 |
| dlm-vae | 保留 | 重参数化、高斯KL、VQ梯度及codec职责齐全；未闭合名称保持研究线索 |
| harbor-framework-guide | 保留 | 版本、执行、隔离、重评分、适配与任务研究分层；不刷新全部动态榜单或声称运行任务 |

## 新增内容的来源与核对范围

2026-11-15读取以下一手内容；课程仅借鉴组织方式，不把课程结构当技术实验来源。

- CS336 2026课程表：<https://cs336.stanford.edu/>。
- Smol Training Playbook目录与组织：<https://huggingfacetb-smol-training-playbook.hf.space/>。
- Kaplan及Chinchilla：<https://arxiv.org/abs/2001.08361v1>、<https://arxiv.org/html/2203.15556v1>；
  固定算力最优解是条件推导，没有新训练拟合。
- μTransfer v2及mup官方README：<https://arxiv.org/abs/2203.03466v2>、
  <https://github.com/microsoft/mup>；核对隐藏矩阵LR、base shapes、深度约束和coordinate check。
- MiniCPM：<https://arxiv.org/abs/2404.06395>、<https://openbmb.vercel.app/minicpm> §2.4；
  WSD分支与2.5%/10%观察限该沙盒实验。
- Roofline：<https://jax-ml.github.io/scaling-book/roofline/>；
  本文数字200、16、512为教学假设，没有设备测速。
- TorchTitan源码`631d544b1f6794ecfeca734a7bba861e03ddd5e3`、
  MaxText源码`538dcdd3e60865f80cf5c567f266a2abc1c7b6e4`：核对README职责、组件与版本边界。
- Training nGPT v2：<https://arxiv.org/html/2608.01284v2> §3–4/Table 1；
  整套参数化/训练方案与门控消融分开，6%开销不标成FLOPs。
- Agentic-OPD v1：<https://arxiv.org/html/2611.12799v1> §3–4/Table 1–2；
  核对HCN集合、LAD三级筛选、student top-k重归一化、测试与验证集、恢复60/遗忘45。
- ECOS v1：<https://arxiv.org/html/2611.12232v1> §3–4/Table 2–3；
  主结果与消融分母、训练seed与评测seed、SFT和额外在线耗时分开。
- Kimi K3.1工程报告：<https://vllm-project.github.io/2026/11/04/kimi-k31-pro.html>；
  核对FP8索引/潜在KV字节、层数、TP8单请求TTFT及token分片含义。

## 本轮验收

本轮验收完成。逐源SHA见 `blog-curriculum-review-20261115.json`，
机器验收明细见 `blog-curriculum-validation-20261115.json`；没有改写不可变基线。

- `make check OUTPUT=/tmp/my-blogs-structure-20261115`：107个HTML页面、303个公开文件通过。
- 引用登记：1119个来源/版本记录通过；本轮新增MiniMax原论文的使用位置同步登记。
- 74源 × 390/768/1440px：222项来源检查，装配为26个阅读页、78次页面检查；无公式错误、
  原始TeX泄漏、页面横向溢出、坏图片或重复H1。新Scaling导数及WSD分段式按手机宽度拆排后复验。
- 48个旧章节 × 三种宽度：144次旧片段跳转通过；74个地址的无JavaScript阅读通过；
  63次科研图放大/关闭通过。学习、面试及项目研究路径通过。
- 四类目录：12项三屏检查、20条实际点击及无脚本导航通过；11项分类/旧分类别名检查通过；
  4项新增次主题跳转及16项新章节视图检查通过。
- 已核看桌面目录、阶段交叉表、Kimi读取链路，及手机roofline、修正后的WSD公式截图。
- 数学复算：固定算力最优点、预算恒等式与相邻损失；数据目标占比；μP隐藏LR；
  Kimi每层读取与24层存储字节。仅为解析复算，没有训练性能复现。
- 集成套件首次16项通过、1项因Harbor项目地址误改失败；恢复两个
  `/my-work/harbor-task-sync/`原地址后，失败项独立重跑通过（67.483秒）。
  全部17项均取得通过结果，不将首次失败隐去。
- 前沿更新18项自动化测试及实际校验入口通过；原有追踪日期与目录日期一致。
- 最终保留检查：299个原锚点、59个原标记、199个登记路由通过；
  9项原SHA不变、32项历史累计变化有精确记录，数量不是本轮修改页数。

本轮没有执行GPU训练、服务benchmark或科学任务。九家族表保留固定版本来源；
未声称逐一刷新所有型号、动态榜单与商业价格。发布时以Actions结果、线上
`build-info.json`的提交及输入摘要，并与本次实际页面字节对照确认。
