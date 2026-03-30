"""Shared candidate builders for tests."""

from datetime import datetime, timezone

from app.models.candidate import Candidate


def make_candidate(
    *,
    candidate_id: int = 1,
    name: str = "John Doe",
    email: str = "john@test.com",
    skills: list[str] | None = None,
    experience: int = 5,
    resume_url: str | None = None,
    created_at: datetime | None = None,
) -> Candidate:
    """Build a candidate model for tests."""
    return Candidate(
        id=candidate_id,
        name=name,
        email=email,
        skills=skills or ["Python"],
        experience=experience,
        resume_url=resume_url,
        created_at=created_at or datetime(2025, 1, 15, 10, 30, tzinfo=timezone.utc),
    )


def candidate_payload(
    *,
    name: str = "John Doe",
    email: str = "john@test.com",
    skills: list[str] | None = None,
    experience: int = 5,
    resume_url: str | None = None,
) -> dict[str, object]:
    """Build a JSON payload for candidate endpoints."""
    return {
        "name": name,
        "email": email,
        "skills": skills or ["Python", "FastAPI"],
        "experience": experience,
        "resume_url": resume_url,
    }
