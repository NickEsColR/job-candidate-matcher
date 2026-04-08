"""Unit tests for job router endpoints."""

from unittest.mock import AsyncMock

import pytest
from fastapi import status
from httpx import AsyncClient

from tests.support.job import job_payload, make_job


class TestListJobs:
    @pytest.mark.asyncio
    async def test_returns_empty_list(self, client: AsyncClient, mock_service: AsyncMock) -> None:
        mock_service.list_jobs.return_value = []

        response = await client.get("/api/v1/jobs/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []


class TestGetJob:
    @pytest.mark.asyncio
    async def test_returns_job(self, client: AsyncClient, mock_service: AsyncMock) -> None:
        mock_service.get_job.return_value = make_job()

        response = await client.get("/api/v1/jobs/1")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["title"] == "Backend Engineer"
        mock_service.get_job.assert_called_once_with(1)


class TestCreateJob:
    @pytest.mark.asyncio
    async def test_creates_job(self, client: AsyncClient, mock_service: AsyncMock) -> None:
        mock_service.create_job.return_value = make_job(title="Backend Engineer")

        response = await client.post("/api/v1/jobs/", json=job_payload())
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["title"] == "Backend Engineer"


class TestUpdateJob:
    @pytest.mark.asyncio
    async def test_updates_job(self, client: AsyncClient, mock_service: AsyncMock) -> None:
        mock_service.update_job.return_value = make_job(title="Senior Backend Engineer")

        response = await client.patch("/api/v1/jobs/1", json={"title": "Senior Backend Engineer"})
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["title"] == "Senior Backend Engineer"


class TestDeleteJob:
    @pytest.mark.asyncio
    async def test_deletes_job(self, client: AsyncClient, mock_service: AsyncMock) -> None:
        mock_service.delete_job.return_value = None

        response = await client.delete("/api/v1/jobs/1")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        mock_service.delete_job.assert_called_once_with(1)
