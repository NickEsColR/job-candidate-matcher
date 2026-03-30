"""Job router — HTTP endpoints for CRUD operations."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db import get_session
from app.models.job import Job
from app.repositories.job_repository import JobRepository, JobRepositoryProtocol
from app.schemas.job import JobCreate, JobRead, JobUpdate
from app.services.job_service import JobService, JobServiceProtocol

router = APIRouter(prefix="/api/v1/jobs", tags=["jobs"])


def get_job_repository(session: AsyncSession = Depends(get_session)) -> JobRepositoryProtocol:
    return JobRepository(session)


def get_job_service(
    repository: JobRepositoryProtocol = Depends(get_job_repository),
    session: AsyncSession = Depends(get_session),
) -> JobServiceProtocol:
    return JobService(repository, session)


@router.get("/", response_model=list[JobRead])
async def list_jobs(
    offset: int = 0,
    limit: int = 100,
    service: JobServiceProtocol = Depends(get_job_service),
) -> list[Job]:
    return await service.list_jobs(offset=offset, limit=limit)


@router.get("/{job_id}", response_model=JobRead)
async def get_job(job_id: int, service: JobServiceProtocol = Depends(get_job_service)) -> Job:
    return await service.get_job(job_id)


@router.post("/", response_model=JobRead, status_code=status.HTTP_201_CREATED)
async def create_job(data: JobCreate, service: JobServiceProtocol = Depends(get_job_service)) -> Job:
    return await service.create_job(data)


@router.patch("/{job_id}", response_model=JobRead)
async def update_job(
    job_id: int,
    data: JobUpdate,
    service: JobServiceProtocol = Depends(get_job_service),
) -> Job:
    return await service.update_job(job_id, data)


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(job_id: int, service: JobServiceProtocol = Depends(get_job_service)) -> None:
    await service.delete_job(job_id)
