# YT-DeepReSearch - Quick Start Guide

Get up and running with YT-DeepReSearch in 5 minutes!

## Prerequisites

- Python 3.10 or higher
- PostgreSQL database
- Perplexity API key ([Get one here](https://www.perplexity.ai/))

## Step 1: Clone and Install

```bash
# Clone the repository
git clone https://github.com/funwithaistudio-tech/YT-DeepReSearch.git
cd YT-DeepReSearch

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Set Up Database

```bash
# Create a PostgreSQL database
createdb yt_deepresearch

# Run the schema
psql -d yt_deepresearch -f database_schema.sql
```

The schema includes sample topics to get you started!

## Step 3: Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your credentials
nano .env  # or use your preferred editor
```

Required variables:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/yt_deepresearch
PERPLEXITY_API_KEY=your_perplexity_api_key_here
```

## Step 4: Add a Topic

Connect to your database and add a topic:

```sql
INSERT INTO topics (topic, style, language, priority)
VALUES ('The Science of Sleep', 'educational', 'en', 10);
```

Or use the sample topics already included in the schema!

## Step 5: Run the Pipeline

```bash
# Process the next pending topic
python -m src.main
```

That's it! The pipeline will:
1. Fetch the highest-priority pending topic
2. Generate a question framework (5 main questions × 2 sub-questions)
3. Perform deep research on all 10 sub-questions
4. Generate a comprehensive ~6000-7000 word script
5. Save all artifacts to the `generated/` directory

## What Gets Generated?

After a successful run, check the `generated/` directory:

```
generated/
├── topic_1_question_framework.json    # Question framework
├── research/
│   ├── topic_1_m1_s1.json            # Research results (10 files)
│   ├── topic_1_m1_s2.json
│   └── ...
└── script_topic_1.json               # Final script
```

## Example Output Structure

### Question Framework
```json
{
  "topic_id": 1,
  "topic": "The Science of Sleep",
  "main_questions": [
    {
      "main_index": 1,
      "main_question": "What is sleep and why do we need it?",
      "subquestions": [
        {"sub_index": 1, "question": "How is sleep defined scientifically?"},
        {"sub_index": 2, "question": "What happens to our body during sleep?"}
      ]
    }
    // ... 4 more main questions
  ]
}
```

### Research Results
```json
{
  "topic_id": 1,
  "sub_question": "How is sleep defined scientifically?",
  "sources": [
    {
      "id": "src_1",
      "title": "Sleep Science: A Comprehensive Overview",
      "url": "https://example.com/sleep-science"
    }
    // ... more sources
  ],
  "summary": "Research findings...",
  "key_points": ["Point 1", "Point 2", "..."]
}
```

### Final Script
```json
{
  "topic_id": 1,
  "topic": "The Science of Sleep",
  "total_word_count": 6543,
  "main_segments": [
    {
      "index": 1,
      "title": "Understanding Sleep: The Basics",
      "subsegments": [
        {
          "index": 1,
          "text": "Sleep is defined as...",  // 600-700 words
          "word_count": 653,
          "sources_used": ["src_1", "src_3"]
        },
        {
          "index": 2,
          "text": "During sleep, our body...",  // 600-700 words
          "word_count": 687,
          "sources_used": ["src_2", "src_4"]
        }
      ]
    }
    // ... 4 more main segments
  ]
}
```

## Continuous Processing

To process multiple topics continuously:

```bash
# Process all pending topics
while python -m src.main; do
    echo "Processed one topic, checking for next..."
    sleep 5
done
```

Or set up a cron job:

```bash
# Add to crontab: run every hour
0 * * * * cd /path/to/YT-DeepReSearch && python -m src.main >> logs/cron.log 2>&1
```

## Monitoring Progress

Check logs:
```bash
tail -f logs/yt_deepresearch.log
```

Check database status:
```sql
SELECT id, topic, status, last_run_at, last_error 
FROM topics 
ORDER BY id DESC 
LIMIT 10;
```

## Troubleshooting

### "No pending topics found"
- Add topics to the database with `status='pending'`
- Check: `SELECT * FROM topics WHERE status='pending';`

### Database connection errors
- Verify `DATABASE_URL` format in `.env`
- Ensure PostgreSQL is running: `pg_isready`
- Test connection: `psql $DATABASE_URL`

### API errors
- Verify `PERPLEXITY_API_KEY` in `.env`
- Check API quota/limits
- Review logs for specific error messages

### Import errors
- Ensure all dependencies installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (needs 3.10+)

## Next Steps

- **Read the [full README](README.md)** for detailed architecture and configuration options
- **Check [example_usage.py](example_usage.py)** for programmatic usage examples
- **Review [CHANGELOG.md](CHANGELOG.md)** to understand what's new in version 2.0

## Need Help?

- 📖 [Full Documentation](README.md)
- 🐛 [Report Issues](https://github.com/funwithaistudio-tech/YT-DeepReSearch/issues)
- 💬 [Discussions](https://github.com/funwithaistudio-tech/YT-DeepReSearch/discussions)

---

Happy researching! 🎥🔬✨
