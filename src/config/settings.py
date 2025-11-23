"""Settings and configuration management using Pydantic."""

from typing import Optional, Literal
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # API Keys
    perplexity_api_key: str = Field(default="", description="Perplexity API key")
    gemini_api_key: str = Field(default="", description="Gemini API key")
    youtube_api_key: Optional[str] = Field(default=None, description="YouTube Data API key")
    
    # Google Cloud Settings
    google_cloud_project: str = Field(default="", description="GCP project ID")
    google_application_credentials: Optional[str] = Field(
        default=None, 
        description="Path to GCP credentials JSON"
    )
    gcp_location: str = Field(default="us-central1", description="GCP location for Vertex AI")
    
    # Database
    database_url: str = Field(
        default="sqlite:///./yt_deepresearch.db",
        description="Database connection URL"
    )
    
    # Output Configuration
    output_dir: str = Field(default="./output", description="Output directory")
    logs_dir: str = Field(default="./logs", description="Logs directory")
    assets_dir: str = Field(default="./output/assets", description="Assets directory")
    
    # Logging
    log_level: str = Field(default="INFO", description="Logging level")
    log_file: str = Field(
        default="./logs/yt-deepresearch.log",
        description="Log file path"
    )
    
    # Research Settings
    max_search_results: int = Field(default=10, description="Max search results")
    research_depth: Literal["quick", "medium", "deep"] = Field(
        default="deep",
        description="Research depth"
    )
    questions_per_topic: int = Field(default=5, description="Main questions per topic")
    sub_questions_per_question: int = Field(default=2, description="Sub-questions per main question")
    
    # Script Generation Settings
    script_language: str = Field(default="en", description="Script language code")
    script_length: Literal["short", "medium", "long"] = Field(
        default="medium",
        description="Script length"
    )
    content_style: Literal["educational", "entertaining", "documentary"] = Field(
        default="educational",
        description="Content style"
    )
    
    # Asset Generation Settings
    image_model: str = Field(
        default="imagegeneration@006",
        description="Vertex AI image generation model"
    )
    image_resolution: str = Field(default="1920x1080", description="Image resolution")
    image_aspect_ratio: str = Field(default="16:9", description="Image aspect ratio")
    images_per_subsegment: int = Field(default=1, description="Images per subsegment")
    image_retry_count: int = Field(default=3, description="Image generation retry count")
    image_retry_delay: int = Field(default=5, description="Delay between image retries (seconds)")
    
    # TTS Settings
    tts_language_code: str = Field(default="en-US", description="TTS language code")
    tts_voice_name: Optional[str] = Field(default=None, description="TTS voice name")
    tts_speaking_rate: float = Field(default=1.0, description="TTS speaking rate")
    tts_pitch: float = Field(default=0.0, description="TTS pitch")
    tts_delay_between_calls: int = Field(default=2, description="Delay between TTS API calls (seconds)")
    
    # Video Assembly Settings
    video_resolution: str = Field(default="1920x1080", description="Video resolution")
    video_fps: int = Field(default=30, description="Video FPS")
    video_codec: str = Field(default="libx264", description="Video codec (libx264, h264_nvenc)")
    video_bitrate: str = Field(default="5000k", description="Video bitrate")
    
    # YouTube Publishing Settings
    youtube_client_secret_path: str = Field(
        default="./client_secret.json",
        description="YouTube OAuth client secret path"
    )
    youtube_token_path: str = Field(
        default="./token.json",
        description="YouTube OAuth token path"
    )
    youtube_category_id: str = Field(default="27", description="YouTube category ID (27=Education)")
    youtube_privacy_status: Literal["public", "unlisted", "private"] = Field(
        default="unlisted",
        description="YouTube video privacy status"
    )
    youtube_playlist_id: Optional[str] = Field(
        default=None,
        description="YouTube playlist ID (optional)"
    )
    
    # Cleanup Settings
    cleanup_on_success: bool = Field(
        default=False,
        description="Delete heavy temp files after successful publish"
    )
    archive_artifacts: bool = Field(
        default=True,
        description="Archive artifacts before cleanup"
    )
    
    # Pipeline Control
    run_phases: str = Field(
        default="all",
        description="Phases to run (all, script_only, assets_only, etc.)"
    )
    skip_existing_assets: bool = Field(
        default=True,
        description="Skip asset generation if files already exist"
    )
    
    def validate_required_settings(self):
        """Validate that required settings are present."""
        errors = []
        
        if not self.perplexity_api_key:
            errors.append("PERPLEXITY_API_KEY is required")
        
        if not self.gemini_api_key:
            errors.append("GEMINI_API_KEY is required")
        
        if not self.google_cloud_project:
            errors.append("GOOGLE_CLOUD_PROJECT is required")
        
        if errors:
            raise ValueError(f"Missing required settings: {', '.join(errors)}")
    
    def ensure_directories(self):
        """Ensure all required directories exist."""
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        Path(self.logs_dir).mkdir(parents=True, exist_ok=True)
        Path(self.assets_dir).mkdir(parents=True, exist_ok=True)
        Path(self.assets_dir).joinpath("images").mkdir(parents=True, exist_ok=True)
        Path(self.assets_dir).joinpath("audio").mkdir(parents=True, exist_ok=True)
