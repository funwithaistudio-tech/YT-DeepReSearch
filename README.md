# YT-DeepReSearch

AI-powered deep research system for creating educational video scripts using Perplexity API and Gemini Vertex API. Produces in-depth content inspired by channels like Veritasium, Dhruv Rathee, and Fern.

## Overview

YT-DeepReSearch implements a **Hybrid Hierarchical-GraphRAG System** that processes research topics through an 8-phase pipeline:

1. **Phase 1**: Topic Decomposition - Break down complex topics into manageable sub-topics
2. **Phase 2**: Deep Research - Conduct comprehensive research using Perplexity API
3. **Phase 3**: Content Compression - Extract key insights from research data
4. **Phase 4**: Knowledge Graph Construction - Build entity-relationship graphs
5. **Phase 5**: Hierarchical Organization - Create structured knowledge hierarchies
6. **Phase 6**: Narrative Planning - Plan content structure and flow
7. **Phase 7**: Content Generation - Generate educational content
8. **Phase 8**: Final Output - Produce final video scripts

## Current Status: Phase 0 Complete ✅

The core orchestrator infrastructure is implemented and ready for phase implementations.

### Phase 0 Features

- ✅ **Job Queue System**: Excel-based queue management for tracking research topics
- ✅ **Workspace Manager**: Automatic workspace creation and state persistence
- ✅ **Core Orchestrator**: Main processing loop with error handling and recovery
- ✅ **Configuration Management**: Environment variables and system constants
- ✅ **State Tracking**: Pydantic-based state models with full lifecycle tracking
- ✅ **Architecture Structure**: Complete module structure for all 8 phases

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and add your API keys:

```bash
cp .env.example .env
```

Edit `.env`:
```
PERPLEXITY_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here
```

### 3. Add Topics to Queue

Use the example script to add topics:

```bash
python example.py add
```

Or add topics programmatically:

```python
from orchestrator.job_queue import JobQueue

queue = JobQueue()
queue.add_topic("The History of Artificial Intelligence", "Educational video")
```

Or edit the Excel file directly at `job_queue/research_queue.xlsx`.

### 4. Run the Orchestrator

```bash
cd src
python main.py
```

The orchestrator will:
- Process all pending topics from the queue
- Create workspaces for each topic
- Execute all 8 phases (currently placeholder implementations)
- Update job status in the Excel file
- Save state after each phase

### 5. Check Status

```bash
python example.py status
```

## Project Structure

```
YT-DeepReSearch/
├── src/
│   ├── config.py                 # Configuration and constants
│   ├── main.py                   # Core orchestrator
│   │
│   ├── orchestrator/             # Phase 0: Orchestration
│   │   ├── job_queue.py          # Excel-based job queue
│   │   └── README.md             # Orchestrator documentation
│   │
│   ├── foundation/               # Phases 1-3
│   │   ├── decomposition.py      # Phase 1: Topic decomposition
│   │   ├── research.py           # Phase 2: Deep research
│   │   └── compression.py        # Phase 3: Content compression
│   │
│   ├── knowledge/                # Phases 4-5
│   │   ├── graph.py              # Phase 4: Knowledge graph
│   │   └── hierarchy.py          # Phase 5: Hierarchical organization
│   │
│   ├── narrative/                # Phases 6-7
│   │   ├── planner.py            # Phase 6: Narrative planning
│   │   └── generator.py          # Phase 7: Content generation
│   │
│   └── utils/                    # Utilities
│       ├── state.py              # State management
│       ├── llm_gemini.py         # Gemini API client
│       └── llm_perplexity.py     # Perplexity API client
│
├── job_queue/                    # Auto-generated job queue
│   └── research_queue.xlsx       # Excel file with topic queue
│
├── projects/                     # Auto-generated workspaces
│   └── <workspace-id>/
│       ├── manifest.json         # Workspace metadata
│       └── state.json            # Pipeline state
│
├── example.py                    # Example usage script
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Job Queue Format

The system uses an Excel spreadsheet (`job_queue/research_queue.xlsx`) to manage topics:

| Column | Description |
|--------|-------------|
| Topic | Research topic |
| Status | Pending / In_Progress / Completed / Error |
| Timestamp_Start | When processing started |
| Timestamp_End | When processing finished |
| Duration_Seconds | Total processing time |
| Quality_Score | Quality metric (0-100) |
| Error_Message | Error details if failed |
| Notes | Additional information |

## Development Status

### ✅ Completed
- Phase 0: Core orchestrator infrastructure
- Job queue management system
- Workspace and state management
- Project structure and architecture

### 🔄 In Progress
- Phase 1-8 implementations (placeholders currently exist)

### 📋 Planned
- Phase 1: Implement topic decomposition with LLM
- Phase 2: Integrate Perplexity API for research
- Phase 3: Implement content compression
- Phase 4: Build knowledge graph construction
- Phase 5: Create hierarchical organization
- Phase 6: Implement narrative planning
- Phase 7: Add content generation
- Phase 8: Finalize output formatting

## API Keys Required

- **Perplexity API**: For deep research and information retrieval
- **Gemini API**: For content generation and processing

## License

MIT

## Contributing

Contributions welcome! Please check the issues page for current tasks.

