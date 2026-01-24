"""
Convertitore HTML → PDF
Supporta formati: .html, .htm → .pdf
"""
from pathlib import Path
from typing import Optional, Callable

from core.converter_base import ConverterBase
from utils.error_handler import ConversionError


class HTMLToPDFConverter(ConverterBase):
    """
    Convertitore da HTML a PDF.
    
    Usa pdfkit/wkhtmltopdf per rendering HTML→PDF.
    """
    
    def __init__(self):
        """Inizializza il convertitore HTML → PDF"""
        super().__init__()
    
    def get_info(self) -> dict:
        """Ritorna informazioni sul convertitore"""
        return {
            'name': 'HTML to PDF',
            'input_formats': ['.html', '.htm'],
            'output_format': '.pdf',
            'description': 'Converte pagine HTML in formato PDF',
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
        Converte un file HTML in PDF.
        
        Args:
            input_path: Path del file HTML da convertire
            output_path: Path del file PDF di output
            progress_callback: Callback per aggiornamenti progresso
            **kwargs: Parametri aggiuntivi
        
        Returns:
            True se conversione riuscita
        
        Raises:
            ConversionError: In caso di errore durante la conversione
        """
        self.logger.info(f"Inizio conversione HTML→PDF: {input_path}")
        
        try:
            # Validazione input
            self._report_progress(progress_callback, 5, "Validazione file...")
            if not self.validate_input(input_path):
                raise ConversionError(
                    "File di input non valido",
                    file_path=input_path
                )
            
            # Import librerie (prova diversi metodi)
            self._report_progress(progress_callback, 10, "Caricamento librerie...")
            
            # Metodo 1: weasyprint (puro Python, nessuna dipendenza esterna)
            try:
                from weasyprint import HTML
                method = 'weasyprint'
                self.logger.info("Usando weasyprint per conversione")
            except ImportError:
                # Metodo 2: pdfkit (richiede wkhtmltopdf)
                try:
                    import pdfkit
                    method = 'pdfkit'
                    self.logger.info("Usando pdfkit per conversione")
                except ImportError:
                    raise ConversionError(
                        "Nessuna libreria HTML→PDF disponibile",
                        details=(
                            "Installa una di queste librerie:\n"
                            "  pip install weasyprint (consigliato)\n"
                            "  pip install pdfkit (richiede wkhtmltopdf)"
                        )
                    )
            
            # Prepara path
            input_file = Path(input_path).resolve()
            output_file = Path(output_path).resolve()
            output_dir = output_file.parent
            
            # Assicura che la directory di output esista
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Conversione
            self._report_progress(progress_callback, 30, "Conversione in corso...")
            
            if method == 'weasyprint':
                HTML(filename=str(input_file)).write_pdf(str(output_file))
            else:  # pdfkit
                import pdfkit
                pdfkit.from_file(str(input_file), str(output_file))
            
            # Verifica output
            if not output_file.exists() or output_file.stat().st_size == 0:
                raise ConversionError(
                    "File PDF non generato",
                    file_path=input_path
                )
            
            self._report_progress(progress_callback, 100, "Completato!")
            self.logger.info(f"Conversione completata: {output_file}")
            
            return True
        
        except ConversionError:
            raise
        
        except Exception as e:
            self.logger.error(f"Errore conversione HTML→PDF: {e}", exc_info=True)
            raise ConversionError(
                f"Errore conversione: {str(e)}",
                file_path=input_path,
                details=str(e)
            )
