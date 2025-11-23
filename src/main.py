"""Main entry point for YT-DeepReSearch system."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.config.settings import Settings
from src.orchestrator.orchestrator import Orchestrator
from src.repository.topic_repository import TopicRepository
from src.utils.logger import setup_logger


def main():
    """Main execution function."""
    # Load configuration
    settings = Settings()
    
    # Setup logging
    logger = setup_logger(
        log_level=settings.log_level,
        log_file=settings.log_file
    )
    
    logger.info("=" * 60)
    logger.info("YT-DeepReSearch - Automated Video Creation Pipeline")
    logger.info("=" * 60)
    
    try:
        # Validate settings
        settings.validate_required_settings()
        settings.ensure_directories()
        
        # Initialize orchestrator
        orchestrator = Orchestrator(settings)
        
        # Check command line arguments
        if len(sys.argv) > 1:
            command = sys.argv[1].lower()
            
            if command == "add-topic":
                # Add a new topic
                if len(sys.argv) < 3:
                    print("Usage: python -m src.main add-topic <title> [description] [niche]")
                    sys.exit(1)
                
                title = sys.argv[2]
                description = sys.argv[3] if len(sys.argv) > 3 else None
                niche = sys.argv[4] if len(sys.argv) > 4 else "educational"
                
                topic_repo = TopicRepository(settings.database_url)
                topic = topic_repo.create_topic(title, description, niche)
                
                print(f"\n✅ Topic created successfully!")
                print(f"   ID: {topic.id}")
                print(f"   Title: {topic.title}")
                print(f"   Status: {topic.status.value}")
                
            elif command == "list-topics":
                # List all topics
                topic_repo = TopicRepository(settings.database_url)
                topics = topic_repo.list_topics()
                
                if not topics:
                    print("\nNo topics found.")
                else:
                    print(f"\n{'ID':<5} {'Status':<12} {'Title':<50} {'YouTube ID':<20}")
                    print("-" * 90)
                    for topic in topics:
                        yt_id = topic.youtube_video_id or "-"
                        print(f"{topic.id:<5} {topic.status.value:<12} {topic.title:<50} {yt_id:<20}")
                
            elif command == "run":
                # Run pipeline for next pending topic
                success = orchestrator.run_for_next_topic()
                if not success:
                    print("\nNo pending topics to process.")
                
            elif command == "run-all":
                # Run pipeline for all pending topics
                max_iter = int(sys.argv[2]) if len(sys.argv) > 2 else None
                orchestrator.run_continuous(max_iterations=max_iter)
                
            elif command == "run-topic":
                # Run pipeline for specific topic ID
                if len(sys.argv) < 3:
                    print("Usage: python -m src.main run-topic <topic_id>")
                    sys.exit(1)
                
                topic_id = int(sys.argv[2])
                orchestrator.run_for_topic_id(topic_id)
                
            else:
                print(f"Unknown command: {command}")
                print_usage()
                
        else:
            # Interactive mode - run next pending topic
            logger.info("Running in interactive mode...")
            success = orchestrator.run_for_next_topic()
            
            if success:
                print("\n✅ Topic processed successfully!")
            else:
                print("\n❌ No pending topics to process.")
                print("   Use 'python -m src.main add-topic <title>' to add a topic.")
        
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"\n❌ Error: {e}")
        sys.exit(1)


def print_usage():
    """Print usage information."""
    print("""
Usage: python -m src.main [command] [args]

Commands:
  add-topic <title> [description] [niche]  - Add a new topic to process
  list-topics                              - List all topics
  run                                      - Process next pending topic
  run-all [max_count]                      - Process all pending topics
  run-topic <topic_id>                     - Process specific topic
  
Examples:
  python -m src.main add-topic "Climate Change" "Deep dive into climate science"
  python -m src.main list-topics
  python -m src.main run
  python -m src.main run-all 5
  python -m src.main run-topic 1
""")


if __name__ == "__main__":
    main()    
