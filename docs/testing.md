---
title: Testing
---

# Testing

Job-Candidate-Matcher uses pytest with pytest-asyncio for comprehensive testing of async endpoints and background tasks.

## Test Directory Structure

```
tests/
├── __init__.py
├── conftest.py           # Shared fixtures
├── test_candidates.py   # Candidate endpoint tests
├── test_jobs.py         # Job endpoint tests
├── test_evaluations.py  # Evaluation endpoint tests
└── fixtures/
    ├── candidates.json  # Test data
    └── jobs.json
```

## Test File Naming

- **Convention**: `test_*.py`
- **Location**: All tests under `tests/` directory
- **Configuration**: Defined in `pyproject.toml`

## Running Tests

### Run All Tests

```bash
uv run pytest
```

### Run with Verbose Output

```bash
uv run pytest -v
```

### Run Specific Test File

```bash
uv run pytest tests/test_candidates.py
```

### Run by Marker

```bash
pytest -m unit
pytest -m integration
```

## Pytest Configuration

Configured in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
```

## Key Patterns

### Using AsyncClient for Endpoint Testing

Use `httpx.AsyncClient` with `app` fixture to test FastAPI endpoints:

```python
from httpx import AsyncClient, ASGITransport
import pytest

@pytest.fixture
async def client(app):
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac

@pytest.mark.asyncio
async def test_create_candidate(client):
    response = await client.post(
        "/candidates",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "skills": ["Python", "FastAPI"],
            "experience": 5
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "John Doe"
```

### Testing BackgroundTasks

When testing endpoints that use `BackgroundTasks`, use the `await` pattern to ensure tasks complete:

```python
@pytest.mark.asyncio
async def test_evaluation_async(client, app):
    response = await client.post(
        "/evaluations",
        json={
            "candidate_id": 1,
            "job_id": 1
        }
    )
    assert response.status_code == 202
    
    # Background task should complete
    # Access app.state or database to verify
```

### Shared Fixtures in conftest.py

Define common fixtures in `conftest.py`:

```python
import pytest
from sqlmodel import Session, create_engine
from app.models import Candidate, Job

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Session.configure_bind(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture
def sample_candidate(db_session):
    candidate = Candidate(
        name="Test User",
        email="test@example.com",
        skills=["Python"],
        experience=3
    )
    db_session.add(candidate)
    db_session.commit()
    return candidate
```

## Test Categories

### Unit Tests

Test individual components in isolation:

```python
@pytest.mark.asyncio
async def test_skill_matching():
    # Test matching logic
    from app.agent.tools import calculate_skill_match
    
    result = calculate_skill_match(
        candidate_skills=["Python", "FastAPI"],
        job_requirements=["Python", "Django"]
    )
    assert result["match_percentage"] == 50
```

### Integration Tests

Test endpoint interactions:

```python
@pytest.mark.asyncio
async def test_full_evaluation_flow(client, db_session):
    # Create candidate
    candidate_response = await client.post(
        "/candidates",
        json={...}
    )
    
    # Create job
    job_response = await client.post(
        "/jobs",
        json={...}
    )
    
    # Create evaluation
    eval_response = await client.post(
        "/evaluations",
        json={
            "candidate_id": candidate_response.json()["id"],
            "job_id": job_response.json()["id"]
        }
    )
    assert eval_response.status_code == 202
```

## Best Practices

1. **Use descriptive test names**: `test_create_candidate_returns_201`
2. **Test one thing per test**: Avoid testing multiple assertions
3. **Use fixtures for setup**: Reuse common test data
4. **Clean up after tests**: Reset database state
5. **Assert meaningful outcomes**: Check specific fields, not just status codes
6. **Use async/await correctly**: Remember `pytest-asyncio` auto mode

## Code Coverage

Generate coverage reports:

```bash
uv run pytest --cov=src --cov-report=term-missing
```

View HTML report:

```bash
uv run pytest --cov=src --cov-report=html
# Open htmlcov/index.html in browser
```