"""Logging utilities for YT-DeepReSearch."""

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any, Dict, MutableMapping, Optional, Tuple


class ContextLoggerAdapter(logging.LoggerAdapter):
    """Logger adapter that adds contextual information to log records.
    
    Allows tagging logs with topic_id and phase for better traceability.
    """

    def __init__(self, logger: logging.Logger, extra: Optional[Dict[str, Any]] = None):
        """Initialize the adapter with a logger and optional context.
        
        Args:
            logger: Base logger instance
            extra: Optional context dictionary (topic_id, phase, etc.)
        """
        super().__init__(logger, extra or {})

    def process(
        self, msg: str, kwargs: MutableMapping[str, Any]
    ) -> Tuple[str, MutableMapping[str, Any]]:
        """Process the log message to add context.
        
        Args:
            msg: Log message
            kwargs: Additional keyword arguments
            
        Returns:
            Tuple of processed message and kwargs
        """
        # Build context prefix from extra fields
        context_parts = []
        if "topic_id" in self.extra:
            context_parts.append(f"topic_id={self.extra['topic_id']}")
        if "phase" in self.extra:
            context_parts.append(f"phase={self.extra['phase']}")
        
        if context_parts:
            context_prefix = f"[{', '.join(context_parts)}] "
            msg = context_prefix + msg
        
        return msg, kwargs

    def with_context(self, **context: Any) -> "ContextLoggerAdapter":
        """Create a new adapter with additional context.
        
        Args:
            **context: Additional context fields to add
            
        Returns:
            New ContextLoggerAdapter with merged context
        """
        new_extra = {**self.extra, **context}
        return ContextLoggerAdapter(self.logger, new_extra)


def setup_logger(
    name: str = "yt_deepresearch",
    log_level: str = "INFO",
    log_dir: Optional[Path] = None,
    console_output: bool = True
) -> logging.Logger:
    """Setup and configure the application logger.
    
    Args:
        name: Logger name
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: Optional directory for log files
        console_output: Whether to output logs to console
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Console handler
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, log_level.upper()))
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # File handler (rotating)
    if log_dir:
        log_dir = Path(log_dir)
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "yt_deepresearch.log"
        
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5
        )
        file_handler.setLevel(getattr(logging, log_level.upper()))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(
    topic_id: Optional[int] = None,
    phase: Optional[str] = None,
    base_logger_name: str = "yt_deepresearch"
) -> ContextLoggerAdapter:
    """Get a context-aware logger adapter.
    
    Args:
        topic_id: Optional topic ID for context
        phase: Optional phase name for context
        base_logger_name: Base logger name to use
        
    Returns:
        ContextLoggerAdapter with specified context
    """
    base_logger = logging.getLogger(base_logger_name)
    context = {}
    if topic_id is not None:
        context["topic_id"] = topic_id
    if phase is not None:
        context["phase"] = phase
    
    return ContextLoggerAdapter(base_logger, context)
