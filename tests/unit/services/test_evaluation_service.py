"""Unit tests for EvaluationService."""

from unittest.mock import AsyncMock

import pytest

from app.models.evaluation import Evaluation, EvaluationStatus
from app.schemas.evaluation import EvaluationCreate
from app.services.evaluation_service import EvaluationService
from tests.support.evaluation import make_evaluation


class TestEvaluationServiceCreateOrGet:
    """Tests for create_or_get_evaluation."""

    @pytest.mark.asyncio
    async def test_checks_for_existing_before_creating(
        self, evaluation_service: EvaluationService, evaluation_repository_mock: AsyncMock
    ) -> None:
        """Test that the service checks for an existing evaluation before creating."""
        evaluation_repository_mock.get_by_candidate_and_job.return_value = None

        data = EvaluationCreate(candidate_id=1, job_id=1)
        await evaluation_service.create_or_get_evaluation(data)

        # Verify get_by_candidate_and_job was called BEFORE create
        evaluation_repository_mock.get_by_candidate_and_job.assert_called_once_with(1, 1)
        evaluation_repository_mock.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_returns_existing_evaluation(
        self, evaluation_service: EvaluationService, evaluation_repository_mock: AsyncMock
    ) -> None:
        """Test that when an existing evaluation is found, it returns that record without calling create."""
        existing_evaluation = make_evaluation(
            evaluation_id=42, candidate_id=1, job_id=1
        )
        evaluation_repository_mock.get_by_candidate_and_job.return_value = (
            existing_evaluation
        )

        data = EvaluationCreate(candidate_id=1, job_id=1)
        result = await evaluation_service.create_or_get_evaluation(data)

        assert result.id == 42
        assert result.candidate_id == 1
        assert result.job_id == 1

        # Verify create was NOT called since we found existing
        evaluation_repository_mock.create.assert_not_called()

    @pytest.mark.asyncio
    async def test_creates_new_evaluation_when_not_found(
        self, evaluation_service: EvaluationService, evaluation_repository_mock: AsyncMock
    ) -> None:
        """Test that when no existing evaluation is found, it creates one."""
        evaluation_repository_mock.get_by_candidate_and_job.return_value = None
        new_evaluation = make_evaluation(
            evaluation_id=1, candidate_id=1, job_id=1
        )
        evaluation_repository_mock.create.return_value = new_evaluation

        data = EvaluationCreate(candidate_id=1, job_id=1)
        result = await evaluation_service.create_or_get_evaluation(data)

        assert result.id == 1
        assert result.candidate_id == 1
        assert result.job_id == 1

        # Verify create was called
        evaluation_repository_mock.create.assert_called_once()
        evaluation_service._session.commit.assert_called_once()  # type: ignore[attr-defined]

    @pytest.mark.asyncio
    async def test_returns_evaluation_with_pending_status(
        self, evaluation_service: EvaluationService, evaluation_repository_mock: AsyncMock
    ) -> None:
        """Test that newly created evaluations have PENDING status."""
        evaluation_repository_mock.get_by_candidate_and_job.return_value = None
        new_evaluation = make_evaluation(
            evaluation_id=1, candidate_id=1, job_id=1, status=EvaluationStatus.PENDING.value
        )
        evaluation_repository_mock.create.return_value = new_evaluation

        data = EvaluationCreate(candidate_id=1, job_id=1)
        result = await evaluation_service.create_or_get_evaluation(data)

        assert result.status == EvaluationStatus.PENDING.value

        # Verify the created evaluation has PENDING status
        created_call = evaluation_repository_mock.create.call_args
        created_evaluation: Evaluation = created_call[0][0]
        assert created_evaluation.status == EvaluationStatus.PENDING.value
