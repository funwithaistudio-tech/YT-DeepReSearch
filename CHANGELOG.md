# Changelog

All notable changes to the YT-DeepReSearch project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-11-23

### Added - Complete Deep Research Pipeline

This major release completely redesigns the YT-DeepReSearch system with a database-driven, multi-phase research and script generation pipeline.

#### Core Infrastructure
- **Configuration System**: Pydantic-based settings management with environment variable support
- **Logging System**: Context-aware logging with topic_id and phase tagging using custom ContextLoggerAdapter
- **Database Integration**: PostgreSQL-based topic management with SQLAlchemy
- **Database Schema**: Complete schema with topics table, indexes, and sample data

#### Domain Models
- **Question Framework**: Structured model for 5 main questions with 2 sub-questions each (10 total)
- **Research Models**: Source and SubQuestionResearch models for organizing research data
- **Script Models**: SubSegment, MainSegment, and Script models for long-form content (~6000-7000 words)
- **Validation**: Pydantic validators ensuring exactly 5 main questions and 2 sub-questions per main

#### Research & Generation
- **Perplexity Client**: Robust HTTP client with retry logic, rate limiting, and error handling
- **Question Planner**: Generates comprehensive question frameworks using Perplexity API
- **Deep Researcher**: Performs targeted research for each sub-question with source tracking
- **Script Generator**: Creates long-form educational scripts from research data

#### Pipeline Orchestration
- **Orchestrator**: Manages complete pipeline flow from topic fetch to script generation
- **Phase Management**: Clear phase separation (0: Config, 1: Fetch, 2: Questions, 3: Research, 4: Script)
- **Error Handling**: Comprehensive error tracking with database status updates
- **Transaction Management**: Proper database transaction handling for topic state

#### Prompt Engineering
- **Deep Questions Prompt**: Template for generating question frameworks
- **Subsegment Prompt**: Template for generating 600-700 word subsegments with source attribution
- **Segment Title Prompt**: Template for creating compelling segment titles and summaries

#### Documentation & Examples
- **Comprehensive README**: Complete usage guide, architecture overview, and troubleshooting
- **Database Schema SQL**: Ready-to-use schema with indexes and sample data
- **Example Usage Script**: Demonstrates all key features and access patterns
- **.env.example**: Updated with all required and optional configuration variables

#### Quality Assurance
- **Import Validation**: All modules import successfully
- **Domain Model Tests**: Validators working correctly for all constraints
- **JSON Serialization**: All models serialize/deserialize properly
- **Pipeline Instantiation**: Complete pipeline can be instantiated successfully
- **Security Scan**: CodeQL security analysis passes with 0 alerts

### Changed

#### Breaking Changes
- **Entry Point**: `src/main.py` now uses Orchestrator instead of interactive input
- **Configuration**: Now requires DATABASE_URL and PERPLEXITY_API_KEY environment variables
- **Workflow**: Changed from trend-based to database-driven topic selection
- **Output Format**: Changed from plain text to structured JSON artifacts

#### Improvements
- **Script Length**: Increased from ~1500-1750 words to ~6000-7000 words (4× longer)
- **Research Depth**: Each topic now has 10 sub-questions with dedicated research
- **Source Attribution**: All script segments track and cite their sources
- **Extensibility**: Clear extension points for assets, video assembly, and publishing

### Removed
- **Interactive Input**: Removed manual topic input in favor of database-driven processing
- **Old Research Module**: Removed placeholder researcher.py
- **Old Script Generator**: Removed placeholder script generation logic

### Technical Details

#### Dependencies Added
- `sqlalchemy>=2.0.0` - Database ORM
- `psycopg2-binary>=2.9.0` - PostgreSQL adapter
- `pydantic>=2.4.0` - Data validation (already present)
- `pydantic-settings>=2.0.0` - Settings management (already present)

#### Architecture
```
src/
├── config/         # Settings and configuration
├── db/             # Database models and repository
├── domain/         # Core domain models (questions, research, script)
├── research/       # Research clients and logic
├── content/        # Script generation and prompts
├── orchestrator/   # Pipeline orchestration
└── utils/          # Logging and utilities
```

#### Generated Artifacts
- `generated/topic_X_question_framework.json` - Question framework (5×2 structure)
- `generated/research/topic_X_m{main}_s{sub}.json` - Research per sub-question (10 files)
- `generated/script_topic_X.json` - Final script with all segments

### Migration Guide

For users upgrading from 1.x:

1. **Update Environment Variables**
   ```bash
   cp .env.example .env
   # Add DATABASE_URL and PERPLEXITY_API_KEY
   ```

2. **Create Database**
   ```bash
   psql -U your_user -d your_db -f database_schema.sql
   ```

3. **Add Topics**
   ```sql
   INSERT INTO topics (topic, style, language, priority)
   VALUES ('Your Topic', 'educational', 'en', 10);
   ```

4. **Run Pipeline**
   ```bash
   python -m src.main
   ```

### Future Roadmap

#### Planned for Version 2.1+
- **Phase 5**: Asset Generation (images, infographics, B-roll suggestions)
- **Phase 6**: Audio Generation (TTS, background music)
- **Phase 7**: Video Assembly (editing, transitions, effects)
- **Phase 8**: Publishing (YouTube upload, metadata optimization)
- **Phase 9**: Cleanup (archiving, cache management)

#### Enhancements Under Consideration
- Gemini/Vertex AI integration for improved summarization
- Multi-language support for non-English content
- Custom prompt templates per topic
- Webhook notifications for pipeline completion
- REST API for programmatic access
- Web UI for topic management

### Security

- All API keys stored in environment variables (never in code)
- SQL injection prevention through parameterized queries
- Input validation on all external data
- CodeQL security analysis passing
- Secrets masked in logs and error messages

### Acknowledgments

This release represents a complete architectural redesign focused on:
- Production-grade code quality
- Extensible and maintainable architecture
- Comprehensive documentation
- Robust error handling
- Deep, well-researched content generation

---

## [1.0.0] - Initial Release

Initial skeleton release with basic structure and placeholder components.
