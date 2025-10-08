"""
Logging configuration module for Business Analytics
Supports log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
"""

import logging
import os
from datetime import datetime
from typing import Optional, Dict

# Store the configured log level globally
_LOG_LEVEL = None

# Example usage in modules:
# logger.debug("Detailed info for diagnosing problems")      # Level 10 - Most verbose
# logger.info("General informational messages")              # Level 20
# logger.warning("Warning messages")                         # Level 30
# logger.error("Error messages")                             # Level 40
# logger.critical("Critical problems")                       # Level 50 - Least verbose

def setup_logging(log_level: str = 'INFO', config: Optional[Dict] = None) -> str:
    """
    Configure logging for the entire application

    Args:
        log_level: One of 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
        config: Configuration dictionary containing 'project_name'. If provided,
                automatically creates log file at logs/{project_name}_{YYmmdd_HHMMSS}.log

    Returns:
        Path to log file if created, otherwise None

    Example:
        setup_logging('DEBUG', config)  # Creates log file automatically
        setup_logging('INFO')  # Console only
    """
    global _LOG_LEVEL

    # Validate and set log level
    log_level = log_level.upper()
    valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    if log_level not in valid_levels:
        log_level = 'INFO'

    _LOG_LEVEL = getattr(logging, log_level)

    # Clear any existing handlers
    root_logger = logging.getLogger()
    root_logger.handlers.clear()

    # Set root logger level
    root_logger.setLevel(_LOG_LEVEL)

    # Create file formatter
    file_format = logging.Formatter(
        '%(asctime)s - [%(levelname)s] - %(name)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # File handler - automatically create if config is provided
    log_file_path = None
    if config and 'client' in config:
        # Create logs directory if it doesn't exist
        logs_dir = 'logs'
        os.makedirs(logs_dir, exist_ok=True)

        # Generate log filename with timestamp: {client}_{YYmmdd_HHMMSS}.log
        now = datetime.now()
        timestamp = now.strftime('%Y%m%d_%H%M%S')
        client = config['client'].replace(" ", "")
        run_id = f"{client}_{timestamp}"
        log_filename = run_id + f".log"
        log_file_path = os.path.join(logs_dir, log_filename)

        # Create file handler - only log to file, not console
        file_handler = logging.FileHandler(log_file_path, mode='w', encoding='utf-8')
        file_handler.setLevel(_LOG_LEVEL)
        file_handler.setFormatter(file_format)
        root_logger.addHandler(file_handler)

        # Suppress noisy third-party library logs
        logging.getLogger('matplotlib').setLevel(logging.WARNING)
        logging.getLogger('PIL').setLevel(logging.WARNING)
        logging.getLogger('urllib3').setLevel(logging.WARNING)

        # Print confirmation to console
        print(f"📝 Run instance ID: {run_id} - Logging [{log_level}] to: {log_file_path}")

    return log_file_path


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger for a specific module

    Args:
        name: Module name (usually __name__)

    Returns:
        Configured logger instance

    Example:
        logger = get_logger(__name__)
        logger.debug("Debug message")
        logger.info("Info message")
    """
    logger = logging.getLogger(name)

    # If logging hasn't been set up yet, use INFO as default
    if _LOG_LEVEL is None:
        setup_logging('INFO')

    return logger


def get_current_level() -> str:
    """Get the current log level as a string"""
    if _LOG_LEVEL is None:
        return 'INFO'
    return logging.getLevelName(_LOG_LEVEL)
