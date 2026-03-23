---
title: Stack
---

# Technology Stack

Job-Candidate-Matcher leverages modern Python technologies to build a high-performance, async-first API with robust AI capabilities.

## Core Framework

### FastAPI

- **Why**: Native async support with automatic OpenAPI documentation
- **Usage**: REST API framework with background task support
- **BackgroundTasks**: Enables non-blocking evaluation processing via `BackgroundTasks`

## Data Validation

### Pydantic v2

- **Why**: Best-in-class Python validation with excellent performance
- **Usage**: All request/response models and data schemas
- **Key Features**: Field validation, nested models, JSON schema generation

## Database

### PostgreSQL

- **Why**: Robust relational database with excellent async support
- **Usage**: Primary data store for all entities

### asyncpg

- **Why**: High-performance async PostgreSQL driver
- **Usage**: Async database connections and queries
- **Why not**: psycopg2 (synchronous only)

### SQLModel

- **Why**: SQLModel provides SQLModel (based on Pydantic + SQLAlchemy) combines ORM capabilities with Pydantic validation
- **Usage**: ORM layer for database entities
- **Key Features**: Type-safe queries, auto-generated schemas

### Alembic

- **Why**: Industry-standard database migration tool
- **Usage**: Schema versioning and migrations
- **Integration**: Works seamlessly with SQLModel

## AI Integration

### OpenAI Function Calling

- **Why**: Native support for tool/function definitions in GPT models
- **Usage**: Agent engine for structured candidate evaluation
- **Key Features**: JSON schema definitions for evaluation tools, structured outputs

## Development Tools

### Docker Compose

- **Why**: Simplified local development environment
- **Usage**: PostgreSQL container orchestration
- **Services**: API + PostgreSQL

### uv

- **Why**: Ultra-fast Python package manager with superior dependency resolution
- **Usage**: Package installation and script execution
- **Key Features**: Lock file support, virtualenv management

## Testing

### pytest

- **Why**: Standard Python testing framework
- **Usage**: Unit and integration tests

### pytest-asyncio

- **Why**: First-class async test support
- **Usage**: Testing async endpoints and background tasks

## Code Quality

### ruff

- **Why**: Extremely fast Python linter written in Rust
- **Usage**: Linting and formatting
- **Selected Rules**: E (errors), F (pyflakes), I (isort), N (naming), W (warnings), UP (pyupgrade), ANN (type annotations)

### mypy

- **Why**: Static type checker for Python
- **Usage**: Type validation and catching bugs early
- **Configuration**: Python 3.12 target, strict mode disabled

## Architecture Summary

| Layer | Technology | Purpose |
|-------|------------|---------|
| API Framework | FastAPI | REST endpoints + async |
| Validation | Pydantic v2 | Data schemas |
| Database | PostgreSQL | Persistent storage |
| ORM | SQLModel | Entity management |
| Migrations | Alembic | Schema versioning |
| AI | OpenAI | Agent evaluation |
| Testing | pytest + pytest-asyncio | Test execution |
| Linting | ruff | Code quality |
| Type Checking | mypy | Type safety |
| Container | Docker Compose | Environment |