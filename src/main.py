"""Main entry point for YT-DeepReSearch system."""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import Settings
from research.researcher import DeepResearcher
from content.script_generator import ScriptGenerator
from utils.logger import setup_logger


def main():
    """Main execution function."""
    # Setup logging
    logger = setup_logger()
    logger.info("Starting YT-DeepReSearch system...")
    
    # Load configuration
    settings = Settings()
    
    try:
        # Initialize components
        researcher = DeepResearcher(
            perplexity_api_key=settings.perplexity_api_key,
            gemini_api_key=settings.gemini_api_key
        )
        
        script_generator = ScriptGenerator(
            gemini_api_key=settings.gemini_api_key
        )
        
        # Get topic from user
        topic = input("Enter research topic: ")
        
        # Perform deep research
        logger.info(f"Researching topic: {topic}")
        research_data = researcher.research(topic)
        
        # Generate script
        logger.info("Generating video script...")
        script = script_generator.generate_script(research_data)
        
        # Save output
        output_path = Path(settings.output_dir) / f"{topic.replace(' ', '_')}_script.txt"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(script)
        
        logger.info(f"Script saved to: {output_path}")
        print(f"\nScript generated successfully!\nSaved to: {output_path}")
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()    
