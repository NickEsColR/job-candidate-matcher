"""Unit tests for CandidateService."""

from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException

from app.schemas.candidate import CandidateCreate, CandidateUpdate
from app.services.candidate_service import CandidateService
from tests.support.candidate import make_candidate


class TestCandidateServiceListCandidates:
    """Tests for list_candidates."""

    @pytest.mark.asyncio
    async def test_returns_list(self, candidate_service: CandidateService, mock_repository: AsyncMock) -> None:
        mock_repository.get_all.return_value = [make_candidate()]

        result = await candidate_service.list_candidates()
        assert len(result) == 1
        mock_repository.get_all.assert_called_once_with(offset=0, limit=100)

    @pytest.mark.asyncio
    async def test_passes_pagination_params(
        self, candidate_service: CandidateService, mock_repository: AsyncMock
    ) -> None:
        mock_repository.get_all.return_value = []

        await candidate_service.list_candidates(offset=10, limit=5)
        mock_repository.get_all.assert_called_once_with(offset=10, limit=5)


class TestCandidateServiceGetCandidate:
    """Tests for get_candidate."""

    @pytest.mark.asyncio
    async def test_returns_candidate_when_found(
        self, candidate_service: CandidateService, mock_repository: AsyncMock
    ) -> None:
        mock_repository.get_by_id.return_value = make_candidate()

        result = await candidate_service.get_candidate(1)
        assert result.id == 1
        mock_repository.get_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_raises_404_when_not_found(
        self, candidate_service: CandidateService, mock_repository: AsyncMock
    ) -> None:
        mock_repository.get_by_id.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            await candidate_service.get_candidate(999)
        assert exc_info.value.status_code == 404
        assert "999" in exc_info.value.detail


class TestCandidateServiceCreateCandidate:
    """Tests for create_candidate."""

    @pytest.mark.asyncio
    async def test_creates_candidate(
        self, candidate_service: CandidateService, mock_repository: AsyncMock
    ) -> None:
        mock_repository.get_by_email.return_value = None
        mock_repository.create.return_value = make_candidate()

        data = CandidateCreate(name="John Doe", email="john@test.com", skills=["Python"])
        result = await candidate_service.create_candidate(data)

        assert result.name == "John Doe"
        mock_repository.create.assert_called_once()
        candidate_service._session.commit.assert_called_once()  # type: ignore[attr-defined]

    @pytest.mark.asyncio
    async def test_raises_409_when_email_exists(
        self, candidate_service: CandidateService, mock_repository: AsyncMock
    ) -> None:
        mock_repository.get_by_email.return_value = make_candidate()

        data = CandidateCreate(name="Jane", email="john@test.com")
        with pytest.raises(HTTPException) as exc_info:
            await candidate_service.create_candidate(data)
        assert exc_info.value.status_code == 409
        assert "already exists" in exc_info.value.detail


class TestCandidateServiceUpdateCandidate:
    """Tests for update_candidate."""

    @pytest.mark.asyncio
    async def test_updates_candidate(
        self, candidate_service: CandidateService, mock_repository: AsyncMock
    ) -> None:
        existing = make_candidate()
        mock_repository.get_by_id.return_value = existing
        mock_repository.update.return_value = make_candidate(name="Jane Doe")

        data = CandidateUpdate(name="Jane Doe")
        result = await candidate_service.update_candidate(1, data)

        assert result.name == "Jane Doe"
        mock_repository.update.assert_called_once()
        candidate_service._session.commit.assert_called_once()  # type: ignore[attr-defined]

    @pytest.mark.asyncio
    async def test_raises_404_when_candidate_not_found(
        self, candidate_service: CandidateService, mock_repository: AsyncMock
    ) -> None:
        mock_repository.get_by_id.return_value = None

        data = CandidateUpdate(name="Jane")
        with pytest.raises(HTTPException) as exc_info:
            await candidate_service.update_candidate(999, data)
        assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_raises_409_when_email_taken_by_other(
        self, candidate_service: CandidateService, mock_repository: AsyncMock
    ) -> None:
        existing = make_candidate(candidate_id=1)
        other = make_candidate(candidate_id=2)
        other.email = "taken@test.com"

        mock_repository.get_by_id.return_value = existing
        mock_repository.get_by_email.return_value = other

        data = CandidateUpdate(email="taken@test.com")
        with pytest.raises(HTTPException) as exc_info:
            await candidate_service.update_candidate(1, data)
        assert exc_info.value.status_code == 409

    @pytest.mark.asyncio
    async def test_allows_same_email_update(
        self, candidate_service: CandidateService, mock_repository: AsyncMock
    ) -> None:
        existing = make_candidate()
        mock_repository.get_by_id.return_value = existing
        mock_repository.update.return_value = existing

        # Updating with same email should NOT call get_by_email
        data = CandidateUpdate(email="john@test.com")
        result = await candidate_service.update_candidate(1, data)

        mock_repository.get_by_email.assert_not_called()
        assert result.email == "john@test.com"


class TestCandidateServiceDeleteCandidate:
    """Tests for delete_candidate."""

    @pytest.mark.asyncio
    async def test_deletes_candidate(
        self, candidate_service: CandidateService, mock_repository: AsyncMock
    ) -> None:
        mock_repository.get_by_id.return_value = make_candidate()

        await candidate_service.delete_candidate(1)
        mock_repository.delete.assert_called_once()
        candidate_service._session.commit.assert_called_once()  # type: ignore[attr-defined]

    @pytest.mark.asyncio
    async def test_raises_404_when_not_found(
        self, candidate_service: CandidateService, mock_repository: AsyncMock
    ) -> None:
        mock_repository.get_by_id.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            await candidate_service.delete_candidate(999)
        assert exc_info.value.status_code == 404
