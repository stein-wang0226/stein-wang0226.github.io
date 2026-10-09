# LLM Frontier 2026 — Codex 每 3 天更新与事实巡检协议

> 本文件是由 Codex 执行的本机定时任务（每 3 天一次，Asia/Shanghai 09:00）所遵循的更新协议存档。
> 定时任务的 payload message 即下方「定时任务 Prompt」原文。手动更新也应遵循同一协议。

## 目标页面
`llm-frontier-2026.html`（仓库根目录）。主题分区锚点：
`#overview #models #frontier #arch #optimizer #agent #rl #opd #training #bench #protein #rumor #changelog #sources`

## 增量插入锚点
每个主题 section 顶部有 `<!-- AUTO:INSERT:<topic> -->` 注释（topic ∈ models/frontier/arch/optimizer/agent/rl/opd/training/bench/protein/changelog）。
**定时任务只在该锚点之后插入新的 `.update-entry` 块，绝不重写整页。**

## 条目块结构（统一 HTML）
```html
<div class="update-entry">
    <time class="entry-date" datetime="YYYY-MM-DD">YYYY-MM-DD</time>
    <div class="card-title">标题<span class="pill fact">FACT</span></div>
    <p>正文：是什么 → 关键 insight → 代表工作/模型（带链接）→ 与前作差异。</p>
</div>
```
状态徽章四选一：`pill fact`（已核实）/ `pill rumor`（传闻）/ `pill self`（厂商自报）/ `pill preprint`（预印本）。

## 更新步骤（每次运行）
1. 在仓库根目录执行 `git status --porcelain` 与 `git pull --ff-only origin main`。若存在无关未提交修改，或快进失败，则不修改、不提交，只报告准确阻塞点。
2. 读取 `llm-frontier-2026.html`，取 `#changelog` 最新一条 `entry-date` 作为「上次成功更新日」；以 canonical URL 和条目标题去重，避免同一消息重复入页。
3. 先做**事实巡检**，再做增量调研：每轮复核所有待发布的新条目，以及一个轮换主题 section 的既有高风险断言（模型发布日期、参数/上下文、许可、基准排名或性能、论文/版本号）。对同一断言优先比对一手来源；无法确认的说法降为 `RUMOR` 或 `SELF-REPORT`，来源失效、与一手来源冲突或无法合理修正的内容删除。每次也检查 `#rumor` 是否已有可转为 `FACT` 的条目。不得因“网页原有内容”而跳过复核。
4. 只做**增量调研**：找上次成功更新日以来的新进展（官方 blog / arXiv / HF / 权威媒体）。实质增量限于正式模型/版本、技术报告、权重/许可/可用性、架构或能力发生重大变化；仅下载量、元数据或 README 微调不入页。
5. **组织级巡检（每次必做，优于固定仓库清单）**：对下方「已跟踪组织」逐个调 HF 组织 API `https://huggingface.co/api/models?author=<org>&sort=lastModified&direction=-1&limit=20`，检查最近 20 个候选模型并按修改时间倒序；需要完整历史时分页拉取。判定规则：任一仓库 `lastModified`/`createdAt` 晚于「上次成功更新日」，或官方来源确认了一个尚未收录的新版本，才视为候选新进展。对命中的仓库再调 `api/models/<repo>?blobs=true` 看是否新增 `*Tech_Report*.pdf`/新权重/README 大改；技术报告 PDF 用 `/resolve/main/<file>` 下载（`/raw/` 对 LFS 只返回 ~132B 指针），优先用 `python3` + `pypdf` 抽首页/摘要核实参数、架构、许可、作者（团队署名以 PDF 首页为准）。本机缺少 `python3` 或 `pypdf` 时，跳过 PDF 抽取并在报告中说明，不阻断其余核验。
   - **礼貌与容错**：组织间 `sleep 2`，HF 返回非 JSON/429 时改用 `https://hf-mirror.com/api/...`；单个组织失败不阻断其余。GitHub 为**尽力而为**：优先 `gh api orgs/<org>/repos?sort=pushed`（本机若已登录），否则读 `https://github.com/<org>/<repo>/releases.atom`（免鉴权），再否则跳过——**GitHub 限流绝不使整轮失败**（未鉴权 api.github.com 仅 60 次/时且共享 IP 易 429）。
   - **闭源实验室**（OpenAI/Anthropic/Google DeepMind/xAI）无 HF 权重，改巡检官方 news/changelog 页 + 权威媒体（见「已跟踪组织」）。
6. 独立核实来源、附可点击的 `https` 链接；区分事实与传闻。发布事件可标 `FACT`，但每个厂商比较或性能数字必须紧邻 `SELF-REPORT`，不能被标题的 `FACT` 覆盖。动态文本必须做 HTML 转义。
7. 把新条目插入对应 section 的 `<!-- AUTO:INSERT -->` 锚点之后（新条目放最前）。每条必须保留局部来源；`#sources` 是去重后的精选入口，只有稳定且不重复的一手来源才更新。
8. 有新增或事实修正时，更新 hero 的 `<time id="last-updated">` 为今天日期；在 `#changelog` 锚点后追加一条更新日志，明确列出修正/降级/删除的断言及理由。
9. 更新前对 `llm-frontier-2026.html` 做时间戳备份（如 `.automation/backup/llm-frontier-2026.<ts>.html`，该目录已忽略）。
10. 用支持 HTML5 的校验器做结构检查；macOS 自带的旧版 `tidy` 会把 `header`、`main`、`time` 等合法 HTML5 元素误报为错误，不得作为唯一硬门槛。随后以 headless Chromium/Chrome 渲染页面，检查所有目录锚点、`#last-updated`、更新条目与主要 section 均存在且无页面级异常。浏览器工具缺失时可降级为结构/锚点检查并在报告说明；真实结构检查失败则**不提交**。
11. 若无实质新进展且事实巡检没有产生修正 → 跳过提交，仅记录「本轮无实质更新」。
12. 提交：`git add llm-frontier-2026.html`（只 add 本文件），commit message `docs(frontier): update YYYY-MM-DD`，push 到 `main`。
13. 在 scheduled run 的结果中报告：轮换复核的主题、核验/修正/删除数量、新增条目数、最多 3 条要点、提交 SHA 与阻塞项；只有明确配置并授权了目标会话时，才发送 IM。

## 已跟踪组织（组织级巡检：HF org + GitHub org + 官方 news）
**开源权重实验室**（HF `api/models?author=<org>` + GitHub org releases）：
| 实验室 | HF org | GitHub org | 备注 |
| --- | --- | --- | --- |
| DeepSeek | `deepseek-ai` | `deepseek-ai` | V3.2 / V4-Pro / V4-Flash / V4.1-Flash 及 DSpark/Vision 变体 |
| Moonshot Kimi | `moonshotai` | `MoonshotAI` | K2.x / K2.7-Code / K3 及后续 |
| Qwen（阿里） | `Qwen` | `QwenLM` | Qwen3.x-Max / -Next / -Flash / Qwen-VL / Qwen-Drive |
| GLM（智谱 Z.ai） | `zai-org`（旧 `THUDM`） | `THUDM` / `zai-org` | GLM-5 / 5.2 / 5.3 / -Flash |
| MiniMax | `MiniMaxAI` | `MiniMax-AI` | M2 / M2.x / M3 / H3 / Music（M3 已正式发布，勿再当传闻） |
| Meta | `meta-llama` | `meta-llama` | Llama 4 系列及后继 |
| Mistral | `mistralai` | `mistralai` | 欧洲开源前沿 |
| Protein | `biohub` / `facebook`(ESM) / `Evo`(Arc) | `google-deepmind/alphafold3` | ESMC / ESM-3 / Evo 2 / AF3（对应 Holon/ProtAgent） |

**闭源前沿实验室**（无 HF 权重，巡检官方 news/changelog + 权威媒体）：
- OpenAI（GPT-6 系列）：`openai.com/news` · `platform.openai.com/docs/changelog`
- Anthropic（Claude Opus/Sonnet/Fable/Mythos）：`anthropic.com/news`
- Google DeepMind（Gemini）：`deepmind.google/models` · `blog.google/technology/ai`
- xAI（Grok）：`x.ai/news`

> 巡检要点：组织内**任一**模型 `lastModified`/`createdAt` 晚于上次更新日，或页面尚未收录该模型 → 视为实质进展，核实后补 `.update-entry` + 对照表行 + `#sources` 链接。发现清单外的重要新组织/模型时，顺手补进本表。厂商自报基准一律加 `pill self`，未经独立复现的对比数字注明出处。

## 安全护栏
- 只增量插入，不重写整页；不触碰仓库内其它无关文件。
- 不引用本地偏见目录（蚂蚁/AReaL/AWorld/Awex/AntAngelMed/Ling-1T 等）作为唯一来源；相关话题须独立 web 核实。
- 不把 WebSearch snippet 的「教授名+论文名」当作者证据；论文作者以 arXiv abs 全列表为准。
- push 前必须渲染自检通过。

## 定时任务 Prompt（payload.message 原文）
> 由 Codex 对 LLM 前沿做每 3 天一次的增量调研、事实巡检并更新博客页。范围：开源模型（Kimi/Qwen/DeepSeek）、闭源前沿模型、新架构（loop transformer 等）、Muon 优化器、Agent、RL 算法（GRPO 家族）、OPD、训练策略、Benchmark（含 Terminal-Bench）、Protein LLM。
> 步骤：先以 `repo_root=$(git rev-parse --show-toplevel)` 定位仓库根目录，读取 `$repo_root/llm-frontier-2026.html` 的 #changelog 最新日期作为上次成功更新日；开始前确认工作树无无关修改并 `git pull --ff-only origin main`。每轮先核验所有待发布的新条目，并轮换复核一个既有主题 section 的高风险事实（日期、参数、上下文、许可、基准、论文/版本号）；与一手来源冲突或无法确认的断言必须改正、降为 pill rumor / pill self，或删除，并在 changelog 记录。之后只调研此后有实质信息增量的进展，独立核实来源、附 `https` 链接、区分事实与传闻（传闻标 pill rumor，厂商比较/基准标 pill self）。**每次必做已跟踪组织的 HF 组织级巡检**（见 `.automation/update-frontier.md` 的「已跟踪组织」表）：检查最近候选模型的更新时间、权重与技术报告，必要时用 `/resolve/main/` 下载报告并以 `python3` + pypdf 核实参数/架构/许可/作者；工具缺失或单个源不可用时降级并报告，不阻断其余核验。把新条目按统一 `.update-entry` 结构插入对应 section 的 `<!-- AUTO:INSERT -->` 锚点之后；有新增或事实修正时更新 hero 的 #last-updated 与 #changelog，并先备份到 `.automation/backup/`。若本轮无实质新进展且无事实修正，则不改文件、不提交。提交前用 HTML5 兼容的校验器或等价检查验证结构（不把 macOS 旧版 tidy 的 HTML4 误报当作失败），再做可用的 headless 浏览器渲染与目录锚点检查；真实异常则不提交。通过后只暂存 `llm-frontier-2026.html`，提交 `docs(frontier): update <今天日期>` 并 push 到 main。完成后在 scheduled run 结果中报告轮换复核主题、核验/修正/删除数量、新增条目数、三条以内要点、提交 SHA 与任何阻塞项；不要发送 IM，除非任务环境已有明确授权和配置。详细协议见仓库 `.automation/update-frontier.md`。
