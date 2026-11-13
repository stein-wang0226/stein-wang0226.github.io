# Stein's Notes 界面恢复与验证

日期：2026-11-14。范围：博客入口、首页、公共导航、卡片、目录筛选及阅读页公共外壳。

## 设计依据

按原 Stein's Notes 的暖白、墨色、青绿色与排版恢复视觉身份：

- 背景 `#f7f5f0`，正文 `#1a1a2e`，强调色 `#0d9488`。
- 博客入口采用两行 `Stein’s / Notes.` 字标、主题按钮、宽搜索栏与双列笔记卡片。
- 推荐训练系列直接展示四个章节；其他系列保留章节入口。
- 首页使用个人介绍、主题入口、推荐阅读与紧凑的最近更新列表。
- 手机改为单列，保留导航、键盘焦点、搜索、系列链接与正文阅读。

采用用户指定的 Anthropic `frontend-design` 指南：
<https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md>。
安装来源提交为 `2c5958ecac7cee2b583967a2c4981d0f4a75c579`，全局安装目录为
`/Users/bytedance/.trae-cn/skills/frontend-design/`。

科学文章正文、公式、图表与公开 URL 不在这次设计改动范围内。
个人介绍、CV、论文与新简历的内容更新单独验收；本记录不代表那些内容已发布。

## 字体与许可

字体以 WOFF2 存放于 `assets/site/`，页面不依赖外部字体请求。
拉丁标题使用 Sora，正文使用 Literata，日期和编号使用 JetBrains Mono；
中文使用系统字体回退。字体保留 SIL Open Font License：

| 字体 | 上游字体资料 | 仓库许可文件 |
| --- | --- | --- |
| Sora | <https://github.com/google/fonts/tree/main/ofl/sora> | `licenses/Sora-OFL.txt` |
| Literata | <https://github.com/google/fonts/tree/main/ofl/literata> | `licenses/Literata-OFL.txt` |
| JetBrains Mono | <https://github.com/google/fonts/tree/main/ofl/jetbrainsmono> | `licenses/JetBrains-Mono-OFL.txt` |

## 隔离验证

共享工作区当时同时存在个人资料更新。为准确验证本次发布，使用独立暂存索引导出设计范围，
基于 `2e6bfce94c4825b955d09e680a3722aa9973d71c` 构建，未包含同期未提交的个人资料改动。

构建输入指纹：
`0450ed269e48340e82ee6fd8186df7479fc321d09d8c4912a68ecc07ec4fc37b`。
验证时记录为基线提交加本地修改；发布后以线上 `build-info.json` 的提交、dirty 状态及指纹为准。

| 检查 | 结果 |
| --- | --- |
| 构建与静态链接检查 | 57 个 HTML 页面、73 个公开文件，通过 |
| 构建流水线现有测试 | 6 项通过 |
| 原始迁移保留核验 | 27 项精确保留、14 项有记录的变更，通过 |
| 锚点、自动标记、兼容路由 | 299 个锚点、59 个标记、68 条路由，通过 |
| Chrome 布局 | 9 个页面 × 390 / 768 / 1440 px，共 27 项通过 |
| Chrome 交互 | 22 项通过，无 JavaScript 异常 |
| 无脚本或目录请求失败 | 4 项通过 |

布局覆盖首页、博客、个人介绍、CV、论文列表、Midtraining 章节、ELBO/RL 章节、
Transformer 数据流及 Agent Harness。检查页面宽度、图表比例、裁切与卡片列数；
同时目视检查首页、博客的三个视口。

交互覆盖主题选择、组合筛选、ELBO 章节搜索、标题排序、空结果、重置焦点、
刷新与返回后的条件恢复、旧查询兼容、键盘操作、跳转正文和真实章节跳转。
无 JavaScript 时保留原生主题选择、静态文章及章节链接；请求失败时保留同样的浏览入口。

原始浏览器结果位于验证机器的 `/tmp/my-blogs-browser-tests/design-report.json`，
截图为同目录 `design-{blog,home}-{390,768,1440}.png`。
这些临时文件不是站点源文件，也不作为未来版本的验收结果。

## GitHub 仓库职责

- `stein-wang0226.github.io`：统一网站及内容的主维护仓库。
- `stein-wang0226`：GitHub Profile README 的展示仓库。同名仓库需保留，
  才能继续显示个人主页 README；其维护稿可以集中在主仓库的 `docs/github-profile/`，
  发布时再同步到同名仓库根目录。
- `wyx0226.github.io`：旧学术站和历史提交。有效内容已迁入主站，但原提交历史没有合并；
  旧项目 Pages 仍可能占用 `/wyx0226.github.io/` 前缀。

截至本次核对，同名仓库 README 最后推送于 2026-07-23，个人网站字段仍为旧前缀；
主仓库中的新 Profile 稿尚未同步到 GitHub。不能把主站发布等同于 Profile 更新。
保留旧仓库并归档是可选后续操作；停用旧 Pages、设置跳转与删除仓库分别处理，
本次界面发布不改变旧仓库状态。

## 发布后缓存修复

首轮设计提交 `25d7781f018ae205ce64d20b0e50632f56394821` 的校验与 Pages 部署均成功；
线上构建为 clean，输入指纹与隔离验证完全一致。真实浏览器随后发现，
新 HTML 与缓存中的旧 `catalog.js` 混用，造成主题按钮仍隐藏、推荐卡片被旧脚本改写。

公共页面和阅读外壳的样式、目录脚本、目录 JSON 请求现在使用构建输入指纹作为
`v` 查询参数。任何权威输入变化都会生成新的资源 URL，避免旧缓存与新 HTML 混用。
文章自身未修改的历史样式仍沿用原链接。

期间主站的个人资料更新已以 `5801b4ea856c09077639230cffb37554c535a87d`
单独提交并部署。剩余缓存修复基于该版本验证，构建记录为该提交加本地修改；
输入指纹为 `60ccf96677eb8310ef75189fe0f2ec2f30c0af2b0ea18bbe59f3e1080ef02859`。

- `make check OUTPUT=/tmp/my-blogs-design-build`：59 页、79 个公开文件，通过。
- 迁移核验：23 项精确保留、18 项有记录的变更、299 个原锚点、59 个原标记、
  73 条登记路由，通过；原有内容覆盖仍保留。
- 现有构建测试：7 项通过。
- 真实浏览器复测：扩散主题筛选、ELBO 组合搜索、重置与焦点恢复、四个推荐章节通过。
- 实际网络资源：`site.css`、`catalog.js`、`catalog.json` 均携带
  `v=60ccf96677eb8310`；Midtraining 阅读页的公共样式使用同一版本，页面无横向溢出。

最终线上状态以 `build-info.json` 为准。本节记录缓存修复的证据，
不将个人资料稿的提交等同于 GitHub 账户资料或同名 Profile 仓库的远端更新。
