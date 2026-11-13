#!/bin/bash
set -euo pipefail

publish=false
if [[ "${1:-}" == "--publish" && $# == 1 ]]; then
    publish=true
elif [[ $# != 0 ]]; then
    echo "Usage: $0 [--publish]" >&2
    exit 2
fi

repo_root="$(git -C "$(dirname "$0")/.." rev-parse --show-toplevel)"
source_path="content/posts/llm-frontier-2026/index.html"
source_file="$repo_root/$source_path"
state_dir="$repo_root/.automation/state"
last_run_file="$state_dir/last-successful-scheduled-run"
result_file="$state_dir/last-result.md"
interval_seconds=259200
python="${FRONTIER_PYTHON:-python3}"
updater="${FRONTIER_UPDATER:-/Users/bytedance/.local/bin/codex}"
validator="${FRONTIER_VALIDATOR:-$repo_root/.automation/validate-frontier.sh}"
guard="$repo_root/.automation/check-frontier.py"

mkdir -p "$state_dir"
block() {
    printf 'FRONTIER_RESULT: BLOCKED\n\n%s\n' "$*" > "$result_file"
    echo "Frontier update blocked: $*" >&2
    exit 1
}

lock_dir="$state_dir/run.lock"
mkdir "$lock_dir" 2>/dev/null || block "Another run holds $lock_dir; inspect it before removing a stale lock."
trap 'rmdir "$lock_dir"' EXIT

if ! details="$("$python" "$guard" worktree --repo "$repo_root" --phase clean 2>&1)"; then
    block "$details"
fi
now_epoch="$(date +%s)"
if [[ -f "$last_run_file" ]]; then
    last_epoch="$(tr -d '[:space:]' < "$last_run_file")"
    if [[ "$last_epoch" =~ ^[0-9]+$ ]] && (( now_epoch >= last_epoch && now_epoch - last_epoch < interval_seconds )); then
        echo "Frontier update skipped: last successful scheduled run is less than 72 hours ago."
        exit 0
    fi
fi

[[ -x "$updater" ]] || block "Updater is not executable: $updater"
[[ -x "$validator" ]] || block "Build/check interface is required: provide an executable FRONTIER_VALIDATOR (repo root, source path); it must build and check external public output."
if $publish; then
    branch="$(git -C "$repo_root" symbolic-ref --short HEAD)"
    [[ "$branch" == main ]] || block "Publication requires branch main, found $branch."
    git -C "$repo_root" pull --ff-only origin main || block "Fast-forward pull failed; no update was attempted."
    if ! details="$("$python" "$guard" worktree --repo "$repo_root" --phase clean 2>&1)"; then
        block "$details"
    fi
fi

backup_dir="$repo_root/.automation/backup"
mkdir -p "$backup_dir"
backup_file="$backup_dir/llm-frontier-2026.$(date -u +%Y%m%dT%H%M%SZ).$$.html"
cp -p "$source_file" "$backup_file"
if ! details="$("$python" "$guard" document --source "$source_file" 2>&1)"; then
    block "$details"
fi

prompt="$(cat <<'EOF'
在当前仓库中执行一次 LLM 前沿博客增量更新。严格、完整地遵循
.automation/update-frontier.md；该文件是唯一的流程规范。

运行器已检查工作树并备份。只在发现可核实的实质增量时修改
content/posts/llm-frontier-2026/index.html；无实质更新时不要改文件。
保留全部 AUTO:INSERT:* 标记；新增/修正时同步 last-updated 与 changelog 的有效日期。
只编辑该正文，不修改登记表、根目录 HTML、脚本、协议或状态；不要执行任何 Git 写操作
（包括 pull/add/commit/push），不要构建或部署。运行器负责备份、构建、检查和获准后的发布。

报告第一行必须是 FRONTIER_RESULT: UPDATED、FRONTIER_RESULT: NO_CHANGE 或
FRONTIER_RESULT: BLOCKED 之一。随后报告检查时间、上次更新日、轮换复核主题、
核验/修正/删除数量、新增条目数、最多三项要点和准确阻塞点；不要声称已发布或发送 IM。
EOF
)"

# Remove a previous report so an updater failure cannot reuse a success marker.
rm -f "$result_file"
if ! "$updater" exec \
    --sandbox workspace-write \
    --search \
    -C "$repo_root" \
    --output-last-message "$result_file" \
    "$prompt"; then
    block "Updater failed. Backup: $backup_file. Any working-tree changes were left for review."
fi
if ! details="$("$python" "$guard" worktree --repo "$repo_root" --phase updated 2>&1)"; then
    block "$details Backup: $backup_file. No files were staged or committed."
fi
[[ -f "$result_file" ]] || block "Updater did not produce a result report."
result="$(head -n 1 "$result_file")"
case "$result" in
    "FRONTIER_RESULT: UPDATED" | "FRONTIER_RESULT: NO_CHANGE") ;;
    *) block "Updater did not report success ($result). Backup: $backup_file." ;;
esac
if cmp -s "$source_file" "$backup_file"; then
    [[ "$result" == "FRONTIER_RESULT: NO_CHANGE" ]] || block "Updater reported UPDATED but the source did not change."
    printf '%s\n' "$now_epoch" > "$last_run_file"
    echo "Frontier review completed: no substantive change; no commit or push."
    exit 0
fi
[[ "$result" == "FRONTIER_RESULT: UPDATED" ]] || block "Source changed despite a NO_CHANGE report. Backup: $backup_file."
if ! details="$("$python" "$guard" document --source "$source_file" --baseline "$backup_file" 2>&1)"; then
    block "$details Backup: $backup_file."
fi

# The adapter must use the same external build/check output as preview and CI.
validated_source="$(git -C "$repo_root" hash-object -- "$source_path")"
"$validator" "$repo_root" "$source_path" || block "Build/check validator failed. Backup: $backup_file."
[[ "$(git -C "$repo_root" hash-object -- "$source_path")" == "$validated_source" ]] || block "Build/check validator modified the authoritative source; no files were committed."
if ! details="$("$python" "$guard" worktree --repo "$repo_root" --phase updated 2>&1)"; then
    block "$details No files were staged or committed."
fi
if ! $publish; then
    printf '\nPublication: local preparation only; not committed, pushed, or deployed.\n' >> "$result_file"
    echo "Frontier update validated locally; publication was not authorized."
    exit 0
fi

updated_date="$("$python" "$guard" document --source "$source_file")"
git -C "$repo_root" add -- "$source_path"
# --only protects against unrelated index entries appearing after the guard.
git -C "$repo_root" commit --only -m "$(cat <<EOF
docs(frontier): update $updated_date
EOF
)" -- "$source_path"
if ! details="$("$python" "$guard" worktree --repo "$repo_root" --phase clean 2>&1)"; then
    block "$details Commit exists locally; nothing was pushed."
fi
commit_sha="$(git -C "$repo_root" rev-parse HEAD)"
git -C "$repo_root" push origin HEAD:main || block "Push failed; commit $commit_sha remains local."
printf '%s\n' "$now_epoch" > "$last_run_file"
printf '\nPublication: pushed %s to origin/main; Actions and online deployment still require verification.\n' "$commit_sha" >> "$result_file"
echo "Frontier source pushed: $commit_sha; deployment is not yet verified."
