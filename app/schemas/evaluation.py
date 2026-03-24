"""Evaluation DTOs for request/response serialization."""

from datetime import datetime

from pydantic import BaseModel, Field


class EvaluationCreate(BaseModel):
    """Incoming payload to create or lookup an evaluation."""

    candidate_id: int = Field(gt=0)
    job_id: int = Field(gt=0)


class EvaluationRead(BaseModel):
    """Outgoing representation of an evaluation."""

    id: int
    candidate_id: int
    job_id: int
    status: str
    score: int | None
    summary: str | None
    strengths: list[str]
    weaknesses: list[str]
    recommendations: list[str]
    created_at: datetime | None
    completed_at: datetime | None

    model_config = {"from_attributes": True}
