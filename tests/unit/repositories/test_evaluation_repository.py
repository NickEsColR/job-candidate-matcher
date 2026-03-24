"""Unit tests for EvaluationRepository."""

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.evaluation import Evaluation, EvaluationStatus
from app.repositories.evaluation_repository import EvaluationRepository
from tests.support.evaluation import make_evaluation


class TestEvaluationRepositoryGetByCandidateAndJob:
    """Tests for get_by_candidate_and_job."""

    @pytest.mark.asyncio
    async def test_returns_none_when_not_found(
        self, evaluation_repository: EvaluationRepository
    ) -> None:
        """Test that None is returned when no evaluation exists for the pair."""
        result = await evaluation_repository.get_by_candidate_and_job(999, 999)
        assert result is None

    @pytest.mark.asyncio
    async def test_returns_evaluation_when_exists(
        self, evaluation_repository: EvaluationRepository, db_session: AsyncSession
    ) -> None:
        """Test that the existing evaluation is returned."""
        evaluation = make_evaluation(candidate_id=1, job_id=1)
        db_session.add(evaluation)
        await db_session.commit()
        await db_session.refresh(evaluation)

        result = await evaluation_repository.get_by_candidate_and_job(1, 1)
        assert result is not None
        assert result.candidate_id == 1
        assert result.job_id == 1


class TestEvaluationRepositoryCreate:
    """Tests for create."""

    @pytest.mark.asyncio
    async def test_creates_evaluation(
        self, evaluation_repository: EvaluationRepository
    ) -> None:
        """Test that creating an evaluation with a new candidate/job pair succeeds."""
        evaluation = make_evaluation(candidate_id=1, job_id=1)
        result = await evaluation_repository.create(evaluation)

        assert result.id is not None
        assert result.candidate_id == 1
        assert result.job_id == 1
        assert result.status == EvaluationStatus.PENDING.value
        assert result.created_at is not None

    @pytest.mark.asyncio
    async def test_persists_in_database(
        self, evaluation_repository: EvaluationRepository, db_session: AsyncSession
    ) -> None:
        """Test that the evaluation is persisted to the database."""
        evaluation = make_evaluation(candidate_id=1, job_id=1)
        await evaluation_repository.create(evaluation)
        await db_session.commit()

        from sqlmodel import select

        statement = select(Evaluation).where(
            Evaluation.candidate_id == 1, Evaluation.job_id == 1
        )
        db_result = await db_session.execute(statement)
        found = db_result.scalars().first()
        assert found is not None
        assert found.id is not None

    @pytest.mark.asyncio
    async def test_raises_integrity_error_on_duplicate(
        self, evaluation_repository: EvaluationRepository, db_session: AsyncSession
    ) -> None:
        """Test that creating another evaluation with the same candidate/job pair raises IntegrityError."""
        # Create first evaluation
        evaluation1 = make_evaluation(candidate_id=1, job_id=1)
        await evaluation_repository.create(evaluation1)
        await db_session.commit()

        # Try to create another evaluation with same pair - should raise IntegrityError
        evaluation2 = make_evaluation(candidate_id=1, job_id=1)
        with pytest.raises(IntegrityError):
            await evaluation_repository.create(evaluation2)
