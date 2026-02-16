"""
Logging configuration for the application.
"""
import logging
import sys
from app.config import config


def setup_logger(name: str = "agri-genius") -> logging.Logger:
    """
    Setup and configure application logger.
    
    Args:
        name: Logger name
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Set level from config
    level_map = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL
    }
    logger.setLevel(level_map.get(config.LOG_LEVEL.lower(), logging.INFO))
    
    # Console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logger.level)
    
    # Format
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    
    # Add handler if not already added
    if not logger.handlers:
        logger.addHandler(handler)
    
    return logger


# Global logger instance
logger = setup_logger()
