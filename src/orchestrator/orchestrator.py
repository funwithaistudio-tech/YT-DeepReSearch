"""Orchestrator for managing the complete research pipeline."""

import traceback
from typing import Optional

from src.config.settings import Settings
from src.content.script_generator import ScriptGenerator
from src.db.topic_repository import TopicRepository
from src.research.deep_researcher import DeepResearcher
from src.research.question_planner import QuestionPlanner
from src.utils.logger import get_logger, setup_logger


class Orchestrator:
    """Orchestrates the complete deep research pipeline.
    
    Manages the flow from topic fetching through script generation.
    """

    def __init__(self, settings: Settings):
        """Initialize the orchestrator with all required components.
        
        Args:
            settings: Application settings
        """
        self.settings = settings
        self.logger = setup_logger(
            log_level=settings.log_level,
            log_dir=settings.logs_dir,
            console_output=True
        )
        
        # Initialize components
        self.topic_repo = TopicRepository(settings)
        self.question_planner = QuestionPlanner(settings)
        self.deep_researcher = DeepResearcher(settings)
        self.script_generator = ScriptGenerator(settings)

    def run_for_next_topic(self) -> bool:
        """Run the pipeline for the next pending topic.
        
        Executes all phases: fetch topic, build questions, research, generate script.
        
        Returns:
            True if a topic was processed, False if no pending topics
        """
        self.logger.info("=" * 80)
        self.logger.info("Starting Deep Research Pipeline")
        self.logger.info("=" * 80)
        
        try:
            # Phase 1: Fetch next topic
            self.logger.info("PHASE 1: Fetching next pending topic from database")
            topic = self.topic_repo.fetch_next_topic()
            
            if topic is None:
                self.logger.info("No pending topics found. Exiting.")
                return False
            
            logger = get_logger(topic_id=topic.id)
            logger.info(
                f"Processing topic {topic.id}: '{topic.topic}' "
                f"(style={topic.style}, language={topic.language})"
            )
            
            # Phase 2: Build question framework
            logger.info("PHASE 2: Building question framework")
            framework = self.question_planner.build_question_framework(
                topic_id=topic.id,
                topic=topic.topic,
                style=topic.style,
                language=topic.language
            )
            
            # Phase 3: Deep research
            logger.info("PHASE 3: Performing deep research")
            research_results = self.deep_researcher.research_topic(framework)
            
            # Phase 4: Generate script
            logger.info("PHASE 4: Generating script")
            script = self.script_generator.generate_script(
                framework=framework,
                research_results=research_results
            )
            
            # Mark topic as completed
            logger.info("Marking topic as completed")
            self.topic_repo.mark_topic_done(topic.id)
            
            logger.info("=" * 80)
            logger.info(
                f"Pipeline completed successfully for topic {topic.id}! "
                f"Generated {script.total_word_count} words across "
                f"{len(script.main_segments)} segments."
            )
            logger.info("=" * 80)
            
            return True
            
        except Exception as e:
            error_msg = f"Pipeline failed: {str(e)}"
            self.logger.error(error_msg)
            self.logger.error(traceback.format_exc())
            
            # Try to mark topic as failed if we have a topic ID
            if 'topic' in locals() and topic:
                try:
                    self.topic_repo.mark_topic_failed(
                        topic.id,
                        error_message=error_msg[:500]  # Limit error message length
                    )
                except Exception as repo_error:
                    self.logger.error(
                        f"Failed to mark topic as failed: {repo_error}"
                    )
            
            raise

    def close(self) -> None:
        """Clean up resources."""
        self.topic_repo.close()
        self.logger.info("Orchestrator resources cleaned up")
