"""
Classe base astratta per tutti i convertitori
"""
from abc import ABC, abstractmethod
from typing import Callable, Optional, Dict, List
from pathlib import Path

from utils.logger import get_logger
from utils.error_handler import ConversionError


class ConverterBase(ABC):
    """
    Classe base astratta per implementare convertitori di documenti.
    
    Ogni nuovo convertitore deve ereditare da questa classe e implementare
    i metodi astratti get_info() e convert().
    """
    
    def __init__(self):
        """Inizializza il convertitore"""
        self.logger = get_logger(self.__class__.__name__)
        self._info = None
    
    @abstractmethod
    def get_info(self) -> Dict:
        """
        Ritorna informazioni sul convertitore.
        
        Returns:
            Dizionario con:
                - name (str): Nome del convertitore
                - input_formats (List[str]): Formati input supportati (es. ['.doc', '.docx'])
                - output_format (str): Formato output (es. '.pdf')
                - description (str): Descrizione convertitore
                - requires_dependency (Optional[str]): Dipendenza richiesta (es. 'libreoffice')
        
        Example:
            {
                'name': 'Word to PDF',
                'input_formats': ['.doc', '.docx'],
                'output_format': '.pdf',
                'description': 'Converte documenti Word in PDF',
                'requires_dependency': 'libreoffice'
            }
        """
        pass
    
    @abstractmethod
    def convert(
        self,
        input_path: str,
        output_path: str,
        progress_callback: Optional[Callable[[int, str], None]] = None,
        **kwargs
    ) -> bool:
        """
        Esegue la conversione del documento.
        
        Args:
            input_path: Path completo del file di input
            output_path: Path completo del file di output
            progress_callback: Callback opzionale per aggiornare il progresso.
                              Firma: callback(percentuale: int, messaggio: str)
            **kwargs: Parametri aggiuntivi specifici del convertitore
        
        Returns:
            True se conversione riuscita, False altrimenti
        
        Raises:
            ConversionError: In caso di errore durante la conversione
        """
        pass
    
    def validate_input(self, input_path: str) -> bool:
        """
        Valida il file di input per questo convertitore.
        
        Args:
            input_path: Path del file da validare
        
        Returns:
            True se il file è valido per questo convertitore
        """
        path = Path(input_path)
        
        # Verifica esistenza file
        if not path.exists():
            self.logger.error(f"File non trovato: {input_path}")
            return False
        
        # Verifica estensione supportata
        extension = path.suffix.lower()
        info = self.get_info()
        
        if extension not in info['input_formats']:
            self.logger.error(
                f"Formato {extension} non supportato da {info['name']}. "
                f"Formati supportati: {', '.join(info['input_formats'])}"
            )
            return False
        
        return True
    
    def _report_progress(
        self,
        callback: Optional[Callable],
        percentage: int,
        message: str = ""
    ):
        """
        Invia un aggiornamento di progresso alla callback.
        
        Args:
            callback: Funzione di callback
            percentage: Percentuale completamento (0-100)
            message: Messaggio opzionale
        """
        if callback:
            try:
                callback(percentage, message)
            except Exception as e:
                self.logger.error(f"Errore in progress callback: {e}")
    
    def get_supported_extensions(self) -> List[str]:
        """
        Ritorna le estensioni supportate da questo convertitore.
        
        Returns:
            Lista di estensioni (es. ['.doc', '.docx'])
        """
        return self.get_info()['input_formats']
    
    def get_output_extension(self) -> str:
        """
        Ritorna l'estensione del file di output.
        
        Returns:
            Estensione output (es. '.pdf')
        """
        return self.get_info()['output_format']
    
    def get_name(self) -> str:
        """
        Ritorna il nome del convertitore.
        
        Returns:
            Nome del convertitore
        """
        return self.get_info()['name']
    
    def requires_dependency(self) -> Optional[str]:
        """
        Ritorna la dipendenza richiesta (se presente).
        
        Returns:
            Nome della dipendenza o None
        """
        info = self.get_info()
        return info.get('requires_dependency')
    
    def __str__(self):
        """Rappresentazione stringa del convertitore"""
        info = self.get_info()
        return (
            f"{info['name']}: "
            f"{', '.join(info['input_formats'])} → {info['output_format']}"
        )
    
    def __repr__(self):
        """Rappresentazione tecnica del convertitore"""
        return f"<{self.__class__.__name__}: {self.get_name()}>"
