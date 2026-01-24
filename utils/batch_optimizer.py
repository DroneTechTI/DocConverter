"""
Batch Optimizer - Ottimizza conversioni multiple
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Callable, Tuple, Any
from pathlib import Path
import psutil

from .logger import get_logger


class BatchOptimizer:
    """
    Ottimizza l'esecuzione di conversioni batch
    """
    
    def __init__(self, max_workers: int = None):
        """
        Inizializza batch optimizer
        
        Args:
            max_workers: Numero massimo worker paralleli (auto se None)
        """
        self.logger = get_logger("BatchOptimizer")
        
        # Determina numero ottimale di worker basato su CPU e memoria
        if max_workers is None:
            cpu_count = psutil.cpu_count(logical=True)
            available_memory_gb = psutil.virtual_memory().available / (1024**3)
            
            # Usa 2 thread per core, ma limita in base a memoria disponibile
            max_workers = min(cpu_count * 2, int(available_memory_gb / 0.5))
            max_workers = max(1, min(max_workers, 8))  # Min 1, max 8
        
        self.max_workers = max_workers
        self.logger.info(f"Batch optimizer: {max_workers} worker paralleli")
    
    def process_batch(
        self,
        items: List[Any],
        process_func: Callable,
        progress_callback: Callable = None
    ) -> List[Tuple[Any, bool, str]]:
        """
        Processa batch di item in parallelo
        
        Args:
            items: Lista di item da processare
            process_func: Funzione che processa singolo item
            progress_callback: Callback per progresso
            
        Returns:
            Lista di (item, success, message)
        """
        results = []
        total = len(items)
        completed = 0
        
        self.logger.info(f"Inizio batch processing: {total} item")
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Sottometti tutti i task
            future_to_item = {
                executor.submit(process_func, item): item
                for item in items
            }
            
            # Processa risultati man mano che completano
            for future in as_completed(future_to_item):
                item = future_to_item[future]
                completed += 1
                
                try:
                    success, message = future.result()
                    results.append((item, success, message))
                    
                    if progress_callback:
                        progress = int((completed / total) * 100)
                        progress_callback(progress, f"Processati {completed}/{total}")
                
                except Exception as e:
                    self.logger.error(f"Errore processing {item}: {e}")
                    results.append((item, False, str(e)))
        
        successes = sum(1 for _, success, _ in results if success)
        self.logger.info(f"Batch completato: {successes}/{total} successi")
        
        return results
    
    def get_optimal_chunk_size(self, total_items: int, item_size_mb: float = 1.0) -> int:
        """
        Calcola dimensione ottimale chunk per batch processing
        
        Args:
            total_items: Numero totale item
            item_size_mb: Dimensione media item in MB
            
        Returns:
            Dimensione chunk ottimale
        """
        available_memory_gb = psutil.virtual_memory().available / (1024**3)
        
        # Usa max 25% della memoria disponibile
        max_memory_usage_gb = available_memory_gb * 0.25
        
        # Calcola quanti item possiamo tenere in memoria
        chunk_size = int((max_memory_usage_gb * 1024) / item_size_mb)
        
        # Limiti ragionevoli
        chunk_size = max(1, min(chunk_size, total_items, 100))
        
        self.logger.debug(f"Chunk size ottimale: {chunk_size} (memoria: {available_memory_gb:.1f}GB)")
        
        return chunk_size
    
    def should_use_parallel(self, num_items: int, min_items: int = 3) -> bool:
        """
        Determina se usare processing parallelo
        
        Args:
            num_items: Numero di item da processare
            min_items: Minimo item per parallelizzazione
            
        Returns:
            True se conviene parallelizzare
        """
        return num_items >= min_items and self.max_workers > 1


# Istanza globale
_batch_optimizer = None


def get_batch_optimizer() -> BatchOptimizer:
    """
    Ottiene istanza globale del batch optimizer
    
    Returns:
        Istanza singleton di BatchOptimizer
    """
    global _batch_optimizer
    if _batch_optimizer is None:
        _batch_optimizer = BatchOptimizer()
    return _batch_optimizer
