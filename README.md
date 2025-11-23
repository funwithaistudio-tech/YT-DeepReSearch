# YT-DeepReSearch

AI-powered deep research system for creating educational video scripts using Perplexity API. Produces in-depth, well-researched content inspired by channels like Veritasium, Dhruv Rathee, and Fern.

## Overview

YT-DeepReSearch is a database-driven, multi-phase pipeline that transforms topics into comprehensive, deeply researched video scripts. The system:

1. **Fetches topics** from a PostgreSQL database
2. **Builds a question framework** (5 main questions, each with 2 sub-questions = 10 total)
3. **Performs deep research** using Perplexity API for each sub-question
4. **Generates long-form scripts** with 10 internal segments (~600-700 words each, totaling ~6000-7000 words)

## Architecture

### Pipeline Phases

- **Phase 0**: Environment & Configuration Validation
- **Phase 1**: Fetch Topic from Database
- **Phase 2**: Question Framework Builder (5 main × 2 sub = 10 questions)
- **Phase 3**: Deep Research per Sub-question (Perplexity search)
- **Phase 4**: Script Generation (10 internal segments)
- **Phase 5+**: _(Future)_ Assets, Video Assembly, Publishing, Cleanup

### Key Features

- **DB-Driven Workflow**: Topics managed in PostgreSQL with status tracking
- **Structured Research**: Question framework ensures comprehensive coverage
- **Deep Content**: ~4× longer than typical YouTube scripts (6000-7000 words vs 1500-1750)
- **Source Attribution**: All claims backed by research sources
- **Extensible Design**: Clear hooks for future image/audio/video generation

## Database Schema

Create a `topics` table in your PostgreSQL database:

```sql
CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    topic VARCHAR(500) NOT NULL,
    style VARCHAR(50) DEFAULT 'educational',
    language VARCHAR(10) DEFAULT 'en',
    status VARCHAR(20) DEFAULT 'pending',
    priority INTEGER DEFAULT 0,
    last_run_at TIMESTAMP,
    last_error TEXT,
    youtube_video_id VARCHAR(50)
);

CREATE INDEX idx_topics_status ON topics(status);
CREATE INDEX idx_topics_priority ON topics(priority DESC);
```

### Sample Data

```sql
INSERT INTO topics (topic, style, language, priority) VALUES
    ('Quantum Computing Explained', 'educational', 'en', 10),
    ('The Future of Artificial Intelligence', 'documentary', 'en', 8),
    ('Climate Change: Latest Research', 'educational', 'en', 9);
```

## Installation

### Prerequisites

- Python 3.10+
- PostgreSQL database
- Perplexity API key

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/funwithaistudio-tech/YT-DeepReSearch.git
   cd YT-DeepReSearch
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   
   Copy `.env.example` to `.env` and fill in your credentials:
   ```bash
   cp .env.example .env
   ```
   
   Required variables:
   ```env
   DATABASE_URL=postgresql://user:password@localhost:5432/yt_deepresearch
   PERPLEXITY_API_KEY=your_perplexity_api_key_here
   ```

4. **Create database and tables**
   
   Use the SQL schema above to create the `topics` table.

## Usage

### Running the Pipeline

Process one pending topic:

```bash
python -m src.main
```

The system will:
1. Fetch the highest-priority pending topic
2. Generate a question framework
3. Perform deep research (10 sub-questions)
4. Generate a comprehensive script
5. Mark the topic as completed

### Output Artifacts

All generated files are stored in the `generated/` directory:

```
generated/
├── topic_1_question_framework.json    # Question framework
├── research/
│   ├── topic_1_m1_s1.json            # Research for main Q1, sub Q1
│   ├── topic_1_m1_s2.json            # Research for main Q1, sub Q2
│   ├── topic_1_m2_s1.json            # Research for main Q2, sub Q1
│   └── ...                           # (10 research files total)
└── script_topic_1.json               # Final generated script
```

### Example Workflow

1. **Add topics to database**:
   ```sql
   INSERT INTO topics (topic, style, language, priority)
   VALUES ('Neural Networks Demystified', 'educational', 'en', 10);
   ```

2. **Run the pipeline**:
   ```bash
   python -m src.main
   ```

3. **Check the results**:
   - Question framework: `generated/topic_X_question_framework.json`
   - Research data: `generated/research/topic_X_m*_s*.json`
   - Final script: `generated/script_topic_X.json`

### Batch Processing

For continuous processing, run in a loop or cron job:

```bash
# Process all pending topics
while python -m src.main; do
    echo "Processed one topic, checking for next..."
    sleep 5
done
```

## Configuration

Key settings in `.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | _Required_ |
| `PERPLEXITY_API_KEY` | Perplexity API key | _Required_ |
| `LOG_LEVEL` | Logging level | `INFO` |
| `MAIN_SEGMENTS` | Number of main segments | `5` |
| `SUBSEGMENTS_PER_MAIN` | Subsegments per main | `2` |
| `WORDS_PER_SUBSEGMENT_MIN` | Min words per subsegment | `600` |
| `WORDS_PER_SUBSEGMENT_MAX` | Max words per subsegment | `700` |
| `MAX_LLM_RETRIES` | Max API retry attempts | `3` |
| `HTTP_TIMEOUT_SECONDS` | API request timeout | `120` |

## Project Structure

```
YT-DeepReSearch/
├── src/
│   ├── config/
│   │   └── settings.py              # Pydantic settings
│   ├── db/
│   │   ├── models.py                # TopicJob model
│   │   └── topic_repository.py     # Database operations
│   ├── domain/
│   │   ├── questions.py             # Question framework models
│   │   ├── research.py              # Research data models
│   │   └── script.py                # Script models
│   ├── research/
│   │   ├── perplexity_client.py    # Perplexity API client
│   │   ├── question_planner.py     # Question framework builder
│   │   └── deep_researcher.py      # Research conductor
│   ├── content/
│   │   ├── prompts/                 # Prompt templates
│   │   │   ├── deep_questions_prompt.txt
│   │   │   ├── deep_subsegment_prompt.txt
│   │   │   └── main_segment_title_prompt.txt
│   │   └── script_generator.py     # Script generation
│   ├── orchestrator/
│   │   └── orchestrator.py         # Pipeline orchestration
│   ├── utils/
│   │   └── logger.py               # Logging utilities
│   └── main.py                     # Entry point
├── generated/                      # Generated artifacts (gitignored)
├── logs/                           # Log files (gitignored)
├── requirements.txt
├── README.md
└── .env.example
```

## Extending the System

### Future Phases (Not Yet Implemented)

The system is designed with extension points for:

- **Phase 5**: Asset Generation (images, infographics, B-roll suggestions)
- **Phase 6**: Audio Generation (TTS, background music)
- **Phase 7**: Video Assembly (editing, transitions, effects)
- **Phase 8**: Publishing (YouTube upload, metadata optimization)
- **Phase 9**: Cleanup (archiving, cache management)

Extension points exist in:
- `SubSegment.assets` field for asset metadata
- `Script.metadata` field for video/publishing info

### Adding Custom Research Sources

To integrate additional research APIs (e.g., Google Scholar, arXiv):

1. Create a new client in `src/research/`
2. Update `DeepResearcher` to use multiple sources
3. Merge results into `SubQuestionResearch`

### Customizing Prompts

Prompts are stored as text files in `src/content/prompts/`:
- Edit these files to adjust tone, style, or output format
- Changes take effect immediately (no code modifications needed)

## Troubleshooting

### Common Issues

**"No pending topics found"**
- Add topics to the database with `status='pending'`
- Check database connectivity

**API rate limiting**
- The system handles rate limits with exponential backoff
- Increase `LLM_BACKOFF_BASE` if needed

**Database connection errors**
- Verify `DATABASE_URL` format: `postgresql://user:password@host:port/database`
- Ensure PostgreSQL is running and accessible

**Script generation errors**
- Check logs in `logs/yt_deepresearch.log`
- Verify Perplexity API key is valid
- Check API quota/limits

## Development

### Testing

```bash
pytest tests/
```

### Code Quality

```bash
# Format code
black src/

# Type checking
mypy src/

# Linting
flake8 src/
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues, questions, or feature requests, please open an issue on GitHub.

---

**Note**: This system currently uses Perplexity API for all LLM operations. Future versions may integrate Gemini/Vertex AI for enhanced summarization and generation capabilities.
