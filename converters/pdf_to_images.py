"""
Convertitore PDF → Immagini
Supporta formato: .pdf → .png, .jpg
"""
from pathlib import Path
from typing import Optional, Callable

from core.converter_base import ConverterBase
from utils.error_handler import ConversionError


class PDFToImagesConverter(ConverterBase):
    """
    Convertitore da PDF a immagini (PNG/JPEG).
    
    Converte ogni pagina del PDF in un'immagine separata.
    """
    
    def __init__(self):
        """Inizializza il convertitore PDF → Immagini"""
        super().__init__()
    
    def get_info(self) -> dict:
        """Ritorna informazioni sul convertitore"""
        return {
            'name': 'PDF to Images',
            'input_formats': ['.pdf'],
            'output_format': '.png',
            'description': 'Converte pagine PDF in immagini (PNG/JPEG)',
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
        Converte un PDF in immagini.
        
        Args:
            input_path: Path del file PDF da convertire
            output_path: Path base per le immagini (es. output.png → output_1.png, output_2.png...)
            progress_callback: Callback per aggiornamenti progresso
            **kwargs: 
                - format: 'png' o 'jpeg' (default: png)
                - dpi: Risoluzione (default: 200)
        
        Returns:
            True se conversione riuscita
        
        Raises:
            ConversionError: In caso di errore durante la conversione
        """
        self.logger.info(f"Inizio conversione PDF→Immagini: {input_path}")
        
        try:
            # Validazione input
            self._report_progress(progress_callback, 5, "Validazione file...")
            if not self.validate_input(input_path):
                raise ConversionError(
                    "File di input non valido",
                    file_path=input_path
                )
            
            # Import librerie
            self._report_progress(progress_callback, 10, "Caricamento librerie...")
            try:
                from pdf2image import convert_from_path
            except ImportError:
                raise ConversionError(
                    "Libreria pdf2image non installata",
                    details="Installa con: pip install pdf2image"
                )
            
            # Parametri
            output_format = kwargs.get('format', 'png').lower()
            dpi = kwargs.get('dpi', 200)
            
            # Prepara path
            input_file = Path(input_path).resolve()
            output_file = Path(output_path).resolve()
            output_dir = output_file.parent
            output_base = output_file.stem
            
            # Assicura che la directory di output esista
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Conversione
            self._report_progress(progress_callback, 30, "Conversione pagine...")
            
            images = convert_from_path(
                str(input_file),
                dpi=dpi,
                fmt=output_format
            )
            
            if not images:
                raise ConversionError(
                    "Nessuna pagina trovata nel PDF",
                    file_path=input_path
                )
            
            # Salva immagini
            self._report_progress(progress_callback, 60, f"Salvataggio {len(images)} immagini...")
            
            saved_files = []
            for i, image in enumerate(images, start=1):
                if len(images) == 1:
                    # Un'unica pagina: usa nome originale
                    img_path = output_dir / f"{output_base}.{output_format}"
                else:
                    # Multiple pagine: aggiungi numero
                    img_path = output_dir / f"{output_base}_pagina_{i}.{output_format}"
                
                image.save(str(img_path), output_format.upper())
                saved_files.append(img_path)
                
                # Aggiorna progresso
                progress = 60 + int((i / len(images)) * 30)
                self._report_progress(progress_callback, progress, f"Pagina {i}/{len(images)}")
            
            self._report_progress(progress_callback, 100, "Completato!")
            self.logger.info(f"Conversione completata: {len(saved_files)} immagini salvate")
            
            return True
        
        except ConversionError:
            raise
        
        except Exception as e:
            self.logger.error(f"Errore conversione PDF→Immagini: {e}", exc_info=True)
            raise ConversionError(
                f"Errore conversione: {str(e)}",
                file_path=input_path,
                details=str(e)
            )
