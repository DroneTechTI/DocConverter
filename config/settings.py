"""
Global application settings for DocConverter.

Centralized configuration management for the application including paths,
logging settings, GUI parameters, and supported formats.
"""
from pathlib import Path
from typing import Dict, List, Any


class Settings:
    """
    Centralized application settings management.
    
    All configuration constants are defined as class attributes for easy access
    throughout the application. Use class methods for dynamic operations.
    
    Example:
        >>> Settings.ensure_directories()
        >>> print(Settings.APP_VERSION)
        '2.5.0'
        >>> extensions = Settings.get_all_supported_extensions()
    """
    
    # Application metadata
    APP_NAME = "DocConverter"
    APP_VERSION = "2.5.0"
    APP_AUTHOR = "DocConverter Team"
    
    # Base directories
    BASE_DIR = Path(__file__).resolve().parent.parent
    LOGS_DIR = BASE_DIR / "logs"
    CONFIG_DIR = BASE_DIR / "config"
    
    # Logging configuration
    LOG_FILE = LOGS_DIR / "docconverter.log"
    LOG_MAX_SIZE = 10 * 1024 * 1024  # 10 MB
    LOG_BACKUP_COUNT = 5
    LOG_LEVEL = "INFO"
    
    # Conversion settings
    DEFAULT_OUTPUT_DIR = None  # None = same directory as input file
    BATCH_MODE = True
    MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB per file
    
    # GUI settings
    WINDOW_WIDTH = 900
    WINDOW_HEIGHT = 700
    WINDOW_MIN_WIDTH = 700
    WINDOW_MIN_HEIGHT = 500
    
    # Supported input formats by category
    SUPPORTED_INPUT_FORMATS: Dict[str, List[str]] = {
        'word': ['.doc', '.docx'],
        'pdf': ['.pdf'],
        'image': ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff'],
        'text': ['.txt'],
        'html': ['.html', '.htm']
    }
    
    # System dependencies configuration
    DEPENDENCIES: Dict[str, Dict[str, Any]] = {
        'libreoffice': {
            'windows': ['soffice.exe', 'soffice.bin'],
            'linux': ['soffice', 'libreoffice'],
            'required_for': ['word_to_pdf']
        }
    }
    
    @classmethod
    def ensure_directories(cls) -> None:
        """
        Create required directories if they don't exist.
        
        Creates logs and config directories with all parent directories
        as needed. Safe to call multiple times.
        """
        cls.LOGS_DIR.mkdir(parents=True, exist_ok=True)
        cls.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def get_all_supported_extensions(cls) -> List[str]:
        """
        Get list of all supported file extensions.
        
        Returns:
            List of all supported extensions across all format categories
            
        Example:
            >>> Settings.get_all_supported_extensions()
            ['.doc', '.docx', '.pdf', '.png', '.jpg', ...]
        """
        extensions = []
        for format_list in cls.SUPPORTED_INPUT_FORMATS.values():
            extensions.extend(format_list)
        return extensions
