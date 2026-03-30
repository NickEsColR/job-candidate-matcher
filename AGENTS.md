# Job-Candidate-Matcher - AI Agent Guidelines

## How to Use This Guide

- Start here for cross-project norms. This is a monorepo with several components.
- Each component has an `AGENTS.md` file with specific guidelines (e.g., `api/AGENTS.md`).
- Component docs override this file when guidance conflicts.

## Project Overview

Job-Candidate-Matcher is an AI-powered platform that evaluates candidates against job requirements using LLM agents.

| Component | Location | Tech Stack |
|-----------|----------|------------|
| API | `api/` | Python 3.12+, FastAPI, SQLModel, uv |
| Web | `web/` | TBD (Angular/React) |

## Available Skills

### Generic Skills (Any Project)

| Skill | Description | Location |
|-------|-------------|----------|
| `uv-python` | Ultra-fast Python package manager | [SKILL.md](skills/uv-python/SKILL.md) |
| `pytest` | Testing patterns with pytest and pytest-asyncio | [SKILL.md](skills/pytest/SKILL.md) |
| `git-commit` | Git commit workflow following conventional commits | [SKILL.md](skills/git-commit/SKILL.md) |
| `pr-creation` | Pull request workflow | [SKILL.md](skills/pr-creation/SKILL.md) |

### Project-Specific Skills

| Skill | Description | Location |
|-------|-------------|----------|
| `langchain-agents` | LangChain v1 patterns for AI agents with create_agent | [SKILL.md](skills/langchain-agents/SKILL.md) |
| `langchain-agent-architecture` | Architecture decision guide for workflows, single agents, multi-agent | [SKILL.md](skills/langchain-agent-architecture/SKILL.md) |
| `langchain-tests` | Testing patterns for LangChain v1 agents and tools | [SKILL.md](skills/langchain-tests/SKILL.md) |

### Auto-invoke Skills

When performing these actions, ALWAYS invoke the corresponding skill FIRST:

| Action | Skill |
|--------|-------|
| Writing Python tests with pytest | `pytest` |
| Writing tests for LangChain agents/tools | `langchain-tests` |
| Creating a git commit | `git-commit` |
| Creating a pull request | `pr-creation` |
| Working with Python packages (install, sync, run) | `uv-python` |
| Designing LangChain agent architecture | `langchain-agent-architecture` |
| Creating or modifying LangChain agents | `langchain-agents` |
| Adding new features | `langchain-agent-architecture` |

---

## Python Development

```bash
cd api
uv sync --extra dev
uv run pytest
uv run ruff check .
uv run ruff format .
```

---

## Commit & Pull Request Guidelines

Follow conventional-commit style: `<type>[scope]: <description>`

**Types:** `feat`, `fix`, `docs`, `chore`, `perf`, `refactor`, `style`, `test`

**Scopes:** `api`, `web`, `infra`, `ci`, `docs`

**Examples:**
- `feat(api): add candidate evaluation endpoint`
- `fix(api): handle null skills in candidate model`
- `ci: add path filters to test workflow`
- `docs: update API setup instructions`

---

## Key Architectural Decisions

- **Monorepo structure**: Backend in `api/`, frontend in `web/`, shared config at root
- **Clean Architecture**: API follows Repository → Service → Router pattern
- **Protocol-based DI**: Services depend on repository protocols, not concrete classes
- **Async-first**: All database operations use async SQLAlchemy
