"""State management for workspace and persistence."""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional


class StateManager:
    """
    Manages workspace directories and state persistence for research jobs.
    
    Workspace structure:
    projects/{uuid}/
        - manifest.json: Job metadata (topic, start time, etc.)
        - state.json: Current state for resumability
        - phase_outputs/: Output from each phase
    """
    
    def __init__(self, base_dir: str = "projects"):
        """
        Initialize StateManager.
        
        Args:
            base_dir: Base directory for all project workspaces
        """
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        self.workspace_path: Optional[Path] = None
        self.manifest: Dict[str, Any] = {}
        self.state: Dict[str, Any] = {}
    
    def create_workspace(self, topic: str) -> str:
        """
        Create a unique workspace directory for a topic.
        
        Args:
            topic: Research topic
            
        Returns:
            Path to the created workspace
        """
        # Generate unique ID
        workspace_id = str(uuid.uuid4())
        self.workspace_path = self.base_dir / workspace_id
        self.workspace_path.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        (self.workspace_path / "phase_outputs").mkdir(exist_ok=True)
        
        # Initialize manifest
        self.manifest = {
            "workspace_id": workspace_id,
            "topic": topic,
            "created_at": datetime.now().isoformat(),
            "status": "initialized",
            "phases": {}
        }
        
        # Initialize state
        self.state = {
            "current_phase": 0,
            "completed_phases": [],
            "phase_data": {}
        }
        
        # Save manifest and state
        self.save_manifest()
        self.save_state()
        
        return str(self.workspace_path)
    
    def load_workspace(self, workspace_path: str):
        """
        Load an existing workspace.
        
        Args:
            workspace_path: Path to workspace directory
        """
        self.workspace_path = Path(workspace_path)
        
        if not self.workspace_path.exists():
            raise ValueError(f"Workspace not found: {workspace_path}")
        
        # Load manifest and state
        manifest_path = self.workspace_path / "manifest.json"
        state_path = self.workspace_path / "state.json"
        
        if manifest_path.exists():
            with open(manifest_path, 'r') as f:
                self.manifest = json.load(f)
        else:
            self.manifest = {}
        
        if state_path.exists():
            with open(state_path, 'r') as f:
                self.state = json.load(f)
        else:
            self.state = {
                "current_phase": 0,
                "completed_phases": [],
                "phase_data": {}
            }
    
    def save_manifest(self):
        """Save manifest.json to workspace."""
        if not self.workspace_path:
            raise ValueError("No workspace initialized")
        
        manifest_path = self.workspace_path / "manifest.json"
        with open(manifest_path, 'w') as f:
            json.dump(self.manifest, f, indent=2)
    
    def save_state(self):
        """Save state.json to workspace for resumability."""
        if not self.workspace_path:
            raise ValueError("No workspace initialized")
        
        state_path = self.workspace_path / "state.json"
        with open(state_path, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def load_state(self) -> Dict[str, Any]:
        """
        Load state.json from workspace.
        
        Returns:
            State dictionary
        """
        if not self.workspace_path:
            raise ValueError("No workspace initialized")
        
        state_path = self.workspace_path / "state.json"
        
        if not state_path.exists():
            return {
                "current_phase": 0,
                "completed_phases": [],
                "phase_data": {}
            }
        
        with open(state_path, 'r') as f:
            self.state = json.load(f)
        
        return self.state
    
    def update_manifest(self, updates: Dict[str, Any]):
        """
        Update manifest with new data.
        
        Args:
            updates: Dictionary of updates to apply
        """
        self.manifest.update(updates)
        self.save_manifest()
    
    def update_state(self, updates: Dict[str, Any]):
        """
        Update state with new data.
        
        Args:
            updates: Dictionary of updates to apply
        """
        self.state.update(updates)
        self.save_state()
    
    def mark_phase_complete(self, phase_number: int, phase_data: Dict[str, Any]):
        """
        Mark a phase as complete and save its data.
        
        Args:
            phase_number: Phase number (1-8)
            phase_data: Data from the completed phase
        """
        if phase_number not in self.state.get("completed_phases", []):
            self.state["completed_phases"].append(phase_number)
        
        self.state["phase_data"][str(phase_number)] = phase_data
        self.state["current_phase"] = phase_number + 1
        
        # Update manifest
        self.manifest["phases"][str(phase_number)] = {
            "completed_at": datetime.now().isoformat(),
            "status": "completed"
        }
        
        self.save_state()
        self.save_manifest()
    
    def get_phase_output_path(self, phase_number: int) -> Path:
        """
        Get the output directory path for a specific phase.
        
        Args:
            phase_number: Phase number
            
        Returns:
            Path to phase output directory
        """
        if not self.workspace_path:
            raise ValueError("No workspace initialized")
        
        phase_dir = self.workspace_path / "phase_outputs" / f"phase_{phase_number}"
        phase_dir.mkdir(parents=True, exist_ok=True)
        
        return phase_dir
    
    def get_workspace_path(self) -> Optional[str]:
        """
        Get the current workspace path.
        
        Returns:
            Workspace path or None if not initialized
        """
        return str(self.workspace_path) if self.workspace_path else None
