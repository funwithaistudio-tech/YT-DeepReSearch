# Phase 0 Implementation: Orchestrator and Project Structure

## Overview

This document describes the implementation of Phase 0 (Orchestrator) for the YT-DeepReSearch system, based on the "Hybrid Hierarchical-GraphRAG System" specification.

## Project Structure

```
YT-DeepReSearch/
├── src/
│   ├── __init__.py
│   ├── main.py                     # Entry point
│   ├── orchestrator/               # Phase 0: Orchestrator
│   │   ├── __init__.py
│   │   ├── job_queue.py           # Excel-based job queue
│   │   └── workflow.py            # Main orchestrator loop
│   ├── foundation/                 # Phase 1: Foundation Research (placeholder)
│   │   └── __init__.py
│   ├── knowledge/                  # Phase 3-5: Knowledge Graph (placeholder)
│   │   └── __init__.py
│   ├── narrative/                  # Phase 6-7: Narrative Generation (placeholder)
│   │   └── __init__.py
│   └── utils/                      # Utilities
│       ├── __init__.py
│       └── state.py               # State management
├── job_queue/                      # Auto-created
│   └── topics.xlsx                # Excel job queue
├── projects/                       # Auto-created
│   └── {uuid}/                    # Per-topic workspaces
│       ├── manifest.json          # Topic metadata
│       └── state.json             # Workflow state
└── requirements.txt
```

## Key Components

### 1. Job Queue (`src/orchestrator/job_queue.py`)

**Purpose**: Manages research topics using an Excel-based queue system.

**Features**:
- Auto-creates `job_queue/topics.xlsx` with sample topics if not present
- Implements locking strategy (Read Phase → Write Phase with check)
- Handles stale locks (topics locked beyond timeout are reset)
- Tracks topic status, timestamps, duration, quality scores, and errors

**Key Methods**:
- `get_next_pending_topic()`: Finds the first pending topic
- `claim_topic(topic_name)`: Claims a topic for processing
- `update_status(...)`: Updates topic status and metrics
- `add_topic(topic_name)`: Adds a new topic to the queue

**Excel Columns**:
1. Topic
2. Status (Pending, In_Progress, Completed, Failed)
3. Timestamp_Start
4. Timestamp_End
5. Duration_Seconds
6. Quality_Score
7. Error_Message
8. Notes

**Note**: The Excel-based locking has inherent race condition limitations. For production use with concurrent workers, consider migrating to a proper database with atomic operations.

### 2. State Management (`src/utils/state.py`)

**Purpose**: Manages workflow state persistence and workspace creation.

**Features**:
- Creates unique workspace directories (`/projects/{uuid}/`)
- Tracks current phase, completed phases, phase outputs, metrics, and errors
- Persists state to JSON for resume capability

**Key Functions**:
- `create_workspace(topic)`: Creates workspace with manifest.json
- `save_state(state)`: Persists state to state.json
- `load_state(workspace_path)`: Loads state from workspace

**State Class Fields**:
- `topic`: Research topic
- `workspace_path`: Path to workspace directory
- `current_phase`: Current phase being executed
- `phases_completed`: List of completed phase names
- `phase_outputs`: Dictionary of phase outputs
- `metrics`: Workflow metrics
- `errors`: List of errors encountered
- `created_at`: Creation timestamp (ISO 8601, UTC)
- `updated_at`: Last update timestamp (ISO 8601, UTC)

### 3. Orchestrator Workflow (`src/orchestrator/workflow.py`)

**Purpose**: Main orchestration loop that manages the complete research pipeline.

**Features**:
- Polls for pending topics continuously
- Claims topics using the job queue
- Creates workspaces and initializes state
- Executes all phases (1-8) sequentially
- Updates job queue on completion/failure
- Handles errors gracefully

**Main Loop Logic**:
1. Get next pending topic from job queue
2. Claim the topic (with locking)
3. Create workspace and initialize state
4. Execute phases 1-8 in sequence
5. Update job queue with results (status, duration, quality score)
6. Repeat until max_iterations reached (or infinite if max_iterations=0)

**Phase Placeholders**:
- Phase 1: Foundation Research
- Phase 2: Deep Dive Research
- Phase 3: Knowledge Graph Construction
- Phase 4: Community Detection
- Phase 5: Summary Generation
- Phase 6: Narrative Construction
- Phase 7: Script Generation
- Phase 8: Quality Assurance

### 4. Entry Point (`src/main.py`)

**Purpose**: Main entry point for the YT-DeepReSearch system.

**Configuration**:
- `excel_path`: Path to job queue Excel file (default: "job_queue/topics.xlsx")
- `max_iterations`: Maximum topics to process (0 = infinite, 3 for testing)
- `iteration_delay`: Seconds to wait between iterations (default: 2)

## Usage

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

Required packages:
- `loguru>=0.7.0` (logging)
- `openpyxl>=3.1.0` (Excel operations)
- `pandas>=2.1.0` (data processing)

### Running the Orchestrator

```bash
# Run from project root
python src/main.py
```

This will:
1. Create `job_queue/topics.xlsx` with sample topics (if not exists)
2. Process up to 3 topics (configurable in main.py)
3. Create workspaces in `projects/` for each topic
4. Execute all phases (currently placeholders)
5. Update Excel with completion status

### Adding Topics

Topics can be added in two ways:

**Method 1: Edit Excel directly**
- Open `job_queue/topics.xlsx`
- Add new row with Topic name and Status="Pending"
- Save the file

**Method 2: Use JobQueue programmatically**
```python
from src.orchestrator.job_queue import JobQueue

jq = JobQueue()
jq.add_topic("Your New Topic", notes="Optional notes")
```

### Monitoring Progress

**Check Excel File**:
Open `job_queue/topics.xlsx` to see:
- Current status of all topics
- Processing timestamps
- Duration and quality scores
- Error messages (if any)

**Check Workspace**:
Each processed topic creates a workspace in `projects/{uuid}/`:
- `manifest.json`: Topic metadata
- `state.json`: Complete workflow state

**View Logs**:
The system uses `loguru` for logging. All operations are logged to stdout with different log levels (INFO, DEBUG, ERROR, WARNING).

## Configuration

### Orchestrator Parameters

Edit `src/main.py` to configure:

```python
orchestrator_main_loop(
    excel_path="job_queue/topics.xlsx",  # Path to Excel file
    max_iterations=3,                     # 0 = infinite
    iteration_delay=2,                    # Seconds between iterations
)
```

### Lock Timeout

Edit `src/orchestrator/job_queue.py`:

```python
def __init__(self, excel_path: str = "job_queue/topics.xlsx", lock_timeout: int = 3600):
    # lock_timeout: Maximum time (seconds) a topic can be locked
    # Default: 3600 seconds (1 hour)
```

## Testing

The implementation has been tested with:
- ✓ JobQueue operations (create, claim, update)
- ✓ State management (create workspace, save/load state)
- ✓ Full workflow execution (3 topics processed successfully)
- ✓ Excel file updates correctly
- ✓ Workspace creation with proper structure
- ✓ Error handling and recovery
- ✓ Timezone-aware datetime handling (Python 3.12+)
- ✓ Security scan (0 vulnerabilities found)

## Known Limitations

1. **Excel-based Locking**: The current implementation uses a simple read-check-write pattern which has inherent race condition limitations. For production use with multiple concurrent workers, consider:
   - Migrating to a proper database (PostgreSQL, MongoDB)
   - Implementing file-level locking (fcntl on Unix, msvcrt on Windows)
   - Using a distributed lock manager (Redis, etcd)

2. **Phase Implementations**: Phases 1-8 are currently placeholders. They will be implemented in subsequent phases of development.

3. **No Authentication**: The system does not currently implement authentication or authorization.

## Future Enhancements

1. **Database Migration**: Replace Excel with a proper database for better concurrency and reliability
2. **Phase Implementations**: Implement actual research, knowledge graph, and narrative generation phases
3. **Web UI**: Add a web interface for monitoring and management
4. **API**: Expose REST API for programmatic access
5. **Distributed Processing**: Support multiple workers across machines
6. **Resume Capability**: Full support for resuming interrupted workflows
7. **Quality Metrics**: Implement comprehensive quality scoring
8. **Notifications**: Add email/webhook notifications for completion/failures

## Dependencies

Core dependencies:
- `loguru>=0.7.0`: Logging framework
- `openpyxl>=3.1.0`: Excel file operations
- `pandas>=2.1.0`: Data processing
- Python 3.12+: Modern Python features and timezone support

## Code Quality

- ✓ Code review completed
- ✓ Security scan completed (0 vulnerabilities)
- ✓ Uses timezone-aware datetime (Python 3.12+ compatible)
- ✓ Comprehensive error handling
- ✓ Detailed logging at appropriate levels
- ✓ Type hints for better code clarity
- ✓ Docstrings for all public methods

## Contributing

When implementing future phases:
1. Follow the existing code structure and style
2. Update `phase_outputs` in the State object
3. Add proper error handling
4. Use `loguru` for logging
5. Save state after each major operation
6. Update this documentation

## License

See LICENSE file in the project root.
