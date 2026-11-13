# LLM Frontier 2026 — Codex 每 3 天更新与事实巡检协议

> 本文件是由 Codex 执行的本机定时任务（每 3 天一次，Asia/Shanghai 09:00）所遵循的更新协议存档。
> 手动更新也应遵循同一协议。更新器只编辑正文，运行器负责工作树护栏、备份、构建检查及显式授权后的 Git 操作。
> `run-frontier-update.sh` 默认仅本地准备；只有用户明确授权提交和推送后，才使用 `--publish`。本次规格实施不启动定时任务、不提交、不推送。

## 目标页面
唯一正文源：`content/posts/llm-frontier-2026/index.html`。
公开 URL 仍为 `/llm-frontier-2026.html`；根目录旧 HTML 不再是可编辑的第二份源。
主题分区锚点：
`#overview #models #frontier #arch #optimizer #agent #rl #opd #training #bench #protein #rumor #changelog #sources`

## 运行边界与构建接口
- 运行器调用更新器前，拒绝所有已暂存、未暂存和未跟踪修改，包括前沿正文尚未提交的人工修改；须由维护者先处理，不自动 stash、reset、覆盖或提交。
- 更新器使用 `workspace-write` 沙箱，不执行 `pull/add/commit/push` 或部署，不改登记表、生成页、协议、工具及其他内容。运行器在更新后和构建后再次检查工作树，只允许权威正文的未暂存修改。
- `FRONTIER_VALIDATOR` 指向一个可执行适配器；运行器传入两个独立参数：仓库绝对路径、相对正文路径。适配器须使用 T2 确认的统一构建/检查入口，在仓库外生成同一公开产物，检查正文、公开文章及博客目录日期一致；失败返回非零，不能回写正文或其他仓库文件。未配置时默认查找 `.automation/validate-frontier.sh`，不存在即阻塞。T2 接口未提供前，不臆造构建命令。
- `FRONTIER_UPDATER` / `FRONTIER_PYTHON` 可指定可执行更新器与 Python；默认沿用本机 Codex 路径与 `python3`。隔离测试使用模拟工具，不调用真实 Codex、远端或定时服务。
- 更新器报告第一行必须为 `FRONTIER_RESULT: UPDATED`、`FRONTIER_RESULT: NO_CHANGE` 或 `FRONTIER_RESULT: BLOCKED`。退出成功却缺少该标记、状态与文件变化不符或检查失败，均按阻塞处理。
- `.automation/state/last-result.md` 保存结果；`run.lock` 阻止并发运行。异常中断的遗留锁须人工确认后移除。保留 `last-successful-scheduled-run` 的 72 小时间隔；仅无实质变化的成功巡检或成功推送才更新它，本地准备及失败不更新。
- `.automation/backup/llm-frontier-2026.<UTC 时间戳>.<pid>.html` 在更新器启动前保存正文。失败后保留备份和现场供人工审阅，不自动恢复以免覆盖并发人工修改。备份、状态、日志和缓存不得进入公开产物。

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
1. 运行器先检查工作树与暂存区；有任意未提交修改即报告阻塞，不调用更新器。仅显式获准的 `--publish` 模式，在干净的 `main` 上执行 `git pull --ff-only origin main` 并重新检查工作树；快进失败即停止。本地准备模式不执行远端操作。
2. 读取 `content/posts/llm-frontier-2026/index.html`，取 `#changelog` 最新一条有效 `entry-date` 作为「上次成功更新日」；它必须与 `<time id="last-updated" datetime="YYYY-MM-DD">` 的日期及可见文本一致。以 canonical URL 和条目标题去重，避免同一消息重复入页。博客登记表不另写更新时间，由构建读取正文的有效 `last-updated`；不能使用运行时间或提交时间代替内容日期。
3. 先做**事实巡检**，再做增量调研：每轮复核所有待发布的新条目，以及一个轮换主题 section 的既有高风险断言（模型发布日期、参数/上下文、许可、基准排名或性能、论文/版本号）。对同一断言优先比对一手来源；无法确认的说法降为 `RUMOR` 或 `SELF-REPORT`，来源失效、与一手来源冲突或无法合理修正的内容删除。每次也检查 `#rumor` 是否已有可转为 `FACT` 的条目。不得因“网页原有内容”而跳过复核。
4. 只做**增量调研**：找上次成功更新日以来的新进展（官方 blog / arXiv / HF / 权威媒体）。实质增量限于正式模型/版本、技术报告、权重/许可/可用性、架构或能力发生重大变化；仅下载量、元数据或 README 微调不入页。
5. **组织级巡检（每次必做，优于固定仓库清单）**：对下方「已跟踪组织」逐个调 HF 组织 API `https://huggingface.co/api/models?author=<org>&sort=lastModified&direction=-1&limit=20`，检查最近 20 个候选模型并按修改时间倒序；需要完整历史时分页拉取。判定规则：任一仓库 `lastModified`/`createdAt` 晚于「上次成功更新日」，或官方来源确认了一个尚未收录的新版本，才视为候选新进展。对命中的仓库再调 `api/models/<repo>?blobs=true` 看是否新增 `*Tech_Report*.pdf`/新权重/README 大改；技术报告 PDF 用 `/resolve/main/<file>` 下载（`/raw/` 对 LFS 只返回 ~132B 指针），优先用 `python3` + `pypdf` 抽首页/摘要核实参数、架构、许可、作者（团队署名以 PDF 首页为准）。本机缺少 `python3` 或 `pypdf` 时，跳过 PDF 抽取并在报告中说明，不阻断其余核验。
   - **礼貌与容错**：组织间 `sleep 2`，HF 返回非 JSON/429 时改用 `https://hf-mirror.com/api/...`；单个组织失败不阻断其余。GitHub 为**尽力而为**：优先 `gh api orgs/<org>/repos?sort=pushed`（本机若已登录），否则读 `https://github.com/<org>/<repo>/releases.atom`（免鉴权），再否则跳过——**GitHub 限流绝不使整轮失败**（未鉴权 api.github.com 仅 60 次/时且共享 IP 易 429）。
   - **闭源实验室**（OpenAI/Anthropic/Google DeepMind/xAI）无 HF 权重，改巡检官方 news/changelog 页 + 权威媒体（见「已跟踪组织」）。
6. 独立核实来源、附可点击的 `https` 链接；区分事实与传闻。发布事件可标 `FACT`，但每个厂商比较或性能数字必须紧邻 `SELF-REPORT`，不能被标题的 `FACT` 覆盖。动态文本必须做 HTML 转义。
7. 把新条目插入对应 section 的 `<!-- AUTO:INSERT -->` 锚点之后（新条目放最前）。每条必须保留局部来源；`#sources` 是去重后的精选入口，只有稳定且不重复的一手来源才更新。
8. 有新增或事实修正时，更新 hero 的 `<time id="last-updated">` 为今天日期；在 `#changelog` 锚点后追加一条更新日志，明确列出修正/降级/删除的断言及理由。
9. 运行器在更新前对权威正文做时间戳备份（`.automation/backup/llm-frontier-2026.<ts>.<pid>.html`，目录已忽略），更新器不自行写备份或状态。
10. 更新后先检查工作树、全部插入标记、唯一 ID、主题锚点、日期有效性与一致性，日期不得倒退；随后运行统一构建和产物检查。`.automation/check-frontier.py` 是语义护栏，不冒充完整 HTML5 结构校验器。结构检查须支持 HTML5；macOS 自带的旧版 `tidy` 会误报合法 HTML5 元素，不得作为唯一硬门槛。以 headless Chromium/Chrome 渲染**公开产物**，检查目录锚点、`#last-updated`、更新条目与主要 section；浏览器工具缺失时可降级为结构/锚点检查并在报告说明。真实结构/产物检查失败或出现其他文件修改则**不提交**。正文、公开文章与博客最近更新日期必须一致，状态、备份和缓存不能公开。
11. 若无实质新进展且事实巡检没有产生修正 → 跳过提交，仅记录「本轮无实质更新」。
12. 默认到此只报告本地准备完成，不提交、不推送。仅明确获准的 `--publish` 模式由运行器执行 `git add -- content/posts/llm-frontier-2026/index.html`，再用 `git commit --only -m "docs(frontier): update YYYY-MM-DD" -- content/posts/llm-frontier-2026/index.html` 限定提交范围；消息日期取已校验的正文 `last-updated`。其他暂存、未暂存、未跟踪文件仍须阻塞，不能因限定路径而忽略它们。提交后工作树仍须干净才允许 `git push origin HEAD:main`。更新器本身绝不执行这些操作。
13. 结果报告轮换复核的主题、核验/修正/删除数量、新增条目数、最多 3 条要点、提交 SHA 与阻塞项。本地准备、已提交、已推送与已部署必须分别表达；推送成功不证明 Actions 发布成功。IM 不在本自动化授权范围。

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
- 只增量插入和必要事实修正，不重写整页；只编辑 `content/posts/llm-frontier-2026/index.html`。不得为修正登记日期而编辑 `content/catalog.json`，不得把根目录生成 HTML 加入提交。
- 不引用本地偏见目录（蚂蚁/AReaL/AWorld/Awex/AntAngelMed/Ling-1T 等）作为唯一来源；相关话题须独立 web 核实。
- 不把 WebSearch snippet 的「教授名+论文名」当作者证据；论文作者以 arXiv abs 全列表为准。
- push 前必须完成同一产物的检查及可用的渲染自检；没有远端写入授权时到本地准备为止。

## 定时任务 Prompt（payload.message 原文）
> 由 Codex 对 LLM 前沿做每 3 天一次的增量调研、事实巡检并更新博客页。范围：开源模型（Kimi/Qwen/DeepSeek）、闭源前沿模型、新架构（loop transformer 等）、Muon 优化器、Agent、RL 算法（GRPO 家族）、OPD、训练策略、Benchmark（含 Terminal-Bench）、Protein LLM。
> 更新器步骤：运行器已确认工作树干净并完成备份；读取 `$repo_root/content/posts/llm-frontier-2026/index.html` 的 #changelog 最新有效日期作为上次成功更新日。每轮先核验所有待发布的新条目，并轮换复核一个既有主题 section 的高风险事实；冲突或无法确认的断言改正、降级或删除并记录理由。之后只调研有实质增量的新进展，独立核实来源、附 `https` 链接并标明事实性质；按「已跟踪组织」执行组织级巡检，工具缺失或单个源不可用时降级并报告。仅编辑该正文，按 `.update-entry` 结构插入对应 `AUTO:INSERT:*` 标记之后；保留所有标记，新内容或事实修正同步更新 #last-updated 与 #changelog，无实质更新则不改文件。不执行任何 Git 写操作、构建、部署或 IM，不修改登记表、根目录 HTML 或其他仓库文件。报告第一行必须是 FRONTIER_RESULT: UPDATED、FRONTIER_RESULT: NO_CHANGE 或 FRONTIER_RESULT: BLOCKED；随后给出轮换复核主题、核验/修正/删除数量、新增条目数、三条以内要点和准确阻塞项。运行器负责后续统一构建检查，仅显式授权后才提交唯一正文并推送；不得把本地准备或推送描述为线上已同步。详细协议见 `.automation/update-frontier.md`。
