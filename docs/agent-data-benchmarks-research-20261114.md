# 任务合成、评测体系与 DeepSeek 架构增补依据

调研日期：2026-11-14。新增内容服务于作者的学习笔记和公开履历关联；
论文实验、团队发布数字与作者简历声明分别标注。没有执行模型训练或 benchmark。

## 交付范围

- 深化现有 `llm-research-map-2026/s03_base_architecture.html`，保留 URL 和锚点。
  交付 CED 张量路径、CSA2 实际层计划、hierarchical indexer、FP4 格式、
  890 bytes/token 推导、SWA 两种 replay、mHC / MoE / Engram / 训练系统及比较图。
- 新系列 `agent-data-benchmarks` 两章：可执行任务合成；Agent benchmark 地图。
  经典 benchmark 分类速查，前沿体系重点分析，接入 catalog / 旧专题关联。
- 图表是基于规格的机制图和带出处的静态比较。没有编造训练曲线、
  跨硬件速度排名或 benchmark 统一难度分数。

## 已核实的架构规格

主要来源：DeepSeek `2609.19969v1`，§2.2–2.4、§3.1.2–3.2.2、§4.2.1；
官方归档 PDF 与 SHA 已在原 `assets/research/2026-11-14/sources.json`。

- 40 层，20 encoder + 20 decoder，hidden 5120。
- 前两层只有 SWA。其余 encoder 18 层：3 组 × 6，`Full, Reuse×5`，
  压缩比 m=2。decoder 20 层：5 组 × 4，第一组 `Full, Reuse×3`，
  其余四组 `Reindex, Reuse×3`，m=1。
- decoder Full global KV 来源于末层 encoder hidden：
  `C_l=H_20 W_l^KV`，压缩权重 `Z_l=H_20 W_l^Z`；
  本层 Q 和 SWA KV 仍来源于本层。C/Z 不是传统独立 K/V 两份存储。
- indexer 32 query heads ×128 channels；main Q 64 heads ×512，
  query compression 1280；SWA window128，attention top-k512。
- decoder 首 Full 全局扫描；按 block max 选最多2048个8位置block，
  候选池最多16384位置。后四个 Reindex 在池内选512；Reuse不重新索引。
  这是 decode 中的 decoder 优化，在 post-training 引入，并保持训练推理一致。
  首扫描仍 O(N)，不是整网 O(1)。
- main KV：512渠道 E2M1，每16值一个 E4M3 scale，省略标准 NVFP4 的
  第二级全局 scale；RoPE之后量化，post-training QAT，读时反量化。
  indexer K 使用 OCP MXFP4；SWA仍FP8。不要写成全模型FP4 GEMM。
- OCP MX v1.0 规格表确认 MXFP4：E2M1，32元素block，8-bit E8M0 scale。
  NVIDIA NVFP4 2025-06-24正文确认标准NVFP4还有per-tensor FP32 scale；
  DeepSeek省略该级，不能称完全相同布局。
- **规格推导，非实测**：main `512/2+512/16=288` B/entry；
  indexer `128/2+128/32=68` B/entry；总356 B/entry。
  encoder3组每2token一entry + decoder1组每token一entry：
  `(3/2+1)*(288+68)=890` B/token。长序列近似，不含尾部block、
  allocator、alignment、SWA、weights、Engram、workspace、分片复制。
- 原报告global HBM约前序1/4；persistent SSD/host约前序1/8。
  两个口径不可相乘1/32。persistent变小来自不保留长期SWA及global压缩。
- Encoder replay：global hit/SWA miss时重放cached prefix末128token，
  只补SWA，不覆盖cached global；uncached suffix同时产生两类state。
  仍有短TTL host pool（10% host DRAM）保留encoder SWA。
- Decoder replay：每次prefill把末128token的encoder outputs送过decoder，
  生成只用于decode的SWA，从不作为prefix cache保存。
  exact encoder全40层recovery理论L×W；decoder20层L_dec×W；
  实际bounded replay都只重放W，近似状态，不是bit-exact。
- MoE每层1shared +384routed，激活6routed，expert intermediate2304。
  mHC expansion4，Sinkhorn20；Single-Pass使用上一block的A，
  报告activation traffic由(4n+4)d降(2n+2)d，n=4时20d→10d，
  为此map口径，不是整体模型2×。
- Engram196B，两个模块zero-indexed层1/14，n-gram{2,3,4}，
  8hash heads；FP8lookup；inferencehost RDMA prefetch，RLrolloutGPU驻留。
  CSA2分布式训练有shadow indexer（单一logicalowner）、
  pipeline payload和microbatch生命周期管理。

## 新合成章节的研究组织

对象层次：原始资料/需求 → 可执行环境 → task+independent verifier →
校准episode → 合格轨迹 → CPT/SFT/RL/critic，固定benchmark留出。

重点对比以下机制，不将跨论文SWE分数画成数据方案排名：

1. SWE-Gym `2412.21139v2`：2438 tasks /11 Python repos，真实issue+环境+tests；
   Raw64689缺环境，不能称2438/Raw同对象。agent和outcome verifier训练。
2. R2E-Gym `2504.07164v1`：SweGen从commit、F2P、test生成反译问题；
   full8135 /去SWE repos subset4578；版本后续8.7k不能覆盖v1。
   execution-based和execution-free verifier互补，后者有风格偏差。
3. SWE-smith `2504.21798v1`：可运行repo上引入缺陷生成tasks；
   mutation语法通过不足，需behavioral坏/好对照。
4. SWE-Universe `2602.02361v1`：807693 multilingual instances，>52000 repos；
   test/fix patch拆分、bug/fixed双状态、in-loop hacking detector；
   论文未证明全部规模均完整公开。报告vs可下载数量分开。
5. daVinci-Env `2603.13023v1`（OpenSWE）：45320 Docker environments，
   >12.8k repos；质量筛选后约9000 environments /13000 trajectories。
   环境规模、筛后规模、轨迹规模不互换；建设和采样成本分列。
6. CoderForge-Preview 2026-02-25：51201 tasks，1655去重repos；
   258134 trajectories /155144pass。OpenHands0.52.1，
   Qwen3-Coder480B；train成功轨迹，失败另用于critic。
   source repo counts不能相加，来源有重叠；issue/baserev去污
   不自动证明repo/family/time级泛化。
7. NexForge `2607.14186v6`：需求驱动合成；公开baseline受scaffold影响。
8. EvoSyn `2610.12593v1`：space内预算调度和generation space扩展分开；
   以fixedbudget+heldout+samepolicy测试，防止追逐verifier漏洞。
9. ProgramGym `2610.13395v1`：paper→program reproduction environment；
   代码可跑与复现论文结论不是同一验收。
10. ScienceIDE `2609.19134v1`：27codebases/64environments/2812tasks
    （2515repair/295implementation/2acceleration）；Hard85。
    七类taxonomy不是七类等量生产。专家先定module/observable/tolerance，
    再specialize factory。pointwise `|c-r|≤a+ρ|r|` 或invariant；
    只comparison数字不足，需正/坏/变体和crossbuild校准。
    repairreward `max(0,(r-f)/(1-f))`；timeout与gradedfailure分离；
    bounded/filtered cohort的训练结果不能推成科学全领域成功。
11. SWE-Critix `2610.13356v1`：CoderForge成功失败差异分析→SFT+GRPO critic。
    alltestaccuracy57→66→78%只指预测testlabel，不等于78%科学/代码真实正确率；
    R2E子集SFT更差，在论文TableII体现，保留这种异质性。
12. DeepSeek V4.1 §5.1.1：tasktriplet，generalfailure回放/mocktool，
    coding多角色build/test/solve/independentinspect/repairloop；模型自造任务
    能力仍不完美。数据工程收益结论是该团队报告，非所有算法无价值。

履历连接依据 `content/pages/cv.md`：
AutoResearch专家protocol→审计/合成/校准/rollout/修订/SFT，2000+packages；
Qwen3.8-27B SFT；TB相关提高无数值；TB Sci“一轮review通过”
不得写成accepted/merge/official benchmark inclusion。
GUI Setup→Rollout→Verify→Reset；9641events为trace审计量不是任务量。
这些为作者提供材料，公开论文只是机制对照，不背书内部成绩。
不公开内部数据、task包、截图、私有路径或未授权细节。

## 评测章节的版本与名称

- Terminal-Bench **v4.1.0**，GitHub release2026-11-03：
  66tasks，无新增删除，所有66modified；verifier修复/复现/anti-hack，
  新CPU-only63tasks。官方命令
  `harbor run -d terminal-bench/terminal-bench@4.1.0` 和
  `harbor run -d terminal-bench/terminal-bench-cpu@4.1.0`。
  4.0官方post8removed/19fixed/66tasks/8hagenttimeout；
  不能4.0成绩直接覆盖4.1，也不能CPU63冒充full66。
- TBScience只有正式release **v0.1.0**（2026-08-26），官方postAug27：
  70tasks/5domains，3trials，每model使用native harness，不是puremodel对照；
  920proposals/464approved/386PR/70release，不同gate。
  0.2只有roadmap，未在release API发现，别写“已发布”。
- Challenges Jun18：首发3项 RustCompilerSpeedup/InferenceEngineCodegolf/
  WASMWebGLRenderer；singleproject，day-scale，无统一time/resource限制，
  finalrepo+完整autonomouslogs，task-specificcorrectness/performance；
  不宜与TB的pass@1单列总榜。
- Harbor framework不是benchmark；Hub registry也不是benchmark；
  HarborIndex初版1.0是82tasks，从6627/54adapters选出，
  最新Hub **rev5 (1.4)** 是80tasks；不能1.0候选漏斗贴上1.4新计数。
  currentsubmission每task≥5trials，部分LLM ensemblejudge必须pin。
  Index是hard slice，非总体能力latentindex。
- **DeepSWE双义必须显式区分**：
  Datacurve benchmark v1.1：113tasks/91repos/5langs，
  originaltasks，behavioraltests，mini-swe-agent；
  isolatedcommitteddiff→cleanverifier/CTRF，没有futuregit，
  公开号称contaminationfree是降低公开旧patch风险，不能证明任何模型从未见过。
  verifier误判数据由团队LLMaudit，不是独立真值。
  Together/Agentica DeepSWE-Preview 2025-07-02是RLmodel/recipe，
  Qwen3-32B/R2E4.5k；42.2pass@1/71pass@16/59hybridTTS三个口径。
- SWE-Gym/R2E/CoderForge/ScienceIDE是训练资源或环境系统；
  与SWE-bench testset分开，也可有各自heldouteval不改变主定位。
- SWE-bench Verified官方500issues；Lite300，Multimodal与Multilingual是
  各自split，不从名字推相同难度。SWE-benchPro public731/
  private276/heldout858=1865，41repos（来源Scale overview）；
  旧实验50turn/cappedcost与新250turn/uncapped不同；copyleft不证明零污染。
- SWE-bench-Live official当前扩展MultiLang/Windows；
  Pythonlite/verifiedfrozen，test滚动；“Live”并非每split月更新；
  Paper2025v1的1319/93与后续1890/223是不同快照，正文避免写滚动总数。
- AA解释为**Artificial Analysis**。方法页访问2026-11-14为
  IntelligenceIndex **v5.0.1** /9evals /4categories各25%：
  Knowledge:AA-Briefcase1.1 15%,AutomationBench-AA5%,GDP.pdf5%；
  Coding:FrontierCode2.0 15%,TB4.0 10%；
  Science:TBScience0.1 15%,CritPt2hard10%；
  General:AA-Omniscience1.1 15%,HLE-Diamond10%。
  AA仍TB4.0，不能写其已采用TB4.1。GDPval/APEX/EnterpriseOps属于additional，
  非这版index成员。不同子项pass/Elo/rubric不是直接相加原始值。

## 经典速查范围

分类表逐项给测量对象、评分、用途和边界；避免非必要规模/历史SOTA数字。

- 单段代码：HumanEval `2107.03374`；MBPP `2108.07732`；
  EvalPlus `2305.01210`；LiveCodeBench `2403.07974`；
  BigCodeBench `2406.15877`。前两者不等同repoagent，EvalPlus强化测试非新environment。
- 通用Agent：AgentBench `2308.03688`；GAIA `2311.12983`；
  τ²-Bench `2506.07982v1`（已有原全文）、SkillsBench1.1官方（已有源）。
- Web/GUI：WebArena `2307.13854`；VisualWebArena `2401.13649`；
  OSWorld `2404.07972` vs OSWorld2.0官方（已有108tasksource），
  AndroidWorld `2405.14573`（Google projectpage verified116programmatictasks/
  20apps，动态参数化，不称无限独立taskfamilies）。
- 科学：SciCode `2407.13168`、LAB-Bench `2407.10362`、
  MLAgentBench `2310.03302`、MLE-bench `2410.07095`；
  BixBench原`2503.00096`（搜索定位） vs BixBench3 **2608.25286v2**（absverified）：
  20tasks/138artifacts，rawdata→研究产物，程序对原studyartifact评分；
  不能等同自主选问题或wetlab新发现。
- AIRS-Bench `2602.06855v3`已有原全文：validsubmission和scientificmetric分开。
  PaperBench/CORE-Bench/ScienceAgentBench可作为复现扩展点，追加正式来源再写。
- GeneralQA只作为保留性评测一段，不把MMLU/GSM8K类成绩当作tooluse证据。

## 来源与中间证据

全量原文暂存在 `/tmp/my-blogs-frontier-research-20261114/`
和 `/tmp/my-blogs-bench-research-20261114/`；后者retrieveJSON记录fetch。
已发现错误：`2503.02175`不是BixBench，是DivPrune，**禁止引用**；
正确BixBench `2503.00096`；BixBench3 `2608.25286v2`。
OCP原PDF在tmp，不转载到站点；已用pypdf核对表字段。
Web/GitHub信息是访问快照；GitHub一律ghCLI查询，未操作远端benchmarkrepo。

需要为新增两章建立独立公开来源清单；与原研究地图43号索引分开。
后续验收在 `docs/validation.md`追加当次范围和真实结果。

## 已实施的正文、来源与图表

新增 `/agent-data-benchmarks/`，两章分别为
`s01_task_synthesis.html` 与 `s02_benchmark_map.html`。
前者比较上述十二条路线并连接CV；后者深入当前评测版本，
同时提供代码、通用Agent、Web / GUI、科学任务及基础保留性评测分类表。
完整来源索引52项（35篇论文、17项项目文档），与原研究地图43项独立；
`assets/research/agent-data-benchmarks/sources.json` 从HTML权威引用索引生成。

DeepSeek原第03章保留原URL / section anchors，新增CED张量来源、
40层CSA2图、hierarchical indexer、FP4格式与890 B/token分项推导、
两种SWA replay、MoE / mHC / Engram / pipeline细节。
五张SVG图、分项CSV及规格JSON登记为公共资源；
`scripts/research_figures.py`可重生成，连续生成的全部字节一致。
本次没有添加跨模型硬件速度排名或伪造训练曲线。

SWE-bench Pro来源改用可访问的Scale官方overview：
`https://scale.com/blog/swe-bench-pro`，其列明1,865实例、
731 public / 858 held-out / 276 commercial和41仓库。
旧榜单URL重定向到labs子域，并在本机返回403；
没有绕过站点验证，也没有用无法读取的榜单冒充独立检查。
旧50-turn / capped-cost与后续250-turn / uncapped来自此前研究快照，
属于不同协议，正文保留版本边界，不提供跨版本分数横比。

本次在线CV只新增公开学习笔记入口；作者原始项目数字及review状态没有改写。
CV改前SHA `acb3e4572e0966b0892678dfc3083744acc5226a14ba56a55f799d42befed60f`，
改后SHA `7c28abbe781275accfd9c2e408906f461fc490f52bb1b661279765fdf44984fe`，
对应精确变更理由已更新，原迁移manifest未重建。
