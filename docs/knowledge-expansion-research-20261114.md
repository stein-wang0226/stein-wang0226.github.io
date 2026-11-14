# LLM / Agent 知识体系扩展：来源、分析与交付记录

调研截止：2026-11-14。权威实施范围见工作区 `.trae/documents/blog-llm-agent-knowledge-roadmap-20261114.md`，已审阅批准。

本轮交付调研总结、机制解释、科学任务合同与工业集群方案；不在本地真实执行模型训练、科学任务、rollout、SFT/RL 对照或 benchmark。站点构建和浏览器检查独立记录在 `validation.md`。

最终内容已完成：新增15章及3个系列入口，修订训练/数据旧章、8篇独立指南与DLM14章，
补60道题解，发布13份设计资源。以下阶段记录保留各次实际进度；
最终检查与发布以文末和`validation.md`的新记录为准。

## 证据与主要维护位置

基础机制在独立 `/llm-architecture/` 六章维护；具体新型号与 AttnRes/mHC/LatentMoE/Muon 证据复用研究地图第06–07章，V4.1 专章地址与引用号保留。训练阶段定义归训练系列，系统策略归 Agent 系统，部署归 serving；覆盖表与阅读路线只在研究地图 index 维护。

本轮原始源码基线保存于工作区外 `/tmp/my-blogs-knowledge-work/before/`，`before.json` 记录31个既有文章源文件的精确 SHA/字节，便于审阅有意增补。原始迁移清单不修改。

## 架构基础来源核对

| 来源 | 固定版本 | 本轮核对/使用范围 |
|---|---|---|
| Attention Is All You Need | 1706.03762v7 | 原始 encoder-decoder、scaled dot-product、head/FFN；现代 decoder 示例不冒充原报告实验 |
| Fast Transformer Decoding / MQA | 1911.02150v1 | 共享 KV 的推理带宽动机 |
| GQA | 2305.13245v3 | KV head 分组、MHA checkpoint uptraining 与质量边界 |
| RoFormer | 2104.09864v5 | Q/K 旋转与相对位置内积 |
| FlashAttention | 2205.14135v2 | exact/IO-aware；数学不等于任意浮点实现逐位相同 |
| GLU Variants | 2002.05202v1 | SwiGLU 门控 FFN 与三矩阵参数推导 |
| Switch Transformers | 2101.03961v3 | top-1、负载/容量与 selective precision；不把配方泛化所有 MoE |
| On Layer Normalization | 2002.04745v2 | Pre/Post-LN 的初始化梯度分析及 warm-up 条件 |
| RMSNorm | 1910.07467v1 | 不显式 re-center 的均方根归一化 |
| Mamba | 2312.00752v2 | 输入选择性状态及硬件算法 |
| Mamba-2 / SSD | 2405.21060v1 | 半可分结构、递归/并行连接 |
| Gated Delta Networks | 2412.06464v3 | 原文 HTML §2–3：外积、遗忘、delta、gated delta 与 chunkwise |
| Transformers Llama | v4.57.1，8cb5963cc22174954e7dca2c0a3320b7dc2f4edc | 通过 GitHub API 核对 L53–67 Norm、L143–156 MLP、L159–194 repeat/attention、L197–220 QKV 和 L268起 residual |

全部链接见新架构系列 index 的来源锚点。仅引用链接，不额外转载许可未确认的基础论文；源码片段保留 Apache-2.0 署名与固定文件链接。现有研究地图的型号报告/config/原件登记由并行架构调研维护，此处不把同团队多个页面视为独立复现。

## 推导与编辑判断

- 基础 MHA Attention 参数 `≈4d²`、两矩阵 FFN `2df`、SwiGLU `3df`：忽略 bias/Norm，要求实际 head/矩阵形状满足约定。
- 规划 KV 例子 `80层 × 8 KV heads × 128 channels × K/V × BF16` 得320 KiB/token/request；32768 token 得10 GiB。是选定规格推导，排除权重、workspace、碎片、临时区与复制。
- GDN 本文使用 `S∈R^(dv×dk)` 列向量约定；与其它章行向量约定转置等价。遗忘进入旧状态及 delta 读取项，避免漏乘 α。
- mHC 局部双随机约束不是完整网络稳定性证明；AttnRes 轴是深度，state mixer 轴是序列。
- 前沿系列不按参数量、层占比或单 kernel 数字排名；科学 Agent 设计分析明确标作建议，等待另行真实实验。

## 实施进度与验收边界

已写入架构6章与index、catalog记录、研究地图覆盖表和三条阅读路线、博客路线入口。它们暂时链接后续拟交付章节，因此全站验收须在其余章节及资源完成后运行；不得将此阶段视为已发布或链接检查通过。

后续来源、旧文复核范围、题库增补与实际验收将追加到本记录及 `content-audit.md`。没有吞吐、容差、科学参考结果和采购价格时，配置/结果 schema 保留空值与明确状态，不能生成伪造结果。

## 训练方法与科学任务设计交付

已新增训练第05章、科学任务第03–04章，并修订训练原01–04章的架构/来源交接、
角色与目标密度、轨迹准入/教师接口、异质RL/命名空间。训练index明确“四阶段+
一横向方法章”；数据与Benchmark index扩为四章，原27/52引用号保留。

| 一手来源 | 固定版本 / 位置 | 核对与使用范围 |
| --- | --- | --- |
| LoRA | 2106.09685v2 | 冻结底座、低秩增量；参数与激活收益分开 |
| QLoRA | 2305.14314v1 | NF4、double quantization、paged optimizer；65B/48GB仅原报告条件 |
| AdamW | 1711.05101v3 | weight decay与自适应梯度解耦 |
| ZeRO | 1910.02054v3 | 状态冗余分片；不将历史吞吐推至新硬件 |
| PEFT | v0.17.1，53c25fe4fdd7c6aa4b40db0560815ea570d32303 | `lora/layer.py` scaling、forward、merge；Apache-2.0简化摘录 |
| Megatron Core | core_v0.14.0，23e00ed0963c35382dfe8a5a94fb3cda4d21e133 | `parallel_state.py` L647–728普通与专家RankGenerator |
| verl | v0.6.0，ddd86f527a4af75095e4677b02b5aa272913a088 | `engine/megatron.yaml`实际字段、one-step-off-policy recipe；未联合运行 |
| AReaL | 2505.24298v5（2026-03-02） | 完全异步与staleness路线；不将v1/v5报告收益混用，也不外推本任务 |
| Qwen2.5-72B-Instruct | 495f39366efef23836d0cfae4fbe635880d2be31 | 官方config：80层、8192hidden、64heads、8KV、32768原生位置 |
| Qwen3-235B-A22B | 8efa61729e24bd65b1d152b5ab5409052aa80e65 | 官方config：94层、64heads、4KV、128专家/top8、1536专家FFN、40960位置 |
| GSE52778 | GEO访问2026-11-14 | 16样本、4供体×4处理；FPKM / diff与SRA入口，未下载数据 |
| airway | BioC3.23，1.32.0及vignette | `airway`计数对象文档63,677×8、STAR/GRCh37/Ensembl75、Union/fragments；区别其它对象 |
| DESeq2 | 2014原文PMC4302049；BioC3.23 / 1.52.0 | NB、dispersion/LFC与GLM；当前版本只核对页面，不运行分析 |
| edgeR | 2009/2010 btp616；2016 QL workflow version2；BioC3.23 / 4.10.7 | 基础exact-test与后续QL区分；v4方法引用由当前官方包页面确认 |

科学来源审计发现：BioC3.23 vignette中重新生成的中间元数据表打印16行、dex全
untrt；冻结`data(airway)`输出为8样本、4组正确配对。已显式保留冲突，实际包内
`sample_table.csv` / `colData` / 逐GSM语义核对是未来构建阻塞项；位置解析失效
只是解释假设，未运行GEOquery确认根因。airway1.30.0对应BioC3.22，
本方案明确选1.32.0 / BioC3.23，不将动态release代替固定版本。

按所选MCore源码修正计划中的简化“EP嵌DP”说法：普通层
`TP2×PP4×CP2×DP32=512`；专家层`ETP2×PP4×EP8×expert_DP8=512`，
后者cp=1，ETP=TP时expert_DP=DP×CP/EP。源代码检查只确认分组公式；
94层规划24/23/23/24、rank放置、模型转换、CP/EP与optimizer组合仍待实测。

资源目录`assets/research/scientific-agent-design-20261114/`共10个文件：7份JSON
（含3份Schema）与3份Markdown，全部显式登记在`site.json.assets`。
它们是来源审计、公共题面/完整输出合同、轨迹schema、集群/对照方案、失败分类与
成本schema，不是真实task package。fixture / reference / 容差 / run结果不存在，
未知时长、吞吐、价格、CPU配置和结果为null。128/1024 H100、长度、G=8和seed
设定为本文规划；Dense70B静态32.8125GB/rank为有边界的理想推导，非峰值。

本阶段实际检查：catalog唯一ID、related有效、三系列顺序1–6/1–5/1–4、
资源存在、7个JSON解析、HTMLParser解析3新章、普通/专家world size与94层加总。
全部通过。检查最初尝试使用bs4，但该库不在当前环境；改用Python标准库，
未增加依赖。当前全文仍链接待交付Agent/serving系列，尚未执行全站make check、
浏览器、迁移保留或发布验收；不能把本阶段标作已上线。

## Agent系统与推理部署交付

新增两个独立系列（各index+三章）。Agent按证据→规划→信任组织，服务按调度→
并行/精度→容量/成本组织；catalog显式登记8条，新增3个下载资源登记在site.json。
六章均包含机制、具体科学/服务例子、失败、评测、来源和自测。

| 来源 | 固定版本 / commit | 本轮范围 |
| --- | --- | --- |
| RAG | 2005.11401v4 | 检索与生成联合的经典定义 |
| Searching for Best Practices in RAG | 2407.01219v1 | §3–4的chunk、融合、重排与组合边界 |
| Self-RAG | 2310.11511v1 | reflection tokens与自适应检索 |
| Search-R1 | 2503.09516v5 | 多轮检索/观察mask；明确v1/v5指标变化，不混数值 |
| Agentic-R | 2601.11888v1 | 局部相关与全局答案utility、retriever/agent迭代 |
| Search-R1++ | 2602.19526v1 | prompt/reward/optimizer解耦、answer avoidance与任务依赖 |
| PROGRESS | 2608.00969v1 | teacher essential queries与覆盖奖励；代理目标不等于科学有效 |
| ReAct / Reflexion / ToT | 2210.03629v1 / 2303.11366v1 / 2305.10601v1 | 交互、语言反思、候选搜索；工具环境状态另设计 |
| Test-time compute | 2408.03314v1 | 难度自适应，数学任务证据不外推工具Agent |
| Agent安全设计模式 | 2506.08837v3 | §2–3六模式与隔离条件，非通用免疫 |
| AgentDojo | 2406.13352v3 | clean/attacked utility与ASR分母、版本边界 |
| PagedAttention / SGLang | 2309.06180v1 / 2312.07104v2 | 分页/共享与Radix复用，不套用历史吞吐倍数 |
| DistServe | 2401.09670v3 | PD/网络/TTFT-TPOT goodput |
| GPTQ / AWQ / KIVI | 2210.17323v1 / 2306.00978v1 / 2402.02750v2 | 权重方法与KV对象/格式，质量需独立验收 |
| Speculative decoding | 2211.17192v1 | p/q接受与拒绝重采样，贪心一致不同于采样分布精确 |
| Faiss | v1.12.0 e8234e563f1ecef5f036e83c3cfee366d3f1fbca | 官方1-Flat.py接口已读取；MIT简化摘录，未运行 |
| vLLM | v0.32.0 5df63a7203cdb9328d824a27b682e77c7b9928be | V1 scheduler L591起token/进度/抢占、KV manager L264起prefix/groups |
| SGLang | v0.5.23 297e54fd105e974cdf401e5b4d20253a22c16f90 | radix_cache L364匹配、L552–610回收/引用保护 |

vLLM releases/latest实际返回v0.33.0rc3，GitHub prerelease字段为false；
按名称排除RC后选v0.32.0（2026-10-18），没有将字段false解释成正式稳定版本。
曾探测v0.32.1但标签不存在，未采用；最终commit由实际API核对。
SGLang v0.5.23发布日期2026-11-02。当前版本组合未启动或联合验证。

容量CSV仅用官方模型geometry与本文N=70B理想近似。名义80GB/rank、预留16GB、
TP4、无prefix共享、8请求候选；BF16 32K历史2.5GiB/rank/request、理想上界10。
数据1byte的KV行排除scale，只是候选容量上界；并未宣称已启用FP8或有质量结果。
CSV、假设JSON、测量Markdown共3文件，没有GPU价格/吞吐/实际成功数。
构建契约不接受`.md`公开URL；四个Markdown源资源保留原格式，
以`.txt`公开路由逐字节复制下载，未扩大公开文件白名单。

本阶段静态检查catalog唯一/related、六HTML解析和四行容量计算通过。
全站build首次发现Markdown下载路由不符合契约，已按上面处理；
尚需旧文有限复核、60题答案、迁移差异记录与全站/浏览器/发布检查。
源码读取和规格推导不是模型训练、科学执行或服务benchmark。

新系列全部补齐后，`make build OUTPUT=/tmp/my-blogs-knowledge-build`通过，
实际为95个HTML页面/169个公开文件（包括并行任务新增的后训练专题）。
build装配和产物链接检查通过；尚未完成旧文/题库修订、
迁移保留、全套make check、浏览器及发布，不能作为最终验收。
发现并修正3处新链接：前沿应用章真实文件为`s05_agent_frontiers.html`，
架构报告来源锚点使用真实`#versions`/`#reading`。

## 旧文、DLM与题库的有限复核

8篇独立指南按各自职责补具体机制、例子及跨专题路径；14个DLM章节分别补
状态/目标/采样/实验边界，原AUTO标记、题目、原锚点和原件均需保留。
逐文件原始SHA在before.json，差异收据只覆盖实际改动文件，迁移manifest不重建。
没有把旧文状态批量改成reviewed。

核对SPG 2510.09541v1原算法1/§3：正优势乘ELBO下界，负优势乘EUBO/混合界；
原文“奖励减界形成优势”不是该算法，已替换。HTML正文内部date与arXiv v1日期
不同，不据内部日期重写版本。GDSD 2605.29398v1原§3式6–10：
冻结old/ref、共同masked输入、加性优势引导、token-level centralization；
修正旧公式将当前raw logit乘exp(A/β)的错误。引用原式10的practical目标，
单KL倾斜仅作教学特例；不把TIM-bypass写成任意条件的无偏保证。

DDPM纠正有限步逆向边缘“严格高斯”、KL漏常数以及不能跳步的表述。
VP v-pred按本节数据→噪声时间轴纠正端点；FM条件直线不等于边际流直线，
扩散也可以ODE采样。其它DLM模型/性能/Uniform方差与迁移断言保留显式复核缺口，
不是已经完成所有70+论文事实核对。

补60个具体题解，配额与问题号：
LLM12(4,6,8,9,10,11,12,14,15,18,19,22)；
Agent10(3–12)；RAG10(2,3,4,5,7,8,9,10,11,12)；
工程10(4,5,6,7,8,9,11,12,13,14)；评测10(1–10)；
AgenticRL8(5,6,7,9,10,12,13,14)。
静态逐字对照确认470个原q-item及95个原q-answer保留，
当前155答案、315缺口。无JS全部答案展示，JS就绪后再折叠/启用按钮。

新增一手核对：MemGPT2310.08560v2、Medusa2401.10774v3、
EAGLE2401.15077v3、Lookahead2402.02057v1、
ReTool2504.11536v2、ToolRL2504.13958v1、
R1-Searcher2503.05592v2、k1.5 2501.12599v4、
YaRN2309.00071v3、LongRoPE2402.13753v1、DPM-Solver2206.00927v3。
摘要只用于其明确机制范围；未从摘要复制统一性能。EAGLE最初候选2402.15769
实际为GenCode，已排除并通过标题查到正确ID，不引用误号。

`make check`首次暴露4个旧文新增链接误写文件名，已改为catalog真实route；
这属于站点链接失败，不能计入训练/科学实验证据。

## 最终内容与站点验收

独立快照基于`bae271a`，只装配本任务70个文件，排除未提交的管理协议、
Profile及后训练专题；`make check`通过88 HTML页/154公开文件，
迁移检查通过9项原SHA、32项登记变化、299原锚点和59原标记。
现有8项pipeline测试通过。Chrome检查52页×390/768/1440px共156项布局、
92项入口/导航/搜索/题解/下载检查、8项无JS阅读，均通过且无页面脚本异常。
13份资源逐字节SHA核对通过，3份Schema和其余JSON可解析；
470个原问题及95个原答案的保留检查见前文，当前155答案/315缺口。

截图复核保留现有Stein’s Notes设计；科学章节标题精简为“数据与验证合同”，
避免桌面单字换行。为基础架构搜索补充“Gated Delta Networks”完整名称。
早期浏览器脚本误用旧文单一h1假设、错误结果卡片选择器及不在索引中的搜索词；
按实际页面/登记改正，失败尝试不计入通过数量。
内置浏览器连接返回inactive execution round，改用本机Chrome/Playwright真实交互。

随后远端主分支已包含同期后训练专题，最终整合从`567654e`重新建立隔离快照，
保留已提交的六章后训练、共享交接和Profile极简设计，再纳入本任务内容。
没有把其他会话未提交的管理或Profile改动加入发布；最终部署以Actions和线上
`build-info.json`核对，不以共享工作树干净状态推断。

最终整合产物95页/169文件，163路由的迁移检查及256项Chrome验收全部通过。
实际输入digest为`68f1e3e099cef2dac71846c59909e17aedd5d063c02dca19f1fc349d5c6807b9`；
详细快照与公开部署核对协议见`validation.md`。

## 全站组织整合后的维护位置

2026-11-14 全站整合将现行路线、概念主讲与覆盖入口统一到 `/blog/`；
研究地图旧表及路线留在同页冻结参考，具体规则见 `organization-integration-20261114.md`。
