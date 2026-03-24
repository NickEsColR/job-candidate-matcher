"""Evaluation service — business logic layer."""

from typing import Protocol, runtime_checkable

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.evaluation import Evaluation, EvaluationStatus
from app.repositories.evaluation_repository import EvaluationRepositoryProtocol
from app.schemas.evaluation import EvaluationCreate


@runtime_checkable
class EvaluationServiceProtocol(Protocol):
    """Protocol that any Evaluation service implementation must satisfy."""

    async def create_or_get_evaluation(self, data: EvaluationCreate) -> Evaluation: ...


class EvaluationService:
    """Business logic for evaluation operations.

    Receives an EvaluationRepository via constructor injection.
    """

    def __init__(
        self,
        repository: EvaluationRepositoryProtocol,
        session: AsyncSession,
    ) -> None:
        self._repo = repository
        self._session = session

    async def create_or_get_evaluation(self, data: EvaluationCreate) -> Evaluation:
        """Create a new evaluation or return existing one for candidate/job pair.

        If an evaluation already exists for the given candidate_id and job_id,
        return the existing evaluation without creating a duplicate.
        Otherwise, create a new evaluation with PENDING status.
        """
        # Check if evaluation already exists
        existing = await self._repo.get_by_candidate_and_job(
            data.candidate_id, data.job_id
        )
        if existing is not None:
            return existing

        # Create new evaluation
        evaluation = Evaluation(
            candidate_id=data.candidate_id,
            job_id=data.job_id,
            status=EvaluationStatus.PENDING.value,
        )
        evaluation = await self._repo.create(evaluation)
        await self._session.commit()
        return evaluation
