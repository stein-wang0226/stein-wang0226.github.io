# Harbor 评测体系与研究进展：调研依据

日期：2026-11-14。独立专题公开地址 `/harbor-framework-guide/`。
范围以 Harbor 框架与团队相关评测工作为主，另单列 scalingX 社区任务资源，不替代通用 Agent / RL 综述。

## scalingX 社区数据补充

按用户提供的 `https://huggingface.co/scalingX` 调研并整合。
17 套数据集在 2026-11-11 至 11-14 公开；每套固定 HF revision，
根据文件列表中的 `/task.toml` 统计，共 4,980 个目录。
其中 14 套 PR-diff 集共 4,769 个目录，按最后一级 owner__repo-PR
名称去重为 3,688 项；十个生命科学领域共 2,845 个目录、2,550 个 PR 名称。
这是名称去重，未做内容或语义去重，不能将总目录数称作独立任务数。
最大 cancer 版本 1,479 目录，660 / 1,000 目标仓库产出。

完整 17 项固定 SHA、API、数据卡、日期、计数与许可证元数据保存在
`content/posts/harbor-framework-guide/assets/scalingx-datasets.json`。
来源登记增加 11 项一手证据，Notes 由 44 增至 55 来源，
团队版由 18 增至 29 来源。Notes 仍为 13 节，团队版仍为 5 节；
社区资源分别放在覆盖章节和发布进展章节的 `#scalingx` 小节。
未将 scalingX 写作 Harbor 团队正式发布的评测。

抽查 cell2location-435 固定 ref，公开指令给出三文件 pandas / NumPy
索引修复步骤；任务元数据为 unverified / generation、
validation_not_run、空 evidence。默认评分权重
format / size / file / region / similarity / judge =
0 / .08 / .12 / .20 / .10 / .50，并有补丁规模等限制；
缺少 judge 或评分基础设施失败时无有效 reward、标 ungraded。
该分数不是功能测试通过率。Python slim Dockerfile 不安装科学依赖，
尚需环境、oracle 和功能测试校准。

科学原型三套为 AgingBench 100、Cell Response 31、闭环 Taskset 80。
抽查 aging 文本统计任务、Cell Response 根目录 Dockerfile 与 PASS-only
verifier、uvvis-01 无标准环境 Dockerfile，分别说明科学内容与运行合同边界。
闭环观测由真实统计量驱动的前向模型模拟生成，非湿实验测量。
上述判断为样本静态阅读，不能外推全量任务状态。
数据卡旧“未 push”措辞与实际已公开文件分开说明；
少数 Apache 元数据不外推第三方代码及输入数据许可。
本次未运行 Docker、Harbor rollout 或 LLM judge。

本次整合验收：`make check OUTPUT=/tmp/my-blogs-harbor-scalingx-build`
通过，97 HTML / 192 public files，新增清单已登记资源 allowlist。
Notes / 团队版在 390 / 768 / 1440 px 共六组浏览器检查通过：
社区锚点跳转、17 项清单展开、四行团队概览、55 / 29 来源、
无页面横向溢出、错误或外部资源请求。既有三张链路图与计数图
仍可读，放大 / Escape 与来源筛选通过，无 JavaScript 时图与正文可读。
团队单文件为 33,864 bytes，复制到 `/tmp` 独立验证，无脚本或资源加载依赖。

## 来源与版本

- Harbor 正式发布 v0.26.0，2026-11-13T23:49:24Z，tag commit
  `3cb627394b95d3ae605f31e0d694edf508cf4b7b`。
- 核心源码阅读 main `ec6aeab7fe0eb51df52b4e72c524daf5ea9cc5f4`，
  比 release 多五个提交。文章明确区分 main 取消修复与发布功能。
- TB 4.1.0 标签 11-03 / 公告 11-09，full66 / CPU63，全部modified；
  重评分162初始变化，134采纳（89FN、45FP），28测量差异保留旧分。
- Science 正式 release 仅v0.1.0 /70；main README96活跃任务；
  当前贡献页0.2/1.0准备中，2.0截止12-15。旧公告0.2/10-05不作现行roadmap。
- HarborIndex 1.4 /80题，与论文初版82题及54/6627大规模研究分开。
- Adapters 已拆独立仓库；README 标注 85 个 adapter，本次逐项核对固定
  `40b140eab2aae7375b2369aeddd2f8b3f872e2da` 的 `src/` 实际有 88 个目录。
  目录存在不等于逐项可运行或采用上游最新版本。
  harbor-client 为未发布 package 的开发预览，
  区别于Harbor包的内置客户端。

详细 44 项来源、访问口径、88 项适配目录与五段核心源码 SHA 在
`content/posts/harbor-framework-guide/assets/sources.json`。
源码Apache-2.0、本地字体OFL、ECharts及Mermaid上游许可均保留。

## 内容与案例

修订为 13 节，以最新 benchmark 概览与各项目分析为主体：
Terminal-Bench、Science、Challenges、HarborIndex，然后介绍框架近期更新、
评分可靠性、持续评测与优化示例。基础 Task / Job / Trial 压缩，
完整单步骤链路与源码可展开。
主表只列团队维护的四类评测，Challenges 展开为三个单项目，共六项；
使用 Overview、版本与内容、最新进展和直接引用链接。
88 个外部适配目录独立展示、可筛选，并注明与 README 85 的计数差异。
直接嵌入安全求和、FreeCAD、music-harmony、ambient-rna-correction、
推理引擎、Rust compiler和GEPA/MedAgentBench。
科学任务摘录保留canary，不公开hidden truth或参考解；
原任务synthetic数据明确标注，不生成模拟性能。

三张结构图由 Mermaid 生成，内嵌 SVG 保持比例并为各图所有 ID 加前缀。
单步骤图补齐 shared / separate、跳过验证、异常恢复和 finally 收尾；
独立验证图补齐交接约束与 Worker 的可选范围；
复用图先检查实际任务变化，再列出 regrade 前提、无效记录和 TB 4.1 的特定回退规则。
图中使用原生 SVG 文本，避免 foreignObject 继承正文样式后出现裁切。
三图均可在对话框放大、滚动查看，以 Escape 或按钮关闭。
一张原生 SVG 柱状图采用真实官方计数，并保留静态表格与CSV。
正文、原生details、源码、表格及引用无需JavaScript即可阅读。

## 证据边界

完成的是公开来源核对、源码分析和HTML交付，不是模型训练、
科学任务复现或完整benchmark运行。团队报告、recipe示例与分析推断分别表述。
浏览器、构建与发布验证只证明对应技术范围。

## 最终收尾验收

- Notes 保留 13 节、44 来源与基础讲解；团队版独立编辑为
  “Harbor 评测发布与进展”，5 节、六项主表、18 项关键来源。
  团队版以评测发布、项目进展与代表案例为主，框架压缩为两段；
  不包含完整目录清单、基础执行链路或源码教程。
- 团队单文件 `/Users/bytedance/Desktop/my_blogs/harbor-benchmarks-20261114.html`
  为 26,251 bytes。无脚本、字体或资源加载依赖；复制到 `/tmp` 独立打开，
  无外部请求。原导出目录的同名入口同步更新。
- 实际复现移除 SVG 样式后的黑色节点 / 连线；为三图写入明确的
  填色、线宽、字体和箭头样式，并修复分支标签背景继承文字颜色的问题。
  截图逐张复核节点、箭头、分支文字与完整边界，不再仅检查 viewBox。
- 计数图改为原生静态 SVG，无 JavaScript 时仍显示；不再依赖 ECharts 初始化。
- `make check OUTPUT=/tmp/my-blogs-harbor-polished-build` 通过：
  97 HTML / 191 public files，governance 11 份协议通过。
  本次基线为 `ffb2bd5`，构建时含本专题未提交的修改。
- Notes 与团队版 390 / 768 / 1440 px 共六组检查通过：
  无页面横向溢出、脚本错误、缺失资源或外部请求；
  Notes 三图无文字越界，连线无填色、线宽小于 4px，
  标签为白底深色文字；移除 SVG 内样式表后仍可读。
  三图放大 / Escape、引用筛选、团队版引用展开均实际操作通过。
  关闭 JavaScript 后四张图均可阅读。

下列修订版与初版验收保留为历史记录，其导出大小及依赖不代表最终团队版。

## 前次修订版验收

- 标题改为“Harbor 评测体系与研究进展”，公开 URL 保持不变。
- `make check OUTPUT=/tmp/my-blogs-harbor-revised-build`：通过，
  96 HTML / 187 public files；catalog、链接、锚点与资源 allowlist 通过。
- Notes 与团队版分别验证 390 / 768 / 1440 px；正文无页面横向溢出、
  无脚本错误、无缺失资源；13 节、主表六项、44 来源、88 适配目录。
- 三张 SVG 所有文字均位于 viewBox 内，无 foreignObject、无重复 ID，
  实际宽高比与 viewBox 一致；实际点击三图放大并用 Escape 关闭。
- 适配目录筛选 / 清除、源码展开、来源筛选 / 清除均通过；
  关闭 JavaScript 后全文、88 项目录、源码、三图及静态计数表可读。
- 团队交付为真正的单文件
  `/Users/bytedance/Desktop/my_blogs/harbor-benchmarks-20261114.html`，
  约 1.6 MB。内嵌脚本、字体、SVG、JSON / CSV 下载与许可；
  无 Stein’s Notes 导航、关联阅读或品牌文字。
- 将单文件复制到 `/tmp` 后独立打开，加载无外部 HTTP 请求；
  实际下载 `harbor-sources.json` 并核对 44 来源与 88 项目录。
- 修订版基于随后发布的管理协议提交 `3406fc7` 同步；
  与该基线的差异仅为本专题正文、catalog、资源和本研究说明。
- `make check OUTPUT=/tmp/my-blogs-harbor-final-build` 在该基线上通过，
  包含 governance（11 份协议）与 96 HTML / 187 public files 的构建检查。

## 初版验收记录

下列为修订前的历史检查，不代表修订版的节数或来源数。

- `make check OUTPUT=/tmp/my-blogs-harbor-build`：通过，78 HTML /156 public files。
  所有正文链接、锚点、导航、catalog与资源allowlist通过。
- Chrome 390/768/1440px：无页面横向溢出、无页面脚本错误与缺失资源；
  三图保留viewBox比例；正文18节、8个details（含目录）、43项来源。
- 实际点击源码展开、章节跳转、来源Worker筛选与清除均通过；
  关闭JavaScript后源码、静态图、数据表与43项来源可读。
- 离线HTML采用本地字体及JS，加载时没有外部HTTP请求。
- 博客目录已出现独立入口。截图复核后压缩重复站点标题，
  保留博客路径、报告封面、完整目录和三图大图链接。
- 发布基于最新远端 `f5d3821`；再次构建通过96 HTML /187 public files，
  并重复核对专题390/768/1440px、交互、无脚本与离线资源。
- 当前主工作区 `make governance` 通过（11份协议文档与本地登记）；
  仅精准增加本专题catalog与8项资源记录，原JSON内容保持原值。

验证脚本、截图与运行日志位于仓库外，不作为正文或科研实验结果提交。
