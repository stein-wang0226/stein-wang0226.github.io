---
title: harbor-task-sync：科学任务合成与证据驱动迭代
---

<p><a href="../">My Work 目录</a> · <a href="full-report.html">完整 GEO-Harbor 方法报告</a></p>

本项目的主报告为 [GEO-Harbor-Bench-Method-Report.html（Unified-produce）](https://github.com/stein-wang0226/harbor-task-sync/blob/Unified-produce/docs/GEO-Harbor-Bench-Method-Report.html)。完整正文已收录在 My Work 的 harbor-task-sync 目录；本页补充方法路线、实现与实验边界，来源快照版本见末节。

## 项目定位与方法路线

harbor-task-sync 将公开组学研究转化为可执行、可复核的 Harbor 科学任务。它把候选发现、来源审计、造题、质量检查、隔离盲测、判分和交付拆成角色与落盘产物。项目研究的对象包括任务产线，以及完成任务后能否通过 refinement 增加真实科学难度。[1](#ref-1)[2](#ref-2)

```text
public study → candidate discovery → source audit + data scope freeze
  → task authoring → deterministic gates → isolated Solver
  → independent Verifier → rubric + failure attribution
  → self-contained task package → lifecycle + delivery inventory
```

最关键的设计是分开治理开放科学问题与确定性判分：公共合同保留合理的方法自由度，私有校准记录合法分析路径及错误反例，verifier 对最终输出检查证据。产线能运行、任务完成、打包验收、科学难度认证与训练收益是不同结论。[1](#ref-1)

## 公开研究怎样成为任务

候选审计首先确认数据可得、实验设计有效、分析深度足够、运行预算可承受及输出能客观判分。在下载大型原始数据之前冻结输入范围，区分 raw、near-raw、intermediate、processed 与 answer-bearing 数据。源论文的结论是待检验的假设，不能直接写进 oracle。[1](#ref-1)[2](#ref-2)

来源图应连接 accession、样本、论文、补充资料、作者代码、参考基因组及注释版本。确定性 fixture 的每次切片、转置、筛选和重命名都要记录输入/输出 hash、脚本、参数、计数和 schema。输入的坐标、单位、样本映射、缺失语义和设计边界必须公开，避免把难度建在隐藏事实上。

一个有科学深度的任务通常保留“验证数据 → 聚合/比较 → 统计判断 → 生成结果”等实质分析。大文件搬运、复制作者 hit list、强制指定工具链或隐藏 JSON 字段不能作为难度来源。这里描述的是产线方法要求，不是每个历史任务都已经独立完成了全部证据审计。[1](#ref-1)

## 公共合同与私有评价的边界

| 资产 | Solver 可见 | 作用 |
| --- | --- | --- |
| `instruction.md` | 是 | 科学目标、输入语义、输出 schema、运行边界 |
| `environment/data/` | 是 | 冻结的公开 fixture 和 checksum |
| `task.toml` 与环境 | 按 harness 合同 | 时间、内存、依赖和输出声明 |
| `solution/` | 盲测排除 | 参考分析与 oracle 生成 |
| `tests/` | 盲测排除 | 独立 verifier、测试入口与判分材料 |
| `authoring/` | 盲测排除 | 来源、校准、反例与出题证据 |

任务包可以同时保存公开与私有两类资产，但运行时必须从 agent 的文件树物理排除答案相关部分。Solver 只基于公共问题生成并冻结答案；Verifier 在独立环境中评分。参考解跑通仅属于 maintainer 自检，不能代替盲测。[1](#ref-1)[2](#ref-2)

## 多路径 oracle 与完整结果一致性

科学问题允许多个合理实现时，先实际运行可接受路径，观察数值、集合或坐标变化，再冻结评分范围。known-wrong、边界和等价表示与合法路径共同约束 verifier，避免只校验 canonical 输出。[1](#ref-1)[3](#ref-3)

一个反复暴露的缺陷是**逐字段包络接受了无法由任何完整分析产生的拼接结果**。例如每个基因的效应值都来自某条合法 normalization 路径，但整张表混用了不同路径；每个标量都“在范围内”，联合产物却不属于任何合法结果。解决方向是把允许的完整路径或可验证 invariant 纳入合同，而不是机械放宽容差。[3](#ref-3)[4](#ref-4)

对每个任务，最小检查应覆盖正确结果、科学错误、部分错误、边界容差、缺失与稀疏零、重复和 malformed 输出、错误单位或坐标，以及历史盲测失败。任务可判性来自这些具体证据。

## 角色接力、门禁与失败恢复

低成本的确定性 gates 在昂贵盲测前检查包结构、schema、题面泄漏、依赖可重放性、oracle、test.sh 和校准一致性。Judge 再按规格、可解性、科学依据和结果验证等 rubric 评审；不同角色看到的材料受白名单控制。[1](#ref-1)

盲测失败先归因再修复：题面缺陷、公开证据不足、verifier 错误、reward hacking、真实科学难点、near miss、timeout 与拒答走不同路线。网络、队列、容器、transport 或 CLI 协议失败属于基础设施问题，不能转写成科学拒绝。[1](#ref-1)[2](#ref-2)

生命周期和 resume 保留同一 task slug、来源 accession 与证据链。任何改变 instruction、fixture、scorer 或 oracle 的修复都可能使旧证据失效，需要重新认证。完成任务的增量交付还要检查历史库存：`packaged=yes` 永久排除后续批次，不因 Harbor v2 修复或质量升级重新获得打包资格。[2](#ref-2)[5](#ref-5)

## Refinement 怎样避免“假加难”

Refinement 从已完成任务开始，锁定科学问题、数据和预算，增加可验证的科学判断。流程是 parent 冻结 → 准确性审计 → parent headroom → 定向 operator → child 独立质量检查 → 同条件配对盲测 → 失败归因与接受/停止。[3](#ref-3)

```text
accept child only if
  quality preserved
  AND preregistered difficulty effect observed
  AND failures attributed to the new scientific bottleneck
```

质量缺陷先走 `repair_required`。质量合格且有测量余量才是 `hardening_candidate`。pass@1 为主，pass@2/4 补充；qualification 筛选与正式样本的分母分开。身份漂移、基础设施无结论和中途换 runner 不产生有效科学证据。[3](#ref-3)

| 当前主说明中的代表结果 | 支持的解释 |
| --- | --- |
| V5.2：parent/child 都是 5/5 + 3/4，drop=0 | 质量通过但 operator 无观测增益 |
| v4：原 scorer child 为 0/5 + 0/4 | 单看通过率会得到强下降；9/9 失败被归为规格缺陷 |
| v4：合同一致的反事实 child 为 5/5 + 4/4，drop=0 | 原下降是 verifier universe mismatch，不能算科学加难 |
| v6：两题 parent/child 都是 5/5 + 4/4 | invariant-first 质量闭合但无难度变化 |
| v14：完整 4题 calibration 只有 1/4 命中 headroom，低于 ≥2/4 | parent 选择规则 No-go；不是 operator 效果结论 |
| v15：pre-live、isolation 与 dry-run 已准备 | 在本次读取的固定版本中尚未产生 parent 结果 |

上述记录来自 2026-11-12 更新的当前主说明；它明确记录 accepted child 仍为 0。这个停止结果同样具有方法价值：归因、反事实和预注册边界阻断了质量缺陷导致的假阳性。不能以大量工程检查、任务交付或通过率下降代替 refinement 有效性。[3](#ref-3)

## 规模与报告数字怎样阅读

原始 GEO-Harbor 方法报告保留 740 ready、413 done、70%+ / 91.0% 成功率以及成本估计，并已标明这些是原稿历史口径。它没有重新核验批次、分母、价格来源和全部执行证据，因此本页不将其更新为 2026-11-14 的生产读数。[1](#ref-1)

项目简历中“2,000+ task packages”对应作者提供的更大范围交付事实，也不能与本机 GEO 库存直接求比。若要报告当前库存，应从 task-record、campaign 状态和 tracked coordination inventory 重新聚合，分别给出来源、批次、完成、历史打包与本次新增。[5](#ref-5)

## 实现入口与复核范围

当前 GitHub 默认分支是 `Unified-produce`。先读 README 与 `docs/README.md`，再看 production 与 refinement 主说明；角色 prompt、gates、Solver/Verifier、lifecycle 和 packaging 的实现位于 `pipeline/`。旧环境分支和旧状态叙述只作历史背景，本页不修改本机生产配置。

本次使用 GitHub 固定版本报告、当前 refinement 主说明与仓库规则核验方法和结论边界，没有启动 task pipeline、盲测、清理或打包。完整原稿在[方法报告](full-report.html)中保留。

## 来源与固定版本

GitHub 固定到 `0efe0d276c6f4f2d804897843620ba7cb73974e7`，需要权限。

1. <span id="ref-1"></span>[GEO-Harbor-Bench 方法报告](https://github.com/stein-wang0226/harbor-task-sync/blob/0efe0d276c6f4f2d804897843620ba7cb73974e7/docs/GEO-Harbor-Bench-Method-Report.html)：原稿历史统计与 2026-11-05 文档说明。
2. <span id="ref-2"></span>[当前 README](https://github.com/stein-wang0226/harbor-task-sync/blob/0efe0d276c6f4f2d804897843620ba7cb73974e7/README.md)：来源、运行边界与入口。
3. <span id="ref-3"></span>[Refinement 主说明](https://github.com/stein-wang0226/harbor-task-sync/blob/0efe0d276c6f4f2d804897843620ba7cb73974e7/docs/refinement-mvp-implementation.md)：2026-11-12，验收、反事实、v3–v15 与停止边界。
4. <span id="ref-4"></span>[版本与证据失效设计](https://github.com/stein-wang0226/harbor-task-sync/blob/0efe0d276c6f4f2d804897843620ba7cb73974e7/docs/refinement-chain-design.md)及[历史 refinement 记录](https://github.com/stein-wang0226/harbor-task-sync/blob/0efe0d276c6f4f2d804897843620ba7cb73974e7/docs/refinement-v1-status.md)。
5. <span id="ref-5"></span>[生产记录与打包规则](https://github.com/stein-wang0226/harbor-task-sync/blob/0efe0d276c6f4f2d804897843620ba7cb73974e7/docs/production-status.md)。作者项目规模另参见站点[在线 CV](../../cv/#autoresearch)，两者统计范围分别保留。
