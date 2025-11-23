"""Main entry point for YT-DeepReSearch system."""

import sys
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import Settings
from orchestrator.pipeline_orchestrator import PipelineOrchestrator
from orchestrator.excel_queue_manager import ExcelQueueManager
from utils.logger import setup_logger


def run_single_topic(topic: str, settings: Settings):
    """
    Run pipeline for a single topic.
    
    Args:
        topic: Research topic
        settings: Application settings
    """
    logger = setup_logger(settings.log_file, settings.log_level)
    
    logger.info(f"Running single topic mode: {topic}")
    
    # Initialize orchestrator
    orchestrator = PipelineOrchestrator(settings)
    
    # Execute pipeline
    result = orchestrator.execute_pipeline(topic)
    
    if result["status"] == "completed":
        logger.info(f"✅ Successfully completed pipeline for: {topic}")
        logger.info(f"Output directory: {result.get('output_directory')}")
        print(f"\n{'='*80}")
        print(f"✅ SUCCESS: Script generated for '{topic}'")
        print(f"📁 Output: {result.get('output_directory')}")
        print(f"{'='*80}\n")
    else:
        logger.error(f"❌ Pipeline failed for: {topic}")
        print(f"\n{'='*80}")
        print(f"❌ FAILED: Pipeline failed for '{topic}'")
        print(f"Error: {result.get('error', 'Unknown error')}")
        print(f"{'='*80}\n")
        sys.exit(1)


def run_excel_queue(settings: Settings):
    """
    Run pipeline for all pending topics in Excel queue.
    
    Args:
        settings: Application settings
    """
    logger = setup_logger(settings.log_file, settings.log_level)
    
    logger.info("Running Excel queue mode")
    
    # Initialize managers
    queue_manager = ExcelQueueManager(settings.excel_input_path, settings.excel_sheet_name)
    orchestrator = PipelineOrchestrator(settings)
    
    # Get pending topics
    pending_topics = queue_manager.get_pending_topics()
    
    if not pending_topics:
        logger.info("No pending topics found in queue")
        print("No pending topics found in Excel queue.")
        return
    
    logger.info(f"Found {len(pending_topics)} pending topics")
    print(f"\n{'='*80}")
    print(f"📋 Processing {len(pending_topics)} pending topics from Excel queue")
    print(f"{'='*80}\n")
    
    # Process each topic
    for i, topic_info in enumerate(pending_topics, 1):
        topic_index = topic_info["index"]
        topic = topic_info["topic"]
        
        logger.info(f"Processing topic {i}/{len(pending_topics)}: {topic}")
        print(f"\n[{i}/{len(pending_topics)}] Processing: {topic}")
        
        # Update status to processing
        queue_manager.update_status(topic_index, "processing")
        
        try:
            # Execute pipeline
            result = orchestrator.execute_pipeline(topic)
            
            if result["status"] == "completed":
                # Update status to completed
                queue_manager.update_status(
                    topic_index,
                    "completed",
                    output_dir=result.get("output_directory")
                )
                logger.info(f"✅ Completed: {topic}")
                print(f"✅ Success: {topic}")
            else:
                # Update status to failed
                error_msg = result.get("error", f"Failed at phase {result.get('error_phase', 'unknown')}")
                queue_manager.update_status(
                    topic_index,
                    "failed",
                    error_message=error_msg
                )
                logger.error(f"❌ Failed: {topic} - {error_msg}")
                print(f"❌ Failed: {topic}")
        
        except Exception as e:
            logger.error(f"Exception while processing {topic}: {str(e)}")
            queue_manager.update_status(
                topic_index,
                "failed",
                error_message=str(e)
            )
            print(f"❌ Error: {topic}")
    
    # Print statistics
    stats = queue_manager.get_statistics()
    print(f"\n{'='*80}")
    print(f"📊 Queue Statistics:")
    print(f"   Total: {stats.get('total', 0)}")
    print(f"   Completed: {stats.get('completed', 0)}")
    print(f"   Failed: {stats.get('failed', 0)}")
    print(f"   Pending: {stats.get('pending', 0)}")
    print(f"{'='*80}\n")


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="YT-DeepReSearch: AI-powered deep research system for educational video scripts"
    )
    
    parser.add_argument(
        "--mode",
        choices=["single", "queue"],
        default="single",
        help="Execution mode: 'single' for one topic, 'queue' for Excel queue"
    )
    
    parser.add_argument(
        "--topic",
        type=str,
        help="Research topic (required for single mode)"
    )
    
    args = parser.parse_args()
    
    # Load settings
    settings = Settings()
    
    # Execute based on mode
    if args.mode == "single":
        if not args.topic:
            print("Error: --topic is required for single mode")
            print("Usage: python main.py --mode single --topic 'Your Topic Here'")
            sys.exit(1)
        
        run_single_topic(args.topic, settings)
    
    elif args.mode == "queue":
        run_excel_queue(settings)


if __name__ == "__main__":
    main()    
