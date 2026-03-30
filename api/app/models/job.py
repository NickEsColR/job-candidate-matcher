"""Job entity."""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, Text
from sqlalchemy.dialects.postgresql import JSON
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.evaluation import Evaluation


class Job(SQLModel, table=True):
    __tablename__ = "jobs"  # type: ignore[assignment]

    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str | None = Field(default=None, sa_column=Column(Text))
    requirements: list[str] = Field(default=[], sa_column=Column(JSON))
    location: str | None = Field(default=None)
    salary_range: str | None = Field(default=None)
    created_at: datetime | None = Field(default=None)

    evaluations: list["Evaluation"] = Relationship(back_populates="job")
