"""Gemini API client for content generation."""

import os
from typing import Dict, List, Optional
from loguru import logger
from google.cloud import aiplatform
from google.cloud.aiplatform import gapic
from utils.helpers import retry_with_backoff


class GeminiClient:
    """Client for interacting with Gemini/Vertex AI API."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        project_id: Optional[str] = None,
        location: str = "us-central1",
        model: str = "gemini-1.5-pro"
    ):
        """
        Initialize Gemini client.
        
        Args:
            api_key: Gemini API key (for direct API access)
            project_id: Google Cloud project ID
            location: GCP location
            model: Model to use
        """
        self.api_key = api_key
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
        self.location = location
        self.model = model
        
        # Initialize Vertex AI
        if self.project_id:
            aiplatform.init(project=self.project_id, location=self.location)
            logger.info(f"Initialized Vertex AI with project: {self.project_id}")
    
    @retry_with_backoff(max_retries=3, initial_delay=5)
    def generate_content(
        self,
        prompt: str,
        max_tokens: int = 8000,
        temperature: float = 0.7,
        system_instruction: Optional[str] = None
    ) -> str:
        """
        Generate content using Gemini API.
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature
            system_instruction: System instruction for model
        
        Returns:
            Generated content text
        """
        logger.info(f"Generating content with Gemini (prompt length: {len(prompt)})")
        
        try:
            # Use Vertex AI SDK
            from vertexai.generative_models import GenerativeModel, GenerationConfig
            
            model = GenerativeModel(
                self.model,
                system_instruction=system_instruction or []
            )
            
            generation_config = GenerationConfig(
                max_output_tokens=max_tokens,
                temperature=temperature,
            )
            
            response = model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            content = response.text
            logger.info(f"Gemini generation successful (response length: {len(content)})")
            
            return content
        
        except Exception as e:
            logger.error(f"Gemini API request failed: {str(e)}")
            raise
    
    @retry_with_backoff(max_retries=3, initial_delay=5)
    def generate_structured_content(
        self,
        prompt: str,
        schema: Dict,
        max_tokens: int = 8000,
        temperature: float = 0.7
    ) -> Dict:
        """
        Generate structured content following a schema.
        
        Args:
            prompt: Input prompt
            schema: JSON schema for structured output
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature
        
        Returns:
            Generated structured content as dictionary
        """
        logger.info(f"Generating structured content with Gemini")
        
        try:
            from vertexai.generative_models import GenerativeModel, GenerationConfig
            
            model = GenerativeModel(self.model)
            
            generation_config = GenerationConfig(
                max_output_tokens=max_tokens,
                temperature=temperature,
            )
            
            # Add schema guidance to prompt
            structured_prompt = f"{prompt}\n\nProvide response in JSON format following this schema: {schema}"
            
            response = model.generate_content(
                structured_prompt,
                generation_config=generation_config
            )
            
            import json
            content = response.text
            
            # Try to extract JSON from response
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            result = json.loads(content)
            logger.info(f"Gemini structured generation successful")
            
            return result
        
        except Exception as e:
            logger.error(f"Gemini structured generation failed: {str(e)}")
            raise
