# Codex Harness 源码实例：依据与验收

核对日期：2026-11-14。目标：补充 `agent-harness-guide.html` 中的实际 Agent 案例，重点说明上下文管理与 memory，按用户要求以 Codex 开源实现为主，社区文章仅作参考。

正文源：`content/posts/agent-harness-guide/index.html`。新增三节：`#codex-loop`、`#codex-context`、`#codex-memory`。阅读准备和页内目录提供直接入口；两张响应式 SVG、一个短 Rust 节选、折叠细节与贯穿示例支持分层阅读。

## 证据版本与范围

- 主要证据：[openai/codex](https://github.com/openai/codex/tree/c2c1ebba0a7985ebee065c5492233a843b84c4c6)，完整提交 `c2c1ebba0a7985ebee065c5492233a843b84c4c6`，提交时间 2026-11-14T02:55:41Z。通过 GitHub CLI 获取元数据和源码归档，解包到 `/tmp/my-blogs-codex-harness-20261114` 后静态阅读。
- 正文的源码链接固定到此提交，避免主分支变化后行号与结论漂移。短 Rust 节选注明 OpenAI、原文件和 Apache-2.0 许可。
- 官方产品文档：[Codex as a platform](https://developers.openai.com/blog/codex-as-a-platform)、[Memories](https://developers.openai.com/codex/memories)、[配置参考](https://developers.openai.com/codex/config-reference)。
- 用户参考：[53AI 文章](https://www.53ai.com/news/OpenSourceLLM/2026102790874.html)、[learn-harness-engineering Codex 章节](https://github.com/walkinglabs/learn-harness-engineering/blob/a9342ff471f2c0e60be0c08b9f4a7c502df4e442/docs/zh/harness-designs/codex/index.md)。后者固定到 `a9342ff471f2c0e60be0c08b9f4a7c502df4e442`；其概括与路径不优先于本次源码。
- 这是源码静态分析与博客集成，没有编译 Codex、调用它的托管 history/notes 服务或测量 Agent 性能。示例与对照实验均明确标为说明或待执行。

## 核心结论对应的源文件

以下路径均相对固定提交的仓库根目录，正文包含可点击的不可变引用。

| 结论 | 实现依据 | 解释边界 |
|---|---|---|
| Harness 覆盖运行循环、上下文、工具与恢复；训练可再接 Reward / 更新 | `codex-rs/core/src/session/turn.rs:217–805` | 修正原文把 Harness 限定为训练基础设施的定义；不把 Codex 当作 RL trainer |
| 工具输出与后续采样形成持续循环 | `core/src/session/turn.rs:650–805`、`core/src/tools/router.rs:267–435`（以上 core 路径前缀均为 `codex-rs/`） | 图解省略 hooks、重试、子 Agent；有 follow-up 或待处理输入才继续 |
| live history 可截断而完整 payload 保存在 rollout | `codex-rs/core/src/context_manager/history.rs:628–640` | 当前模型输入与原始事件是两种视图；不是保证任何 provider 的远程历史都逐字原样暴露 |
| 调用/输出需配对，孤立输出及不支持媒体需清理 | 同文件 `1185–1202` | 结构约束是源码事实 |
| AGENTS.md 从项目根到 cwd 发现，在字节预算内组合 | `codex-rs/core/src/agents_md.rs:126–274` | 未变化不重复发送；变化发替换提示与新的完整文本，见 `core/src/context/world_state/agents_md.rs:44–79` |
| 默认阈值按已解析窗口的 90% 计算并受配置上限约束 | `codex-rs/protocol/src/openai_models.rs:579–591` | 实际触发还由 `core/src/session/context_window.rs` 的范围、预留与硬上限决定；不是固定 80% |
| 自动 compaction 存在摘要与 token-budget 分支 | `codex-rs/core/src/session/turn.rs:1687–1744` | 本地摘要 prompt 位于 `codex-rs/prompts/templates/compact/prompt.md`；远程 compaction 服务实现不在仓库 |
| token-budget 分支跳过摘要，重新装配窗口 | `codex-rs/core/src/compact_token_budget.rs:55–61`、`core/src/session/mod.rs:5459–5508` | full world state + retained client items，空 compact message 不是空输入；文件与环境不清空 |
| feature 表的 token_budget 为开发中、默认关闭 | `codex-rs/features/src/lib.rs:2265–2275` | 模型默认值与符合条件的实验配置可启用，见 `core/src/session/token_budget.rs:22–55,134–173` |
| history/notes 是有启用条件的托管客户端扩展 | `codex-rs/ext/history-notes/src/extension.rs:31–140`、`tools.rs:87–100` | OpenAI provider、Codex backend 认证与配置门控；服务端检索/生成实现不可推断 |
| thread_hint 最大 4,000 UTF-8 bytes | 同 `extension.rs` | 不是 4,000 tokens；默认 developer 窗口元数据另可配置为工具输出，见 `core/src/context/token_budget_context.rs:33–107` |
| history 支持按窗口/条目有界读取与字面子串搜索，notes 使用虚拟路径 | `codex-rs/ext/history-notes/src/requests.rs:1–238` | history 最终一致；notes 写后直接读取立即可见，列表/搜索最终一致；写工具注册为非并行 |
| memory 在合格根会话启动后的后台提炼与整理 | `codex-rs/memories/write/src/start.rs:20–102`、`phase1.rs:48–90`、`phase1_output.rs:33–55` | 需 feature、非 ephemeral、DB 和配额；旧 rollout 的资格筛选决定实际输入 |
| DB 按保留窗口、usage_count 与近期性选择 Phase 2 的 Top-N 输入 | `codex-rs/state/src/runtime/memories.rs:445–500` | 不是 query embedding 检索，也不是指数/连续权重衰减 |
| Phase 2 用 workspace diff 判断是否需重新整理 | `codex-rs/memories/write/src/phase2.rs:53–184` | 输入已同步且产物有效、没有变化时跳过 consolidation agent |
| V1 提炼 raw memory + summary，V2 只提炼 summary/slug | `codex-rs/memories/write/src/phase1_output.rs` | V2 summary 上限 9,000 UTF-8 bytes；V2 consolidation 模板要求完整摘要低于 10,000 bytes |
| V1 手册/skills 与 V2 摘要/来源指针不同 | `codex-rs/memories/write/templates/memories/consolidation.md`、`consolidation_v2.md` | 模板描述整理行为，不能把旧版所有文件产物推广到 V2 |
| 新会话读取短摘要并装入版本相应的 developer 模板 | `codex-rs/ext/memories/src/prompts.rs:31–63`、`templates/memories/read_path_v2.md` | 后续来源读取按任务需要；历史经验不能证明当前仓库状态 |
| memories feature stable 但默认关闭；符合条件的新 profile 选 V2 | `codex-rs/features/src/lib.rs:1460–1464`、`core/src/config/mod.rs:3754–3767` | 保留显式选择和过渡退出配置，不保证每个已安装 Codex 都启用 |

## 内容保留与维护边界

- 修改前正文 SHA-256：`d709280e4c89a3aa1252c9d0f72f80e706850b0c7d0b57e07f5bc2a26fef759e`；原文另存 `/tmp/my-blogs-harness-before-20261114.html` 用于本次比较。
- 保留既有公开 URL、16 个原章节锚点、原训练公式与代码、ProtAgent 和课程案例。改动限于定义、导读、目录、新增三节、参考资源与日期说明。
- 原四层架构与五大组件明确标为训练侧的一种设计；保留原模型/工具类比所用的概念，但修正 Framework 与 Harness 必然互斥或严格上下游的说法。
- 原 ProtAgent 性能数字、训练算法叙述及历史框架比较没有在本次源码任务中全面复核。目录登记保持 `needs-review`，不能把新增 Codex 部分的核对描述为整篇文章已审定。
- `content/catalog.json` 只修改对应文章的摘要、标签、复核状态与内容日期。`docs/content-changes.json` 只更新该正文的精确 SHA 与理由；其他同时进行的 benchmark / CV / 构建器修改保留。
- 以上为本地实现阶段记录，该阶段完成时尚未提交、推送或发布。2026-11-14 用户明确要求完成博客后推送；后续线上状态以对应提交的 GitHub Actions 与 `build-info.json` 为准。

## 本次验收

1. `make check OUTPUT=/tmp/my-blogs-harness-build`：通过，68 个 HTML 页面、109 个公开文件；登记、链接、锚点、导航和资源清单有效。初次构建发现校验器把内嵌 SVG 的 `title` 也计入页面标题；图解改用 `aria-label` 与 `desc` 保留可访问描述后通过，未改构建器。
2. `python3 docs/verify-content-migration.py --require-clean`：最终校验通过，23 项原始 SHA 一致、18 项已有或本次有意变化已登记，299 个原始锚点和 59 个原始标记保留。该结果是内容保留证据，不是整站科研事实审定。
3. 本次专项比较脚本 `/tmp/my-blogs-harness-integrity.py`：通过，17 个修改前正文锚点全部保留、15 段原有 pre 代码/公式原样保留、13 个原章节全文不变；36 个不同的固定提交源码链接文件和行号有效；Rust 节选与原文 5478–5487 行一致，仅移除共同缩进。
4. Chromium 交互脚本 `/tmp/my-blogs-browser-tests/harness-check.js`：通过，6 项布局检查（文章与博客入口 × 390/768/1440px）、21 项交互检查、3 项无 JavaScript 阅读检查；无 pageerror。覆盖导读跳转、细节展开/收起、键盘、Codex / Memory / Context Management 搜索、搜索结果打开正文；两张 SVG 保持原始比例，无页面水平溢出。
5. Browser MCP 实际操作确认：搜索 Codex 得到该文章，点击结果打开原 URL，导读跳到上下文节，折叠内容展开后源码可见。桥接点击在平滑滚动未结束时一次命中失败，重新读取当前节点状态后重试成功。
6. 像素核对：查看 `/tmp/my-blogs-browser-tests/harness-loop-1440.png` 与 `harness-memory-390.png`，桌面流程完整、手机图解无裁切；宽比较表在独立容器内横向滚动。详细浏览器记录在同目录 `harness-report.json`。

正文最终 SHA-256：`fd66776824735c00f1ca184ea092d5f67bad877159be4643e62b72e8a51e388e`。构建基于主站提交 `784f449a51e1158377e3ccb9b282fbbfa5b3614b`，`dirty=true`；`input_digest=430dfab8b1ac86588467760ef3aee7f366b500a530d7cd8bec018fd9ea89971b`。产物包含当前工作区已有的并行 benchmark 等修改，不能把上述所有页面都计为本任务新建。

本地验收预览：[Codex 实例](http://127.0.0.1:8772/agent-harness-guide.html#codex-loop)，产物目录 `/tmp/my-blogs-harness-build`。没有运行 Codex 性能对照。发布前再次执行 `make check OUTPUT=/tmp/my-blogs-harness-publish-build`，68 页与 109 个公开文件检查通过；主站分支 `main` 与 `origin/main` 同步后准备提交本次四个文件。

公开入口：[Codex 源码实例](https://stein-wang0226.github.io/agent-harness-guide.html#codex-loop)。该链接在对应提交部署完成后包含本次内容，地址本身不能代替部署结果核验。
