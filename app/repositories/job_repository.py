"""Job repository — direct database interaction."""

from datetime import datetime, timezone
from typing import Protocol, runtime_checkable

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.job import Job


@runtime_checkable
class JobRepositoryProtocol(Protocol):
    async def get_all(self, offset: int, limit: int) -> list[Job]: ...
    async def get_by_id(self, job_id: int) -> Job | None: ...
    async def create(self, job: Job) -> Job: ...
    async def update(self, job: Job, data: dict) -> Job: ...
    async def delete(self, job: Job) -> None: ...


class JobRepository:
    """SQLModel-based repository for jobs."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_all(self, offset: int = 0, limit: int = 100) -> list[Job]:
        statement = select(Job).offset(offset).limit(limit)
        result = await self._session.execute(statement)
        return list(result.scalars().all())

    async def get_by_id(self, job_id: int) -> Job | None:
        return await self._session.get(Job, job_id)

    async def create(self, job: Job) -> Job:
        job.created_at = datetime.now(timezone.utc)
        self._session.add(job)
        await self._session.flush()
        await self._session.refresh(job)
        return job

    async def update(self, job: Job, data: dict) -> Job:
        for key, value in data.items():
            if value is not None:
                setattr(job, key, value)
        self._session.add(job)
        await self._session.flush()
        await self._session.refresh(job)
        return job

    async def delete(self, job: Job) -> None:
        await self._session.delete(job)
        await self._session.flush()
