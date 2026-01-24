"""
Convertitore Immagini → PDF
Supporta formati: .png, .jpg, .jpeg, .bmp, .gif → .pdf
"""
from pathlib import Path
from typing import Optional, Callable

from core.converter_base import ConverterBase
from utils.error_handler import ConversionError


class ImagesToPDFConverter(ConverterBase):
    """
    Convertitore da immagini a PDF.
    
    Converte una o più immagini in un documento PDF.
    """
    
    def __init__(self):
        """Inizializza il convertitore Immagini → PDF"""
        super().__init__()
    
    def get_info(self) -> dict:
        """Ritorna informazioni sul convertitore"""
        return {
            'name': 'Images to PDF',
            'input_formats': ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp'],
            'output_format': '.pdf',
            'description': 'Converte immagini in formato PDF',
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
        Converte un'immagine in PDF.
        
        Args:
            input_path: Path dell'immagine da convertire
            output_path: Path del file PDF di output
            progress_callback: Callback per aggiornamenti progresso
            **kwargs:
                - quality: Qualità JPEG (1-100, default: 95)
        
        Returns:
            True se conversione riuscita
        
        Raises:
            ConversionError: In caso di errore durante la conversione
        """
        self.logger.info(f"Inizio conversione Immagine→PDF: {input_path}")
        
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
                from PIL import Image
            except ImportError:
                raise ConversionError(
                    "Libreria Pillow non installata",
                    details="Installa con: pip install Pillow"
                )
            
            # Parametri
            quality = kwargs.get('quality', 95)
            
            # Prepara path
            input_file = Path(input_path).resolve()
            output_file = Path(output_path).resolve()
            output_dir = output_file.parent
            
            # Assicura che la directory di output esista
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Carica immagine
            self._report_progress(progress_callback, 30, "Caricamento immagine...")
            
            img = Image.open(str(input_file))
            
            # Converti in RGB se necessario (PDF richiede RGB)
            if img.mode in ('RGBA', 'LA', 'P'):
                self._report_progress(progress_callback, 50, "Conversione formato...")
                # Crea sfondo bianco per trasparenza
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Salva come PDF
            self._report_progress(progress_callback, 70, "Creazione PDF...")
            
            img.save(
                str(output_file),
                'PDF',
                resolution=100.0,
                quality=quality,
                optimize=True
            )
            
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
            self.logger.error(f"Errore conversione Immagine→PDF: {e}", exc_info=True)
            raise ConversionError(
                f"Errore conversione: {str(e)}",
                file_path=input_path,
                details=str(e)
            )
