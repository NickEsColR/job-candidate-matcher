"""Unit tests for JobService."""

from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException

from app.schemas.job import JobCreate, JobUpdate
from app.services.job_service import JobService
from tests.support.job import make_job


class TestJobServiceListJobs:
    @pytest.mark.asyncio
    async def test_returns_list(self, job_service: JobService, job_repository: AsyncMock) -> None:
        job_repository.get_all.return_value = [make_job()]

        result = await job_service.list_jobs()
        assert len(result) == 1
        job_repository.get_all.assert_called_once_with(offset=0, limit=100)


class TestJobServiceGetJob:
    @pytest.mark.asyncio
    async def test_returns_job_when_found(self, job_service: JobService, job_repository: AsyncMock) -> None:
        job_repository.get_by_id.return_value = make_job()

        result = await job_service.get_job(1)
        assert result.id == 1
        job_repository.get_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_raises_404_when_not_found(self, job_service: JobService, job_repository: AsyncMock) -> None:
        job_repository.get_by_id.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            await job_service.get_job(999)
        assert exc_info.value.status_code == 404


class TestJobServiceCreateJob:
    @pytest.mark.asyncio
    async def test_creates_job(self, job_service: JobService, job_repository: AsyncMock) -> None:
        job_repository.create.return_value = make_job()

        data = JobCreate(title="Backend Engineer", description="Build APIs")
        result = await job_service.create_job(data)

        assert result.title == "Backend Engineer"
        job_repository.create.assert_called_once()
        job_service._session.commit.assert_called_once()  # type: ignore[attr-defined]


class TestJobServiceUpdateJob:
    @pytest.mark.asyncio
    async def test_updates_job(self, job_service: JobService, job_repository: AsyncMock) -> None:
        existing = make_job()
        job_repository.get_by_id.return_value = existing
        job_repository.update.return_value = make_job(title="Senior Backend Engineer")

        data = JobUpdate(title="Senior Backend Engineer")
        result = await job_service.update_job(1, data)

        assert result.title == "Senior Backend Engineer"
        job_repository.update.assert_called_once()
        job_service._session.commit.assert_called_once()  # type: ignore[attr-defined]

    @pytest.mark.asyncio
    async def test_raises_404_when_job_not_found(self, job_service: JobService, job_repository: AsyncMock) -> None:
        job_repository.get_by_id.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            await job_service.update_job(999, JobUpdate(title="X"))
        assert exc_info.value.status_code == 404


class TestJobServiceDeleteJob:
    @pytest.mark.asyncio
    async def test_deletes_job(self, job_service: JobService, job_repository: AsyncMock) -> None:
        job_repository.get_by_id.return_value = make_job()

        await job_service.delete_job(1)
        job_repository.delete.assert_called_once()
        job_service._session.commit.assert_called_once()  # type: ignore[attr-defined]

    @pytest.mark.asyncio
    async def test_raises_404_when_not_found(self, job_service: JobService, job_repository: AsyncMock) -> None:
        job_repository.get_by_id.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            await job_service.delete_job(999)
        assert exc_info.value.status_code == 404
