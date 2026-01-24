"""
Abstract base class for all document converters.

This module provides the foundation for implementing document conversion plugins
following a consistent interface and contract.
"""
from abc import ABC, abstractmethod
from typing import Callable, Optional, Dict, List, Any
from pathlib import Path
import logging

from utils.logger import get_logger
from utils.error_handler import ConversionError


class ConverterBase(ABC):
    """
    Abstract base class for implementing document converters.
    
    Each converter must inherit from this class and implement the abstract
    methods get_info() and convert(). This ensures a consistent interface
    across all converter implementations.
    
    Attributes:
        logger: Logger instance for this converter
        
    Example:
        >>> class MyConverter(ConverterBase):
        ...     def get_info(self) -> Dict[str, Any]:
        ...         return {
        ...             'name': 'My Converter',
        ...             'input_formats': ['.txt'],
        ...             'output_format': '.pdf',
        ...             'description': 'Converts text to PDF'
        ...         }
        ...     
        ...     def convert(self, input_path: str, output_path: str, 
        ...                progress_callback=None, **kwargs) -> bool:
        ...         # Implementation here
        ...         return True
    """
    
    def __init__(self) -> None:
        """Initialize the converter with logging capabilities."""
        self.logger: logging.Logger = get_logger(self.__class__.__name__)
        self._info: Optional[Dict[str, Any]] = None
    
    @abstractmethod
    def get_info(self) -> Dict[str, Any]:
        """
        Return metadata information about this converter.
        
        Returns:
            Dictionary containing:
                - name (str): Human-readable converter name
                - input_formats (List[str]): Supported input file extensions
                  (e.g., ['.doc', '.docx'])
                - output_format (str): Output file extension (e.g., '.pdf')
                - description (str): Brief converter description
                - requires_dependency (Optional[str]): External dependency name
                  if required (e.g., 'libreoffice')
        
        Example:
            >>> converter.get_info()
            {
                'name': 'Word to PDF',
                'input_formats': ['.doc', '.docx'],
                'output_format': '.pdf',
                'description': 'Converts Word documents to PDF format',
                'requires_dependency': None
            }
        """
        pass
    
    @abstractmethod
    def convert(
        self,
        input_path: str,
        output_path: str,
        progress_callback: Optional[Callable[[int, str], None]] = None,
        **kwargs: Any
    ) -> bool:
        """
        Execute document conversion.
        
        Args:
            input_path: Full path to input file
            output_path: Full path to output file
            progress_callback: Optional callback for progress updates.
                             Signature: callback(percentage: int, message: str)
            **kwargs: Additional converter-specific parameters
        
        Returns:
            True if conversion succeeded, False otherwise
        
        Raises:
            ConversionError: If conversion fails with details about the error
            
        Example:
            >>> converter.convert('input.docx', 'output.pdf',
            ...                   progress_callback=lambda p, m: print(f'{p}%: {m}'))
            True
        """
        pass
    
    def validate_input(self, input_path: str) -> bool:
        """
        Validate input file for this converter.
        
        Checks file existence and whether the file extension is supported
        by this converter.
        
        Args:
            input_path: Path to file to validate
        
        Returns:
            True if file is valid for this converter, False otherwise
            
        Example:
            >>> converter.validate_input('document.docx')
            True
            >>> converter.validate_input('nonexistent.docx')
            False
        """
        path = Path(input_path)
        
        # Check file existence
        if not path.exists():
            self.logger.error(f"File not found: {input_path}")
            return False
        
        # Check supported extension
        extension = path.suffix.lower()
        info = self.get_info()
        
        if extension not in info['input_formats']:
            self.logger.error(
                f"Format {extension} not supported by {info['name']}. "
                f"Supported formats: {', '.join(info['input_formats'])}"
            )
            return False
        
        return True
    
    def _report_progress(
        self,
        callback: Optional[Callable[[int, str], None]],
        percentage: int,
        message: str = ""
    ) -> None:
        """
        Send progress update to callback if provided.
        
        Args:
            callback: Progress callback function
            percentage: Completion percentage (0-100)
            message: Optional status message
        """
        if callback:
            try:
                callback(percentage, message)
            except Exception as e:
                self.logger.error(f"Error in progress callback: {e}")
    
    def get_supported_extensions(self) -> List[str]:
        """
        Get list of supported input file extensions.
        
        Returns:
            List of file extensions (e.g., ['.doc', '.docx'])
        """
        return self.get_info()['input_formats']
    
    def get_output_extension(self) -> str:
        """
        Get output file extension.
        
        Returns:
            Output file extension (e.g., '.pdf')
        """
        return self.get_info()['output_format']
    
    def get_name(self) -> str:
        """
        Get converter name.
        
        Returns:
            Human-readable converter name
        """
        return self.get_info()['name']
    
    def requires_dependency(self) -> Optional[str]:
        """
        Check if converter requires external dependency.
        
        Returns:
            Dependency name if required, None otherwise
        """
        info = self.get_info()
        return info.get('requires_dependency')
    
    def __str__(self) -> str:
        """Return string representation of converter."""
        info = self.get_info()
        return (
            f"{info['name']}: "
            f"{', '.join(info['input_formats'])} → {info['output_format']}"
        )
    
    def __repr__(self) -> str:
        """Return technical representation of converter."""
        return f"<{self.__class__.__name__}: {self.get_name()}>"
