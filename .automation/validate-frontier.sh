#!/bin/bash
set -euo pipefail
repo_root="${1:?repository root required}"
source_path="${2:?authoritative source required}"
[[ "$source_path" == "content/posts/llm-frontier-2026/index.html" ]]
python="${FRONTIER_PYTHON:-$HOME/.cache/stein-notes/venv/bin/python}"
[[ -x "$python" ]] || { echo "Run make setup or set FRONTIER_PYTHON to the pinned-dependency interpreter." >&2; exit 1; }
artifact="$(mktemp -d "${TMPDIR:-/tmp}/frontier-artifact.XXXXXX")"
trap 'rm -rf "$artifact"' EXIT
"$python" "$repo_root/scripts/build.py" --output "$artifact"
"$python" "$repo_root/scripts/check.py" --output "$artifact"
"$python" - "$artifact" <<'PY'
import json, pathlib, sys
root = pathlib.Path(sys.argv[1])
catalog = json.loads((root / "blog/catalog.json").read_text())
record = next(e for e in catalog["entries"] if e["id"] == "llm-frontier-2026")
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from html.parser import HTMLParser
class Date(HTMLParser):
    value = None
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id") == "last-updated":
            self.value = attrs.get("datetime")
doc = Date()
doc.feed((root / "llm-frontier-2026.html").read_text())
assert record["updated"] == doc.value, (record["updated"], doc.value)
print("PASS: frontier source date and public catalog date agree: " + doc.value)
PY
