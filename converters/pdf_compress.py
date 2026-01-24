"""
PDF Compress Converter - Comprime PDF riducendo dimensioni

Usa pypdf per comprimere PDF
"""

from pathlib import Path

from core.converter_base import ConverterBase
from utils.error_handler import ConversionError


class PDFCompressConverter(ConverterBase):
    """
    Convertitore per comprimere file PDF riducendo le dimensioni
    """
    
    def __init__(self):
        """Inizializza il convertitore PDF Compress"""
        super().__init__()
    
    def get_info(self) -> dict:
        """Informazioni sul convertitore"""
        return {
            'name': 'PDF Compress',
            'description': 'Comprime file PDF riducendo le dimensioni',
            'input_formats': ['.pdf'],
            'output_format': '.pdf',
            'requires_dep': None
        }
    
    def convert(self, input_file: Path, output_file: Path, progress_callback=None) -> bool:
        """
        Comprime un PDF
        
        Args:
            input_file: File PDF di input
            output_file: File PDF compresso di output
            progress_callback: Callback per progress bar
            
        Returns:
            True se successo
        """
        try:
            from pypdf import PdfReader, PdfWriter
            
            self.logger.info(f"Compressione PDF: {input_file}")
            self._report_progress(progress_callback, 10, "Lettura PDF...")
            
            # Leggi PDF
            reader = PdfReader(str(input_file))
            writer = PdfWriter()
            
            self._report_progress(progress_callback, 30, "Compressione pagine...")
            
            # Copia pagine con compressione
            total_pages = len(reader.pages)
            for i, page in enumerate(reader.pages):
                # Comprimi immagini nella pagina
                page.compress_content_streams()
                writer.add_page(page)
                
                # Aggiorna progresso
                progress = 30 + int((i / total_pages) * 50)
                self._report_progress(progress_callback, progress, f"Pagina {i+1}/{total_pages}...")
            
            # Rimuovi oggetti duplicati e comprimi
            self._report_progress(progress_callback, 80, "Ottimizzazione finale...")
            
            # Impostazioni di compressione
            writer.add_metadata(reader.metadata)
            
            self._report_progress(progress_callback, 90, "Salvataggio...")
            
            # Scrivi output
            with open(output_file, 'wb') as f:
                writer.write(f)
            
            self._report_progress(progress_callback, 100, "Completato!")
            
            # Verifica risultato
            if output_file.exists() and output_file.stat().st_size > 0:
                original_size = input_file.stat().st_size
                compressed_size = output_file.stat().st_size
                reduction = ((original_size - compressed_size) / original_size) * 100
                
                self.logger.info(
                    f"✅ PDF compresso: {output_file}\n"
                    f"   Originale: {original_size / 1024:.1f} KB\n"
                    f"   Compresso: {compressed_size / 1024:.1f} KB\n"
                    f"   Riduzione: {reduction:.1f}%"
                )
                return True
            
            return False
        
        except ImportError as e:
            self.logger.error(f"Libreria mancante: {e}")
            raise ConversionError(
                "Libreria pypdf mancante!\n\n"
                "Installa con: pip install pypdf"
            )
        
        except Exception as e:
            self.logger.error(f"Errore compressione PDF: {e}")
            raise ConversionError(
                f"Errore compressione PDF: {str(e)}",
                file_path=str(input_file)
            )
