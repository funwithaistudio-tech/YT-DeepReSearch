"""Domain models for question framework."""

from typing import List

from pydantic import BaseModel, Field, field_validator


class SubQuestion(BaseModel):
    """Represents a sub-question within a main question."""

    sub_index: int = Field(..., description="Index of this sub-question (1 or 2)")
    role: str = Field(
        ...,
        description="Purpose/role of this sub-question (e.g., 'Define', 'Analyze')"
    )
    question: str = Field(..., description="The actual sub-question text")


class MainQuestion(BaseModel):
    """Represents a main question with exactly 2 sub-questions."""

    main_index: int = Field(..., description="Index of this main question (1-5)")
    role: str = Field(
        ...,
        description="Purpose/role of this main question (e.g., 'Introduction', 'Deep Dive')"
    )
    main_question: str = Field(..., description="The main question text")
    subquestions: List[SubQuestion] = Field(
        ...,
        description="List of exactly 2 sub-questions"
    )

    @field_validator("subquestions")
    @classmethod
    def validate_subquestions_count(cls, v: List[SubQuestion]) -> List[SubQuestion]:
        """Ensure exactly 2 sub-questions exist."""
        if len(v) != 2:
            raise ValueError(f"Expected exactly 2 sub-questions, got {len(v)}")
        return v


class QuestionFramework(BaseModel):
    """Complete question framework for a topic.
    
    Contains exactly 5 main questions, each with 2 sub-questions (10 total).
    """

    topic_id: int = Field(..., description="ID of the topic this framework belongs to")
    topic: str = Field(..., description="The research topic")
    style: str = Field(..., description="Content style (educational, documentary, etc.)")
    language: str = Field(..., description="Target language code")
    main_questions: List[MainQuestion] = Field(
        ...,
        description="List of exactly 5 main questions"
    )

    @field_validator("main_questions")
    @classmethod
    def validate_main_questions_count(cls, v: List[MainQuestion]) -> List[MainQuestion]:
        """Ensure exactly 5 main questions exist."""
        if len(v) != 5:
            raise ValueError(f"Expected exactly 5 main questions, got {len(v)}")
        return v

    @property
    def total_subquestions(self) -> int:
        """Get total number of sub-questions (should always be 10)."""
        return sum(len(mq.subquestions) for mq in self.main_questions)
