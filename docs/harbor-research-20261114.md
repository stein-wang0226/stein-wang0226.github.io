# Harbor Framework 与团队 Benchmark 调研依据

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
- Adapters已拆独立仓库；harbor-client为未发布package的开发预览，
  区别于Harbor包的内置客户端。

详细43项来源、访问口径与五段核心源码SHA在
`content/posts/harbor-framework-guide/assets/sources.json`。
源码Apache-2.0、本地字体OFL、ECharts及Mermaid上游许可均保留。

## 内容与案例

18节覆盖合同、Job/Trial、环境、verifier/Worker、error policy、ATIF、
regrade、Server/SDK/MCP、多步骤/模拟用户/Cookbook与团队benchmark。
直接嵌入安全求和、FreeCAD、music-harmony、ambient-rna-correction、
推理引擎、Rust compiler和GEPA/MedAgentBench。
科学任务摘录保留canary，不公开hidden truth或参考解；
原任务synthetic数据明确标注，不生成模拟性能。

三张结构图由Mermaid生成，内嵌SVG保持比例并对各图ID加前缀；
一张ECharts图采用真实官方计数，并保留静态表格与CSV。
正文、原生details、源码、表格及引用无需JavaScript即可阅读。

## 证据边界

完成的是公开来源核对、源码分析和HTML交付，不是模型训练、
科学任务复现或完整benchmark运行。团队报告、recipe示例与分析推断分别表述。
浏览器、构建与发布验证只证明对应技术范围。

## 本次验收

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
