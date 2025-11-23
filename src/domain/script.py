"""Domain models for generated scripts."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator


class SubSegment(BaseModel):
    """Represents a subsegment of the script.
    
    Each subsegment corresponds to one sub-question's research.
    """

    index: int = Field(..., description="Global index of this subsegment (1-10)")
    role: str = Field(..., description="Role/purpose of this subsegment")
    sub_question: str = Field(..., description="The sub-question this answers")
    text: str = Field(..., description="The actual script text")
    word_count: int = Field(..., description="Word count of the text")
    sources_used: List[str] = Field(
        default_factory=list,
        description="List of source IDs used in this subsegment"
    )
    assets: Optional[Dict[str, Any]] = Field(
        None,
        description="Optional asset metadata (for future phases: images, audio, etc.)"
    )


class MainSegment(BaseModel):
    """Represents a main segment containing exactly 2 subsegments."""

    index: int = Field(..., description="Index of this main segment (1-5)")
    role: str = Field(..., description="Role/purpose of this main segment")
    main_question: str = Field(..., description="The main question this segment addresses")
    title: str = Field(..., description="Descriptive title for this segment (60-80 chars)")
    summary: str = Field(..., description="2-4 sentence summary of this segment")
    subsegments: List[SubSegment] = Field(
        ...,
        description="List of exactly 2 subsegments"
    )

    @field_validator("subsegments")
    @classmethod
    def validate_subsegments_count(cls, v: List[SubSegment]) -> List[SubSegment]:
        """Ensure exactly 2 subsegments exist."""
        if len(v) != 2:
            raise ValueError(f"Expected exactly 2 subsegments, got {len(v)}")
        return v

    @property
    def total_words(self) -> int:
        """Get total word count for this main segment."""
        return sum(sub.word_count for sub in self.subsegments)


class Script(BaseModel):
    """Complete generated script for a topic.
    
    Contains exactly 5 main segments, each with 2 subsegments (10 total).
    """

    topic_id: int = Field(..., description="ID of the topic this script belongs to")
    topic: str = Field(..., description="The research topic")
    style: str = Field(..., description="Content style")
    language: str = Field(..., description="Target language code")
    total_word_count: int = Field(..., description="Total word count across all segments")
    main_segments: List[MainSegment] = Field(
        ...,
        description="List of exactly 5 main segments"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Optional metadata (timestamps, assets info, etc. for future phases)"
    )

    @field_validator("main_segments")
    @classmethod
    def validate_main_segments_count(cls, v: List[MainSegment]) -> List[MainSegment]:
        """Ensure exactly 5 main segments exist."""
        if len(v) != 5:
            raise ValueError(f"Expected exactly 5 main segments, got {len(v)}")
        return v

    @property
    def total_subsegments(self) -> int:
        """Get total number of subsegments (should always be 10)."""
        return sum(len(ms.subsegments) for ms in self.main_segments)

    @property
    def average_subsegment_words(self) -> float:
        """Calculate average words per subsegment."""
        total_subs = self.total_subsegments
        return self.total_word_count / total_subs if total_subs > 0 else 0.0
