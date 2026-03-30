"""Evaluation service — business logic layer."""

from datetime import datetime
from typing import Protocol, runtime_checkable

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import get_logger
from app.models.evaluation import Evaluation, EvaluationStatus
from app.repositories.candidate_repository import CandidateRepositoryProtocol
from app.repositories.evaluation_repository import EvaluationRepositoryProtocol
from app.repositories.job_repository import JobRepositoryProtocol
from app.schemas.evaluation import (
    CandidateEvaluationContext,
    EvaluationAnalysisInput,
    EvaluationCreate,
    JobEvaluationContext,
)
from app.services.evaluation_analyzer import EvaluationAnalyzerProtocol

logger = get_logger(__name__)


@runtime_checkable
class EvaluationServiceProtocol(Protocol):
    """Protocol that any Evaluation service implementation must satisfy."""

    async def create_or_get_evaluation(self, data: EvaluationCreate) -> tuple[Evaluation, bool]: ...
    async def get_evaluation(self, evaluation_id: int) -> Evaluation: ...
    async def process_evaluation(self, evaluation_id: int) -> None: ...


class EvaluationService:
    """Business logic for evaluation operations.

    Receives an EvaluationRepository via constructor injection.
    """

    def __init__(
        self,
        repository: EvaluationRepositoryProtocol,
        candidate_repository: CandidateRepositoryProtocol,
        job_repository: JobRepositoryProtocol,
        session: AsyncSession,
        analyzer: EvaluationAnalyzerProtocol | None = None,
    ) -> None:
        self._repo = repository
        self._candidate_repo = candidate_repository
        self._job_repo = job_repository
        self._session = session
        self._analyzer = analyzer

    async def create_or_get_evaluation(self, data: EvaluationCreate) -> tuple[Evaluation, bool]:
        """Create a new evaluation or return existing one for candidate/job pair.

        If an evaluation already exists for the given candidate_id and job_id,
        return the existing evaluation without creating a duplicate.
        Otherwise, create a new evaluation with PENDING status.
        """
        existing = await self._repo.get_by_candidate_and_job(data.candidate_id, data.job_id)
        if existing is not None:
            if existing.status in {
                EvaluationStatus.PENDING.value,
                EvaluationStatus.IN_PROGRESS.value,
                EvaluationStatus.COMPLETED.value,
            }:
                return existing, False

            existing = await self._repo.update(
                existing,
                {
                    "status": EvaluationStatus.IN_PROGRESS.value,
                    "score": None,
                    "summary": None,
                    "strengths": [],
                    "weaknesses": [],
                    "recommendations": [],
                    "completed_at": None,
                },
            )
            await self._session.commit()
            return existing, True

        evaluation = Evaluation(
            candidate_id=data.candidate_id,
            job_id=data.job_id,
            status=EvaluationStatus.PENDING.value,
        )
        try:
            evaluation = await self._repo.create(evaluation)
            await self._session.commit()
            return evaluation, True
        except SQLAlchemyError:
            # Handle race condition on concurrent create-or-get requests.
            await self._session.rollback()
            existing = await self._repo.get_by_candidate_and_job(
                data.candidate_id, data.job_id
            )
            if existing is not None:
                return existing, False
            raise

    async def get_evaluation(self, evaluation_id: int) -> Evaluation:
        """Return a single evaluation by ID or raise 404."""
        evaluation = await self._repo.get_by_id(evaluation_id)
        if evaluation is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Evaluation with id {evaluation_id} not found",
            )
        return evaluation

    async def process_evaluation(self, evaluation_id: int) -> None:
        """Run analyzer in background and persist final evaluation status."""
        evaluation = await self._repo.get_by_id(evaluation_id)

        if evaluation is None:
            return

        if evaluation.status == EvaluationStatus.COMPLETED.value:
            return

        if evaluation.status == EvaluationStatus.IN_PROGRESS.value:
            return

        if self._analyzer is None:
            logger.error("Evaluation analyzer not configured")
            await self._repo.update(
                evaluation,
                {
                    "status": EvaluationStatus.FAILED.value,
                    "completed_at": datetime.now(),
                },
            )
            await self._session.commit()
            return

        try:
            await self._repo.update(
                evaluation,
                {
                    "status": EvaluationStatus.IN_PROGRESS.value,
                    "completed_at": None,
                },
            )
            await self._session.commit()

            candidate = await self._candidate_repo.get_by_id(evaluation.candidate_id)
            job = await self._job_repo.get_by_id(evaluation.job_id)

            if candidate is None or job is None:
                await self._repo.update(
                    evaluation,
                    {
                        "status": EvaluationStatus.FAILED.value,
                        "completed_at": datetime.now(),
                    },
                )
                await self._session.commit()
                return

            analysis_input = EvaluationAnalysisInput(
                candidate=CandidateEvaluationContext(
                    skills=candidate.skills,
                    experience_years=candidate.experience,
                    education=None,
                    resume_text=None,
                ),
                job=JobEvaluationContext(
                    title=job.title,
                    description=job.description or "",
                    requirements=job.requirements,
                ),
            )

            analysis = await self._analyzer.analyze(analysis_input)

            await self._repo.update(
                evaluation,
                {
                    "status": EvaluationStatus.COMPLETED.value,
                    "score": analysis.score,
                    "summary": analysis.summary,
                    "strengths": analysis.strengths,
                    "weaknesses": analysis.weaknesses,
                    "recommendations": analysis.recommendations,
                    "completed_at": datetime.now(),
                },
            )
            await self._session.commit()
        except Exception as exc:
            await self._session.rollback()
            failed_evaluation = await self._repo.get_by_id(evaluation_id)
            if failed_evaluation is None:
                return
            logger.exception("Evaluation processing failed", exc_info=exc)
            await self._repo.update(
                failed_evaluation,
                {
                    "status": EvaluationStatus.FAILED.value,
                    "completed_at": datetime.now(),
                },
            )
            await self._session.commit()
