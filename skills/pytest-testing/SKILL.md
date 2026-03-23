---
name: pytest-testing
description: >
  Testing patterns for Job-Candidate-Matcher using pytest and pytest-asyncio.
  Trigger: When writing tests, running tests, or adding test coverage.
license: Apache-2.0
metadata:
  author: NickEsColR
  version: "1.0"
---

## When to Use

- Writing unit tests for the API
- Testing async endpoints with BackgroundTasks
- Adding test coverage to new features
- Debugging test failures

## Critical Patterns

### Test Structure

| Pattern | Purpose |
|---------|---------|
| `tests/` directory | All test files go here |
| `test_*.py` | Test file naming |
| `Test*` | Test class naming |
| `test_*` | Test function naming |
| `conftest.py` | Shared fixtures |

### pytest-asyncio for FastAPI

FastAPI handlers are `async def`. Use `AsyncClient` with `pytest-asyncio`:

```python
import pytest
from httpx import AsyncClient
from myapp.main import app

@pytest.mark.asyncio
async def test_create_candidate():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/candidates",
            json={
                "full_name": "John Doe",
                "email": "john@example.com",
                "skills": ["Python", "FastAPI"],
                "years_of_experience": 5
            }
        )
    assert response.status_code == 201
```

### Testing BackgroundTasks

When testing endpoints that launch BackgroundTasks:

```python
@pytest.mark.asyncio
async def test_evaluation_returns_202():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/evaluations",
            json={"candidate_id": "...", "job_id": "..."}
        )
    
    # Returns 202 immediately
    assert response.status_code == 202
    
    # Check DB for completed status
    evaluation_id = response.json()["id"]
    # Poll or wait for status change
```

## Code Examples

### conftest.py - Basic fixtures

```python
import pytest
from httpx import AsyncClient
from sqlmodel import Session, SQLModel, create_engine
from myapp.main import app
from myapp.db import get_session

# Test database engine
TEST_DATABASE_URL = "postgresql://user:pass@localhost/test_db"

@pytest.fixture
def test_engine():
    engine = create_engine(TEST_DATABASE_URL)
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)

@pytest.fixture
def session(test_engine):
    with Session(test_engine) as session:
        yield session

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
```

### Test a Pydantic model

```python
from pydantic import ValidationError
from myapp.schemas.candidate import CandidateCreate

def test_candidate_create_valid():
    candidate = CandidateCreate(
        full_name="John Doe",
        email="john@example.com",
        skills=["Python"],
        years_of_experience=5
    )
    assert candidate.email == "john@example.com"

def test_candidate_create_invalid_email():
    with pytest.raises(ValidationError):
        CandidateCreate(
            full_name="John",
            email="invalid-email",
            skills=["Python"],
            years_of_experience=5
        )
```

### Test SQLModel model

```python
from myapp.models.candidate import Candidate

def test_candidate_model_defaults():
    candidate = Candidate(
        full_name="John",
        email="john@test.com",
        skills=["Python"],
        years_of_experience=3
    )
    assert candidate.id is not None
    assert candidate.created_at is not None
```

## Commands

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=myapp --cov-report=html

# Run specific test file
pytest tests/test_candidates.py

# Run specific test
pytest tests/test_candidates.py::test_create_candidate

# Run with verbose output
pytest tests/ -v

# Run with async mode auto (from pyproject.toml)
pytest tests/ -v

# Stop on first failure
pytest tests/ -x

# Show local variables in failures
pytest tests/ -l
```

## Test Checklist

- [ ] Test files in `tests/` directory
- [ ] Files named `test_*.py`
- [ ] Use `pytest.mark.asyncio` for async tests
- [ ] Use `AsyncClient` for endpoint tests
- [ ] Test both success and error cases
- [ ] Mock external calls when needed

## Resources

- **AGENTS.md**: See [AGENTS.md](../AGENTS.md) for project context
- **pyproject.toml**: See pytest configuration
