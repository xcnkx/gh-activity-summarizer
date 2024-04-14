BRANCH:=$(subst _,-,$(subst /,-,$(shell git branch --show-current)))
COMMIT_HASH := $(shell git rev-parse --short HEAD | head -c 7)

POETRY := poetry
PYTEST := .venv/bin/pytest
RUFF   := .venv/bin/ruff
MYPY   := .venv/bin/mypy

.PHONY: setup
setup:
	$(POETRY) env use python3.12
	$(POETRY) install

.PHONY: lint
lint:
	$(RUFF) check src tests
	$(MYPY) src tests

.PHONY: fix
fix:
	$(RUFF) check src tests --fix
	$(RUFF) format src tests

.PHONY: run/*
run/cli:
	$(POETRY) run python cli/summarizer.py

run/llm:
	$(POETRY) run python cli/llm.py