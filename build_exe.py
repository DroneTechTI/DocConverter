#!/usr/bin/env python3
"""
Build script for creating DocConverter executable.

This script builds a standalone executable for Windows using PyInstaller.
"""

import sys
import subprocess
import shutil
from pathlib import Path


def check_pyinstaller():
    """Check if PyInstaller is installed."""
    try:
        import PyInstaller
        print("✓ PyInstaller is installed")
        return True
    except ImportError:
        print("✗ PyInstaller not found")
        print("\nInstalling PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        return True


def clean_build():
    """Clean previous build artifacts."""
    print("\n🧹 Cleaning previous builds...")
    
    for folder in ['build', 'dist', '__pycache__']:
        if Path(folder).exists():
            shutil.rmtree(folder)
            print(f"  Removed: {folder}/")
    
    # Remove .spec file if exists (we use build.spec)
    if Path('main.spec').exists():
        Path('main.spec').unlink()
        print("  Removed: main.spec")


def build_executable():
    """Build the executable using PyInstaller."""
    print("\n🔨 Building executable...")
    print("This may take a few minutes...\n")
    
    try:
        subprocess.check_call([
            'pyinstaller',
            '--clean',
            '--noconfirm',
            'build.spec'
        ])
        
        print("\n✅ Build completed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build failed: {e}")
        return False


def verify_build():
    """Verify the built executable exists."""
    exe_path = Path('dist') / 'DocConverter.exe'
    
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"\n📦 Executable created:")
        print(f"   Path: {exe_path}")
        print(f"   Size: {size_mb:.1f} MB")
        return True
    else:
        print("\n❌ Executable not found!")
        return False


def main():
    """Main build process."""
    print("=" * 60)
    print("DocConverter - Build Script")
    print("=" * 60)
    
    # Check dependencies
    if not check_pyinstaller():
        return 1
    
    # Clean previous builds
    clean_build()
    
    # Build executable
    if not build_executable():
        return 1
    
    # Verify build
    if not verify_build():
        return 1
    
    print("\n" + "=" * 60)
    print("🎉 Build process completed successfully!")
    print("=" * 60)
    print("\nYou can find the executable at: dist/DocConverter.exe")
    print("\nTo test it, run:")
    print("  .\\dist\\DocConverter.exe")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
