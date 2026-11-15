# 博客讲解图示逐源审阅集成

权威逐源数据：`blog-diagram-review-20261115.json`。

日期：2026-11-15。基线：`d1bfb5b82776e1787510003e5dd6a87643cb1a22`。本记录为 T4 静态集成，不代表 T5/T6 完成。

仅审阅各页 examined 与 reason 明确记录的讲解/图示范围；reviewed 不等于所有科研事实或历史实验已经复现。

三模块记录的 examined、reason、改前/改后 SHA 和 diagrams 完整合入同名 JSON；历史 review 保持原样。
图数按作者 schema 与实际图示增删核对：旧图重新获得唯一 ID 不机械计为新图；LoRA 的 existing-split-merge-refinement 计为修图。

| 模块 | 唯一源 | 改稿 | 保留 | 新图 | 修图 |
| --- | ---: | ---: | ---: | ---: | ---: |
| architecture-inference | 18 | 6 | 12 | 6 | 4 |
| training-data | 29 | 6 | 23 | 6 | 1 |
| agent-multimodal-diffusion | 27 | 10 | 17 | 4 | 6 |
| 合计 | 74 | 22 | 52 | 16 | 11 |

## 共享样式

手机端同 specificity 的 chain 规则曾覆盖 options 的分支标记；compare 单列也显示串行箭头。
T5a 将 options/compare 的 `◇` 放在通用 chain 的 `↓` 之后；真正 chain 保持向下顺序箭头，非手机规则不变。
CSS 改前 SHA：`a66b39bb6699fc8852585888bed34cebcd81364ec7e9af20744db140ed5f2279`。
CSS 改后 SHA：`16c934726c459f5c2aa9986e4637c3e0a08bfa0a558954bb75060ad8e3b44602`。
`reading.css` 原无 receipt，本次新增精确凭据；不虚构历史 prior_reason。仅完成静态级联检查，三屏实际浏览器交独立验证。

## 静态证据

- 74 个 catalog 本地 ID/source 恰好覆盖一次，模块归属与 base_commit 匹配。
- 三模块记录的改前 SHA 等于指定 Git 基线字节，改后 SHA 等于当前源字节；changed 与实际 diff 一致。
- 实际正文 diff 恰为 22 源；16 新图和 11 修图与实际图示增删对应，标识唯一、caption 匹配。
- 三模块源级检查实际重新执行成功：原锚点、链接、公式、代码、科研资源和非图正文保留；选定教学算例静态复算通过。
- catalog 仅 22 个改稿源修改 summary/有依据日期；updated_source、review_status、关系与其他条目不变。
- 两份不可变基线 SHA 匹配；四份无关未跟踪 docs 保留并排除，archive 未修改。
- receipt refresh 的字段级与幂等性检查、拒绝非法覆盖测试见下方后续证据。

命令与逐页详细检查范围在同名 JSON 的 static_checks/pages；中间快照与证据位于 `/tmp/my-blogs-diagram-review-20261115/`。

## 凭据与拒绝测试

已实际执行 `python3 -B scripts/learning_review.py refresh`、`check` 及
`python3 -B /tmp/my-blogs-diagram-review-20261115/t4-verify-integration.py`，均通过。

- 改前/改后逐字段比较：仅 22 条 ledger 的 reason 追加图示补充，22 条 receipt 的 reason/SHA 更新。
- 其他字段/记录、现有 prior_reason、reading.css 精确凭据、历史 review 和历史 derive 结果保持不变。
- 合并后的 74 页记录与三模块输入逐字段一致，diagrams 仅新增已核对的 change_kind 分类。
- 11 个负例覆盖重复 ID/source、遗漏、source/module/base 不匹配、changed/SHA 不一致及陈旧 reason/共享 CSS/图示 SHA；全部拒绝，陈旧 refresh 不写凭据。
- 再次 refresh 后 ledger/receipt 的字节及 mtime 完全一致；`learning_review.py check`、`git diff --check` 通过。

字段明细与负例信息：`/tmp/my-blogs-diagram-review-20261115/t4-static-integration-checks.json`。
这些证据仍仅属于静态集成，不提升后续独立语义、构建或浏览器验收状态。

## 未执行

本轮 build、390/768/1440px browser、截图、无脚本真实交互、完整引用/迁移保留/流水线检查均尚未执行。
主 agent 已确认 27 张新/修图独立静态语义全部通过、浏览器准备 ready；这是独立交接状态，不冒充本代理的执行结果。
T4 已完成，可启动 T5/T6。三屏视觉与真实交互仍待验收；未运行模型、攻击、科学实验或历史结果复现。本轮不提交、不发布。

## T5 Source-Local Fix

2026-11-15 supplement; the T4 execution statements above retain their original scope.
The independent 1440px JS and noJS pixel observations for `agent-task-synthesis--data-admission-map`
found that auto-fit's 3+1 layout places Critic below CPT, with a downward marker implying CPT -> Critic.
This is a branch-clarity blocker, not clipping, geometry or noJS visibility.

One source-local rule now uses a hollow diamond (`content:"\25c7";font-size:16px`) for every
admission-route marker at all widths. The figure-ID suffix selector survives chapter namespacing
and outranks the shared mobile selectors. Auto-fit, prose, graph title, existing IDs, formulas,
links and all four independent admission contracts are unchanged. Shared `reading.css`, its
already-correct mobile options/compare rules, catalog summaries/dates and immutable baselines are untouched.

- Immediate before: 24,579 bytes, SHA `dbfc072680662adaaf2e0128b0c1b88559c34910e4f86e5f910bbb5379e9825a`.
- After: 24,709 bytes, SHA `6f40a994b7dbbf4c480797340a4eb6cd7ff53363bea1076aaeaecbe771793785`.
- Exact before bytes and receipt/review snapshots: `/tmp/my-blogs-diagram-review-20261115/t5-admission-before/`.
- Only this source's current SHA/reason, its module input SHA and corresponding ledger reason are updated.
- Current command evidence is separate: `/tmp/my-blogs-diagram-review-20261115/t5-admission-checks-result.json`
  and `t5-admission-scope-result.json`; the original `t6-result.json` remains historical.

No browser, semantic or pixel approval is performed by the fixer. Original failure reports,
screenshots and independent decisions remain intact. The independent verifier must recheck
390/768/1440px in JS and noJS on the current manifest/build, inspect the route markers and nearby
prose, and record new current-SHA decisions without overwriting the failed pixel evidence.
The affected physical page is `/agent-data-benchmarks/`; T5 acceptance remains pending.

## 完整覆盖

| ID | 唯一源 | 判断 | 检查锚点 | 新/修图 |
| --- | --- | --- | --- | --- |
| `llm-serving` | `content/series/llm-serving/index.html` | 保留 | `purpose`, `connections` | 0/0 |
| `serving-runtime` | `content/series/llm-serving/s01_runtime_scheduling.html` | 改稿 | `phases`, `paging`, `prefix`, `implementation`, `kimi-sparse-traffic` | 1/0 |
| `serving-parallel` | `content/series/llm-serving/s02_parallel_quantization.html` | 改稿 | `parallel`, `disaggregation`, `quantized-dot-example`, `speculative-trace` | 2/0 |
| `serving-capacity` | `content/series/llm-serving/s03_capacity_cost.html` | 保留 | `ledger`, `example`, `metrics`, `cost` | 0/0 |
| `llm-architecture` | `content/series/llm-architecture/index.html` | 保留 | `purpose`, `connections`, `sources` | 0/0 |
| `architecture-transformer` | `content/series/llm-architecture/s01_transformer_foundations.html` | 保留 | `tensor-flow`, `attention-mask`, `block`, `objective`, `state` | 0/0 |
| `architecture-attention` | `content/series/llm-architecture/s02_attention_position_cache.html` | 保留 | `head-sharing`, `kv-bytes`, `position`, `online-softmax-example`, `frontier-comparison` | 0/0 |
| `architecture-moe` | `content/series/llm-architecture/s03_ffn_moe_routing.html` | 保留 | `swiglu`, `routing`, `moe-full-example`, `latent`, `frontier-comparison` | 0/0 |
| `architecture-residual` | `content/series/llm-architecture/s04_residual_norm_stability.html` | 改稿 | `norm-position`, `rmsnorm`, `new-residual`, `frontier-comparison` | 0/1 |
| `architecture-hybrid` | `content/series/llm-architecture/s05_hybrid_architectures.html` | 改稿 | `purpose`, `gated-delta`, `hybrid`, `state-branch-example` | 0/2 |
| `architecture-comparison` | `content/series/llm-architecture/s06_model_comparison.html` | 保留 | `axes`, `co-design`, `mtp`, `experiments` | 0/0 |
| `research-base-architecture` | `content/series/llm-research-map-2026/s03_base_architecture.html` | 保留 | `ced`, `csa2`, `cache`, `engram` | 0/0 |
| `research-inference-diffusion` | `content/series/llm-research-map-2026/s04_inference_diffusion.html` | 改稿 | `budget`, `methods`, `exactness`, `opd`, `frontier-comparison` | 0/1 |
| `research-architecture-landscape` | `content/series/llm-research-map-2026/s06_architecture_landscape.html` | 保留 | `overview`, `state`, `qwen`, `kimi`, `glm`, `minimax`, `gemma`, `closed` | 0/0 |
| `research-architecture-training` | `content/series/llm-research-map-2026/s07_architecture_training.html` | 改稿 | `residual`, `latent-moe`, `muon`, `precision`, `depth` | 3/0 |
| `llm-frontier-2026` | `content/posts/llm-frontier-2026/index.html` | 保留 | `frontier-evidence-bridge`, `models`, `arch`, `optimizer`, `opd`, `bench` | 0/0 |
| `transformer-decoder-flow` | `content/posts/transformer-decoder-flow/index.html` | 保留 | `training-forward`, `numerical-forward`, `decode-forward`, `cache`, `code` | 0/0 |
| `llm-interview-bank` | `content/posts/llm-interview-bank/index.html` | 保留 | `sec-overview`, `sec-llm`, `sec-infra`, `code-attention`, `code-online`, `sec-frontier` | 0/0 |
| `my-work-protagent` | `content/posts/my-work-protagent/index.md` | 保留 | `#work-knowledge`, `#work-example`, `#work-review` | 0/0 |
| `my-work-harbor` | `content/posts/my-work-harbor/index.md` | 保留 | `#work-knowledge`, `#work-example`, `#work-review` | 0/0 |
| `my-work-protagent-full` | `content/posts/my-work-protagent/full-report.html` | 保留 | `#scope`, `#setting`, `#reward`, `#deep-dive` | 0/0 |
| `my-work-harbor-full` | `content/posts/my-work-harbor/full-report.html` | 改稿 | `#problem`, `#roles`, `#joint-path` | 1/0 |
| `llm-posttraining` | `content/series/llm-posttraining/index.html` | 保留 | `#overview`, `#read`, `#findings` | 0/0 |
| `posttraining-supervision` | `content/series/llm-posttraining/s01_supervision_preference.html` | 保留 | `#sft-objective`, `#recovery`, `#dpo-full-example`, `#rejection` | 0/0 |
| `posttraining-algorithms` | `content/series/llm-posttraining/s02_rl_algorithms.html` | 改稿 | `#ppo-gae`, `#gae-boundary-example`, `#grpo-full-example`, `#normalization` | 1/0 |
| `posttraining-opd` | `content/series/llm-posttraining/s03_opd_self_distillation.html` | 保留 | `#full-vocabulary`, `#sampled-gradient`, `#historical-teachers`, `#mopd2`, `#guided-intervention` | 0/0 |
| `posttraining-rewards` | `content/series/llm-posttraining/s04_environment_reward_credit.html` | 保留 | `#environment`, `#signal-types`, `#long-credit`, `#gar` | 0/0 |
| `posttraining-frameworks` | `content/series/llm-posttraining/s05_frameworks_async.html` | 改稿 | `#roles`, `#three-policy`, `#async-full-example`, `#partial-rollout` | 1/0 |
| `posttraining-cases` | `content/series/llm-posttraining/s06_task_cases_experiments.html` | 保留 | `#code-case`, `#science-case`, `#gui-case`, `#trajectory` | 0/0 |
| `training-methods-systems` | `content/series/llm-training-lifecycle/s05_training_methods_systems.html` | 改稿 | `#peft`, `#adamw-derivation`, `#muon-mechanism`, `#parallel`, `#state-sharding` | 1/1 |
| `scientific-task-family` | `content/series/agent-data-benchmarks/s03_scientific_task_family.html` | 保留 | `#provenance`, `#statistics`, `#verifier`, `#splits` | 0/0 |
| `cluster-training-evaluation` | `content/series/agent-data-benchmarks/s04_cluster_training_evaluation.html` | 保留 | `#design`, `#resources`, `#measurement`, `#failure` | 0/0 |
| `agent-data-benchmarks` | `content/series/agent-data-benchmarks/index.html` | 保留 | `#overview`, `#boundaries`, `#mastery` | 0/0 |
| `agent-task-synthesis` | `content/series/agent-data-benchmarks/s01_task_synthesis.html` | 改稿 | `#objects`, `#contract`, `#science`, `#admission` | 1/0 |
| `agent-benchmark-map` | `content/series/agent-data-benchmarks/s02_benchmark_map.html` | 保留 | `#map`, `#metrics`, `#terminal`, `#selection` | 0/0 |
| `research-agent-data` | `content/series/llm-research-map-2026/s01_agent_data_bench.html` | 改稿 | `#synthesis`, `#harbor`, `#parity`, `#audit` | 1/0 |
| `research-agentic-rl` | `content/series/llm-research-map-2026/s02_agentic_rl.html` | 保留 | `#map`, `#credit`, `#heterogeneity`, `#asynchrony` | 0/0 |
| `llm-training-lifecycle` | `content/series/llm-training-lifecycle/index.html` | 保留 | `#overview`, `#training-map`, `#artifacts` | 0/0 |
| `llm-training-pretraining` | `content/series/llm-training-lifecycle/s01_pretraining.html` | 保留 | `#packing-full-example`, `#compute-derivation`, `#scaling-ladder`, `#wsd-schedule` | 0/0 |
| `llm-training-midtraining` | `content/series/llm-training-lifecycle/s02_midtraining.html` | 保留 | `#recipe`, `#data`, `#mixture`, `#science-bridge` | 0/0 |
| `llm-training-sft-rft` | `content/series/llm-training-lifecycle/s03_sft_rft.html` | 保留 | `#sft`, `#quality`, `#rejection`, `#handoff` | 0/0 |
| `llm-training-rl-evaluation` | `content/series/llm-training-lifecycle/s04_rl_evaluation.html` | 保留 | `#loop`, `#reward`, `#systems`, `#protocol` | 0/0 |
| `agentic-rl-guide` | `content/posts/agentic-rl-guide/index.html` | 保留 | `#part3`, `#credit-example`, `#part5`, `#part7` | 0/0 |
| `rl-interview-guide` | `content/posts/rl-interview-guide/index.html` | 保留 | `#symbols`, `#pg-to-ppo`, `#faq`, `#classic-rl` | 0/0 |
| `distributed-training-guide` | `content/posts/distributed-training-guide/index.html` | 保留 | `#deepspeed`, `#fsdp`, `#megatron`, `#example` | 0/0 |
| `rl-interview-guide-legacy` | `content/archive/rl-interview-guide/index.html` | 保留 | `#symbols`, `#pg-to-ppo`, `#ppo-detail` | 0/0 |
| `harbor-framework-guide` | `content/posts/harbor-framework-guide/index.html` | 保留 | `#summary`, `#architecture`, `#verification`, `#trajectory` | 0/0 |
| `my-work-holon` | `content/posts/my-work-holon/index.md` | 保留 | `#work-knowledge`, `#work-example`, `#work-review` | 0/0 |
| `my-work-dllm` | `content/posts/my-work-dllm/index.md` | 保留 | `#work-knowledge`, `#work-example`, `#work-review` | 0/0 |
| `my-work-holon-full` | `content/posts/my-work-holon/full-report.html` | 保留 | `#chapter-1`, `#chapter-2`, `#holon-loss`, `#chapter-5`, `#chapter-6`, `#chapter-9`, `#chapter-12` | 0/0 |
| `my-work-dllm-full` | `content/posts/my-work-dllm/full-report.html` | 保留 | `#question`, `#algorithms`, `#theory`, `#structured`, `#framework`, `#audit` | 0/0 |
| `agent-systems` | `content/series/agent-systems/index.html` | 保留 | `#purpose`, `#case`, `#mastery` | 0/0 |
| `agent-rag` | `content/series/agent-systems/s01_rag_retrieval.html` | 改稿 | `#overview`, `#retrieval`, `#agentic`, `#evaluation` | 1/0 |
| `agent-planning` | `content/series/agent-systems/s02_planning_compute.html` | 保留 | `#strategies`, `#search`, `#environment`, `#budget` | 0/0 |
| `agent-trust` | `content/series/agent-systems/s03_trust_safety.html` | 改稿 | `#overview`, `#isolation`, `#science`, `#evaluating` | 0/1 |
| `llm-research-map-2026` | `content/series/llm-research-map-2026/index.html` | 保留 | `#overview`, `#priorities`, `#sources` | 0/0 |
| `research-agent-frontiers` | `content/series/llm-research-map-2026/s05_agent_frontiers.html` | 改稿 | `#scope`, `#gui`, `#science`, `#adaptation`, `#multiagent` | 1/0 |
| `dlm-survey` | `content/series/dlm-survey/index.html` | 改稿 | `#foundations`, `#mastery` | 0/1 |
| `agent-harness-guide` | `content/posts/agent-harness-guide/index.html` | 改稿 | `#codex-loop`, `#sandbox`, `#codex-compaction-paths`, `#codex-memory`, `#mapping` | 0/1 |
| `vlm-knowledge-interview` | `content/posts/vlm-knowledge-interview/index.html` | 改稿 | `#sec1`, `#clip-siglip`, `#sec1-2`, `#sec1-4`, `#sec1-5`, `#code2` | 1/0 |
| `dlm-ddpm` | `content/series/dlm-survey/s00a_ddpm.html` | 改稿 | `#model`, `#posterior`, `#sampling`, `#ddpm-full-example` | 0/1 |
| `dlm-flow-sde` | `content/series/dlm-survey/s00b_flow_sde.html` | 保留 | `#conditional-path`, `#flow-full-example`, `#probability-flow` | 0/0 |
| `dlm-overview` | `content/series/dlm-survey/s01_overview.html` | 改稿 | `#s1`, `#generation`, `#lineage` | 0/1 |
| `dlm-discrete` | `content/series/dlm-survey/s02_discrete.html` | 保留 | `#kernel`, `#weighted-mlm`, `#llada`, `#duality` | 0/0 |
| `dlm-block` | `content/series/dlm-survey/s03_block.html` | 保留 | `#factorization`, `#attention-mask`, `#cache`, `#cost-example` | 0/0 |
| `dlm-continuous` | `content/series/dlm-survey/s04_continuous.html` | 改稿 | `#interface`, `#flow`, `#rounding`, `#evaluation` | 0/1 |
| `dlm-paradigms` | `content/series/dlm-survey/s05_paradigms.html` | 改稿 | `#vp-conversion`, `#loss-weight`, `#score`, `#discrete-score` | 1/0 |
| `dlm-scaling` | `content/series/dlm-survey/s06_scaling.html` | 保留 | `#scaling-budget`, `#compute-optimal`, `#crossover` | 0/0 |
| `dlm-speculative` | `content/series/dlm-survey/s07_speculative.html` | 保留 | `#system-role`, `#acceptance`, `#cycle-cost`, `#methods` | 0/0 |
| `dlm-elbo-rl` | `content/series/dlm-survey/s08_elbo_rl.html` | 保留 | `#probability`, `#elbo-gap`, `#spg`, `#gdsd` | 0/0 |
| `dlm-commercial` | `content/series/dlm-survey/s09_commercial.html` | 保留 | `#evidence`, `#latency` | 0/0 |
| `dlm-comparison` | `content/series/dlm-survey/s10_comparison.html` | 保留 | `#comparison`, `#protocol`, `#research` | 0/0 |
| `dlm-loop-transformer` | `content/series/dlm-survey/s11_loop_transformer.html` | 保留 | `#recurrence`, `#gradient`, `#halting` | 0/0 |
| `dlm-vae` | `content/series/dlm-survey/s12_vae.html` | 保留 | `#elbo`, `#reparameterization`, `#vq`, `#system-role`, `#cvae-robot` | 0/0 |

## 图示登记

| 源 ID | 图 ID | 判断 | 主讲位置 | 图题 |
| --- | --- | --- | --- | --- |
| `serving-runtime` | `shared-kv-page-layout` | 新图 | `paging` | 两个请求、两张 block table、一份共享物理前缀 |
| `serving-parallel` | `serving-parallel-domains` | 新图 | `parallel` | 并行域按对象划分：TP、服务 DP、EP 不是三个串行阶段 |
| `serving-parallel` | `pd-state-handoff` | 新图 | `disaggregation` | PD 分离的跨服务边界：发送状态，不是只发送生成文本 |
| `architecture-residual` | `norm-bypass-map` | 修图 | `introductory figure immediately before purpose; explains norm-position` | 同一输入的两种残差布局：Norm 是否覆盖旁路 |
| `architecture-hybrid` | `hybrid-state-layout` | 修图 | `introductory figure immediately before purpose` | 混合模型的逐层状态：按本层类型读取，不是三步固定流水线 |
| `architecture-hybrid` | `state-fork-map` | 修图 | `agent-state / state-branch-example` | 从同一不可变快照分叉：A 的更新不能流入 B |
| `research-inference-diffusion` | `diffusion-drafter-options` | 修图 | `methods` | DFlash、DSpark、AdaFlash：三种方法对照，不是每轮依次执行 |
| `research-architecture-training` | `attnres-depth-read` | 新图 | `residual / Attention Residuals formula` | AttnRes：同一 token 的历史表示分成 key 与 value 两条路径 |
| `research-architecture-training` | `mhc-stream-layout` | 新图 | `residual / mHC formula` | mHC：旧流混合与模块写回是并行的数据依赖 |
| `research-architecture-training` | `recurrent-core-loop` | 新图 | `depth / recurrent-depth` | 递归深度：重复执行同一个 core，再做词表读出 |
| `my-work-harbor-full` | `joint-path-map` | 新图 | `#joint-path` | 完整路径接受域：允许 A 或 B，不允许逐字段拼接 A 与 B |
| `posttraining-algorithms` | `gae-boundary-map` | 新图 | `#gae-boundary-example` | GAE 的两道边界：下一 value 与下一优势分别接通 |
| `posttraining-frameworks` | `async-handoff-map` | 新图 | `#async-full-example` | 同一任务，两条版本线：采样历史延续，训练快照另行固定 |
| `training-methods-systems` | `lora-branch-map` | 修图 | `#peft` | LoRA：一条冻结路径和一条可训练增量相加 |
| `training-methods-systems` | `parallel-ownership-map` | 新图 | `#parallel` | 并行布局：谁持有什么，谁与谁交换什么 |
| `agent-task-synthesis` | `data-admission-map` | 新图 | `#admission` | 数据交接是按用途分流，不是把同一日志依次喂给四种训练 |
| `research-agent-data` | `artifact-handoff-map` | 新图 | `#harbor` | Separate verifier 的交接边界：传声明产物，不传整台运行环境 |
| `agent-rag` | `agent-retrieval-observation-map` | 新图 | `#agentic` | 模型生成查询动作，检索服务返回外部观察；两种 token 不混成策略输出 |
| `agent-trust` | `agent-trust-boundaries-map` | 修图 | `#isolation` | 数据通道影响模型判断；可信授权通道控制真实副作用 |
| `research-agent-frontiers` | `gui-observation-action-map` | 新图 | `#gui` | GUI 的闭环更新环境状态，不是把坐标输出直接当作任务成功 |
| `dlm-survey` | `dlm-training-generation-map` | 修图 | `#foundations` | 训练与生成是两条路径，共享去噪器；不是把训练输入接成生成先验 |
| `agent-harness-guide` | `codex-compaction-branches-map` | 修图 | `#codex-compaction-paths` | 按配置选择 A 或 B，再重建后续输入；不是先摘要、再执行无摘要换窗 |
| `vlm-knowledge-interview` | `vlm-fusion-paths-map` | 新图 | `#sec1-2` | 视觉表示与文本状态在哪里交互？三条接口支路，不是三个连续阶段 |
| `dlm-ddpm` | `ddpm-training-sampling-map` | 修图 | `#sampling` | 两条路径，共享可学习的噪声预测器；训练不接着运行反向采样 |
| `dlm-overview` | `ar-masked-state-map` | 修图 | `#generation` | 同一目标“我 喜欢 学习 数学”，两条独立的生成示意 |
| `dlm-continuous` | `continuous-text-interface-map` | 修图 | `#interface` | 真实表示提供训练端点；生成从噪声起步，不读取未知的真实文本 |
| `dlm-paradigms` | `vp-coordinate-map` | 新图 | `#vp-conversion` | 一次可学习预测，三条确定性坐标换算；不是依次训练三个模型 |

## T5/T6 实际验收（2026-11-15 最终补记）

本节汇总独立验收及修复后当前输入检查的实际报告；上文 T4、“未执行”及修复者声明均保留为当日阶段快照，不将其执行范围追溯扩大，也不声称本记录代理重跑了浏览器、像素审批或构建。

- 逐源范围：74 份唯一源，22 份改稿、52 份保留；16 张新图、11 张修图，共 27 张。保留与改稿判断仍以逐源 examined/reason 为界。
- T5 独立验收：390/768/1440px、JS/无 JS 共 60/60 浏览器用例通过，图示检查 162/162、独立像素检查 162/162、当前源独立语义判断 27/27 通过，最终问题列表为空。覆盖默认读图、邻近讲解、公式、旧链接及折叠阅读；无 JS 验可读与回退，不声称完成数学脚本排版。
- T6 本地检查：修复后同一输入的 7 项必需检查全部退出 0，涵盖构建/校验、学习凭据、组织、引用、迁移保留、流水线测试及输入快照；17/17 测试通过，产物为 107 个 HTML、303 个公开文件，基于上文提交且 `dirty=true`。依据为 `t5-admission-checks-result.json`，原 `t6-result.json` 仅作历史证据。

独立像素审阅曾在 1440px 的 JS/无 JS 下发现 `agent-task-synthesis--data-admission-map` 自动布局为 3+1，向下标记误示 CPT → Critic 串行依赖。源内局部规则改为全宽度空心菱形，保留共同输入与四条独立用途分支；修复后的三屏双模式观察及当前 SHA 的独立判断已通过。

随后邻接检查把不渲染的 `STYLE` 元数据误当隐藏讲解，产生六项失败；验收器仅排除紧邻的 `STYLE/SCRIPT/TEMPLATE` 元数据，真实正文、标题、关键图可见性与遮挡断言不变，未降低任何阈值。48 个隐藏正文负例及六项摘要控制通过。最终全量运行为 60 个缓存命中、0 个原始浏览器用例重跑；全部 162 条观察经当前键、源 SHA、几何及 PNG 字节一致性审计后复用，原观察时间与独立审批字节不变，不冒充新截图或新审批。

原分支失败、六项邻接失败报告、截图和原独立决定均保留，未用通过结果覆盖；包括 `reports/browser-before-admission-current-recheck.json`、`reports/browser-admission-current-full.json` 及 `adjacency-harness-before/`。

最终修复源 `content/series/agent-data-benchmarks/s01_task_synthesis.html` SHA-256：`6f40a994b7dbbf4c480797340a4eb6cd7ff53363bea1076aaeaecbe771793785`。
最终产品输入摘要：`47f7a6ea673ecc465e768fd348f7f77718c8a3f1541a29b5e3e4addfb93dea4b`。

证据根目录为 `/tmp/my-blogs-diagram-review-20261115/`；以下为本补记核对的报告字节 SHA-256，详细链条见报告，不重复展开：

| 证据报告 | SHA-256 |
| --- | --- |
| `reports/independent-summary.json` | `91bbef8ba492e14dab1e0cee12cdf5a61eabf23b79c0f980ee1b233415eec0e0` |
| `reports/t5-adjacency-gate-result.json` | `0e7de737e6b587e5b1419b0f4239306761644883d176afcc944065737eadbcc3` |
| `t5-admission-checks-result.json` | `89cbe1d64fde06252aab421e69d6f077709012cea26f92a4ad2be54dfc773cf9` |
| `reports/browser-adjacency-fixed-full.json` | `f364b341e09ca9e6a6b6c50c0265de77183980e1db76e74a26d617cdb731154a` |
| `reports/t5-adjacency-rekey-provenance.json` | `f30891231e09c3faeedb66d16e07f478c6e2132efb30eac899cd0aeefba90637` |

当前结论仅为 T5 独立本地门禁通过、T6 本地必需检查通过；独立摘要的 `t6Complete=false`、`t5TaskMarkedComplete=false` 原样保留，不据此关闭规格任务。发布仍待 Actions 部署、线上 `build-info.json` 输入指纹及实际正文/图示核验。本补记不提交、不发布；语义验收仅涉及记录范围内的对象、边、假设及当前产物阅读，不表示科学实验、模型性能或历史结果已复现。
