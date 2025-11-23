"""Main entry point for YT-DeepReSearch system."""

import logging
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from orchestrator.workflow import Orchestrator


def setup_logging() -> logging.Logger:
    """Setup basic logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('orchestrator.log')
        ]
    )
    return logging.getLogger(__name__)


def main():
    """Main execution function."""
    # Setup logging
    logger = setup_logging()
    logger.info("Starting YT-DeepReSearch Orchestrator...")
    
    try:
        # Initialize orchestrator
        orchestrator = Orchestrator(
            queue_file="topics.xlsx",
            workspace_dir="workspaces",
            logger=logger
        )
        
        # Display queue status
        logger.info("Current queue status:")
        status = orchestrator.get_queue_status()
        logger.info(f"Total topics: {status['total_topics']}")
        logger.info(f"Status breakdown: {status['status_breakdown']}")
        
        # Run orchestrator (process one topic at a time)
        orchestrator.run(max_iterations=1)
        
        # Display final queue status
        logger.info("\nFinal queue status:")
        final_status = orchestrator.get_queue_status()
        logger.info(f"Status breakdown: {final_status['status_breakdown']}")
        
        print("\n✓ Orchestrator completed successfully!")
        
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
