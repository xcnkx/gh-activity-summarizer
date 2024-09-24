BRANCH:=$(subst _,-,$(subst /,-,$(shell git branch --show-current)))
COMMIT_HASH := $(shell git rev-parse --short HEAD | head -c 7)

uv := uv
PYTEST := .venv/bin/pytest
RUFF   := .venv/bin/ruff
MYPY   := .venv/bin/mypy

.PHONY: setup
setup:
	$(uv) venv
	$(uv) sync

.PHONY: lint
lint:
	$(RUFF) check src tests
	$(MYPY) src tests

.PHONY: fix
fix:
	$(RUFF) check src tests --fix
	$(RUFF) format src tests