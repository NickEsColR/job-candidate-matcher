"""Candidate service — business logic layer."""

from typing import Protocol, runtime_checkable

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.candidate import Candidate
from app.repositories.candidate_repository import CandidateRepositoryProtocol
from app.schemas.candidate import CandidateCreate, CandidateUpdate


@runtime_checkable
class CandidateServiceProtocol(Protocol):
    """Protocol that any Candidate service implementation must satisfy."""

    async def list_candidates(self, offset: int, limit: int) -> list[Candidate]: ...
    async def get_candidate(self, candidate_id: int) -> Candidate: ...
    async def create_candidate(self, data: CandidateCreate) -> Candidate: ...
    async def update_candidate(self, candidate_id: int, data: CandidateUpdate) -> Candidate: ...
    async def delete_candidate(self, candidate_id: int) -> None: ...


class CandidateService:
    """Business logic for candidate operations.

    Receives a CandidateRepository via constructor injection.
    """

    def __init__(
        self,
        repository: CandidateRepositoryProtocol,
        session: AsyncSession,
    ) -> None:
        self._repo = repository
        self._session = session

    async def list_candidates(self, offset: int = 0, limit: int = 100) -> list[Candidate]:
        """Return paginated candidates."""
        return await self._repo.get_all(offset=offset, limit=limit)

    async def get_candidate(self, candidate_id: int) -> Candidate:
        """Return a single candidate or raise 404."""
        candidate = await self._repo.get_by_id(candidate_id)
        if candidate is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Candidate with id {candidate_id} not found",
            )
        return candidate

    async def create_candidate(self, data: CandidateCreate) -> Candidate:
        """Create a candidate, ensuring email uniqueness."""
        existing = await self._repo.get_by_email(data.email)
        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Candidate with email {data.email} already exists",
            )
        candidate = Candidate(**data.model_dump())
        candidate = await self._repo.create(candidate)
        await self._session.commit()
        return candidate

    async def update_candidate(self, candidate_id: int, data: CandidateUpdate) -> Candidate:
        """Update a candidate, ensuring it exists and email is unique."""
        candidate = await self.get_candidate(candidate_id)

        # If email is changing, verify it's not taken by another candidate
        if data.email is not None and data.email != candidate.email:
            existing = await self._repo.get_by_email(data.email)
            if existing is not None:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Candidate with email {data.email} already exists",
                )

        update_data = data.model_dump(exclude_unset=True)
        candidate = await self._repo.update(candidate, update_data)
        await self._session.commit()
        return candidate

    async def delete_candidate(self, candidate_id: int) -> None:
        """Delete a candidate, ensuring it exists."""
        candidate = await self.get_candidate(candidate_id)
        await self._repo.delete(candidate)
        await self._session.commit()
