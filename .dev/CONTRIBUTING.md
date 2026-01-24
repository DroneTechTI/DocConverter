# 🤝 Contribuire a DocConverter

Grazie per il tuo interesse nel contribuire a DocConverter! Questo documento fornisce linee guida per contribuire al progetto.

---

## 📋 Indice

1. [Come Contribuire](#come-contribuire)
2. [Segnalare Bug](#segnalare-bug)
3. [Proporre Nuove Funzionalità](#proporre-nuove-funzionalità)
4. [Sviluppo](#sviluppo)
5. [Aggiungere Convertitori](#aggiungere-convertitori)
6. [Standard di Codice](#standard-di-codice)
7. [Commit e Pull Request](#commit-e-pull-request)

---

## 🚀 Come Contribuire

Ci sono molti modi per contribuire:

- 🐛 **Segnalare bug**
- 💡 **Proporre nuove funzionalità**
- 📝 **Migliorare la documentazione**
- 🔧 **Scrivere codice**
- 🧪 **Aggiungere test**
- 🌍 **Tradurre l'interfaccia**

---

## 🐛 Segnalare Bug

Quando segnali un bug, includi:

1. **Versione** di DocConverter
2. **Sistema Operativo** (Windows, Linux, macOS + versione)
3. **Versione Python** (`python --version`)
4. **Descrizione dettagliata** del problema
5. **Passi per riprodurre** il bug
6. **Comportamento atteso** vs **comportamento effettivo**
7. **Log** (da `logs/docconverter.log`)
8. **Screenshot** se applicabile

### Template Bug Report

```markdown
**Versione DocConverter:** 1.0.0
**Sistema Operativo:** Windows 11
**Versione Python:** 3.11.5

**Descrizione:**
Quando provo a convertire un file .docx di grandi dimensioni...

**Passi per riprodurre:**
1. Apri DocConverter
2. Aggiungi file "documento_grande.docx" (50MB)
3. Clicca "Converti Tutto"
4. L'applicazione si blocca

**Comportamento atteso:**
Il file dovrebbe essere convertito normalmente

**Comportamento effettivo:**
L'applicazione si blocca dopo 30 secondi

**Log:**
[2026-01-09 10:00:00] ERROR - Timeout conversione...
```

---

## 💡 Proporre Nuove Funzionalità

Per proporre una nuova funzionalità:

1. **Cerca** se qualcuno l'ha già proposta
2. **Crea una Issue** con tag `enhancement`
3. **Spiega** il caso d'uso
4. **Descrivi** l'implementazione proposta (opzionale)

### Template Feature Request

```markdown
**Funzionalità richiesta:**
Supporto per conversione PDF → Word

**Motivazione:**
Molti utenti hanno bisogno di modificare PDF esistenti...

**Proposta di implementazione:**
Utilizzare la libreria `pdf2docx` per...

**Alternative considerate:**
- Usare `pdfplumber`
- Integrazione con API esterne
```

---

## 🛠️ Sviluppo

### Setup Ambiente di Sviluppo

```bash
# Clona il repository
git clone https://github.com/TUO_USERNAME/DocConverter.git
cd DocConverter

# Crea ambiente virtuale
python -m venv venv

# Attiva ambiente
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Installa dipendenze + dev dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Avvia applicazione
python main.py
```

### Struttura Branch

- `main`: Branch stabile (solo release)
- `develop`: Branch di sviluppo principale
- `feature/nome-feature`: Nuove funzionalità
- `bugfix/nome-bug`: Correzioni bug
- `hotfix/nome-hotfix`: Fix urgenti per produzione

---

## 🔧 Aggiungere Convertitori

Vedi `converters/README.md` per guida dettagliata.

### Checklist Nuovo Convertitore

- [ ] Creare file `converters/nuovo_convertitore.py`
- [ ] Ereditare da `ConverterBase`
- [ ] Implementare `get_info()`
- [ ] Implementare `convert()`
- [ ] Aggiungere gestione errori
- [ ] Usare `self._report_progress()`
- [ ] Aggiungere logging
- [ ] Registrare in `converters/__init__.py`
- [ ] Scrivere test in `tests/`
- [ ] Aggiornare `README.md`
- [ ] Aggiornare `CHANGELOG.md`

---

## 📏 Standard di Codice

### Stile Python

Seguiamo **PEP 8** con alcune eccezioni:

```python
# ✅ CORRETTO
def converti_documento(input_path: str, output_path: str) -> bool:
    """
    Converte un documento.
    
    Args:
        input_path: Path del file di input
        output_path: Path del file di output
    
    Returns:
        True se conversione riuscita
    """
    logger.info(f"Conversione: {input_path}")
    
    try:
        # Logica conversione
        return True
    except Exception as e:
        logger.error(f"Errore: {e}")
        return False

# ❌ ERRATO
def conv(i,o):  # Nomi poco chiari
    print("converting...")  # Usa logger, non print
    # Codice senza gestione errori
```

### Convenzioni Naming

- **Classi**: `PascalCase` (es. `WordToPDFConverter`)
- **Funzioni/Metodi**: `snake_case` (es. `convert_file`)
- **Costanti**: `UPPER_SNAKE_CASE` (es. `MAX_FILE_SIZE`)
- **Privati**: Prefisso `_` (es. `_internal_method`)

### Documentazione

```python
def metodo_complesso(param1: str, param2: int = 10) -> dict:
    """
    Breve descrizione (una riga).
    
    Descrizione dettagliata opzionale che spiega
    cosa fa il metodo in modo più approfondito.
    
    Args:
        param1: Descrizione parametro 1
        param2: Descrizione parametro 2 (default: 10)
    
    Returns:
        Dizionario con risultati
    
    Raises:
        ValueError: Se param1 è vuoto
        RuntimeError: In caso di errore runtime
    
    Example:
        >>> risultato = metodo_complesso("test", 20)
        >>> print(risultato['status'])
        'success'
    """
```

### Commenti

```python
# ✅ CORRETTO - Spiega PERCHÉ, non COSA
# Usiamo LibreOffice perché supporta più formati di Word
libreoffice_path = self._check_libreoffice()

# ❌ ERRATO - Ovvio dal codice
# Assegna il valore a x
x = 5
```

---

## 📝 Commit e Pull Request

### Messaggi di Commit

Usa **Conventional Commits**:

```
<tipo>(<scope>): <descrizione breve>

<descrizione dettagliata opzionale>

<footer opzionale>
```

**Tipi:**
- `feat`: Nuova funzionalità
- `fix`: Bug fix
- `docs`: Documentazione
- `style`: Formattazione
- `refactor`: Refactoring
- `test`: Test
- `chore`: Manutenzione

**Esempi:**

```bash
feat(converters): aggiungi supporto PDF to Word

Implementato nuovo convertitore che usa pdf2docx per
convertire file PDF in documenti Word modificabili.

Closes #42

---

fix(gui): risolvi crash con file grandi

Il thread di conversione andava in timeout con file >50MB.
Aumentato timeout a 120 secondi.

Fixes #38

---

docs(readme): aggiorna guida installazione Linux
```

### Pull Request

1. **Fork** il repository
2. Crea un **branch** da `develop`:
   ```bash
   git checkout -b feature/mia-funzionalita
   ```
3. **Sviluppa** e **testa** le modifiche
4. **Commit** con messaggi descrittivi
5. **Push** al tuo fork
6. Apri **Pull Request** verso `develop`

### Template Pull Request

```markdown
## Descrizione
Breve descrizione delle modifiche

## Tipo di modifica
- [ ] Bug fix
- [ ] Nuova funzionalità
- [ ] Breaking change
- [ ] Documentazione

## Checklist
- [ ] Il codice segue gli standard di progetto
- [ ] Ho commentato parti complesse
- [ ] Ho aggiornato la documentazione
- [ ] Ho aggiunto test
- [ ] Tutti i test passano
- [ ] Ho aggiornato CHANGELOG.md

## Test
Descrizione di come è stato testato

## Screenshot
(se applicabile)
```

---

## 🧪 Test

### Eseguire Test

```bash
# Tutti i test
python -m pytest tests/

# Test specifico
python -m pytest tests/test_converters.py

# Con coverage
python -m pytest --cov=. tests/
```

### Scrivere Test

```python
import unittest
from converters.mio_convertitore import MioConvertitore

class TestMioConvertitore(unittest.TestCase):
    def setUp(self):
        """Setup prima di ogni test"""
        self.converter = MioConvertitore()
    
    def test_conversion_success(self):
        """Test conversione riuscita"""
        result = self.converter.convert("input.txt", "output.pdf")
        self.assertTrue(result)
    
    def test_invalid_input(self):
        """Test input non valido"""
        with self.assertRaises(ConversionError):
            self.converter.convert("nonexistent.txt", "out.pdf")
```

---

## 🎨 UI e Design

Se modifichi l'interfaccia:

- Mantieni **coerenza** con lo stile esistente
- Testa su **diversi sistemi operativi**
- Verifica **accessibilità**
- Aggiungi **screenshot** nella PR

---

## 📄 Licenza

Contribuendo a DocConverter, accetti che il tuo codice sia rilasciato sotto licenza MIT.

---

## ❓ Domande?

Apri una **Discussion** su GitHub o contattaci via email.

---

**Grazie per contribuire a DocConverter! 🎉**
