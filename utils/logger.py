"""
Sistema di logging centralizzato per DocConverter
"""
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from datetime import datetime

try:
    import colorlog
    COLORLOG_AVAILABLE = True
except ImportError:
    COLORLOG_AVAILABLE = False

from config.settings import Settings


def setup_logger(name: str = None, log_file: Path = None, level: str = None):
    """
    Configura e ritorna un logger con output su console e file
    
    Args:
        name: Nome del logger (default: root logger)
        log_file: Path del file di log (default: Settings.LOG_FILE)
        level: Livello di logging (default: Settings.LOG_LEVEL)
    
    Returns:
        Logger configurato
    """
    # Assicura che la directory dei log esista
    Settings.ensure_directories()
    
    logger_name = name or Settings.APP_NAME
    logger = logging.getLogger(logger_name)
    
    # Se il logger è già configurato, ritornalo
    if logger.handlers:
        return logger
    
    log_level = getattr(logging, (level or Settings.LOG_LEVEL).upper())
    logger.setLevel(log_level)
    
    # Formato log
    file_format = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler per file con rotazione
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
    
    # Handler per console con colori (se disponibile)
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
    
    # Evita propagazione al root logger
    logger.propagate = False
    
    logger.info(f"{Settings.APP_NAME} v{Settings.APP_VERSION} - Logger inizializzato")
    
    return logger


def get_logger(name: str = None):
    """
    Ottiene un logger esistente o ne crea uno nuovo
    
    Args:
        name: Nome del logger
    
    Returns:
        Logger configurato
    """
    logger_name = name or Settings.APP_NAME
    logger = logging.getLogger(logger_name)
    
    # Se non ha handler, configuralo
    if not logger.handlers:
        return setup_logger(logger_name)
    
    return logger


class LoggerMixin:
    """Mixin per aggiungere logging alle classi"""
    
    @property
    def logger(self):
        """Ritorna il logger per questa classe"""
        if not hasattr(self, '_logger'):
            self._logger = get_logger(self.__class__.__name__)
        return self._logger
