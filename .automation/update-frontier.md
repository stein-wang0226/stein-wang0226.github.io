# LLM Frontier 2026 — 每周自动更新协议

> 本文件是 QoderWork 每周定时任务（cron `0 9 * * 1`，Asia/Shanghai）所遵循的更新协议存档。
> 定时任务的 payload message 即下方「定时任务 Prompt」原文。手动更新也应遵循同一协议。

## 目标页面
`llm-frontier-2026.html`（仓库根目录）。主题分区锚点：
`#overview #models #frontier #arch #optimizer #agent #rl #opd #training #bench #protein #rumor #changelog #sources`

## 增量插入锚点
每个主题 section 顶部有 `<!-- AUTO:INSERT:<topic> -->` 注释（topic ∈ models/frontier/arch/optimizer/agent/rl/opd/training/bench/protein/changelog）。
**每周任务只在该锚点之后插入新的 `.update-entry` 块，绝不重写整页。**

## 条目块结构（统一 HTML）
```html
<div class="update-entry">
    <span class="entry-date">YYYY-MM-DD</span>
    <div class="card-title">标题<span class="pill fact">FACT</span></div>
    <p>正文：是什么 → 关键 insight → 代表工作/模型（带链接）→ 与前作差异。</p>
</div>
```
状态徽章四选一：`pill fact`（已核实）/ `pill rumor`（传闻）/ `pill self`（厂商自报）/ `pill preprint`（预印本）。

## 更新步骤（每次运行）
1. 读取 `llm-frontier-2026.html`，取 `#changelog` 最新一条 `entry-date` 作为「上次更新日」。
2. 只做**增量调研**：找上次更新日以来的新进展（官方 blog / arXiv / HF / 权威媒体）。
3. **组织级巡检（每次必做，优于固定仓库清单）**：对下方「已跟踪组织」逐个调 HF 组织 API `https://huggingface.co/api/models?author=<org>&sort=lastModified&direction=-1&limit=20`，列出该组织**全部**模型并按修改时间倒序——这样能自动发现清单外的新模型（如 GLM-5.3、MiniMax-M3、V4-Pro 正式版都是这样被发现的）。判定规则：任一仓库 `lastModified`/`createdAt` 晚于「上次更新日」，或页面尚无该模型 → 视为候选新进展。对命中的仓库再调 `api/models/<repo>?blobs=true` 看是否新增 `*Tech_Report*.pdf`/新权重/README 大改；技术报告 PDF 用 `/resolve/main/<file>` 下载（`/raw/` 对 LFS 只返回 ~132B 指针），`~/miniforge3/bin/python` + `pypdf` 抽首页/摘要核实参数、架构、许可、作者（团队署名以 PDF 首页为准）。
   - **礼貌与容错**：组织间 `sleep 2`，HF 返回非 JSON/429 时改用 `https://hf-mirror.com/api/...`；单个组织失败不阻断其余。GitHub 为**尽力而为**：优先 `gh api orgs/<org>/repos?sort=pushed`（本机若已登录），否则读 `https://github.com/<org>/<repo>/releases.atom`（免鉴权），再否则跳过——**GitHub 限流绝不使整轮失败**（未鉴权 api.github.com 仅 60 次/时且共享 IP 易 429）。
   - **闭源实验室**（OpenAI/Anthropic/Google DeepMind/xAI）无 HF 权重，改巡检官方 news/changelog 页 + 权威媒体（见「已跟踪组织」）。
4. 独立核实来源、附可点击链接；区分事实与传闻；厂商自报基准加 `pill self`。
5. 把新条目插入对应 section 的 `<!-- AUTO:INSERT -->` 锚点之后（新条目放最前）。
6. 更新 hero 的 `<span id="last-updated">` 为今天日期；在 `#changelog` 锚点后追加一条更新日志。
7. 更新前对 `llm-frontier-2026.html` 做时间戳备份（如 `.automation/backup/llm-frontier-2026.<ts>.html`）。
8. headless 渲染自检（`--dump-dom` 确认 section/div/table 配平、无异常）；异常则**不提交**并告警。
9. 若无实质新进展 → 跳过提交，仅记录「本周无实质更新」。
10. 提交：`git add llm-frontier-2026.html`（只 add 本文件），commit message `docs(frontier): weekly update YYYY-MM-DD`，push 到 `main`。
11. 将本次更新摘要（新增条目数 + 要点 3 条内）发送到指定 IM 会话通知。

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
> 对 LLM 前沿做每周增量调研并更新博客页。范围：开源模型（Kimi/Qwen/DeepSeek）、闭源前沿模型、新架构（loop transformer 等）、Muon 优化器、Agent、RL 算法（GRPO 家族）、OPD、训练策略、Benchmark（含 Terminal-Bench）、Protein LLM。
> 步骤：先读 /Users/stein/Desktop/算法面试-LLM学习/stein-wang0226.github.io/llm-frontier-2026.html 的 #changelog 最新日期作为上次更新日；只调研该日期之后的新进展，独立核实来源、附链接、区分事实与传闻（传闻标 pill rumor，厂商自报标 pill self）。**每次必巡检已跟踪开源模型的 HF 仓库**（见 .automation/update-frontier.md「已跟踪开源模型 HF 仓库」清单，含 Kimi-K3 / DeepSeek-V4.1-Flash / Qwen3-Next 等）：调 `api/models/<repo>?blobs=true` 看 lastModified 是否更新、是否新增 `*Tech_Report*.pdf` 或新权重，技术报告用 `/resolve/main/` 下载、pypdf 抽首页核实参数/架构/许可/作者。把新条目按统一 .update-entry 结构插入对应 section 的 <!-- AUTO:INSERT --> 锚点之后，更新 hero 的 #last-updated 与 #changelog。更新前先备份该 html 到 .automation/backup/。若本周无实质新进展则跳过提交。提交前做 headless 渲染自检，异常则不提交并告警。通过后 git add 仅该文件，commit「docs(frontier): weekly update <今天日期>」并 push 到 main。完成后将更新摘要（新增条目数+3条要点）发送到指定 IM 会话通知我。详细协议见仓库 .automation/update-frontier.md。
