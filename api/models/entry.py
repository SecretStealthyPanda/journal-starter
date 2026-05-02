from datetime import UTC, datetime
from typing import Annotated
from uuid import uuid4

from pydantic import BaseModel, Field, StringConstraints


class AnalysisResponse(BaseModel):
    """Response model for journal entry analysis."""

    entry_id: str = Field(description="ID of the analyzed entry")
    sentiment: str = Field(description="Sentiment: positive, negative, or neutral")
    summary: str = Field(description="2 sentence summary of the entry")
    topics: list[str] = Field(description="2-4 key topics mentioned in the entry")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Timestamp when the analysis was created",
    )


class EntryCreate(BaseModel):
    """Model for creating a new journal entry (user input)."""

    work: Annotated[str, StringConstraints(min_length=1, max_length=256, strip_whitespace=True)]

    struggle: Annotated[str, StringConstraints(min_length=1, max_length=256, strip_whitespace=True)]

    intention: Annotated[
        str, StringConstraints(min_length=1, max_length=256, strip_whitespace=True)
    ]


class EntryUpdate(BaseModel):
    work: (
        Annotated[str, StringConstraints(min_length=1, max_length=256, strip_whitespace=True)]
        | None
    ) = None
    struggle: (
        Annotated[str, StringConstraints(min_length=1, max_length=256, strip_whitespace=True)]
        | None
    ) = None
    intention: (
        Annotated[str, StringConstraints(min_length=1, max_length=256, strip_whitespace=True)]
        | None
    ) = None


class Entry(BaseModel):
    id: str = Field(
        default_factory=lambda: str(uuid4()), description="Unique identifier for the entry (UUID)."
    )
    work: str = Field(..., max_length=256, description="What did you work on today?")
    struggle: str = Field(
        ..., max_length=256, description="What's one thing you struggled with today?"
    )
    intention: str = Field(..., max_length=256, description="What will you study/work on tomorrow?")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Timestamp when the entry was created.",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Timestamp when the entry was last updated.",
    )
