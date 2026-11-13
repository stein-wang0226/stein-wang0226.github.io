# GitHub Profile 实施稿

更新日期：2026-11-14。这里是可审阅的本地发布输入，尚未写入 GitHub。

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

优先置顶两份已公开科研代码 `trainable-masked-diffusion`、`STM`，再保留有独立内容的
`llm-study-notes`、`mllm-interview-notes`。
`terminal-bench-science` 是 `harbor-framework/terminal-bench-science` 的公开 fork，
可以作为相关 benchmark 入口展示，必须保留 fork 归属；不能据此宣称整个 benchmark 为本人创建，
也不能将 2,000+ 内部交付任务都视为该仓库公开任务。
Harbor、ProtAgent、Holon 目前仅有作者提供的项目描述；没有把内部项目写成可下载的公开代码仓库。
拿到已获准公开的项目链接后，再置顶相应仓库并添加项目页链接。

## 按顺序同步

1. 审阅并提交主站本次差异；推送 `main`，等待 Pages 部署成功。
2. 核对 `/about/`、`/cv/`、两种 PDF、`/publication/protagent/`、`/publication/cua-recovery/` 和线上 `build-info.json`。
3. 对 Profile 仓库先读取最新 README / 分支状态，再提交本稿；不覆盖期间新增的其他内容。
4. 按 `settings.json` 更新 GitHub Profile，实测个人主页及下载链接。
5. 旧仓库 `wyx0226.github.io` 的 Pages 仍占用 `/wyx0226.github.io/` 前缀。迁移跳转、停用旧 Pages 或归档旧仓库分别处理；本次本地更新不改变其线上状态。

这些步骤尚未执行。普通主页维护的本地授权不自动涵盖提交、推送、GitHub Profile 写入和停用旧站；
已明确授权的后续步骤直接执行，不重复请求。

## 后续维护入口

- 履历与项目：`content/pages/about.md`、`content/pages/cv.md`。
- 首页近期工作：由 `about.md` 的 `Selected Work` 自动生成，不维护第二份项目卡片数据。
- 论文：`content/publications/*.md`；首页精选仅登记 ID。
- English PDF：`assets/Curriculum_Vitae.pdf`；中文 PDF：`assets/Yuxiang-Wang-Resume-zh.pdf`。
- GitHub README：本目录 `README.md`。每次履历更新同步核对本稿和 Profile 仓库。
- 未知论文日期用 `date: null` 和明确的 `date_label`；不要以编辑日代替投稿 / 发表日。
