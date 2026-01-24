"""
PDF Compress Converter - Compresses PDF files to reduce size.

Uses pypdf library to compress PDF files.
"""

from pathlib import Path
from typing import Optional, Callable

from core.converter_base import ConverterBase
from utils.error_handler import ConversionError


class PDFCompressConverter(ConverterBase):
    """
    Converter to compress PDF files reducing file size.
    """
    
    def __init__(self) -> None:
        """Initialize PDF Compress converter."""
        super().__init__()
    
    def get_info(self) -> dict:
        """Return converter metadata."""
        return {
            'name': 'PDF Compress',
            'description': 'Compresses PDF files reducing file size',
            'input_formats': ['.pdf'],
            'output_format': '.pdf',
            'requires_dep': None
        }
    
    def convert(
        self,
        input_file: Path,
        output_file: Path,
        progress_callback: Optional[Callable[[int, str], None]] = None
    ) -> bool:
        """
        Compress a PDF file.
        
        Args:
            input_file: Input PDF file
            output_file: Compressed PDF output file
            progress_callback: Optional callback for progress bar
            
        Returns:
            True if successful
        """
        try:
            from pypdf import PdfReader, PdfWriter
            
            self.logger.info(f"Compressing PDF: {input_file}")
            self._report_progress(progress_callback, 10, "Reading PDF...")
            
            # Read PDF
            reader = PdfReader(str(input_file))
            writer = PdfWriter()
            
            self._report_progress(progress_callback, 30, "Compressing pages...")
            
            # Copy pages with compression
            total_pages = len(reader.pages)
            for i, page in enumerate(reader.pages):
                # Compress images in page
                page.compress_content_streams()
                writer.add_page(page)
                
                # Update progress
                progress = 30 + int((i / total_pages) * 50)
                self._report_progress(progress_callback, progress, f"Page {i+1}/{total_pages}...")
            
            # Remove duplicate objects and compress
            self._report_progress(progress_callback, 80, "Final optimization...")
            
            # Compression settings
            writer.add_metadata(reader.metadata)
            
            self._report_progress(progress_callback, 90, "Saving...")
            
            # Write output
            with open(output_file, 'wb') as f:
                writer.write(f)
            
            self._report_progress(progress_callback, 100, "Completed!")
            
            # Verify result
            if output_file.exists() and output_file.stat().st_size > 0:
                original_size = input_file.stat().st_size
                compressed_size = output_file.stat().st_size
                reduction = ((original_size - compressed_size) / original_size) * 100
                
                self.logger.info(
                    f"✅ PDF compressed: {output_file}\n"
                    f"   Original: {original_size / 1024:.1f} KB\n"
                    f"   Compressed: {compressed_size / 1024:.1f} KB\n"
                    f"   Reduction: {reduction:.1f}%"
                )
                return True
            
            return False
        
        except ImportError as e:
            self.logger.error(f"Missing library: {e}")
            raise ConversionError(
                "pypdf library missing!\n\n"
                "Install with: pip install pypdf"
            )
        
        except Exception as e:
            self.logger.error(f"PDF compression error: {e}")
            raise ConversionError(
                f"PDF compression error: {str(e)}",
                file_path=str(input_file)
            )
