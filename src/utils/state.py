"""State management for workspace and pipeline state persistence."""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional


def create_workspace(topic: str, base_dir: str = "projects") -> str:
    """
    Create a workspace directory for a topic.

    Args:
        topic: Topic name
        base_dir: Base directory for projects

    Returns:
        Path to the created workspace
    """
    # Generate UUID4 for true randomness
    topic_uuid = str(uuid.uuid4())
    
    # Create workspace path
    workspace_path = Path(base_dir) / topic_uuid
    workspace_path.mkdir(parents=True, exist_ok=True)
    
    return str(workspace_path)


def initialize_state(topic: str, workspace_path: str) -> Dict[str, Any]:
    """
    Initialize state object for a new topic.

    Args:
        topic: Topic name
        workspace_path: Path to workspace directory

    Returns:
        Initial state dictionary
    """
    state = {
        "topic": topic,
        "workspace_path": workspace_path,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "current_phase": 0,
        "status": "initialized",
        "phases": {
            "phase_0": {"status": "completed", "timestamp": datetime.now().isoformat()},
            "phase_1": {"status": "pending", "timestamp": None},
            "phase_2": {"status": "pending", "timestamp": None},
            "phase_3": {"status": "pending", "timestamp": None},
            "phase_4": {"status": "pending", "timestamp": None},
            "phase_5": {"status": "pending", "timestamp": None},
            "phase_6": {"status": "pending", "timestamp": None},
            "phase_7": {"status": "pending", "timestamp": None},
            "phase_8": {"status": "pending", "timestamp": None},
        },
        "metadata": {},
        "errors": []
    }
    return state


def save_state(state: Dict[str, Any]) -> bool:
    """
    Save state to state.json in the workspace.

    Args:
        state: State dictionary

    Returns:
        True if successful, False otherwise
    """
    try:
        workspace_path = Path(state["workspace_path"])
        state_file = workspace_path / "state.json"
        
        # Update timestamp
        state["updated_at"] = datetime.now().isoformat()
        
        # Save to file
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        print(f"Error saving state: {e}")
        return False


def load_state(workspace_path: str) -> Optional[Dict[str, Any]]:
    """
    Load state from state.json in the workspace.

    Args:
        workspace_path: Path to workspace directory

    Returns:
        State dictionary or None if file doesn't exist
    """
    try:
        state_file = Path(workspace_path) / "state.json"
        
        if not state_file.exists():
            return None
        
        with open(state_file, 'r', encoding='utf-8') as f:
            state = json.load(f)
        
        return state
    except Exception as e:
        print(f"Error loading state: {e}")
        return None


def update_phase_status(
    state: Dict[str, Any],
    phase: int,
    status: str,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Update phase status in the state.

    Args:
        state: State dictionary
        phase: Phase number (1-8)
        status: Phase status (e.g., "in_progress", "completed", "failed")
        metadata: Optional metadata to store

    Returns:
        Updated state dictionary
    """
    phase_key = f"phase_{phase}"
    
    if phase_key in state["phases"]:
        state["phases"][phase_key]["status"] = status
        state["phases"][phase_key]["timestamp"] = datetime.now().isoformat()
        
        if metadata:
            if "metadata" not in state["phases"][phase_key]:
                state["phases"][phase_key]["metadata"] = {}
            state["phases"][phase_key]["metadata"].update(metadata)
    
    state["current_phase"] = phase
    state["updated_at"] = datetime.now().isoformat()
    
    return state


def add_error(state: Dict[str, Any], error_message: str, phase: Optional[int] = None) -> Dict[str, Any]:
    """
    Add an error to the state.

    Args:
        state: State dictionary
        error_message: Error message
        phase: Optional phase number where error occurred

    Returns:
        Updated state dictionary
    """
    error_entry = {
        "message": error_message,
        "timestamp": datetime.now().isoformat(),
        "phase": phase
    }
    
    state["errors"].append(error_entry)
    state["updated_at"] = datetime.now().isoformat()
    
    return state
