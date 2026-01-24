"""
PDF Merge Converter - Unisce più PDF in uno solo

Usa pypdf per unire PDF
"""

from pathlib import Path
from typing import List

from core.converter_base import ConverterBase
from utils.error_handler import ConversionError


class PDFMergeConverter(ConverterBase):
    """
    Convertitore per unire più file PDF in un unico PDF
    """
    
    def __init__(self):
        """Inizializza il convertitore PDF Merge"""
        super().__init__()
    
    def get_info(self) -> dict:
        """Informazioni sul convertitore"""
        return {
            'name': 'PDF Merge',
            'description': 'Unisce più file PDF in un unico documento',
            'input_formats': ['.pdf'],
            'output_format': '.pdf',
            'requires_dep': None
        }
    
    def merge_pdfs(self, pdf_files: List[Path], output_file: Path, progress_callback=None) -> bool:
        """
        Unisce più PDF in uno solo
        
        Args:
            pdf_files: Lista di file PDF da unire
            output_file: File PDF di output
            progress_callback: Callback per progress bar
            
        Returns:
            True se successo
        """
        try:
            from pypdf import PdfWriter, PdfReader
            
            self.logger.info(f"Unione di {len(pdf_files)} file PDF...")
            self._report_progress(progress_callback, 10, "Inizializzazione...")
            
            # Crea writer
            writer = PdfWriter()
            
            # Aggiungi ogni PDF
            for i, pdf_file in enumerate(pdf_files):
                progress = 10 + int((i / len(pdf_files)) * 80)
                self._report_progress(progress_callback, progress, f"Elaborazione {pdf_file.name}...")
                
                try:
                    reader = PdfReader(str(pdf_file))
                    
                    # Aggiungi tutte le pagine
                    for page in reader.pages:
                        writer.add_page(page)
                    
                    self.logger.info(f"✓ Aggiunto: {pdf_file.name} ({len(reader.pages)} pagine)")
                
                except Exception as e:
                    self.logger.error(f"Errore lettura {pdf_file}: {e}")
                    raise ConversionError(
                        f"Impossibile leggere PDF: {pdf_file.name}",
                        file_path=str(pdf_file),
                        details=str(e)
                    )
            
            self._report_progress(progress_callback, 90, "Salvataggio PDF unificato...")
            
            # Scrivi output
            with open(output_file, 'wb') as f:
                writer.write(f)
            
            self._report_progress(progress_callback, 100, "Completato!")
            
            if output_file.exists() and output_file.stat().st_size > 0:
                total_pages = len(writer.pages)
                self.logger.info(f"✅ PDF unificato creato: {output_file} ({total_pages} pagine)")
                return True
            
            return False
        
        except ImportError as e:
            self.logger.error(f"Libreria mancante: {e}")
            raise ConversionError(
                "Libreria pypdf mancante!\n\n"
                "Installa con: pip install pypdf"
            )
        
        except Exception as e:
            self.logger.error(f"Errore merge PDF: {e}")
            raise ConversionError(f"Errore unione PDF: {str(e)}")
    
    def convert(self, input_file: Path, output_file: Path, progress_callback=None) -> bool:
        """
        Implementazione convert per compatibilità con ConverterBase
        Nota: per merge PDF usare merge_pdfs() direttamente
        """
        raise NotImplementedError(
            "Per unire PDF usa merge_pdfs() con lista di file"
        )
