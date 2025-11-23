"""Main entry point for YT-DeepReSearch system."""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from orchestrator.workflow import orchestrator_main_loop


def main():
    """Main execution function."""
    print("Starting YT-DeepReSearch system...")
    
    # Check if topics.xlsx exists, if not provide helpful message
    topics_file = "topics.xlsx"
    if not Path(topics_file).exists():
        print(f"\n⚠ Warning: '{topics_file}' not found.")
        print("The orchestrator will create it automatically with headers.")
        print("Please add topics to the file with Status='Pending' and run again.\n")
    
    try:
        # Run the orchestrator main loop
        orchestrator_main_loop(excel_path=topics_file)
        
    except KeyboardInterrupt:
        print("\n\nOrchestrator interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()    
