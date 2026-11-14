# GitHub Profile 实施稿

更新日期：2026-11-14。README 源稿、静态配图与发布记录都维护在本目录；
实时状态使用 `python scripts/profile.py status --gh /path/to/gh` 核对。

## 已准备的输入

- `README.md`：用于 `stein-wang0226/stein-wang0226` 仓库根目录，替换过时的实习信息、论文状态和旧站链接。
- `settings.json`：仅更新 display name、bio 和 website。网站字段统一为根站，不再指向旧项目 Pages 前缀。
- 主站 `content/pages/about.md`、`cv.md` 与论文记录：已落实内容；中英文附件已接入下载。

README 使用主站的规范入口，不依赖外部统计图片。项目工作放在论文和学习笔记之前；
完整经历、实验口径与状态来源链接回主站，避免首页过长。
正式发布前必须先部署主站，因为 README 中的新增 PDF 与两篇稿件链接依赖本次主站更新。

## 仓库展示建议

置顶主维护仓库 `stein-wang0226.github.io`，description 建议：

> Research profile and study notes on Agentic RL, scientific task synthesis, GUI agents, diffusion language models, and AI4S.

优先置顶主站与两份已公开科研代码 `trainable-masked-diffusion`、`STM`；
`llm-study-notes`、`mllm-interview-notes` 有独立内容时作为后续入口。
Profile 仓库本身和 `algorithms` 练习仓库不占优先置顶位置。
普通 `terminal-bench-science` fork 不在 README 精选和置顶建议中展示。
只有存在可核对的原创补丁、上游贡献或独立实验时，才描述该具体贡献；
不能将 2,000+ 内部交付任务当作该 fork 的公开贡献。
Harbor、ProtAgent、Holon 目前仅有作者提供的项目描述；没有把内部项目写成可下载的公开代码仓库。
拿到已获准公开的项目链接后，再置顶相应仓库并添加项目页链接。

## 按顺序同步

1. 审阅并提交主站本次差异；推送 `main`，等待 Pages 部署成功。
2. 核对 `/about/`、`/cv/`、两种 PDF、`/publication/protagent/`、`/publication/cua-recovery/` 和线上 `build-info.json`。
3. 对 Profile 仓库先读取最新 README / 分支状态，再提交本稿；不覆盖期间新增的其他内容。
4. 按 `settings.json` 更新 GitHub Profile，实测个人主页及下载链接。
5. 旧仓库 `wyx0226.github.io` 的 Pages 仍占用 `/wyx0226.github.io/` 前缀。迁移跳转、停用旧 Pages 或归档旧仓库分别处理；本次本地更新不改变其线上状态。

用户随后明确要求同步推送，步骤 1–3 已执行：主站内容提交 `5801b4e` 已通过校验和 Pages
部署，线上 10 个页面 / PDF 文件与发布清单一致；Profile README 提交
`51246757924db14af2ea9d5b5d6c39c83767991b` 已推送并与本目录源文件逐字节核对。
步骤 4 的字段写入返回 HTTP 404，gh 明确提示需要 `user` scope；
当前 OAuth 只有 `gist`、`read:org`、`repo`。设备授权已发起，需要用户登录完成授权；
不得把 README 发布成功描述为 account 字段也已更新。
步骤 5 未执行：旧仓库仍未归档，旧 Pages 仍从 `master` 根目录提供旧地址。

普通主页维护的本地授权不自动涵盖停用旧站、归档或删除；
已明确授权的后续步骤直接执行，不重复请求。各阶段的实际证据见
[个人资料更新依据](../profile-update-20261114.md)。

## 后续维护入口

- 履历与项目：`content/pages/about.md`、`content/pages/cv.md`。
- 首页近期工作：由 `about.md` 的 `Selected Work` 自动生成，不维护第二份项目卡片数据。
- 论文：`content/publications/*.md`；首页精选仅登记 ID。
- English PDF：`assets/Curriculum_Vitae.pdf`；中文 PDF：`assets/Yuxiang-Wang-Resume-zh.pdf`。
- GitHub README：本目录 `README.md`。每次履历更新同步核对本稿和 Profile 仓库。
- 未知论文日期用 `date: null` 和明确的 `date_label`；不要以编辑日代替投稿 / 发表日。

## 管理与预览命令

```bash
python scripts/profile.py check
python scripts/profile.py status --gh /path/to/gh
"$HOME/.cache/stein-notes/venv/bin/python" scripts/profile.py preview \
  --gh /path/to/gh --output /tmp/github-profile-preview.html
```

检查和预览均不修改远端。`status` 输出远端 README 与本地的逐字节比较、
实际账号字段、目标字段和置顶项目；同步差异是状态，不作为读取失败。
`preview` 使用 GitHub Markdown API 的真实渲染，外加本地模拟 CSS；
它不代表已发布的网页，也不改变 GitHub 平台的字体或主题。

首版展示稿准备时的核对（2026-11-14，保留历史状态）：

- 线上 README 为 `51246757924db14af2ea9d5b5d6c39c83767991b` 的旧版，
  修改前与本地主稿一致；新版两列项目/论文状态表已在本地准备，尚未发布。
- 账号名称仍为 `stein-wang`，bio 仍为旧研究方向，website 仍指向旧项目站前缀。
  当前 `gh` scope 为 `gist/read:org/repo`，账号字段更新需 `user` 授权。
- 置顶仍是 `trainable-masked-diffusion`、`STM`、`llm-study-notes`、
  `mllm-interview-notes`、`algorithms`、`stein-wang0226`；主站未置顶。
- 本次移除无具体贡献描述的 fork 条目，未修改 fork 仓库和历史研究依据。

GitHub 原生 README 可通过仓库静态图片美化。图片版采用 ryme.md 的 MIT
横幅模板思路，并为四项研究工作增加主题配图；模板、许可、提示词与维护命令见
[图片与开源方案](VISUALS.md)。正文继续使用原生 HTML/Markdown 层级、表格和折叠详情。

## 图片版本发布（2026-11-14）

Profile 仓库提交 `514379c4a9d87e9e6c06b0cbf0030dee6643e288` 已推送至 `main`。
README 与展示图片一起发布；主稿仍在本目录集中维护。
本地候选通过 26 个链接 / 16 个主站入口和 5 张图片的校验；
390 / 650 / 1024px 亮色及 1024px 暗色预览无整体横向溢出，
图片加载、比例和折叠区的点击 / 键盘操作通过。
线上 README 逐字节一致，5 张展示图片的 Git blob 哈希与本地资源一致。
真实 GitHub Profile 在 390 / 1440px 下的图片加载、比例、图片链接、
四项研究标题、论文状态和折叠操作均通过，项目表格也无需横向滚动。

主站同时有其他章节的未完成编辑；本次链接核验以已发布的 `7158e73`
内容快照为基准。Profile 图片改动没有把这些章节算作本次验收内容。
账号字段与置顶顺序仍沿用上述实际状态。
