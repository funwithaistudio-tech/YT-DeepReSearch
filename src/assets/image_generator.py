"""Image generation module using Vertex AI Imagen."""

import time
from pathlib import Path
from typing import List, Optional
from PIL import Image
import io

from src.domain.models import Script, SubSegment
from src.config.settings import Settings
from src.utils.logger import get_logger

logger = get_logger()


class ImageGenerator:
    """Generates images for script segments using Vertex AI Imagen."""
    
    def __init__(self, settings: Settings):
        """Initialize image generator.
        
        Args:
            settings: Application settings
        """
        self.settings = settings
        self.image_dir = Path(settings.assets_dir) / "images"
        self.image_dir.mkdir(parents=True, exist_ok=True)
        
        # Parse resolution
        width, height = map(int, settings.image_resolution.split("x"))
        self.width = width
        self.height = height
        
        # Initialize Vertex AI client (placeholder)
        self._init_vertex_client()
    
    def _init_vertex_client(self):
        """Initialize Vertex AI client."""
        # Placeholder for Vertex AI initialization
        # In production:
        # from google.cloud import aiplatform
        # aiplatform.init(
        #     project=self.settings.google_cloud_project,
        #     location=self.settings.gcp_location
        # )
        logger.info("Initialized Vertex AI client (placeholder)")
    
    def generate_images_for_script(self, script: Script) -> Script:
        """Generate images for all subsegments in the script.
        
        Args:
            script: Script to generate images for
            
        Returns:
            Updated Script with image paths
        """
        logger.info(f"Generating images for script: {script.title}")
        
        for main_segment in script.main_segments:
            for subsegment in main_segment.sub_segments:
                if self.settings.skip_existing_assets and subsegment.assets.get("images"):
                    logger.info(f"Skipping existing images for {subsegment.id}")
                    continue
                
                images = self._generate_images_for_subsegment(
                    subsegment,
                    script.topic_id
                )
                
                for img_path in images:
                    subsegment.add_image(str(img_path))
                
                logger.info(f"Generated {len(images)} images for subsegment {subsegment.id}")
        
        return script
    
    def _generate_images_for_subsegment(
        self, 
        subsegment: SubSegment,
        topic_id: int
    ) -> List[Path]:
        """Generate images for a single subsegment.
        
        Args:
            subsegment: Subsegment to generate images for
            topic_id: Topic ID for file naming
            
        Returns:
            List of generated image paths
        """
        image_paths = []
        
        for i in range(self.settings.images_per_subsegment):
            # Generate prompt from subsegment content
            prompt = self._create_image_prompt(subsegment)
            
            # Generate image with retry logic
            image_path = self._generate_image_with_retry(
                prompt,
                f"topic_{topic_id}_{subsegment.id}_{i}"
            )
            
            if image_path:
                image_paths.append(image_path)
        
        return image_paths
    
    def _create_image_prompt(self, subsegment: SubSegment) -> str:
        """Create image generation prompt from subsegment.
        
        Args:
            subsegment: Subsegment
            
        Returns:
            Image prompt
        """
        # Extract key concepts from content (simplified)
        # In production, use NLP or AI to extract visual concepts
        content_preview = subsegment.content[:200]
        
        prompt = f"Educational illustration for: {subsegment.title}. "
        prompt += f"Visual style: clean, modern, professional. "
        prompt += f"Context: {content_preview}..."
        
        return prompt
    
    def _generate_image_with_retry(self, prompt: str, filename: str) -> Optional[Path]:
        """Generate image with retry logic.
        
        Args:
            prompt: Image generation prompt
            filename: Base filename
            
        Returns:
            Path to generated image, or None if failed
        """
        for attempt in range(self.settings.image_retry_count):
            try:
                logger.debug(f"Generating image (attempt {attempt + 1}): {filename}")
                
                # Generate image (placeholder)
                image_data = self._call_imagen_api(prompt)
                
                if image_data:
                    # Save and resize image
                    image_path = self._save_and_resize_image(image_data, filename)
                    return image_path
                
            except Exception as e:
                logger.warning(f"Image generation attempt {attempt + 1} failed: {e}")
                if attempt < self.settings.image_retry_count - 1:
                    time.sleep(self.settings.image_retry_delay)
        
        logger.error(f"Failed to generate image after {self.settings.image_retry_count} attempts")
        return None
    
    def _call_imagen_api(self, prompt: str) -> bytes:
        """Call Vertex AI Imagen API.
        
        Args:
            prompt: Image prompt
            
        Returns:
            Image bytes
        """
        # Placeholder for actual Imagen API call
        # In production:
        # from vertexai.preview.vision_models import ImageGenerationModel
        # model = ImageGenerationModel.from_pretrained(self.settings.image_model)
        # response = model.generate_images(
        #     prompt=prompt,
        #     number_of_images=1,
        #     aspect_ratio=self.settings.image_aspect_ratio
        # )
        # return response.images[0]._image_bytes
        
        # Create a placeholder image
        img = Image.new('RGB', (self.width, self.height), color='lightblue')
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        return buf.getvalue()
    
    def _save_and_resize_image(self, image_data: bytes, filename: str) -> Path:
        """Save and resize image to exact dimensions.
        
        Args:
            image_data: Image bytes
            filename: Base filename
            
        Returns:
            Path to saved image
        """
        # Load image
        img = Image.open(io.BytesIO(image_data))
        
        # Resize to exact dimensions
        img = img.resize((self.width, self.height), Image.LANCZOS)
        
        # Save
        output_path = self.image_dir / f"{filename}.png"
        img.save(output_path, format='PNG')
        
        logger.debug(f"Saved image to {output_path}")
        return output_path
