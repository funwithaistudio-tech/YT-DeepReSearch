"""Domain models for research data."""

from typing import List, Optional

from pydantic import BaseModel, Field


class Source(BaseModel):
    """Represents a research source/citation."""

    id: str = Field(..., description="Unique identifier for this source (e.g., 'src_1')")
    title: str = Field(..., description="Title of the source")
    url: str = Field(..., description="URL of the source")
    publisher: Optional[str] = Field(None, description="Publisher/domain name")
    date: Optional[str] = Field(None, description="Publication date")
    snippet: Optional[str] = Field(None, description="Relevant snippet/excerpt")


class SubQuestionResearch(BaseModel):
    """Research results for a single sub-question.
    
    Contains search results, sources, and synthesized information.
    """

    topic_id: int = Field(..., description="ID of the parent topic")
    topic: str = Field(..., description="The research topic")
    main_index: int = Field(..., description="Index of the parent main question")
    sub_index: int = Field(..., description="Index of this sub-question")
    main_question: str = Field(..., description="The parent main question text")
    sub_question: str = Field(..., description="The sub-question text")
    search_query: str = Field(
        ...,
        description="The actual search query used for research"
    )
    sources: List[Source] = Field(
        default_factory=list,
        description="List of sources found during research"
    )
    summary: str = Field(
        ...,
        description="Summary of research findings for this sub-question"
    )
    key_points: List[str] = Field(
        default_factory=list,
        description="Key points extracted from research"
    )
    controversies: Optional[List[str]] = Field(
        None,
        description="Optional list of controversies or differing viewpoints"
    )

    @property
    def source_count(self) -> int:
        """Get the number of sources found."""
        return len(self.sources)
