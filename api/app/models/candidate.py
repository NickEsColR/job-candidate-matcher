"""Candidate entity."""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSON
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.evaluation import Evaluation


class Candidate(SQLModel, table=True):
    __tablename__ = "candidates"  # type: ignore[assignment]

    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True, index=True)
    skills: list[str] = Field(default=[], sa_column=Column(JSON))
    experience: int | None = Field(default=None)
    resume_url: str | None = Field(default=None)
    created_at: datetime | None = Field(default=None)

    evaluations: list["Evaluation"] = Relationship(back_populates="candidate")
