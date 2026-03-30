"""Evaluation repository — direct database interaction."""

from datetime import datetime
from typing import Protocol, runtime_checkable

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.evaluation import Evaluation


@runtime_checkable
class EvaluationRepositoryProtocol(Protocol):
    """Protocol that any Evaluation repository implementation must satisfy."""

    async def get_by_id(self, evaluation_id: int) -> Evaluation | None: ...
    async def get_by_candidate_and_job(self, candidate_id: int, job_id: int) -> Evaluation | None: ...
    async def create(self, evaluation: Evaluation) -> Evaluation: ...
    async def update(self, evaluation: Evaluation, data: dict) -> Evaluation: ...


class EvaluationRepository:
    """SQLModel-based repository for evaluations.

    Receives an AsyncSession via constructor injection.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, evaluation_id: int) -> Evaluation | None:
        """Return a single evaluation by ID, or None."""
        return await self._session.get(Evaluation, evaluation_id)

    async def get_by_candidate_and_job(
        self, candidate_id: int, job_id: int
    ) -> Evaluation | None:
        """Return an evaluation matching the given candidate_id and job_id, or None."""
        statement = select(Evaluation).where(
            Evaluation.candidate_id == candidate_id,
            Evaluation.job_id == job_id,
        )
        result = await self._session.execute(statement)
        return result.scalars().first()

    async def create(self, evaluation: Evaluation) -> Evaluation:
        """Persist a new evaluation and refresh from DB (fills defaults)."""
        evaluation.created_at = datetime.now()
        self._session.add(evaluation)
        await self._session.flush()
        await self._session.refresh(evaluation)
        return evaluation

    async def update(self, evaluation: Evaluation, data: dict) -> Evaluation:
        """Apply partial update fields to an existing evaluation."""
        for key, value in data.items():
            setattr(evaluation, key, value)
        self._session.add(evaluation)
        await self._session.flush()
        await self._session.refresh(evaluation)
        return evaluation
