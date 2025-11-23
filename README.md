# YT-DeepReSearch

AI-powered deep research system for creating educational video scripts using Perplexity API and Gemini Vertex API. Produces in-depth content inspired by channels like Veritasium, Dhruv Rathee, and Fern.

## Features

- **Complete End-to-End Pipeline**: From research to YouTube publishing
- **Deep Research**: Uses Perplexity API for thorough topic investigation
- **AI Script Generation**: Gemini-powered script writing
- **Asset Generation**: Automated image and audio generation
- **Video Assembly**: Combines assets into polished videos
- **YouTube Publishing**: Automated upload with metadata
- **Intelligent Cleanup**: Archive and cleanup management

## Pipeline Phases

### Phase 0: Settings & Environment
- Configuration management via Pydantic
- Environment validation
- Logging setup

### Phase 1: Topic Management
- SQLite database for topic tracking
- Status tracking (pending, in_progress, completed, failed)

### Phase 2: Question Planning
- Generates structured research questions
- Configurable question depth (5 main questions × 2 sub-questions by default)

### Phase 3: Deep Research
- Perplexity API integration for comprehensive research
- Sources and citations tracking
- Research results saved as JSON

### Phase 4: Script Generation
- Gemini-powered script writing
- Structured segments and subsegments
- Duration estimation

### Phase 5: Asset Generation
- **Images**: Vertex AI Imagen for educational illustrations
- **Audio**: Google Cloud Text-to-Speech with voice selection
- Retry logic and error handling

### Phase 6: Video Assembly
- MoviePy-based video creation
- Image and audio synchronization
- Configurable resolution and codecs

### Phase 7: YouTube Publishing
- YouTube Data API integration
- Automated metadata generation
- Playlist support

### Phase 8: Cleanup
- Artifact archival
- Optional temp file deletion
- Space management

## Installation

### Prerequisites

- Python 3.8+
- Google Cloud Platform account (for Vertex AI and TTS)
- Perplexity API key
- YouTube Data API credentials (for publishing)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/funwithaistudio-tech/YT-DeepReSearch.git
cd YT-DeepReSearch
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env with your API keys and settings
```

4. Set up Google Cloud credentials:
   - Create a GCP project
   - Enable Vertex AI and Text-to-Speech APIs
   - Download service account credentials JSON
   - Set `GOOGLE_APPLICATION_CREDENTIALS` in `.env`

5. Set up YouTube API (for publishing):
   - Enable YouTube Data API v3 in Google Cloud Console
   - Create OAuth 2.0 credentials
   - Download `client_secret.json`
   - Set path in `.env`

## Usage

### Adding Topics

Add a new topic to the queue:
```bash
python -m src.main add-topic "Climate Change" "Deep dive into climate science" "educational"
```

### Listing Topics

View all topics and their status:
```bash
python -m src.main list-topics
```

### Running the Pipeline

Process the next pending topic:
```bash
python -m src.main run
```

Process all pending topics:
```bash
python -m src.main run-all
```

Process a specific topic:
```bash
python -m src.main run-topic 1
```

### Partial Pipeline Execution

You can run only specific phases by setting `RUN_PHASES` in `.env`:

- `all`: Run complete pipeline (default)
- `script_only`: Stop after script generation
- `assets_only`: Stop after asset generation
- `video_only`: Stop after video assembly (no publishing)

Example:
```bash
# In .env
RUN_PHASES=script_only
```

Then run:
```bash
python -m src.main run
```

## Configuration

All settings are configured via environment variables in `.env`. Key settings:

### API Configuration
- `PERPLEXITY_API_KEY`: Perplexity API key (required)
- `GEMINI_API_KEY`: Gemini API key (required)
- `GOOGLE_CLOUD_PROJECT`: GCP project ID (required)

### Research Settings
- `QUESTIONS_PER_TOPIC`: Number of main questions (default: 5)
- `SUB_QUESTIONS_PER_QUESTION`: Sub-questions per main (default: 2)
- `RESEARCH_DEPTH`: Research thoroughness (quick/medium/deep)

### Asset Settings
- `IMAGE_RESOLUTION`: Image size (default: 1920x1080)
- `IMAGES_PER_SUBSEGMENT`: Images per segment (default: 1)
- `TTS_VOICE_NAME`: Text-to-speech voice
- `TTS_SPEAKING_RATE`: Speech speed (default: 1.0)

### Video Settings
- `VIDEO_RESOLUTION`: Video resolution (default: 1920x1080)
- `VIDEO_FPS`: Frames per second (default: 30)
- `VIDEO_CODEC`: Codec (libx264 or h264_nvenc)

### YouTube Settings
- `YOUTUBE_CATEGORY_ID`: Video category (27 = Education)
- `YOUTUBE_PRIVACY_STATUS`: public/unlisted/private
- `YOUTUBE_PLAYLIST_ID`: Optional playlist ID

### Cleanup Settings
- `CLEANUP_ON_SUCCESS`: Delete temp files after success (default: false)
- `ARCHIVE_ARTIFACTS`: Archive artifacts (default: true)

## Project Structure

```
YT-DeepReSearch/
├── src/
│   ├── config/           # Settings and configuration
│   ├── domain/           # Domain models (Topic, Script, etc.)
│   ├── repository/       # Database operations
│   ├── research/         # Question planning and research
│   ├── content/          # Script generation
│   ├── assets/           # Image and audio generation
│   ├── video/            # Video assembly
│   ├── publish/          # YouTube publishing
│   ├── cleanup/          # Cleanup and archival
│   ├── orchestrator/     # Pipeline orchestration
│   ├── utils/            # Logging and helpers
│   └── main.py           # Entry point
├── output/               # Generated files
├── logs/                 # Log files
├── tests/                # Tests (to be added)
├── .env                  # Configuration (not in git)
├── .env.example          # Example configuration
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Development

### Running Tests
```bash
pytest tests/
```

### Code Quality
```bash
# Format code
black src/

# Lint
flake8 src/

# Type checking
mypy src/
```

## Troubleshooting

### Missing API Keys
Ensure all required API keys are set in `.env`:
- PERPLEXITY_API_KEY
- GEMINI_API_KEY
- GOOGLE_CLOUD_PROJECT

### GCP Authentication Issues
1. Verify `GOOGLE_APPLICATION_CREDENTIALS` points to valid JSON
2. Check service account has required permissions:
   - Vertex AI User
   - Cloud Text-to-Speech API User

### YouTube Upload Errors
1. Ensure OAuth credentials are configured
2. Run authentication flow on first use
3. Check `token.json` is created and valid

### Video Assembly Issues
MoviePy requires ffmpeg. Install it:
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/
```

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Acknowledgments

- Inspired by educational YouTube channels: Veritasium, Dhruv Rathee, Fern
- Built with Perplexity API, Google Gemini, and Vertex AI
- Uses MoviePy for video assembly
