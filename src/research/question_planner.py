"""Question planner for building research framework."""

import json
from pathlib import Path

from src.config.settings import Settings
from src.domain.questions import QuestionFramework
from src.research.perplexity_client import PerplexityClient
from src.utils.logger import get_logger


class QuestionPlanner:
    """Builds a question framework for a topic using Perplexity AI.
    
    Generates 5 main questions with 2 sub-questions each (10 total).
    """

    def __init__(self, settings: Settings):
        """Initialize the question planner.
        
        Args:
            settings: Application settings
        """
        self.settings = settings
        self.perplexity = PerplexityClient(settings)
        self.logger = get_logger()
        
        # Load the prompt template
        prompt_path = Path(__file__).parent.parent / "content" / "prompts" / "deep_questions_prompt.txt"
        with open(prompt_path, "r", encoding="utf-8") as f:
            self.prompt_template = f.read()

    def build_question_framework(
        self, topic_id: int, topic: str, style: str, language: str
    ) -> QuestionFramework:
        """Build a question framework for the given topic.
        
        Args:
            topic_id: Database ID of the topic
            topic: The research topic text
            style: Content style (educational, documentary, etc.)
            language: Target language code
            
        Returns:
            QuestionFramework with 5 main questions and 10 sub-questions
            
        Raises:
            Exception: If framework generation or validation fails
        """
        logger = self.logger.with_context(topic_id=topic_id, phase="question_planning")
        
        logger.info(f"Building question framework for topic: '{topic}'")
        
        # Build the prompt
        prompt = self.prompt_template.replace("[TOPIC_PLACEHOLDER]", topic)
        
        # Call Perplexity to generate questions
        try:
            response_json = self.perplexity.chat_json(
                prompt=prompt,
                model="sonar-pro"
            )
            
            # Parse the JSON response
            response_data = json.loads(response_json)
            
            # Inject the required metadata fields
            response_data["topic_id"] = topic_id
            response_data["topic"] = topic
            response_data["style"] = style
            response_data["language"] = language
            
            # Validate and construct the QuestionFramework
            framework = QuestionFramework(**response_data)
            
            logger.info(
                f"Question framework built successfully: "
                f"{len(framework.main_questions)} main questions, "
                f"{framework.total_subquestions} sub-questions"
            )
            
            # Save to file
            output_path = self.settings.generated_dir / f"topic_{topic_id}_question_framework.json"
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(framework.model_dump_json(indent=2))
            
            logger.info(f"Question framework saved to: {output_path}")
            
            return framework
            
        except Exception as e:
            logger.error(f"Failed to build question framework: {e}")
            raise
