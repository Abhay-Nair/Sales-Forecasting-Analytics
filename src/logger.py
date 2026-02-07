"""
Centralized logging configuration for the sales forecasting project.
"""
import logging
import sys
from pathlib import Path
from config import LOG_FILE, LOG_LEVEL, LOG_FORMAT

def setup_logger(name: str, log_to_file: bool = True) -> logging.Logger:
    """
    Set up a logger with console and optional file output.
    
    Args:
        name: Name of the logger (usually __name__)
        log_to_file: Whether to also log to file
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    logger.setLevel(getattr(logging, LOG_LEVEL))
    
    # Console handler with UTF-8 encoding
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(message)s')
    console_handler.setFormatter(console_formatter)
    
    # Fix Windows encoding issue (only if not in test mode)
    if sys.platform == 'win32' and not hasattr(sys.stdout, '_pytest_capture'):
        try:
            import io
            if hasattr(sys.stdout, 'buffer'):
                sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        except (AttributeError, ValueError):
            # If stdout is already wrapped or doesn't have buffer, skip
            pass
    
    logger.addHandler(console_handler)
    
    # File handler with UTF-8 encoding
    if log_to_file:
        file_handler = logging.FileHandler(LOG_FILE, mode='a', encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(LOG_FORMAT)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger

def log_section(logger: logging.Logger, title: str, width: int = 50):
    """Log a section header."""
    logger.info("=" * width)
    logger.info(title.center(width))
    logger.info("=" * width)

def log_success(logger: logging.Logger, message: str):
    """Log a success message with checkmark."""
    logger.info(f"✓ {message}")

def log_error(logger: logging.Logger, message: str):
    """Log an error message with X mark."""
    logger.error(f"✗ {message}")

def log_warning(logger: logging.Logger, message: str):
    """Log a warning message."""
    logger.warning(f"⚠ {message}")
