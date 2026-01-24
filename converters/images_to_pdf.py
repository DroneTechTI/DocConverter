"""
Images to PDF Converter.

Converts image files to PDF format with support for multiple image formats.
"""
from pathlib import Path
from typing import Optional, Callable

from core.converter_base import ConverterBase
from utils.error_handler import ConversionError


class ImagesToPDFConverter(ConverterBase):
    """
    Images to PDF converter.
    
    Converts image files to PDF documents with automatic format handling.
    """
    
    def __init__(self) -> None:
        """Initialize Images to PDF converter."""
        super().__init__()
    
    def get_info(self) -> dict:
        """Return converter metadata."""
        return {
            'name': 'Images to PDF',
            'input_formats': ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp'],
            'output_format': '.pdf',
            'description': 'Converts images to PDF format',
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
        Convert image to PDF format.
        
        Args:
            input_path: Path to image file to convert
            output_path: Path for output PDF file
            progress_callback: Optional callback for progress updates
            **kwargs:
                - quality: JPEG quality (1-100, default: 95)
        
        Returns:
            True if conversion succeeded
        
        Raises:
            ConversionError: If conversion fails
        """
        self.logger.info(f"Starting Image→PDF conversion: {input_path}")
        
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
                from PIL import Image
            except ImportError:
                raise ConversionError(
                    "Pillow library not installed",
                    details="Install with: pip install Pillow"
                )
            
            # Parameters
            quality = kwargs.get('quality', 95)
            
            # Prepare paths
            input_file = Path(input_path).resolve()
            output_file = Path(output_path).resolve()
            output_dir = output_file.parent
            
            # Ensure output directory exists
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Load image
            self._report_progress(progress_callback, 30, "Loading image...")
            
            img = Image.open(str(input_file))
            
            # Convert to RGB if needed (PDF requires RGB)
            if img.mode in ('RGBA', 'LA', 'P'):
                self._report_progress(progress_callback, 50, "Converting format...")
                # Create white background for transparency
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Save as PDF
            self._report_progress(progress_callback, 70, "Creating PDF...")
            
            img.save(
                str(output_file),
                'PDF',
                resolution=100.0,
                quality=quality,
                optimize=True
            )
            
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
            self.logger.error(f"Image→PDF conversion error: {e}", exc_info=True)
            raise ConversionError(
                f"Conversion error: {str(e)}",
                file_path=input_path,
                details=str(e)
            )
