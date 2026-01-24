"""
Script per verificare dipendenze prima dell'avvio
"""
import sys
import subprocess

REQUIRED_PACKAGES = {
    'PyQt6': 'PyQt6>=6.6.0',
    'psutil': 'psutil>=5.9.6',
    'docx': 'python-docx>=1.1.0',
    'pypdf': 'pypdf>=3.17.0',
    'PIL': 'Pillow>=10.1.0',
    'reportlab': 'reportlab>=4.0.7',
}

def check_and_install():
    """Verifica e installa dipendenze mancanti"""
    missing = []
    
    print("🔍 Verifica dipendenze DocConverter...")
    print()
    
    for module_name, package_name in REQUIRED_PACKAGES.items():
        try:
            __import__(module_name)
            print(f"  ✅ {module_name:<15} OK")
        except ImportError:
            print(f"  ❌ {module_name:<15} MANCANTE")
            missing.append(package_name)
    
    if missing:
        print()
        print("⚠️  Alcune dipendenze sono mancanti!")
        print()
        print("Per installarle automaticamente, esegui:")
        print(f"  pip install {' '.join(missing)}")
        print()
        print("Oppure installa tutto con:")
        print("  pip install -r requirements.txt")
        print()
        
        response = input("Vuoi installarle ora? (s/n): ").lower().strip()
        
        if response == 's':
            print()
            print("📦 Installazione in corso...")
            try:
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install"
                ] + missing)
                print()
                print("✅ Installazione completata!")
                print()
                return True
            except subprocess.CalledProcessError:
                print()
                print("❌ Errore durante l'installazione.")
                print("Prova manualmente con:")
                print(f"  pip install {' '.join(missing)}")
                return False
        else:
            return False
    else:
        print()
        print("✅ Tutte le dipendenze sono installate!")
        print()
        return True

if __name__ == "__main__":
    success = check_and_install()
    sys.exit(0 if success else 1)
