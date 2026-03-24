"""Candidate repository — direct database interaction."""

from datetime import datetime, timezone
from typing import Protocol, runtime_checkable

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.candidate import Candidate


@runtime_checkable
class CandidateRepositoryProtocol(Protocol):
    """Protocol that any Candidate repository implementation must satisfy."""

    async def get_all(self, offset: int, limit: int) -> list[Candidate]: ...
    async def get_by_id(self, candidate_id: int) -> Candidate | None: ...
    async def get_by_email(self, email: str) -> Candidate | None: ...
    async def create(self, candidate: Candidate) -> Candidate: ...
    async def update(self, candidate: Candidate, data: dict) -> Candidate: ...
    async def delete(self, candidate: Candidate) -> None: ...


class CandidateRepository:
    """SQLModel-based repository for candidates.

    Receives an AsyncSession via constructor injection.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_all(self, offset: int = 0, limit: int = 100) -> list[Candidate]:
        """Return a paginated list of candidates."""
        statement = select(Candidate).offset(offset).limit(limit)
        result = await self._session.execute(statement)
        return list(result.scalars().all())

    async def get_by_id(self, candidate_id: int) -> Candidate | None:
        """Return a single candidate by ID, or None."""
        return await self._session.get(Candidate, candidate_id)

    async def get_by_email(self, email: str) -> Candidate | None:
        """Return a candidate matching the given email, or None."""
        statement = select(Candidate).where(Candidate.email == email)
        result = await self._session.execute(statement)
        return result.scalars().first()

    async def create(self, candidate: Candidate) -> Candidate:
        """Persist a new candidate and refresh from DB (fills defaults)."""
        candidate.created_at = datetime.now(timezone.utc)
        self._session.add(candidate)
        await self._session.flush()
        await self._session.refresh(candidate)
        return candidate

    async def update(self, candidate: Candidate, data: dict) -> Candidate:
        """Apply partial update fields to an existing candidate."""
        for key, value in data.items():
            if value is not None:
                setattr(candidate, key, value)
        self._session.add(candidate)
        await self._session.flush()
        await self._session.refresh(candidate)
        return candidate

    async def delete(self, candidate: Candidate) -> None:
        """Remove a candidate from the database."""
        await self._session.delete(candidate)
        await self._session.flush()
