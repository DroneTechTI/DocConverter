#!/usr/bin/env python3
"""
DocConverter - Professional Document Conversion Software

Application entry point.
"""
import sys
import platform
from pathlib import Path
from typing import Dict

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from config.settings import Settings
from gui.main_window import MainWindow
from utils.logger import setup_logger


# Fix Windows taskbar icon
if platform.system() == 'Windows':
    try:
        import ctypes
        # Set AppUserModelID for taskbar icon
        myappid = 'DocConverter.v2.5.0'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception:
        pass


def check_and_install_dependencies() -> bool:
    """
    Check if critical dependencies are available.
    
    Returns:
        True if all dependencies are satisfied, False otherwise
    """
    # Critical dependencies mapping
    critical_deps: Dict[str, str] = {
        'PyQt6': 'PyQt6>=6.6.0',
        'psutil': 'psutil>=5.9.6',
        'docx': 'python-docx>=1.1.0',
        'pypdf': 'pypdf>=3.17.0',
        'PIL': 'Pillow>=10.1.0',
        'reportlab': 'reportlab>=4.0.7',
    }
    
    missing = []
    
    for module_name, package_name in critical_deps.items():
        try:
            __import__(module_name)
        except ImportError:
            missing.append(package_name)
    
    if missing:
        print()
        print("❌ Missing required dependencies:")
        print()
        for pkg in missing:
            print(f"   • {pkg}")
        print()
        print("📋 Install with:")
        print(f"   pip install {' '.join(missing)}")
        print()
        input("Press ENTER to close...")
        return False
    
    return True


def main() -> int:
    """
    Main application entry point.
    
    Returns:
        Application exit code
    """
    # Check dependencies
    if not check_and_install_dependencies():
        return 1
    
    # Ensure required directories exist
    Settings.ensure_directories()
    
    # Setup logger
    logger = setup_logger()
    logger.info("=" * 60)
    logger.info(f"Starting {Settings.APP_NAME} v{Settings.APP_VERSION}")
    logger.info("=" * 60)
    
    try:
        # Create Qt application
        app = QApplication(sys.argv)
        
        # Configure application metadata
        app.setApplicationName(Settings.APP_NAME)
        app.setApplicationVersion(Settings.APP_VERSION)
        app.setOrganizationName(Settings.APP_AUTHOR)
        
        # Set application icon
        icon_path = Settings.BASE_DIR / "assets" / "icon.ico"
        if icon_path.exists():
            app.setWindowIcon(QIcon(str(icon_path)))
            logger.info(f"✅ Application icon set: {icon_path}")
        
        # Enable high DPI scaling
        if hasattr(Qt, 'AA_EnableHighDpiScaling'):
            app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
        if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
            app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
        
        # Create and show main window
        logger.info("Initializing graphical interface...")
        window = MainWindow()
        window.show()
        
        logger.info("Application started successfully")
        logger.info("Interface ready - waiting for user input")
        
        # Start event loop
        exit_code = app.exec()
        
        logger.info(f"Application terminated (exit code: {exit_code})")
        return exit_code
    
    except Exception as e:
        logger.critical(f"Fatal error: {e}", exc_info=True)
        
        # Try to show error message
        try:
            QMessageBox.critical(
                None,
                "Fatal Error",
                f"A fatal error occurred:\n\n{str(e)}\n\n"
                f"Check the log file for more details."
            )
        except Exception:
            pass
        
        return 1


if __name__ == "__main__":
    sys.exit(main())
