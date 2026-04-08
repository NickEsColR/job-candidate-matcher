"""Job service — business logic layer."""

from typing import Protocol, runtime_checkable

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.job import Job
from app.repositories.job_repository import JobRepositoryProtocol
from app.schemas.job import JobCreate, JobUpdate


@runtime_checkable
class JobServiceProtocol(Protocol):
    async def list_jobs(self, offset: int, limit: int) -> list[Job]: ...
    async def get_job(self, job_id: int) -> Job: ...
    async def create_job(self, data: JobCreate) -> Job: ...
    async def update_job(self, job_id: int, data: JobUpdate) -> Job: ...
    async def delete_job(self, job_id: int) -> None: ...


class JobService:
    def __init__(self, repository: JobRepositoryProtocol, session: AsyncSession) -> None:
        self._repo = repository
        self._session = session

    async def list_jobs(self, offset: int = 0, limit: int = 100) -> list[Job]:
        return await self._repo.get_all(offset=offset, limit=limit)

    async def get_job(self, job_id: int) -> Job:
        job = await self._repo.get_by_id(job_id)
        if job is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Job with id {job_id} not found")
        return job

    async def create_job(self, data: JobCreate) -> Job:
        job = Job(**data.model_dump())
        job = await self._repo.create(job)
        await self._session.commit()
        return job

    async def update_job(self, job_id: int, data: JobUpdate) -> Job:
        job = await self.get_job(job_id)
        update_data = data.model_dump(exclude_unset=True)
        job = await self._repo.update(job, update_data)
        await self._session.commit()
        return job

    async def delete_job(self, job_id: int) -> None:
        job = await self.get_job(job_id)
        await self._repo.delete(job)
        await self._session.commit()
