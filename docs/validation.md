# 本地整理验收记录

2026-11-14 首次本地验收完成。维护仓库为 `site/`，当时内容已具备本地发布准备条件；
首次验收时尚未提交、推送或远端部署。后续发布状态以 Actions 与线上 `build-info.json`
为准。本记录不将阅读和迁移检查等同于科研事实全面核验。

## 2026-11-14 发布前复核

本轮在完整训练系列正文与原始材料写入后重新检查，不沿用缺少章节时的构建结果。
以下检查全部通过：

```bash
make OUTPUT=/tmp/my-blogs-push-build check
python3 docs/verify-content-migration.py --require-clean
~/.cache/stein-notes/venv/bin/python scripts/test_pipeline.py
python3 .automation/test-frontier-update.py
FRONTIER_PYTHON=~/.cache/stein-notes/venv/bin/python \
  .automation/validate-frontier.sh "$PWD" content/posts/llm-frontier-2026/index.html
```

产物为 **57 个 HTML 页面、70 个公开文件**，当前包含 10 个本地集合、18 个章节和 4 篇论文。
原迁移基线仍保留 9 个集合、14 章：27 个 SHA 完全相同，14 项有意修改与精确记录一致，
299 个原锚点、59 个原标记通过。6 组隔离构建检查、18 组自动化检查及实际前沿校验接口通过。

迁移数量检查现按不可重建的基线来源核对，允许登记额外系列；
另核对删除原集合或原章节仍会失败。没有改写原始清单或批量刷新保留校验值。
维护 skill 已纳入 `.trae/skills/blog-maintainer/`，默认依赖环境已配置。
本节记录发布前的本地检查；部署结果与提交以 Actions、线上 `build-info.json` 为准。

## 内容保留与结构

覆盖 9 个活跃本地集合、14 个扩散章节、4 篇论文、历史 RL 页、个人介绍、在线 CV、
原 PDF、来源许可及 2 个独立子站链接。文章登记与正文分别维护于
`content/catalog.json` 和 `content/posts/` / `content/series/`；首页、博客和关联阅读引用同一登记。
论文列表引用 `content/publications/*.md`，个人资料引用 `content/pages/`。

```bash
python3 docs/verify-content-migration.py --require-clean
```

结果：27 个原 SHA-256 校验值相同，14 个有意差异与 `content-changes.json` 中固定的
校验值和原因一致；299 个原锚点、59 个原标记和 63 个登记路由通过。
迁移恢复时 31 个移动源文件逐字节一致；后续修订没有重新生成原始基线。
14 个章节、4 个论文记录、PDF、历史 RL 页、系列辅助文件与许可仍保持原字节。
原正文脚本、公式、代码和 SVG 的保留已在正文修订时核对；后续显示修复通过生成层完成。

具体修订及未核验项见 [内容检查](content-audit.md)。题库原有 470 道题、95 个内联答案，
375 道无内联答案的缺口仍明确保留；分布式性能表缺实验出处，已标为待核实。

## 构建、导出与隔离检查

验收环境：macOS arm64、Python 3.9.6，依赖版本由 `requirements.txt` 固定。

```bash
make VENV=/tmp/my-blogs-t2-venv check
/tmp/my-blogs-t2-venv/bin/python scripts/test_pipeline.py
```

生成并检查 **52 个 HTML 页面、64 个公开文件**。6 组隔离测试通过，覆盖：

- 重复 ID/URL、缺源文件、错误主题/类型、错误章节关系及无效日期等 8 种失败样本。
- 草稿创建、同名拒绝覆盖、空模板拒绝发布、草稿不出现在公开目录。
- 重复构建字节一致、正文和 Git 工作区状态不变、清单外遗留文件被发现并清理。
- 无效构建保留上一份成功产物；输出目录必须独立、不能覆盖无关目录。
- 删除已登记内容后旧输出不残留；源变化后的旧产物不能通过新校验。
- 前沿日期增量在正文与目录一致，源文件不被构建改写。

另在全新的临时目录复制当前源文件和 Git 元数据，以空产物目录运行实际命令行入口，
再重复构建和导出。64 个文件与现行预览逐字节一致，源文件校验值和
`git status --porcelain` 不变。Git 自身可能刷新 `.git/index`，该内部缓存不属于正文或产物检查范围。
这是**未提交内容的等效隔离快照检查**；尚无整理后的正式提交，因此不声称运行过该未来提交的干净
checkout 或 GitHub Actions。

最终发布产物：

| 项目 | 值 |
|---|---|
| 本地预览 | `http://127.0.0.1:8766/` |
| 公开文件目录 | `/tmp/my-blogs-site-build` |
| 构建基准提交 | `41ea2752875e27fa51bef619713649a4ddb98fd0` |
| 本地修改状态 | `dirty: true` |
| 构建输入摘要 | `70a789917b6172486b078c45b8df34cfad6c4ffd3bdde12770e8810226df5a1b` |
| 同内容独立导出 | `/private/var/folders/nz/vx8b3lvn5pd9pnj9kslp7j540000gn/T/blog-release-validation-9kq38wiy/export` |

输入摘要涵盖权威正文、资源、模板、构建脚本、依赖及前沿检查器；文档更新不改变该摘要。
产物不含正文源、Python、Markdown、模板、自动化状态、Git、虚拟环境或缓存。

## 浏览器验收

使用实际 Google Chrome，通过点击、输入、选择、Tab/Enter 和禁用 JavaScript 验证。
首页、博客、个人介绍、CV、论文列表、4 个论文详情、9 个活跃集合、14 章及历史 RL 页共
**33 个页面 × 390 / 768 / 1440px = 99 项布局检查，全部通过**。
整页没有横向溢出；宽表格、代码、长公式在各自区域滚动；科学图表保持比例。
数学排版内部的 SVG 字形不作为独立科研图表做宽高比判断。

**38 项交互检查通过**，包括：

- 首页 → 博客 → ELBO 命中章节 → 返回博客，主题/类型筛选、刷新恢复、无结果及清除条件。
- 键盘跳转正文、搜索、主题控件、目录展开和目录锚点；原题库答案展开/收起。
- 14 章的登记顺序和相邻导航；实测第 08 章位于 10/14，前后为 07/09。
- MathJax、KaTeX 正常生成公式，没有发现被测试页的公式错误节点；长行内公式补测
  `s00b_flow_sde.html` 共 268 个 MathJax 容器、0 错误，390px 下 41 个容器独立滚动。
- VLM 手机目录展开/收起，桌面目录位于共享导航下方；菜单不再遮住站点入口。
- `/notes/`、`/year-archive/`、旧论文和旧 RL 地址的跳转；旧分类映射、未知分类提示、
  新条件优先、附加查询参数与锚点保留。
- 无 JavaScript 的全部文章、系列目录、章节跳转、旧地址可见回退及 VLM 目录。
- 模拟公式 CDN 请求失败时正文仍可见，返回博客仍能操作。
- CV PDF 新旧地址均返回原字节，SHA-256 为
  `66b3c0d7c7cf44f23caf4cae80eaaac4e8948373fe39b682fc2111c2735ccde6`。

PDF 校验值来自实际下载与原文件比对；原文件保留也由迁移清单独立校验。
浏览器详细记录、验收脚本及截图保留于 `/tmp/my-blogs-browser-tests/`：
`layout-report.json`、`interaction-report.json`、`release-report.json`、
`check.js`、`release.py` 和手机截图。它们是本次临时验收证据，不是站点运行依赖。

## 自动维护与发布边界

前沿自动更新运行器的 18 个隔离样本通过，真实校验适配器与日期提取也通过。
测试覆盖干净工作区要求、其他未提交改动拦截、备份、标记、日期、失败状态及本地模式；
测试中的发布操作由替身命令接收，没有真实提交、push 或定时发布。可复跑：

```bash
python3 .automation/test-frontier-update.py
FRONTIER_PYTHON=/tmp/my-blogs-t2-venv/bin/python .automation/validate-frontier.sh
```

`.github/workflows/pages.yml` 的部署作业 `needs: build`；登记、构建、链接检查、
源文件未变检查和清单导出均为必须成功的步骤，未设置跳过错误或失败后部署。
这验证了本地逻辑与工作流依赖，没有虚报一次远端 CI 运行。

GitHub 个人主页为 `https://github.com/stein-wang0226`，维护仓库为
`https://github.com/stein-wang0226/stein-wang0226.github.io`，主站为
`https://stein-wang0226.github.io/`。本地的 `/blog/` 和旧路由不能据此称为线上已生效。
旧学术仓库、Pages 和独立子站保持原状态；切换步骤见 [迁移说明](../MIGRATION.md)。

外部网站的持续可达性、模型/论文归属、性能数字、个人履历真实性以及 GPU 配置复现不属于
已通过的站点验收。相关缺口保留在内容检查记录中；数学 CDN 是既有依赖，失败时可阅读原文，
精排公式仍需对应脚本成功加载。

## 2026-11-14 增量验收：LLM 训练全链路

新增系列入口和四章，公开入口 `/llm-training-lifecycle/`。
`make VENV=/tmp/my-blogs-t2-venv check` 通过：**57 个 HTML 页面、70 个公开文件**。
当前10个活跃本地集合、18个章节、4篇论文和2个独立子站链接。
原迁移验证再次通过：27个精确SHA、14项已有有意差异、299个原锚点、59个原标记；
当前68个登记公开路由，原9个集合、14章仍完整。

本次只验收新增系列及其发现入口，未重新运行原99项全站布局检查。
使用实际Google Chrome验证：

- **15项布局通过**：系列入口及4章 × 390 / 768 / 1440px，无整页横向溢出；
  流程图依次为单列、两列、四列，宽表格、代码与公式在各自区域滚动，单页只有一个H1。
- **42项交互通过**：首页推荐、系列目录、四章顺序及前后跳转、原文六个锚点、
  Harbor扩展链接、关键词 / 中文标题 / 算法搜索、主题筛选与刷新恢复、键盘跳正文、
  来源链接及原件隔离。该数量含原件和来源的检查，不等同于42次点击。
- **5页无JavaScript阅读通过**；额外实测无脚本博客目录、原锚点和相邻章节可操作。
- 实际截图检查桌面系列总览与手机Midtraining流程，版式正常；新系列不依赖公式CDN或外部图片。

原上传材料19,556字节，SHA-256
`9be90744e1db851023a2a2e26d02d53df2d43ec20eb814314bcdca0df92a5061`，
与存档逐字节相同，原件没有进入发布产物。来源共27项，版本、表格位置、数字口径与
原文修订见 [训练全链路来源复核](llm-training-research-20261114.md)。
公开论文数字是作者报告；CSV示例与Harbor A–E方案未执行训练，不提供虚构收益。

临时浏览器证据保存在 `/tmp/my-blogs-browser-tests/`：
`training-series-check.js`、`training-series-report.json`、
`training-series-1440.png`、`training-mid-390.png`。
首次发现原文锚点与自动目录新编号分离，已将六个ID移至对应标题并复验。
另一处等待导航完成的验收脚本问题已修正，最终没有浏览器错误。

本次浏览器快照的输入摘要为
`42cfb141b2954cc80b4f1e9e69ef3f7dc0c5c668375eb3419820b41419faf5dd`，
当时构建记录提交 `c2c713a19d43d10905e664739fe5f6ff82c777bd`、`dirty: true`。
工作区在验收期间另有提交与同步活动，以上仅标识所测本地内容；
上述本地浏览器验收本身未执行发布；另一次线上发布核对记录如下。

## 2026-11-14 线上发布核对

主站 Pages 已从根目录直接发布切换为 GitHub Actions。仓库整合提交 `c2c713a`、
训练章节锚点修正提交 `8b31420` 均已推送至 `origin/main`，两次校验与发布工作流均成功。
最终章节修正对应的发布记录：
https://github.com/stein-wang0226/stein-wang0226.github.io/actions/runs/43489133694 。

核对时线上 `build-info.json` 的提交为
`8b31420136a820e730440450e2875c45b8b0ea2c`，`dirty: false`，清单共70个公开文件。
实际下载首页、博客、About、CV、论文列表、新系列入口与Midtraining章、
ELBO章、历史RL页和CV PDF，共10个文件，SHA均与线上发布清单一致。
实际浏览器操作验证首页进入博客、ELBO搜索5项匹配、进入第08章后位置10/14与前后章正确，
论文列表显示4条记录。此后纯文档提交的发布版本仍以线上清单为准。

旧学术仓库与旧Pages仍保留，`/wyx0226.github.io/` 实测仍由旧学术站提供。
有效个人内容已迁入主站，原提交历史及旧主题保留在旧仓库；没有删除、归档或停用旧Pages。
