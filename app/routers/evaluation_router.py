"""Evaluation router — HTTP endpoints for evaluation operations."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db import get_session
from app.models.evaluation import Evaluation
from app.repositories.evaluation_repository import (
    EvaluationRepository,
    EvaluationRepositoryProtocol,
)
from app.schemas.evaluation import EvaluationCreate, EvaluationRead
from app.services.evaluation_service import (
    EvaluationService,
    EvaluationServiceProtocol,
)

router = APIRouter(prefix="/api/v1/evaluations", tags=["evaluations"])


# ── Dependency providers ──────────────────────────────────────────────────────


def get_evaluation_repository(
    session: AsyncSession = Depends(get_session),
) -> EvaluationRepositoryProtocol:
    """Provide an EvaluationRepository wired to the request session."""
    return EvaluationRepository(session)


def get_evaluation_service(
    repository: EvaluationRepositoryProtocol = Depends(get_evaluation_repository),
    session: AsyncSession = Depends(get_session),
) -> EvaluationServiceProtocol:
    """Provide an EvaluationService wired to the repository."""
    return EvaluationService(repository, session)


# ── Endpoints ───────────────────────────────────────────────────────────────


@router.post("/", response_model=EvaluationRead, status_code=status.HTTP_201_CREATED)
async def create_evaluation(
    data: EvaluationCreate,
    service: EvaluationServiceProtocol = Depends(get_evaluation_service),
) -> Evaluation:
    """Create a new evaluation or return existing one for candidate/job pair.

    If an evaluation already exists for the given candidate_id and job_id,
    returns the existing evaluation without creating a duplicate.
    Otherwise, creates a new evaluation with PENDING status.
    """
    return await service.create_or_get_evaluation(data)
