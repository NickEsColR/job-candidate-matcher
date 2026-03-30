"""Evaluation DTOs for request/response serialization."""

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class EvaluationReadStatus(StrEnum):
    """API status values exposed to clients."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class EvaluationCreate(BaseModel):
    """Incoming payload to create or lookup an evaluation."""

    candidate_id: int = Field(gt=0)
    job_id: int = Field(gt=0)


class EvaluationRead(BaseModel):
    """Outgoing representation of an evaluation."""

    id: int
    candidate_id: int
    job_id: int
    status: EvaluationReadStatus
    score: int | None
    summary: str | None
    strengths: list[str]
    weaknesses: list[str]
    recommendations: list[str]
    created_at: datetime | None
    completed_at: datetime | None

    model_config = {"from_attributes": True}


# ============================================================
# Analyzer Schemas
# ============================================================


class CandidateEvaluationContext(BaseModel):
    """Context about a candidate for evaluation."""

    skills: list[str]
    experience_years: int | None = None
    education: str | None = None
    resume_text: str | None = None


class JobEvaluationContext(BaseModel):
    """Context about a job position for evaluation."""

    title: str
    description: str
    requirements: list[str]


class EvaluationAnalysisInput(BaseModel):
    """Input data for LLM-based evaluation analysis."""

    candidate: CandidateEvaluationContext
    job: JobEvaluationContext


class EvaluationAnalysis(BaseModel):
    """Analysis result from LLM evaluation."""

    score: int = Field(ge=0, le=100, description="Match score from 0 to 100")
    summary: str = Field(description="Brief summary of the evaluation")
    strengths: list[str] = Field(description="Candidate's strengths for this role")
    weaknesses: list[str] = Field(description="Candidate's weaknesses or gaps for this role")
    recommendations: list[str] = Field(description="Recommendations for improving candidate fit")
