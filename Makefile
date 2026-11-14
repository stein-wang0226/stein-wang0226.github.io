PYTHON ?= python3
VENV ?= $(HOME)/.cache/stein-notes/venv
PORT ?= 8000
OUTPUT ?= /tmp/my-blogs-site-build
GH ?= gh

.PHONY: setup build check preview new export governance inventory profile-check profile-status
setup:
	$(PYTHON) -m venv "$(VENV)"
	"$(VENV)/bin/pip" install -r requirements.txt

build:
	"$(VENV)/bin/python" scripts/build.py --output "$(OUTPUT)"

check: governance build
	"$(VENV)/bin/python" scripts/check.py --output "$(OUTPUT)"

preview: check
	$(PYTHON) -m http.server $(PORT) --bind 127.0.0.1 --directory "$(OUTPUT)"

new:
	"$(VENV)/bin/python" scripts/new_post.py "$(ID)" --title "$(TITLE)" --topic "$(TOPIC)" --type "$(or $(TYPE),principles)"

export: check
	"$(VENV)/bin/python" scripts/export.py --output "$(OUTPUT)" --dest "$(DEST)"

governance:
	"$(VENV)/bin/python" scripts/governance.py

inventory:
	"$(VENV)/bin/python" scripts/governance.py --inventory

profile-check:
	"$(VENV)/bin/python" scripts/profile.py check

profile-status:
	"$(VENV)/bin/python" scripts/profile.py status --gh "$(GH)"
