---
title: Testing
---

# Testing

Usamos `pytest` + `pytest-asyncio`.

## Estructura

```text
tests/
  support/
  unit/
    repositories/
    services/
    routers/
  conftest.py
```

## Convenciones

- `tests/support/` para builders, helpers y factories reutilizables.
- `conftest.py` solo por scope: global o por capa.
- `conftest.py` debe vivir cerca de los tests que consume; evitá helpers globales si aplican solo a una capa.
- Repository tests: DB real de test.
- Service tests: repository mock.
- Router tests: service mock.
- `AsyncClient` solo cuando el test cruza la capa HTTP; para unit tests, mantené el aislamiento con mocks.
- Un test = un comportamiento.

## Comandos

Suite completa:

```bash
uv run python -m pytest tests
```

Un archivo específico:

```bash
uv run python -m pytest tests/unit/services/test_candidate_service.py
```

Fail fast:

```bash
uv run python -m pytest tests -x
```
