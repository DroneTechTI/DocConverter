"""
Word to PDF Converter - Pure Python Implementation.

No Office/LibreOffice required! Uses only Python libraries: python-docx + reportlab.
"""

from pathlib import Path
import platform
from typing import Optional, Callable, Any

from core.converter_base import ConverterBase
from utils.error_handler import ConversionError


class WordToPDFConverter(ConverterBase):
    """
    Word to PDF converter using ONLY Python libraries.
    
    No Office/LibreOffice installation required!
    """
    
    def __init__(self) -> None:
        """Initialize Word to PDF converter."""
        super().__init__()
        self._system = platform.system().lower()
    
    def get_info(self) -> dict:
        """Return converter metadata."""
        return {
            'name': 'Word to PDF',
            'description': 'Converts Word documents (.docx, .doc) to PDF',
            'input_formats': ['.docx', '.doc'],
            'output_format': '.pdf',
            'requires_dep': None  # ✅ No external dependencies!
        }
    
    def convert(
        self,
        input_file: Path,
        output_file: Path,
        progress_callback: Optional[Callable[[int, str], None]] = None,
        **kwargs: Any
    ) -> bool:
        """
        Convert Word to PDF using ONLY Python libraries.
        
        Args:
            input_file: Input Word file
            output_file: Output PDF file
            progress_callback: Optional callback for progress bar
            **kwargs: Additional parameters
            
        Returns:
            True if successful
        """
        try:
            self.logger.info(f"Starting conversion: {input_file} → {output_file}")
            self._report_progress(progress_callback, 10, "Reading Word document...")
            
            # ✅ Pure Python method
            return self._convert_with_python_libs(input_file, output_file, progress_callback)
            
        except Exception as e:
            self.logger.error(f"Conversion error: {e}")
            raise ConversionError(
                f"Word→PDF conversion error: {str(e)}",
                file_path=str(input_file)
            )
    
    def _convert_with_python_libs(
        self,
        input_file: Path,
        output_file: Path,
        progress_callback: Optional[Callable[[int, str], None]] = None
    ) -> bool:
        """
        ⚡ Pure Python conversion - No Office required!
        
        Uses:
        - python-docx: Reads .docx files
        - reportlab: Creates PDF
        """
        try:
            from docx import Document
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.units import inch
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
            
            self._report_progress(progress_callback, 20, "Reading Word document...")
            
            # Read Word document
            doc = Document(str(input_file))
            
            self._report_progress(progress_callback, 40, "Creating PDF...")
            
            # Create PDF with ReportLab
            pdf_doc = SimpleDocTemplate(
                str(output_file),
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18,
            )
            
            # Styles
            styles = getSampleStyleSheet()
            story = []
            
            self._report_progress(progress_callback, 60, "Converting content...")
            
            # Convert paragraphs
            for para in doc.paragraphs:
                if para.text.strip():
                    # Determine style
                    if para.style.name.startswith('Heading'):
                        style = styles['Heading1']
                    else:
                        style = styles['Normal']
                    
                    # Add paragraph
                    p = Paragraph(para.text, style)
                    story.append(p)
                    story.append(Spacer(1, 0.2*inch))
            
            # Convert tables (simplified)
            for table in doc.tables:
                for row in table.rows:
                    row_text = ' | '.join([cell.text for cell in row.cells])
                    if row_text.strip():
                        p = Paragraph(row_text, styles['Normal'])
                        story.append(p)
                        story.append(Spacer(1, 0.1*inch))
                
                story.append(Spacer(1, 0.3*inch))
            
            self._report_progress(progress_callback, 80, "Saving PDF...")
            
            # Generate PDF
            pdf_doc.build(story)
            
            self._report_progress(progress_callback, 100, "Completed!")
            
            if output_file.exists() and output_file.stat().st_size > 0:
                self.logger.info(f"✅ Conversion completed: {output_file}")
                return True
            
            return False
            
        except ImportError as e:
            self.logger.error(f"Missing libraries: {e}")
            raise ConversionError(
                f"Missing Python libraries!\n\n"
                f"Install with:\n"
                f"pip install python-docx reportlab\n\n"
                f"Error: {e}"
            )
        
        except Exception as e:
            self.logger.error(f"Python conversion error: {e}")
            raise ConversionError(f"Conversion error: {str(e)}")
