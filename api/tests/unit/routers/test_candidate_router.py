"""Unit tests for candidate router endpoints."""

from unittest.mock import AsyncMock

import pytest
from fastapi import status
from httpx import AsyncClient

from app.models.candidate import Candidate
from tests.support.candidate import candidate_payload, make_candidate


class TestListCandidates:
    """Tests for GET /api/v1/candidates/."""

    @pytest.mark.asyncio
    async def test_returns_empty_list(self, client: AsyncClient, mock_service: AsyncMock) -> None:
        mock_service.list_candidates.return_value = []

        response = await client.get("/api/v1/candidates/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    @pytest.mark.asyncio
    async def test_returns_candidates(self, client: AsyncClient, mock_service: AsyncMock) -> None:
        candidate = make_candidate()
        mock_service.list_candidates.return_value = [candidate]

        response = await client.get("/api/v1/candidates/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "John Doe"

    @pytest.mark.asyncio
    async def test_passes_pagination_params(
        self, client: AsyncClient, mock_service: AsyncMock
    ) -> None:
        mock_service.list_candidates.return_value = []

        await client.get("/api/v1/candidates/?offset=5&limit=10")
        mock_service.list_candidates.assert_called_once_with(offset=5, limit=10)


class TestGetCandidate:
    """Tests for GET /api/v1/candidates/{candidate_id}."""

    @pytest.mark.asyncio
    async def test_returns_candidate(self, client: AsyncClient, mock_service: AsyncMock) -> None:
        candidate = make_candidate()
        mock_service.get_candidate.return_value = candidate

        response = await client.get("/api/v1/candidates/1")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["name"] == "John Doe"
        mock_service.get_candidate.assert_called_once_with(1)


class TestCreateCandidate:
    """Tests for POST /api/v1/candidates/."""

    @pytest.mark.asyncio
    async def test_creates_candidate(self, client: AsyncClient, mock_service: AsyncMock) -> None:
        candidate = make_candidate(candidate_id=1, name="Jane Doe", email="jane@test.com")
        mock_service.create_candidate.return_value = candidate

        payload = candidate_payload(name="Jane Doe", email="jane@test.com", skills=["Rust"], experience=3)
        response = await client.post("/api/v1/candidates/", json=payload)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == "Jane Doe"
        assert data["email"] == "jane@test.com"

    @pytest.mark.asyncio
    async def test_returns_422_for_invalid_payload(self, client: AsyncClient) -> None:
        # Missing required 'name' and 'email'
        response = await client.post("/api/v1/candidates/", json={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


class TestUpdateCandidate:
    """Tests for PATCH /api/v1/candidates/{candidate_id}."""

    @pytest.mark.asyncio
    async def test_updates_candidate(self, client: AsyncClient, mock_service: AsyncMock) -> None:
        candidate = make_candidate(name="Jane Updated")
        mock_service.update_candidate.return_value = candidate

        response = await client.patch("/api/v1/candidates/1", json={"name": "Jane Updated"})
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["name"] == "Jane Updated"


class TestDeleteCandidate:
    """Tests for DELETE /api/v1/candidates/{candidate_id}."""

    @pytest.mark.asyncio
    async def test_deletes_candidate(self, client: AsyncClient, mock_service: AsyncMock) -> None:
        mock_service.delete_candidate.return_value = None

        response = await client.delete("/api/v1/candidates/1")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        mock_service.delete_candidate.assert_called_once_with(1)
