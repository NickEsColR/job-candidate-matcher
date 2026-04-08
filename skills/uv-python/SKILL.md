---
name: uv-python
description: >
  Ultra-fast Python package manager for installations and script execution.
  Trigger: When working with Python packages, virtual environments, or running Python scripts.
license: Apache-0.0
metadata:
  author: NickEsColR
  version: "1.0"
---

## When to Use

- Installing Python libraries (dependencies)
- Running Python scripts without manual venv activation
- Managing virtual environments
- Creating reproducible Python environments with lockfiles

## Critical Patterns

1. **Use `uv run` instead of activating venv** — No manual activation needed
2. **Always use lockfiles (`uv.lock`)** — Ensures reproducible builds
3. **Use `uv add`** instead of `uv pip install` for project dependencies — Updates pyproject.toml automatically
4. **Pin Python version** with `.python-version` for consistency

## Installation

```bash
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or via pip
pip install uv
```

Verify: `uv --version`

## Package Management

### Install Dependencies

```bash
# Add package to project (updates pyproject.toml)
uv add requests pandas

# Add with version constraint
uv add "django>=4.0,<5.0"

# Add dev dependencies
uv add --dev pytest ruff

# Install from requirements.txt
uv pip install -r requirements.txt
```

### Remove Dependencies

```bash
uv remove requests
uv remove --dev pytest
```

### Lockfile

```bash
# Create/update lockfile
uv lock

# Install from lockfile (exact versions, no resolution)
uv sync --frozen
```

## Running Python

### Pattern: Use `uv run`

```bash
# Run script (auto-activates venv)
uv run python script.py

# Run CLI tool
uv run pytest
uv run black .
uv run ruff check .

# Pass arguments
uv run python script.py --arg value
```

### Running as Module

When code is structured as a package (with `__init__.py`), run as module:

```bash
# Run main module from project root
uv run python -m app

# Run from subdirectory
uv run python -m app.main

# Run with dev dependencies (e.g., uvicorn for FastAPI)
uv run uvicorn app.main:app --reload
```

### Running from Subdirectories

For projects where code lives in subfolders like `/app`, `/src`, or `/lib`:

```bash
# From project root, run script in subdirectory
uv run python app/main.py
uv run python src/utils.py

# Run as module (if package structure exists)
uv run python -m app.main
uv run python -m src.models

# Run dev server from subdirectory
uv run uvicorn app.main:app --reload --port 8000
```

### Common Patterns by Framework

```bash
# FastAPI
uv run uvicorn app.main:app --reload

# Flask
uv run flask --app app.main run --debug

# Django
uv run python manage.py runserver

# Streamlit
uv run streamlit run app/main.py
```

## Quick Reference

| Task | Command |
|------|---------|
| Add dependency | `uv add <package>` |
| Add dev dependency | `uv add --dev <package>` |
| Install from lockfile | `uv sync --frozen` |
| Run script | `uv run python <script>.py` |
| Run script in subdir | `uv run python app/main.py` |
| Run as module | `uv run python -m app` |
| Run module in subdir | `uv run python -m app.main` |
| Run dev server | `uv run uvicorn app.main:app --reload` |
| Run tool | `uv run <tool> <args>` |
| Create lockfile | `uv lock` |
| Update all | `uv sync --upgrade` |

## Best Practices

- Commit `uv.lock` to version control
- Use `--frozen` in CI/CD for consistent builds
- Use `uv run` instead of activating venv manually
- NEVER use pip in this project — always use uv
