"""Script generation module using Gemini."""

import json
from pathlib import Path
from typing import List

from src.domain.models import (
    Script, MainSegment, SubSegment, 
    QuestionFramework, SubQuestionResearch
)
from src.config.settings import Settings
from src.utils.logger import get_logger

logger = get_logger()


class ScriptGenerator:
    """Generates video scripts using Gemini API."""
    
    def __init__(self, settings: Settings):
        """Initialize script generator.
        
        Args:
            settings: Application settings
        """
        self.settings = settings
        self.output_dir = Path(settings.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_script(
        self,
        topic_id: int,
        topic_title: str,
        framework: QuestionFramework,
        research_results: List[SubQuestionResearch]
    ) -> Script:
        """Generate complete script from research.
        
        Args:
            topic_id: Topic ID
            topic_title: Topic title
            framework: Question framework
            research_results: List of research results
            
        Returns:
            Complete Script
        """
        logger.info(f"Generating script for topic: {topic_title}")
        
        # Build script structure
        main_segments = []
        
        for main_q in framework.main_questions:
            # Create main segment
            main_segment = MainSegment(
                id=main_q.id,
                title=main_q.text,
                summary=f"Summary of {main_q.text}",
                based_on_main_question_id=main_q.id,
                sub_segments=[]
            )
            
            # Create sub-segments for each sub-question
            for sub_q in main_q.sub_questions:
                # Find corresponding research
                research = next(
                    (r for r in research_results if r.sub_question_id == sub_q.id),
                    None
                )
                
                if research:
                    content = self._generate_subsegment_content(research)
                else:
                    content = f"Content for {sub_q.text}"
                
                subsegment = SubSegment(
                    id=sub_q.id,
                    title=sub_q.text,
                    content=content,
                    duration_estimate=30.0,  # Estimate 30 seconds per subsegment
                    based_on_sub_question_id=sub_q.id,
                    assets={}
                )
                
                main_segment.sub_segments.append(subsegment)
            
            main_segments.append(main_segment)
        
        # Create complete script
        script = Script(
            topic_id=topic_id,
            title=topic_title,
            description=f"Deep research video on {topic_title}",
            main_segments=main_segments,
            metadata={
                "language": self.settings.script_language,
                "style": self.settings.content_style,
                "length": self.settings.script_length
            }
        )
        
        # Calculate total duration
        script.total_duration_estimate = script.estimate_total_duration()
        
        # Save script
        self._save_script(script)
        
        logger.info(f"Generated script with {len(main_segments)} main segments, "
                   f"estimated duration: {script.total_duration_estimate:.1f}s")
        
        return script
    
    def _generate_subsegment_content(self, research: SubQuestionResearch) -> str:
        """Generate script content from research.
        
        Args:
            research: Research results
            
        Returns:
            Script content text
        """
        # In production, this would use Gemini to generate engaging script
        # For now, use research content directly
        return research.research_content
    
    def _save_script(self, script: Script):
        """Save script to JSON file.
        
        Args:
            script: Script to save
        """
        filename = f"script_topic_{script.topic_id}.json"
        filepath = self.output_dir / filename
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(script.model_dump(), f, indent=2, default=str)
        
        logger.info(f"Saved script to {filepath}")
    
    def load_script(self, topic_id: int) -> Script:
        """Load script from file.
        
        Args:
            topic_id: Topic ID
            
        Returns:
            Script
        """
        filename = f"script_topic_{topic_id}.json"
        filepath = self.output_dir / filename
        
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        return Script(**data)
