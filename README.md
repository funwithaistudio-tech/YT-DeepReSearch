# YT-DeepReSearch

AI-powered deep research system for creating educational video scripts using Perplexity API and Gemini Vertex API. Produces in-depth content inspired by channels like Veritasium, Dhruv Rathee, and Fern.

## Phase 0: Orchestrator Implementation

The core orchestration system has been implemented, featuring:

- **Excel-based Job Queue**: Track research topics through their lifecycle
- **State Management**: Persistent workspace and resumability support
- **8-Phase Pipeline**: Modular research workflow from foundation to output
- **Concurrent Processing**: Support for multiple orchestrator instances

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Create a Job Queue

```bash
python manage_queue.py create job_queue.xlsx --topics "Your Topic 1" "Your Topic 2"
```

### 3. Run the Orchestrator

**Continuous mode** (processes all pending jobs):
```bash
cd src
python main.py --mode orchestrator
```

**Single job mode** (process one topic):
```bash
cd src
python main.py --mode single --topic "Your Research Topic"
```

### 4. Check Results

Results are stored in `projects/{uuid}/` with manifest, state, and phase outputs.

## Documentation

- [Orchestrator Guide](ORCHESTRATOR_GUIDE.md) - Detailed usage and architecture
- [Project Structure](PROJECT_STRUCTURE.md) - Complete project layout

## Examples

Run the examples to see the system in action:

```bash
python examples.py
```

Or use the queue management tool:

```bash
# List jobs
python manage_queue.py list job_queue.xlsx

# Add a new job
python manage_queue.py add job_queue.xlsx "New Topic"

# Reset a stuck job
python manage_queue.py reset job_queue.xlsx "Topic Name"
```

## Architecture

The system uses a Hybrid Hierarchical-GraphRAG approach with 8 processing phases:

1. **Foundation Research** - Initial topic investigation
2. **Deep Dive Research** - Detailed analysis
3. **Cross-Validation** - Information verification
4. **Knowledge Graph Construction** - Relationship mapping
5. **Hierarchical Clustering** - Content organization
6. **Narrative Generation** - Script creation
7. **Final Review & Refinement** - Quality assurance
8. **Output & Archival** - Result persistence

## Current Status

✅ **Phase 0 Complete**: Orchestrator, job queue, and state management implemented with placeholder phase functions.

🚧 **Next Steps**: Implement actual research logic for phases 1-8 with API integrations.

## License

MIT License - see [LICENSE](LICENSE) file for details.

