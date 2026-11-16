# 博客讲解连贯性续轮审阅（2026-11-16）

基线提交：`80148053b623c4b6e1fc5a1a062f1113e5039443`。本记录为 T9 源级集成快照，不替代后续当前构建和真实页面验收。

## 执行摘要

- 74 份本地权威源恰好覆盖一次：13 改稿、61 保留；三模块分别为 18/4、29/6、27/3（源数/改稿数）。
- 33 个局部改动单元；修正两张已有编辑机制图，新增一张四路线HTML主讲，原SVG保留为参考。完整推导、代码、公式、来源及原稿继续保留。
- 核心修改为有效目标分母、mask 表示转换、AttnRes 算例输入、缓存对象与时效边界、CSV 类型条件、VLM 逆映射及返回数量、离散后验支持与实际抽样。
- 仅 11 页人工日期更新；离散扩散章补具体摘要。前沿滚动页的自动日期不变。

## SHA 与保留

冻结旧 diagram 的最终 SHA 等于真实 `git show 8014805:<source>` 字节 SHA，也等于本轮 before；本轮 after 必须等于当前源字节。旧 review、原稿/archive 和两份保留 baseline 未改；精确冻结列表及 SHA 见同名 JSON 的 `frozen_files`。
刷新仅为 13 份实际改稿追加本轮具体理由及更新当前 SHA。既有 `prior_reason`、61 份保留页凭据、归档单位和无关共享资源凭据不变；不批量吸收其它改动。

CI depth=1 缺少基线对象时，只有 `check` 可使用冻结历史与三个集成文件的精确指纹；本地有 Git 时仍验证真实字节，`refresh` 和 `--verify-git-base` 不允许降级。

## 证据边界

作者检查报告分别记录 11、35、42 组教学复算/静态检查。本线程核对模块原始 SHA、覆盖、当前差异位置和凭据，不将作者报告等同于独立科研复现。
T9 未执行当前构建、引用/迁移完整验收、17 项站点流水线测试、浏览器、三屏、无脚本或 MathJax 运行，也未提交、推送。上述工作由后续 T10/T11 对实际产物执行；历史验收不得复用为本轮通过。

## 变量前置定义轮（T12，后续检查）

- 41 源在公式首次使用前补充或改写符号说明，其中 32 源由保留转为改稿；累计 45 改 / 29 保留、74 个局部改动单元（上面的 13/61、33 单元为 T9 快照）。
- Kimi 自制图按报告原文改为“router 在 hidden 7168 上算分 → 896 选 16 → 被选 token 降到 3584”，并注明 router 不读 latent；Gemma 图改为 E2B 4:1、E4B 5:1 的 local:global 比例。两图用无头 Chrome 在 1440px 实际截图核对，未见过溢出。
- 三个 `assets/research/**/sources.json` 仅由 `scripts/citations.py refresh-usages` 重算 `used_in` / `historical_used_in`，来源元数据未改，故从冻结集移入精确集成集（247 → 244）。
- 方法与边界：先用仓外扫描脚本按文档顺序定位公式首次出现与说明位置，再逐页对照源文本修复；`make check` 通过（107 HTML 页、303 公开文件），`learning_review.py check` 通过（74 源 SHA 链与凭据）。未重跑模型训练、科研复现或全量三屏浏览器像素，不把静态检查当作运行验证。
- 窄屏可读性补记：家族速查表与跨模块矩阵在 390px 下原会逐字换行；两表加 `wide` 标记并在本页 `style` 块声明 40rem 最小宽度，改为表内横向滚动，表前各加一句滚动提示。无头 Chrome 实测 390px 表宽 640px、容器 314px、页面 scrollWidth 未增加；1440px 表宽 772px、不滚动。同轮扫描全站表格后发现 trainable-dllm 完整报告的“受控任务”四列表第二列仅约 53px、逐字换行，也给该表加 40rem 最小宽度；390px 实测表宽 640px、容器 358px、页面无溢出，1440px 表宽 910px、不滚动。

## 逐源记录

下列检查位置与判断沿用作者原始记录；完整 SHA、假设、检查 ID 与差异行范围见同名 JSON。保留页也有范围，不能由 SHA 相等推成全部内容审阅。

### my-work-holon

`content/posts/my-work-holon/index.md` · `agent-multimodal-diffusion` · **改稿**

理由：仅完整报告已有的舍入说明未在方法总结算例就近出现；路由、监督与预算主讲已有充分说明和图。

- `#work-knowledge`：P2T/T2P与protein-only不是确定性互逆；MoT路由图和caption已说明任务索引决定参数侧，保留图而不把所有蛋白token画成生成侧。
- `heading:从目标 token 比例到可执行采样`：有效率×均长反推记录权重，600/300例可复算；输入、监督、loss权重与active FLOPs已分开说明，无需重复配图。
- `#work-example`：逐项核对L0/L3端点、margin方向、DiD与CI口径；补显示值舍入造成1e-7复算差的说明，不改原结果。
- `#work-review`：single-seed、token share未审计、expanded非strict OOD和结构路线未闭合的限制保留。

改动：

- `#work-example` · `explanation`：补显示七位端点复算为-0.0058519/+0.0051415，与原精度-0.0058518/+0.0051416分开；明确CI复算还需逐anchor与依赖组件。

范围与限制：本次阅读方法总结的表示/路由、监督、配比、预算、Negative Ladder算例及限制；独立核算教学配比与显示端点，不重新训练、读取私有逐样本结果或重算CI。

### my-work-protagent

`content/posts/my-work-protagent/index.md` · `training-data` · **改稿**

理由：仅修编辑机制图的调用/终止分支歧义；已有回报推导、监督mask、独立评价及科研结果解释足够。 T10c仅在原figure/SVG声明局部横向滚动与780px最小宽度，防止手机默认标签缩至12px以下；不改线条、比例或语义。 T10h修复owner01六组确证的无箭头和交叉歧义：六条连线增加12×12实心尖端，history回线拱桥与调用reward竖线14单位留隙明确不汇合，observation另从x790送入reward；保留780px最小宽度、840×200比例、旧ID、节点文字和终止答案语义。

- `work-knowledge`：实际检查工具调用/观察循环，发现节点把最终答案也送入工具执行；改为只画调用回合，终止评分在就近caption/desc明确。
- `work-example`：原始step return的R-0.05/R-0.30/R与episode广播区分充分；normalization、whitening、优势clip不冒充原始return，保留完整公式和算例。
- `work-review`：全样本OOD分母、严格recall>0.5、61.00指定checkpoint与61.40三seed均值、PFUA独立协议和缺工件边界清楚，不扩写历史实验。

改动：

- `work-knowledge` · `diagram`：复用原SVG，调用节点不再包含最终答案；title/desc/caption限定工具回合，说明最终答案终止评分而不再执行工具或接观察。
- `work-knowledge` · `diagram-readability`：原figure显式max-width:100%/overflow-x:auto，原SVG加min-width:780px；840单位宽图的13px标签默认至少12.07px，不依赖zoom或折叠。
- `work-knowledge` · `diagram-direction`：工具链三处向右、observation回history向上、调用局部reward向下、observation到reward向左各有实心尖端；history在x312处拱桥跨线，调用reward竖线y88–102留隙不join，observation反馈与reward独立出口。仅desc补交叉说明，caption/正文/数值不变。

范围与限制：本轮审阅方法总结、编辑图和原有算式；独立复算教学return和guard算术，未运行工具、ROLL、训练、OOD/PFUA或重新取得私有论文工件。

### my-work-harbor

`content/posts/my-work-harbor/index.md` · `training-data` · **改稿**

理由：只修总结图的实际产物输入线，保留完整路径算例、refinement停止结论及历史来源。 T10c仅在原figure/SVG声明局部横向滚动与780px最小宽度，防止手机默认标签缩至12px以下；不改线条、比例或语义。

- `work-knowledge`：图中冻结答案原先直连评分框，独立Verifier只接私有校准；改为答案与校准汇入Verifier后输出评分，匹配正文信息隔离。
- `work-example`：完整路径并集拒绝(1,20)混拼，与逐字段包络的反例一致；公开输入、转换hash、known-wrong、冻结答案和独立判分的顺序充分。
- `work-review`：生产交付、质量认证、refinement效果和训练收益分层，资格/正式分母与历史库存不混用；accepted child=0边界保留，不刷新历史结果。

改动：

- `work-knowledge` · `diagram`：原SVG的冻结答案连线改接独立Verifier；caption明确答案+私有校准→Verifier→评分/归因，校准不回流Solver。
- `work-knowledge` · `diagram-readability`：原figure显式max-width:100%/overflow-x:auto，原SVG加min-width:780px；840单位宽图的13px标签默认至少12.07px，不依赖zoom或折叠。

范围与限制：检查方法总结的合同、路径算例、接力与停止边界；未启动生产、盲测、refinement、打包或读取当前库存，不把固定历史记录当新效果。

### my-work-dllm

`content/posts/my-work-dllm/index.md` · `agent-multimodal-diffusion` · **保留**

理由：表示、可见性、监督密度和输出指标已有具体例子与充分图示；未发现需新增讲解的确证缺口。

- `#work-knowledge`：AR/MDM训练与生成、调度/attention/loss mask三轴分明；三列调度图不是串行三阶段，保留。
- `#work-example`：两块a1/b1可见性表对应同side同offset及xt→x0严格较小offset；保留源码分支与多跳、sample_mode边界。
- `heading:熵选块为什么不等于选出正确块`：平均熵、未提交集合、低熵不保证正确与probe成本均已说明。
- `#work-review`：Test/Gen-PPL、top-p混合T sweep、NFE、历史smoke与主实验缺口分开，不补实验数字。

范围与限制：阅读总结的目标、Scatter两块算例、Jigsaw变体、ICL/PF/Sudoku与LM1B口径；没有重放源码、训练、采样或历史Test/Gen-PPL审计。

### my-work-holon-full

`content/posts/my-work-holon/full-report.html` · `agent-multimodal-diffusion` · **保留**

理由：所读主讲已有MoT分路、训练/评测链、margin分解与codec权衡图；图和文字说明互补，完整报告已有舍入与实验边界，无需重复增补。

- `#chapter-2`：实际阅读2.1-2.6主讲的模态分路、GQA、packed attention、初始化与参数公式；静态查看MoT双路及单层图，分路后共享交互清楚，保留。
- `#chapter-3`：读取主讲配置、lookahead/consumed frontier恢复与3.3有效位置/typed空间/reducer；2文本8蛋白例得到2.6与4，不能混作等权平均。
- `#chapter-5`：输入token目标、fetch与监督分母分开；5.2长度100/400及拒绝采样支持条件清楚。历史校准精确份额未重新测量。
- `#chapter-9`：读取likelihood/生成、reverse索引L-1-i、EOS与target softmax、requested/valid/metric分母合同。
- `#chapter-12`：读取主讲12.1-12.3、舍入注记；静态查看IG+Interference示意和PS8/PSC端点图，绝对值与保持幅度不混用，不重复作图。
- `#chapter-16`：读取16.1-16.5主讲及SEPIT split/gate原文；查看codec链路与五臂散点，AA/structure、native/codec真值及whole/segment分母已区分。
- `#chapter-17`：读取主讲接口、128×1与5876版本、全池检索与候选设置、失败分母和去同源子集；不把r@4/10/20字段直接当标准Recall@K。
- `#chapter-19`：读取研究复盘与single-seed、sidecar、SFT稿件、data-ready限制，保留历史范围。

范围与限制：本次只阅读列出的主讲段、3.3算例、5.2算例、12章DiD及16章SEPIT split/gate原文，并静态查看6张指定图；未通读全部artifact折叠区或21章所有历史材料，未复现训练、73行全榜、bootstrap、codec或ProtText-Eval实验。

### my-work-protagent-full

`content/posts/my-work-protagent/full-report.html` · `training-data` · **改稿**

理由：实际检查段落已有监督、回报、评测分母和复现限制，科学正文与原件保持。T10x仅将报告目录重置断点760px对齐既有单列布局850px，解除761–850px目录浮动吸顶对标题和正文的真实遮挡；未修改共享样式或历史统计。

- `sft`：检查04节masked NLL、shift、模板和局部batch不能推global batch；sum与平均分母区别已说明。
- `reward`：检查05节score-function、step/episode回报、reward附着与无工具guard；raw return不称最终advantage，观察不计动作似然。
- `results`：检查07节全1000分母、缺答失败、10例6/10与6/8、禁工具及Signal退化；已有独立评价边界。
- `repro`：检查10节阶段重启/optimizer/reference、temperature配置冲突及缺失权重/rollout；不能仅凭补充包复现全部表。
- `deep-dive`：检查12.1-12.4、12.6-12.7的四臂因素、指定checkpoint与seed均值、return教学例、traj_id/step顺序、阈值和诊断分母；现有说明充分，保留所有表与科研图。

- `#setting` · `toc-layout-readability`：源第59行报告目录media断点760px改850px；只在761–850px重置position/top/float/height，与原单列布局一致。

范围与限制：审阅范围为04/05/07/10与12节所列阅读链路，核对的是现存文本条件及教学算式；未重新复现四臂三seed、MMseqs2同源审计、OOD/PFUA、bootstrap区间或所有历史实验。 T10x源级单替换及反向字节核对通过，科学正文、公式、图表、锚点与原件不变；旧9fa失败与截图继续保留，新产物的目录、正文、JS/noJS及独立像素仍须实际验收。

### my-work-harbor-full

`content/posts/my-work-harbor/full-report.html` · `training-data` · **保留**

理由：实际审阅段落已明确完整路径、隔离、cohort和历史成本边界；不改报告原稿、科研图、历史case或统计。

- `problem`：检查阅读引入与问题定位：多路径可判、可解性与生产启动分开；历史时间/规模已有导读限制。
- `roles`：检查角色间公开/私有资产和工件交接，明确实际权限而非prompt声明决定隔离。
- `joint-path`：检查第3节完整接受域并集、混拼反例、正负控制和冻结包指纹；原近主讲分支图足够，无需增图。
- `historical-results`：检查第5节740/668/413库存与匹配cohort分母、pending和尝试区别；不把413/740推成成功率，全部原统计保留。
- `cost`：检查第7节全部尝试成本与c/p教学估算，85.7%与原稿79%明确不同；usage覆盖和价格未核验的限制充分。
- `interview`：检查收束追问：drop=0、accepted child=0不被生产库存替代，失败归因和证据失效条件明确。

范围与限制：仅检查引入、第1/2节、第3节失败路由/双路径/联合接受域/产物目录、第5节、第7节和第8节；未复跑历史CRISPR案例、247proposal评审、生产批次、4601 usage或refinement。c/p只作教学算术复算。

### my-work-dllm-full

`content/posts/my-work-dllm/full-report.html` · `agent-multimodal-diffusion` · **保留**

理由：所读理论、算法、受控任务、LM1B与框架章节已将调度、状态、监督与实验口径讲清；三张证据图和已有流程图保留，不重复增加。

- `#objectives`：AR因式分解、线性吸收1/τ、只监督mask位置及Block-Diff块边际/界关系清楚。
- `#algorithms`：Scatter offset图及B1/B2/B3公式区分调度与mask；Jigsaw probe→选择→提交保留独立计算成本。
- `#theory`：读取标准高斯先验岭回归、solve与无噪声投影风险1/1/3；静态查看d=10/15/20 ICL原图，不把可识别性等同于训练收敛。
- `#structured`：读取PF从goal反查但输出start→goal与Sudoku行列宫/空格分母；实际查看PF原图和Sudoku坐标消融图，原图及缺失主图日志边界保留。
- `#lm1b`：逐项阅读Test/Gen-PPL主表与top-p/first-hitting/25或100样本协议，SEDD差异未被抹平。
- `#compute`：达阈值训练成本、未达标删失、NFE与延迟分开；affinity=1教学读数可复算，未重做profiling。
- `#framework`：读取结构化/LM1B配置、模型、loss、checkpoint/EMA与评测职责，保留原两条框架图。
- `#config`：完整CLI/YAML例保留，长度128与默认1024、block_size/T、shape与checkpoint匹配明确。
- `#audit`：699/630日志、27/32 Gen-PPL及历史CPU/MI308X smoke均为原记录，不写成本轮复现。

范围与限制：实际阅读所列章节与其完整公式/配置算例，静态查看ICL、PF、Sudoku三张嵌入PNG；没有读取699/630条原始日志、恢复D5/P5、独立重算论文表值或复跑任何历史smoke/训练/采样。

### agent-systems

`content/series/agent-systems/index.html` · `agent-multimodal-diffusion` · **保留**

理由：入口图与案例只承担学习组织，核心推导由装配子章负责，已有依赖和权限说明足够。

- `#purpose`：三决策引入与证据/决策/约束/验收图说明权限贯穿读取和动作，不是最终才门控。
- `#case`：16个GEO样本与8样本冻结对象分开；配对/count先于计算，教学方案未执行。
- `#mastery`：检索、selector、环境与ASR分母的学习出口明确，入口不重复子章长推导。

范围与限制：完整阅读入口源；未执行RNA-seq分析、任务runner或安全测试。

### agent-rag

`content/series/agent-systems/s01_rag_retrieval.html` · `agent-multimodal-diffusion` · **保留**

理由：公式、独立算例、动作/观察图和证据停止规则相接充分，无需新增图。

- `#retrieval`：完整阅读BM25、单位向量、RRF与Faiss代码算例；分数与事实可信度分开，复算排名和长度惩罚。
- `#agent-retrieval-observation-map`：query为动作、外部检索为观察、controller与索引ACL另有职责；已有图紧邻主讲，保留。
- `#evaluation`：Recall非空集合、MRR未命中0、引用支持/完整与研究级切分均明示。
- `#frontier-comparison`：论文EM单位和0.41/1.89/2.36百分点只作报告表差值，不当引用支持率或本地实验。

范围与限制：通读该源并复算教学数值；未运行Faiss、检索、Search-R1训练或重新核验外部论文性能。

### agent-planning

`content/series/agent-systems/s02_planning_compute.html` · `agent-multimodal-diffusion` · **保留**

理由：已有完整BoN/UCT算例与状态分支图；外部副作用不能靠prompt回滚的条件已就近说明。

- `#search`：完整阅读BoN存在性/selector与UCT算例，独立性、零访问与回报尺度假设清楚。
- `#environment`：文件/进程/随机态/预算与prompt分开恢复；S0→独立A/B→验证→提交图中的A/B是同一展开节点的并行分支，非串行两路线。
- `#budget`：净收益单位与停止规则、训练G和部署N区分充分。
- `#frontier-comparison`：两论文表不能拼因素因果排名；搜索次数不等于延迟，保留。

范围与限制：通读该源，复算BoN/UCT/收益教学值；分支runner、科学任务、rollout和论文训练未执行。

### agent-trust

`content/series/agent-systems/s03_trust_safety.html` · `agent-multimodal-diffusion` · **保留**

理由：已有授权/观察分路图、门控伪代码和分母算例足够，未发现新缺口。

- `#agent-trust-boundaries-map`：数据通道与独立授权通道、拒绝不调worker和获准观察回填已明确；保留已有职责图。
- `#isolation`：typed参数、canonical target、凭据/网络与TOCTOU限制在伪代码旁说明，JSON合法不能授予能力。
- `#evaluating`：clean/attacked utility与全部/条件ASR分母分别复算，1-utility不等于ASR。
- `#frontier-comparison`：949攻击实例分母、±未解释成CI、零攻击不推出绝对安全，边界保留。

范围与限制：通读威胁模型、隔离、伪代码和评测定义；未运行攻击、防护、OS sandbox或CaMeL复现。

### llm-serving

`content/series/llm-serving/index.html` · `architecture-inference` · **保留**

理由：保留。系列入口已把输入状态、正确性、服务指标和章节职责接清，不增加重复主讲或第二张入口图。

- `#purpose`：入口按模型状态、服务调度、设备数值、任务成本建立学习顺序；四阶段图明确不是性能比例图，后续章节承担具体计算，不需在入口重复算例。
- `#connections`：分页、复用、投机的对象区别及容量复算目标明确；固定vLLM/SGLang版本与未验证新组合的范围保留。

范围与限制：检查入口引导、概念图、学习收束和版本说明；只读静态核对，未重新核验远端release、运行服务或验收装配页面。

### serving-runtime

`content/series/llm-serving/s01_runtime_scheduling.html` · `architecture-inference` · **保留**

理由：保留。分页、调度、复用和稀疏流量均有实际输入、状态、输出与排除项，既有共享页图已清楚，不重复补图。

- `#phases`：A/B/C连续批处理表给出剩余token和准入，明确prefill/decode混合是调度选择且轮次耗时不同；TTFT/ITL边界已说明。
- `#paging`：T=35、page size=16得到3页13空槽；两请求共享前32token得到4唯一页64槽，复算与地址映射图一致。
- `#shared-kv-page-layout`：A/B表映射同一共享{7,2}及各自尾页；图明确不是A后B串行，并说明引用保护、copy-on-write和退出只解引用。
- `#prefix`：相同token与权重/adapter/位置/模态兼容、锁引用和eviction解释完整；请求退出不等于删除prefix。
- `#kimi-sparse-traffic`：132L+576min(L,2048)读取与24(132+576)存储是两账本；22.9%渐近比、16992/13824 bytes复算一致，GB300单请求prefill表不归因于读取公式。

范围与限制：阅读phases/paging/prefix/implementation/mixed/evaluation及对应图和源码摘录；复算教学整数与规格算术，不重新执行固定后端、抓取源码或复现Kimi硬件测量。

### serving-parallel

`content/series/llm-serving/s02_parallel_quantization.html` · `architecture-inference` · **保留**

理由：保留。并行布局和PD边界图、完整量化与投机轨迹均足够，收益与精确性条件明确，无须新增图或重编。

- `#serving-parallel-domains`：TP/Serving DP/EP按对象分支，头数不足可能复制KV，逻辑并行度不能无条件相乘；不是三步串行。
- `#pd-state-handoff`：源服务、connector、目标物理页与确认/取消责任分明；10GiB/25GB/s下界0.4294967296s已复算，未当总延迟。
- `#quantized-dot-example`：权重/激活、scale与饱和输入完整；整数[2,-3,4,7]、4.67→4.00误差-0.67及含scale6B复算一致，未称实际GPTQ/AWQ。
- `#speculation`：同前缀p/q、接受质量、残差、alpha=1边界及贪心/随机采样区别齐全；三词表最终分布复算回p。
- `#speculative-trace`：B接受、第二B拒绝后补A，后缀C丢弃；输出A与计算A的KV分开，draft/target各自恢复；30/22约1.36不误称3倍。

范围与限制：静态审阅parallel/disaggregation/precision/speculation/plans与既有图；独立复算教学量化、传输下界和离散概率，不运行量化kernel、connector或投机服务，不重现论文性能。

### serving-capacity

`content/series/llm-serving/s03_capacity_cost.html` · `architecture-inference` · **保留**

理由：保留。完整容量和成本例已有输入、单位、分母及未验证条件，入口图只连接账本到服务结果，无重复补充必要。

- `#ledger`：按同一rank、同一时刻互不重复分配计账；物理槽、共享、复制、SWA、scale和递归状态分别说明。
- `#example`：70B近似参数与Qwen72B结构明确区分；TP4、BF16、名义80GB/预留16GB、32K条件齐全。单请求2.5GiB、容量43/21/10/21、8请求72.47483648GB复算一致，均是待测界。
- `#metrics`：提交0s、到达1/1.2/1.5s得到TTFT1、ITL0.2/0.3、TPOT0.25；open/closed loop及超时边界清楚。
- `#rollout`：Little定律写出稳定且同边界条件；2/s×30/60s得到60/120在途，不把活跃生成槽当任务吞吐。
- `#cost`：全部10次尝试、4成功、8GPU-h/20CPU-h及教学单价明确；总18、每成功4.5复算一致；零成功未定义与失败不重复计费保留。

范围与限制：阅读账本、容量、指标、rollout、成本、协议和来源；只复算文中理想规格与教学时间/成本，未测GPU峰值、SLO、实际报价或下载工件运行。

### llm-posttraining

`content/series/llm-posttraining/index.html` · `training-data` · **保留**

理由：入口、产物与学习顺序已有充分导读，补细节应落在对应主讲章而非继续扩入口。

- `overview`：起点→探索→更新→独立验收为学习路线，caption已明确RL回流SFT与失败恢复，不误称工业固定单线。
- `read`：原理/变体/配方/诊断顺序和GRPO完整组算例入口可定位；不再复制手册推导。
- `findings`：状态、反馈、系统、证据四边界均有具体检查，明确无GPU后训练实测。
- `downloads`：case-contracts的design_only与空结果解释充分，资料索引不冒充真实日志。

范围与限制：检查入口/收束/下载状态及固定引用组织；未重新调研79项来源，也未运行课程装配或浏览器。

### posttraining-supervision

`content/series/llm-posttraining/s01_supervision_preference.html` · `training-data` · **改稿**

理由：仅消除有效轨迹集合与N分母的局部歧义；完整DPO、mask、恢复和拒绝采样算例已充分。

- `sft-objective`：原文说仅平均N_n>0轨迹，但N先被称为轨迹总数；含空目标样本时episode分母有歧义，已最小澄清有效集合计数与整批跳过。
- `recovery`：错误学生动作作条件、可靠教师恢复作目标，终止回复须先验产物；mask不是移除观察，保留。
- `rejection`：K=4易/难题保留概率和搜索成本已连接筛选分布，未将拒绝采样等同RL。
- `dpo-full-example`：两回答求和似然、reference冻结、beta=.2、sigmoid梯度、三logit一步SGD和重算loss齐全，独立有限差分符合，不重复补例。
- `handoff`：checkpoint/tokenizer/template/tools/谱系和独立任务执行交接明确。

改动：

- `sft-objective` · `explanation`：N定义为筛除无目标轨迹后的计数，重新索引；全批无目标跳过更新，不以0填空轨迹loss。

范围与限制：本轮检查监督/恢复/RFT/偏好/交接主讲；复算教学CE、DPO和有限差分，不执行SFT或复现SimPO/ReTerm论文表。

### posttraining-algorithms

`content/series/llm-posttraining/s02_rl_algorithms.html` · `training-data` · **保留**

理由：核心推导、完整数值与边界已充分；独立复算通过，不机械增加公式/图或扩论文配方。

- `policy-gradient`：轨迹分解、环境独立theta、reward-to-go外gamma^t和baseline条件完整。
- `gae-full-example`：TD→GAE→固定lambda-return→actor/critic loss，两步数值衔接完整。
- `gae-boundary-example`：bootstrap b与递推c分开，暂停/terminal错误可改变优势符号；现有三分支图说明不拼接续段。
- `grpo-full-example`：reward/std/ratio/min/loss/softmax链式梯度齐全，正负平台与共享概率变化没有混淆。
- `normalization`：2/8长度算例给三个分母和token权重，有效位置不含工具/padding。
- `ratio-methods`：GSPO几何比、CISPO detach权重和soft SAPO导数区分充分；未称通用无偏。
- `heterogeneous`：Bernoulli有效组概率、相关采样限制、全同task梯度与辅助目标区别就近存在。

范围与限制：检查原理、GAE/GRPO/长度与ratio主讲以及配方/诊断；独立算术/有限差分只适用于教学值，不验证公开论文数值、最新模型性能或框架GPU实现。

### posttraining-opd

`content/series/llm-posttraining/s03_opd_self_distillation.html` · `training-data` · **保留**

理由：局部梯度、监督位置、状态支持和独立部署条件已有完整链路；保留原图与数值，不扩大多教师调研。

- `why-on-policy`：生成快照与current区别、固定prefix分布和交替采样循环就近说明。
- `full-vocabulary`：reverse/forward KL方向、softmax导数、支持/温度、teacher no-grad和二候选梯度完整。
- `sampled-gradient`：KL值估计与score加权梯度区别、state-only baseline、sg与旧轨迹校正说明充分，期望与有限差分相符。
- `historical-teachers`：路由验证集用于选教师，LAD/top-k和额外补采成本明确，不伪称独立测试。
- `mopd2`：学生continuation与教师prefix分开，多个prefix的分母/部署自主到达性与成本明确。
- `forgetting`：teacher KL下降不等于综合能力提升；目标域、保留域和全学生终评充分。

范围与限制：审阅上述主讲与recipe/自蒸馏介入边界；只复算固定prefix教学KL，不复现ECOS/Agentic-OPD/MOPD或所有历史模型实验。

### posttraining-rewards

`content/series/llm-posttraining/s04_environment_reward_credit.html` · `training-data` · **保留**

理由：反馈来源、信用假设、可恢复性、终止与产物验收均有具体例子和边界，未发现需局部增补的确证缺口。

- `environment`：初态/动作/终止/产物/verifier链明确，预算失败与容器/服务故障不混reward。
- `signal-types`：outcome、PRM、Q/V、advantage和teacher预测对象分开，续写成功不等于步骤正确。
- `long-credit`：错误后恢复与成功广播反例充分，教学Q/V=-.4/+.6信号明确来自额外估计而非单条成功轨迹。
- `gar`：正优势非零分母、lambda cap/recentering、4/3和2/3总量例限定充分。
- `cases`：代码、科学和GUI产物/状态不变量及投机路径明确；无需再补四节点图。

范围与限制：本轮检查环境/信号/长程信用/GAR与三案例教学链；不重新复现PURE、RLDS、图式信用或grader实验表。

### posttraining-frameworks

`content/series/llm-posttraining/s05_frameworks_async.html` · `training-data` · **保留**

理由：版本、概率、状态续段和服务产物交接已有完整两线图及数值；复算符合，保留不增补。

- `roles`：trainer/rollout/environment/verifier/teacher职责和权重同步、变长分母/资源冲突充分。
- `three-policy`：behavior/old/current/reference不混分母，importance不能创造缺失支持或恢复缺域。
- `async-full-example`：分段mu保存、两段ratio、乘积1.44与几何平均1.2、错误替换分母1.309091、裁剪顺序不同完整可复算。
- `partial-rollout`：旧KV跨权重不默认有效，compaction/真实token prefix与episode/sample/token分母边界充分。
- `slime-opd`：固定commit源码student-teacher logprob方向、adv减少/增加、混合归一化顺序和接口对齐清楚。
- `compute`：rollout/training/grader、teacher、拒绝与重试成本单列，不把算力比例换成美元。

范围与限制：审阅现存固定源码摘录/教学概率与版本说明，未重新读取远端源码、认证全部后端组合、执行异步GPU或复现AReaL耗时。

### posttraining-cases

`content/series/llm-posttraining/s06_task_cases_experiments.html` · `training-data` · **保留**

理由：三种任务已把输入、反馈、监督/评测分母与交付贯通；不将待执行矩阵扩写为虚构日志或新实验。

- `code-case`：空输入ValueError与非空行为、禁止改tests、失败prefix三信号分支及SFT/OPD局部数值完整。
- `science-case`：ID/design/contrast/调整范围和artifact/provenance顺序清楚，不造显著基因数。
- `gui-case`：对象ID、时区、draft权限、保存与持久状态区别，成本/恢复/全学生终评明确。
- `trajectory`：design_only空数组/null不能冒充轨迹，exact prompt/response、segment版本与拒绝原因充分。
- `diagnosis-cost`：全部尝试、teacher/环境/重试入账，零成功比值未定义；未执行矩阵明确。
- `delivery`：权重/协议/tasks/谱系/独立结果和旧能力交付树完整。

范围与限制：检查教学任务合同和设计矩阵，不执行mean修复任务、RNA-seq、GUI状态操作、轨迹采集或模型训练。

### training-methods-systems

`content/series/llm-training-lifecycle/s05_training_methods_systems.html` · `training-data` · **保留**

理由：更新对象、符号、数值、状态所有权、复算条件和恢复合同已有详细主讲；未发现应补的新局部缺口。

- `peft`：LoRA形状、首步B/A梯度、底座冻结仍传输入梯度和并行支路原图充分。
- `adamw-derivation`：sum/EMA动量尺度、v为二阶原点矩、零初始化修正、Adam+L2与解耦衰减边界清楚。
- `adamw-example`：给定梯度两步m/v/修正/方向/Adam/AdamW及代码独立复算一致，非收敛排名。
- `optimizer-cost`：MiB/KiB与bytes、状态/整体容量、Muon主GEMM FLOPs与TFLOP/s区分，单层token数明确。
- `state-sharding`：N=1B D=4的16/7/5.5/4GB持久状态与峰值不混，通信原图充分。
- `batch-accounting`：2×8×DP4=64，TP/PP/CP不重复增加独立样本；专家DP重组与固定源码条件充分。
- `cluster`：128/1024池与70B32.8125GB静态账本明确是规划，CPU/teacher/reference另计，不称投产可用。

范围与限制：独立复算LoRA教学量、AdamW、状态字节、Muon主乘法与进程数；不验证所有优化器论文数据、GPU耗时、kernel、框架支持或集群运行。

### scientific-task-family

`content/series/agent-data-benchmarks/s03_scientific_task_family.html` · `training-data` · **保留**

理由：统计输入、符号/单位、分母、输出和未知reference边界齐全；保留原图、全部公式与科学结果未知状态。

- `provenance`：16样本GEO、8样本airway、FPKM/count/answer-bearing层分开，网页元数据冲突只列待核解释。
- `statistics`：NB方差、相对库大小offset、8×5配对design、log/log2FC、反向contrast、BH四检验全链完整可复算。
- `contract`：gene/sample唯一、缺失与0、未收缩LFC、method路由、调整集合和公开待冻结阻塞项完整。
- `verifier`：同方法复算与跨方法差异分轨，正负/边界/混拼/NaN/alias/泄漏条件充分，未造容差。
- `splits`：研究/供体/source lineage为独立单位，不能随机拆8列或千题面冒充泛化。

范围与限制：只复算现有NB/offset/BH教学数值并检查合同；未下载GEO/SRA/airway、运行DESeq2/edgeR、生成基因结果、验证许可/容差或科学盲测。

### cluster-training-evaluation

`content/series/agent-data-benchmarks/s04_cluster_training_evaluation.html` · `training-data` · **保留**

理由：方案状态、资源量纲、实验归因与统计单位已有充分条件；原教学SE约.0448正确，不应增图或改未测配置。

- `design`：步骤信用/采样/OPD/推理预算独立轴，sci-posttrain与CPT初始化A-E分开。
- `budgets`：单请求输入+输出32768与多轮总轨迹成本不混，G/CPU/step待冻结。
- `resources`：Dense/MoE训练与rollout/reference/teacher/CPU各角色入账，静态容量非峰值。
- `measurement`：全部attempt分母与可执行条件率、零成功成本、reserved/active资源分开；配对8/12例SE与区间可复算，研究组bootstrap保留依赖。
- `failure`：允许多标签/undetermined，规格、方法差异、环境和budget区分，旧失败记录不覆盖。

范围与限制：复算独立教学任务的配对SE/区间，不等于研究group bootstrap或实际训练seed验证；所有集群、科学任务、吞吐/价格/成功率仍未执行。

### llm-architecture

`content/series/llm-architecture/index.html` · `architecture-inference` · **保留**

理由：保留。入口职责、完整forward定位及证据边界已清楚，新增内容会重复子章主讲。

- `#purpose`：先完整forward、再模块、后前沿家族的顺序明确；先修、状态与六个架构问题完整，不把概念关系图当耗时比例。
- `#connections`：读完需能解释mask/shift/状态、推导与比较预算，并区分规格、作者实验和独立复现；完整代码与固定来源入口仍在。
- `#sources`：原Transformer encoder-decoder与现代decoder示例分开，FlashAttention exact不等于逐bit，固定实现不能代表全部工业源码。

范围与限制：入口引导/概念图/收束/来源说明的本轮静态阅读；不以入口通过替代子章或全部历史科研事实复现，未验收真实装配导航。

### architecture-transformer

`content/series/llm-architecture/s01_transformer_foundations.html` · `architecture-inference` · **改稿**

理由：修正一个影响梯度复算的归一化缺口和一个旧章序衔接标签；保留已有张量图、mask例、shift、NLL算例与状态表。 T10e将平均masked梯度原行内公式移入局部可键盘横滚的block显示span，保留全部数学字节、目标下标、闭括号与符号说明，不改共享CSS。 T10z仅追加两处noscript必要说明：block的X/U/Y形状与顺序双残差，平均masked梯度的索引、softmax导数、固定m/N缩放和原算例-0.25。移除两块恢复改前全字节；原LaTeX、代码、图、ID、引用、样式和正文不改。

- `#tensor-flow`：B/S/d/H/dh/f形状与行向量投影、GQA例外、value和权重区别清楚，张量流图保留。
- `#attention-mask`：可见两个score=0、value2/4输出3；自身可见用于预测下一token，布尔API、全屏蔽和packing边界已有解释。
- `#block`：两条同形残差、固定源码顺序正确；跳向残差章的第04章旧标签与当前次序不符，改为按章名定位。
- `#objective`：shift只一次及masked NLL算例完整；原平均L梯度写成单tokenp-y，漏m/N_valid，已区分ell与L并补有效目标数。
- `#state`：参数/激活/请求状态/优化器四账本与KV权重版本条件完整，不需再图示。

改动：

- `#objective` · `correction`：单token导数改用ell；平均masked L导数补m_bi/N_valid，并定义目标ID/词表轴及mask直接梯度与后续条件路径的区别。
- `#block` · `correction`：残差链接保留原URL，过时的第04章标签改为残差与归一化章，避免完整forward插入后章序误导。
- `#objective` · `formula-readability`：仅平均masked梯度增加局部block横滚span及两条局部样式；公式内容/分隔符、词表轴和mask条件说明逐字保留。

- `#block-nojs-recurrence` · `nojs-math-explanation`：block无脚本读式明确X/U/Y同为[B,S,d]，先Attention再FFN，两次残差读取未归一化旧表示且第二步读取U。

- `#masked-gradient-nojs-derivation` · `nojs-math-explanation`：平均masked梯度无脚本定义b/i/j/y/m/N，逐步求softmax交叉熵导数并乘固定m/N，接原mask算例-0.25与N=0拒绝。

范围与限制：逐节阅读tensor/mask/block/objective/state/evaluation；标准库NLL与局部logit梯度有限差分复算，非训练/模型性能复现。展示公式、代码和原ID保留；改正的行内导数是唯一有意公式表述修正。 T10z只证明两块精确追加及局部教学复算；noJS三宽真实阅读和JS正常隐藏仍须新构建浏览器与独立像素。s01原fail/pending及其他owner局部pass保持，残差参考图空白与mask缺证亦不由本修复自动关闭。

### architecture-attention

`content/series/llm-architecture/s02_attention_position_cache.html` · `architecture-inference` · **保留**

理由：保留。尺度、缓存、RoPE和online softmax都能从输入算到输出，既有图和算例不需增补。

- `#attention-scaling`：独立零均值单位方差假设明确；两候选缩放前后2.2384/2.5379复算一致，不宣称实际Q/K必满足假设。
- `#head-sharing`：写入头/读取头、MLA例外和repeat只服务计算已说明，GQA图与持久未重复KV对应。
- `#kv-bytes`：K/V两宽度推导、小形状192B、TP复制与量化附加项齐全。
- `#position`：列向量二维旋转推导方向、相对j-i与逻辑/物理位置边界清楚；共同平移例复算。
- `#online-softmax-example`：完整块输入和m/ell/n定义、两块重标与输出3齐全；第一块已显式给基准，无必要机械再补初始化。
- `#frontier-comparison`：Kimi Linear同1.4T设置与发布5.7T分开；保留EvalPlus非最优负结果，不以资源机制代替硬件性能。

范围与限制：局部数学和教学字节/旋转/分块复算；Kimi Table3及全部历史论文成绩只静态保留条件，未重新查询来源、训练或执行GPU kernel。

### architecture-moe

`content/series/llm-architecture/s03_ffn_moe_routing.html` · `architecture-inference` · **保留**

理由：保留。完整路由、重排身份图、容量分支和通信例构成可复算链，不用新图取代已有推导。

- `#swiglu`：两矩阵/三矩阵、等参数宽度和gate/up/down顺序清楚；d6时288参数与SiLU门控2.1932复算一致。
- `#moe-full-example`：四二维token、2x3 router、softmax后top2归一、线性教学专家及shared=0均明确；输出与[3,4,1]负载复算一致。
- `#balance`：8条assignment取容量3溢出一条，丢D到专家2且不归一产生(8/5,0)，与dropless区分，空专家槽不自动转移。
- `#parameters`：总/激活参数和单向payload区分；具体放置三条跨rank路径产生dispatch12B、combine12B，其余元数据/训练通信排除。
- `#latent`：latent投影、实际发送宽度与shared/router/Norm例外已说明，不由r/d推出整体速度。
- `#frontier-comparison`：Table3能力与Table5另一73B服务模型分开；并发4/64外不占优的结果与成本缺失保留。

范围与限制：标准库复算教学router、输出、容量和网络payload；未执行真正SwiGLU专家、All-to-All或训练。论文性能表及latent工业配置仅静态范围核对，未作全历史事实复现。

### architecture-residual

`content/series/llm-architecture/s04_residual_norm_stability.html` · `architecture-inference` · **保留**

理由：保留。布局对照、梯度限制、Norm算例和科研负结果均已有就近边界，无确证补图缺口。

- `#norm-bypass-map`：同一x两种替代布局、旁路与Norm覆盖位置明确，不误画成两个顺序子层。
- `#norm-position`：局部Jacobian乘法方向及跨层顺序明确；均值方向例明确是LayerNorm且F=ax，未推广成所有Norm或无衰减保证。
- `#rmsnorm`：x=[1,3]的LN[-1,1]、RMS[0.4472,1.3416]及忽略epsilon条件完整，已复算；FP32统计源码保留。
- `#new-residual`：深度表示与多残差流对象区分，双随机谱范数只约束旧流混合，不约束F与pre/post完整Jacobian。
- `#frontier-comparison`：27B/262B tokens、n4条件与MATH较HC低保留；同token非同FLOPs，不从分数证明稳定性。

范围与限制：复算Norm教学例与LN常量平移不变性，链式法则和图作静态语义检查；未求真实网络Jacobian、重训mHC或复现失稳/性能曲线。

### architecture-hybrid

`content/series/llm-architecture/s05_hybrid_architectures.html` · `architecture-inference` · **保留**

理由：保留。递推、状态形状、分叉、换窗及换参数恢复已有完整算例和分支图，不机械增加。

- `#hybrid-state-layout`：按层计划选择GDN/SSM/Attention，本层私有历史与输出/新状态明确，不是三类模块固定流水线。
- `#linear`：dv×dk状态与列q/k/v方向明示；两关联[2,3]、读2/5及8B例可算，省feature map/归一明确不是softmax。
- `#gated-delta`：累加[7,3]、delta[5,3]、gated[5,1.5]复算；key单位范数与beta=1覆盖条件已列。
- `#ssm`：一般离散SSM矩阵维度与h=[2,5]教学例清楚，chunk算法不等于Python串行或O(1)训练内存。
- `#state-branch-example`：前缀5独立分叉8.5/0.5、误串行2.25、截窗8、换参数7.125/旧态7.25复算一致；模型读出非词表预测。
- `#state-fork-map`：两个私有状态从同一快照恢复，底部只汇总管理不合并数值；真实KV/卷积/位置/权重需要一并快照。

范围与限制：标准库教学外积/delta和标量SSM复算、混合图静态阅读；不是GDN/Mamba真实模型或跨权重迁移实现验证，工业质量与chunk性能未复现。

### architecture-comparison

`content/series/llm-architecture/s06_model_comparison.html` · `architecture-inference` · **保留**

理由：保留。此章职责是比较框架和实验合同，具体数值归各主讲，重复增加例子/图会破坏分工。

- `#axes`：六轴分开记录状态、参数、深度、数值对象、预测及系统，active/总参数/上下文不混用；入口图固定版本后才比较任务。
- `#co-design`：任务到结构/训练/服务反馈图只表示设计依赖；训练与decode瓶颈、state分支/系统权限分别说明。
- `#mtp`：MTP信号与候选验证分开，贪心/随机精确性及drafter争资源边界完整。
- `#experiments`：机制、同checkpoint服务、Agent端到端三层合同与固定预算清楚，闭源未披露结构不从榜单或memory行为反推。

范围与限制：阅读六轴、家族定位、co-design、MTP及实验协议；局部方法/边界检查，不将后续型号表或全部闭源材料视为本轮事实复现，未运行任何对照。

### agent-data-benchmarks

`content/series/agent-data-benchmarks/index.html` · `training-data` · **保留**

理由：入口承担对象关系与学习目标，详细算例已有对应章；保留不扩入口。

- `overview`：任务生产→科学操作→轨迹→独立终评的导读与论文/方案/履历证据性质分开。
- `boundaries`：训练环境、benchmark、Harbor/Hub、AA指数对象区分充分，不按名字混DeepSWE。
- `mastery`：合同、统计复算、评测分母与失败定位收束明确，已有关系图不重复。
- `sources`：52项共用编号与新增科学章独立来源清楚，固定版本/访问快照不冒充独立复现。

范围与限制：检查导读、对象分类、来源/下载组织；没有重新调研52来源、运行装配、合成任务或benchmark。

### agent-task-synthesis

`content/series/agent-data-benchmarks/s01_task_synthesis.html` · `training-data` · **保留**

理由：产线、分流、有效任务/样本、容差与反馈/交付均有原图和例子；保留原数据准入图，不重复增内容。

- `objects`：source/environment/task/episode单位区分，环境数和重复轨迹不冒充family覆盖。
- `contract`：公共题面/环境/产物与solution/tests/private审计分开，oracle/bad/alternative/clean reset验收充分。
- `science`：绝对/相对容差单位与近零例、repair剩余进展(r-f)/(1-f)的f<1条件明确，可独立复算。
- `admission`：CPT/SFT/RL/Critic四路原分支图紧邻主讲，旧episode有reward不等于on-policy，角色/来源组继承明确。
- `experiments`：冻结空间/预算与反馈扩张消融、逐family/失败/成本和未执行状态清楚。

范围与限制：检查公开方法归纳与已有教学算式，未执行环境工厂/校准/critic/SFT/RL或重新核验所有来源规模。

### agent-benchmark-map

`content/series/agent-data-benchmarks/s02_benchmark_map.html` · `training-data` · **改稿**

理由：只修确证的主讲衔接定位错误；指标、分母、成本和独立评测已有完整例子。

- `metrics`：pass@1/repeats、pass@k、pass^k、selector和有限n组合例充分；但配对区间被写为前节，实际主讲在后续s04，已改为精确链接。
- `versions`：TB4.1/CPU、Science0.1、Index1.0/1.4、DeepSWE和AA自身版本明确，不混当前榜单。
- `frontier-comparison`：SkillsBench费用仅完整token子集，不用费用÷全体成功率冒充精确成功成本，保留。
- `selection`：核心留出/诊断/控制按能力与产物选，来源族和固定预算条件充分。

改动：

- `metrics` · `correction`：把不存在的“前节配对区间”改为后续训练与终评#measurement直达，标明标准误和研究组重采样。

范围与限制：检查测量对象、指标及版本/成本边界；复算教学组合和配对数，不重新运行榜单、访问私有题、核验服务商实时价格或最新release。

### llm-research-map-2026

`content/series/llm-research-map-2026/index.html` · `agent-multimodal-diffusion` · **保留**

理由：这是来源与旧目录页，主讲在所属主题；已有组织路径足够，不为引用索引增算法图。

- `#overview`：来源参考角色、归位主题与研究组织flow明确；caption说明不是单一真实系统执行链，保留。
- `#priorities`：状态/权限/verifier、同预算与待执行研究边界明确，不扩展调研。
- `#archive`：官方PDF快照与arXiv版本不宣称字节相同，保留原件/许可/来源链接。
- `#sources`：71项固定编号、不同稿件/模型卡/动态发布的版本角色保留；不把多个载体当独立复现。

范围与限制：通读本地来源页的引入、选题、归档和71项索引；未重新抓取或逐篇核验71个外部来源、原件许可与性能。

### research-agent-data

`content/series/llm-research-map-2026/s01_agent_data_bench.html` · `training-data` · **保留**

理由：研究增量、artifact交接和审计已有具体例子与原图；不重复基础协议或刷新历史版本事实。

- `distinctions`：生成空间和反馈增量与基础任务主讲衔接，source/轨迹与同源切分清楚。
- `harbor`：CSV已声明与临时SQLite未声明的交接反例完整，原分支图区分可传文件/不自动传状态。
- `parity`：原/adapter动作、观察、终态、reward与随机状态重放条件明确；不以格式统一称语义等价。
- `audit`：request/span计费0.03+0.02=.05、父span重复计费反例与缓存/失败保留充分。

范围与限制：检查现存四路线归纳、迁移例和审计字段；不重放HAL/τ、Harbor adapter、数据库状态或所有引用实验。

### research-agentic-rl

`content/series/llm-research-map-2026/s02_agentic_rl.html` · `training-data` · **保留**

理由：前沿分类已接回唯一数学主讲；有效组、信用证据与异步交接无需重复增例。

- `map`：advantage/ratio/聚合/准入四维明确，组合结果不称独立相加。
- `objectives`：GRPO task优势、GSPO几何比、CISPO IS权重detach分别落到更新对象，环境观察不计策略。
- `credit`：anchor可比、taxonomy/知识特权/value学习与SAPO同名边界充分。
- `heterogeneity`：100/100派发但99.2/7.7有效组、过滤后约92.8%中等域，明确IID二值假设和课程偏移。
- `asynchrony`：完成偏移/旧策略/同版本数值三问题分开，旧KV非通用有效，behavior与response mask/版本字段完整。

范围与限制：检查现存研究归纳与解析示例，不扩新research，不复现引用模型、RLDS/KnowGPO/T1/SAMPO或routing replay。

### research-base-architecture

`content/series/llm-research-map-2026/s03_base_architecture.html` · `architecture-inference` · **保留**

理由：保留。缓存账本、张量所有权、两种bounded replay的触发/输入/写入及近似边界已完整，既有四张科研图无需重复。

- `#versions`：V4/v1/1017发布、报告和能力更新分开，552B主干+196B查表与8B/16B active不混算。
- `#ced`：H20→C/Z保留token轴，本层Q/SWA来自本层hidden；图明确长prefill仍有decoder尾部replay，不宣称完全不走decoder。
- `#csa2`：Full/Reindex/Reuse分缓存生成、索引重算和候选复用；20+20层表、候选2048×8上限16384与首次O(N)一致。
- `#cache`：288B主entry+68B索引、1.5 encoder+1 decoder条目得到890B/token；图178×3+356一致。SWA/权重/对齐排除；HBM1/4与persistent1/8不相乘。
- `#engram`：参数查表、KV和外部memory/skill职责不同；MoE、mHC流量50%及不同Engram放置条件均局部限定。

范围与限制：本轮实际检查版本引入、CED/CSA2/cache/replay/Engram及实验收束，四SVG读取标签并验证原字节；只复算entry/层组/候选算术。未重新逐页核验51页原报告、历史科研事实、QAT质量或硬件性能，未声称bit-exact恢复。

### research-inference-diffusion

`content/series/llm-research-map-2026/s04_inference_diffusion.html` · `architecture-inference` · **保留**

理由：保留。proposal、target、准入、训练和服务边界清楚，已有对照图与选择偏差例足够，不用额外图伪证精确性。

- `#budget`：长期周期时间/提交量之比不是逐周期比值均值；90ms/5=18ms慢于15ms基线的教学反例明确。
- `#diffusion-drafter-options`：三种方法是替代对照；DSpark轻head依赖与AdaFlash独立trainer分工、版本/成本明确，不画为每轮训练。
- `#exactness`：实际proposal条件概率、准入和状态提交条件齐全；p=q但丢B只验A的负对照确实把P(A)从1/2改到1。
- `#opd`：reverse-KL q_draft||p_target方向、状态监督、Agent reward与drafter质量/费用区别完整。
- `#frontier-comparison`：AdaFlash T0/block16加速与DSpark T1/block7含bonus接受长度不同分母；并发128的DFlash0.76倍负结果与独立trainer缺失成本保留。

范围与限制：阅读budget/methods/exactness/opd/frontier-comparison/experiments；复算周期教学算术与可枚举选择反例，不重训或运行三方法、不复现原论文速度/概率频率，未确认全部DLM proposal可取得精确q。

### research-agent-frontiers

`content/series/llm-research-map-2026/s05_agent_frontiers.html` · `agent-multimodal-diffusion` · **保留**

理由：动作/观察和持续适配图已充分解释分层与时间边界；无新场景实验，保持原数字与公开范围。

- `#gui-observation-action-map`：观察时间/焦点、坐标逆映射、提案/可信执行、新观察和结果未到不重放明确，保留闭环图。
- `#science`：执行/有效提交/科学支持、标签泄漏反例分明，不以文件存在验收。
- `#adaptation`：memory/skill/参数支路与时间冻结、新任务/旧回归图清楚，保留而不画为必经顺序。
- `#multiagent`：10/10秒+3秒协调例可复算；critical path与总资源时间、MOPD训练与runtime协作分开。

范围与限制：通读GUI/科学/skill/持续适配/多Agent本地说明，复算关键路径教学例；未运行OSWorld、科学任务、LoRA或PARL实验。

### research-architecture-landscape

`content/series/llm-research-map-2026/s06_architecture_landscape.html` · `architecture-inference` · **保留**

理由：保留。版本、转置、层计划和性能归因均有局部条件，已有历史路径/层数量图充分；该主讲可作为修正滚动页机制分类的既有依据。

- `#state`：dk×dv状态与基础章转置等价已明确；KDA先Diag再rank-one的AD/DA非交换矩阵复算一致，D=0教学边界保留。
- `#families`：家族表单列主干/查表/视觉参数；层图48/93/45/70/48仅表示组成非顺序/FLOPs，Nemotron108子模块不同单位。
- `#kimi`：K3的KDA、周期Gated MLA、AttnRes深度选择、Stable LatentMoE职责清楚；K3.1换Gated DSA的card/config与旧报告分开。
- `#glm`：Attention与FFN是两张层表；AMD DP/EP vs TP的硬件/版本/96k/32k/并发256明确，随机token服务不是Agent成功率。
- `#minimax`：MSA group选block、前三Attention与dense FFN区别明确；109B论文kernel倍数不套428B发布模型。
- `#closed`：Gemma12B encoder-free例外及闭源披露范围在相邻段落明确，memory/换窗不能反推Loop Transformer。

范围与限制：本轮阅读引导、状态推导、各家族边界和实验协议；对历史路径/层数量SVG读取实际文本、核对原字节，对KDA矩阵作局部复算。未再次外部核验九家完整报告/config或全部历史科研事实，AMD/MSA/模型性能未复现。

### research-architecture-training

`content/series/llm-research-map-2026/s07_architecture_training.html` · `architecture-inference` · **改稿**

理由：仅补AttnRes两表示例的query、Norm简化条件和key/value复核点，使公式真正连接到原输出；其余残差、latent与深度图保持原样。 T10e为原残差对照SVG增加局部横滚容器及1160px最小阅读宽度；按原viewBox864和最小9px注记推导至少1152px内容宽，留边框余量，不改资源、图内字节/ID/语义/比例。 T10p按独立六组合字线相交核实，新增默认四路线HTML主讲，类型、可用表示、操作与注记逐行对应且行间不串行；原figure/object/fallback/caption/URL及1160px横滚保留于原生参考details。原SVG字节与内部字线相交局限未改变，主讲可读性和参考保留/展开分开验收。 T10y仅追加四处noscript语义HTML：AttnRes得分/深度softmax/原value读出及两表示逐步复算，mHC逐流双支更新/约束及理想双随机证明/二乘二矩阵。移除四块可恢复改前全部字节，原LaTeX、图、引用、ID、样式和参考折叠不改。

- `#residual`：原AttnRes得分例缺少q和Norm条件，已补真实可算输入；mHC旧流与F支路、双随机局部范数边界已完整。
- `#attnres-depth-read`：同一token历史分为Norm后的key和原value两路，加权结果仍(0.5,3)，新增条件与原图一致，不需改图。
- `#mhc-stream-layout`：n×n旧流与1×n/n×1模块支路同形相加，数据依赖并行非GPU并发保证；未添加第二普通残差。
- `#latent-moe`：两家hidden/latent/top-k与Norm/shared例外明确；固定1024分派BF16得到16/4MiB，维度比不是全网收益。
- `#recurrent-core-loop`：共享theta执行K次后Post，潜在迭代非CoT输出；1/1.5/1.75收敛例与两种循环成本区分完整。
- `#precision`：KV、训练GEMM、QAT和optimizer迭代分对象，源码/精度机制引用留在既有主讲，不扩大优化器研究。

改动：

- `#residual` · `worked-example`：给h1/h2列向量、Norm scale=1/epsilon=0、归一化key与q=(0,log3/sqrt2)，逐步算得分/softmax，再读取原value得到(0.5,3)。
- `#residual` · `diagram-readability`：原残差对照object外加可键盘横滚容器，局部min-width1160px/max-width:none；原资源、fallback、caption和放大链接逐字保留，不依靠zoom豁免默认可读性。

- `#residual-route-comparison` · `diagram-readability`：默认四路线语义HTML主讲与原SVG原生参考分离；局部自然高度/换行样式服务同一呈现单元，Standard/AttnRes/mHC/GR各有状态→操作和完整注记，行间无执行箭头；原915字节figure块完整保留。

- `#attnres-nojs-formula` · `nojs-math-explanation`：AttnRes无脚本三步读式：逐维点积得分、沿深度指数归一化、读取未作key归一化的原表示。

- `#attnres-nojs-example` · `nojs-math-explanation`：AttnRes两表示无脚本逐步复算：RMS除数、key、query点积、1/4与3/4权重、原value输出(0.5,3)。

- `#mhc-nojs-update` · `nojs-math-explanation`：mHC无脚本逐流更新：res旧流混合与pre/F/post模块写回并行读取旧X，明确形状和约束范围。

- `#mhc-nojs-proof-example` · `nojs-math-explanation`：mHC无脚本理想双随机范数/乘积证明及2x2矩阵表、行列和、同向/差异分量精确复算。

范围与限制：实际检查residual/latent-moe/precision/depth/agent及实验收束；标准库复算AttnRes、mHC两个方向、固定分派payload和共享core标量例，两SVG静态保留。未重训AttnRes/mHC/LatentMoE/Huginn，未外部重核全部科研报告。 T10p仅源级呈现修复与准确保留；原raw布局失败未转为pass，当前主讲/参考浏览器和像素验收仍待独立执行。 T10y source-ready及独立复算仅证明源级精确追加，四块只在noJS需要可见，JS须确认默认隐藏；三屏当前公式/说明/图/原生参考仍需真实浏览器和独立像素。原noJS失败、参考图空白和缺失mask证据保持原状态，不以源码核证改为pass。

### llm-training-lifecycle

`content/series/llm-training-lifecycle/index.html` · `training-data` · **保留**

理由：入口已承担路线和阶段产物，具体公式在子章充分展开，保留不堆叠。

- `overview`：四学习阶段的图已明确真实循环/分叉和RFT两含义，不称通用固定生产顺序。
- `training-map`：阶段与横向方法两轴及Scaling/μP/WSD/optimizer/系统主讲入口完整。
- `artifacts`：每阶段输入/目标/checkpoint/验收列清楚，权重不足以定义Agent协议。
- `findings`：输入/目标/预算、初始化收益与等总算力、均值与分项回归、状态/谱系边界充分。

范围与限制：检查导读、阶段地图、交付与固定引用组织，不验证工业报告全部事实或课程装配/线上内容。

### llm-training-pretraining

`content/series/llm-training-lifecycle/s01_pretraining.html` · `training-data` · **保留**

理由：目标、packing、预算和规模外推均已有默认可读完整算例与检查条件；无需机械增加图或新论文。

- `mixture-budget`：唯一/读取/目标token、重复2倍与目标占比11.1%例、桶/样本分母限制清楚。
- `packing-full-example`：两文档4×4可见性、m=(0,1,0,1)、shift后两有效目标、1.039721损失逐步齐全；attention与loss隔离分别验收。
- `compute-derivation`：2NT+4NT=6NT来源与长Attention/重算/MoE/通信排除明确。
- `scaling-derivation`：固定预算代入、边际加权平衡、正二阶导和N/D计数单位充分，非普适20N规则。
- `scaling-ladder`：独立规模、完成schedule、IsoFLOP、留出外推/失败反馈链完整，μP与WSD条件不混Muon。
- `systems`：optimizer/scheduler/RNG/sampler与权重共同恢复，模型卡阶段/数据污染交接充分。

范围与限制：独立复算教学CE与配比，不执行预训练/规模阶梯/μP/WSD，未验证所有工业训练量或外推性能。

### llm-training-midtraining

`content/series/llm-training-lifecycle/s02_midtraining.html` · `training-data` · **改稿**

理由：仅补确证的CSV类型/空值条件和输出检查，保持原样本/代码/引用；其余配比与归因解释充分。

- `definitions`：阶段位置与训练目标区分，CPT/trace SFT不凭名称混用。
- `results`：逐行下游SFT版本、rollout平均pass@1与pass@3、额外算力/单seed边界充分，不修改论文表。
- `data`：四类CSV样本中真假值过滤没有说明字段类型/空值规则，与保留合法0目标存在条件缺口；已补字符串假设和产物内容复核。
- `mixture`：900文档+5目标trace=5/905而非输入10%梯度权重，桶权重/观察mask与全局归约充分。
- `harbor`：A-D初始化与E额外SFT预算对照、CPT与sci-posttrain命名空间及未执行状态充分。

改动：

- `data` · `explanation`：明确if row['value']仅适用于未转换CSV字符串且空字符串为空；数值0反例、三行输入保留1/3行及内容/顺序/表头/input hash复核，不能仅相信工具行数。

范围与限制：检查现存配方/数据/伪代码/分母与交接，独立复算字符串/数值0和目标密度；不重跑Nemotron消融、合成数据、CPT或Harbor实验。

### llm-training-sft-rft

`content/series/llm-training-lifecycle/s03_sft_rft.html` · `training-data` · **保留**

理由：本章聚焦行为/接口交接，数学主讲链接已有完整推导；现有例子够用，不重复DPO或RL章节。

- `sft`：角色mask、hidden表示链式梯度、两个动作CE完整，观察不直接拟合但仍影响参数。
- `quality`：成功轨迹也筛错误动作，保留真实失败上下文、来源簇/截断/恢复准入。
- `rejection`：易/难各10题筛成功后90%易题反例充分，搜索成本和新策略独立执行不混。
- `handoff`：schema/停止错误、全失败/全成功各有交接判定，模板、split、image、verifier和预算字段明确。

范围与限制：检查教学监督链和准入协议；未执行模板render、SFT/RFT或验证工具合法率，示例2048/8仍非推荐配方。

### llm-training-rl-evaluation

`content/series/llm-training-lifecycle/s04_rl_evaluation.html` · `training-data` · **保留**

理由：此章已说明合法0、完整产物、训练与终评分离、样本分母和版本交付；局部类型条件已补在真正使用过滤代码的Midtraining主讲处，不重复。

- `reward`：CSV原7/空/0输出1/3行、header/rows/input hash与完整结果reward充分，不以文件存在给分。
- `systems`：behavior/动作span/真实prefix/镜像与raw失败成本保存，准入与吞吐不混。
- `protocol`：100题10增5退=5个百分点配对例、全分母/retry/缺失、训练seed与生成seed区别明确。
- `harbor`：同下游初始化与等总成本投入分开，A-E与sci-posttrain两命名空间不混。
- `release`：checkpoint→数据/目标→执行协议→独立结果/成本，完整交付树清楚。

范围与限制：检查教学CSV/配对例与合同，未执行RL、独立CSV任务、Harbor或生成实际训练/终评日志。

### llm-frontier-2026

`content/posts/llm-frontier-2026/index.html` · `architecture-inference` · **改稿**

理由：修正滚动参考页与现有主讲的机制分类冲突、K3及Mistral Large3时效冲突，并补缓存单位/分母/近似边界；不改历史数值、来源、日期、自动标记或整页结构。 T10d仅将3.3标题内FACT状态标签局部设为12px，修复实际10.88px小字号；标签语义、ID、历史信息及共享CSS不变。

- `#frontier-evidence-bridge`：更新至2026-11-10且未验证全部历史断言的快照边界保留；发布、self-report、传闻不升级为复现。
- `#models`：重点读K3/K3.1、V4.1与相关型号对照：K3仍称当前最新，与同页2026-11 K3.1及页首冲突；Mistral Large3仍称当前最大，同页已收录Large4，两者均改历史快照。AttnRes被写成序列Attention，改深度读取；V4.1的890B/两个比例/尾部replay加就近口径说明。
- `#frontier`：闭源接口/负载说明明确不倒推参数与循环架构；本轮不重新验证折叠内历史价格、发布或成绩。
- `#arch`：GLM/Qwen/Kimi/CED概括混同线性Attention，局部改为递归状态、稀疏读取、跨层复用不同对象；Huginn潜在深度与CoT、GPT传闻边界保留。

改动：

- `#models` · `correction`：K3条目及型号表区分KDA+周期Gated MLA的序列混合与AttnRes同token前层深度读取。
- `#models` · `correction`：K3当前最新旗舰及Large3当前最大规模断言改为历史快照；同页已收录后续K3.1 Pro和Large4，不新增当前排名。
- `#models` · `explanation`：V4.1条目就近说明890B是bytes/token非参数，HBM1/4与host/SSD1/8不相乘；decoder尾部replay仍存在且为近似恢复，链接原缓存主讲。
- `#arch` · `correction`：GLM/Qwen/Kimi/DeepSeek概括和混合SSM表不再把AttnRes或全部稀疏/共享KV当线性Attention；按历史访问与深度两个轴解释。
- `#arch` · `label-readability`：仅3.3其它架构信号标题内FACT span增加font-size:12px，保留原pill/fact class和状态文本，不修改其它标签或共享样式。

范围与限制：局部检查阅读引导、overview、models、frontier、arch（源约180–459行）；重点为K3/K3.1、V4.1、Huginn、机制分类及Large3/Large4同页时效冲突。其余优化器/RL/Agent/Protein/benchmark历史条目未作本轮事实复核；全文件仅静态保留ID、来源、图、脚本及AUTO标记。无外部研究、价格/性能/发布日期重核或自动更新运行。

### agentic-rl-guide

`content/posts/agentic-rl-guide/index.html` · `training-data` · **保留**

理由：研究问题→局部例→条件→主讲交接已连贯，保留原图与例，不重复扩算法名录。

- `part3`：五问题与动作/状态/反馈/更新诊断图明确，能力上限观察不当普适定理。
- `ortho`：分支/优势/ratio/聚合/lag单轴与交互不能假定正交，条件和全部成本清楚。
- `credit-example`：同anchor各4续写3/1成功、等权baseline.5、±.25信号完整，样本误差不冒充因果效应。
- `part5`：教师同历史/接管/过滤三介入位置与支持、sg/遗忘/成本充分，指向唯一OPD推导。
- `part7`：代码/GUI/科学状态差异与终局verifier边界充分，旧原稿入口保留。

范围与限制：检查现存教学比较和方法边界，不重新核验所有算法论文、执行分支采样或模型训练。

### dlm-survey

`content/series/dlm-survey/index.html` · `agent-multimodal-diffusion` · **保留**

理由：入口训练/生成图已说明本轮核心边界，无需机械加图。

- `#dlm-training-generation-map`：两条路径共享去噪器但训练loss不接成生成先验；监督目标与终点文本接口分开，保留图。
- `#foundations`：学习顺序、先修与教学算例而非实测边界明确。
- `#mastery`：核/预测坐标/块边际/codec/成本学习出口覆盖正文。
- `#source-policy`：原稿与固定论文对照边界保留，不重复维护型号榜。

范围与限制：完整阅读入口源；未执行任何语言扩散训练、生成或速度测试。

### transformer-decoder-flow

`content/posts/transformer-decoder-flow/index.html` · `architecture-inference` · **改稿**

理由：只补0/1可见矩阵到加性mask的转换解释，防止照公式直接相加而泄漏未来；完整forward、手算、代码、图、来源和旧原稿入口均保留。

- `#training-forward`：B2/T3/d4/H2/D2/F8/V5/L2贯穿embedding→拆头→mask→残差→head→4目标loss，行向量与PyTorch转置存储明确。
- `#numerical-forward`：二维一层、单位投影、关闭RoPE/epsilon0非零输入完整；8站数值、概率与额外EOS NLL1.826695逐步复算一致，不凭输入[A,B]虚构EOS监督。
- `#decode-forward`：prefill3位置后token3尚无KV，逐层本次输入/历史形状、offset与mask条件完整，旧K不重旋转。
- `#cache`：后段M定义0/1可见性而前式M为加性0/-inf，原文未显式转换，已补allowed与masked_fill对应及两增量行。
- `#parameters`：MHA/3矩阵FFN/两Norm/独立head条件完整；26848参数与KV3584B复算一致。
- `#code`：完整代码逐行核对Norm、相邻RoPE、mask、两残差、shift、缓存断言与生成；原代码块字节保留，AST解析通过，不称实际执行。

改动：

- `#cache` · `explanation`：明确0/1 M对应bool allowed，前向加性M为可见0/屏蔽-inf；给S3/T2两行allowed并对应现有masked_fill。

范围与限制：完整主讲forward、手算、decode/公式和全代码实际阅读；标准库独立数学复算不执行模型。当前python3无torch，仅AST/静态保留，不证明PyTorch缓存断言或三屏MathJax已通过；原科研图/URL/原稿链接未改。

### rl-interview-guide

`content/posts/rl-interview-guide/index.html` · `training-data` · **保留**

理由：复习页应维持短答与原理入口，当前边界充分；归档旧误述不回写到当前短卡。

- `symbols`：动作/观察、G/回报、behavior/old/current/ref和epsilon作用清楚，ratio方向是current/old。
- `pg-to-ppo`：短卡准确接到PG/GAE/GRPO/DPO/OPD完整主讲，不需重复推导。
- `faq`：PPO正负只裁改善侧、辅助loss/共享参数仍作用，全同组/std受有限G约束、KL并非普遍必需等短答充分。
- `classic-rl`：DQN2.8目标/terminal1与sg、连续/离散旁支界限明确。
- `sources`：历史稿/下载与当前主讲修订关系清楚，保留旧URL。

范围与限制：检查口述机制、条件、例子与原理链接；未重新认证所有历史问答/科研事实或真实浏览器深链接。

### agent-harness-guide

`content/posts/agent-harness-guide/index.html` · `agent-multimodal-diffusion` · **保留**

理由：状态恢复、上下文与记忆版本边界已有完整教学流程和图，没有必要再添加抽象状态图。

- `#codex-loop`：run_turn/工具路由/观察回填、call/job身份、继续条件与原SVG控制回路已说明，保留。
- `#sandbox`：超时不等于未发生、先查询外部状态、幂等/补偿、预算不重置的恢复链与例子充分。
- `#codex-compaction-branches-map`：摘要A与无摘要B互为配置选择，不串行；文件/进程/副作用不自动恢复，保留已有分支图。
- `#codex-memory`：读取/写入、后台两阶段、SQL选择非向量检索、V1/V2字节预算及明确更正均有固定版本条件。
- `#mapping`：精确token/span/prefix与动作/观察、SFT/RL/有效长度mask已分开。
- `#lab`：0.67/0.715加权记忆教学例及2×2训练/外部记忆对照明确，完整模板和引用保留。

范围与限制：通读本地Harness源及源码节选/模板入口，复算预算与加权score；未再抓固定Codex源码、验证托管backend、执行工具恢复实验或训练。

### distributed-training-guide

`content/posts/distributed-training-guide/index.html` · `training-data` · **保留**

理由：本实现参考已显式限定模型/API/版本与未运行条件，状态数学由主讲承接，不补伪可运行跨版本配方。

- `deepspeed`：auto属集成约定、stage/offload区别、优化器不能双重推进及完整恢复条件清楚。
- `fsdp`：FSDP1/2版本、先shard再optimizer、PEFT冻结混合、Accelerator不重复包裹充分。
- `megatron`：32卡TP8 PP2 DP2，global256需128microbatch，普通/专家视角与固定源码条件清楚。
- `example`：完整LoRA教学代码用attention mask保留真实EOS，不外部double shift；保存adapter关联base/tokenizer且不冒充续训状态。
- `troubleshooting`：OOM按状态/激活、NaN分母/精度、NCCL同步和恢复游标分别诊断，不用无出处历史tokens/s排名。

范围与限制：静态阅读配置/代码及拓扑算式；未pip安装、运行Trainer/DeepSpeed/FSDP/MCore、转换权重或验证GPU/NCCL。

### llm-interview-bank

`content/posts/llm-interview-bank/index.html` · `architecture-inference` · **保留**

理由：保留。架构/推理短答与代码卡已给关键条件和主讲位置，新增长例会重复；其余跨领域卡不据本轮阅读升级事实审阅状态。

- `#sec-overview`：短答、机制、反例和实验四节点图明确，完整推导归主题主讲，原470问原稿入口保留，不把题库作为另一个长课程。
- `#sec-llm`：Attention/key轴、GQA缓存/TP复制、RoPE、Norm、SwiGLU/MoE、sampling、具体型号的条件与主讲链接齐全。
- `#sec-infra`：分页/复用/调度、PD/容量、投机概率修正、量化对象、训练并行与状态边界短答充分，不重复服务算例。
- `#code-ce`：一次shift、ignore=-100、空有效目标拒绝和稳定logsumexp条件明确，与基础章修正后的平均目标一致。
- `#code-attention`：Hq可整除Hkv、repeat教学开销、allowed True可见、全屏蔽拒绝、key轴softmax完整。
- `#code-norm-rope`：FP32统计、相邻RoPE偶数维和position条件、SwiGLU与LoRA形状明确；本轮只作静态阅读。
- `#code-sampling`：tau0 greedy、top-p跨阈值首token、top-k ties及非有限logits上游检查已有追问，未冒充生产完备采样器。
- `#code-online`：m=-inf/ell=o=0、重标两累计量及遮挡块条件齐全，关联具体Attention主讲已有完整算例。

范围与限制：实际检查overview、sec-llm、sec-infra及CE/GQA/Norm/RoPE/sampling/online代码卡；全源只静态保留代码/ID/引用。未执行PyTorch卡，未逐题重新核验RL/VLM/Agent/RAG等全部历史问答、公司频次或论文性能。

### vlm-knowledge-interview

`content/posts/vlm-knowledge-interview/index.html` · `agent-multimodal-diffusion` · **改稿**

理由：主体原理、完整算例与接口图已充分；只补平均loss可定义条件、padding二维逆映射和返回总数三个确证复算/接口缺口。

- `#clip-siglip`：双向softmax/score梯度与两对算例、scale只用一次清楚，独立复算。
- `#siglip`：pair logistic、/N非/N²、正负导数与通信边界完整。
- `#vlm-fusion-paths-map`：三接口是各自支路，不串行；视觉state/KV、codec与生成目标边界明确，保留图。
- `#sec1-4`：补有效目标非空分母与padding/忽略标签处理，仍保留视觉梯度链。
- `#sec1-5`：完整数patch/crop/thumbnail/merge、帧与时间，沿用空间可见性图。
- `#sec1-6`：补单位/bin→处理图像素→减padding→逆resize→加crop的二维复算；原图与GUI点击单位不混用。
- `#code2`：半开image region、query/key和True语义、多层泄漏条件说明保留，原代码不改。
- `#code3`：补max_tiles只约束crop、thumbnail使总返回最多max_tiles+1的真实代码合同，原shape例保留。

改动：

- `#sec1-4` · `explanation`：补m_t排除padding/忽略/无效标签、有效目标分母>0与空监督显式处理；跨样本/rank按声明目标数聚合。
- `#sec1-6` · `worked-example`：补含padding的二维像素逆映射得到(116,62)，说明归一/bin先转单位、GUI逻辑点/窗口/屏幕接口另映射以及过期观察检查。
- `#code3` · `explanation`：说明max_tiles是网格crop预算，pieces+[thumbnail]另加一张；下游总数限制须预留缩略图并验shape。

范围与限制：完整阅读本地VLM源的原理、数学、算例、图和PyTorch代码；独立算术及布尔mask/网格逻辑检查，不运行PyTorch训练、模型processor、实际GUI点击或外部benchmark。MathJax运行、三屏与noJS产物待父任务。

### rl-interview-guide-legacy

`content/archive/rl-interview-guide/index.html` · `training-data` · **保留**

理由：用户限定archive历史原稿只读保留；明确记录确实读到的旧缺口，而非把历史页标为科学正确或改写归档。

- `symbols`：只读历史检查：G通常64等旧符号口径保留为历史；不能作为本轮当前配置结论。
- `ppo-detail`：只读历史检查：clip被绝对称停止更新/保守保证、GAE=.95实践最优等旧表述仍在；当前主讲有更精确分段与terminal处理，归档不改。
- `grpo`：只读历史检查：clip+KL缺一不可、critic显存直接翻倍、KL ratio方向和一/二阶解释、包含自身baseline无偏等旧口径不可当本轮通过；保留原件字节。
- `dpo`：历史Lagrange/Z消去推导完整保留；与先RM再PPO普遍等价的旧解释不扩用，现行DPO主讲限定偏好模型/支持/共享参数。

范围与限制：仅实际检查symbols、PPO/GAE、GRPO与DPO段落；不重审其余历史章节/原SVG像素，不修旧公式，不声称历史算法断言已通过或全面实验复现。

### dlm-ddpm

`content/series/dlm-survey/s00a_ddpm.html` · `agent-multimodal-diffusion` · **保留**

理由：完整标量输入到最终输出算例与两分路图已就近完整，无需新增内容。

- `#posterior`：完整阅读配方精度α/β、真实条件后验与未给x0的反向模型区别，A=14/均值/方差可复算。
- `#ddpm-training-sampling-map`：训练/采样分路、μ为固定坐标换算而非第二网络、t递减与ε/z独立，已有图足够。
- `#ddpm-full-example`：逐项复算加噪、MSE/梯度、真/模型均值、独立z采样、KL交叉检查和最后输出；两步末端非标准高斯先验的限制充分。

范围与限制：通读并独立复算标量教学链，不训练网络或复现DDPM论文实验；未运行MathJax/浏览器。

### dlm-flow-sde

`content/series/dlm-survey/s00b_flow_sde.html` · `agent-multimodal-diffusion` · **保留**

理由：条件监督→边际场图和完整高斯例已说明训练/推理与求解误差；时间方向就近给出，不重复作图。

- `#conditional-path`：噪声0→数据1、条件速度与后验边际平均定义充分。
- `#variance-proof`：条件方差常数与θ独立、交叉项为零及可积条件明示，不把样本直线当网络轨迹。
- `#flow-full-example`：完整高斯条件回归、常数方差、Euler0.2与解析0.180196可复算，保留已有例图。
- `#vp-sde`：SDE数据s=0→噪声s=1、逆向ds递减与score系数β/β/2分明。
- `#solver`：正向h>0/逆向网格、布朗√步长与固定ODE轨迹z区分，未发现时间方向缺口。

范围与限制：通读并独立复算解析教学例；未数值训练FM/score网络或重跑论文采样器。

### dlm-overview

`content/series/dlm-survey/s01_overview.html` · `agent-multimodal-diffusion` · **保留**

理由：具体状态图与分类轴已清楚，概览无需补新的数值或同类图。

- `#s1`：AR训练并行与生成串行、DLM轮内并行与轮间状态成本分清。
- `#ar-masked-state-map`：两独立四token生成路线、每箭头一轮、只示意不修改已提交值且不代表等分布/等耗时，保留图。
- `#lineage`：状态/核/因子化/预测/系统角色是可组合轴，不错画互斥家族。

范围与限制：完整阅读概览源与四token示意；不重新核验全部家族规格或速度。

### dlm-discrete

`content/series/dlm-survey/s02_discrete.html` · `agent-multimodal-diffusion` · **改稿**

理由：确证缺口是一般后验的支持域及预测分布如何接到一次反向抽样，其他已有推导和图保留。

- `#kernel`：行向量、Q每行和1、状态数含mask与uniform自返概率清楚。
- `#bayes`：补可达事件/正分母与干净预测支持条件，防止不可达项0/0混成后验。
- `#absorbing-example`：补0.6揭示质量乘0.7/0.3后的A/B/M分布及u=0.5→B，与干净argmax不同。
- `#weighted-mlm`：SUBS→KL→CE→1/t、长度与实际mask分母区别已完整，保留。
- `#llada`：候选重mask与已提交值carry-over的状态图足够，无需为三状态教学计算加图。

改动：

- `#bayes` · `explanation`：补条件后验分母>0、不可达事件未定义、混合支持由参数化约束以及已揭示SUBS分支。
- `#absorbing-example` · `worked-example`：在原0.6/0.4后验例之后，补A/B/M=(0.42,0.18,0.40)与累积均匀抽样0.5得到B，区分状态概率、预测argmax和真实目标。

范围与限制：通读并独立计算有限状态教学核、后验、加权CE与抽样；未运行LLaDA/D3PM/MDLM模型、训练配方或论文性能复现。

### dlm-block

`content/series/dlm-survey/s03_block.html` · `agent-multimodal-diffusion` · **保留**

理由：可见性矩阵、内外循环图和成本例已说明状态依赖，无需重复补图。

- `#factorization`：块间精确因子化不等于块内边际可算，块长1/L端点边界完整。
- `#attention-mask`：四tokenquery/key矩阵与clean/noisy前缀条件清楚，不能全部加噪冒充干净前缀。
- `#cache`：前缀依赖不变才可缓存，块内token相同不保证hidden相同，提交模式刷新已说明。
- `#cost-example`：8×4=32并另计8commit、4×8仍32却不同长度的完整计数例可复算，保留两层循环图。

范围与限制：通读并复算矩阵/调用教学计数；未测试实际KV等价、kernel、模型训练或缓存性能。

### dlm-continuous

`content/series/dlm-survey/s04_continuous.html` · `agent-multimodal-diffusion` · **保留**

理由：表示/生成/解码三层接口与现有两路径图充分，条件平均与离散输出已有反例。

- `#continuous-text-interface-map`：训练真实编码端点与生成先验分路、codec重建独立对照清楚，保留图。
- `#flow`：噪声0→数据1和速度符号，-1/3/t=.25→0、条件速度4与Euler1明确。
- `#rounding`：等概率-1/+1均值0不等于离散CE分布，密度与argmax单元质量分开。
- `#evaluation`：真实latent重建、生成终点与任务三组验收分开，未把codec错误归给扩散。

范围与限制：通读连续接口源并复算标量教学值，不重训codec、连续生成器或比较论文性能。

### dlm-paradigms

`content/series/dlm-survey/s05_paradigms.html` · `agent-multimodal-diffusion` · **保留**

理由：换算图和连续/离散算例就近充分，已有日程和分母限制，无新增图必要。

- `#vp-coordinate-map`：三坐标换算从同一预测分支出发而非连续训练，score要求s>0，保留图。
- `#loss-weight`：误差0.2→-0.15、MSE0.04→0.0225及a分母边界可复算。
- `#score`：条件score与真实边际后验平均区分，网络近似不写真实等号。
- `#discrete-score`：比率非softmax、广义散度保留r项，速度/比率/奖励不混用。
- `#discrete-flow`：两状态流入流出与0.1步长概率守恒例完整。

范围与限制：通读并复算VP与两状态教学值；没有训练SEDD/DFM或复現少步性能。

### dlm-scaling

`content/series/dlm-survey/s06_scaling.html` · `agent-multimodal-diffusion` · **保留**

理由：预算、条件和幂律推导已完整；新图或新拟合不能补未运行的实验，保留。

- `#scaling-budget`：unique U/处理D/epochs E、随机mask不创造独立事实与现有对照链图明确。
- `#compute-optimal`：固定C代入与求导后N/D幂次、α=β时随√C非√D，推导完整。
- `#crossover`：isoFLOP/iso-data/iso-time与复用饱和边界清楚。
- `#drafter-generalization`：过拟合与留出接受长度、容易请求选择偏差分开，保留。

范围与限制：通读并核算幂次及1B×100教学值；未拟合论文数据、验证crossover或测量FLOPs。

### dlm-speculative

`content/series/dlm-survey/s07_speculative.html` · `agent-multimodal-diffusion` · **保留**

理由：生成合同、完整计数与成本算例及现有循环图已充分。

- `#system-role`：AR drafter/DLM自加速/统一模型三个目标与现有draft/verify/commit图清楚。
- `#acceptance`：尾和与条件独立a=.8/b=4例、bonus/EOS/长度上限分开，复算2.3616/3.3616。
- `#cycle-cost`：期望时间/提交量比、8+25+2ms除5=7ms、1.43×可复算；不是接受长度直接等speedup。
- `#quality`：并行边际q不足以自动提供sequential proposal，标准精确随机/贪心协议区分保留。

范围与限制：通读并独立复算接受/成本教学值；未实测target/drafter、精确采样器或论文速度。

### dlm-elbo-rl

`content/series/dlm-survey/s08_elbo_rl.html` · `agent-multimodal-diffusion` · **保留**

理由：关键概率/界/教师角色已有充分推导和例子，未发现需新图的缺口。

- `#probability`：transition、路径与文本边际分开，调度概率也需入账；已有reward/更新图说明路径到文本，保留。
- `#elbo-gap`：Jensen下界差/MC方差/非线性ratio偏差不混用。
- `#spg`：固定优势正用下界负用上界，-2/-3/-1教学例不等式方向正确。
- `#gdsd`：倾斜特例、中心化token分数、冻结教师及reference项完整，不能当任意decoder文本概率精确化。
- `#diagnosis`：rollout/估计/更新三份随机性与新任务分母分开，论文数字保留历史来源。

范围与限制：通读并核算SPG不等式与二分类倾斜教学例；未复现SPG/GDSD训练、全部定理或性能表。

### dlm-commercial

`content/series/dlm-survey/s09_commercial.html` · `agent-multimodal-diffusion` · **保留**

理由：burst算例与时间线已有充分解释，不为时效性产品线索新增未经核验数据或图。

- `#evidence`：厂商声明/系统吞吐/用户完成时间和版本/硬件条件分开，不构成型号排名。
- `#latency`：200ms提交100token=500tok/s不等首字2ms，既有时间线明确首块尚未提交与外部验收成本。

范围与限制：完整阅读本地产品证据说明并复算burst教学值；未查询现价、API可用性或做线上测速。

### dlm-comparison

`content/series/dlm-survey/s10_comparison.html` · `agent-multimodal-diffusion` · **保留**

理由：本章承担综合复习和比较合同，算法图已在主讲位置，无机械增图必要。

- `#comparison`：机制/收益候选/成本风险表不把可组合路线误列成普适优劣。
- `#protocol`：unique/total、已支付AR初始化、NFE、并发、SLO和bound-PPL分开，可解释比较合同完整。
- `#research`：变化轴与待执行研究明确；总结表不需要再画重复算法图。
- `#interview`：六道短答覆盖1/t、块边际、坐标目标、SPG/GDSD与完整周期成本。

范围与限制：完整阅读比较与短答源；未重新运行Pareto候选、benchmark或训练对照。

### dlm-loop-transformer

`content/series/dlm-survey/s11_loop_transformer.html` · `agent-multimodal-diffusion` · **保留**

理由：状态/参数/计算、梯度与停止已有图和明确例子，保留。

- `#recurrence`：hidden循环不是噪声时间，输入持续条件与共享块反馈图清楚，保留。
- `#cost`：6层×4次=24调用但6份参数，激活/延迟与KV另计，复算。
- `#gradient`：共享θ每轮贡献与Jacobian乘积、0.5/2递推例方向正确。
- `#halting`：状态稳定不保证正确、推理超训练深度需留出验收。
- `#theory`：8元素2→4→8结合性非交换性、精度/均匀性理论边界已有说明。

范围与限制：通读并复算递推/调用教学值，未训练循环模型、核验所有原稿方法或复杂度定理。

### dlm-vae

`content/series/dlm-survey/s12_vae.html` · `agent-multimodal-diffusion` · **保留**

理由：训练/生成图、完整ELBO/重参数推导及量化算例充分，codec/控制边界已就近说明。

- `#elbo`：posterior训练/prior生成共享decoder图分支明确，改β后不自动是原likelihood下界。
- `#gaussian-kl`：μ=1/σ²=.25 KL=.81815、零KL与collapse区别，独立复算。
- `#vq`：最近码、codebook/commitment、STE前后职责与导数.4/-.4β清楚。
- `#quantization`：RQ残差、FSQ组合、LFQ位序与名义容量非有效使用量均有算例。
- `#system-role`：codec→latent生成→decoder与元素压缩1/48，视觉encoder非VAE，接口已讲清。
- `#cvae-robot`：训练可见未来动作posterior与推理z=0/观测分开，ACT不保证消除均值问题，保留。

范围与限制：通读并复算高斯KL、量化导数/残差和压缩教学数值；未重训VAE/codec、执行ACT机器人或复现论文。

### harbor-framework-guide

`content/posts/harbor-framework-guide/index.html` · `training-data` · **保留**

理由：所审执行/反馈/产物/分母链路已有原图、固定源码与小算例，保留不扩大项目/数据集调研。

- `summary`：2026-11-14快照、release/main和benchmark/框架对象分开，不把更新数量称纯模型效果。
- `ambient-error`：observed/native/ambient/corrected矩阵对齐、移除比例与污染比例不同，gap分母/单位及.625例明确；原数据是作者声明synthetic。
- `architecture`：SingleStepTrial原源码清晰给收集→separate停环境→verifier→shared停环境，原图caption区分异常与skip-grade。
- `verification`：artifact source/destination、tar filter、Worker权限、secure整数行[3,0,-2]与可信grader对应充分。
- `valid-denominator`：有效0/1与无效1的.5均值/2/3有效率、全无效未定义、should_grade/retry/reward_valid分开。
- `interaction`：多步骤文件状态保留与默认新conversation、早停步骤不贡献mean、GEPA仅validation recipe收益明确。
- `practice`：repeat/retry、全部尝试费用、artifact/regrade、canary和固定终评条件充分。

范围与限制：实际审阅概述、Science数学、执行/验证/有效奖励/重评分/多步骤/报告协议段；只复算教学gap和有效率，不执行Linux Worker、Harbor容器、17数据集、88adapter、历史重评分或任何榜单模型。

## T10c 默认字号修复

仅两张原SVG声明局部滚动和780px最小宽度，13px标签的静态缩放下限为12.07px。原图线条、文字、title/desc、ID与比例逐字保留；未执行新构建或浏览器矩阵，旧T10a/T10b证据仍仅适用于pre-repair指纹。

## T10d 状态标签字号修复

独立查看原target/context截图并以实际Chrome核对：3.3标题20.8px，FACT标签10.88px，本地JetBrains Mono，非SVG/MathJax。仅该标签局部设12px，不豁免语义状态文本、不改共享CSS或其它页。源文件单属性回退可恢复全部改前字节；新构建及受影响浏览器像素验收待父线程。旧b066f24的T10a/R6通过不得作改后current-pass，原失败报告和截图保持冻结。

## T10e 局部阅读修复

仅Transformer基础章平均masked梯度增加显式block横滚span，数学字节与符号说明不变；架构训练章原残差SVG外加局部横滚容器，1160px最小宽覆盖9px注记达到12px所需1152px内容宽及边框。原资源、图内字节、ID、语义、比例、caption及共享CSS不变。代码右端为缺滚动证据，旧构建诊断不等于新产品通过。保留Frontier的T10d最终修复与receipt；74源12改/62保留，24改动单元。旧42自动pass/1fail及架构41pass/13fail/6pending不转写新通过；父合并一次fresh build后重采19组及源影响范围，完整forward长段与状态表表体不在本次像素claim。

## T10h 箭头与交叉修复

仅ProtAgent机制SVG的六条流向补12×12实心尖端，history回线在x312处拱桥跨越调用reward竖线（y88–102留隙），observation另用x790出口到reward，消除原x750共线汇点。780px最小阅读宽度、840×200 viewBox、旧ID、全部节点文字、caption、正文与数值不变；desc仅补实心箭头和非汇合说明。改前SHA `8fd71a32ace679dd579419e3242ef400844a48ffdd972d5adbb8d0b0f203c596` → 改后SHA `85d72d0303ea38d90376fc2cf8aacff9eb193d29ad317f66881b71fab414852d`。74源12改/62保留、25改动单元；catalog既有摘要/2026-11-16日期仍适用，未改。原owner01六组fail、原截图与a4187c7 frozen build保持原输入范围，不改写为pass。静态源/几何/教学复算与精确凭据不证明当前像素通过；need_new_build=true，由独立owner在新目录构建并重验。

## T10p 主讲与参考续接

本轮起点仍为8014805源SHA `4e6d76d730a7d550013ddaf58778dca7b21c4992faec68b49a26da41f1b93792`；T10p修复前 `dff5f9efc55eeaaac7822cf49459e65db38588d938cc0552a147bcfeb0ae0d5b` → 当前 `c8721d825d295487ef03487e4364d6f18836daaff84c1c6133cfab8beb107bb3`。局部样式与主讲/参考角色构成同一实际修复单元，25+1=26，74源12改/62保留。原figure、object、caption、16个旧source ID及raw SVG字节保持；raw内部字线相交仍存在，不称已修好。默认HTML主讲与原生参考分别验收，旧manifest、plan197绑定、失败、review和PNG不改。当前仅源级集成；新构建/必要检查另存仓外证据，T10a最终、T10b及发布仍待后续唯一owner。

## T10x 完整报告目录续接

源第59行单替换 `552387af44bf3c0149bf131e8831d6f5b3be4580ebbcc493bac79dda5d785228` → `f44de32336f806dd4ca09acf0082f9c90761f4bb21461c4f5ef5bff71d2a0941`，760px改850px；只修761–850px目录浮动吸顶与既有单列布局不一致。74源13改/61保留、27单元，training-data模块29源6改/23保留；原模块和checks文件保持历史字节。catalog摘要仍准确、updated=2026-11-14为原内容日期，纯CSS修复不虚构科研内容更新。科学正文、图表、公式、原件、247冻结文件及两基线不变；旧9fa失败与观察保持原状态，新构建及浏览器/像素另存仓外真实证据。未提交或发布。

## T10y 无脚本数学说明续接

原27单元保持历史内容，精确追加4单元为31；仍74源13改/61保留。s07 `c8721d825d295487ef03487e4364d6f18836daaff84c1c6133cfab8beb107bb3` → `e1e1694fa3ebe4969551282a1f4292752a701e4cbc2fb69eeeb620a8fae07c44`。四块noscript只覆盖必要推导/复算，原字节和模块checks保留；catalog摘要仍准确、科研内容日期不变。当前仅登记与源核证，不声明浏览器、像素或发布通过。s01既有无脚本block递推/平均梯度失败不属于这四块，不自动关闭。

## T10z 必要无脚本推导续接

原31单元完整保留，精确追加2单元为33；仍74源13改/61保留。s01 `8330479acfddbcd8c5b1456bacb95f2f2230b066a3521899edc4033cf01708d3` → `a0e8f6d2fee1076ce3cc3a9514a6c504ed20aa29a26883cbc1618db81bdbc30b`。只增加noscript两处必要说明，catalog摘要和日期仍准确。原失败/待补及局部通过各自保留；源核证不替代真实浏览器、独立像素或发布。
