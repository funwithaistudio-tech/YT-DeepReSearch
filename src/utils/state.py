"""State management for research workspaces."""

import hashlib
import json
from pathlib import Path
from typing import Any, Dict


class StateManager:
    """Manages workspace state for research topics."""

    def __init__(self, base_workspace_dir: str = "workspaces"):
        """
        Initialize StateManager.
        
        Args:
            base_workspace_dir: Base directory for all workspaces
        """
        self.base_workspace_dir = Path(base_workspace_dir)
        self.base_workspace_dir.mkdir(parents=True, exist_ok=True)

    def _hash_topic(self, topic: str) -> str:
        """
        Create a hash of the topic for directory naming.
        
        Args:
            topic: Research topic string
            
        Returns:
            MD5 hash of the topic (first 8 characters)
        """
        return hashlib.md5(topic.encode()).hexdigest()[:8]

    def create_workspace(self, topic: str) -> Path:
        """
        Create a workspace directory for a topic.
        
        Args:
            topic: Research topic string
            
        Returns:
            Path to the created workspace directory
        """
        topic_hash = self._hash_topic(topic)
        # Create a safe directory name from topic
        safe_topic = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in topic)
        safe_topic = safe_topic.replace(' ', '_')[:50]  # Limit length
        
        workspace_name = f"{topic_hash}_{safe_topic}"
        workspace_path = self.base_workspace_dir / workspace_name
        workspace_path.mkdir(parents=True, exist_ok=True)
        
        return workspace_path

    def init_state(self, workspace_path: Path, topic: str) -> Dict[str, Any]:
        """
        Initialize state for a new workspace.
        
        Args:
            workspace_path: Path to workspace directory
            topic: Research topic string
            
        Returns:
            Initial state dictionary
        """
        state = {
            "topic": topic,
            "status": "initialized",
            "workspace_path": str(workspace_path),
            "phases_completed": [],
            "created_at": None,  # Will be set when saved
            "updated_at": None
        }
        
        self.save_state(workspace_path, state)
        return state

    def save_state(self, workspace_path: Path, state: Dict[str, Any]) -> None:
        """
        Save state to workspace directory.
        
        Args:
            workspace_path: Path to workspace directory
            state: State dictionary to save
        """
        from datetime import datetime
        
        # Update timestamp
        state["updated_at"] = datetime.now().isoformat()
        if "created_at" not in state or state["created_at"] is None:
            state["created_at"] = state["updated_at"]
        
        state_file = workspace_path / "state.json"
        with open(state_file, 'w') as f:
            json.dump(state, f, indent=2)

    def load_state(self, workspace_path: Path) -> Dict[str, Any]:
        """
        Load state from workspace directory.
        
        Args:
            workspace_path: Path to workspace directory
            
        Returns:
            State dictionary
            
        Raises:
            FileNotFoundError: If state file doesn't exist
        """
        state_file = workspace_path / "state.json"
        if not state_file.exists():
            raise FileNotFoundError(f"State file not found: {state_file}")
        
        with open(state_file, 'r') as f:
            return json.load(f)

    def get_workspace_path(self, topic: str) -> Path:
        """
        Get the workspace path for a topic (without creating it).
        
        Args:
            topic: Research topic string
            
        Returns:
            Path where the workspace would be/is located
        """
        topic_hash = self._hash_topic(topic)
        safe_topic = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in topic)
        safe_topic = safe_topic.replace(' ', '_')[:50]
        
        workspace_name = f"{topic_hash}_{safe_topic}"
        return self.base_workspace_dir / workspace_name
