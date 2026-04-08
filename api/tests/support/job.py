"""Shared job builders for tests."""

from datetime import datetime, timezone

from app.models.job import Job


def make_job(
    *,
    job_id: int = 1,
    title: str = "Backend Engineer",
    description: str | None = "Build APIs",
    requirements: list[str] | None = None,
    location: str | None = "Remote",
    salary_range: str | None = "$80k-$120k",
    created_at: datetime | None = None,
) -> Job:
    """Build a job model for tests."""
    return Job(
        id=job_id,
        title=title,
        description=description,
        requirements=requirements or ["Python", "FastAPI"],
        location=location,
        salary_range=salary_range,
        created_at=created_at or datetime(2025, 1, 15, 10, 30, tzinfo=timezone.utc),
    )


def job_payload(
    *,
    title: str = "Backend Engineer",
    description: str | None = "Build APIs",
    requirements: list[str] | None = None,
    location: str | None = "Remote",
    salary_range: str | None = "$80k-$120k",
) -> dict[str, object]:
    """Build a JSON payload for job endpoints."""
    return {
        "title": title,
        "description": description,
        "requirements": requirements or ["Python", "FastAPI"],
        "location": location,
        "salary_range": salary_range,
    }
