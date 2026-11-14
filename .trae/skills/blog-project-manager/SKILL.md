---
name: blog-project-manager
description: Manage this blog's content structure, design rules, HTML assets and GitHub profile consistency. Use for project governance, bulk organization or maintenance protocols. Not for unrelated repos.
---

# 博客项目管理

把项目管理要求落实为可执行协议、唯一源入口和可验证结果。
具体文章、CV 或组件编辑复用同仓库的 `blog-maintainer`，不创建第二套内容登记。

## 确认范围

1. 通过 `git rev-parse --show-toplevel`、`content/site.json`、
   `content/catalog.json`、`scripts/build.py` 和 `Makefile` 定位维护仓库。
   当前工作区是 `my_blogs`，实际仓库在 `site/`；不要写入旧 checkout。
2. 读取仓库 `AGENTS.md`、`README.md` 和
   [项目管理协议](../../../docs/project-management.md)。
   查看 Git 状态、当前分支、remote 和既有改动，保留其他任务文件。
3. 按任务读取
   [内容协议](../../../docs/content-contract.md)、
   [设计协议](../../../docs/design-system.md) 或
   [Profile 发布协议](../../../docs/github-profile/DEPLOYMENT.md)。
   正文/页面修改另读 `../blog-maintainer/SKILL.md`。
4. 明确交付属于正文、分类、结构、视觉、个人资料、规则或远端同步。
   有足够上下文就直接实施，不把日常可逆编辑变成审批流程。

## 结构和规模化

- 运行 `make governance` 和 `make inventory`，用真实登记统计规模。
  结合读者路径定位重复、空白、主题错置、系列关系和失效入口。
- 分类复用 `site.json`；文章/章节只有 `catalog.json` 一份登记。
  新主题需要明确覆盖，不按文章标题制造同义分类。
- 将阶段定义留在训练系列，最新机制和证据留在研究地图，
  细节专题用 `related`/锚点连接，题库用于检查理解。
- 移动、拆分和归档先核对公开 URL、锚点、资源、上游引用和迁移基线。
  有效内容不因结构整理丢失，不以重建基线掩盖差异。
- 大资源报告公开必要性、许可和体积；原件字节保留。
  checkout、脚本试验、日志、缓存、截图和产物放仓库外。

## 修改规则和组件

- 把稳定协议更新在 `docs/`，把跨任务入口更新在 `AGENTS.md`。
  本 skill 指向协议，不复制长篇规则、清单或实时状态。
- 视觉沿用 Stein’s Notes；设计改动用 `frontend-design`，
  先确定真实内容、token、排版和组件范围，再检查实现截图。
- 全站样式、个人页、阅读装配和专题样式分别维护，避免宽选择器互相覆盖。
  保留手机阅读、可见焦点、无脚本入口、公式和图表原比例。
- 不用普通 fork、空壳或练习仓库充当成果。写出原创贡献、
  方法和有依据的结果；不知道的公开链接和事实不补造。

## 管理 Profile 同步

1. 先跑 `make profile-check`，再用 `make profile-status GH=/path/to/gh`
   读取远端 README、账号字段和置顶仓库。
2. 在 `docs/github-profile/README.md` 维护展示稿，
   `settings.json` 维护账号字段目标。
   事实回核 `about.md`、`cv.md` 和论文记录。
3. 用 GitHub Markdown 渲染和实际浏览器检查 README。
   GitHub 由平台控制字体、颜色和外壳，不将浏览器主题插件当作公开主页改版。
4. 分别报告主站、README、账号字段和置顶状态。
   缺 `user` scope 只影响账号字段，不据此停止其他已授权工作。
5. 远端写入按照当前或此前明确授权执行；没有授权时完成源稿和预览，
   明确尚未发布。不得用历史“已发布”文字代替当前读取。

## 验证与交付

- 本地协议/登记/Profile 修改跑 `make governance`；站点更新跑 `make check`。
- 构建或契约变化使用已有 `scripts/test_pipeline.py`；
  基线覆盖正文变化使用迁移保留检查；界面变化做影响范围内真实交互验证。
- 每个新增或修改脚本实际执行一次，失败就修复。检查只读取，
  不自动整理 JSON、不改校验值、不提交、不推送。
- 对本次记录源路径、变化理由、实际命令和结果、预览入口及同步对象。
  只将规则变化和必要证据写入长期文档，不堆积每次任务的临时日志。
- 获准提交时检查所有暂存项并只加入本次文件；不跳过 hooks，
  不改 Git 配置，不强制推送，不把并行任务混入发布。

示例：`用 blog-project-manager 审计分类与系列结构，补齐维护协议并检查 Profile 一致性。`
