"""Job DTOs for request/response serialization."""

from datetime import datetime

from pydantic import BaseModel, Field


class JobCreate(BaseModel):
    """Incoming payload to create a new job."""

    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    requirements: list[str] = Field(default_factory=list)
    location: str | None = None
    salary_range: str | None = None


class JobUpdate(BaseModel):
    """Incoming payload to partially update a job (PATCH)."""

    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    requirements: list[str] | None = None
    location: str | None = None
    salary_range: str | None = None


class JobRead(BaseModel):
    """Outgoing representation of a job."""

    id: int
    title: str
    description: str | None
    requirements: list[str]
    location: str | None
    salary_range: str | None
    created_at: datetime | None

    model_config = {"from_attributes": True}
