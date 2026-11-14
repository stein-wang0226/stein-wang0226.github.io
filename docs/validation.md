# 本地整理验收记录

## 2026-11-14 · 后训练六章专题

入口 `/llm-posttraining/`。66项原始来源、六章正文、两张解析/报告图与可下载数据，
三类教学任务、轨迹契约与E0–E6待执行矩阵；旧训练系列与研究地图增加深入链接。
来源位置和边界见 `docs/posttraining-research-20261114.md`。

独立发布快照基于已提交主站组装，不包含同目录并行开发文件。实际通过：

- `make OUTPUT=/tmp/my-blogs-posttraining-build check`：77页、138项公开文件。
- 迁移保留：23项原始SHA一致、18项既有有意变化；299个原锚点、59个原标记保留。
- 19项数学/数据核验：reverse-KL有限差分、Soft SAPO、GRPO解析概率、GAR、比例求和。
- 390/768/1440宽度27项布局、34项实际交互、7页无JS阅读；无pageerror。
- 两张图的手机放大入口实际打开SVG；五种下载逐字节哈希一致。

已查看桌面OPD及手机算力图截图；保持Stein’s Notes配色，图表比例不变。
临时浏览器证据 `/tmp/my-blogs-browser-tests/posttraining-report.json`。
这些验收不包含GPU训练、科学实验或论文性能复现；案例均为design_only。
发布完成状态由Actions与线上build-info记录另行核对。

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

## 2026-11-14 最新简历与个人资料本地更新

更新首页、About、在线 CV、三条既有论文记录，加入 ProtAgent / CUA-Recovery，
接入作者原始中英文研究简历，旧 CV / 正文归档保留；GitHub Profile README 和字段稿
见 `docs/github-profile/`。来源、论文作者差异、实验口径与附件 SHA
见 [个人资料更新依据](profile-update-20261114.md)。

本轮使用 `/tmp/my-blogs-profile-build` 与实际运行的 `http://127.0.0.1:8768/`：

- 构建 / 检查59 HTML页、79公开文件通过。
- 7项隔离构建检查均有通过结果；新增未知日期用例修正后单独复验通过。
- 原始迁移保留检查通过：23项原 SHA 相同、18项后续变化有精确记录，
  299个原始锚点、59个标记保留，原9集合 / 14章保留。
- Google Chrome 56项检查通过：33项布局（11条路径 × 390 / 768 / 1440px）、
  项目 / 稿件 / CV / 键盘 / 搜索导航、真实中英文下载及新旧路径字节、
  5页无JavaScript阅读与项目跳转；无脚本错误。实际截图已查看。

浏览器快照input digest为 `e09f9b60f0f89ea820d47e39992fdc4d0d5091641514b8433518ce731bda05a8`，
构建commit为 `2e6bfce94c4825b955d09e680a3722aa9973d71c`，`dirty: true`。
本次仅完成本地更新；结束时主站remote仍为`2e6bfce`、Profile仍使用旧介绍与旧website。
没有提交 / 推送 / Profile写入 / 旧Pages切换；以上结果不能描述为已上线。

同轮用户随后提供ProtAgent arXiv链接并确认SemDLM+已被NeurIPS主会接收：
ProtAgent采用公开正式标题、2026-10-24首发日期与作者顺序；
SemDLM+明确展示“NeurIPS 2026 Main Conference — Accepted”，并排在首页精选论文首位。
三个arXiv链接重新核对，ProtAgent公开的三随机种子对照与指标范围补入研究记录。

修订后完整7项隔离构建测试在同一次运行全部通过，
59 HTML页 / 79公开文件检查通过，浏览器扩展为**61项通过**，保留检查及`git diff --check`通过。
最终input digest为 `1980c6a2c5a71f5fbd978011b987d26a8f2312def0bf59d8519386ba9c461a20`，
commit仍为`2e6bfce94c4825b955d09e680a3722aa9973d71c`、`dirty: true`。
较早的56项和旧digest保留为初轮记录；最终以本段和`profile-report.json`为准，仍未执行远端写入。

## 2026-11-14 用户授权后的个人资料线上同步

用户随后明确要求同步推送，个人资料提交
`5801b4ea856c09077639230cffb37554c535a87d` 已推送至主站 `origin/main`。
Validate site工作流 `43493652355`、Publish static site工作流 `43493652124` 均成功，
线上 `build-info.json` 提交一致、`dirty: false`。

实际下载首页、About、CV、论文列表、ProtAgent、CUA-Recovery、SemDLM+及
英文PDF、中文PDF、英文别名，共10个文件，SHA全部与线上发布清单一致；
三个PDF同时与本地原附件一致。实际浏览器核对首页论文接收状态、
首页→About→CV导航、当前实习、四项工作与CV项目锚点。
这是发布后的抽查，未重复计入之前61项本地浏览器验收。

GitHub Profile README 已发布至 `stein-wang0226/stein-wang0226`，提交
`51246757924db14af2ea9d5b5d6c39c83767991b`；
通过gh读取远端README，与主站 `docs/github-profile/README.md` 逐字节一致。
账号姓名、bio、website字段更新仍受当前OAuth缺少 `user` scope阻止，
没有虚报字段更新；已发起设备授权，等待用户登录完成。
旧学术仓库仍未归档，旧Pages仍在线；没有删除、归档或停用。
详细来源、附件SHA及权限返回见 [个人资料更新依据](profile-update-20261114.md)。

同时间其他维护线程已提交 `2ad31ae`、`618f66b` 的样式 / 缓存修正；
上述10文件线上抽查对应 `5801b4e`。后续最终发布提交应以最新Actions与
线上 `build-info.json` 核对，不将早先快照标成最新版本。

## 2026-11-14 LLM研究地图、原报告与覆盖审计

完成系列 `/llm-research-map-2026/` 的入口与五章正文：Agent数据 / benchmark、
Agentic RL、DeepSeek V4.1架构、扩散投机推理、GUI / 科学Agent / 持续学习。
编辑判断、来源与修订边界见 [研究复核](blog-research-review-20261114.md)。
旧文通过catalog的related接入专题，原科学正文、URL和AUTO标记未修改。

使用 `make check OUTPUT=/tmp/my-blogs-research-build`：

- 65 HTML页 / 98公开文件构建及检查通过；当前11个本地集合、23章、6篇论文、
  2个独立子站。原件署名说明采用TXT，与PDF和来源JSON一起显式登记。
- 来源清单43项，编号1–43连续；10份PDF共36,619,952字节，PDF签名、长度与SHA-256
  全部匹配。DeepSeek为固定官方HF revision；其他原件CC BY 4.0，完整作者校正，
  完整MIT notice保留。未重写原PDF字节。
- 归档PDF显式按二进制维护，官方MIT notice保留原CRLF换行；
  `.gitattributes`记录对应规则，避免Git将PDF流当作源码或改写许可换行。
- 原始迁移保留检查通过：23项原SHA相同、18项此前变化仍与准确记录一致；
  299个原始锚点、59个标记保留。原始9集合 / 14章保留，迁移基线未重建。
- Google Chrome headless实际操作通过81项：24项布局（首页、博客及6个新页面
  ×390 / 768 / 1440px）、51项导航 / 搜索 / 键盘 / 资源检查、6页无JavaScript阅读。
  检查五章顺序及前后章、来源锚点、作者项目锚点、关键词与主题重载、
  旧Harness / DLM关联入口、10份发布PDF字节及许可下载。无页面脚本错误。
- 已查看桌面入口、手机CED图解、手机信用分配截图；图解保持阅读顺序，
  长表格和公式在各自容器滚动，无页面横向溢出。

验收使用实际运行的 `http://127.0.0.1:8769/`。证据保存在
`/tmp/my-blogs-browser-tests/research-series-check.js`、
`research-series-report.json`、`research-index-1440.png`、
`research-architecture-390.png`、`research-rl-390.png`。
全部检查针对同一构建快照；修正验收脚本对CV路由、原生章节列表和生成目录锚点的
错误假设后，从通过项继续完成剩余检查，不累计重复次数。

该本地快照commit为 `0d04ebfcc0ea81bbb28d5cda6827d2d43f3b8820`、`dirty: true`，
input digest为 `22187b4b840da1426e715d1bf461e3b88a3e607dec70ec07080c1f0e55aa1ea6`。
本地检查不能代替线上发布证据，线上核对另列。

论文 / 团队数字未本地复现，建议训练、任务合成和解码实验均未执行。
TB4官方19项与合作方20项修复的计数分歧、SkillsBench初版 / 1.1口径、
SAPO同名、V4.1 v1 / 1017区别在正文保留。Muon / loop / kernel为后续独立选题，
本轮未完成独立公式和复现实验长文。

先前GitHub账号字段设备授权已返回 `expired_token`；
姓名 / bio / website仍未写入。该授权与主站repo推送是不同权限。

### 研究地图线上核对

内容提交 `50f9ea62675ae64fd1567db4330b58779b733502` 已推送至 `origin/main`。
[Validate site](https://github.com/stein-wang0226/stein-wang0226.github.io/actions/runs/43508203740)
与 [Publish static site](https://github.com/stein-wang0226/stein-wang0226.github.io/actions/runs/43508203729)
均成功，线上 `build-info.json` 的commit一致、`dirty: false`、
input digest与上述本地浏览器快照相同，共98个公开文件。

实际下载核对22个线上文件：首页、博客、catalog、系列入口与五章、10份PDF、
来源JSON、署名TXT及MIT notice；SHA全部与发布清单一致，13项归档资源
也与仓库原件逐字节相同。catalog推荐为新研究地图，章节order 1–5正确。
另核对提交中的10份PDF blob均匹配原SHA，官方license原CRLF字节保留。
证据为 `/tmp/my-blogs-browser-tests/research-release-check.py`、
`research-release-report.json`。本段记录内容发布快照；后续纯验收文档提交
不改变该input digest，最终部署commit继续以线上 `build-info.json` 为准。

## 2026-11-14 任务合成、经典与前沿Benchmark及架构增补

新增 `/agent-data-benchmarks/` 两章：可执行任务合成、Benchmark地图。
正文深入十二条数据路线和TB / Science / Challenges / HarborIndex /
DeepSWE / SWE-bench / AA；附经典代码、通用Agent、Web / GUI、
科学与基础保留性评测的对象、评分、用途和边界。
新系列52项来源（35篇论文、17项项目文档），独立于原43项索引。
原DeepSeek第03章增加CED张量路径、CSA2层计划与hierarchical indexer、
FP4格式和890 B/token推导、两种replay及MoE / mHC / Engram细节。
五张SVG、CSV和JSON均可下载，数值明示为规格推导。

本地命令与结果：

- `make check OUTPUT=/tmp/my-blogs-bench-build`：68 HTML页 / 109公开文件，
  登记、链接、锚点、章节、来源及资源清单通过。
- `python3 docs/verify-content-migration.py --require-clean`：23项原SHA相同、
  18项有准确理由的历史 / 本次变化；299个原始锚点、59个标记保留；
  当前12个本地集合、25章、6篇论文、2个独立子站。
- `~/.cache/stein-notes/venv/bin/python scripts/test_pipeline.py`：8项隔离测试通过。
  增加注册CSV的输出检查及missing object-data图表目标会阻塞构建的检查；
  站点CSV只按显式资源登记发布，不扫描研究目录。
- `python3 scripts/research_figures.py`：5 SVG + CSV + 规格JSON + 来源JSON；
  连续两次生成的8文件逐字节一致，未引入站点运行依赖。
- Chrome实际交互：27项布局（9页 × 390 / 768 / 1440px）、
  39项导航 / 搜索 / 键盘 / 资源检查、6页无JavaScript阅读，共72项通过，
  无页面脚本错误。图表加载、宽高比、放大查看、CSV下载、
  两章前后导航、原来源锚点、CV往返及经典关键词搜索均检查。

验收预览为 `http://127.0.0.1:8771/`。脚本与证据：
`/tmp/my-blogs-browser-tests/bench-series-check.js`、`bench-series-report.json`、
`bench-index-1440.png`、`bench-kv-1440.png`、`bench-classics-390.png`。
已查看系列入口、890B分项图与手机经典表格，保持Stein’s Notes风格，
表格在容器内横向滚动，图表原始比例保留。
验收脚本修正了SVG根节点、生成目录anchor与CV链接形式的错误假设；
最终次数不重复累计已通过项。

浏览器验收输入快照为commit `784f449a51e1158377e3ccb9b282fbbfa5b3614b`、
`dirty: true`，input digest
`7804284bed574464cf573ad3a6119c8e53c5be35e6605db3188a8f954bf9073c`。
之后仅将SWE-bench Pro引用从重定向且返回403的旧榜单入口
改为实际可访问的官方overview，并重新生成来源JSON、构建和检查。
最终发布版本另以Actions / 线上manifest核对，不将旧本地commit当发布证据。

论文及团队报告没有在本站训练 / benchmark复现；作者履历数字单列，
TB Sci仍仅为一轮review通过；0.2 roadmap、TB 4.1与AA TB 4.0、
HarborIndex 82→80及DeepSWE同名区别在正文明确。

### 最终发布范围复核

最后构建时，另一维护线程正在修改
`content/posts/agent-harness-guide/index.html`，共享工作树出现独立的
title检查失败。本次未改写或提交该线程的正文。为避免其影响发布，
在 `/tmp/my-blogs-bench-validation` 从原HEAD建立detached worktree，
只复制本次25个文件，重新构建 / 校验同一预览产物，68页 / 109文件通过。
该隔离快照的input digest为
`ca29de2c7fd853d3adb881e66189b8307af8503311e688cbf8bb8edf18e5c550`。
提交前规范化matplotlib SVG行尾空白与CSV的LF换行，不改变图形或数值，
重新构建与资源验收通过。

最后引用修订通过10项补充浏览器检查：官方Pro来源链接、
手机无脚本系列入口及8项发布资源SHA，结果保存在
`/tmp/my-blogs-browser-tests/bench-final-report.json`；
此前72项交互验收仍对应其明示快照。发布只包含本次文件，
原共享目录中的其他未提交内容保留，不能把共享工作树称为干净。
隔离快照同时排除另一线程的Harness目录摘要与保留记录更新，
仅提交本专题关联链接；最终隔离迁移检查再次通过。

## 2026-11-14 · 多家族架构与训练机制扩展

范围：研究地图由五章扩为七章，追加第06章多家族模型架构与第07章训练机制；
原五章顺序、URL及引用1–43保留。第03章增加新章节入口和跨路线比较。
Qwen、Kimi、Nemotron、GLM、MiniMax、MiMo、Step、Gemma分别分析，
并记录GPT-6.1、Opus 5.5、Gemini 4的披露边界。
目录、搜索、首页摘要与维护说明同步；当前71项来源（47篇论文 + 24项官方文档 / 配置）、
15份原件。新增4张SVG、2份CSV和来源JSON，全部显式注册为公开资源。

- `make OUTPUT=/tmp/my-blogs-architecture-build check`：70 HTML页 / 123公开文件，
  链接、锚点、章节、目录、资源及前沿标记通过。
- `python3 docs/verify-content-migration.py --require-clean`：23项原SHA相同、
  18项已登记历史变化，299原始锚点、59标记保留；当前12本地集合、27章、6篇论文。
  本次只新增和修订非原始基线的研究系列，未刷新旧文SHA。
- `python3 scripts/architecture_figures.py`：4 SVG + 2 CSV + JSON；
  连续生成7文件逐字节一致。15份原PDF长度与SHA均匹配，共51,576,539 bytes。
- Chrome实际交互：18项布局（首页 / 博客 / 研究地图 / 03 / 06 / 07 ×
  390 / 768 / 1440px）、44项入口 / 章节 / 搜索 / 键盘 / 图表 / 下载 / 资源检查、
  5页无JavaScript阅读，共67项通过，无页面脚本错误。
  12个新增家族 / 机制关键词可搜索，七章前后导航与固定引用可跳转；
  图表加载、原始宽高比、放大页面、两份CSV下载及12个新增公开资源SHA均检查。

实际预览 `http://127.0.0.1:8774/`；脚本及证据：
`/tmp/my-blogs-browser-tests/architecture-check.js`、`architecture-report.json`、
`architecture-index-1440.png`、`architecture-layers-1440.png`、
`architecture-latent-1440.png`、`architecture-landscape-390.png`。
已查看四张截图：现有Stein’s Notes纸色、字体和青绿风格保留，
长表在容器内滚动，科研图不拉伸。

测试脚本曾误用首页featured卡片选择器，实际入口位于普通研究地图卡片；
无脚本测试亦曾只读取导读容器，现改为实际正文容器。
两次都是验收假设修正，产品源码无需调整；通过项按名称去重，失败尝试不累计。
迁移检查第一次与图表生成并行，因尚未生成资源而报missing source；
生成完成后串行重跑通过，最终以完整产物验收。

浏览器输入快照：commit `8fbf29df7cdb5878b854d62a305727bef6149287`，
`dirty: true`，input digest
`27859a146c91ac073b5058f6ca354ac48bbe1fc620b9f276c91b490700f44db6`。
随后仅追加维护和验收记录；最终发布版本另由Actions与线上manifest确认。
本章数字为来源规格、来源团队实验或明示推导；本站没有执行训练 / benchmark复现，
不把kernel加速、latent维度比或层数量当作跨模型Agent性能排名。

### 本次提交的隔离核对

提交前发现共享工作区另一任务新增项目管理 / Profile材料和独立架构草稿，
并与本次共用README和maintenance。独立工作树
`/tmp/my-blogs-architecture-release-validation` 从 `8fbf29d` 建立，
只装配本次架构文章、来源、资源与维护说明；共享文档仅保留本次明确的hunk。
其他任务文件及其未提交文档变化保留在原工作区，不随本次发布。
最终提交范围通过暂存差异核对，部署仍以Actions与线上版本为准。

独立快照再次构建70页 / 123文件并通过迁移核对，input digest仍为
`27859a146c91ac073b5058f6ca354ac48bbe1fc620b9f276c91b490700f44db6`。
对122项manifest文件比较，仅HTML资源查询参数及博客data-catalog-version不同；
归一化这些缓存版本后全部一致，正文、导航、数据和资源字节没有其他变化。

## 项目管理协议与 Profile 展示稿（2026-11-14）

范围：新增 `AGENTS.md`、`blog-project-manager`、管理/内容/设计三份协议，
只读规模与 Profile 检查脚本；管理检查接入 `make check` 和 Pages 工作流。
Profile 改为研究项目两列、精选论文状态表和笔记入口，移除普通 Science fork 展示项。
未改动该 fork、履历事实或旧研究依据。

- `make governance`：11 份文档/skill 引用检查通过；Profile 21 个链接，
  其中 12 个站内链接及源锚点通过。
- `make check OUTPUT=/tmp/my-blogs-management-build`：70 个 HTML 页面、
  123 个公开文件通过。输入为 `8fbf29df7cdb5878b854d62a305727bef6149287`
  加本地修改，含并行任务正在维护的架构章节，不是隔离发布快照。
- `scripts/test_pipeline.py`：8 项现有测试通过；`git diff --check` 通过。
- `scripts/profile.py status` 实际读取远端 README、账号字段与置顶项目，
  逐字节比较发现新版稿尚未发布；账号仍为旧资料，主站未置顶。
- `scripts/profile.py preview` 使用 GitHub Markdown API 渲染新版；
  临时浏览器检查 390/650/1024px 均无页面整体横向溢出，项目表在手机自身容器滚动。
  点击展开和 Enter 收起通过；没有外部图片或脚本依赖。

已查看实际桌面和手机截图。公开交付预览为工作区
`github-profile-preview.html`；临时证据在
`/tmp/my-blogs-profile-preview/verification.json` 和该目录截图中。
预览 CSS 模拟 GitHub 外观，实际公开页由 GitHub 平台控制。
管理 skill 的工作区发现路径链接到仓库中的同一个权威文件。

本次管理与 Profile 修改未提交或推送；没有更新账号字段或置顶项目。
已发布旧 README 的提交为 `51246757924db14af2ea9d5b5d6c39c83767991b`。
当前 OAuth scope 缺少账号字段需要的 `user`；主站、README、账号资料和置顶须分别核对。

## 2026-11-14 · 知识体系贯通

本轮新增架构6章、Agent系统3章、部署3章、训练方法1章、科学任务2章及3个系列入口；
训练/数据旧章、8篇独立指南与DLM14章做有限复核，新增60道具体题解。
研究地图维护唯一“原理→实现→实验”覆盖表和三条阅读路线，博客直接链接路线。
13份可下载文件为研究设计、schema与容量推导，未执行真实训练、科学分析或benchmark。
来源与边界见`knowledge-expansion-research-20261114.md`及`content-audit.md`。

- 共享目录`make check OUTPUT=/tmp/my-blogs-knowledge-build`：95页/169文件通过，
  包含同期后训练专题与未提交管理检查；不作为本任务独立提交证据。
- 隔离目录`/tmp/my-blogs-knowledge-release-validation`基于`bae271a`：
  `make check OUTPUT=/tmp/my-blogs-knowledge-release-build`通过88页/154文件。
- `python3 docs/verify-content-migration.py --require-clean`：9项原SHA相同、
  32项已登记变化、299原锚点、59原标记、148公开路由通过；
  当前15本地集合/42章/6论文/2外部入口。原迁移manifest未重建。
- 现有`./scripts/test_pipeline.py`8项测试通过，暂存差异`git diff --check`通过。
- 本机Chrome：52页×390/768/1440px=156项布局、92项交互/资源、
  8项无JS检查，合计256项通过，无页面脚本错误。原生目录/前后章、
  六个机制关键词搜索、答案点击/Enter/aria、13资源SHA及CSV实际下载通过。
  无JS全部155个答案可读。保留470原问题及95原答案的逐字检查另见来源记录。

隔离浏览器输入：commit `bae271a0a021b22ee8a60b9b4be6a96b37b5c585`，
`dirty:true`，input digest
`bde3a4709c79e3f1b67e379242316d0dc2aa84edb01805ff2c500936925f5d46`。
证据在`/tmp/my-blogs-browser-tests/knowledge-check.js`、`knowledge-release-report.json`
及`knowledge-{routes-1440,attention-390,scientific-1440,capacity-390}.png`。
已看4张截图，保留原视觉与宽高比；科学章节标题精简后重新核对。

浏览器早期失败来自旧文单一h1假设、错误结果卡片选择器和索引外词汇；
修订验收脚本后仅统计最终通过项，不重写旧文去迎合测试。
内置浏览器连接不可用，使用本机Chrome/Playwright执行。

同步前远端已发布后训练专题和Profile极简稿。本任务最终从`567654e`的
`/tmp/my-blogs-knowledge-final-release`装配，保留这些已提交内容；
原共享目录的管理协议与Profile未提交改动不纳入。
最终检查、Actions与线上版本由后续实际核对确认。

最终整合快照已通过`make check`：95页/169公开文件；
迁移核验为9项原SHA、32项登记变化、299原锚点、59原标记、163公开路由，
当前16本地集合/48章/6论文/2外部入口。对同一最终产物再次执行156项布局、
92项交互资源和8项无JS检查，256项全部通过。浏览器证据为
`/tmp/my-blogs-browser-tests/knowledge-final-report.json`，
commit `567654eb63cfa772872d5fa095295c3633b2457d`、`dirty:true`、
input digest `68f1e3e099cef2dac71846c59909e17aedd5d063c02dca19f1fc349d5c6807b9`。
提交后只重新构建以记录真实commit/clean状态；发布收据保存在
`/tmp/my-blogs-browser-tests/knowledge-publication-report.json`，
以其中Actions对应版本、线上manifest与实际公开文件SHA为准。

## 2026-11-14 · Git 同步与管理协议落库

本轮先对齐已发布的`1492b6e`（Harbor专题），再提交剩余项目管理协议、
Agent入口、管理skill、构建/Pages治理检查及目录格式整理，共12个文件。
上文“项目管理协议与Profile展示稿”中的未发布描述为初次检查时的历史状态，
不能作为当前Git或Profile远端状态；本轮不改账号字段、置顶或Profile正文。

`make check OUTPUT=/tmp/my-blogs-git-sync-build`通过96 HTML页/187公开文件；
治理检查通过11份协议/skill引用，Profile本地检查22个链接（13个站内链接）。
暂存差异`git diff --cached --check`通过。构建未回写正文，
原迁移基线及差异收据未改动。本轮没有新增页面交互或科研实验结果。

## 全站目录与正文整合 · 2026-11-14

实施记录见 `organization-integration-20261114.md`。隔离工作树
`/tmp/my-blogs-organization-release` 从 `e1cfb6b` 开始，保留含同期内容的
8系列/48章节快照；正式发布前合并最新远端内容，个人事实与 Profile 沿用其独立发布。
共享工作树没有用于提交，未提交的其它任务内容继续保留。

已实际通过：

- `make governance`、`make inventory`：67 项，8 系列、48 章节、9 篇文章、2 外部入口。
- `make check OUTPUT=/tmp/my-blogs-organization-build`：96 HTML 页、173 公开文件。
- `scripts/organization.py check`：65 个源页面、2,744 个原单元、967 源锚点、
  1,546 公开锚点、来源与 AUTO 标记保留；不可变清单无例外。
- `scripts/citations.py check`：465 项来源/版本记录，189 项专题来源登记；
  编号、不同版本、多论文编号、当前/冻结使用位置与原件 SHA/长度核对通过。
- `docs/verify-content-migration.py --require-clean`：9 项原 SHA 完全匹配、
  32 项已记录有意变化、299 原锚点、59 原标记、163 注册路由通过。
  原迁移清单没有重建，当前变化不描述为字节相同。
- `scripts/test_pipeline.py`：12 项隔离测试通过，含失效引用/先修环/缺锚点/
  使用位置与版本冲突、源不回写、确定性及失败保留成功产物。
- Chrome/Playwright：192 项 390/768/1440px 布局与 79 项交互通过；
  核对全部8系列目录、48章节前后章、主页→主线→章节往返、搜索清除/恢复/空结果、
  旧锚点展开、引用返回、无 JavaScript 和目录加载失败入口。
- 实际浏览器再次输入 OPD、GRPO、Harbor、KV、GUI、DLM，
  首项分别为 OPD 主讲、现代 RL、任务合成、Attention/KV、GUI 前沿、DLM 范式。

截图与机器记录在仓库外 `/tmp/my-blogs-browser-tests/organization-*.png`、
`organization-report.json`；已查看博客桌面与 DLM 手机最终像素结果。
额外修正 DLM 自动本文目录的旧小节显示号；旧 `reading-section-*` 链接映射保留。
以上是结构与阅读验证，专题中的研究复现缺口和待执行实验保持原状态。
最终部署提交与线上核对以随后发布记录为准。

### 合并同期内容后的最终核验

已保留远端 `1492b6e` 的 Harbor Framework 完整专题与全部资源，
并维护其 43 个 `cite-*` 原引用。最终为 68 项登记、8 系列、48 章节、
9 篇当前文章加1篇历史文章、2 个外部入口；`make check` 通过97页/191文件。
统一索引适配四份来源登记共232项，生成504项来源/版本记录。
原迁移核验通过9项原SHA、32项精确收据、299原锚点、59原标记和172公开路由；
本次组织基线的2,744单元、967源锚点和1,546公开锚点持续保留。

对合并产物重新执行Chrome检查：195项布局、80项交互全部通过，
包括Harbor原引用返回与新版DLM本文目录。脚本最初对Harbor返回链接错误假设
省略`index.html`，按实际有效公开地址修正选择器后只统计通过项；
没有为测试改变原引用或正文地址。实际浏览器桥后来返回
`Browser operation belongs to an inactive execution round`，余项用本机Chrome完成。
Profile源与最新远端内容一致，没有改写个人事实或把未提交Profile稿加入发布。

最后一轮12项测试与远端合并同时运行，原测试副本携带工作树的 `.git` 指针，
导致状态比较读到了原仓库变化，且后续副本复制到了合并中的JSON。
已修正测试夹具：正文独立复制，Git引用与索引独立克隆，
仅共享不可变对象，不再通过工作树指针读取原仓库状态。
该失败不作为站点通过证据；修正后的测试结果单独核对。
随后的显示核对还统一了研究地图的现行章节链接文字，以及
任务合成/Benchmark共用文献的范围说明；冻结原文继续保留旧章号。
