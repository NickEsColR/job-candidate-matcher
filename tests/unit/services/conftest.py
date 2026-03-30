"""Service test fixtures."""

from unittest.mock import AsyncMock

import pytest

from app.services.candidate_service import CandidateService
from app.services.evaluation_service import EvaluationService
from app.services.job_service import JobService


@pytest.fixture
def mock_repository() -> AsyncMock:
    """Provide a mock repository for service tests."""
    mock = AsyncMock()
    mock.get_all = AsyncMock(return_value=[])
    mock.get_by_id = AsyncMock(return_value=None)
    mock.get_by_email = AsyncMock(return_value=None)
    mock.create = AsyncMock()
    mock.update = AsyncMock()
    mock.delete = AsyncMock()
    return mock


@pytest.fixture
def candidate_service(mock_repository: AsyncMock) -> CandidateService:
    """Provide the candidate service with mocked repository and session."""
    mock_session = AsyncMock()
    mock_session.commit = AsyncMock()
    return CandidateService(mock_repository, mock_session)


@pytest.fixture
def job_repository() -> AsyncMock:
    """Provide a mock repository for job service tests."""
    mock = AsyncMock()
    mock.get_all = AsyncMock(return_value=[])
    mock.get_by_id = AsyncMock(return_value=None)
    mock.create = AsyncMock()
    mock.update = AsyncMock()
    mock.delete = AsyncMock()
    return mock


@pytest.fixture
def job_service(job_repository: AsyncMock) -> JobService:
    """Provide the job service with mocked repository and session."""
    mock_session = AsyncMock()
    mock_session.commit = AsyncMock()
    return JobService(job_repository, mock_session)


@pytest.fixture
def evaluation_repository_mock() -> AsyncMock:
    """Provide a mock repository for evaluation service tests."""
    mock = AsyncMock()
    mock.get_by_id = AsyncMock(return_value=None)
    mock.get_by_candidate_and_job = AsyncMock(return_value=None)
    mock.create = AsyncMock()
    mock.update = AsyncMock()
    return mock


@pytest.fixture
def evaluation_service(evaluation_repository_mock: AsyncMock) -> EvaluationService:
    """Provide the evaluation service with mocked repository and session."""
    mock_session = AsyncMock()
    mock_session.commit = AsyncMock()
    mock_analyzer = AsyncMock()
    mock_analyzer.analyze = AsyncMock()
    mock_candidate_repository = AsyncMock()
    mock_candidate_repository.get_by_id = AsyncMock(return_value=None)
    mock_job_repository = AsyncMock()
    mock_job_repository.get_by_id = AsyncMock(return_value=None)
    return EvaluationService(
        evaluation_repository_mock,
        mock_candidate_repository,
        mock_job_repository,
        mock_session,
        analyzer=mock_analyzer,
    )
