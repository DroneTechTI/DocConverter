"""
Installer automatico LibreOffice portatile per Windows
"""
import os
import sys
import platform
import subprocess
import urllib.request
from pathlib import Path
from zipfile import ZipFile
import tempfile

from utils.logger import get_logger


class LibreOfficeInstaller:
    """Installa LibreOffice portatile automaticamente"""
    
    def __init__(self):
        self.logger = get_logger("LibreOfficeInstaller")
        self.system = platform.system().lower()
        self.base_dir = Path(__file__).parent.parent
        self.portable_dir = self.base_dir / "LibreOfficePortable"
    
    def is_installed(self) -> bool:
        """Verifica se LibreOffice portatile è già installato"""
        if 'windows' not in self.system:
            return False
        
        soffice_path = self.portable_dir / "App" / "libreoffice" / "program" / "soffice.exe"
        return soffice_path.exists()
    
    def get_path(self) -> str:
        """Ritorna il path di LibreOffice portatile"""
        if not self.is_installed():
            return None
        
        soffice_path = self.portable_dir / "App" / "libreoffice" / "program" / "soffice.exe"
        return str(soffice_path)
    
    def install_portable(self, progress_callback=None) -> bool:
        """
        Installa LibreOffice portatile automaticamente
        
        Returns:
            True se installazione riuscita
        """
        if 'windows' not in self.system:
            self.logger.warning("Installazione automatica disponibile solo su Windows")
            return False
        
        try:
            self.logger.info("Inizio installazione LibreOffice portatile...")
            
            if progress_callback:
                progress_callback(10, "Download LibreOffice portatile...")
            
            # URL LibreOffice portatile (versione leggera)
            # Usando 7.5.x che è stabile e veloce
            url = "https://download.documentfoundation.org/libreoffice/portable/7.5.9/LibreOfficePortable_7.5.9_MultilingualStandard.paf.exe"
            
            # Scarica installer
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".exe")
            temp_path = temp_file.name
            temp_file.close()
            
            self.logger.info(f"Download da: {url}")
            urllib.request.urlretrieve(url, temp_path)
            
            if progress_callback:
                progress_callback(50, "Estrazione LibreOffice...")
            
            # Estrai in modo silenzioso
            self.portable_dir.mkdir(parents=True, exist_ok=True)
            
            # Esegui installer in modalità silenziosa
            cmd = [temp_path, "/S", f"/D={str(self.portable_dir)}"]
            subprocess.run(cmd, check=True, timeout=300)
            
            # Cleanup
            os.unlink(temp_path)
            
            if progress_callback:
                progress_callback(100, "LibreOffice installato!")
            
            self.logger.info("LibreOffice portatile installato con successo")
            return True
        
        except Exception as e:
            self.logger.error(f"Errore installazione LibreOffice: {e}")
            return False
    
    def install_via_winget(self) -> bool:
        """
        Installa LibreOffice usando winget (Windows Package Manager)
        
        Returns:
            True se installazione riuscita
        """
        if 'windows' not in self.system:
            return False
        
        try:
            self.logger.info("Tentativo installazione via winget...")
            
            # Verifica se winget è disponibile
            result = subprocess.run(
                ["winget", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0:
                self.logger.warning("winget non disponibile")
                return False
            
            # Installa LibreOffice
            self.logger.info("Installazione LibreOffice via winget...")
            result = subprocess.run(
                ["winget", "install", "--id=TheDocumentFoundation.LibreOffice", "--silent", "--accept-package-agreements"],
                capture_output=True,
                text=True,
                timeout=600
            )
            
            if result.returncode == 0:
                self.logger.info("LibreOffice installato con successo via winget")
                return True
            else:
                self.logger.error(f"Errore winget: {result.stderr}")
                return False
        
        except Exception as e:
            self.logger.error(f"Errore installazione winget: {e}")
            return False
    
    def show_manual_install_dialog(self):
        """Mostra dialog per installazione manuale"""
        try:
            from PyQt6.QtWidgets import QMessageBox
            
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("LibreOffice Richiesto")
            msg.setText("LibreOffice è necessario per la conversione Word → PDF")
            msg.setInformativeText(
                "Scegli un metodo di installazione:\n\n"
                "• Automatico: Installerò LibreOffice portatile per te\n"
                "• Manuale: Scarica da libreoffice.org"
            )
            
            auto_btn = msg.addButton("Installa Automaticamente", QMessageBox.ButtonRole.AcceptRole)
            manual_btn = msg.addButton("Guida Installazione Manuale", QMessageBox.ButtonRole.RejectRole)
            msg.addButton("Annulla", QMessageBox.ButtonRole.RejectRole)
            
            msg.exec()
            
            if msg.clickedButton() == auto_btn:
                return "auto"
            elif msg.clickedButton() == manual_btn:
                return "manual"
            else:
                return None
        
        except Exception as e:
            self.logger.error(f"Errore dialog: {e}")
            return None
