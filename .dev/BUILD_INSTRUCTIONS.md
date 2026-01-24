# 🏗️ Istruzioni Build DocConverter

## 📋 Prerequisiti

- Python 3.10+
- PyInstaller (installato automaticamente)
- Windows (per build .exe)

## 🚀 Build Rapido

### Opzione 1: Script Automatico (CONSIGLIATO)

```bash
cd DocConverter
python build_exe.py
```

Lo script:
1. ✅ Pulisce build precedenti
2. ✅ Installa PyInstaller (se mancante)
3. ✅ Crea DocConverter.exe
4. ✅ Verifica il risultato

### Opzione 2: Manuale

```bash
cd DocConverter
pip install pyinstaller
pyinstaller --name=DocConverter --onefile --windowed --icon=assets/icon.ico --add-data "assets;assets" main.py
```

## 📦 Output

L'eseguibile sarà creato in:
```
DocConverter/dist/DocConverter.exe
```

Dimensione tipica: ~50-80 MB (include Python + dipendenze)

## ✅ Test Eseguibile

1. Vai in `dist/`
2. Doppio click su `DocConverter.exe`
3. L'app si avvia senza bisogno di Python!

## 🌐 Pubblicazione GitHub

### 1. Crea Release

```bash
cd DocConverter
git tag -a v2.3.0 -m "Release 2.3.0 - Ultra Veloce + LibreOffice"
git push origin v2.3.0
```

### 2. Su GitHub

1. Vai su **Releases** → **Draft a new release**
2. Tag: `v2.3.0`
3. Titolo: `DocConverter v2.3.0 - Ultra Veloce`
4. Descrizione:
```markdown
## 🎉 DocConverter v2.3.0

### ⚡ Miglioramenti Performance
- Conversioni 2-3x più veloci con cache intelligente
- LibreOffice come metodo principale (NON serve Office!)
- Rilevamento specifico di Word, Excel, PowerPoint

### 🆕 Novità
- Icona barra applicazioni
- Fix blocco conversione allo 0%
- Messaggi di errore più chiari

### 📥 Download
- **Windows**: Scarica `DocConverter.exe` (standalone)
- **Linux/macOS**: Clona repo e usa `python main.py`

### 📖 Requisiti
- Windows 10/11
- LibreOffice (gratuito): https://www.libreoffice.org/download/

**NON serve Microsoft Office!**
```

5. **Carica file**: Drag & drop `dist/DocConverter.exe`
6. **Publish release**

## 🔧 Parametri PyInstaller

```bash
--name=DocConverter          # Nome eseguibile
--onefile                    # Singolo .exe (tutto incluso)
--windowed                   # Nessuna console (solo GUI)
--icon=assets/icon.ico       # Icona app
--add-data "assets;assets"   # Include cartella assets
--clean                      # Pulizia automatica
```

## 📁 Struttura Release

```
DocConverter-v2.3.0/
├── DocConverter.exe         # ← QUESTO vai su GitHub!
├── README.md                # Istruzioni utente
└── LICENSE                  # Licenza
```

## ⚠️ Problemi Comuni

### PyInstaller non trovato
```bash
pip install pyinstaller --upgrade
```

### Icona non caricata
Verifica che `assets/icon.ico` esista:
```bash
python assets/create_icon.py
```

### .exe troppo grande
Normale! Include:
- Python runtime (~30 MB)
- PyQt6 (~20 MB)
- Dipendenze (~30 MB)

### Antivirus blocca .exe
Normale per nuovi .exe. Soluzione:
1. Firma digitale (costosa)
2. Chiedi agli utenti di aggiungere eccezione

## 📝 Checklist Finale

Prima di pubblicare:

- [ ] Build .exe completato
- [ ] Testato su Windows pulito (senza Python)
- [ ] Conversione Word→PDF funziona
- [ ] Icona visibile
- [ ] Versione corretta (2.3.0)
- [ ] README.md aggiornato
- [ ] CHANGELOG.md aggiornato
- [ ] Tag Git creato
- [ ] Release GitHub pubblicata

## 🎯 Script CI/CD (Futuro)

Per automatizzare con GitHub Actions, crea `.github/workflows/build.yml`:

```yaml
name: Build EXE

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt pyinstaller
      - run: python build_exe.py
      - uses: actions/upload-artifact@v3
        with:
          name: DocConverter-exe
          path: dist/DocConverter.exe
```

## 📞 Supporto

Problemi? Apri un Issue su GitHub!

---

**Buon build! 🚀**
