"""
PDF to Word Converter.

Converts PDF documents to editable Word (.docx) format using pdf2docx library.
"""
from pathlib import Path
from typing import Optional, Callable

from core.converter_base import ConverterBase
from utils.error_handler import ConversionError


class PDFToWordConverter(ConverterBase):
    """
    PDF to Word (.docx) converter.
    
    Uses pdf2docx library to extract text and formatting from PDF documents.
    """
    
    def __init__(self) -> None:
        """Initialize PDF to Word converter."""
        super().__init__()
    
    def get_info(self) -> dict:
        """Return converter metadata."""
        return {
            'name': 'PDF to Word',
            'input_formats': ['.pdf'],
            'output_format': '.docx',
            'description': 'Converts PDF documents to editable Word format',
            'requires_dependency': None
        }
    
    def convert(
        self,
        input_path: str,
        output_path: str,
        progress_callback: Optional[Callable[[int, str], None]] = None,
        **kwargs
    ) -> bool:
        """
        Convert PDF document to Word format.
        
        Args:
            input_path: Path to PDF file to convert
            output_path: Path for output Word file
            progress_callback: Optional callback for progress updates
            **kwargs: Additional parameters
        
        Returns:
            True if conversion succeeded
        
        Raises:
            ConversionError: If conversion fails
        """
        self.logger.info(f"Starting PDF→Word conversion: {input_path}")
        
        try:
            # Validate input
            self._report_progress(progress_callback, 5, "Validating file...")
            if not self.validate_input(input_path):
                raise ConversionError(
                    "Invalid input file",
                    file_path=input_path
                )
            
            # Import library
            self._report_progress(progress_callback, 10, "Loading libraries...")
            try:
                from pdf2docx import Converter
            except ImportError:
                raise ConversionError(
                    "pdf2docx library not installed",
                    details="Install with: pip install pdf2docx"
                )
            
            # Prepare paths
            input_file = Path(input_path).resolve()
            output_file = Path(output_path).resolve()
            output_dir = output_file.parent
            
            # Ensure output directory exists
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Convert
            self._report_progress(progress_callback, 30, "Converting...")
            
            cv = Converter(str(input_file))
            cv.convert(str(output_file), start=0, end=None)
            cv.close()
            
            self._report_progress(progress_callback, 90, "Finalizing...")
            
            # Verify output
            if not output_file.exists() or output_file.stat().st_size == 0:
                raise ConversionError(
                    "Word file not generated",
                    file_path=input_path
                )
            
            self._report_progress(progress_callback, 100, "Completed!")
            self.logger.info(f"Conversion completed: {output_file}")
            
            return True
        
        except ConversionError:
            raise
        
        except Exception as e:
            self.logger.error(f"PDF→Word conversion error: {e}", exc_info=True)
            raise ConversionError(
                f"Conversion error: {str(e)}",
                file_path=input_path,
                details=str(e)
            )
