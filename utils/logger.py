"""
Centralized logging system for DocConverter.

Provides unified logging configuration with file rotation, colored console output,
and easy-to-use logger factory functions.
"""
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional

try:
    import colorlog
    COLORLOG_AVAILABLE = True
except ImportError:
    COLORLOG_AVAILABLE = False

from config.settings import Settings


def setup_logger(
    name: Optional[str] = None,
    log_file: Optional[Path] = None,
    level: Optional[str] = None
) -> logging.Logger:
    """
    Configure and return a logger with console and file output.
    
    Sets up a logger with rotating file handler and colored console output
    (if colorlog is available). Safe to call multiple times - returns existing
    logger if already configured.
    
    Args:
        name: Logger name (default: app name from Settings)
        log_file: Log file path (default: Settings.LOG_FILE)
        level: Logging level (default: Settings.LOG_LEVEL)
    
    Returns:
        Configured logger instance
        
    Example:
        >>> logger = setup_logger('MyModule', level='DEBUG')
        >>> logger.info('Application started')
    """
    # Ensure log directory exists
    Settings.ensure_directories()
    
    logger_name = name or Settings.APP_NAME
    logger = logging.getLogger(logger_name)
    
    # If logger already configured, return it
    if logger.handlers:
        return logger
    
    log_level = getattr(logging, (level or Settings.LOG_LEVEL).upper())
    logger.setLevel(log_level)
    
    # File log format
    file_format = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Rotating file handler
    log_file_path = log_file or Settings.LOG_FILE
    file_handler = RotatingFileHandler(
        log_file_path,
        maxBytes=Settings.LOG_MAX_SIZE,
        backupCount=Settings.LOG_BACKUP_COUNT,
        encoding='utf-8'
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)
    
    # Console handler with colors (if available)
    if COLORLOG_AVAILABLE:
        console_format = colorlog.ColoredFormatter(
            fmt='%(log_color)s%(levelname)-8s%(reset)s %(message)s',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
    else:
        console_format = logging.Formatter('%(levelname)-8s %(message)s')
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    logger.info(f"{Settings.APP_NAME} v{Settings.APP_VERSION} - Logger initialized")
    
    return logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get existing logger or create a new one.
    
    Args:
        name: Logger name (default: app name from Settings)
    
    Returns:
        Configured logger instance
        
    Example:
        >>> logger = get_logger('MyModule')
        >>> logger.debug('Debug message')
    """
    logger_name = name or Settings.APP_NAME
    logger = logging.getLogger(logger_name)
    
    # If no handlers, configure it
    if not logger.handlers:
        return setup_logger(logger_name)
    
    return logger


class LoggerMixin:
    """
    Mixin class to add logging capabilities to any class.
    
    Provides a lazy-initialized logger property that uses the class name
    as the logger name.
    
    Example:
        >>> class MyClass(LoggerMixin):
        ...     def process(self):
        ...         self.logger.info('Processing started')
    """
    
    @property
    def logger(self) -> logging.Logger:
        """
        Get logger for this class.
        
        Returns:
            Logger instance with class name
        """
        if not hasattr(self, '_logger'):
            self._logger = get_logger(self.__class__.__name__)
        return self._logger
