# Testing

## Stack

- `pytest` + `pytest-asyncio` (async mode: `auto`)
- `httpx.AsyncClient` for HTTP-level tests
- `aiosqlite` for repository test isolation
- `unittest.mock.AsyncMock` for service and processor tests

## Structure

```
tests/
  support/                          # Shared builders and helpers
    evaluation.py                   # make_evaluation(), evaluation_payload()
    candidate.py                    # make_candidate(), candidate_payload()
    job.py                          # make_job(), job_payload()
  unit/
    repositories/
      conftest.py                   # SQLite in-memory session fixture
      test_candidate_repository.py
      test_job_repository.py
      test_evaluation_repository.py
    services/
      conftest.py                   # Mock repositories and service fixtures
      test_candidate_service.py
      test_job_service.py
      test_evaluation_service.py
      test_evaluation_processor.py  # Background processor tests
    routers/
      conftest.py                   # AsyncClient + service mock fixtures
      test_candidate_router.py
      test_job_router.py
      test_evaluation_router.py
    infrastructure/
      test_evaluation_analyzer.py   # LLM analyzer unit tests
      test_exceptions.py            # Error translation tests
      test_prompts.py               # Prompt construction tests
  integration/
    test_evaluation_analyzer.py     # Real LLM call (gated by env var)
    test_db_error_handler.py        # DB error handling integration
```

## Conventions

- **One test = one behavior.** Each test asserts a single outcome.
- **Fixtures live in layer-specific `conftest.py`**, not a root conftest.
- **`tests/support/`** contains reusable model builders used across all test layers.
- **Mocking strategy**: each layer mocks the layer below it:
  - Repositories → use real SQLite (in-memory)
  - Services → mock repositories
  - Routers → mock services

## Markers

| Marker | Purpose | How to use |
|--------|---------|------------|
| `integration` | Tests that call real external services (LLM, DB) | `@pytest.mark.integration` |

Run only unit tests (skip integration):

```bash
uv run python -m pytest tests/unit -v
```

Run including integration tests:

```bash
uv run python -m pytest tests -v
```

Run only integration tests:

```bash
uv run python -m pytest tests -m integration -v
```

## LLM Integration Tests

Tests in `tests/integration/test_evaluation_analyzer.py` make **real LLM API calls**. They are gated by the `RUN_LLM_INTEGRATION` environment variable:

```bash
# Skipped by default
uv run python -m pytest tests/integration/test_evaluation_analyzer.py -v

# Run with real LLM
RUN_LLM_INTEGRATION=1 uv run python -m pytest tests/integration/test_evaluation_analyzer.py -v
```

Requires valid LLM credentials in `.env` (see [setup.md](setup.md)).

## Commands

```bash
# Full suite
uv run python -m pytest tests -v

# Unit tests only
uv run python -m pytest tests/unit -v

# Specific file
uv run python -m pytest tests/unit/services/test_candidate_service.py -v

# Specific test
uv run python -m pytest tests/unit/services/test_candidate_service.py::TestCandidateServiceCreateCandidate::test_creates_candidate -v

# With coverage
uv run python -m pytest tests --cov=app --cov-report=html

# Stop on first failure
uv run python -m pytest tests -x
```
