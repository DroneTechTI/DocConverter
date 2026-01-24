"""
Excel to PDF Converter.

Converts Excel spreadsheets to PDF format using Excel (Windows) or LibreOffice (Linux/macOS).
"""
import platform
from pathlib import Path
from typing import Optional, Callable, Any

from core.converter_base import ConverterBase
from utils.error_handler import ConversionError


class ExcelToPDFConverter(ConverterBase):
    """
    Excel to PDF converter.
    
    Windows: Uses installed Excel (if available)
    Linux/macOS: Uses LibreOffice
    """
    
    def __init__(self) -> None:
        """Initialize Excel to PDF converter."""
        super().__init__()
        self._system = platform.system().lower()
        self._excel_available_cache: Optional[bool] = None  # Cache Excel detection
        self._excel_version: Optional[str] = None  # Save Excel version
    
    def get_info(self) -> dict:
        """Return converter metadata."""
        if 'windows' in self._system:
            requires_dep = None  # Excel/LibreOffice already on system
        else:
            requires_dep = 'libreoffice'
        
        return {
            'name': 'Excel to PDF',
            'input_formats': ['.xlsx', '.xls'],
            'output_format': '.pdf',
            'description': 'Converts Excel spreadsheets to PDF format',
            'requires_dependency': requires_dep
        }
    
    def convert(
        self,
        input_path: str,
        output_path: str,
        progress_callback: Optional[Callable[[int, str], None]] = None,
        **kwargs
    ) -> bool:
        """
        Converte un foglio Excel in PDF.
        
        Args:
            input_path: Path del file Excel da convertire
            output_path: Path del file PDF di output
            progress_callback: Callback per aggiornamenti progresso
            **kwargs: Parametri aggiuntivi
        
        Returns:
            True se conversione riuscita
        
        Raises:
            ConversionError: In caso di errore durante la conversione
        """
        self.logger.info(f"Starting Excel→PDF conversion: {input_path}")
        
        try:
            # Validate input
            self._report_progress(progress_callback, 5, "Validating file...")
            if not self.validate_input(input_path):
                raise ConversionError(
                    "File di input non valido",
                    file_path=input_path
                )
            
            # Prepara path
            input_file = Path(input_path).resolve()
            output_file = Path(output_path).resolve()
            output_dir = output_file.parent
            
            # Assicura che la directory di output esista
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Prova Excel su Windows
            if 'windows' in self._system:
                self._report_progress(progress_callback, 30, "Conversione con Excel...")
                try:
                    success = self._convert_with_excel(input_file, output_file)
                    if success:
                        self._report_progress(progress_callback, 100, "Completed!")
                        return True
                except:
                    self.logger.warning("Excel non disponibile, provo LibreOffice")
            
            # Fallback LibreOffice
            self._report_progress(progress_callback, 30, "Conversione con LibreOffice...")
            success = self._convert_with_libreoffice(input_file, output_file)
            
            if success:
                self._report_progress(progress_callback, 100, "Completato!")
                self.logger.info(f"Conversione completata: {output_file}")
                return True
            else:
                raise ConversionError("Conversione fallita", file_path=input_path)
        
        except ConversionError:
            raise
        
        except Exception as e:
            self.logger.error(f"Excel→PDF conversion error: {e}", exc_info=True)
            raise ConversionError(
                f"Conversion error: {str(e)}",
                file_path=input_path,
                details=str(e)
            )
    
    def _is_excel_available(self) -> bool:
        """
        Verifica se Microsoft Excel è installato e accessibile.
        Ricerca SPECIFICA per Excel (non Office generico).
        USA CACHE per evitare rilevamenti multipli (VELOCE!).
        
        Returns:
            True se Excel è disponibile
        """
        # ⚡ USA CACHE - Non rilevare ogni volta!
        if self._excel_available_cache is not None:
            return self._excel_available_cache
        
        if 'windows' not in self._system:
            self._excel_available_cache = False
            return False
        
        try:
            import win32com.client
            import pythoncom
            
            pythoncom.CoInitialize()
            
            try:
                self.logger.info("🔍 Ricerca Microsoft Excel (non Office generico)...")
                excel = win32com.client.DispatchEx("Excel.Application")
                
                # Verifica che sia davvero Excel
                version = excel.Version
                app_name = excel.Name if hasattr(excel, 'Name') else "Microsoft Excel"
                
                # ⚡ SALVA IN CACHE
                self._excel_version = version
                self._excel_available_cache = True
                
                excel.Quit()
                
                self.logger.info(f"✅ {app_name} rilevato: versione {version}")
                self.logger.info(f"   → Excel SPECIFICO trovato e pronto all'uso!")
                return True
            
            finally:
                pythoncom.CoUninitialize()
        
        except Exception as e:
            self.logger.warning(f"❌ Microsoft Excel NON trovato: {e}")
            self.logger.info("   → Cerca solo Excel, non Office generico")
            self._excel_available_cache = False
            return False
    
    def _convert_with_excel(self, input_file: Path, output_file: Path) -> bool:
        """⚡ Conversione VELOCE con Excel (usa cache rilevamento)"""
        try:
            # Usa cache - NON verifica ogni volta!
            if not self._is_excel_available():
                self.logger.warning("Excel non rilevato su questo sistema")
                return False
            
            import win32com.client
            import pythoncom
            
            pythoncom.CoInitialize()
            
            try:
                self.logger.info(f"⚡ Conversione VELOCE con Excel: {input_file.name}")
                excel = win32com.client.DispatchEx("Excel.Application")
                excel.Visible = False
                excel.DisplayAlerts = False
                
                try:
                    wb = excel.Workbooks.Open(str(input_file.absolute()))
                    wb.ExportAsFixedFormat(0, str(output_file.absolute()))
                    wb.Close(False)
                    
                    self.logger.info("✅ Conversione Excel completata VELOCEMENTE!")
                    return True
                finally:
                    excel.Quit()
            
            finally:
                pythoncom.CoUninitialize()
        
        except Exception as e:
            self.logger.error(f"Excel error: {e}")
            return False
    
    def _convert_with_libreoffice(self, input_file: Path, output_file: Path) -> bool:
        """Convert using LibreOffice."""
        import subprocess
        import tempfile
        import shutil
        
        try:
            from core.dependency_checker import DependencyChecker
            checker = DependencyChecker()
            is_available, path = checker.check_dependency('libreoffice')
            
            if not is_available:
                raise ConversionError("LibreOffice not found")
            
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_output_dir = Path(temp_dir)
                
                cmd = [
                    path,
                    '--headless',
                    '--convert-to', 'pdf',
                    '--outdir', str(temp_output_dir),
                    str(input_file)
                ]
                
                result = subprocess.run(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=60,
                    text=True,
                    check=False
                )
                
                if result.returncode != 0:
                    return False
                
                expected_pdf = temp_output_dir / f"{input_file.stem}.pdf"
                if expected_pdf.exists():
                    shutil.move(str(expected_pdf), str(output_file))
                    return True
                
                return False
        
        except Exception as e:
            self.logger.error(f"LibreOffice error: {e}")
            return False
