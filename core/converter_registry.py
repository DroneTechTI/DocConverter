"""
Registry per gestire tutti i convertitori disponibili
"""
from typing import Dict, List, Optional, Type
from pathlib import Path

from .converter_base import ConverterBase
from utils.logger import get_logger


class ConverterRegistry:
    """
    Registro centralizzato di tutti i convertitori disponibili.
    
    Gestisce la registrazione automatica, il recupero e la selezione
    del convertitore appropriato per una data conversione.
    """
    
    def __init__(self):
        """Inizializza il registry"""
        self.logger = get_logger("ConverterRegistry")
        self._converters: Dict[str, ConverterBase] = {}
        self._extension_map: Dict[str, List[str]] = {}
    
    def register(self, converter_class: Type[ConverterBase]):
        """
        Registra un nuovo convertitore.
        
        Args:
            converter_class: Classe del convertitore da registrare
        
        Example:
            registry.register(WordToPDFConverter)
        """
        try:
            # Istanzia il convertitore
            converter = converter_class()
            
            # Ottieni info
            info = converter.get_info()
            name = info['name']
            
            # Registra
            self._converters[name] = converter
            
            # Mappa estensioni input -> convertitore
            for ext in info['input_formats']:
                if ext not in self._extension_map:
                    self._extension_map[ext] = []
                self._extension_map[ext].append(name)
            
            self.logger.info(f"Convertitore registrato: {name}")
            self.logger.debug(f"  Input: {', '.join(info['input_formats'])}")
            self.logger.debug(f"  Output: {info['output_format']}")
            
        except Exception as e:
            self.logger.error(f"Errore registrazione convertitore {converter_class}: {e}")
    
    def get_converter(self, name: str) -> Optional[ConverterBase]:
        """
        Ottiene un convertitore per nome.
        
        Args:
            name: Nome del convertitore
        
        Returns:
            Istanza del convertitore o None
        """
        return self._converters.get(name)
    
    def get_converter_for_file(
        self,
        file_path: str,
        output_format: str = '.pdf'
    ) -> Optional[ConverterBase]:
        """
        Trova il convertitore appropriato per un file.
        
        Args:
            file_path: Path del file da convertire
            output_format: Formato di output desiderato
        
        Returns:
            Convertitore appropriato o None
        """
        extension = Path(file_path).suffix.lower()
        
        # Trova convertitori che supportano questa estensione
        converter_names = self._extension_map.get(extension, [])
        
        if not converter_names:
            self.logger.warning(f"Nessun convertitore per estensione {extension}")
            return None
        
        # Trova il convertitore con il formato output corretto
        for name in converter_names:
            converter = self._converters[name]
            if converter.get_output_extension() == output_format:
                return converter
        
        # Se nessuno ha il formato esatto, ritorna il primo disponibile
        self.logger.warning(
            f"Formato output {output_format} non disponibile per {extension}, "
            f"uso {self._converters[converter_names[0]].get_output_extension()}"
        )
        return self._converters[converter_names[0]]
    
    def get_all_converters(self) -> List[ConverterBase]:
        """
        Ritorna tutti i convertitori registrati.
        
        Returns:
            Lista di convertitori
        """
        return list(self._converters.values())
    
    def get_supported_input_formats(self) -> List[str]:
        """
        Ritorna tutte le estensioni di input supportate.
        
        Returns:
            Lista di estensioni
        """
        return list(self._extension_map.keys())
    
    def get_converters_info(self) -> List[Dict]:
        """
        Ritorna informazioni su tutti i convertitori.
        
        Returns:
            Lista di dizionari con info
        """
        return [conv.get_info() for conv in self._converters.values()]
    
    def is_format_supported(self, extension: str) -> bool:
        """
        Verifica se un formato è supportato.
        
        Args:
            extension: Estensione da verificare (es. '.docx')
        
        Returns:
            True se supportato
        """
        return extension.lower() in self._extension_map
    
    def clear(self):
        """Rimuove tutti i convertitori registrati"""
        self._converters.clear()
        self._extension_map.clear()
        self.logger.info("Registry pulito")
    
    def __len__(self):
        """Ritorna il numero di convertitori registrati"""
        return len(self._converters)
    
    def __str__(self):
        """Rappresentazione stringa del registry"""
        return (
            f"ConverterRegistry: {len(self._converters)} convertitori, "
            f"{len(self._extension_map)} formati supportati"
        )


# Istanza globale del registry
_global_registry = None


def get_registry() -> ConverterRegistry:
    """
    Ottiene l'istanza globale del registry.
    
    Returns:
        Istanza singleton del ConverterRegistry
    """
    global _global_registry
    if _global_registry is None:
        _global_registry = ConverterRegistry()
    return _global_registry
