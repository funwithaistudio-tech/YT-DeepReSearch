"""Configuration settings for YT-DeepReSearch system."""

import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Keys
    perplexity_api_key: str = ""
    gemini_api_key: str = ""
    
    # Google Cloud Settings
    google_cloud_project: Optional[str] = None
    google_application_credentials: Optional[str] = None
    
    # Output Configuration
    output_dir: str = "./output"
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "./logs/yt-deepresearch.log"
    
    # Research Settings
    max_search_results: int = 10
    research_depth: str = "deep"
    
    # Script Generation Settings
    script_language: str = "en"
    script_length: str = "medium"
    content_style: str = "educational"
    
    # Excel Job Queue Settings
    excel_input_path: str = "./input/topics.xlsx"
    excel_sheet_name: str = "Topics"
    
    # Phase Configuration
    max_retries: int = 3
    retry_delay: int = 5
    timeout: int = 300
    
    # Token Safety
    max_tokens_per_request: int = 4000
    token_buffer: int = 500
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    def __init__(self, **kwargs):
        """Initialize settings and create required directories."""
        super().__init__(**kwargs)
        self._create_directories()
    
    def _create_directories(self):
        """Create required directories if they don't exist."""
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        Path(self.log_file).parent.mkdir(parents=True, exist_ok=True)
        Path(self.excel_input_path).parent.mkdir(parents=True, exist_ok=True)
