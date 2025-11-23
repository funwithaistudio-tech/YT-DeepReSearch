"""State management and workspace utilities.

This module provides state management for topics and workspace organization.
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

from pydantic import BaseModel, Field

from config import PROJECTS_DIR, MANIFEST_FILENAME, STATE_FILENAME, Phase


class TopicState(BaseModel):
    """Pydantic model for topic state tracking."""
    
    topic: str = Field(..., description="Research topic")
    workspace_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique workspace identifier")
    current_phase: Phase = Field(default=Phase.PHASE_0_ORCHESTRATION, description="Current pipeline phase")
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Creation timestamp")
    updated_at: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Last update timestamp")
    
    # Phase completion tracking
    completed_phases: list[str] = Field(default_factory=list, description="List of completed phases")
    
    # Artifacts and outputs
    artifacts: Dict[str, Any] = Field(default_factory=dict, description="Phase artifacts and intermediate outputs")
    
    # Metadata
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    # Error tracking
    errors: list[Dict[str, str]] = Field(default_factory=list, description="Error history")
    
    class Config:
        use_enum_values = True


class WorkspaceManager:
    """Manages workspace creation and state persistence."""
    
    def __init__(self, base_dir: Optional[Path] = None):
        """Initialize workspace manager.
        
        Args:
            base_dir: Base directory for workspaces. Defaults to PROJECTS_DIR.
        """
        self.base_dir = base_dir or PROJECTS_DIR
        self.base_dir.mkdir(parents=True, exist_ok=True)
    
    def create_workspace(self, topic: str) -> str:
        """Create a unique workspace folder for a topic.
        
        Args:
            topic: Research topic
            
        Returns:
            Workspace ID (folder name)
        """
        workspace_id = str(uuid.uuid4())
        workspace_path = self.base_dir / workspace_id
        workspace_path.mkdir(parents=True, exist_ok=True)
        
        return workspace_id
    
    def get_workspace_path(self, workspace_id: str) -> Path:
        """Get path to workspace directory.
        
        Args:
            workspace_id: Workspace identifier
            
        Returns:
            Path to workspace directory
        """
        return self.base_dir / workspace_id
    
    def save_manifest(self, workspace_id: str, manifest_data: Dict[str, Any]) -> None:
        """Save manifest metadata to workspace.
        
        Args:
            workspace_id: Workspace identifier
            manifest_data: Manifest data to save
        """
        workspace_path = self.get_workspace_path(workspace_id)
        manifest_path = workspace_path / MANIFEST_FILENAME
        
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest_data, f, indent=2, ensure_ascii=False)
    
    def save_state(self, workspace_id: str, state: TopicState) -> None:
        """Save topic state to workspace.
        
        Args:
            workspace_id: Workspace identifier
            state: TopicState object to save
        """
        workspace_path = self.get_workspace_path(workspace_id)
        state_path = workspace_path / STATE_FILENAME
        
        # Update timestamp
        state.updated_at = datetime.now().isoformat()
        
        with open(state_path, 'w', encoding='utf-8') as f:
            json.dump(state.model_dump(), f, indent=2, ensure_ascii=False)
    
    def load_state(self, workspace_id: str) -> Optional[TopicState]:
        """Load topic state from workspace.
        
        Args:
            workspace_id: Workspace identifier
            
        Returns:
            TopicState object if found, None otherwise
        """
        workspace_path = self.get_workspace_path(workspace_id)
        state_path = workspace_path / STATE_FILENAME
        
        if not state_path.exists():
            return None
        
        with open(state_path, 'r', encoding='utf-8') as f:
            state_data = json.load(f)
        
        return TopicState(**state_data)
    
    def init_state(self, workspace_id: str, topic: str) -> TopicState:
        """Initialize a new topic state for a workspace.
        
        Args:
            workspace_id: Workspace identifier
            topic: Research topic
            
        Returns:
            Initialized TopicState object
        """
        state = TopicState(
            topic=topic,
            workspace_id=workspace_id
        )
        
        # Save initial manifest
        manifest_data = {
            "workspace_id": workspace_id,
            "topic": topic,
            "created_at": state.created_at,
            "pipeline_version": "1.0.0"
        }
        self.save_manifest(workspace_id, manifest_data)
        
        # Save initial state
        self.save_state(workspace_id, state)
        
        return state
