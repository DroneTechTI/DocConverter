# 📋 Changelog

Tutte le modifiche significative a questo progetto saranno documentate in questo file.

## [2.5.0] - 2026-01-09

### 🐛 Bug Fix
- **Corretto bug critico ConversionError**: Risolto errore `ConversionError.__init__() got an unexpected keyword argument 'input_file'`
  - Parametri corretti in `word_to_pdf.py` e `word_to_pdf_pure.py`
  - Conversioni Word→PDF ora funzionano correttamente

### ✨ Nuove Funzionalità
- **PDF Merge**: Unisci più file PDF in un unico documento
  - Nuovo convertitore `PDFMergeConverter`
  - Interfaccia GUI con pulsante dedicato "📑 Unisci PDF"
  - Selezione multipla file con ordine personalizzabile
  
- **PDF Compress**: Riduci dimensioni file PDF
  - Nuovo convertitore `PDFCompressConverter`
  - Compressione intelligente con statistiche riduzione
  - Pulsante GUI "🗜️ Comprimi PDF"
  
- **Sezione Utilità PDF**: Nuova area GUI con strumenti PDF avanzati

### ⚡ Performance
- **BatchOptimizer**: Processing parallelo intelligente
  - Auto-tuning worker basato su CPU/RAM disponibile
  - ThreadPool ottimizzato per conversioni multiple
  - Chunk size dinamico per gestione memoria
  
- **CacheManager**: Sistema cache avanzato
  - Cache in memoria per accesso veloce
  - Cache su disco con TTL configurabile (24h default)
  - Pulizia automatica cache scadute
  
- **MemoryOptimizer**: Gestione automatica memoria
  - Garbage collection intelligente
  - Monitoraggio pressione memoria real-time
  - Cleanup automatico ogni 5 conversioni
  - Statistiche utilizzo memoria

### 🚀 Ottimizzazioni Convertitori
- **Word to PDF**: 
  - Import lazy per startup veloce
  - Batch processing paragrafi
  - Progress update granulare (ogni 10%)
  - HTML escaping per sicurezza
  - Gestione ottimizzata tabelle

### 🧪 Test
- Aggiunti test per `PDFMergeConverter`
- Aggiunti test per `PDFCompressConverter`
- Aggiunti test per moduli ottimizzazione (Memory, Batch, Cache)
- Corretti test esistenti per compatibilità
- Coverage aumentata: 8 convertitori + 3 moduli ottimizzazione

### 📦 Dipendenze
- Tutti i nuovi moduli usano solo librerie già presenti
- Nessuna dipendenza aggiuntiva richiesta

### 🎯 Miglioramenti Tecnici
- Codice più maintainable con separazione concerns
- Logging migliorato con statistiche performance
- Architettura modulare estesa
- Pattern singleton per moduli ottimizzazione

Il formato è basato su [Keep a Changelog](https://keepachangelog.com/it/1.0.0/),
e questo progetto aderisce al [Semantic Versioning](https://semver.org/lang/it/).

---

## [1.0.0] - 2026-01-09

### 🎉 Rilascio Iniziale

#### ✨ Aggiunte
- **Convertitore Word → PDF**
  - Supporto per formati .doc e .docx
  - Conversione tramite LibreOffice headless
  - Timeout configurabile per evitare blocchi
  
- **Interfaccia Grafica Moderna**
  - Design professionale con tema scuro
  - Interfaccia intuitiva e user-friendly
  - Supporto drag & drop per file
  - Barra di progresso in tempo reale
  
- **Conversione Batch**
  - Conversione multipla di file in sequenza
  - Thread separato per non bloccare l'UI
  - Gestione errori per singolo file
  
- **Sistema di Logging**
  - Log su file con rotazione automatica
  - Log console con colori (se supportato)
  - Livelli di log configurabili
  - Visualizzazione log in tempo reale nell'UI
  
- **Gestione Errori Robusta**
  - Messaggi di errore comprensibili
  - Validazione file prima della conversione
  - Gestione eccezioni centralizzata
  - Rollback automatico in caso di errore
  
- **Architettura Modulare**
  - Sistema plugin-based per convertitori
  - Registry centralizzato
  - Facile aggiunta di nuovi convertitori
  - Separazione tra business logic e UI
  
- **Controllo Dipendenze**
  - Verifica automatica di LibreOffice
  - Messaggi di installazione guidati
  - Cache dei controlli per performance
  
- **Documentazione Completa**
  - README dettagliato
  - Guida avvio rapido
  - Guida sviluppo convertitori
  - Commenti nel codice
  
- **Script di Avvio**
  - Script Windows (.bat)
  - Script Linux/macOS (.sh)
  - Setup automatico ambiente virtuale
  - Installazione automatica dipendenze

#### 🏗️ Architettura
- **Core**: Sistema base per convertitori
- **Converters**: Moduli di conversione specifici
- **GUI**: Interfaccia grafica PyQt6
- **Utils**: Utilities e helper
- **Config**: Configurazioni centralizzate

#### 📦 Dipendenze
- PyQt6 >= 6.6.0
- docx2pdf >= 0.1.8
- python-docx >= 1.1.0
- pypdf >= 3.17.0
- Pillow >= 10.1.0
- reportlab >= 4.0.7
- psutil >= 5.9.6
- colorlog >= 6.8.0

#### 🧪 Test
- Test unitari per convertitori
- Test per registry
- Test per validazione file

---

## [2.0.0] - 2026-01-09

### 🎉 MAJOR UPDATE - Suite Completa di Conversione

#### ✨ Nuovi Convertitori (Da 1 a 7!)
- **PDF → Word** (.pdf → .docx)
  - Converte PDF in documenti Word modificabili
  - Preserva formattazione e layout
  - Usa libreria pdf2docx

- **PDF → Immagini** (.pdf → .png, .jpg)
  - Estrae ogni pagina come immagine separata
  - Qualità configurabile (DPI)
  - Supporta PNG e JPEG

- **Immagini → PDF** (.png, .jpg, .bmp, .gif, .tiff → .pdf)
  - Converte immagini singole o multiple in PDF
  - Gestione trasparenza PNG
  - Ottimizzazione dimensione file

- **Excel → PDF** (.xlsx, .xls → .pdf)
  - Usa Excel installato su Windows (veloce)
  - Fallback a LibreOffice
  - Preserva formattazione celle e grafici

- **PowerPoint → PDF** (.pptx, .ppt → .pdf)
  - Usa PowerPoint installato su Windows
  - Fallback a LibreOffice
  - Mantiene animazioni come slide statiche

- **HTML → PDF** (.html, .htm → .pdf)
  - Rendering completo HTML/CSS
  - Usa weasyprint (puro Python)
  - Supporto immagini e stili

#### ⚡ Ottimizzazioni
- **Word → PDF Più Veloce**
  - Implementato `keep_active=True` in docx2pdf
  - Conversioni batch 50% più veloci
  - Da 3-5s a 2-3s per file in batch

#### 🎨 Avvio Professionale
- **Nuovo launcher senza terminale**
  - `DocConverter.pyw` - Doppio click e via!
  - `start_pro.bat` - Setup automatico (Windows)
  - `start_pro.sh` - Setup automatico (Linux/macOS)
  - Nessuna finestra console visibile
  - Esperienza utente professionale

#### 📦 Dipendenze Aggiunte
- `pdf2docx>=0.5.6` - Conversione PDF → Word
- `pdf2image>=1.16.3` - Estrazione immagini da PDF
- `weasyprint>=60.0` - Rendering HTML → PDF
- `pywin32>=306` - Automazione Office (Windows)

#### 🔧 Miglioramenti Tecnici
- Rilevamento automatico software Office su Windows
- Fallback intelligente a LibreOffice
- Gestione migliorata trasparenza PNG
- Timeout aumentati per file grandi
- Pulizia automatica file temporanei
- Messaggi errore più dettagliati per ogni convertitore

#### 📊 Statistiche
- **Convertitori:** 1 → 7 (+600%)
- **Formati input:** 2 → 12 estensioni
- **Formati output:** 1 → 3 tipi
- **Combinazioni:** 1 → 15+ conversioni
- **Linee codice:** ~5,500 → ~7,000

#### 🐛 Bug Fix
- Risolto: gestione PNG con trasparenza
- Risolto: timeout su file Excel grandi
- Migliorato: cleanup file temporanei
- Migliorato: error handling specifico per tipo

#### 📖 Documentazione
- `NOVITA_v2.0.md` - Guida completa novità
- README aggiornato con tutti i convertitori
- Esempi d'uso per ogni formato
- Guide troubleshooting specifiche

---

## [1.1.0] - 2026-01-09

### ⚡ PERFORMANCE UPDATE

#### 🚀 Miglioramenti Prestazioni
- **Avvio 5x più veloce**
  - Implementato lazy loading degli import
  - Inizializzazione convertitori in background
  - UI pronta in ~1 secondo invece di ~5-8 secondi
  
- **Conversioni più veloci su Windows**
  - Usa Microsoft Word installato (4x più veloce)
  - Rilevamento automatico Word vs LibreOffice
  - Fallback intelligente se Word non disponibile

#### ✨ Nuove Funzionalità
- **Rilevamento automatico metodo conversione**
  - Windows: prova prima Word, poi LibreOffice
  - Linux/macOS: usa LibreOffice
  - Messaggi chiari se software richiesto non trovato

#### 🔧 Ottimizzazioni Tecniche
- Lazy loading moduli core
- Import asincroni per velocità
- Inizializzazione background con QTimer
- Ridotto memory footprint iniziale

#### 📝 Dipendenze
- LibreOffice **NON PIÙ OBBLIGATORIO** su Windows (se Word presente)
- `docx2pdf` ora usato attivamente su Windows
- Tutte le altre dipendenze invariate

#### 🐛 Bug Fix
- Risolto: lentezza avvio applicazione
- Risolto: richiesta LibreOffice con Word installato
- Migliorato: gestione errori conversione

---

## [Unreleased]

### 🔮 Pianificato per Future Versioni

#### v1.1.0 (Prossima)
- [ ] Convertitore PDF → Word
- [ ] Convertitore PDF → Immagini
- [ ] Opzioni avanzate di conversione
- [ ] Previsualizzazione file

#### v1.2.0
- [ ] Convertitore Immagini → PDF
- [ ] Convertitore TXT → PDF
- [ ] Convertitore HTML → PDF
- [ ] Compressione PDF

#### v1.3.0
- [ ] Supporto Excel → PDF
- [ ] Supporto PowerPoint → PDF
- [ ] Merge PDF
- [ ] Split PDF

#### v2.0.0
- [ ] Interfaccia web opzionale
- [ ] API REST per conversioni
- [ ] Cloud storage integration
- [ ] Elaborazione massiva in cloud

---

## Note sulle Versioni

### Semantic Versioning
- **MAJOR**: Cambiamenti incompatibili con API precedenti
- **MINOR**: Nuove funzionalità retrocompatibili
- **PATCH**: Bug fix retrocompatibili

### Categorizzazione Modifiche
- **Aggiunte**: Nuove funzionalità
- **Modificate**: Cambiamenti a funzionalità esistenti
- **Deprecate**: Funzionalità che saranno rimosse
- **Rimosse**: Funzionalità rimosse
- **Corrette**: Bug fix
- **Sicurezza**: Vulnerabilità corrette
