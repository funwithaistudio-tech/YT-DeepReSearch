#!/usr/bin/env python3
"""
Example script demonstrating how to use the YT-DeepReSearch pipeline.

This script shows:
1. How to set up the environment
2. How to add topics to the database
3. How to run the pipeline
4. How to access the generated artifacts
"""

import os
import sys
from pathlib import Path

# Example 1: Setting environment variables programmatically
# In production, use .env file instead
def setup_environment():
    """Set up required environment variables."""
    print("=== Setting Up Environment ===")
    
    # Required: Database connection
    os.environ['DATABASE_URL'] = 'postgresql://user:password@localhost:5432/yt_deepresearch'
    
    # Required: Perplexity API key
    os.environ['PERPLEXITY_API_KEY'] = 'your_perplexity_api_key_here'
    
    # Optional: Google Cloud settings (for future phases)
    # os.environ['GOOGLE_CLOUD_PROJECT'] = 'your-project-id'
    # os.environ['GEMINI_API_KEY'] = 'your_gemini_key'
    
    # Optional: Override default settings
    # os.environ['LOG_LEVEL'] = 'DEBUG'
    # os.environ['MAIN_SEGMENTS'] = '5'
    # os.environ['WORDS_PER_SUBSEGMENT_MIN'] = '600'
    
    print("✓ Environment configured")


# Example 2: Adding topics to the database (SQL)
def example_add_topics_sql():
    """
    Example SQL commands to add topics to the database.
    Run these in your PostgreSQL client or using psycopg2.
    """
    sql_commands = """
    -- Add a single topic
    INSERT INTO topics (topic, style, language, priority)
    VALUES ('Quantum Computing Explained', 'educational', 'en', 10);
    
    -- Add multiple topics
    INSERT INTO topics (topic, style, language, priority) VALUES
        ('The Future of Artificial Intelligence', 'educational', 'en', 9),
        ('Climate Change: Latest Research', 'documentary', 'en', 8),
        ('History of the Internet', 'educational', 'en', 7);
    
    -- Check pending topics
    SELECT id, topic, status, priority FROM topics WHERE status = 'pending';
    """
    
    print("\n=== Example SQL Commands ===")
    print(sql_commands)


# Example 3: Running the pipeline programmatically
def run_pipeline_programmatically():
    """Run the pipeline programmatically instead of using command line."""
    print("\n=== Running Pipeline Programmatically ===")
    
    try:
        from src.config.settings import Settings
        from src.orchestrator.orchestrator import Orchestrator
        
        # Load settings
        settings = Settings()
        print(f"✓ Settings loaded")
        print(f"  - Generated dir: {settings.generated_dir}")
        print(f"  - Main segments: {settings.main_segments}")
        print(f"  - Words per subsegment: {settings.words_per_subsegment_min}-{settings.words_per_subsegment_max}")
        
        # Create orchestrator
        orchestrator = Orchestrator(settings)
        print("✓ Orchestrator initialized")
        
        # Process next topic
        print("\nProcessing next pending topic...")
        processed = orchestrator.run_for_next_topic()
        
        if processed:
            print("✓ Topic processed successfully!")
        else:
            print("ℹ No pending topics found")
        
        # Clean up
        orchestrator.close()
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


# Example 4: Accessing generated artifacts
def access_generated_artifacts(topic_id: int = 1):
    """Show how to access generated artifacts."""
    print(f"\n=== Accessing Generated Artifacts for Topic {topic_id} ===")
    
    import json
    from pathlib import Path
    
    generated_dir = Path("generated")
    
    # 1. Question Framework
    framework_file = generated_dir / f"topic_{topic_id}_question_framework.json"
    if framework_file.exists():
        with open(framework_file, 'r') as f:
            framework = json.load(f)
        print(f"\n✓ Question Framework:")
        print(f"  Topic: {framework['topic']}")
        print(f"  Main Questions: {len(framework['main_questions'])}")
        for mq in framework['main_questions']:
            print(f"    {mq['main_index']}. {mq['main_question']}")
    else:
        print(f"✗ Question framework not found: {framework_file}")
    
    # 2. Research Results
    research_dir = generated_dir / "research"
    if research_dir.exists():
        research_files = list(research_dir.glob(f"topic_{topic_id}_*.json"))
        print(f"\n✓ Research Results: {len(research_files)} files")
        for rf in sorted(research_files)[:3]:  # Show first 3
            with open(rf, 'r') as f:
                research = json.load(f)
            print(f"  - {rf.name}: {research['sub_question'][:50]}... ({len(research['sources'])} sources)")
    else:
        print("✗ Research directory not found")
    
    # 3. Final Script
    script_file = generated_dir / f"script_topic_{topic_id}.json"
    if script_file.exists():
        with open(script_file, 'r') as f:
            script = json.load(f)
        print(f"\n✓ Final Script:")
        print(f"  Topic: {script['topic']}")
        print(f"  Total Words: {script['total_word_count']}")
        print(f"  Main Segments: {len(script['main_segments'])}")
        for ms in script['main_segments']:
            print(f"    {ms['index']}. {ms['title']}")
            print(f"       Subsegments: {len(ms['subsegments'])}, Words: {sum(s['word_count'] for s in ms['subsegments'])}")
    else:
        print(f"✗ Script not found: {script_file}")


# Example 5: Batch processing
def batch_process_topics(max_topics: int = 5):
    """Process multiple topics in a batch."""
    print(f"\n=== Batch Processing (max {max_topics} topics) ===")
    
    from src.config.settings import Settings
    from src.orchestrator.orchestrator import Orchestrator
    
    settings = Settings()
    orchestrator = Orchestrator(settings)
    
    processed_count = 0
    
    try:
        while processed_count < max_topics:
            print(f"\nProcessing topic {processed_count + 1}/{max_topics}...")
            
            processed = orchestrator.run_for_next_topic()
            
            if not processed:
                print("No more pending topics")
                break
            
            processed_count += 1
            print(f"✓ Processed {processed_count} topic(s)")
    
    finally:
        orchestrator.close()
    
    return processed_count


# Main execution
if __name__ == "__main__":
    print("YT-DeepReSearch Pipeline - Example Usage\n")
    print("=" * 60)
    
    # Note: This is a demonstration script
    # In production, use environment variables from .env file
    
    # Show example SQL commands
    example_add_topics_sql()
    
    print("\n" + "=" * 60)
    print("\nTo run the pipeline in production:")
    print("1. Set up your .env file with DATABASE_URL and PERPLEXITY_API_KEY")
    print("2. Create the database schema using database_schema.sql")
    print("3. Add topics to the database")
    print("4. Run: python -m src.main")
    print("\nGenerated artifacts will be in:")
    print("  - generated/topic_X_question_framework.json")
    print("  - generated/research/topic_X_m*_s*.json")
    print("  - generated/script_topic_X.json")
    print("\n" + "=" * 60)
