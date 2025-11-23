"""State management for workflow execution.

This module implements state handling as defined in the Hybrid Hierarchical-GraphRAG System specification
(Section 4.3 and 4.4). It manages workspace creation, state persistence, and state loading.
"""

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from loguru import logger


class State:
    """Tracks the state of a research workflow.
    
    Attributes:
        topic: The research topic
        workspace_path: Path to the workspace directory
        current_phase: Current phase being executed
        phases_completed: List of completed phase names
        phase_outputs: Dictionary mapping phase names to their outputs
        metrics: Dictionary of workflow metrics
        errors: List of error messages encountered
        created_at: Timestamp when state was created
        updated_at: Timestamp when state was last updated
    """
    
    def __init__(
        self,
        topic: str,
        workspace_path: Path,
        current_phase: str = "Phase_0",
        phases_completed: Optional[List[str]] = None,
        phase_outputs: Optional[Dict[str, Any]] = None,
        metrics: Optional[Dict[str, Any]] = None,
        errors: Optional[List[str]] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
    ):
        """Initialize State object.
        
        Args:
            topic: Research topic
            workspace_path: Path to workspace directory
            current_phase: Current phase name
            phases_completed: List of completed phases
            phase_outputs: Phase output dictionary
            metrics: Metrics dictionary
            errors: List of errors
            created_at: Creation timestamp
            updated_at: Update timestamp
        """
        self.topic = topic
        self.workspace_path = Path(workspace_path)
        self.current_phase = current_phase
        self.phases_completed = phases_completed or []
        self.phase_outputs = phase_outputs or {}
        self.metrics = metrics or {}
        self.errors = errors or []
        self.created_at = created_at or datetime.now(timezone.utc).isoformat()
        self.updated_at = updated_at or datetime.now(timezone.utc).isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert state to dictionary for serialization.
        
        Returns:
            Dictionary representation of state
        """
        return {
            "topic": self.topic,
            "workspace_path": str(self.workspace_path),
            "current_phase": self.current_phase,
            "phases_completed": self.phases_completed,
            "phase_outputs": self.phase_outputs,
            "metrics": self.metrics,
            "errors": self.errors,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "State":
        """Create State from dictionary.
        
        Args:
            data: Dictionary containing state data
            
        Returns:
            State object
        """
        return cls(
            topic=data["topic"],
            workspace_path=Path(data["workspace_path"]),
            current_phase=data.get("current_phase", "Phase_0"),
            phases_completed=data.get("phases_completed", []),
            phase_outputs=data.get("phase_outputs", {}),
            metrics=data.get("metrics", {}),
            errors=data.get("errors", []),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )


def create_workspace(topic: str, base_path: str = "projects") -> Path:
    """Create a unique workspace directory for a research topic.
    
    Creates a directory structure: /projects/{topic_uuid}/
    Also creates a manifest.json file with basic topic information.
    
    Args:
        topic: The research topic
        base_path: Base directory for workspaces (default: "projects")
        
    Returns:
        Path to the created workspace directory
        
    Raises:
        IOError: If workspace creation fails
    """
    try:
        # Generate unique identifier for this topic
        topic_uuid = str(uuid.uuid4())
        
        # Create workspace path
        workspace_path = Path(base_path) / topic_uuid
        workspace_path.mkdir(parents=True, exist_ok=True)
        
        # Create manifest.json
        manifest = {
            "topic": topic,
            "uuid": topic_uuid,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "workspace_path": str(workspace_path),
        }
        
        manifest_path = workspace_path / "manifest.json"
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)
        
        logger.info(f"Created workspace: {workspace_path}")
        return workspace_path
        
    except Exception as e:
        logger.error(f"Failed to create workspace for topic '{topic}': {e}")
        raise IOError(f"Workspace creation failed: {e}") from e


def save_state(state: State) -> None:
    """Persist state to state.json in the workspace.
    
    Args:
        state: State object to save
        
    Raises:
        IOError: If state saving fails
    """
    try:
        # Update timestamp
        state.updated_at = datetime.now(timezone.utc).isoformat()
        
        # Save to state.json
        state_path = state.workspace_path / "state.json"
        with open(state_path, "w", encoding="utf-8") as f:
            json.dump(state.to_dict(), f, indent=2)
        
        logger.debug(f"Saved state to: {state_path}")
        
    except Exception as e:
        logger.error(f"Failed to save state: {e}")
        raise IOError(f"State saving failed: {e}") from e


def load_state(workspace_path: Path) -> State:
    """Load state from state.json in the workspace.
    
    Args:
        workspace_path: Path to workspace directory
        
    Returns:
        Loaded State object
        
    Raises:
        FileNotFoundError: If state.json doesn't exist
        IOError: If state loading fails
    """
    try:
        state_path = Path(workspace_path) / "state.json"
        
        if not state_path.exists():
            raise FileNotFoundError(f"State file not found: {state_path}")
        
        with open(state_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        state = State.from_dict(data)
        logger.debug(f"Loaded state from: {state_path}")
        return state
        
    except FileNotFoundError:
        raise
    except Exception as e:
        logger.error(f"Failed to load state from {workspace_path}: {e}")
        raise IOError(f"State loading failed: {e}") from e
