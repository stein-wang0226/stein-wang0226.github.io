# My Work 项目报告接入与复核

2026-11-14。本次将四项个人研究工作加入博客的独立 `/my-work/` 目录，
顶部导航位于“博客与笔记”和“CV”之间。修改保存在本地；没有创建 commit、
推送或触发 Pages 发布。其他任务已有的正文与引用改动继续保留。

## 来源与版本

| 项目 | 来源 commit | 原始报告字节数 | 复核重点 |
| --- | --- | ---: | --- |
| Holon | `7de0f4d67f9d18d166e715f6e4e200de22cb21ea` | 1,414,145 | MoT 路由、token 配比、CPT 预算、Negative Ladder 结论 |
| ProtAgent | `d66fa7c287d196d5c26ec23e53c02327c5bbc6a8` | 41,953 | assistant-only SFT、step return、论文附录与结果分母 |
| harbor-task-sync | `0efe0d276c6f4f2d804897843620ba7cb73974e7` | 42,457 | 当前 Unified-produce、方法合同、refinement 归因与停止 |
| trainable-dllm-overview | `28ed9621c93951f6032ce8a2ae28c115779ee918` | 2,298,865 | attention mask、Jigsaw supervision、论文与复算差异 |

全部来源通过已授权 GitHub CLI 读取。四仓库在读取时均为 private；
源码入口标注需要权限。详细文件清单、原 SHA-256、固定 URL、
适配链接与许可说明保存在 `assets/research/my-work/sources.json`。

## 正文与保留

- 四篇 `index.md` 分别解释问题、方法、输入与监督、实现、实验和限制。
- 四份 `full-report.html` 保留完整正文、公式、嵌入图表与原内联脚本；
  仅适配链接、原 CSS 作用域、报告容器和来源提示。
- 原始 HTML 逐字节归档为 `*-original.html.txt`；下载时恢复 `.html` 文件名。
- 187 个仓库相对链接固定到对应 commit。Holon 的三个兄弟仓库
  `Protext-Eval` 链接未在当前快照内，保留文字与缺失说明，不生成虚构目标。
- LM1B `scatdiff_mask` 只比较 offset 与 x0 side，未比较 block id；
  同 offset 跨块可见。方法总结和完整 DLLM 报告提示这一实现差异，
  原概念描述与逐字节原件仍保留。
- ProtAgent 主模型 61.00%、三种子均值 61.40% 与 PFUA ROUGE 分开；
  Harbor 原稿库存和成本不改成当前实时统计。
- 原件比对确认 SVG 18/3/1/0、MathML 57/0/0/0、IMG 0/0/0/3
  的数量一致，图片 src 和原内联脚本一致。

`review_status=reviewed` 仅表示上述明确范围对照了报告、实现或台账；
没有新执行训练、科学 task pipeline、OOD 评测或全部论文图表的独立复算。

## 接入实现

项目身份、正文、URL 和关联仍只在 catalog 登记。目录由
`views.render_my_work` 从 `Personal Project` 标签生成；页面内容来自
`content/pages/my-work.md`。`pipeline.render_academic` 装配页面；
共享导航根据配置中的 My Work 前缀标出 active，项目页不再同时标出博客。

局部样式位于 `assets/site/my-work.css`。完整报告原 CSS 限定于
`.work-original-report`，Holon 原固定目录改为正文内 sticky，避免覆盖顶部导航。
HTML 检查器区别页面 `<title>` 与 SVG 无障碍 `<title>`，仍拒绝重复页面标题。

## 实际验收

- `make check OUTPUT=/tmp/my-work-blog-build-20261114`：
  governance 与全站 106 HTML 页面、207 public files 的构建和链接检查通过。
- `scripts/test_pipeline.py`：13 项通过，含 SVG title 回归、隔离构建、
  失败保留、引用、来源版本和资源检查。
- 实际 Chrome/Playwright：390/768/1440px × 12 页面，36/36 布局通过；
  包含首页、博客、关于、项目目录与全部八个项目页面。
- 13 项交互检查通过：键盘打开、完整报告、证据展开/收起、简洁模式、
  展开后表格筛选/清空、导航返回、博客检索及无 JavaScript 阅读。
- 没有页面 JS 错误、横向整页溢出、图片缺失或科学图表比例异常。

构建与浏览器产物均位于仓库外；本次构建保留真实 HEAD 与 dirty 标志，
不是线上部署证明。临时证据目录为 `/tmp/my-work-research-20261114/`。
