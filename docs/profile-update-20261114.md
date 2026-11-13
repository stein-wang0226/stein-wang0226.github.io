# 个人主页、CV 与 GitHub Profile 更新依据

资料核对日期：2026-11-14。本记录区分作者提供的履历、公开论文元数据与待确认项。
新版主页和附件的本地实施、校验及远端状态将在完成后补记。

## 输入材料与优先级

| 来源 | 页数 / 大小 | SHA-256 | 用途 |
|---|---|---|---|
| `/Users/bytedance/Desktop/resume-template/outputs/pdf/resume.pdf` | 2页，264,854字节 | `639a6be51226e0cb58ba251674430343b34fcd3be1cf23ffce9f48c4c0e700ab` | 用户明确引用的新版中文研究简历，内容主依据 |
| 用户上传 `王煜祥简历.pdf` | 2页，1,729,410字节 | `13763f188510ea377ce5b9895601524cf9c1b36287e049baab5e30642b1f0e72` | 交叉核对项目、时间与量化结果，保留原件 |
| 同产物目录 `resume-en.pdf` | 3页，79,396字节 | `1e479455f75403182378dea8282a4bdd685ae5c6d1ea5616e82dde803c59b2f0` | 现成英文附件；核心事实与新版中文一致 |

新版中文PDF元数据标题为“王煜祥 · 研究型简历”，2026-11-13生成；
上传版元数据为2026-11-11。日期只解释输入版本，不作为论文发表日或项目起始日。
临时逐页文本和页面预览位于 `/tmp/resume-profile-review/`，不作为站点运行依赖。
使用逐页提取与任务查询检索；中文两版已覆盖全部页面，英文核对教育、论文、实习和项目页。

## 已核对的履历事实

- 姓名王煜祥 / Yuxiang Wang；复旦大学大数据学院人工智能方向硕士，知识工场实验室，
  2025.09–2028.06（预计）；本科杭州电子科技大学卓越学院，2021.09–2025.06。
- GPA 4.59/5.0；新简历采用专业前1%，以此替换旧主页的前0.6%，不推断新的精确排名。
- 字节跳动 Seed / AI Data，GUI Agent 数据算法实习生，2026.09至今。
- 阿里巴巴平台技术 / AIR计划，Research Intern，2025.12–2026.09；
  替换旧CV的2025.10至今。天翼交通科技VLA实习2025.04–2025.07保持一致。
- 联系方式采用作者提供的复旦邮箱；附件保留原始内容，不改写用户PDF。

## 推荐突出工作的证据边界

### AutoResearch：科学 Harbor 任务合成

作者负责将专家Skill / Protocol工程化，贯通Data Audit、Task Generation、Calibration、
Rollout、Refinement、Evaluation与SFT验证；Solver / Verifier隔离、多路径校准、
跨模型Rubric Judge用于识别评测缺陷、推理错误及Reward Hacking。
Multi-Agent批量系统支持并发、断点恢复和版本追踪，累计交付2,000+个Harbor任务包。

简历说明数据经Qwen3.8-27B SFT验证后交付Qwen后训练团队，推动Terminal-Bench等指标提升，
相关任务提交Terminal-Bench Sci并通过一轮review。没有具体提升数值；
不将其写成正式接收、公开发布全部任务或独立复现的榜单收益。

### ProtAgent：步骤级 Agentic RL

Qwen3-8B、五类蛋白质注释任务；Tool-Trajectory SFT → On-Policy RL。
方法为Batched Step-Level REINFORCE，对中间工具调用与最终答案分别设reward，
按交互步骤计算reward-to-go并更新对应响应token。替换旧CV将当前项目概括为GRPO的表述。

作者项目实验的五类任务均衡OOD-1000上，Base14.1%、SFT40.2%、RL61.0%；
SFT→RL为+20.8个百分点。主页可突出结果并标明评测集；
不补未知seed、生成预算、统计显著性或独立第三方验证。
两份简历的闭源模型比较未提供完整同预算协议，网站编辑稿优先展示本项目内部阶段对照；
原附件中的完整比较照原件保留。

### GUI Agent 数据与环境

Setup–GUI Rollout–Verify–Reset、Trace回放、独立Oracle正负例与产物审计；
区分App缺陷、Agent失败和环境异常；复核9,641个Trace事件。
真实回流任务以冻结初始条件、干净VM关键动作重放和资产 / 动作双重验证转化为RL任务。
9,641是事件数量，不写成独立任务数或用户数。

### Holon / ProtText-Eval

Protein–Text双向建模，蛋白预训练、多模态CPT、科学SFT；UniRef与文本–蛋白配对混合，
Muon、Token配比和Scaling实验，0.6B→8B。
0.6B六组SFT对照中，通用 / 专业混合数据的IFEval比纯专业训练提升29.02个百分点。
15.3%→21.2%的指标，新中文和英文版称蛋白位点坐标判别，上传旧版称P3描述排名；
若不能获取正式指标定义，网站不扩大解释，优先采用一致的IFEval对照。
ProtText-Eval覆盖生成、编辑、理解、指令对齐、序列 / 结构质量与下游效果。
旧材料中的18工具、26指标等细节未由新简历再次确认，保留历史来源，不改写成新的实测结果。

## 论文标题、状态与作者核对

1. **Semantic DLM+**：两份新简历与英文版均写NeurIPS2026已录用、一作。
   [arXiv:2606.15327v1](https://arxiv.org/abs/2606.15327v1) 于2026-06-13提交；
   作者顺序Keyue Jiang、Yuxiang Wang等，公开PDF首页没有共同一作标记，仍写Preprint / Under review。
   可按作者新资料更新录用状态并注明状态来源；保留公开版citation作者顺序。
   **录用版本是否更换作者顺序或注明共同一作尚待作者确认**，编辑稿先不将“一作”作为该论文的公开标签。
2. **On the Trainability of Masked Diffusion Language Models via Blockwise Locality**：
   [arXiv:2604.24832v1](https://arxiv.org/abs/2604.24832v1) 的正式标题、Yuxiang Wang第一作者、
   2026-04-27首发已核对；新简历写ACL2027在审。
   保留已有`2026-locality-aware-dlm` ID与URL，修正旧展示标题和错误的2026-03发表日期。
3. **ProtAgent**：简历标题为“Step-Level Post-Training Agent for Protein Understanding”，
   新版写ARR在审、一作；上传版清单写ACL2027，正文写ARR在审。
   用户随后提供 [arXiv:2610.33746](https://arxiv.org/abs/2610.33746)，公开正式标题为
   **ProtAgent: Post-Training Compact Protein Tool Agents with Interaction-Level Credit Assignment**，
   首发2026-10-24，Yuxiang Wang为首位作者。站点改用公开标题、作者顺序与首发日期；
   ARR在审状态仍采用新版简历，arXiv首发不等于ARR投稿日期。
4. **STM: A Spatio-Temporal Model for Dynamic Graph Fraud Detection**：
   [DOI / Crossref元数据](https://api.crossref.org/works/10.1007%2F978-981-95-3906-2_3) 确认正式标题，
   作者首位Yuxiang Wang、会议DASFAA2025、在线出版2026-01-02、页37–52。
   修正旧记录泛称CCF-B / Springer及2024发表日，保留原URL和研究期2023.04–2024.08的区分。
5. **CUA-Recovery: Benchmarking Error Recovery in Long-Horizon Computer-Use Agents**：
   两份简历均写ICLR2027在审；未提供作者顺序、公开链接、准确投稿日期或论文实验结果。
   只使用标题与在审状态，不猜测一作或以实习结果代替论文结果。

原SemDLM研究记录与SemDLM+分别保留，不因最新简历未列旧工作而直接删除。
对缺失的日期使用明确的未知日期支持或履历条目，不能用本次编辑日冒充发表日。

## GitHub 与旧地址的现状

通过只读gh CLI核对：

- Profile `stein-wang0226`：display name为`stein-wang`，bio为Fudan / LLMs / Diffusion / AI4S，
  website仍为`https://stein-wang0226.github.io/wyx0226.github.io/`。
- Profile README仓库`stein-wang0226/stein-wang0226`，分支main；
  README仍写Alibaba在岗、旧论文标题 / 状态与July2026更新时间，包含大量外部统计图。
- 主维护仓库`site/`对应`stein-wang0226/stein-wang0226.github.io`。
  本次开始时HEAD为`2e6bfce94c4825b955d09e680a3722aa9973d71c`，工作区干净。
- 旧学术仓库`stein-wang0226/wyx0226.github.io`仍从master根目录使用legacy Pages，
  其前缀占用使主站本地的兼容跳转不能直接控制用户给出的两个线上旧URL。

新版主站的规范入口为根站、`/about/`、`/cv/`、`/publications/`与`/blog/`。
本地优化及Profile README / settings建议可以先完成；GitHub资料修改、两个仓库的提交 / 推送、
旧Pages切换分别需要既有或新的明确授权，不把“优化主页”自动视为停用旧站。
本轮至此没有进行远端写入。

## 本地实施结果

已依据上述材料更新：

- `content/pages/about.md`：当前 ByteDance Seed / AI Data 实习、已完成的 Alibaba AIR 实习，
  Harbor、ProtAgent、GUI 环境与 Holon 四项工作，履历时间、研究方向、新闻与下载。
- `content/pages/cv.md`：教育、实习、项目方法与结果、科研、技能及历史内容；项目锚点稳定为
  `autoresearch`、`protagent`、`gui-agent`、`holon`。
- 首页从 `about.md` 的 `Selected Work` 生成近期工作卡片；没有另建第二份项目数据。
  论文与笔记仍从共享记录生成，新增 `profile.css` 只负责个人资料组件。
- 修订 STM、Blockwise Locality、SemDLM+ 三条记录；补入 ProtAgent 与 CUA-Recovery。
  原 SemDLM 记录仍保留，总计6条记录。
- 缺失日期的CUA-Recovery使用 `date: null` / `date_label`；
  ProtAgent后续由用户提供的arXiv链接补齐公开日期。校验要求未知日期的明确标签，拒绝以编辑日填充。
- `docs/github-profile/` 保存可直接用于 Profile 仓库的 README、name / bio / website 建议，
  以及先部署主站、再同步 Profile 的顺序。bio 为120个字符，在 GitHub 限制内。

通过 gh 核对了公开的 `trainable-masked-diffusion` 和 `STM` README，加入实现链接。
`terminal-bench-science` 是 `harbor-framework/terminal-bench-science` 的公开 fork，
在 Profile 稿中明确保留 fork 归属；未把 Harbor 内部任务、ProtAgent 或 Holon 的私有代码当成公开资源。

## 附件与历史保留

| 公开路径 | 内容 | SHA-256 |
|---|---|---|
| `/assets/Curriculum_Vitae.pdf` | 原始英文研究简历，3页 / 79,396字节 | `1e479455f75403182378dea8282a4bdd685ae5c6d1ea5616e82dde803c59b2f0` |
| `/assets/Yuxiang-Wang-Resume-en.pdf` | 构建生成的英文别名，同一份源文件 | 同上 |
| `/assets/Yuxiang-Wang-Resume-zh.pdf` | 原始中文研究简历，2页 / 264,854字节 | `639a6be51226e0cb58ba251674430343b34fcd3be1cf23ffce9f48c4c0e700ab` |
| `/assets/archive/Curriculum_Vitae-before-20261114.pdf` | 原 CV，2,502,216字节 | `66b3c0d7c7cf44f23caf4cae80eaaac4e8948373fe39b682fc2111c2735ccde6` |

旧下载路径 `/wyx0226.github.io/assets/Curriculum_Vitae.pdf` 在本地构建中与新版英文附件一致；
线上前缀仍受旧项目 Pages 控制，不能由本地副本证明线上已切换。

旧 about、CV 和三篇修改论文的完整源文件保存于 `content/archive/profile-before-20261114/`，
用户上传的原始简历保存为 `uploaded-resume.original.pdf`；该目录未进入公开构建。
外部 `resume-template`、原上传文件均未修改。`docs/content-migration-manifest.json` 没有重建，
本次受覆盖的七项更改分别在 `docs/content-changes.json` 记录精确 SHA 和理由。

## 本次实际验收

- `make check OUTPUT=/tmp/my-blogs-profile-build`：**59 HTML页 / 79公开文件**；登记、链接、
  锚点、导航、论文、原自动标记及产物白名单通过。
- 隔离 `scripts/test_pipeline.py`：原六项通过；新增未知日期检查首次因测试用例被 YAML
  日期解析器提前拒绝而失败，改为显式字符串日期后单独复验通过。七项均获得通过结果；
  包括重复构建字节一致、源未被构建回写、失败保留旧产物和未知日期不伪造。
- `docs/verify-content-migration.py --require-clean`：23项原 SHA 完全相同、
  18项有意后续变化有记录；299个原始锚点、59个标记保留。原9集合 / 14章保留，
  当前10集合 / 18章 / 6论文 / 2独立子站。
- 实际 Google Chrome：**56项检查通过**。其中33项为11条路径 × 390 / 768 / 1440px；
  其余覆盖键盘跳正文、主页项目→CV、稿件往返、CV分区导航、两种真实下载、
  英文别名 / 旧地址 / 历史PDF字节、论文覆盖、主题按钮、Harbor搜索 / 刷新 / 空结果 / 清除。
- 禁用 JavaScript 的5页阅读与项目跳转通过；无浏览器脚本错误。
  实际查看桌面首页、手机项目卡片和手机CV截图，布局可读，无整页横向溢出。

浏览器报告与截图位于 `/tmp/my-blogs-browser-tests/profile-report.json`、
`profile-home-1440.png`、`profile-home-390.png`、`profile-work-390.png`、`profile-cv-390.png`。
这些是当次验证证据，不是站点运行依赖。

本次构建记录：commit `2e6bfce94c4825b955d09e680a3722aa9973d71c`、`dirty: true`，
输入摘要 `e09f9b60f0f89ea820d47e39992fdc4d0d5091641514b8433518ce731bda05a8`。
本地预览实际运行于 `http://127.0.0.1:8768/`，对应 `/tmp/my-blogs-profile-build`。
校验和界面通过不等于独立复现项目科研结果。

## 最终远端边界与待确认事实

完成时再次只读核对：主站远端main仍为 `2e6bfce`；
GitHub Profile display name仍为 `stein-wang`，bio仍为旧Fudan / diffusion介绍，
website仍指向旧 `/wyx0226.github.io/`。本次没有提交、推送、写入 GitHub Profile、
切换或停用旧 Pages。Profile 发布稿中的新增线上链接需要主站部署后才能正式使用。

SemDLM+ 的最新简历一作标注与公开v1顺序差异仍待录用版确认；当前编辑稿保留公开citation，
没有猜测共同一作。Harbor review、项目评测与 CUA-Recovery 作者信息的边界如前文所述。

## 用户补充论文链接与主会接收确认后的最终复验

用户明确补充 `https://arxiv.org/abs/2610.33746`，并确认 SemDLM+ 已获 NeurIPS 主会接收。
核对三个公开摘要页：

| 工作 | arXiv | 公开首发 | 当前展示 |
|---|---|---|---|
| ProtAgent | `2610.33746` | 2026-10-24 | 正式公开标题、第一作者、ARR在审 |
| Blockwise Locality / Trainability | `2604.24832` | 2026-04-27 | 正式公开标题、第一作者、ACL2027在审 |
| Semantic DLM+ | `2606.15327` | 2026-06-13 | **NeurIPS 2026 Main Conference — Accepted** |

主页精选论文将SemDLM+置于首位。NeurIPS主会接收是用户明确确认的信息，
不因arXiv v1尚保留preprint标记而降回在审。没有推断oral / spotlight / poster类型，
公开citation仍遵循现有arXiv作者顺序。

ProtAgent公开摘要进一步提供三随机种子信用分配对照：
identity normalization下episode-level均值42.70%、step-level61.40%；
group-relative下36.50%与58.20%。论文详情已补充此表。
61.40%均值与61.00%主结果分别标明，未合并为同一个实验数字。
主页、CV与Profile稿将成功指标明确为annotation coverage；
按论文说明，它衡量固定协议下的参考注释恢复，不能单独证明生物正确性或完整证据支撑。

最终从本次修订后重新执行：

- `make check OUTPUT=/tmp/my-blogs-profile-build`：59 HTML页 / 79公开文件，通过。
- `scripts/test_pipeline.py`：完整7项在同一次运行中全部通过。
- `profile-check.js`：**61项全部通过**，包括三个arXiv链接、ProtAgent正式标题与首发日期、
  SemDLM+主会接收，以及此前布局 / 下载 / 导航 / 无脚本范围。
- 原始迁移保留检查通过：23项原SHA相同、18项记录变化，299个锚点、59个标记保留。
- `git diff --check`通过；将CV的Markdown行尾换行改为等效显式`<br />`。

最终构建commit仍为 `2e6bfce94c4825b955d09e680a3722aa9973d71c`、`dirty: true`；
input digest为 `1980c6a2c5a71f5fbd978011b987d26a8f2312def0bf59d8519386ba9c461a20`。
61项浏览器报告对应此最终修订。本文较早的56项 / 旧digest是初轮验收记录，不代表最终输入。
本次没有新增远端写入，预览仍为 `http://127.0.0.1:8768/`。

## 用户授权同步后的实际发布记录

本节记录用户随后要求“github 同步推送”后的真实结果，取代前文仅本地完成时的远端状态描述；
此前本地检查和历史状态保留，不回写成当时已经发布。

- 唯一主维护目录：`/Users/bytedance/Desktop/my_blogs/site`；
  `origin` 为 `git@github.com:stein-wang0226/stein-wang0226.github.io.git`，分支 `main`。
- 个人资料内容提交：
  `5801b4ea856c09077639230cffb37554c535a87d`，已推送。
  [Validate site](https://github.com/stein-wang0226/stein-wang0226.github.io/actions/runs/43493652355)
  与 [Publish static site](https://github.com/stein-wang0226/stein-wang0226.github.io/actions/runs/43493652124)
  均成功。
- 实际线上 `build-info.json` 核对提交为 `5801b4e`、`dirty: false`，
  input digest 为 `8ad74f7a02a071b27e74251f16523783203a7a996d093ff15acb1a991a1e498a`。
  发布清单登记78个文件，另加清单自身为79个公开文件。
  实际下载首页、About、CV、论文列表、ProtAgent、CUA-Recovery、SemDLM+及三个中英文PDF
  路径，共10个文件，SHA全部与发布清单一致；三个PDF同时与本地原附件一致。
- 实际浏览器从首页进入About，再进入CV：当前字节实习、四项近期工作、中英文下载入口、
  CV的四个项目锚点均正确。首页SemDLM+显示NeurIPS 2026主会接收；
  与本地61项验收分别记录，没有将线上抽查计成重复完整验收。
- GitHub Profile 仓库 `stein-wang0226/stein-wang0226` 提交
  `51246757924db14af2ea9d5b5d6c39c83767991b` 已推送至 `main`。
  通过 gh 读取远端README，确认与 `docs/github-profile/README.md` 逐字节一致，
  SHA-256 为 `05eb45090d7513d04034f6d190df9e9e1474a4acdb25cebd36ede2a3d237fdb1`。

账号 `name` / `bio` / `blog` 的 PATCH 返回HTTP404，并由gh明确提示缺少 `user` scope。
当前授权为 `gist` / `read:org` / `repo`；随后重新查询，三个字段仍为原值。
已准备 `docs/github-profile/settings.json` 并发起设备授权，须待用户登录完成授权后再写入。
浏览器已交由用户操作，不能将授权请求已发起记为授权完成或字段写入成功。

旧学术仓库 `stein-wang0226/wyx0226.github.io` 实测仍未归档，
legacy Pages从 `master` 根目录提供 `/wyx0226.github.io/`。
有效内容已迁入主站，旧提交历史仍独立保留；建议迁移旧链接后归档保留。
GitHub用于显示Profile README的同名仓库 `stein-wang0226/stein-wang0226` 必须保留，
它是账号展示机制的入口；源稿统一在主站维护不改变这一要求。
本次没有删除、归档或停用旧仓库。

同步期间另一个维护线程提交了样式 / 缓存修正 `2ad31ae`、`618f66b`；
它们位于主站内容提交之后。本文的线上SHA和浏览器抽查明确对应 `5801b4e`，
后续文档提交与最终站点版本以最新Actions及线上 `build-info.json` 为准。
