"""Shared evaluation builders for tests."""

from datetime import datetime, timezone

from app.models.evaluation import Evaluation, EvaluationStatus


def make_evaluation(
    *,
    evaluation_id: int = 1,
    candidate_id: int = 1,
    job_id: int = 1,
    status: str = EvaluationStatus.PENDING.value,
    score: int | None = None,
    summary: str | None = None,
    strengths: list[str] | None = None,
    weaknesses: list[str] | None = None,
    recommendations: list[str] | None = None,
    created_at: datetime | None = None,
    completed_at: datetime | None = None,
) -> Evaluation:
    """Build an evaluation model for tests."""
    return Evaluation(
        id=evaluation_id,
        candidate_id=candidate_id,
        job_id=job_id,
        status=status,
        score=score,
        summary=summary,
        strengths=strengths or [],
        weaknesses=weaknesses or [],
        recommendations=recommendations or [],
        created_at=created_at or datetime(2025, 1, 15, 10, 30, tzinfo=timezone.utc),
        completed_at=completed_at,
    )


def evaluation_payload(
    *,
    candidate_id: int = 1,
    job_id: int = 1,
) -> dict[str, object]:
    """Build a JSON payload for evaluation endpoints."""
    return {
        "candidate_id": candidate_id,
        "job_id": job_id,
    }
