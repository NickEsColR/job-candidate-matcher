"""Candidate DTOs for request/response serialization."""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class CandidateCreate(BaseModel):
    """Incoming payload to create a new candidate."""

    name: str = Field(min_length=1, max_length=255)
    email: EmailStr
    skills: list[str] = Field(default_factory=list)
    experience: int | None = Field(default=None, ge=0)
    resume_url: str | None = Field(default=None)


class CandidateUpdate(BaseModel):
    """Incoming payload to partially update a candidate (PATCH)."""

    name: str | None = Field(default=None, min_length=1, max_length=255)
    email: EmailStr | None = None
    skills: list[str] | None = None
    experience: int | None = Field(default=None, ge=0)
    resume_url: str | None = None


class CandidateRead(BaseModel):
    """Outgoing representation of a candidate."""

    id: int
    name: str
    email: str
    skills: list[str]
    experience: int | None
    resume_url: str | None
    created_at: datetime | None

    model_config = {"from_attributes": True}
