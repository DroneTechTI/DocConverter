"""
Script per creare l'eseguibile Windows (.exe) di DocConverter
Usa PyInstaller per creare un'applicazione standalone

DocConverter v2.5.0 Build Script
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def clean_build_dirs():
    """Pulisce le directory di build precedenti"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    
    for dir_name in dirs_to_clean:
        if Path(dir_name).exists():
            print(f"🧹 Pulizia {dir_name}/...")
            shutil.rmtree(dir_name, ignore_errors=True)
    
    # Rimuovi file .spec precedenti
    for spec_file in Path('.').glob('*.spec'):
        print(f"🧹 Rimozione {spec_file}...")
        spec_file.unlink()

def check_pyinstaller():
    """Verifica che PyInstaller sia installato"""
    try:
        import PyInstaller
        print(f"✅ PyInstaller trovato: versione {PyInstaller.__version__}")
        return True
    except ImportError:
        print("❌ PyInstaller non trovato!")
        print("\n📥 Installazione PyInstaller...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
            print("✅ PyInstaller installato!")
            return True
        except:
            print("❌ Errore installazione PyInstaller")
            return False

def create_exe():
    """Crea l'eseguibile con PyInstaller"""
    
    print("\n" + "="*60)
    print("🚀 BUILD DOCCONVERTER .EXE")
    print("="*60 + "\n")
    
    # 1. Pulizia
    print("📋 Fase 1: Pulizia directory build...")
    clean_build_dirs()
    
    # 2. Verifica PyInstaller
    print("\n📋 Fase 2: Verifica PyInstaller...")
    if not check_pyinstaller():
        return False
    
    # 3. Build
    print("\n📋 Fase 3: Creazione eseguibile...")
    
    # Parametri PyInstaller
    icon_path = Path("assets/icon.ico")
    main_script = Path("main.py")
    
    if not main_script.exists():
        print(f"❌ Script principale non trovato: {main_script}")
        return False
    
    if not icon_path.exists():
        print(f"⚠️ Icona non trovata: {icon_path} (continuo senza icona)")
        icon_path = None
    
    # Comando PyInstaller (esegui dalla root)
    cmd = [
        sys.executable,
        "-m", "PyInstaller",
        "--name=DocConverter",
        "--onefile",  # Un singolo .exe
        "--windowed",  # Nessuna console
        "--clean",
        "--optimize=2",  # Ottimizzazione Python bytecode
        "--noupx",  # Disabilita UPX (migliore compatibilità)
        "--workpath=.dev/build",  # Build in .dev
        "--distpath=.dev/dist",  # Output in .dev
        "--specpath=.dev",  # Spec in .dev
    ]
    
    # Escludi moduli non necessari per ridurre dimensioni
    excludes = [
        "unittest",
        "test",
        "pytest",
        "setuptools",
        "distutils",
        "tkinter",
        "lib2to3",
        "numpy",  # Se non usato
        "pandas",  # Se non usato
    ]
    
    for module in excludes:
        cmd.extend(["--exclude-module", module])
    
    # Aggiungi icona se disponibile
    if icon_path:
        cmd.extend(["--icon", str(icon_path)])
    
    # Aggiungi dati (assets) - path assoluto
    assets_path = Path("assets").absolute()
    if assets_path.exists():
        cmd.extend(["--add-data", f"{assets_path};assets"])
    
    # Aggiungi file main.py
    cmd.append(str(main_script))
    
    print(f"\n🔨 Comando build:")
    print(f"   {' '.join(cmd)}\n")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        print("\n✅ Build completato con successo!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Errore durante il build: {e}")
        return False

def verify_exe():
    """Verifica che l'eseguibile sia stato creato"""
    exe_path = Path("dist/DocConverter.exe")
    
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"\n✅ Eseguibile creato: {exe_path}")
        print(f"   Dimensione: {size_mb:.1f} MB")
        
        # Calcola hash per verifica integrità
        import hashlib
        sha256_hash = hashlib.sha256()
        with open(exe_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        
        print(f"   SHA256: {sha256_hash.hexdigest()[:16]}...")
        print(f"\n📦 File pronto per la distribuzione!")
        print(f"   Percorso: {exe_path.absolute()}")
        
        # Salva info build
        build_info_path = Path("dist/BUILD_INFO.txt")
        with open(build_info_path, "w", encoding="utf-8") as f:
            f.write(f"DocConverter v2.5.0 - Build Info\n")
            f.write(f"================================\n\n")
            f.write(f"File: DocConverter.exe\n")
            f.write(f"Size: {size_mb:.2f} MB\n")
            f.write(f"SHA256: {sha256_hash.hexdigest()}\n")
            f.write(f"Built with: PyInstaller\n")
            f.write(f"Python: {sys.version.split()[0]}\n")
        
        print(f"   Build info salvato: {build_info_path}")
        
        return True
    else:
        print(f"\n❌ Eseguibile non trovato: {exe_path}")
        return False

def main():
    """Funzione principale"""
    
    # Cambia directory alla ROOT del progetto (non .dev)
    os.chdir(Path(__file__).parent.parent)
    
    # Build
    success = create_exe()
    
    if not success:
        print("\n❌ BUILD FALLITO!")
        return 1
    
    # Verifica
    if not verify_exe():
        print("\n❌ VERIFICA FALLITA!")
        return 1
    
    print("\n" + "="*60)
    print("🎉 BUILD COMPLETATO CON SUCCESSO!")
    print("="*60)
    print("\n📝 Prossimi passi:")
    print("   1. Testa l'eseguibile: dist/DocConverter.exe")
    print("   2. Crea release su GitHub")
    print("   3. Carica DocConverter.exe come asset")
    print("\n")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
