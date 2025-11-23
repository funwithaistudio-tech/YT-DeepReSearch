"""Asset generation coordinator."""

import json
from pathlib import Path

from src.domain.models import Script
from src.config.settings import Settings
from src.assets.image_generator import ImageGenerator
from src.assets.audio_generator import AudioGenerator
from src.utils.logger import get_logger

logger = get_logger()


class AssetGenerator:
    """Coordinates image and audio generation for scripts."""
    
    def __init__(self, settings: Settings):
        """Initialize asset generator.
        
        Args:
            settings: Application settings
        """
        self.settings = settings
        self.image_generator = ImageGenerator(settings)
        self.audio_generator = AudioGenerator(settings)
        self.output_dir = Path(settings.output_dir)
    
    def generate_assets(self, script: Script) -> Script:
        """Generate all assets (images and audio) for the script.
        
        Args:
            script: Script to generate assets for
            
        Returns:
            Updated Script with asset paths
        """
        logger.info(f"Starting asset generation for script: {script.title}")
        
        # Generate images
        logger.info("Generating images...")
        script = self.image_generator.generate_images_for_script(script)
        
        # Generate audio
        logger.info("Generating audio...")
        script = self.audio_generator.generate_audio_for_script(script)
        
        # Update total duration based on actual audio
        script.total_duration_estimate = script.estimate_total_duration()
        
        # Save updated script with assets
        self._save_script_with_assets(script)
        
        logger.info(f"Asset generation complete. Total duration: {script.total_duration_estimate:.1f}s")
        
        return script
    
    def _save_script_with_assets(self, script: Script):
        """Save script with asset information.
        
        Args:
            script: Script to save
        """
        filename = f"script_topic_{script.topic_id}_with_assets.json"
        filepath = self.output_dir / filename
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(script.model_dump(), f, indent=2, default=str)
        
        logger.info(f"Saved script with assets to {filepath}")
