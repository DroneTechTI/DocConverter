"""
Centralized error handling for DocConverter.

Provides custom exception classes and utilities for consistent error handling
throughout the application.
"""
from typing import Optional, Callable, Dict, Any
from functools import wraps
import traceback
import logging

from .logger import get_logger


class ConversionError(Exception):
    """
    Custom exception for document conversion errors.
    
    Attributes:
        message: Error description
        file_path: Path to file that caused error (if applicable)
        details: Additional error details
        
    Example:
        >>> raise ConversionError(
        ...     "Failed to convert document",
        ...     file_path="document.docx",
        ...     details="Unsupported format"
        ... )
    """
    
    def __init__(
        self,
        message: str,
        file_path: Optional[str] = None,
        details: Optional[str] = None
    ) -> None:
        """Initialize conversion error with context."""
        super().__init__(message)
        self.file_path = file_path
        self.details = details
        self.message = message
    
    def __str__(self) -> str:
        """Return formatted error message."""
        base = f"Conversion error: {self.message}"
        if self.file_path:
            base += f"\nFile: {self.file_path}"
        if self.details:
            base += f"\nDetails: {self.details}"
        return base


class DependencyError(Exception):
    """
    Exception for missing or unavailable dependencies.
    
    Example:
        >>> raise DependencyError("LibreOffice not found")
    """
    pass


class FileAccessError(Exception):
    """
    Exception for file access problems.
    
    Example:
        >>> raise FileAccessError("Permission denied: document.pdf")
    """
    pass


class ErrorHandler:
    """Gestore centralizzato degli errori"""
    
    def __init__(self):
        self.logger = get_logger("ErrorHandler")
        self.error_callbacks = []
    
    def register_callback(self, callback: Callable):
        """
        Registra una callback da chiamare in caso di errore
        
        Args:
            callback: Funzione da chiamare con (error_type, error_message, details)
        """
        self.error_callbacks.append(callback)
    
    def handle_error(self, error: Exception, context: str = None) -> dict:
        """
        Gestisce un errore in modo centralizzato
        
        Args:
            error: L'eccezione da gestire
            context: Contesto in cui è avvenuto l'errore
        
        Returns:
            Dizionario con informazioni sull'errore
        """
        error_info = {
            'type': type(error).__name__,
            'message': str(error),
            'context': context,
            'details': None
        }
        
        # Gestione specifica per tipo di errore
        if isinstance(error, ConversionError):
            error_info['details'] = error.details
            error_info['file_path'] = error.file_path
            self.logger.error(f"Errore conversione: {error}")
        
        elif isinstance(error, DependencyError):
            error_info['user_message'] = (
                "Dipendenza mancante. "
                "Assicurati che tutti i software necessari siano installati."
            )
            self.logger.error(f"Dipendenza mancante: {error}")
        
        elif isinstance(error, FileAccessError):
            error_info['user_message'] = (
                "Impossibile accedere al file. "
                "Verifica i permessi e che il file non sia in uso."
            )
            self.logger.error(f"Errore accesso file: {error}")
        
        elif isinstance(error, PermissionError):
            error_info['user_message'] = (
                "Permessi insufficienti. "
                "Verifica di avere i diritti necessari per accedere al file."
            )
            self.logger.error(f"Errore permessi: {error}")
        
        elif isinstance(error, FileNotFoundError):
            error_info['user_message'] = "File non trovato."
            self.logger.error(f"File non trovato: {error}")
        
        else:
            error_info['user_message'] = f"Errore imprevisto: {str(error)}"
            error_info['details'] = traceback.format_exc()
            self.logger.error(f"Errore imprevisto: {error}", exc_info=True)
        
        # Notifica le callback registrate
        for callback in self.error_callbacks:
            try:
                callback(
                    error_info['type'],
                    error_info.get('user_message', error_info['message']),
                    error_info.get('details')
                )
            except Exception as cb_error:
                self.logger.error(f"Errore in callback: {cb_error}")
        
        return error_info
    
    def get_user_friendly_message(self, error: Exception) -> str:
        """
        Converte un'eccezione in un messaggio comprensibile all'utente
        
        Args:
            error: L'eccezione da convertire
        
        Returns:
            Messaggio user-friendly
        """
        if isinstance(error, ConversionError):
            return f"Conversione fallita: {error.message}"
        elif isinstance(error, DependencyError):
            return f"Software richiesto non trovato: {str(error)}"
        elif isinstance(error, FileAccessError):
            return f"Impossibile accedere al file: {str(error)}"
        elif isinstance(error, PermissionError):
            return "Permessi insufficienti per accedere al file"
        elif isinstance(error, FileNotFoundError):
            return "File non trovato"
        else:
            return f"Errore: {str(error)}"


def handle_exceptions(error_handler: ErrorHandler = None, context: str = None):
    """
    Decorator per gestire automaticamente le eccezioni
    
    Args:
        error_handler: Istanza di ErrorHandler da usare
        context: Contesto dell'operazione
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                handler = error_handler or ErrorHandler()
                handler.handle_error(e, context or func.__name__)
                raise
        return wrapper
    return decorator
