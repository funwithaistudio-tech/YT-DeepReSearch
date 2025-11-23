"""Main entry point for YT-DeepReSearch system - Core Orchestrator (Phase 0).

This is the main orchestrator that manages the 8-phase research pipeline
using a job queue and workspace management system.
"""

import sys
import time
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from config import JobStatus, Phase
from orchestrator.job_queue import JobQueue
from utils.state import WorkspaceManager, TopicState

# Placeholder imports for phases (to be implemented)
from foundation.decomposition import decompose_topic
from foundation.research import research_subtopic
from foundation.compression import compress_research
from knowledge.graph import build_knowledge_graph
from knowledge.hierarchy import create_hierarchy
from narrative.planner import plan_narrative
from narrative.generator import generate_content


def execute_phase_1(state: TopicState) -> TopicState:
    """Execute Phase 1: Topic Decomposition.
    
    Args:
        state: Current topic state
        
    Returns:
        Updated state
    """
    print(f"[Phase 1] Decomposing topic: {state.topic}")
    # Placeholder: decompose_topic(state.topic)
    state.completed_phases.append(Phase.PHASE_1_DECOMPOSITION.value)
    state.current_phase = Phase.PHASE_2_RESEARCH
    return state


def execute_phase_2(state: TopicState) -> TopicState:
    """Execute Phase 2: Deep Research.
    
    Args:
        state: Current topic state
        
    Returns:
        Updated state
    """
    print(f"[Phase 2] Conducting research on: {state.topic}")
    # Placeholder: research_subtopic(state.topic)
    state.completed_phases.append(Phase.PHASE_2_RESEARCH.value)
    state.current_phase = Phase.PHASE_3_COMPRESSION
    return state


def execute_phase_3(state: TopicState) -> TopicState:
    """Execute Phase 3: Content Compression.
    
    Args:
        state: Current topic state
        
    Returns:
        Updated state
    """
    print(f"[Phase 3] Compressing research data")
    # Placeholder: compress_research({})
    state.completed_phases.append(Phase.PHASE_3_COMPRESSION.value)
    state.current_phase = Phase.PHASE_4_GRAPH_CONSTRUCTION
    return state


def execute_phase_4(state: TopicState) -> TopicState:
    """Execute Phase 4: Knowledge Graph Construction.
    
    Args:
        state: Current topic state
        
    Returns:
        Updated state
    """
    print(f"[Phase 4] Building knowledge graph")
    # Placeholder: build_knowledge_graph({})
    state.completed_phases.append(Phase.PHASE_4_GRAPH_CONSTRUCTION.value)
    state.current_phase = Phase.PHASE_5_HIERARCHY
    return state


def execute_phase_5(state: TopicState) -> TopicState:
    """Execute Phase 5: Hierarchical Organization.
    
    Args:
        state: Current topic state
        
    Returns:
        Updated state
    """
    print(f"[Phase 5] Creating hierarchical organization")
    # Placeholder: create_hierarchy({})
    state.completed_phases.append(Phase.PHASE_5_HIERARCHY.value)
    state.current_phase = Phase.PHASE_6_PLANNING
    return state


def execute_phase_6(state: TopicState) -> TopicState:
    """Execute Phase 6: Narrative Planning.
    
    Args:
        state: Current topic state
        
    Returns:
        Updated state
    """
    print(f"[Phase 6] Planning narrative structure")
    # Placeholder: plan_narrative({})
    state.completed_phases.append(Phase.PHASE_6_PLANNING.value)
    state.current_phase = Phase.PHASE_7_GENERATION
    return state


def execute_phase_7(state: TopicState) -> TopicState:
    """Execute Phase 7: Content Generation.
    
    Args:
        state: Current topic state
        
    Returns:
        Updated state
    """
    print(f"[Phase 7] Generating content")
    # Placeholder: generate_content({})
    state.completed_phases.append(Phase.PHASE_7_GENERATION.value)
    state.current_phase = Phase.PHASE_8_FINAL_OUTPUT
    return state


def execute_phase_8(state: TopicState) -> TopicState:
    """Execute Phase 8: Final Output.
    
    Args:
        state: Current topic state
        
    Returns:
        Updated state
    """
    print(f"[Phase 8] Finalizing output")
    state.completed_phases.append(Phase.PHASE_8_FINAL_OUTPUT.value)
    return state


def process_topic(topic: str, queue: JobQueue, workspace: WorkspaceManager) -> None:
    """Process a single topic through the pipeline.
    
    Args:
        topic: Research topic
        queue: Job queue instance
        workspace: Workspace manager instance
    """
    start_time = datetime.now()
    
    try:
        # Update status to In_Progress
        queue.update_status(
            topic=topic,
            status=JobStatus.IN_PROGRESS,
            timestamp_start=start_time.isoformat()
        )
        
        # Create workspace
        workspace_id = workspace.create_workspace(topic)
        print(f"Created workspace: {workspace_id}")
        
        # Initialize state
        state = workspace.init_state(workspace_id, topic)
        
        # Execute phases
        print(f"\nProcessing topic: {topic}\n")
        print("=" * 60)
        
        state = execute_phase_1(state)
        workspace.save_state(workspace_id, state)
        
        state = execute_phase_2(state)
        workspace.save_state(workspace_id, state)
        
        state = execute_phase_3(state)
        workspace.save_state(workspace_id, state)
        
        state = execute_phase_4(state)
        workspace.save_state(workspace_id, state)
        
        state = execute_phase_5(state)
        workspace.save_state(workspace_id, state)
        
        state = execute_phase_6(state)
        workspace.save_state(workspace_id, state)
        
        state = execute_phase_7(state)
        workspace.save_state(workspace_id, state)
        
        state = execute_phase_8(state)
        workspace.save_state(workspace_id, state)
        
        print("=" * 60)
        print(f"\nCompleted all phases for topic: {topic}\n")
        
        # Update status to Completed
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        queue.update_status(
            topic=topic,
            status=JobStatus.COMPLETED,
            timestamp_end=end_time.isoformat(),
            duration_seconds=duration,
            notes=f"Workspace: {workspace_id}"
        )
        
    except Exception as e:
        # Handle errors
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        error_message = str(e)
        
        print(f"\nError processing topic '{topic}': {error_message}\n")
        
        queue.update_status(
            topic=topic,
            status=JobStatus.ERROR,
            timestamp_end=end_time.isoformat(),
            duration_seconds=duration,
            error_message=error_message
        )


def main():
    """Main orchestrator loop."""
    print("YT-DeepReSearch Core Orchestrator (Phase 0)")
    print("=" * 60)
    
    # Initialize components
    queue = JobQueue()
    workspace = WorkspaceManager()
    
    print(f"Job queue file: {queue.queue_file}")
    print(f"Projects directory: {workspace.base_dir}")
    print("=" * 60)
    
    # Main processing loop
    while True:
        # Get next pending topic
        topic = queue.get_next_pending_topic()
        
        if not topic:
            print("\nNo pending topics in queue.")
            print("Add topics to the queue Excel file to process them.")
            break
        
        # Process topic
        process_topic(topic, queue, workspace)
        
        # Brief pause between topics
        time.sleep(1)
    
    print("\nOrchestrator finished.")


if __name__ == "__main__":
    main()    
