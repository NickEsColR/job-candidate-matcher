"""Unit tests for evaluation_processor background orchestration."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.models.evaluation import EvaluationStatus
from app.services.evaluation_processor import (
    _mark_failed,
    _processing_ids,
    process_evaluation_job,
)
from tests.support.evaluation import make_evaluation


@pytest.fixture(autouse=True)
def _reset_processing_ids() -> None:
    """Clear the module-level processing set between tests to avoid state leakage."""
    _processing_ids.clear()


@pytest.fixture
def mock_session() -> AsyncMock:
    """Provide a mock async session."""
    session = AsyncMock()
    session.commit = AsyncMock()
    return session


@pytest.fixture
def mock_session_factory(mock_session: AsyncMock) -> MagicMock:
    """Provide a callable that returns an async context manager yielding the mock session.

    async_session_factory is used as:  async with async_session_factory() as session:
    So the factory must be a regular callable (not an AsyncMock) whose return value
    supports __aenter__ / __aexit__.
    """
    factory = MagicMock()
    factory.return_value.__aenter__ = AsyncMock(return_value=mock_session)
    factory.return_value.__aexit__ = AsyncMock(return_value=False)
    return factory


# ---------------------------------------------------------------------------
# _mark_failed
# ---------------------------------------------------------------------------


class TestMarkFailed:
    """Tests for the _mark_failed fallback function."""

    @pytest.mark.asyncio
    async def test_marks_evaluation_as_failed(
        self,
        mock_session_factory: MagicMock,
        mock_session: AsyncMock,
    ) -> None:
        """Should update the evaluation status to FAILED and commit."""
        pending = make_evaluation(
            evaluation_id=10,
            status=EvaluationStatus.PENDING.value,
        )
        mock_repo = AsyncMock()
        mock_repo.get_by_id.return_value = pending
        mock_repo.update.return_value = pending

        with (
            patch("app.services.evaluation_processor.async_session_factory", mock_session_factory),
            patch("app.services.evaluation_processor.EvaluationRepository", return_value=mock_repo),
        ):
            await _mark_failed(10)

        mock_repo.update.assert_called_once()
        update_call = mock_repo.update.call_args
        assert update_call[0][0] is pending
        data = update_call[0][1]
        assert data["status"] == EvaluationStatus.FAILED.value
        assert "completed_at" in data
        mock_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_skips_when_evaluation_not_found(
        self,
        mock_session_factory: MagicMock,
        mock_session: AsyncMock,
    ) -> None:
        """Should return silently if the evaluation doesn't exist."""
        mock_repo = AsyncMock()
        mock_repo.get_by_id.return_value = None

        with (
            patch("app.services.evaluation_processor.async_session_factory", mock_session_factory),
            patch("app.services.evaluation_processor.EvaluationRepository", return_value=mock_repo),
        ):
            await _mark_failed(999)

        mock_repo.update.assert_not_called()
        mock_session.commit.assert_not_called()

    @pytest.mark.asyncio
    async def test_skips_when_already_completed(
        self,
        mock_session_factory: MagicMock,
        mock_session: AsyncMock,
    ) -> None:
        """Should not overwrite a COMPLETED evaluation."""
        completed = make_evaluation(
            evaluation_id=5,
            status=EvaluationStatus.COMPLETED.value,
        )
        mock_repo = AsyncMock()
        mock_repo.get_by_id.return_value = completed

        with (
            patch("app.services.evaluation_processor.async_session_factory", mock_session_factory),
            patch("app.services.evaluation_processor.EvaluationRepository", return_value=mock_repo),
        ):
            await _mark_failed(5)

        mock_repo.update.assert_not_called()
        mock_session.commit.assert_not_called()


# ---------------------------------------------------------------------------
# process_evaluation_job
# ---------------------------------------------------------------------------


class TestProcessEvaluationJob:
    """Tests for the main background job function."""

    @pytest.mark.asyncio
    async def test_processes_evaluation_successfully(
        self,
        mock_session_factory: MagicMock,
    ) -> None:
        """Should create repositories, analyzer, service, and call process_evaluation."""
        mock_service_instance = AsyncMock()
        mock_service_instance.process_evaluation = AsyncMock()

        with (
            patch("app.services.evaluation_processor.async_session_factory", mock_session_factory),
            patch("app.services.evaluation_processor.EvaluationRepository", return_value=AsyncMock()),
            patch("app.services.evaluation_processor.CandidateRepository", return_value=AsyncMock()),
            patch("app.services.evaluation_processor.JobRepository", return_value=AsyncMock()),
            patch("app.services.evaluation_processor.LangChainEvaluationAnalyzer", return_value=AsyncMock()),
            patch("app.services.evaluation_processor.EvaluationService", return_value=mock_service_instance),
        ):
            await process_evaluation_job(1)

        mock_service_instance.process_evaluation.assert_called_once_with(1)
        assert 1 not in _processing_ids

    @pytest.mark.asyncio
    async def test_duplicate_prevention(
        self,
        mock_session_factory: MagicMock,
    ) -> None:
        """Second call with the same ID should return immediately without processing."""
        _processing_ids.add(42)

        with patch(
            "app.services.evaluation_processor.async_session_factory", mock_session_factory
        ):
            await process_evaluation_job(42)

        mock_session_factory.assert_not_called()

    @pytest.mark.asyncio
    async def test_marks_failed_on_analyzer_init_error(
        self,
        mock_session_factory: MagicMock,
        mock_session: AsyncMock,
    ) -> None:
        """Should mark evaluation as FAILED when LangChainEvaluationAnalyzer raises."""
        pending = make_evaluation(
            evaluation_id=7,
            status=EvaluationStatus.PENDING.value,
        )
        mock_eval_repo = AsyncMock()
        mock_eval_repo.get_by_id.return_value = pending
        mock_eval_repo.update.return_value = pending

        with (
            patch("app.services.evaluation_processor.async_session_factory", mock_session_factory),
            patch("app.services.evaluation_processor.EvaluationRepository", return_value=mock_eval_repo),
            patch(
                "app.services.evaluation_processor.LangChainEvaluationAnalyzer",
                side_effect=RuntimeError("provider unavailable"),
            ),
        ):
            await process_evaluation_job(7)

        mock_eval_repo.update.assert_called_once()
        update_data = mock_eval_repo.update.call_args[0][1]
        assert update_data["status"] == EvaluationStatus.FAILED.value
        mock_session.commit.assert_called_once()
        assert 7 not in _processing_ids

    @pytest.mark.asyncio
    async def test_marks_failed_on_unhandled_exception(
        self,
        mock_session_factory: MagicMock,
    ) -> None:
        """Should call _mark_failed when an unhandled exception escapes the try block."""
        mock_service = AsyncMock()
        mock_service.process_evaluation = AsyncMock(
            side_effect=RuntimeError("unexpected failure")
        )

        with (
            patch("app.services.evaluation_processor.async_session_factory", mock_session_factory),
            patch("app.services.evaluation_processor.EvaluationRepository", return_value=AsyncMock()),
            patch("app.services.evaluation_processor.CandidateRepository", return_value=AsyncMock()),
            patch("app.services.evaluation_processor.JobRepository", return_value=AsyncMock()),
            patch("app.services.evaluation_processor.LangChainEvaluationAnalyzer", return_value=AsyncMock()),
            patch("app.services.evaluation_processor.EvaluationService", return_value=mock_service),
            patch(
                "app.services.evaluation_processor._mark_failed", new_callable=AsyncMock
            ) as mock_mark_failed,
        ):
            await process_evaluation_job(3)

        mock_mark_failed.assert_called_once_with(3)
        assert 3 not in _processing_ids

    @pytest.mark.asyncio
    async def test_processing_ids_cleaned_up_on_outer_exception(
        self,
        mock_session_factory: MagicMock,
    ) -> None:
        """Even on outer exception, the evaluation ID must be removed from _processing_ids."""
        mock_service = AsyncMock()
        mock_service.process_evaluation = AsyncMock(
            side_effect=RuntimeError("boom")
        )

        with (
            patch("app.services.evaluation_processor.async_session_factory", mock_session_factory),
            patch("app.services.evaluation_processor.EvaluationRepository", return_value=AsyncMock()),
            patch("app.services.evaluation_processor.CandidateRepository", return_value=AsyncMock()),
            patch("app.services.evaluation_processor.JobRepository", return_value=AsyncMock()),
            patch("app.services.evaluation_processor.LangChainEvaluationAnalyzer", return_value=AsyncMock()),
            patch("app.services.evaluation_processor.EvaluationService", return_value=mock_service),
            patch("app.services.evaluation_processor._mark_failed", new_callable=AsyncMock),
        ):
            await process_evaluation_job(88)

        assert 88 not in _processing_ids

    @pytest.mark.asyncio
    async def test_different_ids_can_process_concurrently(
        self,
        mock_session_factory: MagicMock,
    ) -> None:
        """Different evaluation IDs should not block each other."""
        _processing_ids.add(10)

        mock_service = AsyncMock()
        mock_service.process_evaluation = AsyncMock()

        with (
            patch("app.services.evaluation_processor.async_session_factory", mock_session_factory),
            patch("app.services.evaluation_processor.EvaluationRepository", return_value=AsyncMock()),
            patch("app.services.evaluation_processor.CandidateRepository", return_value=AsyncMock()),
            patch("app.services.evaluation_processor.JobRepository", return_value=AsyncMock()),
            patch("app.services.evaluation_processor.LangChainEvaluationAnalyzer", return_value=AsyncMock()),
            patch("app.services.evaluation_processor.EvaluationService", return_value=mock_service),
        ):
            # ID 10 is already in processing_ids, but ID 20 is not
            await process_evaluation_job(20)

        mock_service.process_evaluation.assert_called_once_with(20)
