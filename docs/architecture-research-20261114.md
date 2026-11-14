# 前沿模型架构调研与扩展依据

调研截止：2026-11-14。公开规格和性能均为来源团队报告，本次未训练、运行或复现这些模型。该记录服务于研究地图第06、07章及第03章关联阅读；发布状态须根据当次验收补充。

## 调研范围与证据

原研究地图的43项来源保留；新增28项，当前共71项：47篇论文、24项官方文档及模型卡/配置。来源清单位于 `assets/research/2026-11-14/sources.json`，编号是七章共用引用号。技术报告、模型卡和发布博客属于同一团队的一组证据，不能计为三个独立实验。单一团队规格在正文标为报告/配置口径；编辑综合判断与待执行实验分开呈现。

八个可公开分析的家族：DeepSeek、Qwen、Kimi、Nemotron、GLM、MiniMax、MiMo、Step；另列Gemma端侧路线及OpenAI、Anthropic、Gemini的披露边界。比较按历史表示、跨层信息、专家宽度、数值对象、多模态输入和端到端成本组织，不能把所有层都称为同一种Attention。

## 新来源编号

| 编号 | 依据 |
|---|---|
| 44–46 | Qwen3.8-Flash-Next官方发布、固定arXiv报告、固定模型卡/config |
| 47–49 | Kimi K3.1 Pro模型卡/config、Kimi Linear、Gated Delta Networks |
| 50–51 | Nemotron 3 Ultra模型卡/config、LatentMoE原论文 |
| 52–53 | GLM-5原报告、GLM-5.3-Flash模型卡/config |
| 54–55 | MiniMax Sparse Attention v2、MiniMax-M3.1-Flash模型卡/config |
| 56–59 | MiMo-V2.6、Step 3.5报告、Step 3.7模型卡/config、Gemma 4报告 |
| 60–64 | Attention Residuals、mHC、Muon/Moonlight、Kimi K2、Huginn循环深度 |
| 65–66 | AMD GLM-5.3-Flash MI300X服务实测、Z.ai架构发布 |
| 67–70 | GPT-6.1 Sol发布、Opus 5.5系统卡、Gemini 4 Carbon / Argon模型卡 |
| 71 | Qwen3.5-397B-A17B固定模型卡/config |

Kimi K3和Nemotron完整报告继续引用原编号5和33，不重新编号。

## 核对后的关键口径

- Qwen3.8-Flash-Next：125B主模型，另有51B n-gram表；6B activated。48层中36 GDN、12 global槽；global在CPT切为QSA。config仍使用`full_attention`字符串，不能据字符串认定实际kernel为稠密Attention。QSA压缩比4、indexer budget2048；4路GR；官方报告28页。官方GitHub固定revision `69885871a64393807d988b27b1b5e380e8f28526`，PDF封面2026-08-26；arXiv v1提交2026-08-31，文件未宣称逐字节相同。
- Kimi K3 / K3.1：2.8T总参数、104B activated；不能把“三万亿级”写成精确3T。K3.1固定模型卡列93层=69 KDA+24 Gated DSA；将K3的full-attention Gated MLA层替换为Gated DSA。896路由专家、top16、2共享专家；latent3584，hidden7168。Stable LatentMoE插入RMSNorm、SiTU-GLU以及Quantile Balancing。K3 Per-head Muon与K2 MuonClip不是同一个机制。
- Nemotron 3 Ultra：550B总参数、55B active；108是Mamba、Attention和MoE子模块总数，不能与其他模型的Transformer block数直接比较。latent8192→2048、512路由专家top22；预训练两个共享权重MTP头，released config一个共享模块。支持1M但config默认262144，模型卡给出开启长上下文的额外配置。NVFP4 fprop/dgrad/wgrad有高精度保留项，未证明全模型FP4。报告§2.7明确披露后期训练不稳定，切BF16并未解决。
- GLM-5.3-Flash：320B/18B、45层=34 KDA+11 DSA/MLA；3 dense FFN+42 MoE，288路由专家top8+1共享。IndexPool4；mHC。旧GLM-5论文不是新5.3所有结构的证据。AMD 2026-11-11报告独立核对配置；8×MI300X、vLLM0.31.0、96k输入/32k输出、并发256下DP8+EP8为4719输出tok/s，TP8为2317；是随机token服务测试，不是Agent成功率测试。
- MiniMax M3.1：428B/23B、1M；把前三个full-attention层改为MSA，MoE仍在前三层为dense；注意力与FFN分布必须分开。MSA是GQA group各自选block，不等同MLA或循环状态。MSA论文109B/3T训练对照以及H800 1M kernel的14.2×/7.6×不是428B M3.1端到端加速。
- MiMo-V2.6：Pro1.02T/42B，Flash310B/15B；主干70层=60 SWA+10 GA和48层=39 SWA+9 GA；窗口128、无shared专家。Flash/Pro不能笼统按5:1或7:1代替实际层表。diffusion drafter5层，anchor后7token、窗口1024；AdamW预训练，mid-training hidden矩阵改Muown，embedding/head/router继续AdamW；MXFP4 QAT在mid-training。公开蒸馏模型与RL代码不代表Pro/Flash所有权重已开放。
- Step 3.5：196B/11B，SWA/Full3:1、窗口512、MTP3；Step3.7约198B包含196B文本+1.8B视觉，45层、256K。3.5的训练报告不能冒充3.7单独完整报告。3.5报告披露Polar Express在BF16下罕见outlier，改其迭代到FP16后不再出现；不能推广成所有矩阵用FP16。
- Gemma 4：E2B/E4B、12B、26B-A4B、31B结构不同；有效参数不等总参数。12B独有encoder-free，48×48×3图块、40ms音频块通过projection进LLM；不是所有Gemma4都无encoder。Local/global4:1或5:1、KV sharing、global K=V有型号例外。
- mHC：Birkhoff双随机约束及谱范数性质属于理想residual mixing；20轮Sinkhorn为近似，整个带非线性更新的网络不因此得到无条件稳定证明。
- Muon：动量矩阵的polar/semi-orthogonal update，权重不做永久正交约束；Qwen融合矩阵先拆、Kimi按head拆；参数分工、数值精度、分布式梯度完整性和scale重调均有独立成本。
- Huginn：共享权重的recurrent depth是公开研究路线；闭源GPT的notes/history等harness状态不能推出Loop Transformer。Gemini Argon明确披露稀疏MoE Transformer，Carbon基于Argon；更细层计划、专家数等未披露项保留未知。

## 原件、许可与可重建性

新增原件：`nemotron-ultra-2606.15007v1.pdf`、`gdn-2412.06464v3.pdf`、`latent-moe-2601.18089v1.pdf`、`glm5-2602.15763v1.pdf`、`gemma4-2607.02770v1.pdf`。均核对CC BY 4.0，下载字节未改动，版本、长度、SHA和署名登记在来源清单。合计15份原件。没有明确转载依据的报告保留固定版本链接，权重许可不自动当作论文转载许可。

调研中间材料保存在仓库外 `/tmp/my-blogs-architecture-research-20261114/`，正式事实依据由版本化来源清单和本记录保留。

## 正文、图表与集成

第06章 `content/series/llm-research-map-2026/s06_architecture_landscape.html`：
版本速查、四种历史访问路径、GDN / KDA公式、实际混合层数量、逐家族分析、
Gemma端侧多模态、闭源披露边界及待执行对照。
第07章 `s07_architecture_training.html`：
AttnRes / mHC / GR、LatentMoE与payload推导、Muon矩阵更新和参数分工、
低精度对象、Huginn递归深度、Agentic RL联系与等算力实验设计。

七章按order 1–7登记；首页入口与博客搜索复用目录，DeepSeek保留URL并增加醒目关联。
原引用号1–43不变，44–71在统一索引追加；第45项官方PDF路径与注册记录一致。
第52项解析时丢失的团队名前缀已按全文修正为GLM-5 Team。
未修改原始迁移清单或其他文章保留SHA。

图表位于 `assets/research/architecture-20261114/`，由
`python3 scripts/architecture_figures.py` 生成4张SVG、2份CSV和来源关联JSON。
混合层柱状图为block数量，不代表实际层顺序、FLOPs或速度；
latent维度比仅支持固定token assignment与精度下的表示payload推导。
图表比例与现有文章样式一致，提供放大和下载入口，没有模拟性能数据。

## 本地验收

`make OUTPUT=/tmp/my-blogs-architecture-build check`：70页 / 123公开文件通过；
迁移核对：23项原SHA相同、18项已登记历史变化、299锚点、59标记保留。
当前12个本地集合、27章、6篇论文；本次不代表旧文科学断言全面复核。
图表连续生成逐字节一致，15份原件的长度与SHA全部匹配来源登记。
Chrome浏览器67项检查通过，具体范围与版本见 `docs/validation.md`。
本地预览 `http://127.0.0.1:8774/llm-research-map-2026/`。
发布结果以当次Actions与线上build-info核对为准。
