"""
Converter Registry - Central registry for managing all available converters.

This module provides a singleton registry that handles converter registration,
discovery, and selection based on file types and output formats.
"""
from typing import Dict, List, Optional, Type, Any
from pathlib import Path
import logging

from .converter_base import ConverterBase
from utils.logger import get_logger


class ConverterRegistry:
    """
    Centralized registry for all available document converters.
    
    Manages automatic registration, retrieval, and selection of the appropriate
    converter for a given conversion operation. Implements a plugin-like
    architecture for easy extensibility.
    
    Attributes:
        logger: Logger instance for registry operations
        
    Example:
        >>> registry = ConverterRegistry()
        >>> registry.register(WordToPDFConverter)
        >>> converter = registry.get_converter_for_file('document.docx')
        >>> converter.convert('document.docx', 'output.pdf')
    """
    
    def __init__(self) -> None:
        """Initialize the converter registry with empty mappings."""
        self.logger: logging.Logger = get_logger("ConverterRegistry")
        self._converters: Dict[str, ConverterBase] = {}
        self._extension_map: Dict[str, List[str]] = {}
    
    def register(self, converter_class: Type[ConverterBase]) -> None:
        """
        Register a new converter class.
        
        Instantiates the converter and adds it to the registry, mapping
        all supported input formats to this converter.
        
        Args:
            converter_class: Converter class to register (not an instance)
        
        Example:
            >>> registry.register(WordToPDFConverter)
            >>> registry.register(PDFToWordConverter)
        """
        try:
            # Instantiate converter
            converter = converter_class()
            
            # Get converter metadata
            info = converter.get_info()
            name = info['name']
            
            # Register converter
            self._converters[name] = converter
            
            # Map input extensions to converter
            for ext in info['input_formats']:
                if ext not in self._extension_map:
                    self._extension_map[ext] = []
                self._extension_map[ext].append(name)
            
            self.logger.info(f"Converter registered: {name}")
            self.logger.debug(f"  Input: {', '.join(info['input_formats'])}")
            self.logger.debug(f"  Output: {info['output_format']}")
            
        except Exception as e:
            self.logger.error(f"Error registering converter {converter_class}: {e}")
    
    def get_converter(self, name: str) -> Optional[ConverterBase]:
        """
        Retrieve a converter by name.
        
        Args:
            name: Converter name (e.g., 'Word to PDF')
        
        Returns:
            Converter instance if found, None otherwise
            
        Example:
            >>> converter = registry.get_converter('Word to PDF')
        """
        return self._converters.get(name)
    
    def get_converter_for_file(
        self,
        file_path: str,
        output_format: str = '.pdf'
    ) -> Optional[ConverterBase]:
        """
        Find appropriate converter for a file.
        
        Selects converter based on input file extension and desired output format.
        If multiple converters support the input format, prefers the one with
        matching output format.
        
        Args:
            file_path: Path to file to convert
            output_format: Desired output format (default: '.pdf')
        
        Returns:
            Appropriate converter instance or None if no converter found
            
        Example:
            >>> converter = registry.get_converter_for_file('doc.docx', '.pdf')
        """
        extension = Path(file_path).suffix.lower()
        
        # Find converters supporting this extension
        converter_names = self._extension_map.get(extension, [])
        
        if not converter_names:
            self.logger.warning(f"No converter for extension {extension}")
            return None
        
        # Find converter with matching output format
        for name in converter_names:
            converter = self._converters[name]
            if converter.get_output_extension() == output_format:
                return converter
        
        # If no exact match, return first available
        self.logger.warning(
            f"Output format {output_format} not available for {extension}, "
            f"using {self._converters[converter_names[0]].get_output_extension()}"
        )
        return self._converters[converter_names[0]]
    
    def get_all_converters(self) -> List[ConverterBase]:
        """
        Get all registered converters.
        
        Returns:
            List of all converter instances
        """
        return list(self._converters.values())
    
    def get_supported_input_formats(self) -> List[str]:
        """
        Get all supported input file extensions.
        
        Returns:
            List of supported extensions (e.g., ['.docx', '.pdf', '.png'])
        """
        return list(self._extension_map.keys())
    
    def get_converters_info(self) -> List[Dict[str, Any]]:
        """
        Get metadata for all registered converters.
        
        Returns:
            List of converter info dictionaries
        """
        return [conv.get_info() for conv in self._converters.values()]
    
    def is_format_supported(self, extension: str) -> bool:
        """
        Check if a file format is supported.
        
        Args:
            extension: File extension to check (e.g., '.docx')
        
        Returns:
            True if format is supported by at least one converter
            
        Example:
            >>> registry.is_format_supported('.docx')
            True
            >>> registry.is_format_supported('.xyz')
            False
        """
        return extension.lower() in self._extension_map
    
    def clear(self) -> None:
        """Clear all registered converters."""
        self._converters.clear()
        self._extension_map.clear()
        self.logger.info("Registry cleared")
    
    def __len__(self) -> int:
        """Return number of registered converters."""
        return len(self._converters)
    
    def __str__(self) -> str:
        """Return string representation of registry."""
        return (
            f"ConverterRegistry: {len(self._converters)} converters, "
            f"{len(self._extension_map)} formats supported"
        )


# Global registry instance
_global_registry: Optional[ConverterRegistry] = None


def get_registry() -> ConverterRegistry:
    """
    Get the global registry instance (singleton pattern).
    
    Returns:
        Singleton instance of ConverterRegistry
        
    Example:
        >>> registry = get_registry()
        >>> registry.register(MyConverter)
    """
    global _global_registry
    if _global_registry is None:
        _global_registry = ConverterRegistry()
    return _global_registry
