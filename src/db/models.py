"""Database models for YT-DeepReSearch."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TopicJob(BaseModel):
    """Represents a topic job from the database.
    
    This model maps to the topics table in the database.
    """

    id: int = Field(..., description="Unique topic ID")
    topic: str = Field(..., description="The research topic/subject")
    style: str = Field(
        default="educational",
        description="Content style (educational, documentary, etc.)"
    )
    language: str = Field(
        default="en",
        description="Target language code (en, hi, ta, etc.)"
    )
    status: Optional[str] = Field(
        default="pending",
        description="Current status (pending, in_progress, completed, failed)"
    )
    priority: Optional[int] = Field(
        default=0,
        description="Priority level for processing order"
    )
    last_run_at: Optional[datetime] = Field(
        None,
        description="Timestamp of last processing attempt"
    )
    last_error: Optional[str] = Field(
        None,
        description="Error message from last failed attempt"
    )
    youtube_video_id: Optional[str] = Field(
        None,
        description="YouTube video ID after publishing"
    )

    class Config:
        """Pydantic configuration."""
        from_attributes = True  # Enable ORM mode for SQLAlchemy models
