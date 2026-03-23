"""ToolLog entity."""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSON
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.evaluation import Evaluation


class ToolLog(SQLModel, table=True):
    __tablename__ = "tool_logs"  # type: ignore[assignment]

    id: int | None = Field(default=None, primary_key=True)
    evaluation_id: int = Field(foreign_key="evaluations.id", index=True)
    tool_name: str
    input_data: dict = Field(default={}, sa_column=Column(JSON))
    output_data: dict = Field(default={}, sa_column=Column(JSON))
    created_at: datetime | None = Field(default=None)

    evaluation: "Evaluation" = Relationship(back_populates="tool_logs")
