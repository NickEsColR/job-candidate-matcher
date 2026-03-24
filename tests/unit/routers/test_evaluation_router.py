"""Unit tests for evaluation router endpoints."""

from unittest.mock import AsyncMock

import pytest
from fastapi import status
from httpx import AsyncClient

from app.models.evaluation import EvaluationStatus
from tests.support.evaluation import evaluation_payload, make_evaluation


class TestCreateEvaluation:
    """Tests for POST /api/v1/evaluations/."""

    @pytest.mark.asyncio
    async def test_creates_new_evaluation(
        self, client: AsyncClient, mock_service: AsyncMock
    ) -> None:
        """Test that posting a new candidate/job pair creates a new evaluation."""
        evaluation = make_evaluation(evaluation_id=1, status=EvaluationStatus.PENDING.value)
        mock_service.create_or_get_evaluation.return_value = evaluation

        payload = evaluation_payload(candidate_id=1, job_id=1)
        response = await client.post("/api/v1/evaluations/", json=payload)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["id"] == 1
        assert data["candidate_id"] == 1
        assert data["job_id"] == 1
        assert data["status"] == "pending"

    @pytest.mark.asyncio
    async def test_returns_existing_evaluation(
        self, client: AsyncClient, mock_service: AsyncMock
    ) -> None:
        """Test that posting an existing candidate/job pair returns the existing evaluation."""
        # First, simulate an existing evaluation
        existing_evaluation = make_evaluation(
            evaluation_id=42,
            candidate_id=1,
            job_id=1,
            status=EvaluationStatus.PENDING.value,
        )
        mock_service.create_or_get_evaluation.return_value = existing_evaluation

        payload = evaluation_payload(candidate_id=1, job_id=1)
        response = await client.post("/api/v1/evaluations/", json=payload)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["id"] == 42
        # Verify it was called - the service should check for existing and return it
        mock_service.create_or_get_evaluation.assert_called_once()

    @pytest.mark.asyncio
    async def test_returns_422_for_invalid_payload(self, client: AsyncClient) -> None:
        """Test that missing required fields returns 422."""
        # Missing candidate_id and job_id
        response = await client.post("/api/v1/evaluations/", json={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    @pytest.mark.asyncio
    async def test_returns_422_for_invalid_candidate_id(self, client: AsyncClient) -> None:
        """Test that invalid candidate_id returns 422."""
        # candidate_id must be > 0
        response = await client.post(
            "/api/v1/evaluations/", json={"candidate_id": 0, "job_id": 1}
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    @pytest.mark.asyncio
    async def test_returns_422_for_invalid_job_id(self, client: AsyncClient) -> None:
        """Test that invalid job_id returns 422."""
        # job_id must be > 0
        response = await client.post(
            "/api/v1/evaluations/", json={"candidate_id": 1, "job_id": 0}
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
