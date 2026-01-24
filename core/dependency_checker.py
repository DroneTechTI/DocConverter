"""
Controllo dipendenze sistema per DocConverter
"""
import os
import sys
import platform
import shutil
import subprocess
from typing import Dict, List, Tuple, Optional

from config.settings import Settings
from utils.logger import get_logger
from utils.error_handler import DependencyError


class DependencyChecker:
    """
    Controlla la presenza delle dipendenze necessarie per i convertitori.
    """
    
    def __init__(self):
        """Inizializza il checker"""
        self.logger = get_logger("DependencyChecker")
        self.system = platform.system().lower()
        self._cache = {}
    
    def check_dependency(self, dependency_name: str) -> Tuple[bool, Optional[str]]:
        """
        Controlla se una dipendenza è disponibile.
        
        Args:
            dependency_name: Nome della dipendenza (es. 'libreoffice')
        
        Returns:
            Tupla (is_available, path_or_error_message)
        """
        # Usa cache se disponibile
        if dependency_name in self._cache:
            return self._cache[dependency_name]
        
        # Ottieni configurazione dipendenza
        dep_config = Settings.DEPENDENCIES.get(dependency_name)
        
        if not dep_config:
            self.logger.warning(f"Dipendenza sconosciuta: {dependency_name}")
            return False, f"Dipendenza non configurata: {dependency_name}"
        
        # Determina comandi da cercare per il sistema corrente
        if 'windows' in self.system:
            commands = dep_config.get('windows', [])
        elif 'linux' in self.system:
            commands = dep_config.get('linux', [])
        elif 'darwin' in self.system:  # macOS
            commands = dep_config.get('linux', [])  # Usa config Linux per macOS
        else:
            self.logger.error(f"Sistema operativo non supportato: {self.system}")
            return False, f"Sistema operativo non supportato: {self.system}"
        
        # Cerca ogni comando
        for cmd in commands:
            path = self._find_executable(cmd)
            if path:
                self.logger.info(f"Dipendenza {dependency_name} trovata: {path}")
                result = (True, path)
                self._cache[dependency_name] = result
                return result
        
        # Non trovata
        error_msg = self._get_installation_hint(dependency_name)
        result = (False, error_msg)
        self._cache[dependency_name] = result
        return result
    
    def _find_executable(self, command: str) -> Optional[str]:
        """
        Cerca un eseguibile nel sistema.
        
        Args:
            command: Nome del comando/eseguibile
        
        Returns:
            Path completo se trovato, None altrimenti
        """
        # Usa shutil.which per cercare nel PATH
        path = shutil.which(command)
        if path:
            return path
        
        # Windows: cerca in Program Files
        if 'windows' in self.system and command.endswith('.exe'):
            common_paths = [
                os.path.join(os.environ.get('ProgramFiles', 'C:\\Program Files'), 'LibreOffice', 'program'),
                os.path.join(os.environ.get('ProgramFiles(x86)', 'C:\\Program Files (x86)'), 'LibreOffice', 'program'),
                os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Programs', 'LibreOffice', 'program'),
            ]
            
            for base_path in common_paths:
                full_path = os.path.join(base_path, command)
                if os.path.isfile(full_path):
                    return full_path
        
        # Linux: cerca in percorsi comuni
        elif 'linux' in self.system:
            common_paths = [
                '/usr/bin',
                '/usr/local/bin',
                '/opt/libreoffice/program',
                '/snap/bin'
            ]
            
            for base_path in common_paths:
                full_path = os.path.join(base_path, command)
                if os.path.isfile(full_path):
                    return full_path
        
        return None
    
    def _get_installation_hint(self, dependency_name: str) -> str:
        """
        Genera un suggerimento di installazione per una dipendenza.
        
        Args:
            dependency_name: Nome della dipendenza
        
        Returns:
            Messaggio con istruzioni di installazione
        """
        if dependency_name == 'libreoffice':
            if 'windows' in self.system:
                return (
                    "LibreOffice non trovato.\n"
                    "Scaricalo da: https://www.libreoffice.org/download/download/\n"
                    "Installalo e riavvia l'applicazione."
                )
            elif 'linux' in self.system:
                return (
                    "LibreOffice non trovato.\n"
                    "Installalo con: sudo apt-get install libreoffice\n"
                    "(o equivalente per la tua distribuzione)"
                )
        
        return f"{dependency_name} non trovato. Installalo e riprova."
    
    def check_all_dependencies(self) -> Dict[str, Tuple[bool, str]]:
        """
        Controlla tutte le dipendenze configurate.
        
        Returns:
            Dizionario {dependency_name: (is_available, path_or_message)}
        """
        results = {}
        
        for dep_name in Settings.DEPENDENCIES.keys():
            results[dep_name] = self.check_dependency(dep_name)
        
        return results
    
    def get_missing_dependencies(self) -> List[str]:
        """
        Ritorna lista delle dipendenze mancanti.
        
        Returns:
            Lista di nomi dipendenze mancanti
        """
        missing = []
        
        for dep_name in Settings.DEPENDENCIES.keys():
            is_available, _ = self.check_dependency(dep_name)
            if not is_available:
                missing.append(dep_name)
        
        return missing
    
    def verify_converter_dependencies(self, converter_name: str) -> Tuple[bool, List[str]]:
        """
        Verifica che tutte le dipendenze per un convertitore siano disponibili.
        
        Args:
            converter_name: Nome del convertitore da verificare
        
        Returns:
            Tupla (all_available, list_of_missing)
        """
        missing = []
        
        # Trova quali dipendenze servono per questo convertitore
        for dep_name, dep_config in Settings.DEPENDENCIES.items():
            required_for = dep_config.get('required_for', [])
            
            if converter_name in required_for:
                is_available, _ = self.check_dependency(dep_name)
                if not is_available:
                    missing.append(dep_name)
        
        return len(missing) == 0, missing
    
    def clear_cache(self):
        """Pulisce la cache dei controlli"""
        self._cache.clear()
    
    def get_system_info(self) -> Dict:
        """
        Ottiene informazioni sul sistema.
        
        Returns:
            Dizionario con info sistema
        """
        return {
            'platform': platform.platform(),
            'system': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'python_version': sys.version
        }
