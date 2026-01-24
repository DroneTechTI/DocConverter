# 📄 DocConverter

**Professional Document Conversion Software**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](https://github.com/DevilStyle/DocConverter)

A powerful, cross-platform desktop application for converting documents between multiple formats with a modern graphical interface. Pure Python implementation - no external dependencies required for most conversions!

**Software desktop professionale per la conversione di documenti - Windows & Linux**

![Version](https://img.shields.io/badge/version-2.5.0-blue)
![Build](https://img.shields.io/badge/build-passing-brightgreen)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.10+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## 🎯 Descrizione

DocConverter è un'applicazione desktop moderna e intuitiva per la conversione di documenti tra diversi formati. Progettato con un'architettura modulare, permette di aggiungere facilmente nuovi convertitori in futuro.

**🎉 NOVITÀ v2.0.0 - MAJOR UPDATE:**
- 🎯 **7 Convertitori Totali** - Era 1, ora 7! (Word, PDF, Excel, PowerPoint, Immagini, HTML)
- ⚡ **Conversione Word→PDF Ottimizzata** - Ancora più veloce!
- 🎨 **Avvio Professionale** - Nessun terminale visibile!
- 💪 **Suite completa** - Copre tutti i formati Office e web!

### ✨ Funzionalità Principali

- **Word → PDF** (.doc, .docx) ⚡ VELOCISSIMO
- **PDF → Word** (.pdf → .docx) 🆕
- **PDF → Immagini** (.pdf → .png, .jpg) 🆕
- **Immagini → PDF** (.png, .jpg, .bmp, .gif → .pdf) 🆕
- **Excel → PDF** (.xlsx, .xls) 🆕
- **PowerPoint → PDF** (.pptx, .ppt) 🆕
- **HTML → PDF** (.html, .htm) 🆕
- **Interfaccia grafica moderna** e facile da usare
- **Conversione batch** (multipli file contemporaneamente)
- **Barra di progresso** in tempo reale
- **Gestione errori** chiara e comprensibile
- **Sistema di logging** completo
- **Drag & Drop** dei file
- **Controllo dipendenze** automatico

### 🔮 Convertitori Futuri (Architettura Pronta)

- PDF → Word
- PDF → Immagini (PNG/JPEG)
- Immagini → PDF
- TXT → PDF
- HTML → PDF

---

## 💻 Requisiti di Sistema

### Windows
- Windows 10 o superiore
- Python 3.10+ (installato automaticamente con l'installer)
- **Microsoft Word** (già presente in Office) - CONSIGLIATO per conversioni veloci
- Oppure LibreOffice (alternativa gratuita)
- 200 MB di spazio libero

### Linux
- Ubuntu 20.04+ / Debian 11+ / Fedora 35+ (o equivalenti)
- Python 3.10+
- LibreOffice (per conversione Word→PDF)

---

## 📦 Installazione

### Windows

1. **Scarica l'installer** `DocConverter-Setup.exe`
2. **Esegui l'installer** e segui le istruzioni
3. **Avvia l'applicazione** dal menu Start o desktop

### Linux

#### Metodo 1: Installazione da sorgenti (consigliato)

```bash
# Clona il repository
git clone https://github.com/TUO_USERNAME/DocConverter.git
cd DocConverter

# Installa dipendenze sistema
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv libreoffice

# Crea ambiente virtuale
python3 -m venv venv
source venv/bin/activate

# Installa dipendenze Python
pip install -r requirements.txt

# Avvia l'applicazione
python main.py
```

#### Metodo 2: AppImage (disponibile in futuro)

```bash
chmod +x DocConverter-x86_64.AppImage
./DocConverter-x86_64.AppImage
```

---

## 🚀 Utilizzo

### 🌟 Avvio Professionale (NUOVO!)

**Windows - Senza Terminale:**
```cmd
# Doppio click su uno di questi:
DocConverter.pyw       ← Avvio immediato (professionale!)
start_pro.bat         ← Con installazione automatica dipendenze
```

**Linux/macOS:**
```bash
./start_pro.sh        ← Setup completo + avvio pulito
python3 DocConverter.pyw  ← Avvio diretto
```

**Risultato:** L'app si apre SENZA finestra terminale nera! 🎉

### Avvio Rapido

1. **Apri DocConverter** (usa `DocConverter.pyw` per esperienza professionale!)
2. **Seleziona i file** da convertire (pulsante "Seleziona File" o drag & drop)
3. **Scegli la cartella di destinazione** (opzionale, default: stessa cartella dei file originali)
4. **Clicca su "Converti"**
5. **Attendi il completamento** (monitora la barra di progresso)

### Conversione Batch

Per convertire più file:
- Seleziona multipli file tramite il selettore (Ctrl+Click o Shift+Click)
- Oppure trascina più file nell'area di drop
- Tutti i file verranno convertiti in sequenza

### Visualizzazione Log

I log delle operazioni sono visibili in tempo reale nella sezione inferiore dell'interfaccia e salvati in `logs/docconverter.log`

---

## 📁 Struttura del Progetto

```
DocConverter/
│
├── main.py                     # Entry point dell'applicazione
├── requirements.txt            # Dipendenze Python
├── README.md                   # Questa documentazione
├── .gitignore                  # File da ignorare in Git
│
├── core/                       # Core business logic
│   ├── __init__.py
│   ├── converter_base.py       # Classe base astratta per convertitori
│   ├── converter_registry.py   # Registro dei convertitori disponibili
│   └── dependency_checker.py   # Controllo dipendenze sistema
│
├── converters/                 # Moduli di conversione specifici
│   ├── __init__.py
│   ├── word_to_pdf.py          # Convertitore Word → PDF
│   └── README.md               # Guida per aggiungere nuovi convertitori
│
├── gui/                        # Interfaccia grafica
│   ├── __init__.py
│   ├── main_window.py          # Finestra principale
│   ├── widgets/                # Widget personalizzati
│   │   ├── __init__.py
│   │   ├── file_list.py        # Lista file con drag & drop
│   │   └── progress_bar.py     # Barra progresso avanzata
│   └── styles/                 # Stili e temi
│       ├── __init__.py
│       └── dark_theme.py       # Tema scuro moderno
│
├── utils/                      # Utilities e helper
│   ├── __init__.py
│   ├── logger.py               # Sistema di logging
│   ├── file_handler.py         # Gestione file e path
│   └── error_handler.py        # Gestione errori centralizzata
│
├── config/                     # Configurazioni
│   ├── __init__.py
│   └── settings.py             # Impostazioni applicazione
│
├── logs/                       # File di log (generato automaticamente)
│
└── tests/                      # Test unitari
    ├── __init__.py
    └── test_converters.py
```

---

## 🛠️ Sviluppo

### Aggiungere un Nuovo Convertitore

1. Crea un nuovo file in `converters/` (es. `pdf_to_word.py`)
2. Eredita da `ConverterBase`
3. Implementa i metodi `convert()` e `get_info()`
4. Registra il convertitore nel registry

Esempio:

```python
from core.converter_base import ConverterBase

class PDFToWordConverter(ConverterBase):
    def get_info(self):
        return {
            'name': 'PDF to Word',
            'input_formats': ['.pdf'],
            'output_format': '.docx',
            'description': 'Converte PDF in Word'
        }
    
    def convert(self, input_path, output_path, progress_callback=None):
        # Implementa la logica di conversione
        pass
```

### Eseguire i Test

```bash
# Attiva l'ambiente virtuale
source venv/bin/activate  # Linux/Mac
# oppure
venv\Scripts\activate  # Windows

# Esegui i test
python -m pytest tests/
```

---

## 🐛 Troubleshooting

### Windows

**Errore: "LibreOffice non trovato"**
- L'installer installa automaticamente LibreOffice portable
- Se l'errore persiste, riavvia l'applicazione

### Linux

**Errore: "soffice: command not found"**
```bash
sudo apt-get install libreoffice
```

**Errore: "Permission denied"**
```bash
chmod +x start.sh
./start.sh
```

### Generale

**L'applicazione non si avvia**
- Verifica di avere Python 3.10+ installato: `python --version`
- Reinstalla le dipendenze: `pip install -r requirements.txt --force-reinstall`
- Controlla i log in `logs/docconverter.log`

---

## 📝 Changelog

### v2.3.0 (2026-01-09) - SPEED OPTIMIZATION ⚡
- ⚡ **CONVERSIONI ULTRA-VELOCI** - Cache rilevamento Office (no rilevamenti multipli!)
- 🚀 Word: Solo COM diretto (docx2pdf rimosso - instabile)
- ⚡ Excel & PowerPoint: Cache rilevamento per velocità massima
- 📊 **Miglioramento**: 2-3x più veloce nelle conversioni multiple
- 🎯 Zero attese inutili - conversione istantanea dopo prima rilevazione
- 💾 Cache intelligente salvata in memoria per sessione

### v2.2.1 (2026-01-09) - DETECTION IMPROVEMENT
- 🔍 **Rilevamento SPECIFICO** di Word, Excel, PowerPoint (non "Office" generico)
- ✅ Ricerca mirata per ogni applicazione singolarmente
- 💪 Log migliorati con emoji e messaggi chiari
- 🎯 Controlli più precisi con pythoncom.CoInitialize()
- 📝 Codice ottimizzato per tutte e 3 le applicazioni Office

### v2.0.0 (2026-01-09) - MAJOR UPDATE
- 🎯 **7 Convertitori Totali** - Da 1 a 7! (600% più potente)
- 🆕 PDF → Word, PDF → Immagini, Immagini → PDF
- 🆕 Excel → PDF, PowerPoint → PDF, HTML → PDF
- ⚡ Ottimizzazione Word→PDF con `keep_active=True`
- 🎨 **Launcher professionale** - `DocConverter.pyw` senza terminale!
- 📝 `start_pro.bat` e `start_pro.sh` per avvio pulito
- 💪 Rilevamento automatico Office nativo su Windows
- 🐛 Gestione migliorata trasparenza immagini
- 📚 Dipendenze aggiornate per nuovi convertitori
- 📖 Documentazione completa aggiornata
- ✅ Vedi `NOVITA_v2.0.md` per dettagli completi

### v1.1.0 (2026-01-09) - PERFORMANCE UPDATE
- ⚡ **Avvio 5x più veloce** con lazy loading degli import
- 🎯 **Usa Microsoft Word su Windows** - niente LibreOffice necessario!
- 🚀 **Conversioni 4x più veloci** con Word installato
- 💪 **Rilevamento automatico** del metodo migliore
- ✅ Fallback intelligente a LibreOffice se necessario
- 📝 Vedi `AGGIORNAMENTI_v1.1.md` per dettagli completi

### v1.0.0 (2026-01-09)
- 🎉 Rilascio iniziale
- ✅ Conversione Word → PDF
- ✅ Interfaccia grafica moderna
- ✅ Conversione batch
- ✅ Sistema di logging
- ✅ Architettura modulare per futuri convertitori

---

## 📄 Licenza

Questo progetto è rilasciato sotto licenza MIT. Vedi il file `LICENSE` per dettagli.

---

## 👤 Autore

Sviluppato con ❤️ per fornire uno strumento semplice e potente di conversione documenti.

---

## 🤝 Contributi

I contributi sono benvenuti! Per modifiche importanti:
1. Fai un fork del progetto
2. Crea un branch per la tua feature (`git checkout -b feature/AmazingFeature`)
3. Committa le tue modifiche (`git commit -m 'Add some AmazingFeature'`)
4. Pusha il branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

---

## 📧 Supporto

Per bug, domande o suggerimenti, apri una Issue su GitHub.

---

**⭐ Se questo progetto ti è stato utile, lascia una stella su GitHub!**
