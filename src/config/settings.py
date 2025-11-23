"""Configuration settings for YT-DeepReSearch using Pydantic Settings."""

from pathlib import Path
from typing import Optional

from pydantic import Field, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database configuration
    database_url: str = Field(
        ...,
        alias="DATABASE_URL",
        description="PostgreSQL database URL for topic storage"
    )

    # API Keys
    perplexity_api_key: str = Field(
        ...,
        alias="PERPLEXITY_API_KEY",
        description="Perplexity API key for research and generation"
    )
    
    # Optional GCP fields for future phases
    google_cloud_project: Optional[str] = Field(
        None,
        alias="GOOGLE_CLOUD_PROJECT",
        description="Google Cloud project ID for Vertex AI (optional)"
    )
    google_application_credentials: Optional[str] = Field(
        None,
        alias="GOOGLE_APPLICATION_CREDENTIALS",
        description="Path to GCP credentials JSON file (optional)"
    )
    gemini_api_key: Optional[str] = Field(
        None,
        alias="GEMINI_API_KEY",
        description="Gemini API key (optional, for future phases)"
    )

    # Directory paths
    generated_dir: Path = Field(
        default=Path("generated"),
        description="Directory for generated question frameworks and research"
    )
    assets_dir: Path = Field(
        default=Path("generated/assets"),
        description="Directory for generated assets (images, audio)"
    )
    output_dir: Path = Field(
        default=Path("output"),
        description="Directory for final video outputs"
    )
    logs_dir: Path = Field(
        default=Path("logs"),
        description="Directory for application logs"
    )

    # Content generation parameters
    main_segments: int = Field(
        default=5,
        description="Number of main segments in the script"
    )
    subsegments_per_main: int = Field(
        default=2,
        description="Number of subsegments per main segment"
    )
    words_per_subsegment_min: int = Field(
        default=600,
        description="Minimum words per subsegment"
    )
    words_per_subsegment_max: int = Field(
        default=700,
        description="Maximum words per subsegment"
    )

    # Retry and timeout configuration
    max_llm_retries: int = Field(
        default=3,
        description="Maximum number of retries for LLM API calls"
    )
    llm_backoff_base: float = Field(
        default=2.0,
        description="Base multiplier for exponential backoff (seconds)"
    )
    http_timeout_seconds: int = Field(
        default=120,
        description="HTTP timeout in seconds for API requests"
    )

    # Logging configuration
    log_level: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    @validator("generated_dir", "assets_dir", "output_dir", "logs_dir")
    def create_directories(cls, v: Path) -> Path:
        """Ensure directories exist."""
        v.mkdir(parents=True, exist_ok=True)
        return v

    @property
    def research_dir(self) -> Path:
        """Get the research subdirectory within generated_dir."""
        research_path = self.generated_dir / "research"
        research_path.mkdir(parents=True, exist_ok=True)
        return research_path

    def __repr__(self) -> str:
        """String representation hiding sensitive data."""
        return (
            f"Settings("
            f"database_url='***', "
            f"perplexity_api_key='***', "
            f"generated_dir={self.generated_dir}, "
            f"main_segments={self.main_segments}, "
            f"subsegments_per_main={self.subsegments_per_main})"
        )
