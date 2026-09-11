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
3. 独立核实来源、附可点击链接；区分事实与传闻；厂商自报基准加 `pill self`。
4. 把新条目插入对应 section 的 `<!-- AUTO:INSERT -->` 锚点之后（新条目放最前）。
5. 更新 hero 的 `<span id="last-updated">` 为今天日期；在 `#changelog` 锚点后追加一条更新日志。
6. 更新前对 `llm-frontier-2026.html` 做时间戳备份（如 `.automation/backup/llm-frontier-2026.<ts>.html`）。
7. headless 渲染自检（`--dump-dom` 确认 section/div/table 配平、无异常）；异常则**不提交**并告警。
8. 若无实质新进展 → 跳过提交，仅记录「本周无实质更新」。
9. 提交：`git add llm-frontier-2026.html`（只 add 本文件），commit message `docs(frontier): weekly update YYYY-MM-DD`，push 到 `main`。
10. 将本次更新摘要（新增条目数 + 要点 3 条内）发送到指定 IM 会话通知。

## 安全护栏
- 只增量插入，不重写整页；不触碰仓库内其它无关文件。
- 不引用本地偏见目录（蚂蚁/AReaL/AWorld/Awex/AntAngelMed/Ling-1T 等）作为唯一来源；相关话题须独立 web 核实。
- 不把 WebSearch snippet 的「教授名+论文名」当作者证据；论文作者以 arXiv abs 全列表为准。
- push 前必须渲染自检通过。

## 定时任务 Prompt（payload.message 原文）
> 对 LLM 前沿做每周增量调研并更新博客页。范围：开源模型（Kimi/Qwen/DeepSeek）、闭源前沿模型、新架构（loop transformer 等）、Muon 优化器、Agent、RL 算法（GRPO 家族）、OPD、训练策略、Benchmark（含 Terminal-Bench）、Protein LLM。
> 步骤：先读 /Users/stein/Desktop/算法面试-LLM学习/stein-wang0226.github.io/llm-frontier-2026.html 的 #changelog 最新日期作为上次更新日；只调研该日期之后的新进展，独立核实来源、附链接、区分事实与传闻（传闻标 pill rumor，厂商自报标 pill self）。把新条目按统一 .update-entry 结构插入对应 section 的 <!-- AUTO:INSERT --> 锚点之后，更新 hero 的 #last-updated 与 #changelog。更新前先备份该 html 到 .automation/backup/。若本周无实质新进展则跳过提交。提交前做 headless 渲染自检，异常则不提交并告警。通过后 git add 仅该文件，commit「docs(frontier): weekly update <今天日期>」并 push 到 main。完成后将更新摘要（新增条目数+3条要点）发送到指定 IM 会话通知我。详细协议见仓库 .automation/update-frontier.md。
