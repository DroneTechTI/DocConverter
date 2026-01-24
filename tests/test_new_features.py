"""
Test per nuove funzionalità PDF (merge, compress)
"""
import unittest
import tempfile
from pathlib import Path
import sys

# Aggiungi parent directory al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from converters.pdf_merge import PDFMergeConverter
from converters.pdf_compress import PDFCompressConverter


class TestPDFMergeConverter(unittest.TestCase):
    """Test per il convertitore PDF Merge"""
    
    def setUp(self):
        """Setup per ogni test"""
        self.converter = PDFMergeConverter()
    
    def test_get_info(self):
        """Test informazioni convertitore"""
        info = self.converter.get_info()
        
        self.assertEqual(info['name'], 'PDF Merge')
        self.assertIn('.pdf', info['input_formats'])
        self.assertEqual(info['output_format'], '.pdf')
        self.assertIsNone(info['requires_dep'])
    
    def test_get_supported_extensions(self):
        """Test estensioni supportate"""
        extensions = self.converter.get_supported_extensions()
        self.assertIn('.pdf', extensions)
    
    def test_get_output_extension(self):
        """Test estensione output"""
        ext = self.converter.get_output_extension()
        self.assertEqual(ext, '.pdf')


class TestPDFCompressConverter(unittest.TestCase):
    """Test per il convertitore PDF Compress"""
    
    def setUp(self):
        """Setup per ogni test"""
        self.converter = PDFCompressConverter()
    
    def test_get_info(self):
        """Test informazioni convertitore"""
        info = self.converter.get_info()
        
        self.assertEqual(info['name'], 'PDF Compress')
        self.assertIn('.pdf', info['input_formats'])
        self.assertEqual(info['output_format'], '.pdf')
        self.assertIsNone(info['requires_dep'])
    
    def test_validate_input_nonexistent(self):
        """Test validazione file inesistente"""
        result = self.converter.validate_input('nonexistent_file.pdf')
        self.assertFalse(result)
    
    def test_get_supported_extensions(self):
        """Test estensioni supportate"""
        extensions = self.converter.get_supported_extensions()
        self.assertIn('.pdf', extensions)
    
    def test_get_output_extension(self):
        """Test estensione output"""
        ext = self.converter.get_output_extension()
        self.assertEqual(ext, '.pdf')


class TestOptimizationModules(unittest.TestCase):
    """Test per moduli di ottimizzazione"""
    
    def test_memory_optimizer_import(self):
        """Test import memory optimizer"""
        from utils.memory_optimizer import get_memory_optimizer
        optimizer = get_memory_optimizer()
        self.assertIsNotNone(optimizer)
    
    def test_batch_optimizer_import(self):
        """Test import batch optimizer"""
        from utils.batch_optimizer import get_batch_optimizer
        optimizer = get_batch_optimizer()
        self.assertIsNotNone(optimizer)
    
    def test_cache_manager_import(self):
        """Test import cache manager"""
        from utils.cache_manager import get_cache_manager
        manager = get_cache_manager()
        self.assertIsNotNone(manager)
    
    def test_memory_optimizer_stats(self):
        """Test statistiche memoria"""
        from utils.memory_optimizer import get_memory_optimizer
        optimizer = get_memory_optimizer()
        stats = optimizer.get_memory_usage()
        
        self.assertIn('rss_mb', stats)
        self.assertIn('percent', stats)
        self.assertGreater(stats['rss_mb'], 0)
    
    def test_cache_manager_stats(self):
        """Test statistiche cache"""
        from utils.cache_manager import get_cache_manager
        manager = get_cache_manager()
        stats = manager.get_stats()
        
        self.assertIn('memory_items', stats)
        self.assertIn('disk_items', stats)
        self.assertGreaterEqual(stats['memory_items'], 0)


if __name__ == '__main__':
    unittest.main()
