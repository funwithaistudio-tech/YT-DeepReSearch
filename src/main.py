"""Main entry point for YT-DeepReSearch system."""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from loguru import logger

from orchestrator.workflow import orchestrator_main_loop


def main():
    """Main execution function."""
    # Setup logging
    logger.info("Starting YT-DeepReSearch system with Orchestrator...")
    
    try:
        # Run orchestrator workflow
        # Process up to 3 topics for testing, then stop
        # Set max_iterations=0 for infinite loop in production
        orchestrator_main_loop(
            excel_path="job_queue/topics.xlsx",
            max_iterations=3,
            iteration_delay=2,
        )
        
    except KeyboardInterrupt:
        logger.info("System interrupted by user")
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()    
