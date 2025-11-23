"""Main orchestrator workflow for the YT-DeepReSearch pipeline."""

import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from orchestrator.job_queue import JobQueue
from utils import state as state_manager


def execute_phase_placeholder(phase_num: int, topic: str, state: dict):
    """
    Placeholder for phase execution.
    
    Args:
        phase_num: Phase number (1-8)
        topic: Topic name
        state: Current state dictionary
    """
    print(f"  [Phase {phase_num}] Executing Phase {phase_num} for topic: {topic}...")
    # In future phases, actual implementation will go here
    # For now, just update state
    state_manager.update_phase_status(state, phase_num, "completed")


def orchestrator_main_loop(excel_path: str = "topics.xlsx", max_topics: Optional[int] = None):
    """
    Main orchestrator loop that processes topics from the queue.
    
    Args:
        excel_path: Path to Excel file with topics
        max_topics: Maximum number of topics to process (None for all)
    """
    print("=" * 60)
    print("YT-DeepReSearch Orchestrator - Phase 0")
    print("=" * 60)
    
    # Initialize job queue
    queue = JobQueue(excel_path)
    print(f"✓ Job queue initialized: {excel_path}")
    
    topics_processed = 0
    
    # Main loop
    while True:
        # Check if we've reached max topics
        if max_topics and topics_processed >= max_topics:
            print(f"\n✓ Reached maximum topics limit ({max_topics})")
            break
        
        # Get next pending topic
        print("\n" + "-" * 60)
        print("Checking for pending topics...")
        
        next_topic = queue.get_next_pending()
        
        if next_topic is None:
            print("✓ No more pending topics in queue")
            break
        
        row_index = next_topic["row_index"]
        topic = next_topic["topic"]
        
        print(f"✓ Found pending topic: '{topic}' (row {row_index})")
        
        # Claim the topic
        if not queue.claim_topic(row_index, topic):
            print(f"✗ Failed to claim topic: '{topic}'")
            continue
        
        print(f"✓ Topic claimed and marked as In_Progress")
        
        # Track start time
        start_time = datetime.now()
        
        try:
            # Create workspace
            workspace_path = state_manager.create_workspace(topic)
            print(f"✓ Workspace created: {workspace_path}")
            
            # Initialize state
            state = state_manager.initialize_state(topic, workspace_path)
            state_manager.save_state(state)
            print(f"✓ State initialized and saved")
            
            # Execute phases 1-8 (placeholders for now)
            print("\nExecuting pipeline phases:")
            for phase in range(1, 9):
                execute_phase_placeholder(phase, topic, state)
                state_manager.save_state(state)
            
            # Calculate duration
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            # Update queue with completion
            queue.update_status(
                topic=topic,
                status="Completed",
                end_time=end_time,
                duration=duration,
                workspace_path=workspace_path
            )
            
            print(f"\n✓ Topic '{topic}' completed successfully!")
            print(f"  Duration: {duration:.2f} seconds")
            print(f"  Workspace: {workspace_path}")
            
            topics_processed += 1
            
        except Exception as e:
            # Handle errors
            error_message = str(e)
            print(f"\n✗ Error processing topic '{topic}': {error_message}")
            
            # Update queue with error
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            queue.update_status(
                topic=topic,
                status="Failed",
                end_time=end_time,
                duration=duration,
                error_message=error_message
            )
            
            topics_processed += 1
    
    # Summary
    print("\n" + "=" * 60)
    print(f"Orchestrator completed: {topics_processed} topics processed")
    print("=" * 60)


if __name__ == "__main__":
    # Can be run directly for testing
    orchestrator_main_loop()
