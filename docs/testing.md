---
title: Testing
---

# Testing

We use `pytest` + `pytest-asyncio`.

## Structure

```text
tests/
  support/
  unit/
    repositories/
      conftest.py
      test_*.py
    services/
      conftest.py
      test_*.py
    routers/
      conftest.py
      test_*.py
```

## Conventions

- `tests/support/` is for reusable builders, helpers, and factories.
- There is no root `tests/conftest.py`; fixtures live in layer-specific `conftest.py` files under each `tests/unit/` subfolder.
- Avoid a global `conftest.py` if the fixture only serves one layer.
- Repository tests: real test database.
- Service tests: repository mock.
- Router tests: service mock.
- Use `AsyncClient` only when the test crosses the HTTP layer; for unit tests, keep isolation with mocks.
- One test = one behavior.

## Commands

Full suite:

```bash
uv run python -m pytest tests
```

Specific file:

```bash
uv run python -m pytest tests/unit/services/test_candidate_service.py
```

Fail fast:

```bash
uv run python -m pytest tests -x
```
