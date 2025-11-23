# YT-DeepReSearch Orchestrator - Usage Guide

## Overview

The orchestrator system manages the research workflow through an Excel-based job queue and persistent state management. It processes research topics through 8 phases, from foundation research to final output.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Create a Job Queue

Create an Excel file (e.g., `job_queue.xlsx`) with the following structure or use Python:

```python
from src.orchestrator.job_queue import JobQueue

# Create a new job queue
jq = JobQueue("job_queue.xlsx")

# Add topics to research
jq.add_job("The Future of Quantum Computing")
jq.add_job("Climate Change Solutions")
```

### 3. Run the Orchestrator

#### Continuous Mode (Process all pending jobs)

```bash
cd src
python main.py --mode orchestrator
```

This will continuously check for pending jobs and process them one by one.

#### Single Job Mode (Process one specific topic)

```bash
cd src
python main.py --mode single --topic "Your Research Topic"
```

### 4. Check Results

Results are stored in workspace directories under `projects/`:

```
projects/
└── {uuid}/
    ├── manifest.json          # Job metadata and phase completion status
    ├── state.json             # Current state for resumability
    └── phase_outputs/         # Output from each phase
        ├── phase_1/
        ├── phase_2/
        ...
```

## Command-Line Options

```bash
python main.py [OPTIONS]

Options:
  --mode {orchestrator,single}  Run mode (default: orchestrator)
  --topic TOPIC                 Topic to research (required for single mode)
  --job-queue PATH              Path to Excel job queue (default: job_queue.xlsx)
  --projects-dir PATH           Base directory for workspaces (default: projects)
  --max-iterations N            Max jobs to process (for testing)
```

## Excel Job Queue Format

The job queue Excel file has the following columns:

| Column | Name | Description |
|--------|------|-------------|
| A | Topic | Research topic (string) |
| B | Status | Current status (Pending/In_Progress/Completed/Error) |
| C | Timestamp_Start | When processing started |
| D | Timestamp_End | When processing finished |
| E | Duration_Seconds | Total processing time |
| F | Error_Message | Error details if failed |
| G | Output_Path | Path to workspace directory |

## Pipeline Phases

The orchestrator processes each job through 8 phases:

1. **Foundation Research** - Initial topic research
2. **Deep Dive Research** - Detailed investigation
3. **Cross-Validation** - Verify information accuracy
4. **Knowledge Graph Construction** - Build knowledge relationships
5. **Hierarchical Clustering** - Organize information
6. **Narrative Generation** - Create content
7. **Final Review & Refinement** - Quality check
8. **Output & Archival** - Save final results

**Note:** Current implementation includes placeholder functions for phases 1-8. These will be implemented in subsequent development phases.

## State Management

Each job has its own workspace with:

- **manifest.json** - Tracks job metadata, timestamps, and phase completion
- **state.json** - Stores current state for resumability
- **phase_outputs/** - Directory for phase-specific outputs

## Concurrency

The job queue uses file locking to support multiple orchestrator instances:

- Jobs are claimed atomically to prevent duplicate processing
- Excel file operations use retry logic for robustness
- Each orchestrator instance processes one job at a time

## Examples

### Example 1: Create and Process a Single Job

```python
from src.orchestrator.workflow import Orchestrator

# Initialize orchestrator
orchestrator = Orchestrator()

# Process a single topic
orchestrator.process_single_job("History of Artificial Intelligence")
```

### Example 2: Check Job Status

```python
from src.orchestrator.job_queue import JobQueue

jq = JobQueue("job_queue.xlsx")
status = jq.get_job_status("Your Topic")

print(f"Status: {status['status']}")
print(f"Duration: {status['duration_seconds']} seconds")
print(f"Output: {status['output_path']}")
```

### Example 3: Resume from State

```python
from src.utils.state import StateManager

# Load existing workspace
sm = StateManager()
sm.load_workspace("projects/uuid-here")

# Check current state
state = sm.load_state()
print(f"Current phase: {state['current_phase']}")
print(f"Completed phases: {state['completed_phases']}")
```

## Troubleshooting

### Issue: Jobs stuck in "In_Progress"

This can happen if an orchestrator crashes. Manually update the Excel file to reset the status to "Pending".

### Issue: Cannot access Excel file

Ensure no other process has the file open. The system uses locking, but external programs (like Excel) may block access.

### Issue: Workspace not found

Check that the `projects_dir` path is correct. Workspaces are created relative to where main.py is executed.

## Architecture

```
┌─────────────────┐
│   Job Queue     │  Excel-based job tracking
│  (Excel File)   │  with concurrency support
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Orchestrator   │  Main workflow coordinator
│                 │  - Fetches jobs
│                 │  - Manages phases
│                 │  - Handles errors
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ State Manager   │  Workspace & persistence
│                 │  - Creates workspaces
│                 │  - Saves manifest/state
│                 │  - Tracks phases
└─────────────────┘
```

## Next Steps

The current implementation provides the core orchestration framework. Future development will include:

1. Implementing actual research logic for each phase
2. Integration with Perplexity API for research
3. Integration with Gemini API for content generation
4. Knowledge graph construction
5. Advanced error handling and retry logic
6. Progress monitoring and reporting
