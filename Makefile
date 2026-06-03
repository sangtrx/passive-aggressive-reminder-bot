.PHONY: help install install-dev test test-cov lint format type-check clean run

help:
	@echo "Passive-Aggressive Reminder Bot - Development Commands"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  help          Show this help message"
	@echo "  install       Install the package"
	@echo "  install-dev   Install package with development dependencies"
	@echo "  test          Run the test suite"
	@echo "  test-cov      Run tests with coverage report"
	@echo "  lint          Run Ruff linter"
	@echo "  lint-fix      Run Ruff linter with auto-fix"
	@echo "  format        Format code with Black"
	@echo "  type-check    Run mypy type checker"
	@echo "  check         Run all checks (lint, format, type-check)"
	@echo "  clean         Remove build artifacts and cache files"
	@echo "  run           Run the CLI application"

install:
	pip install -e .

install-dev:
	pip install -e .
	pip install -r requirements-dev.txt

test:
	python3 -m pytest tests/ -v

test-cov:
	python3 -m pytest tests/ -v --cov=passive_aggressive_reminder_bot --cov-report=term-missing

lint:
	ruff check passive_aggressive_reminder_bot tests

lint-fix:
	ruff check --fix passive_aggressive_reminder_bot tests

format:
	black passive_aggressive_reminder_bot tests

type-check:
	mypy passive_aggressive_reminder_bot --no-error-summary

check: lint format type-check test
	@echo "✓ All checks passed!"

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + || true
	find . -type d -name .pytest_cache -exec rm -rf {} + || true
	find . -type d -name .mypy_cache -exec rm -rf {} + || true
	find . -type f -name *.pyc -delete
	find . -type f -name *.pyo -delete
	rm -rf build/ dist/ *.egg-info/
	@echo "✓ Cleaned up cache files"

run:
	python3 -m passive_aggressive_reminder_bot remind "example reminder" --spice 3

docker-build:
	docker build -t passive-aggressive-reminder-bot:local .

