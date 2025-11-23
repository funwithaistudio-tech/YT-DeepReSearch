# Phase 0: Orchestrator Implementation

This document describes the Phase 0 implementation of the YT-DeepReSearch pipeline.

## Overview

Phase 0 provides the core orchestration infrastructure for the YT-DeepReSearch pipeline:
- Excel-based job queue management
- Workspace and state management
- Main workflow loop with phase placeholders

## Components

### 1. Job Queue (`src/orchestrator/job_queue.py`)

The `JobQueue` class manages the `topics.xlsx` file for tracking research topics.

**Key Methods:**
- `get_next_pending()`: Finds the next pending topic in the queue
- `claim_topic(row_index, topic)`: Marks a topic as "In_Progress" 
- `update_status(topic, status, ...)`: Updates completion status, timestamps, metrics
- `add_topic(topic, status)`: Adds a new topic to the queue

**Excel Schema:**
- Topic: The research topic name
- Status: Current status (Pending, In_Progress, Completed, Failed)
- Timestamp_Start: When processing started
- Timestamp_End: When processing completed
- Duration_Seconds: Processing duration
- Quality_Score: Quality score (0-1)
- Error_Message: Error details if failed
- Workspace_Path: Path to workspace directory

### 2. State Management (`src/utils/state.py`)

Functions for managing workspace creation and state persistence.

**Key Functions:**
- `create_workspace(topic)`: Creates a UUID-based workspace directory
- `initialize_state(topic, workspace_path)`: Creates initial state object
- `save_state(state)`: Saves state to `state.json` in workspace
- `load_state(workspace_path)`: Loads state from workspace
- `update_phase_status(state, phase, status)`: Updates phase status
- `add_error(state, error_message, phase)`: Adds error to state

**State Schema:**
```json
{
  "topic": "...",
  "workspace_path": "...",
  "created_at": "...",
  "updated_at": "...",
  "current_phase": 0,
  "status": "initialized",
  "phases": {
    "phase_0": {"status": "completed", "timestamp": "..."},
    "phase_1": {"status": "pending", "timestamp": null},
    ...
  },
  "metadata": {},
  "errors": []
}
```

### 3. Main Workflow (`src/orchestrator/workflow.py`)

The `orchestrator_main_loop()` function implements the main execution loop:

1. Get next pending topic from queue
2. Claim the topic (mark as In_Progress)
3. Create workspace
4. Initialize state
5. Execute phases 1-8 (currently placeholders)
6. Update queue with completion status

### 4. Entry Point (`src/main.py`)

The main entry point that runs the orchestrator workflow.

## Usage

### Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `topics.xlsx` file with topics to process:
```bash
# Copy the example file
cp topics_example.xlsx topics.xlsx
```

Or manually create `topics.xlsx` with:
- Headers: Topic, Status, Timestamp_Start, Timestamp_End, Duration_Seconds, Quality_Score, Error_Message, Workspace_Path
- Rows: Add topics with Status="Pending"

### Run the Orchestrator

```bash
python3 src/main.py
```

The orchestrator will:
- Process all pending topics in the queue
- Create workspaces in `projects/{uuid}/`
- Save state to `projects/{uuid}/state.json`
- Update `topics.xlsx` with completion status

## Output

For each processed topic:
- **Workspace**: `projects/{uuid}/` directory
- **State File**: `projects/{uuid}/state.json` with execution state
- **Queue Update**: Status, timestamps, duration in `topics.xlsx`

## Testing

Run the comprehensive test suite:
```bash
python3 << 'EOF'
import sys
sys.path.insert(0, 'src')
from orchestrator.job_queue import JobQueue
from utils import state as state_manager
# ... (test code)
EOF
```

## Next Steps

Phase 1-8 implementations will replace the placeholder functions in `workflow.py`:
- Phase 1: Foundation analysis
- Phase 2: Knowledge gathering
- Phase 3: Deep research
- Phase 4: Content structuring
- Phase 5: Narrative development
- Phase 6: Script generation
- Phase 7: Quality assurance
- Phase 8: Final delivery
