.PHONY: help run test lint typecheck format check ui translations install dev clean build installer

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

run: ## Run the bot application
	uv run python bot/main.py

test: ## Run tests with coverage
	uv run pytest

lint: typecheck ## Run basedpyright type check then ruff linter and formatter checks
	uv run ruff check bot/ tests/
	uv run ruff format --check bot/ tests/

typecheck: ## Run basedpyright static type checker
	uv run basedpyright

format: ## Auto-fix lint issues and format code
	uv run ruff check --fix bot/ tests/
	uv run ruff format bot/ tests/

check: ## Run pre-commit hooks on all files
	uv run pre-commit run --all-files

ui: ## Compile Qt Designer .ui files to Python
	uv run pyside6-uic bot/ui/main_window.ui -o bot/ui/main_window_ui.py

translations: ## Update .ts translation files and compile to .qm
	uv run pyside6-lupdate bot/ui/main_window.ui bot/ui/modals.py bot/ui/handlers/config_handler.py bot/ui/main_window.py -ts bot/i18n/nw_bot_fr.ts
	uv run pyside6-lrelease bot/i18n/nw_bot_fr.ts -qm bot/i18n/nw_bot_fr.qm

install: ## Install dependencies
	uv sync

dev: ## Install all dev dependencies (test + lint tools)
	uv sync --extra test --extra lint
	uv run pre-commit install

clean: ## Clean build artifacts and cache files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete
	find . -type f -name "coverage.xml" -delete
	rm -rf build/ dist/

build: ui ## Build executable with PyInstaller
	uv run pyinstaller nwbot.spec

installer: build ## Build Windows NSIS installer (requires NSIS)
	makensis installer.nsi
