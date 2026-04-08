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
| Web | `web/` | Preact, TypeScript, Vite, pnpm |

## Available Skills

### Generic Skills (Any Project)

| Skill | Description | Location |
|-------|-------------|----------|
| `uv-python` | Ultra-fast Python package manager | [SKILL.md](skills/uv-python/SKILL.md) |
| `pnpm` | Fast, disk-efficient Node.js package manager | [SKILL.md](skills/pnpm/SKILL.md) |
| `pytest` | Testing patterns with pytest and pytest-asyncio | [SKILL.md](skills/pytest/SKILL.md) |
| `git-commit` | Git commit workflow following conventional commits | [SKILL.md](skills/git-commit/SKILL.md) |
| `pr-creation` | Pull request workflow | [SKILL.md](skills/pr-creation/SKILL.md) |

### Project-Specific Skills

| Skill | Description | Location |
|-------|-------------|----------|
| `langchain-agents` | LangChain v1 patterns for AI agents with create_agent | [SKILL.md](skills/langchain-agents/SKILL.md) |
| `langchain-agent-architecture` | Architecture decision guide for workflows, single agents, multi-agent | [SKILL.md](skills/langchain-agent-architecture/SKILL.md) |
| `langchain-tests` | Testing patterns for LangChain v1 agents and tools | [SKILL.md](skills/langchain-tests/SKILL.md) |
| `preact-ui` | Preact patterns for UI components, forms, and hooks | [SKILL.md](skills/preact-ui/SKILL.md) |
| `tailwind-4` | Tailwind CSS 4 patterns, cn() utility, and best practices (web only) | [SKILL.md](skills/tailwind-4/SKILL.md) |
| `zod-4` | Zod 4 schema validation patterns, parsing, and type inference (web only) | [SKILL.md](skills/zod-4/SKILL.md) |

### Auto-invoke Skills

When performing these actions, ALWAYS invoke the corresponding skill FIRST:

| Action | Skill |
|--------|-------|
| Writing Python tests with pytest | `pytest` |
| Writing tests for LangChain agents/tools | `langchain-tests` |
| Creating a git commit | `git-commit` |
| Creating a pull request | `pr-creation` |
| Working with Python packages (install, sync, run) | `uv-python` |
| Working with Node.js packages (install, run scripts) | `pnpm` |
| Creating or modifying Preact UI components in web/ | `preact-ui` |
| Styling with Tailwind CSS in web/ | `tailwind-4` |
| Creating or modifying Zod validation schemas | `zod-4` |
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

## Frontend Development

```bash
cd web
pnpm install
pnpm dev
pnpm build
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
- **Separation of Concerns (Web)**: Components render only — logic lives in `utils/*.logic.ts` as pure TypeScript with zero framework imports

---

## Component-Specific Guidelines

| Component | Guidelines | Critical Focus |
|-----------|------------|----------------|
| API (`api/`) | [api/AGENTS.md](api/AGENTS.md) | Repository → Service → Router, Protocol DI |
| Web (`web/`) | [web/AGENTS.md](web/AGENTS.md) | Separation of logic from UI components |
