"""Repository test fixtures."""

from collections.abc import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

from app.models import Candidate, Evaluation, Job, ToolLog
from app.repositories.candidate_repository import CandidateRepository
from app.repositories.job_repository import JobRepository

TEST_DATABASE_URL = "sqlite+aiosqlite:///file::memory:?cache=shared&uri=true"

test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
test_session_factory = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(autouse=True)
async def setup_database() -> AsyncGenerator[None, None]:
    """Create and drop all tables around each repository test."""
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide a real async DB session for repository tests."""
    async with test_session_factory() as session:
        yield session


@pytest.fixture
def candidate_repository(db_session: AsyncSession) -> CandidateRepository:
    """Provide the concrete candidate repository."""
    return CandidateRepository(db_session)


@pytest.fixture
def job_repository(db_session: AsyncSession) -> JobRepository:
    """Provide the concrete job repository."""
    return JobRepository(db_session)
