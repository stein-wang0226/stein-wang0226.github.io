# My Work：内容完整度与 HTML 渲染复查

2026-11-14。范围为四篇方法总结及四份完整报告。
基准是 `docs/content-contract.md` §2–5 与 `docs/design-system.md`；
这些是本站内容与阅读标准，不是期刊录用、科学效用或独立复现认证。

## 结论与本次改进

原方法总结已经覆盖研究问题、方法路线、主要结果、固定来源与限制，
但术语、从输入到 loss/判分的例子和工作产物总结不够充分。
完整报告包含更多原始技术细节，其中 Holon 有 21 节、ProtAgent 有 13 节；
它们不能代替面向初次读者的知识解释。

本次在四篇总结新增概念讲解、机制 SVG、具体例子、公式解释、工作产物与
未完成证据表、按需基础阅读。完整报告由 `reading.project_learning` 从
总结的 KNOWLEDGE / EXAMPLE / REVIEW 标记装配三个知识区；
知识稿只有一个权威源，原报告源码与逐字节原件保留。

| 项目 | 技术展开与知识补充 | 工作复盘重点 | 仍需的科学证据 |
| --- | --- | --- | --- |
| Holon | Tokenizer/条件/监督区分；MoT 的 gather→投影→scatter→attention；T2P/P2T 样本到 CE；配方与实际暴露；真实 margin 算例 | 参数路由、混合 CPT 校准、active FLOPs 与分层条件利用评测 | 跨训练 seed、监督 token 暴露、strict protein-OOD 与结构/SFT 各分支实验闭合 |
| ProtAgent | 真实 tool loop；assistant-only SFT；score-function 梯度；重复调用的 step/episode return；mask、normalization、KL 与 reward attachment | 四臂、主 checkpoint、全样本分母、工具禁用及独立 PFUA 协议 | 独立生物正确性、工具数据库泄漏审计、完整权重/rollout/数据库及 matched reward 组件消融 |
| harbor-task-sync | Fixture/oracle/verifier 定义；公开/私有边界图；矩形包络与完整路径接受域；组学输入到交付；pass@k 与选择偏差 | 来源、联合一致性、独立盲测、生命周期/交付及反事实停止机制 | 每个历史任务的完整审计、有效难度效应、独立训练与留出科学收益 |
| Trainable DLLM | AR/MDM 可训练性；attention/loss mask 区分；两块 Scatter 实际边集合；Jigsaw 熵与监督密度；PPL/整盘成功/NFE 解释 | 受控任务、LM1B 逐格来源及 smoke/质量复现区分 | 缺失主图运行、seed 选择/profiling、D3PM 逐样本数据、SEDD 差异及完整 Test-PPL 日志 |

这些缺口不是用写作可以补成的实验结果。报告、源码与台账来自同一项目，
属于一手内部交叉核对，不能算三个独立复现来源。本次未运行 GPU 训练、
生物学评价、Harbor pipeline 或新的论文质量采样。

## 可定位的技术核对

- Holon：`qwen3_navit.py` 的理解/生成投影；token-mixture calibration；
  Negative Ladder 结果表的 L3−L0 差值。真实差上差为
  `−0.0058518−(−0.0109934)=+0.0051416`，不改写成绝对 margin 优势。
- ProtAgent：附录的局部奖励 `+0.25/−0.30`、完成工具 guard 与四臂；
  ROLL `compute_discounted_returns` 的分组、排序、递推和恢复顺序。
  新例子的终止奖励 R 为符号，不伪造一条实验轨迹。
- Harbor：当前 refinement 记录中的联合一致性、规格错误反事实及
  parent/child 结论边界。输入到判分的例子是教学流程，不登记新任务。
- DLLM：`scatdiff_mask` 的三个 OR 分支；相同 side、相同 offset 的跨块边
  与 xt→x0 严格较小 offset。两块索引例子不代表新增训练或采样。

## 用户截图中的渲染缺陷

**根因确认：Markdown 正文没有站点阅读容器。** `pipeline.render_artifact`
原先输出 `<article class="prose">`，再被通用阅读层包裹，但 `site.css`
将排版规则限定在 `.site-page` 内。导读有自己的 reading-intro 样式；
正文没有继承行宽、字体、行高、链接颜色、表格与代码背景。

修复前的线上浏览器证据：正文父节点为 `reading-content`，段落行高为
`normal`，链接为 `rgb(0, 0, 238)`。以前的溢出/图表检查没有覆盖这些属性，
因此上一轮“布局通过”不能作为正文样式正确的证明。

现在 Markdown 用 `body.site-body` 及 `main.site-page.reading-markdown`，
正文最大宽度 900px，继承暖白/墨色/青绿色阅读样式，代码与宽表容器独立滚动。
只在 Markdown 层与新知识区加排版；不扩大选择器污染原科学 HTML。
机制图在小屏独立横向查看，保持比例和原生文字尺寸。

完整报告补充区的自动 heading slug 加命名空间，防止分段 Markdown
重置生成器而产生重复 `_1`。补充插在原标题处理之后，避免移动旧生成锚点。
图注中的引用使用真实 HTML 链接，避免原样显示 Markdown 语法。
引用汇总器先将 Markdown 解析为正文 HTML，再解析来源与使用位置；
来源锚点挂在对应链接，原 `ref-*` 地址仍然有效。

## 实际验收与证据范围

- `make check OUTPUT=/tmp/my-work-quality-build-20261114`：
  全站 106 HTML / 207 public files 的 governance、结构、链接、锚点与资源检查通过。
- Chrome/Playwright：390/768/1440px × 12 页面，36/36 布局检查通过。
  页面包括首页、博客、关于、My Work 与八篇项目页。
  新检查覆盖正文实际颜色/行高/行宽、完整报告三个知识区、重复 ID、
  导航、整页溢出、原图比例与图片加载。
- 48/48 交互检查通过：目录锚点、报告入口、知识例子和复盘展开、
  原报告跳转与返回、Holon 原证据/简洁模式、全部八篇无 JavaScript 阅读、
  四份完整报告的 CDN 失败回退、知识例子的直接片段链接；
  无 uncaught page errors，机制图图注没有未解析的 Markdown 引用。
- 原件检查：四个 archive 字节、原报告内 SVG/IMG/MathML 计数、
  图片来源和内联脚本一致；新 SVG 只来自知识补充，不计为原科研图。
- 浏览器证据及截图在 `/tmp/my-work-research-20261114/quality-local-report.json`
  与 `quality-*-local-*.png`；原件证据为 `preservation-report.json`。

构建、浏览器与 pipeline 回归分别记录，不把文件检查称为逐篇结论重现。
发布后另行核对线上版本、资源字节与 Actions，历史文档不是部署证明。
