"""
PDF Merge Converter - Merges multiple PDFs into one.

Uses pypdf library to merge PDF files.
"""

from pathlib import Path
from typing import List, Optional, Callable

from core.converter_base import ConverterBase
from utils.error_handler import ConversionError


class PDFMergeConverter(ConverterBase):
    """
    Converter to merge multiple PDF files into a single PDF.
    """
    
    def __init__(self) -> None:
        """Initialize PDF Merge converter."""
        super().__init__()
    
    def get_info(self) -> dict:
        """Return converter metadata."""
        return {
            'name': 'PDF Merge',
            'description': 'Merges multiple PDF files into a single document',
            'input_formats': ['.pdf'],
            'output_format': '.pdf',
            'requires_dep': None
        }
    
    def merge_pdfs(
        self,
        pdf_files: List[Path],
        output_file: Path,
        progress_callback: Optional[Callable[[int, str], None]] = None
    ) -> bool:
        """
        Merge multiple PDFs into one.
        
        Args:
            pdf_files: List of PDF files to merge
            output_file: Output PDF file
            progress_callback: Optional callback for progress bar
            
        Returns:
            True if successful
        """
        try:
            from pypdf import PdfWriter, PdfReader
            
            self.logger.info(f"Merging {len(pdf_files)} PDF files...")
            self._report_progress(progress_callback, 10, "Initializing...")
            
            # Create writer
            writer = PdfWriter()
            
            # Add each PDF
            for i, pdf_file in enumerate(pdf_files):
                progress = 10 + int((i / len(pdf_files)) * 80)
                self._report_progress(progress_callback, progress, f"Processing {pdf_file.name}...")
                
                try:
                    reader = PdfReader(str(pdf_file))
                    
                    # Add all pages
                    for page in reader.pages:
                        writer.add_page(page)
                    
                    self.logger.info(f"✓ Added: {pdf_file.name} ({len(reader.pages)} pages)")
                
                except Exception as e:
                    self.logger.error(f"Error reading {pdf_file}: {e}")
                    raise ConversionError(
                        f"Cannot read PDF: {pdf_file.name}",
                        file_path=str(pdf_file),
                        details=str(e)
                    )
            
            self._report_progress(progress_callback, 90, "Saving merged PDF...")
            
            # Write output
            with open(output_file, 'wb') as f:
                writer.write(f)
            
            self._report_progress(progress_callback, 100, "Completed!")
            
            if output_file.exists() and output_file.stat().st_size > 0:
                total_pages = len(writer.pages)
                self.logger.info(f"✅ Merged PDF created: {output_file} ({total_pages} pages)")
                return True
            
            return False
        
        except ImportError as e:
            self.logger.error(f"Missing library: {e}")
            raise ConversionError(
                "pypdf library missing!\n\n"
                "Install with: pip install pypdf"
            )
        
        except Exception as e:
            self.logger.error(f"PDF merge error: {e}")
            raise ConversionError(f"PDF merge error: {str(e)}")
    
    def convert(
        self,
        input_file: Path,
        output_file: Path,
        progress_callback: Optional[Callable[[int, str], None]] = None
    ) -> bool:
        """
        Convert implementation for ConverterBase compatibility.
        Note: For PDF merge use merge_pdfs() directly.
        """
        raise NotImplementedError(
            "To merge PDFs use merge_pdfs() with a list of files"
        )
