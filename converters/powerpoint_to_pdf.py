"""
Convertitore PowerPoint → PDF
Supporta formati: .pptx, .ppt → .pdf
"""
import platform
from pathlib import Path
from typing import Optional, Callable

from core.converter_base import ConverterBase
from utils.error_handler import ConversionError


class PowerPointToPDFConverter(ConverterBase):
    """
    Convertitore da PowerPoint a PDF.
    
    Windows: Usa PowerPoint installato (se disponibile)
    Linux/macOS: Usa LibreOffice
    """
    
    def __init__(self):
        """Inizializza il convertitore PowerPoint → PDF"""
        super().__init__()
        self._system = platform.system().lower()
        self._powerpoint_available_cache = None  # Cache rilevamento PowerPoint
        self._powerpoint_version = None  # Salva versione PowerPoint
    
    def get_info(self) -> dict:
        """Ritorna informazioni sul convertitore"""
        if 'windows' in self._system:
            requires_dep = None  # PowerPoint/LibreOffice già su sistema
        else:
            requires_dep = 'libreoffice'
        
        return {
            'name': 'PowerPoint to PDF',
            'input_formats': ['.pptx', '.ppt'],
            'output_format': '.pdf',
            'description': 'Converte presentazioni PowerPoint in formato PDF',
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
        Converte una presentazione PowerPoint in PDF.
        
        Args:
            input_path: Path del file PowerPoint da convertire
            output_path: Path del file PDF di output
            progress_callback: Callback per aggiornamenti progresso
            **kwargs: Parametri aggiuntivi
        
        Returns:
            True se conversione riuscita
        
        Raises:
            ConversionError: In caso di errore durante la conversione
        """
        self.logger.info(f"Inizio conversione PowerPoint→PDF: {input_path}")
        
        try:
            # Validazione input
            self._report_progress(progress_callback, 5, "Validazione file...")
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
            
            # Prova PowerPoint su Windows
            if 'windows' in self._system:
                self._report_progress(progress_callback, 30, "Conversione con PowerPoint...")
                try:
                    success = self._convert_with_powerpoint(input_file, output_file)
                    if success:
                        self._report_progress(progress_callback, 100, "Completato!")
                        return True
                except:
                    self.logger.warning("PowerPoint non disponibile, provo LibreOffice")
            
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
            self.logger.error(f"Errore conversione PowerPoint→PDF: {e}", exc_info=True)
            raise ConversionError(
                f"Errore conversione: {str(e)}",
                file_path=input_path,
                details=str(e)
            )
    
    def _is_powerpoint_available(self) -> bool:
        """
        Verifica se Microsoft PowerPoint è installato e accessibile.
        Ricerca SPECIFICA per PowerPoint (non Office generico).
        USA CACHE per evitare rilevamenti multipli (VELOCE!).
        
        Returns:
            True se PowerPoint è disponibile
        """
        # ⚡ USA CACHE - Non rilevare ogni volta!
        if self._powerpoint_available_cache is not None:
            return self._powerpoint_available_cache
        
        if 'windows' not in self._system:
            self._powerpoint_available_cache = False
            return False
        
        try:
            import win32com.client
            import pythoncom
            
            pythoncom.CoInitialize()
            
            try:
                self.logger.info("🔍 Ricerca Microsoft PowerPoint (non Office generico)...")
                powerpoint = win32com.client.DispatchEx("PowerPoint.Application")
                
                # Verifica che sia davvero PowerPoint
                version = powerpoint.Version
                app_name = powerpoint.Name if hasattr(powerpoint, 'Name') else "Microsoft PowerPoint"
                
                # ⚡ SALVA IN CACHE
                self._powerpoint_version = version
                self._powerpoint_available_cache = True
                
                powerpoint.Quit()
                
                self.logger.info(f"✅ {app_name} rilevato: versione {version}")
                self.logger.info(f"   → PowerPoint SPECIFICO trovato e pronto all'uso!")
                return True
            
            finally:
                pythoncom.CoUninitialize()
        
        except Exception as e:
            self.logger.warning(f"❌ Microsoft PowerPoint NON trovato: {e}")
            self.logger.info("   → Cerca solo PowerPoint, non Office generico")
            self._powerpoint_available_cache = False
            return False
    
    def _convert_with_powerpoint(self, input_file: Path, output_file: Path) -> bool:
        """⚡ Conversione VELOCE con PowerPoint (usa cache rilevamento)"""
        try:
            # Usa cache - NON verifica ogni volta!
            if not self._is_powerpoint_available():
                self.logger.warning("PowerPoint non rilevato su questo sistema")
                return False
            
            import win32com.client
            import pythoncom
            
            pythoncom.CoInitialize()
            
            try:
                self.logger.info(f"⚡ Conversione VELOCE con PowerPoint: {input_file.name}")
                powerpoint = win32com.client.DispatchEx("PowerPoint.Application")
                powerpoint.Visible = 1  # PowerPoint needs to be visible
                
                try:
                    presentation = powerpoint.Presentations.Open(str(input_file.absolute()), WithWindow=False)
                    presentation.SaveAs(str(output_file.absolute()), 32)  # 32 = ppSaveAsPDF
                    presentation.Close()
                    
                    self.logger.info("✅ Conversione PowerPoint completata VELOCEMENTE!")
                    return True
                finally:
                    powerpoint.Quit()
            
            finally:
                pythoncom.CoUninitialize()
        
        except Exception as e:
            self.logger.error(f"Errore PowerPoint: {e}")
            return False
    
    def _convert_with_libreoffice(self, input_file: Path, output_file: Path) -> bool:
        """Conversione con LibreOffice"""
        import subprocess
        import tempfile
        import shutil
        
        try:
            from core.dependency_checker import DependencyChecker
            checker = DependencyChecker()
            is_available, path = checker.check_dependency('libreoffice')
            
            if not is_available:
                raise ConversionError("LibreOffice non trovato")
            
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
                    timeout=120,  # PowerPoint può richiedere più tempo
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
            self.logger.error(f"Errore LibreOffice: {e}")
            return False
