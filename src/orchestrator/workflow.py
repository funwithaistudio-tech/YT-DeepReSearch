"""Orchestrator workflow for managing the research pipeline."""

import time
import traceback
from datetime import datetime
from typing import Optional
from pathlib import Path

from orchestrator.job_queue import JobQueue
from utils.state import StateManager


class Orchestrator:
    """
    Main orchestrator for managing the research workflow.
    
    Coordinates job queue, state management, and pipeline phases.
    """
    
    def __init__(
        self,
        job_queue_path: str = "job_queue.xlsx",
        projects_dir: str = "projects"
    ):
        """
        Initialize Orchestrator.
        
        Args:
            job_queue_path: Path to Excel job queue
            projects_dir: Base directory for project workspaces
        """
        self.job_queue = JobQueue(job_queue_path)
        self.projects_dir = projects_dir
        self.state_manager: Optional[StateManager] = None
    
    def run(self, max_iterations: Optional[int] = None):
        """
        Run the orchestrator main loop.
        
        Args:
            max_iterations: Maximum number of jobs to process (None = unlimited)
        """
        print("Orchestrator starting...")
        iteration = 0
        
        while True:
            # Check iteration limit
            if max_iterations and iteration >= max_iterations:
                print(f"Reached max iterations ({max_iterations}). Stopping.")
                break
            
            iteration += 1
            
            # Get next pending job
            topic = self.job_queue.get_next_pending_job()
            
            if not topic:
                print("No pending jobs found. Waiting...")
                time.sleep(5)
                continue
            
            print(f"\n{'='*60}")
            print(f"Processing job: {topic}")
            print(f"{'='*60}\n")
            
            # Try to claim the job
            if not self.job_queue.claim_job(topic):
                print(f"Failed to claim job: {topic}. Skipping.")
                continue
            
            # Process the job
            try:
                self._process_job(topic)
                print(f"\n✓ Job completed successfully: {topic}\n")
            except Exception as e:
                error_msg = f"Job failed: {str(e)}\n{traceback.format_exc()}"
                print(f"\n✗ Job failed: {topic}")
                print(f"Error: {error_msg}\n")
                
                # Update job as error
                self.job_queue.update_job_status(
                    topic=topic,
                    status="Error",
                    error_message=str(e)
                )
    
    def _process_job(self, topic: str):
        """
        Process a single job through all pipeline phases.
        
        Args:
            topic: Research topic to process
        """
        # Initialize state manager and workspace
        self.state_manager = StateManager(self.projects_dir)
        workspace_path = self.state_manager.create_workspace(topic)
        
        print(f"Workspace created: {workspace_path}")
        
        try:
            # Execute pipeline phases
            print("\nExecuting pipeline phases...")
            
            # Phase 1: Foundation Research
            print("\n[Phase 1] Foundation Research")
            self._phase_1_foundation_research(topic)
            
            # Phase 2: Deep Dive Research
            print("\n[Phase 2] Deep Dive Research")
            self._phase_2_deep_dive_research(topic)
            
            # Phase 3: Cross-Validation
            print("\n[Phase 3] Cross-Validation")
            self._phase_3_cross_validation(topic)
            
            # Phase 4: Knowledge Graph Construction
            print("\n[Phase 4] Knowledge Graph Construction")
            self._phase_4_knowledge_graph(topic)
            
            # Phase 5: Hierarchical Clustering
            print("\n[Phase 5] Hierarchical Clustering")
            self._phase_5_hierarchical_clustering(topic)
            
            # Phase 6: Narrative Generation
            print("\n[Phase 6] Narrative Generation")
            self._phase_6_narrative_generation(topic)
            
            # Phase 7: Final Review & Refinement
            print("\n[Phase 7] Final Review & Refinement")
            self._phase_7_final_review(topic)
            
            # Phase 8: Output & Archival
            print("\n[Phase 8] Output & Archival")
            self._phase_8_output_archival(topic)
            
            # Update manifest with completion
            self.state_manager.update_manifest({
                "status": "completed",
                "completed_at": datetime.now().isoformat()
            })
            
            # Update job queue as completed
            self.job_queue.update_job_status(
                topic=topic,
                status="Completed",
                output_path=workspace_path
            )
            
        except Exception as e:
            # Update manifest with error
            if self.state_manager:
                self.state_manager.update_manifest({
                    "status": "error",
                    "error": str(e)
                })
            raise
    
    # Placeholder functions for pipeline phases
    
    def _phase_1_foundation_research(self, topic: str):
        """
        Phase 1: Foundation Research (Placeholder).
        
        Args:
            topic: Research topic
        """
        print("  → Conducting foundation research...")
        # TODO: Implement actual research logic
        phase_data = {
            "status": "completed",
            "description": "Foundation research phase (placeholder)"
        }
        self.state_manager.mark_phase_complete(1, phase_data)
        print("  ✓ Phase 1 complete")
    
    def _phase_2_deep_dive_research(self, topic: str):
        """
        Phase 2: Deep Dive Research (Placeholder).
        
        Args:
            topic: Research topic
        """
        print("  → Conducting deep dive research...")
        # TODO: Implement actual research logic
        phase_data = {
            "status": "completed",
            "description": "Deep dive research phase (placeholder)"
        }
        self.state_manager.mark_phase_complete(2, phase_data)
        print("  ✓ Phase 2 complete")
    
    def _phase_3_cross_validation(self, topic: str):
        """
        Phase 3: Cross-Validation (Placeholder).
        
        Args:
            topic: Research topic
        """
        print("  → Performing cross-validation...")
        # TODO: Implement actual validation logic
        phase_data = {
            "status": "completed",
            "description": "Cross-validation phase (placeholder)"
        }
        self.state_manager.mark_phase_complete(3, phase_data)
        print("  ✓ Phase 3 complete")
    
    def _phase_4_knowledge_graph(self, topic: str):
        """
        Phase 4: Knowledge Graph Construction (Placeholder).
        
        Args:
            topic: Research topic
        """
        print("  → Building knowledge graph...")
        # TODO: Implement actual graph construction logic
        phase_data = {
            "status": "completed",
            "description": "Knowledge graph construction phase (placeholder)"
        }
        self.state_manager.mark_phase_complete(4, phase_data)
        print("  ✓ Phase 4 complete")
    
    def _phase_5_hierarchical_clustering(self, topic: str):
        """
        Phase 5: Hierarchical Clustering (Placeholder).
        
        Args:
            topic: Research topic
        """
        print("  → Performing hierarchical clustering...")
        # TODO: Implement actual clustering logic
        phase_data = {
            "status": "completed",
            "description": "Hierarchical clustering phase (placeholder)"
        }
        self.state_manager.mark_phase_complete(5, phase_data)
        print("  ✓ Phase 5 complete")
    
    def _phase_6_narrative_generation(self, topic: str):
        """
        Phase 6: Narrative Generation (Placeholder).
        
        Args:
            topic: Research topic
        """
        print("  → Generating narrative...")
        # TODO: Implement actual narrative generation logic
        phase_data = {
            "status": "completed",
            "description": "Narrative generation phase (placeholder)"
        }
        self.state_manager.mark_phase_complete(6, phase_data)
        print("  ✓ Phase 6 complete")
    
    def _phase_7_final_review(self, topic: str):
        """
        Phase 7: Final Review & Refinement (Placeholder).
        
        Args:
            topic: Research topic
        """
        print("  → Performing final review...")
        # TODO: Implement actual review logic
        phase_data = {
            "status": "completed",
            "description": "Final review phase (placeholder)"
        }
        self.state_manager.mark_phase_complete(7, phase_data)
        print("  ✓ Phase 7 complete")
    
    def _phase_8_output_archival(self, topic: str):
        """
        Phase 8: Output & Archival (Placeholder).
        
        Args:
            topic: Research topic
        """
        print("  → Archiving outputs...")
        # TODO: Implement actual archival logic
        phase_data = {
            "status": "completed",
            "description": "Output & archival phase (placeholder)"
        }
        self.state_manager.mark_phase_complete(8, phase_data)
        print("  ✓ Phase 8 complete")
    
    def process_single_job(self, topic: str):
        """
        Process a single job directly (for testing/debugging).
        
        Args:
            topic: Research topic to process
        """
        print(f"Processing single job: {topic}")
        
        # Add job to queue if it doesn't exist
        self.job_queue.add_job(topic)
        
        # Claim and process
        if self.job_queue.claim_job(topic):
            self._process_job(topic)
        else:
            print(f"Failed to claim job: {topic}")
