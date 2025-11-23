"""Main orchestrator for the YT-DeepReSearch pipeline."""

from typing import Optional

from src.config.settings import Settings
from src.repository.topic_repository import TopicRepository
from src.research.question_planner import QuestionPlanner
from src.research.deep_researcher import DeepResearcher
from src.content.script_generator import ScriptGenerator
from src.assets.asset_generator import AssetGenerator
from src.video.assembler import VideoAssembler
from src.publish.youtube_publisher import YouTubePublisher
from src.cleanup.cleanup_manager import CleanupManager
from src.domain.models import Topic
from src.utils.logger import get_logger

logger = get_logger()


class Orchestrator:
    """Orchestrates the complete video creation pipeline."""
    
    def __init__(self, settings: Settings):
        """Initialize orchestrator with all components.
        
        Args:
            settings: Application settings
        """
        self.settings = settings
        
        # Initialize all components
        logger.info("Initializing pipeline components...")
        
        self.topic_repo = TopicRepository(settings.database_url)
        self.question_planner = QuestionPlanner(settings)
        self.deep_researcher = DeepResearcher(settings)
        self.script_generator = ScriptGenerator(settings)
        self.asset_generator = AssetGenerator(settings)
        self.video_assembler = VideoAssembler(settings)
        self.youtube_publisher = YouTubePublisher(settings)
        self.cleanup_manager = CleanupManager(settings)
        
        logger.info("All components initialized successfully")
    
    def run_for_next_topic(self) -> bool:
        """Run the complete pipeline for the next pending topic.
        
        Returns:
            True if a topic was processed, False if no pending topics
        """
        # Phase 1: Get next pending topic
        topic = self.topic_repo.get_next_pending_topic()
        
        if not topic:
            logger.info("No pending topics to process")
            return False
        
        logger.info(f"Processing topic {topic.id}: {topic.title}")
        
        try:
            # Mark topic as in progress
            self.topic_repo.mark_topic_in_progress(topic.id)
            
            # Run pipeline phases based on configuration
            run_phases = self.settings.run_phases.lower()
            
            # Phase 2: Question Planning
            logger.info("=== Phase 2: Question Planning ===")
            framework = self.question_planner.generate_questions(topic)
            
            # Phase 3: Deep Research
            logger.info("=== Phase 3: Deep Research ===")
            research_results = self.deep_researcher.research_framework(framework, topic.id)
            
            # Phase 4: Script Generation
            logger.info("=== Phase 4: Script Generation ===")
            script = self.script_generator.generate_script(
                topic.id,
                topic.title,
                framework,
                research_results
            )
            
            if run_phases == "script_only":
                logger.info("Stopping after script generation (script_only mode)")
                self.topic_repo.mark_topic_completed(topic.id)
                return True
            
            # Phase 5: Asset Generation
            logger.info("=== Phase 5: Asset Generation ===")
            script = self.asset_generator.generate_assets(script)
            
            if run_phases == "assets_only":
                logger.info("Stopping after asset generation (assets_only mode)")
                self.topic_repo.mark_topic_completed(topic.id)
                return True
            
            # Phase 6: Video Assembly
            logger.info("=== Phase 6: Video Assembly ===")
            video_path = self.video_assembler.assemble_main_video(script)
            
            if run_phases == "video_only":
                logger.info("Stopping after video assembly (video_only mode)")
                self.topic_repo.mark_topic_completed(topic.id)
                return True
            
            # Phase 7: YouTube Publishing
            logger.info("=== Phase 7: YouTube Publishing ===")
            youtube_video_id = self.youtube_publisher.publish_main_video(script, video_path)
            
            # Mark topic as completed
            self.topic_repo.mark_topic_completed(topic.id, youtube_video_id)
            
            # Phase 8: Cleanup
            logger.info("=== Phase 8: Cleanup ===")
            self.cleanup_manager.cleanup_for_topic(topic.id, success=True)
            
            logger.info(f"✅ Successfully completed topic {topic.id}: {topic.title}")
            logger.info(f"   YouTube Video ID: {youtube_video_id}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to process topic {topic.id}: {e}", exc_info=True)
            
            # Mark topic as failed
            self.topic_repo.mark_topic_failed(topic.id, str(e))
            
            # Cleanup on failure (no deletion of temp files)
            try:
                self.cleanup_manager.cleanup_for_topic(topic.id, success=False)
            except Exception as cleanup_error:
                logger.error(f"Cleanup failed: {cleanup_error}")
            
            return False
    
    def run_continuous(self, max_iterations: Optional[int] = None):
        """Run the pipeline continuously for all pending topics.
        
        Args:
            max_iterations: Maximum number of topics to process (None for unlimited)
        """
        logger.info("Starting continuous pipeline execution")
        
        iteration = 0
        while True:
            if max_iterations and iteration >= max_iterations:
                logger.info(f"Reached max iterations ({max_iterations})")
                break
            
            processed = self.run_for_next_topic()
            
            if not processed:
                logger.info("No more pending topics")
                break
            
            iteration += 1
        
        logger.info(f"Continuous execution complete. Processed {iteration} topics")
    
    def run_for_topic_id(self, topic_id: int):
        """Run the pipeline for a specific topic ID.
        
        Args:
            topic_id: Topic ID to process
        """
        topic = self.topic_repo.get_topic(topic_id)
        
        if not topic:
            raise ValueError(f"Topic {topic_id} not found")
        
        logger.info(f"Processing specific topic {topic_id}: {topic.title}")
        
        # Reset topic to pending if needed
        if topic.status.value != "pending":
            logger.info(f"Resetting topic {topic_id} status to pending")
            self.topic_repo.update_topic_status(topic.id, "pending")
        
        # Process the topic
        self.run_for_next_topic()
