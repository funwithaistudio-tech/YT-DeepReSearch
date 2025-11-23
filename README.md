# YT-DeepReSearch

AI-powered deep research system for creating educational video scripts using Perplexity API and Gemini Vertex API. Produces in-depth content inspired by channels like Veritasium, Dhruv Rathee, and Fern.

## Features

- **8-Phase Pipeline**: Comprehensive system from research to final script
- **Multi-Source Research**: Parallel research using Perplexity API
- **Knowledge Graph Construction**: Build structured knowledge representations
- **Hierarchical Summarization**: Multi-tier content organization
- **Narrative Storytelling**: 3-act structure with engagement hooks
- **Quality Validation**: Automated quality and fact-checking
- **Excel Queue Management**: Process multiple topics from spreadsheet
- **Token Safety**: Intelligent token management and chunking
- **Robust Error Handling**: Retry logic with exponential backoff

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/funwithaistudio-tech/YT-DeepReSearch.git
cd YT-DeepReSearch

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys
```

### Usage

**Process a single topic:**
```bash
python src/main.py --mode single --topic "The Science of Black Holes"
```

**Process Excel queue:**
```bash
python src/main.py --mode queue
```

### Docker

```bash
docker-compose up
```

## System Architecture

### 8-Phase Pipeline

1. **Phase 0: System Orchestration** - Excel queue management and pipeline coordination
2. **Phase 1: Query Decomposition** - Break topics into focused sub-queries
3. **Phase 2: Parallel Research** - Multi-source research with Perplexity API
4. **Phase 3: Graph Construction** - Build knowledge graph from research
5. **Phase 4: Hierarchical Tiers** - Generate multi-level summaries
6. **Phase 5: Narrative Outline** - Create 3-act story structure
7. **Phase 6: Script Generation** - Generate complete video script
8. **Phase 7: Validation** - Quality and fact-checking
9. **Phase 8: Finalization** - Package and save all artifacts

### Key Components

- **Pipeline Orchestrator**: Manages end-to-end execution
- **Excel Queue Manager**: Handles job queue from spreadsheet
- **Perplexity Client**: Deep research capabilities
- **Gemini Client**: Content generation with Vertex AI
- **Phase Implementations**: Specialized processors for each phase
- **Utility Functions**: Logging, retry logic, token management

## Output Structure

Each processed topic generates:

```
output/Topic_Name_20231123_143000/
├── script.txt                 # Final video script
├── script_complete.json       # Script with metadata
├── narrative_outline.json     # Story structure
├── knowledge_graph.json       # Concept relationships
├── hierarchical_tiers.json    # Multi-level summaries
├── research_results.json      # Raw research data
├── validation_report.json     # Quality metrics
├── citations.txt              # All sources
├── pipeline_complete.json     # Full pipeline output
└── SUMMARY.md                 # Human-readable summary
```

## Configuration

Edit `.env` file:

```env
# Required API Keys
PERPLEXITY_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here
GOOGLE_CLOUD_PROJECT=your_project_id

# Optional Settings
OUTPUT_DIR=./output
RESEARCH_DEPTH=deep           # quick, medium, deep
SCRIPT_LENGTH=medium          # short, medium, long
CONTENT_STYLE=educational     # educational, entertaining, documentary
```

## Excel Queue Format

Create `./input/topics.xlsx` with columns:

| Topic | Status | Priority | Notes |
|-------|--------|----------|-------|
| The Science of Black Holes | pending | 5 | Focus on event horizons |
| How Vaccines Work | pending | 3 | Include mRNA technology |

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific tests
pytest tests/test_phase1.py -v
```

## Documentation

- [Architecture](docs/ARCHITECTURE.md) - System architecture and design
- [API Documentation](docs/API.md) - API reference and usage
- [Usage Guide](docs/USAGE.md) - Detailed usage instructions

## Development

### Project Structure

```
YT-DeepReSearch/
├── src/
│   ├── config/              # Configuration management
│   ├── orchestrator/        # Pipeline orchestration
│   ├── phases/              # Phase implementations
│   ├── research/            # Research components
│   ├── content/             # Content generation
│   └── utils/               # Utility functions
├── tests/                   # Test suite
├── docs/                    # Documentation
├── input/                   # Input Excel files
├── output/                  # Generated outputs
└── logs/                    # Application logs
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `pytest`
5. Submit a pull request

## CI/CD

GitHub Actions workflow included for:
- Automated testing across Python versions
- Code linting (black, flake8, mypy)
- Docker image building
- Coverage reporting

## License

MIT License - see LICENSE file for details

## Acknowledgments

- Perplexity AI for research capabilities
- Google Gemini/Vertex AI for content generation
- Inspired by educational YouTube channels: Veritasium, Dhruv Rathee, Fern

## Support

For issues and questions:
- Create an issue on GitHub
- Check documentation in `docs/` directory
- Review example outputs in `output/` directory
