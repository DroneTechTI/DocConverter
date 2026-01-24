"""
HTML to PDF Converter.

Converts HTML pages to PDF format using weasyprint or pdfkit.
"""
from pathlib import Path
from typing import Optional, Callable, Any

from core.converter_base import ConverterBase
from utils.error_handler import ConversionError


class HTMLToPDFConverter(ConverterBase):
    """
    HTML to PDF converter.
    
    Uses pdfkit/wkhtmltopdf for HTML→PDF rendering.
    """
    
    def __init__(self) -> None:
        """Initialize HTML to PDF converter."""
        super().__init__()
    
    def get_info(self) -> dict:
        """Return converter metadata."""
        return {
            'name': 'HTML to PDF',
            'input_formats': ['.html', '.htm'],
            'output_format': '.pdf',
            'description': 'Converts HTML pages to PDF format',
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
        Convert HTML file to PDF.
        
        Args:
            input_path: Path to HTML file to convert
            output_path: Path for output PDF file
            progress_callback: Optional callback for progress updates
            **kwargs: Additional parameters
        
        Returns:
            True if conversion succeeded
        
        Raises:
            ConversionError: If conversion fails
        """
        self.logger.info(f"Starting HTML→PDF conversion: {input_path}")
        
        try:
            # Validate input
            self._report_progress(progress_callback, 5, "Validating file...")
            if not self.validate_input(input_path):
                raise ConversionError(
                    "Invalid input file",
                    file_path=input_path
                )
            
            # Import libraries (try different methods)
            self._report_progress(progress_callback, 10, "Loading libraries...")
            
            # Method 1: weasyprint (pure Python, no external dependencies)
            try:
                from weasyprint import HTML
                method = 'weasyprint'
                self.logger.info("Using weasyprint for conversion")
            except ImportError:
                # Method 2: pdfkit (requires wkhtmltopdf)
                try:
                    import pdfkit
                    method = 'pdfkit'
                    self.logger.info("Using pdfkit for conversion")
                except ImportError:
                    raise ConversionError(
                        "No HTML→PDF library available",
                        details=(
                            "Install one of these libraries:\n"
                            "  pip install weasyprint (recommended)\n"
                            "  pip install pdfkit (requires wkhtmltopdf)"
                        )
                    )
            
            # Prepare paths
            input_file = Path(input_path).resolve()
            output_file = Path(output_path).resolve()
            output_dir = output_file.parent
            
            # Ensure output directory exists
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Convert
            self._report_progress(progress_callback, 30, "Converting...")
            
            if method == 'weasyprint':
                HTML(filename=str(input_file)).write_pdf(str(output_file))
            else:  # pdfkit
                import pdfkit
                pdfkit.from_file(str(input_file), str(output_file))
            
            # Verify output
            if not output_file.exists() or output_file.stat().st_size == 0:
                raise ConversionError(
                    "PDF file not generated",
                    file_path=input_path
                )
            
            self._report_progress(progress_callback, 100, "Completed!")
            self.logger.info(f"Conversion completed: {output_file}")
            
            return True
        
        except ConversionError:
            raise
        
        except Exception as e:
            self.logger.error(f"HTML→PDF conversion error: {e}", exc_info=True)
            raise ConversionError(
                f"Conversion error: {str(e)}",
                file_path=input_path,
                details=str(e)
            )
