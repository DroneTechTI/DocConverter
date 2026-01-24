"""
Convertitore PDF → Word
Supporta formato: .pdf → .docx
"""
from pathlib import Path
from typing import Optional, Callable

from core.converter_base import ConverterBase
from utils.error_handler import ConversionError


class PDFToWordConverter(ConverterBase):
    """
    Convertitore da PDF a Word (.docx).
    
    Usa pdf2docx per estrarre testo e formattazione da PDF.
    """
    
    def __init__(self):
        """Inizializza il convertitore PDF → Word"""
        super().__init__()
    
    def get_info(self) -> dict:
        """Ritorna informazioni sul convertitore"""
        return {
            'name': 'PDF to Word',
            'input_formats': ['.pdf'],
            'output_format': '.docx',
            'description': 'Converte documenti PDF in formato Word modificabile',
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
        Converte un documento PDF in Word.
        
        Args:
            input_path: Path del file PDF da convertire
            output_path: Path del file Word di output
            progress_callback: Callback per aggiornamenti progresso
            **kwargs: Parametri aggiuntivi
        
        Returns:
            True se conversione riuscita
        
        Raises:
            ConversionError: In caso di errore durante la conversione
        """
        self.logger.info(f"Inizio conversione PDF→Word: {input_path}")
        
        try:
            # Validazione input
            self._report_progress(progress_callback, 5, "Validazione file...")
            if not self.validate_input(input_path):
                raise ConversionError(
                    "File di input non valido",
                    file_path=input_path
                )
            
            # Import libreria
            self._report_progress(progress_callback, 10, "Caricamento librerie...")
            try:
                from pdf2docx import Converter
            except ImportError:
                raise ConversionError(
                    "Libreria pdf2docx non installata",
                    details="Installa con: pip install pdf2docx"
                )
            
            # Prepara path
            input_file = Path(input_path).resolve()
            output_file = Path(output_path).resolve()
            output_dir = output_file.parent
            
            # Assicura che la directory di output esista
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Conversione
            self._report_progress(progress_callback, 30, "Conversione in corso...")
            
            cv = Converter(str(input_file))
            cv.convert(str(output_file), start=0, end=None)
            cv.close()
            
            self._report_progress(progress_callback, 90, "Finalizzazione...")
            
            # Verifica output
            if not output_file.exists() or output_file.stat().st_size == 0:
                raise ConversionError(
                    "File Word non generato",
                    file_path=input_path
                )
            
            self._report_progress(progress_callback, 100, "Completato!")
            self.logger.info(f"Conversione completata: {output_file}")
            
            return True
        
        except ConversionError:
            raise
        
        except Exception as e:
            self.logger.error(f"Errore conversione PDF→Word: {e}", exc_info=True)
            raise ConversionError(
                f"Errore conversione: {str(e)}",
                file_path=input_path,
                details=str(e)
            )
