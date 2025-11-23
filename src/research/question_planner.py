"""Question planning module for generating research questions."""

from typing import List
import json
from pathlib import Path

from src.domain.models import Topic, QuestionFramework, MainQuestion, SubQuestion
from src.config.settings import Settings
from src.utils.logger import get_logger

logger = get_logger()


class QuestionPlanner:
    """Plans research questions for a topic using AI."""
    
    def __init__(self, settings: Settings):
        """Initialize question planner.
        
        Args:
            settings: Application settings
        """
        self.settings = settings
        self.output_dir = Path(settings.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_questions(self, topic: Topic) -> QuestionFramework:
        """Generate research questions for a topic.
        
        Args:
            topic: Topic to generate questions for
            
        Returns:
            QuestionFramework with main and sub-questions
        """
        logger.info(f"Generating questions for topic: {topic.title}")
        
        # For now, generate simple structured questions
        # In a full implementation, this would use Gemini API
        main_questions = []
        
        num_main = self.settings.questions_per_topic
        num_sub = self.settings.sub_questions_per_question
        
        for i in range(1, num_main + 1):
            main_q_id = f"mq_{i}"
            main_q = MainQuestion(
                id=main_q_id,
                text=f"What is the key aspect {i} of {topic.title}?",
                sub_questions=[]
            )
            
            for j in range(1, num_sub + 1):
                sub_q = SubQuestion(
                    id=f"sq_{i}_{j}",
                    text=f"What are the details of aspect {i}, part {j}?",
                    parent_question_id=main_q_id
                )
                main_q.sub_questions.append(sub_q)
            
            main_questions.append(main_q)
        
        framework = QuestionFramework(
            topic_id=topic.id,
            main_questions=main_questions
        )
        
        # Persist framework
        self._save_framework(framework, topic.id)
        
        logger.info(f"Generated {len(main_questions)} main questions with {num_sub} sub-questions each")
        return framework
    
    def _save_framework(self, framework: QuestionFramework, topic_id: int):
        """Save question framework to JSON file."""
        filename = f"questions_topic_{topic_id}.json"
        filepath = self.output_dir / filename
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(framework.model_dump(), f, indent=2, default=str)
        
        logger.debug(f"Saved question framework to {filepath}")
    
    def load_framework(self, topic_id: int) -> QuestionFramework:
        """Load question framework from file.
        
        Args:
            topic_id: Topic ID
            
        Returns:
            QuestionFramework
        """
        filename = f"questions_topic_{topic_id}.json"
        filepath = self.output_dir / filename
        
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        return QuestionFramework(**data)
