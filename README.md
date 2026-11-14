# Yuxiang Wang · Research & Stein’s Notes

唯一维护仓库：[stein-wang0226.github.io](https://github.com/stein-wang0226/stein-wang0226.github.io)，分支 `main`。
个人 GitHub 主页：https://github.com/stein-wang0226。
公开主站：https://stein-wang0226.github.io/；统一博客入口为 `/blog/`。

本地整合与验收已完成，发布状态以 Actions 和线上 `build-info.json` 为准。
旧学术仓库仍保留，旧 Pages 未停用；旧项目网址的切换需要单独核对。

## 快速维护

需要 Python 3.9+，依赖版本锁定在 `requirements.txt`；无 Ruby、npm 或数据库。

```bash
make setup
make check
make preview
# http://127.0.0.1:8000
make new ID=my-topic TITLE="文章标题" TOPIC=llm-foundations
```

虚拟环境默认 `~/.cache/stein-notes/venv`；产物默认 `/tmp/my-blogs-site-build`，均在仓库外。
可用 `make VENV=/path/to/venv OUTPUT=/tmp/another-build PORT=8766 preview` 覆盖。
预览、校验和 Pages 使用同一份构建产物，构建不回写正文。

## 编辑位置

| 内容 | 唯一维护来源 |
|---|---|
| 站点导航、主题及类型 | `content/site.json` |
| 文章、系列章节、独立子站及关联关系 | `content/catalog.json` |
| 正文 | `content/posts/<id>/index.html` 或 `index.md` |
| 扩散系列 14 章 | `content/series/dlm-survey/*.html` |
| LLM 训练全链路 5 章 | `content/series/llm-training-lifecycle/*.html`；四阶段加训练方法与集群设计，专用样式 `assets/site/training-lifecycle.css` |
| LLM 架构基础 6 章 | `content/series/llm-architecture/*.html`；张量、Attention、MoE、残差、状态与模型比较 |
| Agent 系统 3 章 | `content/series/agent-systems/*.html`；检索证据、规划预算与信任边界 |
| LLM 推理部署 3 章 | `content/series/llm-serving/*.html`；调度、并行量化、容量与成功成本 |
| LLM 研究地图 7 章 | `content/series/llm-research-map-2026/*.html`；数据 / RL / DeepSeek / 推理 / 场景 / 多家族架构 / 训练机制 |
| Agent 任务合成与 Benchmark 4 章 | `content/series/agent-data-benchmarks/*.html`；生产与评测、科学任务合同及工业训练对照；原52项来源保留 |
| 研究报告原件与引用 | `assets/research/2026-11-14/`；`sources.json` 登记固定版本、来源、许可与 SHA，公开资源登记在 `site.json` |
| 个人介绍及在线 CV | `content/pages/about.md`、`cv.md` |
| 论文与精选记录 | `content/publications/*.md`，精选 ID 在 `site.json` |
| 历史 RL 手册 | `content/archive/rl-interview-guide/index.html` |
| 旧地址映射 | `content/redirects.json` |
| 首页布局、共享展示 | `templates/`、`assets/site/`、`scripts/` |
| 研究简历 PDF | 英文 `assets/Curriculum_Vitae.pdf`，中文 `assets/Yuxiang-Wang-Resume-zh.pdf`；原 CV 保留在 `assets/archive/` |
| GitHub Profile 介绍稿 | `docs/github-profile/README.md`、`settings.json`；发布顺序见 `DEPLOYMENT.md` |

不要手改或提交生成 HTML。首页、个人介绍、CV 的论文列表，以及博客搜索和相关文章都从上述记录生成。
新增命令创建草稿，完成内容并移除空模板标记后，将 `status` 改为 `published`；草稿不进入公开产物。
日期仅填写有依据的内容更新时间；前沿追踪直接提取正文 `last-updated`。

研究原件保留下载字节，不做文本归一化；`.gitattributes` 将归档PDF标记为二进制，
并保留官方许可原有换行。添加报告后同步登记来源、署名、许可、长度和SHA，
以及 `site.json` 的公开资源；不要用下载时间代替论文版本。

架构与任务合成SVG由 `python3 scripts/research_figures.py` 生成（调用解释器需有matplotlib，
不属于站点构建依赖）。脚本从专题入口生成来源JSON；数值图为规格推导，CSV与JSON保留分项。
新增架构机制图由 `python3 scripts/architecture_figures.py` 生成，保存于
`assets/research/architecture-20261114/`；4张SVG、2份CSV和JSON只含引用规格与明确推导，
不生成模型性能模拟值。更新规格时同步维护来源清单与正文，并显式登记公开资源。

## 检查和发布

```bash
make check
make export DEST=/tmp/site-export-new
# 导出目录须为空；内容与预览产物一致
```

构建检查登记、重复 ID/URL、源文件、分类、章节关系、链接、锚点、导航、草稿、前沿标记及公开文件清单。
失败时保留上一份成功产物；输出不含正文源、工具、自动化状态或缓存。
外部网站可达性、科研断言和个人履历真实性不由链接检查证明。

获准提交并推送后，Actions 才会构建、检查和发布：
[Actions](https://github.com/stein-wang0226/stein-wang0226.github.io/actions) ·
[Pages 设置](https://github.com/stein-wang0226/stein-wang0226.github.io/settings/pages) ·
[线上版本](https://stein-wang0226.github.io/build-info.json)。
Pages Source 应设置为 GitHub Actions；部署作业依赖构建与校验成功。
`build-info.json` 记录实际提交、是否含本地修改和产物校验值，不使用运行时间冒充内容日期。

## 说明与来源

- [日常维护](docs/maintenance.md)：新增、更新、预览、前沿自动化及线上核对。
- [内容检查](docs/content-audit.md)：覆盖范围、修订与未完成的事实复核。
- [知识体系扩展依据](docs/knowledge-expansion-research-20261114.md)：架构、训练、Agent、部署、科学方案与60道新增题解；贯通路线在 `/llm-research-map-2026/#learning-paths`。
- [训练全链路来源复核](docs/llm-training-research-20261114.md)：27 项原始来源、原 Midtraining 调研修订与实验边界；本地入口 `/llm-training-lifecycle/`。
- [研究地图与覆盖审计](docs/blog-research-review-20261114.md)：初版五章及后续七章扩展说明；公开入口 `/llm-research-map-2026/`。
- [多家族架构调研](docs/architecture-research-20261114.md)：第06–07章版本、机制与证据边界；当前研究地图71项来源、15份原件。
- [验收记录](docs/validation.md)：内容保留、浏览器、隔离构建与真实发布状态。
- [个人资料更新依据](docs/profile-update-20261114.md)：最新简历、项目口径、论文状态、中英文附件与 GitHub Profile 稿。
- [迁移与地址清单](docs/content-inventory.md)：原始 9 个集合、14 章、4 篇论文的保留基线；当前内容以登记与本次验收为准。
- [迁移与远端切换](MIGRATION.md)：保留旧地址、原仓库与许可。

`mllm-interview-notes`、`llm-study-notes` 仍是独立子站。
旧学术主题及示例留在原仓库，MIT 许可保留于 `licenses/academic-pages-MIT.txt`。

## 后训练专题

`content/series/llm-posttraining/` 维护六章 SFT / RL / OPD、环境信用、
异步框架与任务案例；公开入口 `/llm-posttraining/`。来源与数学核对见
`docs/posttraining-research-20261114.md`，图数据和教学契约在
`assets/research/posttraining-20261114/`。实验矩阵标为待执行，不表示模型训练已复现。
