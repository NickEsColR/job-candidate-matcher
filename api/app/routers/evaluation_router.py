"""Evaluation router — HTTP endpoints for evaluation operations."""

from fastapi import APIRouter, BackgroundTasks, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db import get_session
from app.models.evaluation import Evaluation
from app.repositories.candidate_repository import (
    CandidateRepository,
    CandidateRepositoryProtocol,
)
from app.repositories.evaluation_repository import (
    EvaluationRepository,
    EvaluationRepositoryProtocol,
)
from app.repositories.job_repository import JobRepository, JobRepositoryProtocol
from app.schemas.evaluation import EvaluationCreate, EvaluationRead
from app.services.evaluation_processor import process_evaluation_job
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


def get_candidate_repository(
    session: AsyncSession = Depends(get_session),
) -> CandidateRepositoryProtocol:
    """Provide a CandidateRepository wired to the request session."""
    return CandidateRepository(session)


def get_job_repository(
    session: AsyncSession = Depends(get_session),
) -> JobRepositoryProtocol:
    """Provide a JobRepository wired to the request session."""
    return JobRepository(session)


def get_evaluation_service(
    repository: EvaluationRepositoryProtocol = Depends(get_evaluation_repository),
    candidate_repository: CandidateRepositoryProtocol = Depends(get_candidate_repository),
    job_repository: JobRepositoryProtocol = Depends(get_job_repository),
    session: AsyncSession = Depends(get_session),
) -> EvaluationServiceProtocol:
    """Provide an EvaluationService wired to the repository."""
    return EvaluationService(repository, candidate_repository, job_repository, session)


# ── Endpoints ───────────────────────────────────────────────────────────────


@router.post("/", response_model=EvaluationRead, status_code=status.HTTP_201_CREATED)
async def create_evaluation(
    data: EvaluationCreate,
    background_tasks: BackgroundTasks,
    service: EvaluationServiceProtocol = Depends(get_evaluation_service),
) -> Evaluation:
    """Create a new evaluation or return existing one for candidate/job pair.

    If an evaluation already exists for the given candidate_id and job_id,
    returns the existing evaluation without creating a duplicate.
    Otherwise, creates a new evaluation with PENDING status.
    """
    evaluation, should_process = await service.create_or_get_evaluation(data)

    if should_process and evaluation.id is not None:
        background_tasks.add_task(process_evaluation_job, evaluation.id)

    return evaluation


@router.get("/{evaluation_id}", response_model=EvaluationRead)
async def get_evaluation(
    evaluation_id: int,
    service: EvaluationServiceProtocol = Depends(get_evaluation_service),
) -> Evaluation:
    """Return a single evaluation by ID, including processing status."""
    return await service.get_evaluation(evaluation_id)
