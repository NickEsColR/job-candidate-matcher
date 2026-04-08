# Technology Stack

## Core

| Technology | Purpose | Why |
|------------|---------|-----|
| **FastAPI** | REST API framework | Native async, auto-generated OpenAPI docs, dependency injection |
| **Pydantic v2** | Data validation | Request/response schemas, field validation, JSON schema generation |
| **SQLModel** | ORM | Combines SQLAlchemy ORM with Pydantic validation, type-safe queries |
| **PostgreSQL** | Primary database | Robust relational DB with JSON column support for arrays |
| **asyncpg** | DB driver | High-performance async PostgreSQL driver |

## AI / LLM

| Technology | Purpose | Why |
|------------|---------|-----|
| **LangChain** | LLM orchestration | Provider-agnostic model initialization, structured output, retry logic |
| **langchain-openai** | OpenAI integration | Supports GPT models via LangChain |
| **langchain-google-genai** | Google Gemini integration | Multi-provider support (swap `LLM_PROVIDER` in `.env`) |

The analyzer uses LangChain's `init_chat_model()` + `with_structured_output()` to get typed `EvaluationAnalysis` responses directly from the LLM. No function calling or tool definitions — the model returns a validated Pydantic object.

## Configuration

| Technology | Purpose |
|------------|---------|
| **pydantic-settings** | Loads `Settings` from `.env`, validates types, caches singleton |
| **python-dotenv** | `.env` file loading |

## Migrations

| Technology | Purpose |
|------------|---------|
| **Alembic** | Schema versioning and migrations (SQLModel integration) |

## Development

| Technology | Purpose |
|------------|---------|
| **uv** | Package management, virtual environments, script execution |
| **Docker Compose** | PostgreSQL 17 container for local development |
| **ruff** | Linting (E, F, I, N, W, UP, ANN rules) and formatting |
| **mypy** | Static type checking (Python 3.12 target) |
| **pre-commit** | Git hooks for code quality |

## Testing

| Technology | Purpose |
|------------|---------|
| **pytest** | Test runner |
| **pytest-asyncio** | Async test support (mode: auto) |
| **pytest-cov** | Coverage reporting |
| **httpx** | `AsyncClient` for testing FastAPI endpoints |
| **aiosqlite** | SQLite async driver for repository test isolation |
