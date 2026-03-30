# API - AI Agent Ruleset

> **Skills Reference**: For detailed patterns, use these skills:
> - [`pytest`](../skills/pytest/SKILL.md) - Testing patterns with pytest and pytest-asyncio
> - [`langchain-agents`](../skills/langchain-agents/SKILL.md) - LangChain v1 agent patterns
> - [`langchain-agent-architecture`](../skills/langchain-agent-architecture/SKILL.md) - Architecture decisions for agents
> - [`langchain-tests`](../skills/langchain-tests/SKILL.md) - Testing LangChain agents and tools
> - [`uv-python`](../skills/uv-python/SKILL.md) - Package management with uv
> - [`git-commit`](../skills/git-commit/SKILL.md) - Conventional commits

### Auto-invoke Skills

When performing these actions, ALWAYS invoke the corresponding skill FIRST:

| Action | Skill |
|--------|-------|
| Writing Python tests with pytest | `pytest` |
| Writing tests for LangChain agents/tools | `langchain-tests` |
| Creating a git commit | `git-commit` |
| Working with Python packages (install, sync, run) | `uv-python` |
| Designing LangChain agent architecture | `langchain-agent-architecture` |
| Creating or modifying LangChain agents | `langchain-agents` |

---

## CRITICAL RULES — NON-NEGOTIABLE

### Models (SQLModel)

- ALWAYS: Use `SQLModel` with `table=True`, explicit `__tablename__`
- ALWAYS: `id: int | None = Field(default=None, primary_key=True)`
- ALWAYS: Add `created_at` timestamp field
- ALWAYS: Use `TYPE_CHECKING` block for relationship imports
- NEVER: Import relationship types at module level (causes circular imports)

### Repositories

- ALWAYS: Define a `Protocol` class first, then the concrete implementation
- ALWAYS: Inject `AsyncSession` via constructor
- ALWAYS: Use `select()` from SQLAlchemy, not raw queries
- NEVER: Business logic in repositories (only data access)

### Services

- ALWAYS: Depend on repository protocols, not concrete classes
- ALWAYS: Inject `AsyncSession` for multi-entity transactions
- ALWAYS: Handle domain validation and business rules here
- NEVER: Import from `infrastructure` directly (use protocols)

### Routers

- ALWAYS: Use `APIRouter` with `prefix` and `tags`
- ALWAYS: Use `Depends()` for repository and service injection
- ALWAYS: Return domain models, let `response_model` handle serialization
- NEVER: Business logic in routers (delegate to services)

### Schemas (Pydantic)

- ALWAYS: Separate schemas for Create / Read / Update operations
- ALWAYS: Use `model_config = ConfigDict(from_attributes=True)` for Read schemas
- NEVER: Put database logic in schemas

---

## DECISION TREES

### Adding a new entity

```
1. Create model in app/models/<entity>.py
2. Create schemas in app/schemas/<entity>.py (Create, Read, Update)
3. Create repository protocol + implementation in app/repositories/<entity>_repository.py
4. Create service protocol + implementation in app/services/<entity>_service.py
5. Create router in app/routers/<entity>_router.py
6. Register router in app/main.py
7. Create migration if using Alembic
8. Write tests (unit + integration)
```

### Where does this code go?

```
Data access / DB queries?    → Repository
Business rules / validation? → Service
HTTP handling / response?    → Router
Data shape / serialization?  → Schema
External API call (LLM)?     → Service or tools/
Configuration?               → core/settings.py
```

### Testing strategy

```
Testing a repository?  → Use aiosqlite in-memory + async session fixture
Testing a service?     → Mock the repository protocol
Testing a router?      → Use AsyncClient + override Depends
Testing an LLM agent?  → Mock the LLM client, test tool invocation
```

---

## PROJECT STRUCTURE

```
api/
├── app/
│   ├── core/              # Settings, logger
│   ├── infrastructure/    # DB connection, exceptions, LLM clients
│   ├── models/            # SQLModel entities
│   ├── repositories/      # Data access (Protocol + Implementation)
│   ├── schemas/           # Pydantic schemas (Create/Read/Update)
│   ├── services/          # Business logic
│   ├── routers/           # HTTP endpoints
│   └── tools/             # LangChain tools
├── tests/
│   ├── unit/              # Isolated tests (mocked dependencies)
│   └── integration/       # Tests with real DB (aiosqlite)
├── pyproject.toml
└── uv.lock
```

---

## COMMANDS

```bash
# Development
cd api
uv sync --extra dev
uv run uvicorn app.main:app --reload

# Testing & Quality
uv run pytest
uv run pytest --cov=app --cov-report=term-missing
uv run ruff check . --fix
uv run ruff format .

# Package management
uv add <package>
uv remove <package>
uv lock
```

---

## NAMING CONVENTIONS

| Entity | Pattern | Example |
|--------|---------|---------|
| Model | `<Entity>` (PascalCase) | `Candidate` |
| Schema (read) | `<Entity>Read` | `CandidateRead` |
| Schema (create) | `<Entity>Create` | `CandidateCreate` |
| Schema (update) | `<Entity>Update` | `CandidateUpdate` |
| Repository | `<Entity>Repository` / `<Entity>RepositoryProtocol` | `CandidateRepository` |
| Service | `<Entity>Service` / `<Entity>ServiceProtocol` | `CandidateService` |
| Router | `<entity>_router.py` | `candidate_router.py` |
| Test | `test_<entity>_<layer>.py` | `test_candidate_service.py` |

---

## PATTERNS

### Repository with Protocol

```python
from typing import Protocol

class CandidateRepositoryProtocol(Protocol):
    async def get_by_id(self, candidate_id: int) -> Candidate | None: ...
    async def list_all(self, offset: int, limit: int) -> list[Candidate]: ...

class CandidateRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, candidate_id: int) -> Candidate | None:
        return await self._session.get(Candidate, candidate_id)
```

### Service with DI

```python
class CandidateServiceProtocol(Protocol):
    async def get_candidate(self, candidate_id: int) -> Candidate: ...

class CandidateService:
    def __init__(
        self,
        repository: CandidateRepositoryProtocol,
        session: AsyncSession,
    ) -> None:
        self._repo = repository
        self._session = session

    async def get_candidate(self, candidate_id: int) -> Candidate:
        candidate = await self._repo.get_by_id(candidate_id)
        if not candidate:
            raise NotFoundError(f"Candidate {candidate_id} not found")
        return candidate
```

### Router with Depends

```python
router = APIRouter(prefix="/api/v1/candidates", tags=["candidates"])

def get_candidate_service(
    session: AsyncSession = Depends(get_session),
) -> CandidateServiceProtocol:
    return CandidateService(CandidateRepository(session), session)

@router.get("/{candidate_id}", response_model=CandidateRead)
async def get_candidate(
    candidate_id: int,
    service: CandidateServiceProtocol = Depends(get_candidate_service),
) -> Candidate:
    return await service.get_candidate(candidate_id)
```

---

## QA CHECKLIST BEFORE COMMIT

- [ ] `uv run pytest` passes
- [ ] `uv run ruff check .` passes
- [ ] `uv run ruff format .` applied
- [ ] New endpoints have proper response_model and status_code
- [ ] Protocols are defined for new repositories and services
- [ ] Tests cover success and error cases
- [ ] No hardcoded secrets or config (use settings.py)
- [ ] TYPE_CHECKING used for relationship imports
