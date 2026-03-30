"""Evaluation entity."""

from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy import Column, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSON
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.candidate import Candidate
    from app.models.job import Job
    from app.models.tool_log import ToolLog


class EvaluationStatus(StrEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class Evaluation(SQLModel, table=True):
    __tablename__ = "evaluations"  # type: ignore[assignment]
    __table_args__ = (
        UniqueConstraint("candidate_id", "job_id", name="uq_candidate_job"),
    )

    id: int | None = Field(default=None, primary_key=True)
    candidate_id: int = Field(foreign_key="candidates.id", index=True)
    job_id: int = Field(foreign_key="jobs.id", index=True)
    status: str = Field(default=EvaluationStatus.PENDING.value)
    score: int | None = Field(default=None)
    summary: str | None = Field(default=None, sa_column=Column(Text))
    strengths: list[str] = Field(default=[], sa_column=Column(JSON))
    weaknesses: list[str] = Field(default=[], sa_column=Column(JSON))
    recommendations: list[str] = Field(default=[], sa_column=Column(JSON))
    created_at: datetime | None = Field(default=None)
    completed_at: datetime | None = Field(default=None)

    candidate: "Candidate" = Relationship(back_populates="evaluations")
    job: "Job" = Relationship(back_populates="evaluations")
    tool_logs: list["ToolLog"] = Relationship(back_populates="evaluation")
