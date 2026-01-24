"""
Gestione file e path per DocConverter
"""
import os
import shutil
from pathlib import Path
from typing import List, Optional, Tuple

from config.settings import Settings
from .logger import get_logger
from .error_handler import FileAccessError


class FileHandler:
    """Gestisce operazioni sui file in modo sicuro"""
    
    def __init__(self):
        self.logger = get_logger("FileHandler")
    
    def validate_file(self, file_path: str) -> Tuple[bool, Optional[str]]:
        """
        Valida un file di input
        
        Args:
            file_path: Path del file da validare
        
        Returns:
            Tupla (is_valid, error_message)
        """
        path = Path(file_path)
        
        # Verifica esistenza
        if not path.exists():
            return False, f"File non trovato: {file_path}"
        
        # Verifica che sia un file
        if not path.is_file():
            return False, f"Il path non è un file: {file_path}"
        
        # Verifica dimensione
        size = path.stat().st_size
        if size > Settings.MAX_FILE_SIZE:
            size_mb = size / (1024 * 1024)
            max_mb = Settings.MAX_FILE_SIZE / (1024 * 1024)
            return False, f"File troppo grande: {size_mb:.1f}MB (max {max_mb:.0f}MB)"
        
        if size == 0:
            return False, "File vuoto"
        
        # Verifica leggibilità
        if not os.access(path, os.R_OK):
            return False, f"File non leggibile (permessi insufficienti)"
        
        return True, None
    
    def validate_output_path(self, output_path: str) -> Tuple[bool, Optional[str]]:
        """
        Valida un path di output
        
        Args:
            output_path: Path di output da validare
        
        Returns:
            Tupla (is_valid, error_message)
        """
        path = Path(output_path)
        
        # Verifica directory
        if not path.parent.exists():
            try:
                path.parent.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                return False, f"Impossibile creare directory: {e}"
        
        # Verifica scrivibilità directory
        if not os.access(path.parent, os.W_OK):
            return False, f"Directory non scrivibile: {path.parent}"
        
        # Se file esiste già, verifica sovrascrivibilità
        if path.exists():
            if not os.access(path, os.W_OK):
                return False, f"File esistente non sovrascrivibile: {path}"
        
        return True, None
    
    def get_file_extension(self, file_path: str) -> str:
        """
        Ottiene l'estensione del file (lowercase, con punto)
        
        Args:
            file_path: Path del file
        
        Returns:
            Estensione (es. '.docx')
        """
        return Path(file_path).suffix.lower()
    
    def is_supported_format(self, file_path: str) -> bool:
        """
        Verifica se il formato del file è supportato
        
        Args:
            file_path: Path del file
        
        Returns:
            True se supportato
        """
        ext = self.get_file_extension(file_path)
        return ext in Settings.get_all_supported_extensions()
    
    def generate_output_path(
        self,
        input_path: str,
        output_dir: str = None,
        output_extension: str = '.pdf',
        suffix: str = None
    ) -> str:
        """
        Genera il path di output per un file
        
        Args:
            input_path: Path del file di input
            output_dir: Directory di output (None = stessa del file input)
            output_extension: Estensione del file output (default: .pdf)
            suffix: Suffisso da aggiungere al nome (es. '_converted')
        
        Returns:
            Path completo del file di output
        """
        input_file = Path(input_path)
        
        # Determina directory output
        if output_dir:
            out_dir = Path(output_dir)
        else:
            out_dir = input_file.parent
        
        # Costruisci nome file
        base_name = input_file.stem
        if suffix:
            base_name += suffix
        
        output_file = out_dir / f"{base_name}{output_extension}"
        
        # Gestisci conflitti di nome
        counter = 1
        while output_file.exists():
            output_file = out_dir / f"{base_name}_{counter}{output_extension}"
            counter += 1
        
        return str(output_file)
    
    def safe_delete(self, file_path: str) -> bool:
        """
        Elimina un file in modo sicuro
        
        Args:
            file_path: Path del file da eliminare
        
        Returns:
            True se eliminato con successo
        """
        try:
            path = Path(file_path)
            if path.exists() and path.is_file():
                path.unlink()
                self.logger.info(f"File eliminato: {file_path}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Errore eliminazione file {file_path}: {e}")
            return False
    
    def safe_copy(self, source: str, destination: str) -> bool:
        """
        Copia un file in modo sicuro
        
        Args:
            source: Path file sorgente
            destination: Path destinazione
        
        Returns:
            True se copiato con successo
        """
        try:
            shutil.copy2(source, destination)
            self.logger.info(f"File copiato: {source} -> {destination}")
            return True
        except Exception as e:
            self.logger.error(f"Errore copia file: {e}")
            raise FileAccessError(f"Impossibile copiare il file: {e}")
    
    def get_file_info(self, file_path: str) -> dict:
        """
        Ottiene informazioni su un file
        
        Args:
            file_path: Path del file
        
        Returns:
            Dizionario con informazioni
        """
        path = Path(file_path)
        
        if not path.exists():
            return None
        
        stat = path.stat()
        
        return {
            'name': path.name,
            'extension': path.suffix.lower(),
            'size': stat.st_size,
            'size_mb': stat.st_size / (1024 * 1024),
            'modified': stat.st_mtime,
            'path': str(path.absolute()),
            'directory': str(path.parent.absolute())
        }
    
    def filter_files_by_extensions(
        self,
        files: List[str],
        extensions: List[str]
    ) -> List[str]:
        """
        Filtra una lista di file per estensioni
        
        Args:
            files: Lista di path
            extensions: Lista di estensioni (es. ['.doc', '.docx'])
        
        Returns:
            Lista di file filtrati
        """
        filtered = []
        for file_path in files:
            if self.get_file_extension(file_path) in extensions:
                filtered.append(file_path)
        
        return filtered
