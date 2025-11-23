"""Topic repository for database operations."""

from datetime import datetime
from typing import Optional

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

from src.config.settings import Settings
from src.db.models import TopicJob
from src.utils.logger import get_logger


class TopicRepository:
    """Repository for managing topic jobs in the database.
    
    Handles fetching topics, updating their status, and error tracking.
    """

    def __init__(self, settings: Settings):
        """Initialize the repository with database connection.
        
        Args:
            settings: Application settings containing DATABASE_URL
        """
        self.settings = settings
        self.logger = get_logger()
        self.engine: Engine = create_engine(
            settings.database_url,
            pool_pre_ping=True,  # Verify connections before using
            echo=False  # Set to True for SQL debugging
        )

    def fetch_next_topic(self) -> Optional[TopicJob]:
        """Fetch the next pending topic to process.
        
        Selects a pending topic with highest priority, marks it as in_progress,
        and sets last_run_at to current time.
        
        Returns:
            TopicJob if found, None if no pending topics exist
            
        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            with self.engine.connect() as conn:
                # Start a transaction
                with conn.begin():
                    # Fetch next pending topic with highest priority
                    query = text("""
                        SELECT id, topic, style, language, status, priority, 
                               last_run_at, last_error, youtube_video_id
                        FROM topics
                        WHERE status = 'pending'
                        ORDER BY priority DESC, id ASC
                        LIMIT 1
                        FOR UPDATE SKIP LOCKED
                    """)
                    
                    result = conn.execute(query)
                    row = result.fetchone()
                    
                    if not row:
                        self.logger.info("No pending topics found in database")
                        return None
                    
                    # Convert row to TopicJob
                    topic_job = TopicJob(
                        id=row[0],
                        topic=row[1],
                        style=row[2],
                        language=row[3],
                        status=row[4],
                        priority=row[5],
                        last_run_at=row[6],
                        last_error=row[7],
                        youtube_video_id=row[8]
                    )
                    
                    # Mark as in_progress
                    update_query = text("""
                        UPDATE topics
                        SET status = 'in_progress',
                            last_run_at = :now,
                            last_error = NULL
                        WHERE id = :topic_id
                    """)
                    
                    conn.execute(
                        update_query,
                        {"topic_id": topic_job.id, "now": datetime.utcnow()}
                    )
                    
                    self.logger.info(
                        f"Fetched topic {topic_job.id}: '{topic_job.topic}' "
                        f"(style={topic_job.style}, language={topic_job.language})"
                    )
                    
                    return topic_job
                    
        except SQLAlchemyError as e:
            self.logger.error(f"Database error while fetching topic: {e}")
            raise

    def mark_topic_done(
        self, topic_id: int, youtube_video_id: Optional[str] = None
    ) -> None:
        """Mark a topic as completed.
        
        Args:
            topic_id: ID of the topic to mark as done
            youtube_video_id: Optional YouTube video ID if published
            
        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            with self.engine.connect() as conn:
                with conn.begin():
                    query = text("""
                        UPDATE topics
                        SET status = 'completed',
                            youtube_video_id = :video_id,
                            last_error = NULL
                        WHERE id = :topic_id
                    """)
                    
                    conn.execute(
                        query,
                        {"topic_id": topic_id, "video_id": youtube_video_id}
                    )
                    
                    self.logger.info(
                        f"Marked topic {topic_id} as completed "
                        f"(video_id={youtube_video_id})"
                    )
                    
        except SQLAlchemyError as e:
            self.logger.error(
                f"Database error while marking topic {topic_id} as done: {e}"
            )
            raise

    def mark_topic_failed(self, topic_id: int, error_message: str) -> None:
        """Mark a topic as failed with error message.
        
        Args:
            topic_id: ID of the topic to mark as failed
            error_message: Error message describing the failure
            
        Raises:
            SQLAlchemyError: If database operation fails
        """
        try:
            with self.engine.connect() as conn:
                with conn.begin():
                    query = text("""
                        UPDATE topics
                        SET status = 'failed',
                            last_error = :error_msg
                        WHERE id = :topic_id
                    """)
                    
                    conn.execute(
                        query,
                        {"topic_id": topic_id, "error_msg": error_message}
                    )
                    
                    self.logger.error(
                        f"Marked topic {topic_id} as failed: {error_message}"
                    )
                    
        except SQLAlchemyError as e:
            self.logger.error(
                f"Database error while marking topic {topic_id} as failed: {e}"
            )
            raise

    def close(self) -> None:
        """Close the database connection."""
        self.engine.dispose()
        self.logger.info("Database connection closed")
