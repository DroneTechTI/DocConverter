"""
Memory Optimizer - Gestisce utilizzo memoria
"""
import gc
import psutil
from typing import Optional
from contextlib import contextmanager

from .logger import get_logger


class MemoryOptimizer:
    """
    Ottimizza l'utilizzo della memoria durante le conversioni
    """
    
    def __init__(self, max_memory_percent: float = 80.0):
        """
        Inizializza memory optimizer
        
        Args:
            max_memory_percent: Percentuale massima memoria utilizzabile
        """
        self.logger = get_logger("MemoryOptimizer")
        self.max_memory_percent = max_memory_percent
        self.process = psutil.Process()
    
    def get_memory_usage(self) -> dict:
        """
        Ottiene statistiche utilizzo memoria
        
        Returns:
            Dizionario con info memoria
        """
        mem_info = self.process.memory_info()
        sys_mem = psutil.virtual_memory()
        
        return {
            'rss_mb': mem_info.rss / (1024 ** 2),  # Resident Set Size
            'vms_mb': mem_info.vms / (1024 ** 2),  # Virtual Memory Size
            'percent': self.process.memory_percent(),
            'system_available_mb': sys_mem.available / (1024 ** 2),
            'system_percent': sys_mem.percent
        }
    
    def check_memory_pressure(self) -> bool:
        """
        Verifica se c'è pressione sulla memoria
        
        Returns:
            True se memoria sotto pressione
        """
        mem_info = self.get_memory_usage()
        
        # Pressione se:
        # - Processo usa > max_memory_percent della memoria totale
        # - Sistema ha < 500MB disponibili
        is_pressure = (
            mem_info['percent'] > self.max_memory_percent or
            mem_info['system_available_mb'] < 500
        )
        
        if is_pressure:
            self.logger.warning(
                f"Pressione memoria: processo={mem_info['percent']:.1f}%, "
                f"disponibile={mem_info['system_available_mb']:.0f}MB"
            )
        
        return is_pressure
    
    def optimize_memory(self, aggressive: bool = False):
        """
        Ottimizza utilizzo memoria
        
        Args:
            aggressive: Se True, forza garbage collection aggressiva
        """
        before = self.get_memory_usage()
        
        # Garbage collection
        if aggressive:
            # GC aggressivo
            for _ in range(3):
                gc.collect()
        else:
            gc.collect()
        
        after = self.get_memory_usage()
        freed_mb = before['rss_mb'] - after['rss_mb']
        
        if freed_mb > 0:
            self.logger.info(f"Memoria liberata: {freed_mb:.1f} MB")
        
        return freed_mb
    
    def get_recommended_batch_size(self, item_size_mb: float = 5.0) -> int:
        """
        Calcola batch size raccomandato basato su memoria disponibile
        
        Args:
            item_size_mb: Dimensione media item in MB
            
        Returns:
            Batch size raccomandato
        """
        mem_info = self.get_memory_usage()
        available_mb = mem_info['system_available_mb']
        
        # Usa max 50% della memoria disponibile
        usable_mb = available_mb * 0.5
        batch_size = int(usable_mb / item_size_mb)
        
        # Limiti: min 1, max 50
        batch_size = max(1, min(batch_size, 50))
        
        return batch_size
    
    @contextmanager
    def memory_guard(self, cleanup_callback=None):
        """
        Context manager per monitorare memoria durante operazioni
        
        Args:
            cleanup_callback: Funzione da chiamare se pressione memoria
        """
        before = self.get_memory_usage()
        self.logger.debug(f"Memoria prima: {before['rss_mb']:.1f} MB")
        
        try:
            yield self
        
        finally:
            # Verifica memoria dopo operazione
            if self.check_memory_pressure():
                self.logger.warning("Pressione memoria rilevata, cleanup...")
                
                if cleanup_callback:
                    cleanup_callback()
                
                self.optimize_memory(aggressive=True)
            else:
                # GC normale
                self.optimize_memory(aggressive=False)
            
            after = self.get_memory_usage()
            self.logger.debug(f"Memoria dopo: {after['rss_mb']:.1f} MB")
    
    def log_memory_stats(self):
        """Log statistiche memoria dettagliate"""
        mem_info = self.get_memory_usage()
        
        self.logger.info(
            f"Memoria processo: {mem_info['rss_mb']:.1f} MB "
            f"({mem_info['percent']:.1f}%)"
        )
        self.logger.info(
            f"Memoria sistema: {mem_info['system_percent']:.1f}% usata, "
            f"{mem_info['system_available_mb']:.0f} MB disponibili"
        )


# Istanza globale
_memory_optimizer = None


def get_memory_optimizer() -> MemoryOptimizer:
    """
    Ottiene istanza globale del memory optimizer
    
    Returns:
        Istanza singleton di MemoryOptimizer
    """
    global _memory_optimizer
    if _memory_optimizer is None:
        _memory_optimizer = MemoryOptimizer()
    return _memory_optimizer
