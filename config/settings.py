"""
Impostazioni globali dell'applicazione DocConverter
"""
import os
from pathlib import Path

class Settings:
    """Gestione centralizzata delle impostazioni"""
    
    # Informazioni applicazione
    APP_NAME = "DocConverter"
    APP_VERSION = "2.5.0"
    APP_AUTHOR = "DocConverter Team"
    
    # Directory base
    BASE_DIR = Path(__file__).resolve().parent.parent
    LOGS_DIR = BASE_DIR / "logs"
    CONFIG_DIR = BASE_DIR / "config"
    
    # Impostazioni logging
    LOG_FILE = LOGS_DIR / "docconverter.log"
    LOG_MAX_SIZE = 10 * 1024 * 1024  # 10 MB
    LOG_BACKUP_COUNT = 5
    LOG_LEVEL = "INFO"
    
    # Impostazioni conversione
    DEFAULT_OUTPUT_DIR = None  # None = stessa directory del file input
    BATCH_MODE = True
    MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB per file
    
    # Impostazioni GUI
    WINDOW_WIDTH = 900
    WINDOW_HEIGHT = 700
    WINDOW_MIN_WIDTH = 700
    WINDOW_MIN_HEIGHT = 500
    
    # Formati supportati
    SUPPORTED_INPUT_FORMATS = {
        'word': ['.doc', '.docx'],
        'pdf': ['.pdf'],
        'image': ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff'],
        'text': ['.txt'],
        'html': ['.html', '.htm']
    }
    
    # Dipendenze sistema
    DEPENDENCIES = {
        'libreoffice': {
            'windows': ['soffice.exe', 'soffice.bin'],
            'linux': ['soffice', 'libreoffice'],
            'required_for': ['word_to_pdf']
        }
    }
    
    @classmethod
    def ensure_directories(cls):
        """Crea le directory necessarie se non esistono"""
        cls.LOGS_DIR.mkdir(parents=True, exist_ok=True)
        cls.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def get_all_supported_extensions(cls):
        """Ritorna lista di tutte le estensioni supportate"""
        extensions = []
        for format_list in cls.SUPPORTED_INPUT_FORMATS.values():
            extensions.extend(format_list)
        return extensions
