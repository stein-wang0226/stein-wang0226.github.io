#!/bin/bash
set -euo pipefail

repo_root="$(git -C "$(dirname "$0")/.." rev-parse --show-toplevel)"
state_dir="$repo_root/.automation/state"
last_run_file="$state_dir/last-successful-scheduled-run"
result_file="$state_dir/last-result.md"
interval_seconds=259200

mkdir -p "$state_dir"

now_epoch="$(date +%s)"
if [[ -f "$last_run_file" ]]; then
    last_epoch="$(tr -d '[:space:]' < "$last_run_file")"
    if [[ "$last_epoch" =~ ^[0-9]+$ ]] && (( now_epoch - last_epoch < interval_seconds )); then
        echo "Frontier update skipped: last successful scheduled run is less than 72 hours ago."
        exit 0
    fi
fi

prompt="$(cat <<'EOF'
在当前仓库中执行一次 LLM 前沿博客增量更新。严格、完整地遵循
.automation/update-frontier.md；该文件是唯一的流程规范。

必须先检查工作树并 `git pull --ff-only origin main`。只在发现可核实的实质增量时修改
llm-frontier-2026.html；无实质更新时不要改文件、不要提交。若有修改，完成协议要求的
备份、HTML 结构检查和 headless 浏览器渲染检查后，只暂存这个 HTML 文件，使用协议规定的
commit message 提交并 push 到 origin/main。

完成时报告检查时间、上次更新日、新增条目数、最多三项要点、是否提交及 SHA、线上 URL；
失败时报告准确阻塞点。不要发送 IM 或修改本仓库中与协议指定页面无关的文件。
EOF
)"

if /Users/bytedance/.local/bin/codex exec \
    --dangerously-bypass-approvals-and-sandbox \
    --search \
    -C "$repo_root" \
    --output-last-message "$result_file" \
    "$prompt"; then
    printf '%s\n' "$now_epoch" > "$last_run_file"
    echo "Frontier update completed successfully."
else
    echo "Frontier update failed; it will be retried on the next daily scheduler check." >&2
    exit 1
fi
