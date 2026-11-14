# 学习重编检查点

方案已批准，A–F本地实施与最终验收已完成。权威范围与逐页要求见工作区
`.trae/documents/blog-learning-rework-plan-20261115.md`。
最终结果见本文件末尾“F最终验收”；前面的分批记录保留当时的验证范围与修正过程。

## 原稿与保留口径

- 工作区真实快照：`/tmp/my-blogs-learning-rework-20261115.8s6w38/site-before.tar.gz`。
- 改前191项文件SHA：同目录`source-sha256.json`。
- 74份本地源稿在`assets/archive/blog-before-learning-rework-20261115/`以文本逐字归档，构建生成`/blog/history/`下载入口。
- `organization-changes-20261115.json`记录基线单元、改前单元、SHA与去向；两个不可变基线没有重建。
- 组织检查已明确改为“原单元在现稿或精确原件存在＋旧公开锚点与教学去向有效”，原“必须留在原源”口径不能用于获准重编的减法。
- 科研结论的复核状态没有因格式、保留或链接检查而提升。

## 当前完成范围

`llm-posttraining`与`llm-architecture`设为longform，各六个唯一源片段合入父页；
`llm-training-lifecycle`五节也已合入连续主题。Agent系统、任务评测与推理服务已完成三/四/三节装配；七个主线主题的34份源稿完成本轮重编。研究8源与DLM15源也已完成逐节处理和装配，综合题库及VLM2源已完成。

展开PG、baseline、GAE、PPO、DPO和OPD推导与算例；保留现代算法、
六套论文配方及12道参数追问。后训练原有21个伪公式容器已全部转换。
Harbor操作合同与科学案例中的部分重复解释改为短要点和主讲定位。
RL复习页集中为符号、算法卡、参数作用、诊断与短答；Agentic RL参考页集中为
研究问题、方法改动位置、局部信用示例、场景差异和证据边界。
旧稿中GiGPO跨prompt归一、CISPO/PPO混同、固定G/epochs、规则不可hack等
错误断言从当前正文移除，改前原件继续逐字保存。
六幅原SVG由冻结原稿读取并适配到后训练主讲，补折扣、terminal、参数复用与
反馈分类边界；原历史页面仍保留六幅原图。

架构六章逐段审阅：条件概率/NLL/softmax梯度与mask算例；
Attention方差缩放、RoPE旋转乘积与相对位移；FFN参数、门控与MoE容量；
Pre/Post-Norm链式法则、LN/RMS数值例；外积、衰减、delta覆盖与SSM状态例。
所有架构伪公式转换；型号名录折叠，比较协议与检查重点精炼。

训练01补packing边界和6NT来由；02补CSV数据形态链路、输入/目标配比反例，
长论文路线表折叠并保留退化结果。03/04重编为轨迹准入、mask梯度、筛选偏移、
反馈批次、独立验收与交付；删除当前重复DPO/OPD/PPO/GSPO全文。
05保留AdamW逐步推导及论文数据，把剩余伪公式改LaTeX；补LoRA梯度/首步初始化、
Muon polar方向反例、ZeRO分片/通信账本和global batch算例，集群规划按需展开。

Harness逐节重编为运行→工具→并发恢复→context/压缩/换窗→memory→轨迹交接；
保留两幅源码流程SVG、固定c2c1ebb版本、V1/V2、阈值/字节预算/门控与一致性边界，
六份原模板和用户原稿下载。GRPO、训练配方、无来源性能数字从当前正文移除；
课程检索公式保留教学归属与算例，ProtAgent配置保留为示例，事实归项目总结。

Decoder实现参考改为公式/形状→cache与mask→参数账本→完整小模型。
修正Pre-Norm不需warmup、Llama3 8B=MHA、SwiGLU两矩阵计数、双重label shift、
缺Module初始化、缓存未续接、device与bool mask等错误。PyTorch 2.8.0 CPU实际运行：
26,848参数，一步loss=4.7404494286；整段/逐token/多token缓存等价性通过
（atol=rtol=2e-5），含反向和四步生成。非性能/能力训练实验。
隔离验证环境在`/tmp/my-blogs-browser-tests/decoder-venv`；未改主站Python依赖。
分布式参考保留DeepSpeed2/3、FSDP1/2、Accelerate、固定MCore进程组、
LoRA完整教学配置和诊断；移除无出处的速度/显存排名，标明GPU示例未运行。

## 已执行验证

- 构建：107 HTML、303公开文件；链接、ID、目录顺序、原稿与去向检查通过。
- 装配集成测试扩展至架构六节、六幅适配图及伪公式清除；本轮两项测试通过（41.989s）。
- 归档缺失与篡改均必须失败，恢复精确原件后检查通过；修正macOS `/var`/`private/var`测试根解析。
- 引用：1106项source/version，补74原稿历史使用位置；原编号、登记、版本、SHA及装配定位检查通过。新增`citations.py refresh-usages`只刷新派生使用字段。
- 浏览器Chrome：390/768/1440，各查看架构、后训练、RL复习、Agentic RL四页，共12项。断开外部CDN；0pageerror、0TeX错误、0可见未渲染块、0整体溢出/图表超宽/页内坏链接。架构91、后训练118、RL复习9个数学输出；Agentic页无公式，按需加载不启动MathJax。
- 三项无JavaScript检查：两主题正文可读、390px无整体溢出；旧Attention子章有完整锚点手动定位fallback。
- 实际截图：`/tmp/my-blogs-browser-tests/learning-rope-390.png`与`learning-pg-1440.png`已查看。RoPE长行随后拆为多行，须在后续验收重看。
- 浏览器工具在全页13647节点时触发自身10000节点查询预算，截图曾因renderer离屏不可用；这两项是工具限制，未被记录为交互或视觉通过。后续用真实浏览器CLI完成大页与三屏验证。

本批次最新构建107 HTML/303文件通过，引用1099项；
两项扩展集成测试通过（40.838s）。六页×390/768/1440共18项Chrome检查，
全部details展开、外部CDN阻断，0公式错误/未渲染/整体溢出/页内坏链接。
架构92、后训练118、训练51、Harness1、Decoder5个数学输出；
分布式页无数学，未加载MathJax。三项无JS通过，包括训练兼容页手动链接。
截图AdamW390、Harness1440、RoPE390已查看；RoPE多行正确。
Harness竖图限制max-width=600px后专项复查通过：390px为314×282.59，
1440px为600×540，比例保持600:540，无整页溢出；新截图已查看。

当前预览`http://127.0.0.1:8771/llm-posttraining/`、`/llm-architecture/`、
`/llm-training-lifecycle/`、`/agent-harness-guide.html`。
构建HEAD为`e35a4c06a418f119310722e468ae9e520e30ae27`、dirty=true。
全站迁移记录、全测试与74页三屏验收尚未完成；未提交、推送或发布。

## D主题批次

检索与规划：BM25饱和/长度项、cosine度量与归一、RRF两路算例；
BoN独立概率与selector区别、UCT访问算例、环境分支与停止规则；
信任边界、六种隔离模式与clean/attacked/ASR分母。
任务：12路线按缺口比较、长名录按需；容差与repair reward；
NB均值方差、offset、8×5配对设计、contrast、BH四检验；
六独立比较轴、研究组split/bootstrap、配对胜负与不确定性；
pass@k失败组合推导，指标移到名录前。
服务：连续批处理、分页/共享prefix、量化舍入与饱和；
投机接受质量加正残差还原target；70B/TP4容量、Little条件与全部尝试成本。
保留原SVG、固定版本和来源编号；CPU/GPU/科学实验仍未执行。
实验JSON信用/采样拆组，OPD与推理预算分开。

逐页编辑记录见`docs/blog-learning-page-review-20261115.md`。
最新构建107 HTML/303文件通过、引用1099项通过。
两项扩展集成测试48.052s通过。
Chrome三个主题×三屏9项：全部details展开、外CDN阻断，
0错误/未渲染/伪公式/溢出/坏链接，数学输出40/33/37。
10旧子章深链定位并展开目标，4无JSfallback通过。
报告`/tmp/my-blogs-browser-tests/learning-systems-evaluation-serving.json`。
手机实际截图已查看，dense/contrast长式拆行后完整可读；
70B容量符号缩短与多行后专项通过：公式259.89px、可用314px、0错误；
新截图已查看，全部步骤和单位完整可读。

## E研究地图批次

研究地图父页设longform，七源逐节重编后装配；8份源本轮已处理。
旧覆盖表/路线/目录删除，通用合同、GRPO、投机、Muon等重复长讲归主线。
保留固定家族配置、CED/CSA2/FP4/890B/replay、工业矩阵分组、
新残差与KDA详细条件、低精度失稳反例、并发退化、持续适配时间边界；
具体逐页判断见page-review文档。71来源与15原件继续保留。
gui概念归属改父页namespaced锚点，其余研究路线由catalog自动定位父页。

make check107 HTML/303文件通过；引用1099项；
两项扩展集成测试48.493s通过。
Chrome390/768/1440、外CDN阻断、全部details展开，每屏30个数学输出；
0错误/直接display缺失/裸露TeX/伪式/整体溢出/坏链接。
7旧fragment、2无JSfallback通过，手机AttnRes与KDA图式已查看。
报告`/tmp/my-blogs-browser-tests/learning-research.json`。
截图发现裸`<`被HTML当标签导致原检查漏报；`j<l`/`j<K`已改TeX`\lt`。
新增直接display与正文裸TeX检查；最初28输出报告不算通过，30输出复验有效。
F应以更严格标准复验前批次，不能沿用“有任意后代数学节点”的旧判断。

E的DLM15源已逐節审阅重编并装配；bank1与VLM1本批已完成，剩余frontier/Harbor2、MyWork8，共10源；
74源全表/其余真实ledger原因、migration精确SHA、目录二级核心定位与F仍未完成。
未提交、推送或发布。

## E DLM批次

转移核/Bayes/SUBS→KL→CE→连续权重、VP变换/权重/score/SEDD/DFM、
块因子化/训练可见性/cache、连续codec/条件平均反例、
path/marginal/ELBO三误差/SPG/GDSD、U/D/E/compute-optimal、
尾和接受长度/周期成本均展开；结论、诊断与追问精炼。
DDPM五步、FM条件/边际证明及Ito/PF/逆VP、VAE重参数/KL/VQ/RQ/FSQ/LFQ、
循环梯度与停止都保留页内。原稿型号/历史数值未经共同条件验证的只作历史/研究线索。
新增确认：MDLM/LLaDA线性权重1/t；DDPM精度alpha/beta；block1期望等价不保证训练相同。
目录现顺序overview/objective/discrete/block/continuous/RL/scaling/spec/comparison/
loop/DDPM/flow/VAE/commercial；owner改父页namespaced。
15逐页理由更新，不重建归档SHA或baseline；详细page-review表已写。
make check及最终build107 HTML/303files，citations1103通过。
Chrome三屏，all details/CDN block，每屏131数学；0error/rawTex/direct-display缺失/
pseudo/global overflow/actual SVG超宽/坏链；14deep links、2noJS通过。
手机两图已view，131为最终有效报告；旧128/129通过作废。
重要：MathJax display自身overflow会掩盖reading-math.scrollWidth超宽；
F必须测SVG bbox宽度，正文有宽式优先分行，再复验，不能缩小到不可读。
报告/tmp/my-blogs-browser-tests/learning-dlm.json，runner同名js。
未运行GPU/科学/模型性能；未提交/发布。

## E综合题库与VLM批次

题库470问合并90知识卡，全部有短答/追问；11领域知识和经典算法不变量覆盖，
公式/代码保关键机制，完整推导与数值配方归唯一主讲，旧稿精确下载与旧锚点保留。
VLM六部分逐节重编，展开CLIP/SigLIP导数、patch/MLP/query、视觉梯度、
分辨率/merge/帧、空间逆映射、VCD与MaxSim；11问按需。
修正过时/绝对化算法、框架、资源结论与VLM模型/预算代码口径，未核实榜单回原件。
8组PyTorch2.8.0 CPU代码验证通过；两页三屏断CDN/all details检查通过，
分别2/10数学，0error/rawTex/直接display缺失/实际SVG超宽/整页溢出/坏链。
筛选命中4/90且展开收起通过，2无JS通过，手机截图已查看。
报告learning-bank-vlm.json与learning-bank-vlm-code.json位于/tmp/my-blogs-browser-tests。
make check107HTML/303files、citations1103通过；两页ledger和migration精确SHA已更新。
E仍剩10源，74源全表、前批严格复验与F全测试未完成；未发布。

## E前沿与Harbor批次

两源逐节重编完成，E剩MyWork4学习稿+4完整报告共8源。
Frontier基础长讲收敛、旧榜单转快照、领域普遍断言与碱基单位修正，
型号/许可/日期/AUTO和原日志按需保留，last-updated仍2026-11-10。
Harbor科学误差、oracle gap与有效奖励分母展开LaTeX和算例；
三原图默认展示按原比例限宽600px，可放大；固定版本/真实案例/canary、
scalingX17集的计数、去重与未执行边界保留。详录见page-review。
make check107HTML/303files通过；两页三屏断CDN/all details数学5/17，
0error/rawTeX/直接display缺失/实际SVG超宽/整页溢出/坏链，
Harbor三屏放大/ESC和两无JS通过。手机科学数学及分母截图已查看。
首次宽式结果作废，B污染中间量分行后最终通过；
reading.py补旧别名排除intro_id，避免重复reading-intro，F须运行全测试。
SHA与ledger两项已按当前正文更新，baseline/原稿SHA未改；未提交发布。
引用refresh-usages后1105项通过。两篇最终截图已关闭平滑滚动再准确定位，
Frontier手机OPD卡与Harbor科学算式已查看；脚本避免把滚动动画起点当作目标截图。

## E My Work导读与两报告批次

4导读与ProtAgent/dLLM2完整报告已逐节处理，累计72/74源。
六页LaTeX与五追问、PG/return/reward/scoring、ICL配方/rank风险/实际mask与affinity完成。
Holon导读margin定义从matched/null误写修正为mismatch−match；
固定版本与训练seed、实际token、OOD、专家真值边界保留。
reading.py对重编报告改短复习链接，删除克隆导读三节；
reading.js/css为原机制/研究图提供保持比例的默认显示及放大/ESC。
旧最小宽840/680造成内部裁切已修，新增实际图宽验收；
首次dLLM两式超宽已分行，失败报告不计通过。
make check107HTML/303files、citations1105通过。
六页三屏all-details/CDNblocked数学6/4/2/4/7/10，无公式/图形/页内链接错误；
30项原图放大/ESC与6无JS通过，手机ICL/PG/Holon实图已view。
报告`/tmp/my-blogs-browser-tests/learning-my-work.json`，runner同名js。
六源ledger真实理由与receipt精确SHA更新，未改baseline/原件SHA。
仍需Holon与科学任务完整报告2源、全74详表补全与F最终测试，未发布。

## E收尾与F进行中

两报告逐节处理完成，74源全表已补齐。Holon展开loss reducer、长度/mask分母、
拒绝采样与DiD算例；科学任务报告合并重复链路/库存表，展开完整路径接受与成本分母。
原图比例、放大/ESC、固定来源与历史未复现范围保留。
八页三屏24项、63图放大与8无JS通过；手机loss与联合接受截图已查看。
runner/report仍为learning-my-work.js/json，此批通过在全站分行变动前完成，F需覆盖当前产物。

course.py增加48章的核心推导/诊断/追问二级定位，仍只有一目录；
learning_review.py从74行真实编辑表刷新当前SHA与理由，不改任何原件或基线。
迁移脚本改为对获批重编源检查精确receipt、冻结原件、受校验构建的旧公开锚点；
AUTO源标记仍严格检查。make check107HTML/303文件通过，迁移当前已通过；
引用1105项通过。

F runner `/tmp/my-blogs-browser-tests/learning-final.js`覆盖26实体页、48合入片段、
三屏222源覆盖、144旧fragment、74无JS及三类读者路径，尚未最终通过。
首轮手机严格检查发现前批多个display内部SVG更宽，旧批次宽度通过不可沿用。
mathematics.py分行顶层quad/qquad，保护矩阵/cases/分式/函数参数；
latest diagnostic `learning-final-math.json`尚余约31个长式需逐式处理。
16项全测试463.714s仅1旧导读复制断言失败；已按移除克隆导读的最终合同更新，
新增数学结构测试还待复验，不能写成全测试通过。未提交/推送/发布。

## F最终验收

全部74本地源已有逐页编辑判断、当前SHA、精确原件与主讲去向。
34份主线相关源纳入七个连续主题；其余研究、DLM、参考与My Work按各自职责整理。
最终证据为 `docs/blog-learning-validation-20261115.json`，
逐页教学判断为 `docs/blog-learning-page-review-20261115.md`。

- **当前构建：**107 HTML / 303公开文件，`make check`通过。
- **全部阅读内容：**26实际阅读页×390/768/1440，共78页面检查；48装配片段连同父页共222源检查，74源完整覆盖。全部details展开、外CDN阻断；直接display、裸TeX、错误节点、实际公式SVG宽度、原生MathML、原图比例、整页溢出和页内链接均通过。
- **导航与静态阅读：**48旧章节×三屏，共144旧fragment保留query并定位、展开正确目标；74项无JavaScript正文/手动链接检查通过；63项原图放大与ESC关闭通过。
- **共享入口：**首页、博客、My Work、关于、CV、论文、文献和历史集合八页×三屏，共24项；五种关键词的主题去重、首次点击、返回/前进及清除筛选共48项通过。两项目录降级、键盘跳正文、数学加载失败后的局部提示/重试/幂等通过；两个外部课程HTTP 200，只验证入口可达。
- **集成检查：**全部17个不同用例在隔离副本的四组测试中通过，覆盖装配、SVG/ARIA/资源、原件篡改拒绝、确定性与只读构建、失败保留、引用版本、路线合同、CSV/图与更新器。四份日志为 `/tmp/my-blogs-browser-tests/learning-final-tests-{1,2,3,4}.log`。
- **来源与保留：**1105条source/version登记通过；两个不可变基线未重建，74原件逐字保留。迁移检查通过：299原锚点、59基线标记、199登记路由；获批重编以当前精确receipt、精确原件及有效公开去向验收。

最终修正了前批约31个超宽公式，逐式分行或先定义短符号；没有靠缩小字号解决。
数学重排保护矩阵、cases、分式和函数参数，并保留续行缩进；
九份完整手机公式截图（PG、reward-to-go、PPO、reverse-KL、SDPG、AdamW、
优化器内存、KV和配对标准误）已实际查看，公式和解释完整可读。
另外修复搜索输入失焦时重绘吞掉首次结果点击、旧链接命中details自身不展开、
先修/关联入口绕到旧子章、历史阅读壳重复h1四项真实问题。
初轮因这些问题失败的报告不作为最终通过证据；最终core/shared报告均 `ok=true`。

复现runner为 `/tmp/my-blogs-browser-tests/learning-final.js`、
`learning-final-shared.js`；原始结果和逐源验收已合入上述JSON。
本轮验证不构成GPU训练、科学任务执行、论文性能复现或原报告长表逐格复算；
正文既有事实复核状态与实验边界保持原口径。

预览：`http://127.0.0.1:8771/blog/#learning-paths`。
当前构建基于 `e35a4c06a418f119310722e468ae9e520e30ae27`，dirty=true。
本地工作已完成；尚未提交、推送或发布。
