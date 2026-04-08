"""Router test fixtures."""

from collections.abc import AsyncGenerator
from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
def mock_service() -> AsyncMock:
    """Provide a mock candidate service for router tests."""
    mock = AsyncMock()
    mock.list_candidates = AsyncMock(return_value=[])
    mock.get_candidate = AsyncMock()
    mock.create_candidate = AsyncMock()
    mock.update_candidate = AsyncMock()
    mock.delete_candidate = AsyncMock()
    mock.list_jobs = AsyncMock(return_value=[])
    mock.get_job = AsyncMock()
    mock.create_job = AsyncMock()
    mock.update_job = AsyncMock()
    mock.delete_job = AsyncMock()
    mock.create_or_get_evaluation = AsyncMock()
    mock.get_evaluation = AsyncMock()
    mock.process_evaluation = AsyncMock()
    return mock


@pytest.fixture
async def client(mock_service: AsyncMock) -> AsyncGenerator[AsyncClient, None]:
    """Provide an HTTP client wired with dependency overrides."""
    from app.routers.candidate_router import get_candidate_service
    from app.routers.evaluation_router import get_evaluation_service
    from app.routers.job_router import get_job_service

    app.dependency_overrides[get_candidate_service] = lambda: mock_service
    app.dependency_overrides[get_job_service] = lambda: mock_service
    app.dependency_overrides[get_evaluation_service] = lambda: mock_service

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()
