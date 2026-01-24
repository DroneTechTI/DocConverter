"""
PDF to Images Converter.

Converts PDF pages to image files (PNG/JPEG).
"""
from pathlib import Path
from typing import Optional, Callable, Any

from core.converter_base import ConverterBase
from utils.error_handler import ConversionError


class PDFToImagesConverter(ConverterBase):
    """
    PDF to images converter (PNG/JPEG).
    
    Converts each PDF page to a separate image file.
    """
    
    def __init__(self) -> None:
        """Initialize PDF to Images converter."""
        super().__init__()
    
    def get_info(self) -> dict:
        """Return converter metadata."""
        return {
            'name': 'PDF to Images',
            'input_formats': ['.pdf'],
            'output_format': '.png',
            'description': 'Converts PDF pages to images (PNG/JPEG)',
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
        Convert PDF to images.
        
        Args:
            input_path: Path to PDF file to convert
            output_path: Base path for images (e.g., output.png → output_1.png, output_2.png...)
            progress_callback: Optional callback for progress updates
            **kwargs: 
                - format: 'png' or 'jpeg' (default: png)
                - dpi: Resolution (default: 200)
        
        Returns:
            True if conversion succeeded
        
        Raises:
            ConversionError: If conversion fails
        """
        self.logger.info(f"Starting PDF→Images conversion: {input_path}")
        
        try:
            # Validate input
            self._report_progress(progress_callback, 5, "Validating file...")
            if not self.validate_input(input_path):
                raise ConversionError(
                    "Invalid input file",
                    file_path=input_path
                )
            
            # Import libraries
            self._report_progress(progress_callback, 10, "Loading libraries...")
            try:
                from pdf2image import convert_from_path
            except ImportError:
                raise ConversionError(
                    "pdf2image library not installed",
                    details="Install with: pip install pdf2image"
                )
            
            # Parameters
            output_format = kwargs.get('format', 'png').lower()
            dpi = kwargs.get('dpi', 200)
            
            # Prepare paths
            input_file = Path(input_path).resolve()
            output_file = Path(output_path).resolve()
            output_dir = output_file.parent
            output_base = output_file.stem
            
            # Ensure output directory exists
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Convert
            self._report_progress(progress_callback, 30, "Converting pages...")
            
            images = convert_from_path(
                str(input_file),
                dpi=dpi,
                fmt=output_format
            )
            
            if not images:
                raise ConversionError(
                    "No pages found in PDF",
                    file_path=input_path
                )
            
            # Save images
            self._report_progress(progress_callback, 60, f"Saving {len(images)} images...")
            
            saved_files = []
            for i, image in enumerate(images, start=1):
                if len(images) == 1:
                    # Single page: use original name
                    img_path = output_dir / f"{output_base}.{output_format}"
                else:
                    # Multiple pages: add number
                    img_path = output_dir / f"{output_base}_page_{i}.{output_format}"
                
                image.save(str(img_path), output_format.upper())
                saved_files.append(img_path)
                
                # Update progress
                progress = 60 + int((i / len(images)) * 30)
                self._report_progress(progress_callback, progress, f"Page {i}/{len(images)}")
            
            self._report_progress(progress_callback, 100, "Completed!")
            self.logger.info(f"Conversion completed: {len(saved_files)} images saved")
            
            return True
        
        except ConversionError:
            raise
        
        except Exception as e:
            self.logger.error(f"PDF→Images conversion error: {e}", exc_info=True)
            raise ConversionError(
                f"Conversion error: {str(e)}",
                file_path=input_path,
                details=str(e)
            )
