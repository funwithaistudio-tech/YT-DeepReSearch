"""Orchestrator for managing the research pipeline workflow."""

import logging
from pathlib import Path
from typing import Optional

from utils.state import StateManager
from orchestrator.job_queue import JobQueue


class Orchestrator:
    """Orchestrates the entire research pipeline workflow."""

    def __init__(
        self,
        queue_file: str = "topics.xlsx",
        workspace_dir: str = "workspaces",
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize Orchestrator.
        
        Args:
            queue_file: Path to the Excel job queue file
            workspace_dir: Base directory for workspaces
            logger: Optional logger instance
        """
        self.job_queue = JobQueue(queue_file=queue_file)
        self.state_manager = StateManager(base_workspace_dir=workspace_dir)
        self.logger = logger or logging.getLogger(__name__)

    def run(self, max_iterations: int = 1) -> None:
        """
        Run the orchestrator main loop.
        
        Args:
            max_iterations: Maximum number of topics to process (0 for infinite)
        """
        self.logger.info("Starting Orchestrator...")
        
        iteration = 0
        while max_iterations == 0 or iteration < max_iterations:
            iteration += 1
            
            # Step 1: Find next pending topic
            topic = self.job_queue.get_next_pending_topic()
            if topic is None:
                self.logger.info("No pending topics found. Exiting.")
                break
            
            self.logger.info(f"Processing topic: {topic}")
            
            # Step 2: Claim the topic
            if not self.job_queue.claim_topic(topic):
                self.logger.warning(f"Failed to claim topic: {topic}. Skipping.")
                continue
            
            self.logger.info(f"Successfully claimed topic: {topic}")
            
            try:
                # Step 3: Create workspace
                workspace_path = self.state_manager.create_workspace(topic)
                self.logger.info(f"Created workspace: {workspace_path}")
                
                # Initialize state
                state = self.state_manager.init_state(workspace_path, topic)
                self.logger.info(f"Initialized state for topic: {topic}")
                
                # Step 4: Execute pipeline (placeholder)
                self.logger.info("Executing pipeline...")
                self._execute_pipeline(topic, workspace_path, state)
                
                # Step 5: Update status to Completed
                self.job_queue.update_status(topic, "Completed")
                self.logger.info(f"Successfully completed topic: {topic}")
                
            except Exception as e:
                self.logger.error(f"Error processing topic '{topic}': {str(e)}")
                self.job_queue.update_status(topic, "Failed", error=str(e))
        
        self.logger.info("Orchestrator finished.")

    def _execute_pipeline(
        self, 
        topic: str, 
        workspace_path: Path, 
        state: dict
    ) -> None:
        """
        Execute the research pipeline for a topic.
        
        This is a placeholder for the actual pipeline implementation.
        In future phases, this will call:
        - Foundation phase
        - Knowledge phase
        - Narrative phase
        
        Args:
            topic: Research topic
            workspace_path: Path to workspace directory
            state: Current state dictionary
        """
        self.logger.info(f"[PLACEHOLDER] Executing pipeline for topic: {topic}")
        self.logger.info(f"[PLACEHOLDER] Workspace: {workspace_path}")
        
        # Placeholder: Update state with completed phases
        state["phases_completed"].append("foundation")
        state["phases_completed"].append("knowledge")
        state["phases_completed"].append("narrative")
        state["status"] = "pipeline_completed"
        
        # Save updated state
        self.state_manager.save_state(workspace_path, state)
        
        self.logger.info("[PLACEHOLDER] Pipeline execution completed")

    def get_queue_status(self) -> dict:
        """
        Get current status of the job queue.
        
        Returns:
            Dictionary with queue statistics
        """
        all_topics = self.job_queue.get_all_topics()
        
        status_counts = {
            "Pending": 0,
            "In_Progress": 0,
            "Completed": 0,
            "Failed": 0
        }
        
        for topic_data in all_topics:
            status = topic_data.get("status", "Unknown")
            if status in status_counts:
                status_counts[status] += 1
            else:
                status_counts[status] = 1
        
        return {
            "total_topics": len(all_topics),
            "status_breakdown": status_counts,
            "topics": all_topics
        }
