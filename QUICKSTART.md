# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Installation
```bash
git clone https://github.com/funwithaistudio-tech/YT-DeepReSearch.git
cd YT-DeepReSearch
pip install -r requirements.txt
```

### Step 2: Configuration
```bash
# Copy example configuration
cp .env.example .env

# Edit .env and set your API keys
# Minimum required:
# - PERPLEXITY_API_KEY
# - GEMINI_API_KEY  
# - GOOGLE_CLOUD_PROJECT
```

### Step 3: Add a Topic
```bash
python -m src.main add-topic "Your Topic Title" "Description" "educational"
```

### Step 4: Run the Pipeline
```bash
# Full pipeline (all 8 phases)
python -m src.main run

# Or script only (faster for testing)
RUN_PHASES=script_only python -m src.main run
```

### Step 5: Check Results
```bash
# List topics and status
python -m src.main list-topics

# View outputs
ls output/
```

## 📋 Common Commands

### Topic Management
```bash
# Add a topic
python -m src.main add-topic "Climate Science" "Deep dive into climate change"

# List all topics
python -m src.main list-topics

# Run next pending topic
python -m src.main run

# Run specific topic by ID
python -m src.main run-topic 1

# Process all pending topics
python -m src.main run-all

# Process maximum 5 topics
python -m src.main run-all 5
```

### Pipeline Modes

#### Script Only (Fast)
```bash
export RUN_PHASES=script_only
python -m src.main run
```
Generates: Questions → Research → Script (stops here)

#### With Assets
```bash
export RUN_PHASES=assets_only
python -m src.main run
```
Generates: Questions → Research → Script → Images + Audio (stops here)

#### With Video
```bash
export RUN_PHASES=video_only
python -m src.main run
```
Generates: Questions → Research → Script → Assets → Video (stops here)

#### Full Pipeline
```bash
export RUN_PHASES=all
python -m src.main run
```
Generates: Questions → Research → Script → Assets → Video → YouTube Upload → Cleanup

## 🎯 Development Mode (No API Keys)

The system works without real API credentials for testing:

```bash
# Set placeholder values
cat > .env << EOF
PERPLEXITY_API_KEY=test_key
GEMINI_API_KEY=test_key
GOOGLE_CLOUD_PROJECT=test_project
EOF

# Run with placeholders
python -m src.main add-topic "Test Topic"
python -m src.main run
```

This generates:
- ✅ Mock research data
- ✅ Generated script structure
- ✅ Placeholder images (blue squares)
- ✅ Placeholder audio (small files)
- ✅ Placeholder video file
- ✅ Mock YouTube video ID

Perfect for testing the pipeline without API costs!

## 🔧 Configuration Tips

### Essential Settings (.env)
```env
# Required for production
PERPLEXITY_API_KEY=your_actual_key
GEMINI_API_KEY=your_actual_key
GOOGLE_CLOUD_PROJECT=your_gcp_project
GOOGLE_APPLICATION_CREDENTIALS=./credentials.json

# Optional but recommended
RUN_PHASES=all
CLEANUP_ON_SUCCESS=false
ARCHIVE_ARTIFACTS=true
```

### Quality Settings
```env
# Research depth
QUESTIONS_PER_TOPIC=5
SUB_QUESTIONS_PER_QUESTION=2

# Asset quality
IMAGE_RESOLUTION=1920x1080
VIDEO_CODEC=libx264
TTS_SPEAKING_RATE=1.0

# YouTube
YOUTUBE_PRIVACY_STATUS=unlisted
YOUTUBE_CATEGORY_ID=27
```

## 📂 Output Structure

After running, check these locations:

```
output/
├── questions_topic_1.json           # Question framework
├── research_sq_1_1_topic_1.json    # Research results
├── script_topic_1.json              # Generated script
├── script_topic_1_with_assets.json # Script with asset paths
├── main_video_topic_1.mp4          # Final video
├── assets/
│   ├── images/                      # Generated images
│   └── audio/                       # Generated audio
└── archive/                         # Archived artifacts
```

## ⚠️ Troubleshooting

### "Missing required settings" error
```bash
# Check your .env file exists
cat .env

# Ensure minimum keys are set
grep -E "PERPLEXITY|GEMINI|GOOGLE_CLOUD" .env
```

### "No pending topics to process"
```bash
# Add a topic first
python -m src.main add-topic "Your Topic"

# Verify it's added
python -m src.main list-topics
```

### Import errors
```bash
# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import pydantic; print('OK')"
```

### Permission errors on cleanup
```bash
# Disable cleanup temporarily
export CLEANUP_ON_SUCCESS=false
```

## 🎓 Learning Path

1. **Day 1**: Set up and run in placeholder mode
   - Install dependencies
   - Add test topics
   - Run script_only mode
   - Explore outputs

2. **Day 2**: Configure real APIs
   - Get Perplexity API key
   - Get Gemini API key
   - Set up GCP credentials
   - Uncomment API calls in code

3. **Day 3**: Full production pipeline
   - Add real topics
   - Run with assets_only
   - Test video assembly
   - Configure YouTube

4. **Day 4**: Optimization
   - Adjust quality settings
   - Fine-tune prompts
   - Test different niches
   - Monitor performance

## 💡 Pro Tips

1. **Start Small**: Use script_only mode to validate topics before generating assets
2. **Test Locally**: Run in placeholder mode to verify pipeline before using APIs
3. **Monitor Costs**: API calls can add up - use RUN_PHASES to control execution
4. **Archive First**: Keep ARCHIVE_ARTIFACTS=true to save important data
5. **Iterate**: Adjust questions and prompts based on output quality

## 🔗 Next Steps

- Read [README.md](README.md) for full documentation
- Check [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) for technical details
- Review [.env.example](.env.example) for all configuration options
- Explore the [src/](src/) directory for code structure

## 🆘 Getting Help

1. Check the logs: `tail -f logs/yt-deepresearch.log`
2. Review error messages carefully
3. Ensure all dependencies are installed
4. Verify API credentials are valid
5. Test with placeholder mode first

---

**Ready to create amazing educational videos? Start now!** 🎬
