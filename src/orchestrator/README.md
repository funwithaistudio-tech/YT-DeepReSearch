# Phase 0: Core Orchestrator Setup

This directory contains the implementation of Phase 0 of the Hybrid Hierarchical-GraphRAG System.

## Components

### 1. Job Queue (`job_queue.py`)

Excel-based job queue management system that tracks research topics through the pipeline.

**Features:**
- Automatic Excel file creation with proper headers
- File locking with retry logic
- Topic status tracking (Pending, In_Progress, Completed, Error)
- Duration and quality metrics
- Error message logging

**Usage:**
```python
from orchestrator.job_queue import JobQueue
from config import JobStatus

# Initialize queue
queue = JobQueue()

# Add topics
queue.add_topic("The History of Artificial Intelligence", "Test topic")

# Get next pending topic
topic = queue.get_next_pending_topic()

# Update status
queue.update_status(
    topic=topic,
    status=JobStatus.IN_PROGRESS,
    timestamp_start="2025-01-01T00:00:00"
)
```

### 2. Main Orchestrator (`../main.py`)

The main orchestrator that processes topics through all 8 phases of the pipeline.

**Features:**
- Automatic workspace creation for each topic
- State persistence across phases
- Error handling and recovery
- Progress tracking and logging

**Usage:**
```bash
# Run the orchestrator
cd src
python main.py
```

The orchestrator will:
1. Read pending topics from the Excel job queue
2. Create a unique workspace for each topic
3. Execute all 8 phases sequentially
4. Save state after each phase
5. Update job queue with completion status

## Excel File Format

The job queue Excel file (`job_queue/research_queue.xlsx`) contains the following columns:

| Column | Description |
|--------|-------------|
| Topic | Research topic (string) |
| Status | Job status (Pending, In_Progress, Completed, Error) |
| Timestamp_Start | Start timestamp (ISO format) |
| Timestamp_End | End timestamp (ISO format) |
| Duration_Seconds | Total duration in seconds (float) |
| Quality_Score | Quality score 0-100 (float, optional) |
| Error_Message | Error message if failed (string) |
| Notes | Additional notes (string) |

## Adding Topics to Queue

You can add topics in two ways:

### 1. Using Python API

```python
from orchestrator.job_queue import JobQueue

queue = JobQueue()
queue.add_topic("Your Research Topic", "Optional notes")
```

### 2. Editing Excel File Directly

1. Open `job_queue/research_queue.xlsx`
2. Add a new row with:
   - Topic: Your research topic
   - Status: Pending
   - Other columns: Leave empty
3. Save the file
4. Run the orchestrator

## Workspace Structure

Each topic gets a unique workspace directory under `projects/`:

```
projects/
└── <workspace-id>/
    ├── manifest.json    # Workspace metadata
    └── state.json       # Current pipeline state
```

### manifest.json
Contains workspace metadata:
```json
{
  "workspace_id": "uuid",
  "topic": "Topic name",
  "created_at": "ISO timestamp",
  "pipeline_version": "1.0.0"
}
```

### state.json
Contains pipeline state:
```json
{
  "topic": "Topic name",
  "workspace_id": "uuid",
  "current_phase": "Phase_X_Name",
  "created_at": "ISO timestamp",
  "updated_at": "ISO timestamp",
  "completed_phases": [...],
  "artifacts": {...},
  "metadata": {...},
  "errors": [...]
}
```

## Next Steps

The Phase 0 setup provides the foundation for implementing:
- Phase 1: Topic Decomposition
- Phase 2: Deep Research
- Phase 3: Content Compression
- Phase 4: Knowledge Graph Construction
- Phase 5: Hierarchical Organization
- Phase 6: Narrative Planning
- Phase 7: Content Generation
- Phase 8: Final Output

Each phase will be implemented by updating the corresponding placeholder functions in:
- `src/foundation/` (Phases 1-3)
- `src/knowledge/` (Phases 4-5)
- `src/narrative/` (Phases 6-7)
