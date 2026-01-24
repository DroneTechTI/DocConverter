#!/usr/bin/env python3
"""
DocConverter - Software Professionale per Conversione Documenti

Entry point dell'applicazione.
"""
import sys
import os
from pathlib import Path

# Aggiungi la directory corrente al path per import
sys.path.insert(0, str(Path(__file__).parent))

import sys
import platform
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from config.settings import Settings
from gui.main_window import MainWindow
from utils.logger import setup_logger

# Fix icona taskbar Windows
if platform.system() == 'Windows':
    try:
        import ctypes
        # Imposta AppUserModelID per icona taskbar
        myappid = 'DocConverter.v2.4.0'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except:
        pass


def check_and_install_dependencies():
    """
    Verifica e installa automaticamente dipendenze mancanti
    """
    import subprocess
    
    # Lista dipendenze critiche
    critical_deps = {
        'PyQt6': 'PyQt6>=6.6.0',
        'psutil': 'psutil>=5.9.6',
        'docx': 'python-docx>=1.1.0',
        'pypdf': 'pypdf>=3.17.0',
        'PIL': 'Pillow>=10.1.0',
        'reportlab': 'reportlab>=4.0.7',
    }
    
    missing = []
    
    print("🔍 Verifica dipendenze...")
    
    for module_name, package_name in critical_deps.items():
        try:
            __import__(module_name)
        except ImportError:
            missing.append(package_name)
    
    if missing:
        print()
        print(f"⚠️  Trovate {len(missing)} dipendenze mancanti")
        print()
        print("📦 Installazione automatica in corso...")
        print()
        
        try:
            # Installa dipendenze mancanti
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "--quiet"
            ] + missing)
            
            print("✅ Dipendenze installate con successo!")
            print()
            return True
            
        except subprocess.CalledProcessError:
            print()
            print("❌ Errore installazione automatica")
            print()
            print("📋 Installa manualmente con:")
            print(f"   pip install {' '.join(missing)}")
            print()
            input("Premi ENTER per chiudere...")
            return False
    
    return True


def main():
    """
    Funzione principale dell'applicazione.
    """
    # Verifica e installa dipendenze automaticamente
    if not check_and_install_dependencies():
        return 1
    
    # Assicura che le directory necessarie esistano
    Settings.ensure_directories()
    
    # Configura logger
    logger = setup_logger()
    logger.info("=" * 60)
    logger.info(f"Avvio {Settings.APP_NAME} v{Settings.APP_VERSION}")
    logger.info("=" * 60)
    
    try:
        # Crea applicazione Qt
        app = QApplication(sys.argv)
        
        # Configura applicazione
        app.setApplicationName(Settings.APP_NAME)
        app.setApplicationVersion(Settings.APP_VERSION)
        app.setOrganizationName(Settings.APP_AUTHOR)
        
        # 🎨 Imposta icona globale app
        icon_path = Settings.BASE_DIR / "assets" / "icon.ico"
        if icon_path.exists():
            app.setWindowIcon(QIcon(str(icon_path)))
            logger.info(f"✅ Icona app impostata: {icon_path}")
        
        # Abilita high DPI scaling
        if hasattr(Qt, 'AA_EnableHighDpiScaling'):
            app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
        if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
            app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
        
        # Crea e mostra finestra principale
        logger.info("Inizializzazione interfaccia grafica...")
        window = MainWindow()
        window.show()
        
        logger.info("Applicazione avviata con successo")
        logger.info(f"Interfaccia pronta - in attesa di input utente")
        
        # Avvia event loop
        exit_code = app.exec()
        
        logger.info(f"Applicazione terminata (exit code: {exit_code})")
        return exit_code
    
    except Exception as e:
        logger.critical(f"Errore fatale: {e}", exc_info=True)
        
        # Tenta di mostrare messaggio di errore
        try:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(
                None,
                "Errore Fatale",
                f"Si è verificato un errore fatale:\n\n{str(e)}\n\n"
                f"Controlla il file di log per maggiori dettagli."
            )
        except:
            pass
        
        return 1


if __name__ == "__main__":
    sys.exit(main())
