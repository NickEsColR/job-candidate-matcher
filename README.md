# Job-Candidate-Matcher

AI-powered candidate evaluation API that analyzes candidate profiles and job descriptions to generate structured compatibility reports.

## Quick Start

### 1. Start the database

```bash
# Start PostgreSQL 17 (creates tables + seed data automatically)
docker compose up -d
```

This spins up a PostgreSQL 17 instance on `localhost:5432` and seeds it with sample candidates and jobs.

### 2. Set up environment

```bash
# Copy the example env file
cp .env.example .env

# Edit .env with your OpenAI API key
```

### 3. Install & run

```bash
# Install dependencies
uv sync

# Run the API
uv run uvicorn app.main:app --reload
```

### 4. Stop the database

```bash
docker compose down

# Or nuke everything including data
docker compose down -v
```

## Documentation

| Topic | Description |
|-------|-------------|
| [Architecture](docs/architecture.md) | System design and module breakdown |
| [Stack](docs/stack.md) | Technology choices and justifications |
| [API Endpoints](docs/api.md) | Available endpoints and models |
| [Setup](docs/setup.md) | Development environment setup |
| [Testing](docs/testing.md) | Testing patterns and conventions |

---

<div align="center">
<a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT"></a>
</div>
