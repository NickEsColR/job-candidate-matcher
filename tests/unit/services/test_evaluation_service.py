"""Unit tests for EvaluationService."""

from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException

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
        _result, _should_process = await evaluation_service.create_or_get_evaluation(data)

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
        result, should_process = await evaluation_service.create_or_get_evaluation(data)

        assert result.id == 42
        assert result.candidate_id == 1
        assert result.job_id == 1
        assert should_process is False

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
        result, should_process = await evaluation_service.create_or_get_evaluation(data)

        assert result.id == 1
        assert result.candidate_id == 1
        assert result.job_id == 1
        assert should_process is True

        # Verify create was called
        evaluation_repository_mock.create.assert_called_once()
        evaluation_service._session.commit.assert_called_once()  # type: ignore[attr-defined]

    @pytest.mark.asyncio
    async def test_returns_evaluation_with_pending_status(
        self, evaluation_service: EvaluationService, evaluation_repository_mock: AsyncMock
    ) -> None:
        """Test that newly created evaluations start with PENDING status."""
        evaluation_repository_mock.get_by_candidate_and_job.return_value = None
        new_evaluation = make_evaluation(
            evaluation_id=1,
            candidate_id=1,
            job_id=1,
            status=EvaluationStatus.PENDING.value,
        )
        evaluation_repository_mock.create.return_value = new_evaluation

        data = EvaluationCreate(candidate_id=1, job_id=1)
        result, should_process = await evaluation_service.create_or_get_evaluation(data)

        assert result.status == EvaluationStatus.PENDING.value
        assert should_process is True

        # Verify the created evaluation starts with PENDING status
        created_call = evaluation_repository_mock.create.call_args
        created_evaluation: Evaluation = created_call[0][0]
        assert created_evaluation.status == EvaluationStatus.PENDING.value


class TestEvaluationServiceGet:
    """Tests for get_evaluation."""

    @pytest.mark.asyncio
    async def test_returns_evaluation_when_exists(
        self, evaluation_service: EvaluationService, evaluation_repository_mock: AsyncMock
    ) -> None:
        """Should return evaluation if found by ID."""
        evaluation_repository_mock.get_by_id.return_value = make_evaluation(evaluation_id=10)

        result = await evaluation_service.get_evaluation(10)

        assert result.id == 10
        evaluation_repository_mock.get_by_id.assert_called_once_with(10)

    @pytest.mark.asyncio
    async def test_raises_404_when_evaluation_not_found(
        self, evaluation_service: EvaluationService, evaluation_repository_mock: AsyncMock
    ) -> None:
        """Should raise 404 if evaluation ID does not exist."""
        evaluation_repository_mock.get_by_id.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            await evaluation_service.get_evaluation(999)

        assert exc_info.value.status_code == 404


class TestEvaluationServiceRetryFailed:
    """Tests for reusing failed evaluations via create_or_get."""

    @pytest.mark.asyncio
    async def test_reuses_failed_evaluation_and_resets_fields(
        self, evaluation_service: EvaluationService, evaluation_repository_mock: AsyncMock
    ) -> None:
        """When existing evaluation is failed, it should reset to in_progress."""
        failed = make_evaluation(
            evaluation_id=99,
            status=EvaluationStatus.FAILED.value,
            score=10,
            summary="Old failure",
            strengths=["x"],
            weaknesses=["y"],
            recommendations=["z"],
        )
        reset = make_evaluation(
            evaluation_id=99,
            status=EvaluationStatus.IN_PROGRESS.value,
            score=None,
            summary=None,
            strengths=[],
            weaknesses=[],
            recommendations=[],
            completed_at=None,
        )
        evaluation_repository_mock.get_by_candidate_and_job.return_value = failed
        evaluation_repository_mock.update.return_value = reset

        result, should_process = await evaluation_service.create_or_get_evaluation(
            EvaluationCreate(candidate_id=1, job_id=1)
        )

        assert result.id == 99
        assert result.status == EvaluationStatus.IN_PROGRESS.value
        assert should_process is True
        evaluation_repository_mock.update.assert_called_once()
        evaluation_service._session.commit.assert_called_once()  # type: ignore[attr-defined]

    @pytest.mark.asyncio
    async def test_returns_pending_without_reprocessing_when_existing_pending(
        self, evaluation_service: EvaluationService, evaluation_repository_mock: AsyncMock
    ) -> None:
        """Pending evaluations should not retrigger analyzer on repeated POST."""
        pending = make_evaluation(
            evaluation_id=55,
            status=EvaluationStatus.PENDING.value,
        )
        evaluation_repository_mock.get_by_candidate_and_job.return_value = pending

        result, should_process = await evaluation_service.create_or_get_evaluation(
            EvaluationCreate(candidate_id=1, job_id=1)
        )

        assert result.id == 55
        assert result.status == EvaluationStatus.PENDING.value
        assert should_process is False

    @pytest.mark.asyncio
    async def test_returns_in_progress_without_reprocessing_when_existing_in_progress(
        self, evaluation_service: EvaluationService, evaluation_repository_mock: AsyncMock
    ) -> None:
        """In-progress evaluations should not retrigger analyzer on repeated POST."""
        in_progress = make_evaluation(
            evaluation_id=56,
            status=EvaluationStatus.IN_PROGRESS.value,
        )
        evaluation_repository_mock.get_by_candidate_and_job.return_value = in_progress

        result, should_process = await evaluation_service.create_or_get_evaluation(
            EvaluationCreate(candidate_id=1, job_id=1)
        )

        assert result.id == 56
        assert result.status == EvaluationStatus.IN_PROGRESS.value
        assert should_process is False


class TestEvaluationServiceProcessEvaluation:
    """Tests for analyzer execution safeguards and failure handling."""

    @pytest.mark.asyncio
    async def test_does_not_reprocess_when_in_progress(
        self, evaluation_service: EvaluationService, evaluation_repository_mock: AsyncMock
    ) -> None:
        """Should skip analyzer call when evaluation is already in progress."""
        in_progress = make_evaluation(
            evaluation_id=5,
            status=EvaluationStatus.IN_PROGRESS.value,
        )
        evaluation_repository_mock.get_by_id.return_value = in_progress

        await evaluation_service.process_evaluation(5)

        evaluation_repository_mock.update.assert_not_called()

    @pytest.mark.asyncio
    async def test_marks_failed_when_analyzer_raises(
        self, evaluation_service: EvaluationService, evaluation_repository_mock: AsyncMock
    ) -> None:
        """Should mark evaluation as failed if analyzer invocation throws."""
        pending = make_evaluation(
            evaluation_id=6,
            candidate_id=1,
            job_id=1,
            status=EvaluationStatus.PENDING.value,
        )
        failed = make_evaluation(
            evaluation_id=6,
            candidate_id=1,
            job_id=1,
            status=EvaluationStatus.FAILED.value,
        )
        evaluation_repository_mock.get_by_id.side_effect = [pending, failed]
        evaluation_repository_mock.update.side_effect = [pending, failed]

        analyzer = evaluation_service._analyzer
        analyzer.analyze.side_effect = RuntimeError("provider missing")  # type: ignore[union-attr]

        evaluation_service._candidate_repo.get_by_id.return_value = AsyncMock(  # type: ignore[attr-defined]
            skills=["Python"],
            experience=3,
        )
        evaluation_service._job_repo.get_by_id.return_value = AsyncMock(  # type: ignore[attr-defined]
            title="Backend",
            description="",
            requirements=["Python"],
        )

        await evaluation_service.process_evaluation(6)

        assert evaluation_repository_mock.update.call_count >= 2
