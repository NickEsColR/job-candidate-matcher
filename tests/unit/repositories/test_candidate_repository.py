"""Unit tests for CandidateRepository."""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.candidate import Candidate
from app.repositories.candidate_repository import CandidateRepository
from tests.support.candidate import make_candidate


class TestCandidateRepositoryGetAll:
    """Tests for get_all."""

    @pytest.mark.asyncio
    async def test_returns_empty_list_when_no_candidates(
        self, candidate_repository: CandidateRepository
    ) -> None:
        result = await candidate_repository.get_all()
        assert result == []

    @pytest.mark.asyncio
    async def test_returns_candidates(
        self, candidate_repository: CandidateRepository, db_session: AsyncSession
    ) -> None:
        db_session.add(make_candidate(name="Alice", email="alice@test.com"))
        db_session.add(make_candidate(candidate_id=2, name="Bob", email="bob@test.com"))
        await db_session.commit()

        result = await candidate_repository.get_all()
        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_respects_offset_and_limit(
        self, candidate_repository: CandidateRepository, db_session: AsyncSession
    ) -> None:
        for i in range(5):
            db_session.add(
                make_candidate(candidate_id=i + 1, name=f"User{i}", email=f"user{i}@test.com")
            )
        await db_session.commit()

        result = await candidate_repository.get_all(offset=1, limit=2)
        assert len(result) == 2


class TestCandidateRepositoryGetById:
    """Tests for get_by_id."""

    @pytest.mark.asyncio
    async def test_returns_none_for_missing_id(
        self, candidate_repository: CandidateRepository
    ) -> None:
        result = await candidate_repository.get_by_id(999)
        assert result is None

    @pytest.mark.asyncio
    async def test_returns_candidate(
        self, candidate_repository: CandidateRepository, db_session: AsyncSession
    ) -> None:
        candidate = make_candidate()
        db_session.add(candidate)
        await db_session.commit()
        await db_session.refresh(candidate)

        result = await candidate_repository.get_by_id(candidate.id)  # type: ignore[arg-type]
        assert result is not None
        assert result.name == "John Doe"
        assert result.email == "john@test.com"


class TestCandidateRepositoryGetByEmail:
    """Tests for get_by_email."""

    @pytest.mark.asyncio
    async def test_returns_none_for_unknown_email(
        self, candidate_repository: CandidateRepository
    ) -> None:
        result = await candidate_repository.get_by_email("unknown@test.com")
        assert result is None

    @pytest.mark.asyncio
    async def test_returns_candidate_by_email(
        self, candidate_repository: CandidateRepository, db_session: AsyncSession
    ) -> None:
        db_session.add(make_candidate(email="findme@test.com"))
        await db_session.commit()

        result = await candidate_repository.get_by_email("findme@test.com")
        assert result is not None
        assert result.email == "findme@test.com"


class TestCandidateRepositoryCreate:
    """Tests for create."""

    @pytest.mark.asyncio
    async def test_creates_candidate_with_timestamp(
        self, candidate_repository: CandidateRepository
    ) -> None:
        candidate = make_candidate()
        result = await candidate_repository.create(candidate)

        assert result.id is not None
        assert result.created_at is not None
        assert result.name == "John Doe"

    @pytest.mark.asyncio
    async def test_persists_in_database(
        self, candidate_repository: CandidateRepository, db_session: AsyncSession
    ) -> None:
        candidate = make_candidate(email="persisted@test.com")
        await candidate_repository.create(candidate)
        await db_session.commit()

        # Verify via direct query
        from sqlmodel import select

        statement = select(Candidate).where(Candidate.email == "persisted@test.com")
        db_result = await db_session.execute(statement)
        found = db_result.scalars().first()
        assert found is not None


class TestCandidateRepositoryUpdate:
    """Tests for update."""

    @pytest.mark.asyncio
    async def test_updates_fields(
        self, candidate_repository: CandidateRepository, db_session: AsyncSession
    ) -> None:
        candidate = make_candidate()
        db_session.add(candidate)
        await db_session.commit()
        await db_session.refresh(candidate)

        result = await candidate_repository.update(candidate, {"name": "Jane Doe"})
        assert result.name == "Jane Doe"

    @pytest.mark.asyncio
    async def test_updates_skills(
        self, candidate_repository: CandidateRepository, db_session: AsyncSession
    ) -> None:
        candidate = make_candidate()
        db_session.add(candidate)
        await db_session.commit()
        await db_session.refresh(candidate)

        result = await candidate_repository.update(candidate, {"skills": ["Go", "Rust"]})
        assert result.skills == ["Go", "Rust"]


class TestCandidateRepositoryDelete:
    """Tests for delete."""

    @pytest.mark.asyncio
    async def test_removes_candidate(
        self, candidate_repository: CandidateRepository, db_session: AsyncSession
    ) -> None:
        candidate = make_candidate(email="deleteme@test.com")
        db_session.add(candidate)
        await db_session.commit()
        await db_session.refresh(candidate)

        await candidate_repository.delete(candidate)
        await db_session.commit()

        result = await candidate_repository.get_by_id(candidate.id)  # type: ignore[arg-type]
        assert result is None
