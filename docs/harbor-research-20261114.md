# Harbor 评测体系与研究进展：调研依据

日期：2026-11-14。独立专题公开地址 `/harbor-framework-guide/`。
范围限定 Harbor 框架与团队相关评测工作，不替代通用 Agent / RL 综述。

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
一张ECharts图采用真实官方计数，并保留静态表格与CSV。
正文、原生details、源码、表格及引用无需JavaScript即可阅读。

## 证据边界

完成的是公开来源核对、源码分析和HTML交付，不是模型训练、
科学任务复现或完整benchmark运行。团队报告、recipe示例与分析推断分别表述。
浏览器、构建与发布验证只证明对应技术范围。

## 修订版验收

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
