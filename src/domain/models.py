"""Domain models for the YT-DeepReSearch system."""

from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class TopicStatus(str, Enum):
    """Topic processing status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class Topic(BaseModel):
    """Topic to research and create video for."""
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    niche: str = Field(default="educational")
    status: TopicStatus = TopicStatus.PENDING
    youtube_video_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    error_message: Optional[str] = None


class SubQuestion(BaseModel):
    """Sub-question within a main question."""
    id: str
    text: str
    parent_question_id: str


class MainQuestion(BaseModel):
    """Main research question."""
    id: str
    text: str
    sub_questions: List[SubQuestion] = Field(default_factory=list)


class QuestionFramework(BaseModel):
    """Framework of research questions for a topic."""
    topic_id: int
    main_questions: List[MainQuestion] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ResearchSource(BaseModel):
    """Research source citation."""
    url: str
    title: Optional[str] = None
    relevance_score: Optional[float] = None


class SubQuestionResearch(BaseModel):
    """Research results for a sub-question."""
    sub_question_id: str
    sub_question_text: str
    main_question_id: str
    research_content: str
    sources: List[ResearchSource] = Field(default_factory=list)
    researched_at: datetime = Field(default_factory=datetime.utcnow)


class SubSegment(BaseModel):
    """Sub-segment within a main segment of the script."""
    id: str
    title: str
    content: str
    duration_estimate: Optional[float] = None  # seconds
    based_on_sub_question_id: Optional[str] = None
    assets: Dict[str, Any] = Field(default_factory=dict)  # {"images": [...], "audio_path": "..."}
    
    def add_image(self, image_path: str):
        """Add an image asset."""
        if "images" not in self.assets:
            self.assets["images"] = []
        self.assets["images"].append(image_path)
    
    def set_audio(self, audio_path: str):
        """Set audio asset."""
        self.assets["audio_path"] = audio_path


class MainSegment(BaseModel):
    """Main segment of the script."""
    id: str
    title: str
    summary: str
    sub_segments: List[SubSegment] = Field(default_factory=list)
    based_on_main_question_id: Optional[str] = None


class Script(BaseModel):
    """Complete video script."""
    topic_id: int
    title: str
    description: Optional[str] = None
    main_segments: List[MainSegment] = Field(default_factory=list)
    total_duration_estimate: Optional[float] = None  # seconds
    created_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    def get_all_subsegments(self) -> List[SubSegment]:
        """Get all subsegments across all main segments."""
        subsegments = []
        for main_segment in self.main_segments:
            subsegments.extend(main_segment.sub_segments)
        return subsegments
    
    def estimate_total_duration(self) -> float:
        """Estimate total video duration based on subsegments."""
        total = 0.0
        for subsegment in self.get_all_subsegments():
            if subsegment.duration_estimate:
                total += subsegment.duration_estimate
        return total
