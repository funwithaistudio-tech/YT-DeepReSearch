"""Cleanup and archival manager."""

import shutil
from pathlib import Path
from datetime import datetime
from typing import List

from src.config.settings import Settings
from src.utils.logger import get_logger

logger = get_logger()


class CleanupManager:
    """Manages cleanup and archival of artifacts."""
    
    def __init__(self, settings: Settings):
        """Initialize cleanup manager.
        
        Args:
            settings: Application settings
        """
        self.settings = settings
        self.output_dir = Path(settings.output_dir)
        self.archive_dir = self.output_dir / "archive"
        self.archive_dir.mkdir(parents=True, exist_ok=True)
    
    def cleanup_for_topic(self, topic_id: int, success: bool = True):
        """Cleanup artifacts for a topic.
        
        Args:
            topic_id: Topic ID
            success: Whether processing was successful
        """
        logger.info(f"Starting cleanup for topic {topic_id} (success={success})")
        
        # Archive artifacts if configured
        if self.settings.archive_artifacts:
            self._archive_topic_artifacts(topic_id)
        
        # Delete heavy temp files if configured and successful
        if success and self.settings.cleanup_on_success:
            self._delete_temp_files(topic_id)
        
        logger.info(f"Cleanup complete for topic {topic_id}")
    
    def _archive_topic_artifacts(self, topic_id: int):
        """Archive important artifacts for a topic.
        
        Args:
            topic_id: Topic ID
        """
        logger.info(f"Archiving artifacts for topic {topic_id}")
        
        # Create topic archive directory
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        topic_archive = self.archive_dir / f"topic_{topic_id}_{timestamp}"
        topic_archive.mkdir(parents=True, exist_ok=True)
        
        # Files to archive
        files_to_archive = self._get_topic_files(topic_id)
        
        archived_count = 0
        for file_path in files_to_archive:
            if file_path.exists():
                try:
                    dest = topic_archive / file_path.name
                    shutil.copy2(file_path, dest)
                    archived_count += 1
                    logger.debug(f"Archived: {file_path.name}")
                except Exception as e:
                    logger.warning(f"Failed to archive {file_path}: {e}")
        
        logger.info(f"Archived {archived_count} files to {topic_archive}")
    
    def _delete_temp_files(self, topic_id: int):
        """Delete heavy temporary files for a topic.
        
        Args:
            topic_id: Topic ID
        """
        logger.info(f"Deleting temp files for topic {topic_id}")
        
        deleted_count = 0
        deleted_size = 0
        
        # Delete audio files
        audio_dir = Path(self.settings.assets_dir) / "audio"
        if audio_dir.exists():
            for audio_file in audio_dir.glob(f"topic_{topic_id}_*.mp3"):
                size = audio_file.stat().st_size
                audio_file.unlink()
                deleted_count += 1
                deleted_size += size
                logger.debug(f"Deleted audio: {audio_file.name}")
        
        # Delete image files
        image_dir = Path(self.settings.assets_dir) / "images"
        if image_dir.exists():
            for image_file in image_dir.glob(f"topic_{topic_id}_*.png"):
                size = image_file.stat().st_size
                image_file.unlink()
                deleted_count += 1
                deleted_size += size
                logger.debug(f"Deleted image: {image_file.name}")
        
        # Delete video file (keep if you want to retain)
        # video_file = self.output_dir / f"main_video_topic_{topic_id}.mp4"
        # if video_file.exists():
        #     size = video_file.stat().st_size
        #     video_file.unlink()
        #     deleted_count += 1
        #     deleted_size += size
        
        deleted_mb = deleted_size / (1024 * 1024)
        logger.info(f"Deleted {deleted_count} temp files ({deleted_mb:.2f} MB)")
    
    def _get_topic_files(self, topic_id: int) -> List[Path]:
        """Get list of files to archive for a topic.
        
        Args:
            topic_id: Topic ID
            
        Returns:
            List of file paths
        """
        files = []
        
        # Question framework
        files.append(self.output_dir / f"questions_topic_{topic_id}.json")
        
        # Research files
        files.extend(self.output_dir.glob(f"research_*_topic_{topic_id}.json"))
        
        # Script files
        files.append(self.output_dir / f"script_topic_{topic_id}.json")
        files.append(self.output_dir / f"script_topic_{topic_id}_with_assets.json")
        
        # Video file
        files.append(self.output_dir / f"main_video_topic_{topic_id}.mp4")
        
        # Logs (if stored per topic)
        logs_dir = Path(self.settings.logs_dir)
        if logs_dir.exists():
            files.extend(logs_dir.glob(f"*topic_{topic_id}*.log"))
        
        # Filter to only existing files
        return [f for f in files if f.exists()]
    
    def cleanup_old_archives(self, days: int = 90):
        """Delete archives older than specified days.
        
        Args:
            days: Number of days to retain archives
        """
        logger.info(f"Cleaning up archives older than {days} days")
        
        cutoff = datetime.utcnow().timestamp() - (days * 86400)
        deleted_count = 0
        
        for archive_dir in self.archive_dir.iterdir():
            if archive_dir.is_dir():
                mtime = archive_dir.stat().st_mtime
                if mtime < cutoff:
                    shutil.rmtree(archive_dir)
                    deleted_count += 1
                    logger.debug(f"Deleted old archive: {archive_dir.name}")
        
        logger.info(f"Deleted {deleted_count} old archives")
