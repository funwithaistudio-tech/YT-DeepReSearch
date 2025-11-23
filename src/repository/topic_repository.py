"""Database repository for topic management."""

import sqlite3
from typing import Optional, List
from datetime import datetime
from pathlib import Path

from src.domain.models import Topic, TopicStatus
from src.utils.logger import get_logger

logger = get_logger()


class TopicRepository:
    """Repository for managing topics in the database."""
    
    def __init__(self, database_url: str):
        """Initialize repository.
        
        Args:
            database_url: SQLite database path (e.g., 'sqlite:///./yt_deepresearch.db')
        """
        # Extract file path from sqlite:/// URL
        if database_url.startswith("sqlite:///"):
            db_path = database_url.replace("sqlite:///", "")
        else:
            db_path = database_url
        
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
    
    def _get_connection(self):
        """Get database connection."""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn
    
    def _init_database(self):
        """Initialize database schema."""
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS topics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    niche TEXT DEFAULT 'educational',
                    status TEXT DEFAULT 'pending',
                    youtube_video_id TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    error_message TEXT
                )
            """)
            conn.commit()
    
    def create_topic(self, title: str, description: str = None, niche: str = "educational") -> Topic:
        """Create a new topic.
        
        Args:
            title: Topic title
            description: Topic description
            niche: Content niche
            
        Returns:
            Created Topic
        """
        now = datetime.utcnow().isoformat()
        
        with self._get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO topics (title, description, niche, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (title, description, niche, TopicStatus.PENDING.value, now, now))
            conn.commit()
            topic_id = cursor.lastrowid
        
        logger.info(f"Created topic {topic_id}: {title}")
        return self.get_topic(topic_id)
    
    def get_topic(self, topic_id: int) -> Optional[Topic]:
        """Get topic by ID.
        
        Args:
            topic_id: Topic ID
            
        Returns:
            Topic if found, None otherwise
        """
        with self._get_connection() as conn:
            row = conn.execute("SELECT * FROM topics WHERE id = ?", (topic_id,)).fetchone()
            if row:
                return self._row_to_topic(row)
        return None
    
    def get_next_pending_topic(self) -> Optional[Topic]:
        """Get next pending topic to process.
        
        Returns:
            Next pending Topic, or None if no pending topics
        """
        with self._get_connection() as conn:
            row = conn.execute("""
                SELECT * FROM topics 
                WHERE status = ? 
                ORDER BY created_at ASC 
                LIMIT 1
            """, (TopicStatus.PENDING.value,)).fetchone()
            
            if row:
                return self._row_to_topic(row)
        return None
    
    def update_topic_status(
        self, 
        topic_id: int, 
        status: TopicStatus, 
        youtube_video_id: str = None,
        error_message: str = None
    ):
        """Update topic status.
        
        Args:
            topic_id: Topic ID
            status: New status
            youtube_video_id: YouTube video ID (optional)
            error_message: Error message if failed (optional)
        """
        now = datetime.utcnow().isoformat()
        
        with self._get_connection() as conn:
            conn.execute("""
                UPDATE topics 
                SET status = ?, youtube_video_id = ?, error_message = ?, updated_at = ?
                WHERE id = ?
            """, (status.value, youtube_video_id, error_message, now, topic_id))
            conn.commit()
        
        logger.info(f"Updated topic {topic_id} status to {status.value}")
    
    def mark_topic_in_progress(self, topic_id: int):
        """Mark topic as in progress."""
        self.update_topic_status(topic_id, TopicStatus.IN_PROGRESS)
    
    def mark_topic_completed(self, topic_id: int, youtube_video_id: str = None):
        """Mark topic as completed."""
        self.update_topic_status(topic_id, TopicStatus.COMPLETED, youtube_video_id=youtube_video_id)
    
    def mark_topic_failed(self, topic_id: int, error_message: str):
        """Mark topic as failed."""
        self.update_topic_status(topic_id, TopicStatus.FAILED, error_message=error_message)
    
    def list_topics(self, status: Optional[TopicStatus] = None) -> List[Topic]:
        """List topics, optionally filtered by status.
        
        Args:
            status: Filter by status (optional)
            
        Returns:
            List of topics
        """
        with self._get_connection() as conn:
            if status:
                rows = conn.execute(
                    "SELECT * FROM topics WHERE status = ? ORDER BY created_at DESC",
                    (status.value,)
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM topics ORDER BY created_at DESC"
                ).fetchall()
            
            return [self._row_to_topic(row) for row in rows]
    
    def _row_to_topic(self, row) -> Topic:
        """Convert database row to Topic object."""
        return Topic(
            id=row["id"],
            title=row["title"],
            description=row["description"],
            niche=row["niche"],
            status=TopicStatus(row["status"]),
            youtube_video_id=row["youtube_video_id"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
            error_message=row["error_message"]
        )
