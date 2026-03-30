"""Unit tests for JobRepository."""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.job import Job
from app.repositories.job_repository import JobRepository
from tests.support.job import make_job


class TestJobRepositoryGetAll:
    @pytest.mark.asyncio
    async def test_returns_empty_list_when_no_jobs(self, job_repository: JobRepository) -> None:
        result = await job_repository.get_all()
        assert result == []

    @pytest.mark.asyncio
    async def test_returns_jobs(self, job_repository: JobRepository, db_session: AsyncSession) -> None:
        db_session.add(make_job(title="One"))
        db_session.add(make_job(job_id=2, title="Two"))
        await db_session.commit()

        result = await job_repository.get_all()
        assert len(result) == 2


class TestJobRepositoryGetById:
    @pytest.mark.asyncio
    async def test_returns_none_for_missing_id(self, job_repository: JobRepository) -> None:
        result = await job_repository.get_by_id(999)
        assert result is None

    @pytest.mark.asyncio
    async def test_returns_job(self, job_repository: JobRepository, db_session: AsyncSession) -> None:
        job = make_job()
        db_session.add(job)
        await db_session.commit()
        await db_session.refresh(job)

        result = await job_repository.get_by_id(job.id)  # type: ignore[arg-type]
        assert result is not None
        assert result.title == "Backend Engineer"


class TestJobRepositoryCreate:
    @pytest.mark.asyncio
    async def test_creates_job_with_timestamp(self, job_repository: JobRepository) -> None:
        job = make_job()
        result = await job_repository.create(job)

        assert result.id is not None
        assert result.created_at is not None
        assert result.title == "Backend Engineer"

    @pytest.mark.asyncio
    async def test_persists_in_database(self, job_repository: JobRepository, db_session: AsyncSession) -> None:
        job = make_job(title="Persisted")
        await job_repository.create(job)
        await db_session.commit()

        from sqlmodel import select

        statement = select(Job).where(Job.title == "Persisted")
        db_result = await db_session.execute(statement)
        found = db_result.scalars().first()
        assert found is not None


class TestJobRepositoryUpdate:
    @pytest.mark.asyncio
    async def test_updates_fields(self, job_repository: JobRepository, db_session: AsyncSession) -> None:
        job = make_job()
        db_session.add(job)
        await db_session.commit()
        await db_session.refresh(job)

        result = await job_repository.update(job, {"title": "Senior Backend Engineer"})
        assert result.title == "Senior Backend Engineer"


class TestJobRepositoryDelete:
    @pytest.mark.asyncio
    async def test_removes_job(self, job_repository: JobRepository, db_session: AsyncSession) -> None:
        job = make_job(title="Delete me")
        db_session.add(job)
        await db_session.commit()
        await db_session.refresh(job)

        await job_repository.delete(job)
        await db_session.commit()

        result = await job_repository.get_by_id(job.id)  # type: ignore[arg-type]
        assert result is None
