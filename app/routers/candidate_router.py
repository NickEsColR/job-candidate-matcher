"""Candidate router — HTTP endpoints for CRUD operations."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db import get_session
from app.models.candidate import Candidate
from app.repositories.candidate_repository import (
    CandidateRepository,
    CandidateRepositoryProtocol,
)
from app.schemas.candidate import CandidateCreate, CandidateRead, CandidateUpdate
from app.services.candidate_service import CandidateService, CandidateServiceProtocol

router = APIRouter(prefix="/api/v1/candidates", tags=["candidates"])


# ── Dependency providers ──────────────────────────────────────────────


def get_candidate_repository(
    session: AsyncSession = Depends(get_session),
) -> CandidateRepositoryProtocol:
    """Provide a CandidateRepository wired to the request session."""
    return CandidateRepository(session)


def get_candidate_service(
    repository: CandidateRepositoryProtocol = Depends(get_candidate_repository),
    session: AsyncSession = Depends(get_session),
) -> CandidateServiceProtocol:
    """Provide a CandidateService wired to the repository."""
    return CandidateService(repository, session)


# ── Endpoints ─────────────────────────────────────────────────────────


@router.get("/", response_model=list[CandidateRead])
async def list_candidates(
    offset: int = 0,
    limit: int = 100,
    service: CandidateServiceProtocol = Depends(get_candidate_service),
) -> list[Candidate]:
    """Return a paginated list of candidates."""
    return await service.list_candidates(offset=offset, limit=limit)


@router.get("/{candidate_id}", response_model=CandidateRead)
async def get_candidate(
    candidate_id: int,
    service: CandidateServiceProtocol = Depends(get_candidate_service),
) -> Candidate:
    """Return a single candidate by ID."""
    return await service.get_candidate(candidate_id)


@router.post("/", response_model=CandidateRead, status_code=status.HTTP_201_CREATED)
async def create_candidate(
    data: CandidateCreate,
    service: CandidateServiceProtocol = Depends(get_candidate_service),
) -> Candidate:
    """Create a new candidate."""
    return await service.create_candidate(data)


@router.patch("/{candidate_id}", response_model=CandidateRead)
async def update_candidate(
    candidate_id: int,
    data: CandidateUpdate,
    service: CandidateServiceProtocol = Depends(get_candidate_service),
) -> Candidate:
    """Partially update an existing candidate."""
    return await service.update_candidate(candidate_id, data)


@router.delete("/{candidate_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_candidate(
    candidate_id: int,
    service: CandidateServiceProtocol = Depends(get_candidate_service),
) -> None:
    """Delete a candidate by ID."""
    await service.delete_candidate(candidate_id)
