# Setup

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- Docker and Docker Compose (for PostgreSQL)

## 1. Database

Start PostgreSQL 17 with seed data:

```bash
docker compose up -d
```

This creates a PostgreSQL instance on `localhost:5432` with:

- **User**: `jcm_user`
- **Password**: `jcm_password`
- **Database**: `job_candidate_matcher`
- **Seed data**: Loaded from `scripts/seed.sql` on first run

Stop and clean up:

```bash
docker compose down        # Stop, keep data
docker compose down -v     # Stop and delete data
```

## 2. Environment Variables

Copy the example file and edit it:

```bash
cp .env.example .env
```

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `LLM_API_KEY` | API key for the LLM provider | `sk-...` |
| `LLM_PROVIDER` | LangChain provider identifier | `openai`, `google_genai` |
| `LLM_MODEL` | Model name | `gpt-4.1-mini`, `gemini-2.0-flash` |

### Optional Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `postgresql+asyncpg://jcm_user:jcm_password@localhost:5432/job_candidate_matcher` | SQLAlchemy connection string |
| `APP_HOST` | `0.0.0.0` | Server bind address |
| `APP_PORT` | `8000` | Server port |
| `DEBUG` | `false` | Enable debug mode (docs, reload, verbose logging) |
| `LLM_TEMPERATURE` | `0.0` | Model temperature (0.0 = deterministic) |
| `LLM_MAX_TOKENS` | `2048` | Max tokens per LLM response |
| `LLM_TIMEOUT` | `60` | LLM request timeout in seconds |
| `LLM_MAX_RETRIES` | `3` | Retry count on LLM failure |
| `LLM_MAX_CONCURRENCY` | `10` | Max concurrent LLM requests |
| `LLM_BASE_URL` | _(none)_ | Custom base URL for self-hosted or proxy endpoints |

### LLM Provider Examples

**OpenAI:**

```env
LLM_API_KEY=sk-your-openai-key
LLM_PROVIDER=openai
LLM_MODEL=gpt-4.1-mini
```

**Google Gemini:**

```env
LLM_API_KEY=your-google-key
LLM_PROVIDER=google_genai
LLM_MODEL=gemini-2.0-flash
```

**Custom endpoint (e.g., local LLM):**

```env
LLM_API_KEY=no-key
LLM_PROVIDER=openai
LLM_MODEL=local-model
LLM_BASE_URL=http://localhost:8080/v1
```

### Integration Tests

| Variable | Default | Description |
|----------|---------|-------------|
| `RUN_LLM_INTEGRATION` | `false` | Set to `1` or `true` to run tests that call real LLM APIs |

## 3. Install Dependencies

```bash
uv sync
```

This creates a virtual environment and installs all project and dev dependencies from `pyproject.toml`.

## 4. Run the Server

```bash
uv run uvicorn app.main:app --reload
```

- API: `http://localhost:8000`
- Interactive docs (debug mode): `http://localhost:8000/docs`

## 5. Run Tests

```bash
# Unit tests only
uv run python -m pytest tests/unit -v

# All tests (requires running PostgreSQL)
uv run python -m pytest tests -v

# Include real LLM integration tests
RUN_LLM_INTEGRATION=1 uv run python -m pytest tests -v
```

See [testing.md](testing.md) for full testing documentation.
