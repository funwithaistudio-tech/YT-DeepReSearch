"""Main entry point for YT-DeepReSearch system."""

import os
import sys
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from orchestrator.workflow import Orchestrator
from orchestrator.job_queue import JobQueue


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="YT-DeepReSearch: AI-powered deep research system"
    )
    parser.add_argument(
        "--mode",
        choices=["orchestrator", "single"],
        default="orchestrator",
        help="Run mode: 'orchestrator' for continuous processing, 'single' for one-off job"
    )
    parser.add_argument(
        "--topic",
        type=str,
        help="Topic to research (required for 'single' mode)"
    )
    parser.add_argument(
        "--job-queue",
        type=str,
        default="job_queue.xlsx",
        help="Path to job queue Excel file (default: job_queue.xlsx)"
    )
    parser.add_argument(
        "--projects-dir",
        type=str,
        default="projects",
        help="Base directory for project workspaces (default: projects)"
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        help="Maximum number of jobs to process (for testing)"
    )
    
    args = parser.parse_args()
    
    try:
        if args.mode == "orchestrator":
            # Run orchestrator in continuous mode
            print("Starting YT-DeepReSearch Orchestrator...")
            print(f"Job queue: {args.job_queue}")
            print(f"Projects directory: {args.projects_dir}")
            print("")
            
            orchestrator = Orchestrator(
                job_queue_path=args.job_queue,
                projects_dir=args.projects_dir
            )
            orchestrator.run(max_iterations=args.max_iterations)
            
        elif args.mode == "single":
            # Process a single topic
            if not args.topic:
                print("Error: --topic is required for 'single' mode")
                sys.exit(1)
            
            print(f"Processing single topic: {args.topic}")
            print(f"Job queue: {args.job_queue}")
            print(f"Projects directory: {args.projects_dir}")
            print("")
            
            orchestrator = Orchestrator(
                job_queue_path=args.job_queue,
                projects_dir=args.projects_dir
            )
            orchestrator.process_single_job(args.topic)
            
    except KeyboardInterrupt:
        print("\n\nShutting down gracefully...")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()    
