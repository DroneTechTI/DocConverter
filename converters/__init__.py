"""
Moduli di conversione per DocConverter
"""
from .word_to_pdf import WordToPDFConverter
from .pdf_to_word import PDFToWordConverter
from .pdf_to_images import PDFToImagesConverter
from .images_to_pdf import ImagesToPDFConverter
from .excel_to_pdf import ExcelToPDFConverter
from .powerpoint_to_pdf import PowerPointToPDFConverter
from .html_to_pdf import HTMLToPDFConverter
from .pdf_merge import PDFMergeConverter
from .pdf_compress import PDFCompressConverter

# Lista di tutti i convertitori disponibili
AVAILABLE_CONVERTERS = [
    WordToPDFConverter,
    PDFToWordConverter,
    PDFToImagesConverter,
    ImagesToPDFConverter,
    ExcelToPDFConverter,
    PowerPointToPDFConverter,
    HTMLToPDFConverter,
    PDFCompressConverter,
    # PDFMergeConverter non registrato (usa API speciale)
]

__all__ = [
    'WordToPDFConverter',
    'PDFToWordConverter',
    'PDFToImagesConverter',
    'ImagesToPDFConverter',
    'ExcelToPDFConverter',
    'PowerPointToPDFConverter',
    'HTMLToPDFConverter',
    'PDFMergeConverter',
    'PDFCompressConverter',
    'AVAILABLE_CONVERTERS'
]
