---
title: harbor-task-sync：科学任务合成与证据驱动迭代
---

<p><a href="../">My Work 目录</a> · <a href="full-report.html">完整 GEO-Harbor 方法报告</a></p>

## 先记住：公开合同、完整路径、独立盲测

harbor-task-sync 将公开组学研究转化为可执行、可复核的 Harbor 科学任务。它把候选发现、来源审计、造题、质量检查、隔离盲测、判分和交付拆成角色与落盘产物。项目研究的对象包括任务产线，以及完成任务后能否通过 refinement 增加真实科学难度。[1](#ref-1)[2](#ref-2)

**方法链：公开研究 → 来源/输入冻结 → 造题与校准 → 门禁 → 隔离 Solver → 独立判分 → 交付与版本登记。** 下图强调运行时的信息边界。

最关键的设计是分开治理开放科学问题与确定性判分：公共合同保留合理的方法自由度，私有校准记录合法分析路径及错误反例，verifier 对最终输出检查证据。产线能运行、任务完成、打包验收、科学难度认证与训练收益是不同结论。[1](#ref-1)

<!-- WORK:KNOWLEDGE:START -->
## 知识讲解：任务合同、oracle 与 verifier {#work-knowledge}

**Benchmark task** 包括输入、问题、环境、输出及判分，而不只是题面。**公共合同** 是求解者能看到且应遵守的规则；**oracle** 是经来源与分析校准的参考结果；**verifier** 是读取求解结果并执行规则的程序。oracle 本身也会出错，所以不能用“与参考脚本逐字一致”替代科学判断。

**Fixture** 是版本冻结、可重放的数据输入。它可以是有依据的公开数据切片，但必须保留转换出处。**盲测** 要隔离求解者与答案材料；由看过答案的 maintainer 跑参考解，是自检。**Refinement** 试图改变科学推理瓶颈，同时保留可解性与合法方法空间。[1](#ref-1)

<figure class="work-mechanism">
<svg viewBox="0 0 840 220" role="img" aria-labelledby="harbor-contract-title harbor-contract-desc" xmlns="http://www.w3.org/2000/svg">
<title id="harbor-contract-title">科学任务的公开执行与私有判分边界</title><desc id="harbor-contract-desc">公开来源形成冻结输入和题面，求解者产出答案；私有校准参考与反例约束独立验证器，验证器只在答案冻结后评分。</desc>
<g fill="#f7f5f0" stroke="#a9cec7"><rect x="5" y="20" width="180" height="65" rx="6"/><rect x="225" y="20" width="180" height="65" rx="6"/><rect x="445" y="20" width="180" height="65" rx="6"/><rect x="665" y="20" width="170" height="65" rx="6"/><rect x="225" y="145" width="180" height="60" rx="6"/><rect x="445" y="145" width="180" height="60" rx="6"/><rect x="665" y="145" width="170" height="60" rx="6"/></g>
<g fill="none" stroke="#0f766e" stroke-width="2"><path d="M185 52H225M405 52H445M625 52H665M92 85V175H225M405 175H445M625 175H665M750 85V145"/></g>
<path d="M215 115H835" stroke="#b2b0aa" stroke-dasharray="6 5"/>
<g fill="#172d35" text-anchor="middle" font-family="system-ui,sans-serif" font-size="16"><text x="95" y="48">公开研究与来源</text><text x="95" y="70" font-size="13">版本、语义、转换记录</text><text x="315" y="48">fixture + 题面</text><text x="315" y="70" font-size="13">求解者可见</text><text x="535" y="48">隔离 Solver</text><text x="535" y="70" font-size="13">合理方法空间</text><text x="750" y="48">冻结答案</text><text x="750" y="70" font-size="13">输出与分析证据</text><text x="315" y="170">私有校准</text><text x="315" y="192" font-size="13">合法路径 + known-wrong</text><text x="535" y="170">独立 Verifier</text><text x="535" y="192" font-size="13">联合一致性与容差</text><text x="750" y="180">评分与失败归因</text></g>
</svg>
<figcaption>虚线分隔求解者可见与私有评价材料；隔离必须在运行环境中实现，仅在题面声明“不要看答案”不构成盲测。<a href="#ref-1">1</a></figcaption>
</figure>
<!-- WORK:KNOWLEDGE:END -->

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

<!-- WORK:EXAMPLE:START -->
### 为什么逐字段容差不能代表完整科学结果 {#work-example}

设合法结果 A=(1,10)、B=(2,20)。逐字段范围是第一列 [1,2]、第二列 [10,20]，会接受 (1,20)；该向量混用了两条路径。即使每个值都合法，整张结果仍可能不一致。

一种可考虑的设计是围绕**完整路径**建立接受域的并集，或检查科学 invariant：

<div class="reading-math">\[
\begin{aligned}
\mathcal A_{\rm box}
&=\prod_j[\min_a y_j^{(a)},\max_a y_j^{(a)}]\\
\mathcal A_{\rm path}
&=\bigcup_a\mathcal A_a\\
\mathcal A_a
&=\{y:\ \forall j,\ d_j(y_j,y_j^{(a)})\le\epsilon_j\}
\end{aligned}
\]</div>

完整路径并集之外还检查标识符、单位、坐标和联合 invariant。这里给出接受域思路；容差和距离须由具体科学对象校准。

这只是接受域的数学说明，不是所有任务的通用 scorer；集合输出、排序、稀疏计数和统计估计需要各自的距离或一致性规则。容差 `ε` 必须来自实际合法路径及数值误差，不能围绕某次 Solver 失败任意调大。[3](#ref-3)[4](#ref-4)

### 从一个组学任务的输入走到交付

下面是教学流程，不对应新生成任务，也没有新增实验结果。假设科学目标涉及样本分组的差异分析，先公开样本 ID、实验条件、参考注释版本与输入矩阵语义，再要求输出效应、统计证据和标识符。题面字段以实际任务合同为准。

1. 从 accession 和样本元数据确认配对、批次、重复及排除规则；不能只凭文件名猜组别。
2. 记录公开数据到 fixture 的转换、hash、计数与单位；输入若已经含作者最终 hit list，需要重审 answer-bearing 风险。
3. 用可接受的分析路径形成校准结果，检查模型设计、归一化、缺失/零和多重检验语义。
4. 制作 wrong-unit、wrong-group、混拼路径、重复 ID、缺失输出等负例；同时确认合法替代表达能通过。
5. 只挂载公共数据给 Solver；冻结答案后由独立 Verifier 判分，保存运行命令、结果和失败归因。

这条链路的价值在于每一跳都能对应输入和落盘证据。容器里安装了分析软件、答案格式正确或参考解跑通，都不能单独证明科学可判性。[1](#ref-1)[2](#ref-2)
<!-- WORK:EXAMPLE:END -->

## 角色接力、门禁与失败恢复

低成本的确定性 gates 在昂贵盲测前检查包结构、schema、题面泄漏、依赖可重放性、oracle、test.sh 和校准一致性。Judge 再按规格、可解性、科学依据和结果验证等 rubric 评审；不同角色看到的材料受白名单控制。[1](#ref-1)

盲测失败先归因再修复：题面缺陷、公开证据不足、verifier 错误、reward hacking、真实科学难点、near miss、timeout 与拒答走不同路线。网络、队列、容器、transport 或 CLI 协议失败属于基础设施问题，不能转写成科学拒绝。[1](#ref-1)[2](#ref-2)

生命周期和 resume 保留同一 task slug、来源 accession 与证据链。任何改变 instruction、fixture、scorer 或 oracle 的修复都可能使旧证据失效，需要重新认证。完成任务的增量交付还要检查历史库存：`packaged=yes` 永久排除后续批次，不因 Harbor v2 修复或质量升级重新获得打包资格。[2](#ref-2)[5](#ref-5)

## Refinement 怎样避免“假加难”

Refinement 从已完成任务开始，锁定科学问题、数据和预算，增加可验证的科学判断。流程是 parent 冻结 → 准确性审计 → parent headroom → 定向 operator → child 独立质量检查 → 同条件配对盲测 → 失败归因与接受/停止。[3](#ref-3)

- **先过质量门**：来源、合同、oracle、verifier 与可解性保持。
- **再看注册效果**：同条件 parent/child，qualification 与正式分母分开。
- **最后查失败原因**：下降来自新增科学瓶颈，规格或基础设施错误不计为加难。

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

### pass@k 与难度下降怎样解释

pass@k 问 k 次机会中是否至少成功一次。n 次可交换尝试中有 c 次成功，选出 k 次全部失败的比例给出补事件：

<div class="reading-math">\[
\begin{aligned}
\widehat{\mathrm{pass@}k}
&=1-\frac{\binom{n-c}{k}}{\binom nk},\quad n\ge k\\
\Delta&=\mathrm{pass}_{\rm parent}
-\mathrm{pass}_{\rm child}
\end{aligned}
\]</div>

例如 n=4、c=1：pass@1=1/4，pass@2=1−3/6=1/2。依赖与配对按注册协议处理；**Δ&gt;0 仍需质量与归因支持**。headroom 筛选样本不能混进正式效果分母。[3](#ref-3)

## 规模与报告数字怎样阅读

原始 GEO-Harbor 方法报告保留 740 ready、413 done、70%+ / 91.0% 成功率以及成本估计，并已标明这些是原稿历史口径。它没有重新核验批次、分母、价格来源和全部执行证据，因此本页不将其更新为 2026-11-14 的生产读数。[1](#ref-1)

项目简历中“2,000+ task packages”对应作者提供的更大范围交付事实，也不能与本机 GEO 库存直接求比。若要报告当前库存，应从 task-record、campaign 状态和 tracked coordination inventory 重新聚合，分别给出来源、批次、完成、历史打包与本次新增。[5](#ref-5)

<!-- WORK:REVIEW:START -->
## 工作总结与质量验收的层次 {#work-review}

| 层次 | 应检查的产物 | 能支持的结论 |
| --- | --- | --- |
| 来源与输入 | accession、转换记录、冻结 fixture、schema | 数据可得、语义透明、可重放 |
| 科学合同 | instruction、多路径校准、known-wrong 与 verifier | 明确范围内合法结果可接受、错误可区分 |
| 独立盲测 | mount 白名单、冻结答案、Verifier 与 Judge 记录 | 指定运行协议中的求解与判分表现 |
| 生产交付 | lifecycle、task package、历史 inventory | 生命周期可恢复、交付不会重复计入 |
| 难度或训练效用 | 配对实验、失败归因、训练后留出评价 | 对相应假设的效果证据，不能由前四层替代 |

目前报告的方法价值集中在证据链、公共/私有边界、独立验证与防止伪难度的停止机制。要进一步证明任务改善了模型的科学能力，需要独立训练与留出评测；这不在本次整理的已执行范围内。

## 按需补充基础知识

可结合 [Harbor 框架完整介绍](../../harbor-framework-guide/)理解容器和 runner，再看 [可执行任务合成](../../agent-data-benchmarks/s01_task_synthesis.html)、[科学任务族](../../agent-data-benchmarks/s03_scientific_task_family.html)及[评测指标与基准](../../agent-data-benchmarks/s02_benchmark_map.html)。这些页面补通用知识，具体任务合同仍须查任务本身。
<!-- WORK:REVIEW:END -->

## 五道项目面试追问

1. **题面开放，如何确定性评分？** 冻结输入语义和输出合同，用实际合法路径、错误反例与 invariant 校准 scorer。
2. **参考解跑通为何不算盲测？** 作者看过答案；盲测须物理排除 solution/tests/authoring，只给公共资产。
3. **逐字段容差有什么漏洞？** 能接受跨路径混拼的联合结果；检查完整路径与联合约束。
4. **child 通过率下降就有效吗？** 先排规格、oracle、verifier 与基础设施缺陷；再用同条件配对结果确认科学瓶颈。
5. **413 done 能算 70% 成功率吗？** 库存与尝试分母不同；先固定批次、去重、资格与完成时间，不能直接除跨批次 ready 库存。

## 实现入口与复核范围

当前 GitHub 默认分支是 `Unified-produce`。先读 README 与 `docs/README.md`，再看 production 与 refinement 主说明；角色 prompt、gates、Solver/Verifier、lifecycle 和 packaging 的实现位于 `pipeline/`。旧环境分支和旧状态叙述只作历史背景，本页不修改本机生产配置。

本次使用 GitHub 固定版本报告、当前 refinement 主说明与仓库规则核验方法和结论边界，没有启动 task pipeline、盲测、清理或打包。完整原稿在[方法报告](full-report.html)中保留。

## 来源与固定版本

GitHub 固定到 `0efe0d276c6f4f2d804897843620ba7cb73974e7`，需要权限。

1. <a id="ref-1" href="https://github.com/stein-wang0226/harbor-task-sync/blob/0efe0d276c6f4f2d804897843620ba7cb73974e7/docs/GEO-Harbor-Bench-Method-Report.html">GEO-Harbor-Bench 方法报告</a>：原稿历史统计与 2026-11-05 文档说明。
2. <a id="ref-2" href="https://github.com/stein-wang0226/harbor-task-sync/blob/0efe0d276c6f4f2d804897843620ba7cb73974e7/README.md">当前 README</a>：来源、运行边界与入口。
3. <a id="ref-3" href="https://github.com/stein-wang0226/harbor-task-sync/blob/0efe0d276c6f4f2d804897843620ba7cb73974e7/docs/refinement-mvp-implementation.md">Refinement 主说明</a>：2026-11-12，验收、反事实、v3–v15 与停止边界。
4. <a id="ref-4" href="https://github.com/stein-wang0226/harbor-task-sync/blob/0efe0d276c6f4f2d804897843620ba7cb73974e7/docs/refinement-chain-design.md">版本与证据失效设计</a>及<a id="ref-4-history" href="https://github.com/stein-wang0226/harbor-task-sync/blob/0efe0d276c6f4f2d804897843620ba7cb73974e7/docs/refinement-v1-status.md">历史 refinement 记录</a>。
5. <a id="ref-5" href="https://github.com/stein-wang0226/harbor-task-sync/blob/0efe0d276c6f4f2d804897843620ba7cb73974e7/docs/production-status.md">生产记录与打包规则</a>。作者项目规模另参见站点[在线 CV](../../cv/#autoresearch)，两者统计范围分别保留。
