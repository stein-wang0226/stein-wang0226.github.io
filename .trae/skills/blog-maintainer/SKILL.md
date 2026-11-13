---
name: blog-maintainer
description: Maintain this repo's blog, homepage, CV, publications and shared components. Use for content, layout, navigation or release updates. Do not use for unrelated repos.
---

# 博客与主页维护

将用户要求落实到权威源文件，完成相应检查并交付可查看结果。使用现有 Python、Markdown、HTML 和 CSS 构建链；不要为普通维护引入新框架或第二套内容登记。

## 1. 定位仓库与任务

- 当前工作区根目录为 `/Users/bytedance/Desktop/my_blogs`，维护仓库位于其 `site/`，工作区根目录本身不是 Git 仓库。
- 在不同位置使用时，优先采用用户指定路径；否则检查当前工作区的 `site/` 或当前仓库根目录。以 `content/site.json`、`content/catalog.json`、`scripts/build.py`、`Makefile` 和实际 Git 根目录共同确认目标。不要依赖临时文件夹或历史预览存在。
- 在已确认的仓库根目录执行 Git 和维护命令，工具使用 `cwd`，不通过 `cd` 切换。不要写入旧学术 checkout 或独立子站。
- 读取当前 `README.md`、`docs/maintenance.md`，按任务读取必要源文件；结构、历史兼容或内容保留问题另读 `MIGRATION.md`、`docs/content-inventory.md`、`docs/content-audit.md`。
- 先查看工作区状态、暂存/未暂存改动摘要、分支和 remote。已有未提交修改不阻止普通本地维护；保留其内容，只处理本次范围。自动运行器的干净工作区要求单独适用。
- 将要求映射为正文、目录记录、个人资料、论文、展示组件、兼容地址或发布操作。已有上下文足以决定时直接实施；只有内容事实或目标确实无法确定时才询问，并继续可独立完成的工作。

## 2. 选择唯一编辑入口

| 要维护的内容 | 编辑位置 |
|---|---|
| 导航、主题、类型、站点身份、精选论文 ID | `content/site.json` |
| 文章标题、摘要、标签、分类、状态、推荐与关联关系 | `content/catalog.json` |
| 文章正文 | 登记记录中的 `source`，通常为 `content/posts/<id>/index.html` 或 `index.md` |
| 系列入口、章节正文、顺序 | `content/series/` 与对应 `kind/series/order` 登记 |
| 个人介绍、履历、在线 CV | `content/pages/about.md`、`content/pages/cv.md` |
| 论文事实与列表 | `content/publications/*.md` |
| CV PDF | `assets/Curriculum_Vitae.pdf` |
| 首页分区与数据展示 | `templates/home.html`、`scripts/views.py` |
| 博客卡片、目录与筛选交互 | `scripts/views.py`、`assets/site/catalog.js` |
| 全站导航、页脚、基础页面与 SEO | `scripts/render.py`、`assets/site/site.css` |
| 阅读导读、目录、系列导航和关联阅读 | `scripts/reading.py`、`assets/site/reading.css` |
| 个人页面、论文及资源的构建装配 | `scripts/pipeline.py` |
| 旧地址、查询兼容和 PDF 副本 | `content/redirects.json` |
| 前沿自动更新协议、运行器与检查 | `.automation/`；唯一自动正文为 `content/posts/llm-frontier-2026/index.html` |

不要编辑生成 HTML、`/tmp` 中的预览产物或旧根目录文章作为正式源。首页、个人介绍、CV 的论文列表和博客卡片必须继续引用上述记录，不能新增重复手写列表。更详细的任务流程见 [维护流程](references/workflows.md)。

## 3. 保留内容与兼容契约

- 保留原始公式、代码、科研图表、正文交互、有效 ID/锚点、引用、许可、PDF 与 `AUTO:INSERT:*` 标记。仅修改用户要求的内容，不因调整样式重写整篇科学 HTML。
- 正文变化时核对登记摘要和标签；分类、来源、内容形式、发布状态分别维护，日期只填写有依据的内容更新时间。未知日期保持 `null`。前沿日期来自正文 `last-updated`，不维护第二份日期。
- 默认保留 ID 与公开 URL。改名或改路径时保留有效兼容地址、查询及片段；旧分类映射不得覆盖有效新条件。删除公开内容前评估归档和旧链接，不将旧版或辅助材料自动当作冗余。
- 保持所有章节的父系列、正整数顺序和前后章一致，不凭文件名或目录扫描推断顺序。
- 科学结论、模型规格、论文归属、性能数字和个人履历须根据用户材料或可核实来源修改；缺出处或无法确认的项明确标注。不要把迁移、链接或渲染通过描述成事实全面正确。题库没有答案的部分不填充占位答案冒充完成。
- `docs/content-migration-manifest.json` 是不可重建的原始保留证据。对本次确实编辑、且受迁移清单覆盖的文件，先记录改前状态，再核对正文差异并更新对应 `docs/content-changes.json` 的精确 SHA 和具体理由；不要为消除报错批量刷新其他文件校验值。
- 保留检查若因用户明确要求的删除/锚点变更而不能继续适用，具体报告冲突及兼容处理，不能放宽检查后声称原检查通过。

## 4. 修改共享组件

- 区分组件数据与展示逻辑，优先修改最小负责文件。文章和科研图解样式限定在阅读层；不要用全局 `h1/table/svg/body` 规则污染原页面。
- 科研图表保持宽高比。KaTeX/MathJax 内部 SVG 是数学字形，排除在通用科研 SVG 缩放规则外；长公式、表格和代码在各自容器滚动。
- 手机目录按钮不能遮挡全站导航；保留展开/收起和键盘访问。跳转正文目标应可获取焦点，关联和章节链接要能返回博客/系列目录。
- 公式 CDN 或筛选脚本失败时保留可阅读的正文、静态文章与章节入口；加载提示不能覆盖整页，无 JavaScript 必须仍可浏览。
- 生成链接按公开 URL 计算，用现有 `ctx.rel` / `route_path` 等接口，不按 `content/` 源目录猜相对路径。新资源要登记或由现有复制规则纳入产物，并检查输出路径冲突。

## 5. 验证并交付

- 使用当前 `Makefile` 的 `VENV/OUTPUT/PORT` 参数；复用有效解释器，缺少固定依赖时才执行 `make setup`。不要依赖某次任务的 `/tmp` 虚拟环境。
- 普通更新完成后执行 `make check`。它构建并检查同一外部产物，不能使用修改前的预览或历史验收结果作证明。
- 受迁移基线覆盖的正文/资源变化，再执行 `python3 docs/verify-content-migration.py --require-clean` 并说明结果。它不是日常构建器，也不是修改证据的工具。
- 按影响范围验证界面。公共组件变化检查首页、博客、个人页和代表长文章的 390/768/1440px 视口；正文变化检查对应页及相关入口；构建、目录或自动化变化执行现有相应隔离测试。具体命令与验收范围见 [检查与发布](references/verification.md)。
- 需要浏览器验证时先加载可用的浏览器操作 skill，用实际点击、输入、键盘及页面证据确认效果。不要仅根据源码推断交互通过。
- 将当次改动、命令、结果和剩余限制写清。记录实际构建提交和 dirty 状态；如更新验收文档，应保留日期与范围，不把旧结果标成新结果。
- 最终给出改动对象、检查结论、实际预览/文件入口和同步状态。不要假称预览已启动、skill 已热加载或远端已发布。

## 6. 提交和发布

普通维护默认为本地修改。提交、推送、Pages 切换、停用旧站、归档和定时任务变更分别按当前或此前明确授权执行；已有授权不重复询问。用户只说“更新文章/主页/repo”时，不自动扩大为远端发布。

获准提交时只暂存本次相关文件，遵守仓库 Git 规则；不跳过 hooks，不改 Git 配置，不把其他未提交内容混入提交。获准发布时完成本地检查后再执行对应远端动作，并用 Actions、线上 `build-info.json` 和实际页面核对结果。主站的 `/wyx0226.github.io/` 兼容路由要考虑旧项目 Pages 对前缀的占用；本地跳转不能作为线上切换证据。

## 使用示例

- `用 blog-maintainer 新增一篇 KV Cache 笔记，先保存为草稿。`
- `用 blog-maintainer 更新主页推荐阅读，并把这篇文章归入训练与推理工程。`
- `用 blog-maintainer 调整公共导航和手机目录，保留公式与旧链接。`
- `用 blog-maintainer 更新论文与在线 CV，PDF 暂时保留原文件。`
- `用 blog-maintainer 修订这段 DPO 说明，引用我提供的原论文并做本地验证。`
