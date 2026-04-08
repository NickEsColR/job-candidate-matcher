# Job-Candidate-Matcher

AI-powered candidate evaluation API that analyzes candidate profiles against job descriptions and generates structured compatibility reports using LLM-based analysis.

## Quick Start

```bash
# 1. Start the database
docker compose up -d

# 2. Configure environment
cp .env.example .env
# Edit .env with your LLM provider credentials (see docs/setup.md)

# 3. Install & run
uv sync
uv run uvicorn app.main:app --reload

# 4. Open docs
# http://localhost:8000/docs
```

## What It Does

- **Candidates**: CRUD for candidate profiles (name, skills, experience, resume URL)
- **Jobs**: CRUD for job positions (title, requirements, location, salary range)
- **Evaluations**: AI-powered matching — creates an async evaluation that scores a candidate against a job (0–100), with strengths, weaknesses, and recommendations

Evaluations run asynchronously via background tasks. A `POST` returns immediately while the LLM analysis processes in the background. Poll the evaluation to check completion.

## Project Structure

```
app/
  core/           # Settings, logger
  infrastructure/ # DB engine, exceptions, LLM integration
  models/         # SQLModel ORM entities
  repositories/   # Data access layer
  schemas/        # Pydantic request/response DTOs
  services/       # Business logic
  routers/        # FastAPI HTTP endpoints
tests/
  unit/           # Isolated tests with mocks
  integration/    # Real external service tests
  support/        # Shared builders and helpers
```

## Documentation

| Topic | Description |
|-------|-------------|
| [API Endpoints](docs/api.md) | What each endpoint expects and returns |
| [Architecture](docs/architecture.md) | System design and module breakdown |
| [Stack](docs/stack.md) | Technology choices and justifications |
| [Setup](docs/setup.md) | Development environment configuration |
| [Testing](docs/testing.md) | Testing patterns and conventions |

---

<div align="center">
<a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT"></a>
</div>
