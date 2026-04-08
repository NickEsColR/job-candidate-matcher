# Architecture

Job-Candidate-Matcher follows a layered architecture where each layer has a single responsibility and dependencies flow downward.

## Layered Architecture

```
┌──────────────────────────────────────────────────────────┐
│  Routers  (HTTP)                                         │
│  candidate_router · job_router · evaluation_router       │
│  Parse requests, validate input, return responses        │
└────────────────────────┬─────────────────────────────────┘
                         │ depends on (via DI)
                         ▼
┌──────────────────────────────────────────────────────────┐
│  Services  (Business Logic)                              │
│  candidate_service · job_service · evaluation_service    │
│  evaluation_analyzer (protocol) · evaluation_processor   │
│  Orchestrate operations, enforce rules                   │
└────────────────────────┬─────────────────────────────────┘
                         │ depends on
                         ▼
┌──────────────────────────────────────────────────────────┐
│  Repositories  (Data Access)                             │
│  candidate_repository · job_repository                   │
│  evaluation_repository                                   │
│  Query/mutate the database, return ORM entities          │
└────────────────────────┬─────────────────────────────────┘
                         │ depends on
                         ▼
┌──────────────────────────────────────────────────────────┐
│  Infrastructure  (External Concerns)                     │
│  db.py · exceptions.py · llm/                            │
│  Database engine, error translation, LLM integration     │
└──────────────────────────────────────────────────────────┘

Cross-cutting:
  core/       Settings (pydantic-settings), Logger (QueueListener)
  models/     SQLModel ORM entities (Candidate, Job, Evaluation)
  schemas/    Pydantic request/response DTOs
```

## Module Responsibilities

### `app/routers/`

HTTP endpoint definitions. Each router:
- Defines routes under a prefix (`/api/v1/candidates`, `/api/v1/jobs`, `/api/v1/evaluations`)
- Wires dependencies via FastAPI `Depends()` (session, repository, service)
- Delegates all logic to the service layer
- Returns ORM entities serialized through Pydantic response models

### `app/services/`

Business logic. Services receive repositories (not sessions) and own the commit decision.

| Service | Responsibility |
|---------|----------------|
| `CandidateService` | CRUD + email uniqueness enforcement |
| `JobService` | CRUD |
| `EvaluationService` | Create-or-get idempotency, evaluation lifecycle, LLM orchestration |
| `evaluation_analyzer` | `EvaluationAnalyzerProtocol` — interface for LLM analysis |
| `evaluation_processor` | Background job: builds dependencies, calls analyzer, persists results |

### `app/repositories/`

Data access layer. Each repository wraps a SQLAlchemy `AsyncSession` and provides typed query methods. Repositories do NOT commit — the service decides when to commit.

### `app/models/`

SQLModel ORM entities that map directly to database tables.

```
candidates                jobs
┌──────────────┐         ┌──────────────┐
│ id (PK)      │         │ id (PK)      │
│ name         │         │ title        │
│ email (uniq) │         │ description  │
│ skills (JSON)│         │ requirements │
│ experience   │         │ location     │
│ resume_url   │         │ salary_range │
│ created_at   │         │ created_at   │
└──────┬───────┘         └──────┬───────┘
       │                        │
       └────────┬───────────────┘
                ▼
         evaluations
┌──────────────────────────┐
│ id (PK)                  │
│ candidate_id (FK)        │  ← unique together (candidate_id, job_id)
│ job_id (FK)              │
│ status                   │  pending → in_progress → completed / failed
│ score (0-100)            │
│ summary                  │
│ strengths (JSON)         │
│ weaknesses (JSON)        │
│ recommendations (JSON)   │
│ created_at               │
│ completed_at             │
└──────────────────────────┘
```

### `app/schemas/`

Pydantic models for request validation and response serialization. Separate from ORM models to decouple the API contract from the database schema.

### `app/infrastructure/`

| File | Purpose |
|------|---------|
| `db.py` | Creates async engine, provides `get_session` dependency, translates SQLAlchemy errors to app exceptions |
| `exceptions.py` | App-level exception hierarchy (`DatabaseError`, `IntegrityConstraintError`, `DuplicateError`, etc.) and `detect_integrity_error` |
| `llm/evaluation_analyzer.py` | `LangChainEvaluationAnalyzer` — implements `EvaluationAnalyzerProtocol` using LangChain `init_chat_model` + `with_structured_output` |
| `llm/prompts.py` | System and user prompt templates for the LLM analyzer |

### `app/core/`

| File | Purpose |
|------|---------|
| `settings.py` | `pydantic-settings` configuration loaded from `.env` |
| `logger.py` | Non-blocking logging via `QueueHandler` + `QueueListener` |

## Evaluation Flow (Async)

This is the most complex flow in the system:

```
Client                Router              Service              Background
  │                     │                    │                     │
  │ POST /evaluations   │                    │                     │
  │────────────────────>│                    │                     │
  │                     │ create_or_get_     │                     │
  │                     │ evaluation(data)   │                     │
  │                     │───────────────────>│                     │
  │                     │                    │                     │
  │                     │  returns           │                     │
  │                     │  (evaluation,      │                     │
  │                     │   should_process)  │                     │
  │                     │<───────────────────│                     │
  │                     │                    │                     │
  │                     │ if should_process: │                     │
  │                     │ background_tasks   │                     │
  │                     │ .add_task(         │                     │
  │                     │   process_eval_    │                     │
  │                     │   job, id)         │                     │
  │  201 EvaluationRead │                    │                     │
  │<────────────────────│                    │                     │
  │                     │                    │                     │
  │                     │                    │  process_eval_      │
  │                     │                    │  job(eval_id)       │
  │                     │                    │────────────────────>│
  │                     │                    │                     │
  │                     │                    │  1. Build repos +   │
  │                     │                    │     analyzer        │
  │                     │                    │  2. Fetch candidate │
  │                     │                    │     + job data      │
  │                     │                    │  3. Call LLM        │
  │                     │                    │  4. Save results    │
  │                     │                    │  5. Update status   │
  │                     │                    │     → completed     │
  │                     │                    │                     │
  │ GET /evaluations/{id}                   │                     │
  │────────────────────>│                    │                     │
  │  200 (status + results)                 │                     │
  │<────────────────────│                    │                     │
```

Key design decisions:
- **Idempotent creation**: `POST` with the same `candidate_id` + `job_id` returns the existing evaluation
- **Retry on failure**: Re-POSTing a `failed` evaluation resets it and reprocesses
- **Duplicate prevention**: `evaluation_processor` tracks in-flight IDs to prevent concurrent reprocessing
- **Graceful fallback**: If the LLM analyzer fails, the evaluation is marked `failed` with a best-effort database update
