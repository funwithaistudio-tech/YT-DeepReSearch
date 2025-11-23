"""Main entry point for YT-DeepReSearch system.

This script runs the deep research pipeline for one pending topic from the database.
"""

import sys
from pathlib import Path

# Add src to path for direct execution
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config.settings import Settings
from src.orchestrator.orchestrator import Orchestrator


def main():
    """Main execution function.
    
    Loads configuration and runs the pipeline for the next pending topic.
    """
    try:
        # Load configuration from environment
        settings = Settings()
        
        # Initialize orchestrator
        orchestrator = Orchestrator(settings)
        
        # Run pipeline for next topic
        processed = orchestrator.run_for_next_topic()
        
        # Clean up
        orchestrator.close()
        
        # Exit with appropriate code
        sys.exit(0 if processed else 1)
        
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()    
