"""
Test per i convertitori di DocConverter
"""
import unittest
import tempfile
from pathlib import Path
import sys

# Aggiungi parent directory al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from converters.word_to_pdf import WordToPDFConverter
from core.converter_registry import ConverterRegistry


class TestWordToPDFConverter(unittest.TestCase):
    """Test per il convertitore Word → PDF"""
    
    def setUp(self):
        """Setup per ogni test"""
        self.converter = WordToPDFConverter()
    
    def test_get_info(self):
        """Test informazioni convertitore"""
        info = self.converter.get_info()
        
        self.assertEqual(info['name'], 'Word to PDF')
        self.assertIn('.doc', info['input_formats'])
        self.assertIn('.docx', info['input_formats'])
        self.assertEqual(info['output_format'], '.pdf')
        # Aggiornato: ora usa solo Python, no dipendenze esterne
        self.assertIsNone(info['requires_dep'])
    
    def test_validate_input_nonexistent(self):
        """Test validazione file inesistente"""
        result = self.converter.validate_input('nonexistent_file.docx')
        self.assertFalse(result)
    
    def test_get_supported_extensions(self):
        """Test estensioni supportate"""
        extensions = self.converter.get_supported_extensions()
        self.assertIn('.doc', extensions)
        self.assertIn('.docx', extensions)
    
    def test_get_output_extension(self):
        """Test estensione output"""
        ext = self.converter.get_output_extension()
        self.assertEqual(ext, '.pdf')


class TestConverterRegistry(unittest.TestCase):
    """Test per il registry dei convertitori"""
    
    def setUp(self):
        """Setup per ogni test"""
        self.registry = ConverterRegistry()
    
    def test_register_converter(self):
        """Test registrazione convertitore"""
        initial_count = len(self.registry)
        self.registry.register(WordToPDFConverter)
        self.assertEqual(len(self.registry), initial_count + 1)
    
    def test_get_converter(self):
        """Test recupero convertitore per nome"""
        self.registry.register(WordToPDFConverter)
        converter = self.registry.get_converter('Word to PDF')
        self.assertIsNotNone(converter)
        self.assertIsInstance(converter, WordToPDFConverter)
    
    def test_is_format_supported(self):
        """Test verifica formato supportato"""
        self.registry.register(WordToPDFConverter)
        self.assertTrue(self.registry.is_format_supported('.docx'))
        self.assertTrue(self.registry.is_format_supported('.doc'))
        self.assertFalse(self.registry.is_format_supported('.xyz'))
    
    def test_get_supported_input_formats(self):
        """Test lista formati supportati"""
        self.registry.register(WordToPDFConverter)
        formats = self.registry.get_supported_input_formats()
        self.assertIn('.doc', formats)
        self.assertIn('.docx', formats)


if __name__ == '__main__':
    unittest.main()
