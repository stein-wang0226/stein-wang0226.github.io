PYTHON ?= python3
VENV ?= $(HOME)/.cache/stein-notes/venv
PORT ?= 8000
OUTPUT ?= /tmp/my-blogs-site-build

.PHONY: setup build check preview new export
setup:
	$(PYTHON) -m venv "$(VENV)"
	"$(VENV)/bin/pip" install -r requirements.txt

build:
	"$(VENV)/bin/python" scripts/build.py --output "$(OUTPUT)"

check: build
	"$(VENV)/bin/python" scripts/check.py --output "$(OUTPUT)"

preview: check
	$(PYTHON) -m http.server $(PORT) --bind 127.0.0.1 --directory "$(OUTPUT)"

new:
	"$(VENV)/bin/python" scripts/new_post.py "$(ID)" --title "$(TITLE)" --topic "$(TOPIC)" --type "$(or $(TYPE),principles)"

export: check
	"$(VENV)/bin/python" scripts/export.py --output "$(OUTPUT)" --dest "$(DEST)"
