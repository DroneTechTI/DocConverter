"""
Cache Manager per ottimizzare performance
"""
import hashlib
import pickle
from pathlib import Path
from typing import Any, Optional
from datetime import datetime, timedelta

from .logger import get_logger


class CacheManager:
    """
    Gestisce cache per file e risultati di conversioni
    """
    
    def __init__(self, cache_dir: Optional[Path] = None, ttl_hours: int = 24):
        """
        Inizializza il cache manager
        
        Args:
            cache_dir: Directory per cache (default: .cache)
            ttl_hours: Time-to-live in ore per cache
        """
        self.logger = get_logger("CacheManager")
        self.cache_dir = cache_dir or Path.home() / ".docconverter" / "cache"
        self.ttl = timedelta(hours=ttl_hours)
        
        # Crea directory cache se non esiste
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Cache in memoria per accesso veloce
        self._memory_cache = {}
    
    def _get_cache_key(self, file_path: str, operation: str = "convert") -> str:
        """
        Genera chiave cache univoca per file e operazione
        
        Args:
            file_path: Path del file
            operation: Tipo di operazione
            
        Returns:
            Chiave cache (hash)
        """
        file_path_obj = Path(file_path)
        
        # Usa: path + mtime + size per cache key
        if file_path_obj.exists():
            stat = file_path_obj.stat()
            cache_string = f"{file_path}:{stat.st_mtime}:{stat.st_size}:{operation}"
        else:
            cache_string = f"{file_path}:{operation}"
        
        return hashlib.md5(cache_string.encode()).hexdigest()
    
    def get(self, file_path: str, operation: str = "convert") -> Optional[Any]:
        """
        Recupera valore dalla cache
        
        Args:
            file_path: Path del file
            operation: Tipo di operazione
            
        Returns:
            Valore cached o None
        """
        cache_key = self._get_cache_key(file_path, operation)
        
        # Controlla memoria
        if cache_key in self._memory_cache:
            cached_data, timestamp = self._memory_cache[cache_key]
            if datetime.now() - timestamp < self.ttl:
                self.logger.debug(f"Cache hit (memory): {cache_key}")
                return cached_data
            else:
                # Cache scaduta
                del self._memory_cache[cache_key]
        
        # Controlla disco
        cache_file = self.cache_dir / f"{cache_key}.cache"
        if cache_file.exists():
            try:
                with open(cache_file, 'rb') as f:
                    cached_data, timestamp = pickle.load(f)
                
                if datetime.now() - timestamp < self.ttl:
                    # Carica in memoria per accesso futuro
                    self._memory_cache[cache_key] = (cached_data, timestamp)
                    self.logger.debug(f"Cache hit (disk): {cache_key}")
                    return cached_data
                else:
                    # Cache scaduta, rimuovi
                    cache_file.unlink()
            
            except Exception as e:
                self.logger.warning(f"Errore lettura cache: {e}")
        
        return None
    
    def set(self, file_path: str, value: Any, operation: str = "convert"):
        """
        Salva valore in cache
        
        Args:
            file_path: Path del file
            value: Valore da cachare
            operation: Tipo di operazione
        """
        cache_key = self._get_cache_key(file_path, operation)
        timestamp = datetime.now()
        
        # Salva in memoria
        self._memory_cache[cache_key] = (value, timestamp)
        
        # Salva su disco
        cache_file = self.cache_dir / f"{cache_key}.cache"
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump((value, timestamp), f)
            
            self.logger.debug(f"Cached: {cache_key}")
        
        except Exception as e:
            self.logger.warning(f"Errore salvataggio cache: {e}")
    
    def clear(self):
        """Pulisce tutta la cache"""
        # Pulisci memoria
        self._memory_cache.clear()
        
        # Pulisci disco
        for cache_file in self.cache_dir.glob("*.cache"):
            try:
                cache_file.unlink()
            except Exception as e:
                self.logger.warning(f"Errore eliminazione cache {cache_file}: {e}")
        
        self.logger.info("Cache pulita")
    
    def clear_expired(self):
        """Rimuove cache scadute"""
        now = datetime.now()
        removed = 0
        
        # Pulisci memoria
        expired_keys = [
            key for key, (_, timestamp) in self._memory_cache.items()
            if now - timestamp >= self.ttl
        ]
        for key in expired_keys:
            del self._memory_cache[key]
            removed += 1
        
        # Pulisci disco
        for cache_file in self.cache_dir.glob("*.cache"):
            try:
                with open(cache_file, 'rb') as f:
                    _, timestamp = pickle.load(f)
                
                if now - timestamp >= self.ttl:
                    cache_file.unlink()
                    removed += 1
            
            except Exception:
                pass
        
        if removed > 0:
            self.logger.info(f"Rimossi {removed} elementi cache scaduti")
    
    def get_stats(self) -> dict:
        """
        Ottieni statistiche cache
        
        Returns:
            Dizionario con statistiche
        """
        disk_files = list(self.cache_dir.glob("*.cache"))
        total_size = sum(f.stat().st_size for f in disk_files)
        
        return {
            'memory_items': len(self._memory_cache),
            'disk_items': len(disk_files),
            'total_size_mb': total_size / (1024 * 1024),
            'cache_dir': str(self.cache_dir)
        }


# Istanza globale
_cache_manager = None


def get_cache_manager() -> CacheManager:
    """
    Ottiene istanza globale del cache manager
    
    Returns:
        Istanza singleton di CacheManager
    """
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = CacheManager()
    return _cache_manager
