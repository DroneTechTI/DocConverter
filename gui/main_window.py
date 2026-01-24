"""
Finestra principale di DocConverter
"""
import sys
from pathlib import Path
from typing import List, Optional

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QTextEdit,
    QGroupBox, QMessageBox, QStatusBar, QMenuBar,
    QMenu, QSplitter, QSizePolicy, QScrollArea, QFrame
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QIcon, QAction

from config.settings import Settings
from config.i18n import tr, set_language, get_available_languages, get_language
from config.user_settings import get_user_settings
from utils.logger import get_logger
from .widgets.file_list import FileListWidget
from .widgets.progress_bar import AdvancedProgressBar
from .styles.dark_theme import get_dark_theme


class ConversionThread(QThread):
    """Thread per eseguire conversioni senza bloccare la GUI"""
    
    # Signals
    progress_updated = pyqtSignal(int, str)
    file_completed = pyqtSignal(str, bool, str)  # file_path, success, message
    all_completed = pyqtSignal(int, int)  # successi, fallimenti
    
    def __init__(self, files: List[str], output_dir: str = None):
        super().__init__()
        self.files = files
        self.output_dir = output_dir
        self.logger = get_logger("ConversionThread")
        self._is_running = True
        
        # Lazy imports per velocità
        self.registry = None
        self.file_handler = None
    
    def run(self):
        """Esegue le conversioni con ottimizzazioni memoria"""
        # Import solo quando necessario (velocizza avvio)
        from core.converter_registry import get_registry
        from utils.file_handler import FileHandler
        from utils.error_handler import ConversionError
        from utils.memory_optimizer import get_memory_optimizer
        
        self.registry = get_registry()
        self.file_handler = FileHandler()
        memory_optimizer = get_memory_optimizer()
        
        total_files = len(self.files)
        successes = 0
        failures = 0
        
        # Log memoria iniziale
        memory_optimizer.log_memory_stats()
        
        for i, file_path in enumerate(self.files):
            if not self._is_running:
                self.logger.info("Conversione interrotta dall'utente")
                break
            
            try:
                # Aggiorna progresso generale
                overall_progress = int((i / total_files) * 100)
                self.progress_updated.emit(
                    overall_progress,
                    f"Conversione file {i+1}/{total_files}: {Path(file_path).name}"
                )
                
                # Trova convertitore appropriato
                converter = self.registry.get_converter_for_file(file_path, '.pdf')
                
                if not converter:
                    raise ConversionError(
                        f"Nessun convertitore disponibile per {Path(file_path).suffix}",
                        file_path=file_path
                    )
                
                # Genera path output
                output_path = self.file_handler.generate_output_path(
                    file_path,
                    self.output_dir,
                    converter.get_output_extension()
                )
                
                # Esegui conversione
                self.logger.info(f"Conversione {i+1}/{total_files}: {file_path}")
                
                # Converti stringhe in Path per compatibilità
                success = converter.convert(
                    Path(file_path),
                    Path(output_path),
                    progress_callback=self._file_progress_callback
                )
                
                if success:
                    successes += 1
                    self.file_completed.emit(
                        file_path,
                        True,
                        f"✓ Salvato: {output_path}"
                    )
                else:
                    failures += 1
                    self.file_completed.emit(
                        file_path,
                        False,
                        "✗ Conversione fallita"
                    )
            
            except Exception as e:
                failures += 1
                error_msg = str(e)
                self.logger.error(f"Errore conversione {file_path}: {error_msg}")
                self.file_completed.emit(file_path, False, f"✗ {error_msg}")
            
            # Ottimizza memoria ogni 5 file
            if (i + 1) % 5 == 0:
                memory_optimizer.optimize_memory()
        
        # Conversione completata - cleanup finale
        memory_optimizer.optimize_memory(aggressive=True)
        final_progress = 100
        self.progress_updated.emit(
            final_progress,
            f"Completato: {successes} successi, {failures} errori"
        )
        self.all_completed.emit(successes, failures)
    
    def _file_progress_callback(self, percentage: int, message: str):
        """Callback per progresso singolo file"""
        # Qui potremmo aggiornare un progresso più dettagliato se necessario
        pass
    
    def stop(self):
        """Ferma il thread"""
        self._is_running = False


class MainWindow(QMainWindow):
    """
    Finestra principale dell'applicazione DocConverter.
    
    Gestisce l'interfaccia utente e coordina le operazioni di conversione.
    """
    
    def __init__(self):
        super().__init__()
        
        self.logger = get_logger("MainWindow")
        
        # Load user settings (language, etc.)
        user_settings = get_user_settings()
        saved_language = user_settings.get_language()
        set_language(saved_language)
        self.logger.info(f"Loaded language: {saved_language}")
        
        # Lazy loading per velocizzare avvio
        self.registry = None
        self.dependency_checker = None
        self.file_handler = None
        self.error_handler = None
        
        self.conversion_thread: Optional[ConversionThread] = None
        self.output_directory: Optional[str] = None
        
        # Setup UI (veloce)
        self._init_ui()
        
        # Inizializza convertitori in background
        QTimer.singleShot(100, self._initialize_converters_lazy)
        
        self.logger.info("MainWindow inizializzata")
    
    def _initialize_converters_lazy(self):
        """Inizializza convertitori in background dopo l'avvio"""
        # Import lazy per velocizzare avvio
        from core.converter_registry import get_registry
        from core.dependency_checker import DependencyChecker
        from utils.file_handler import FileHandler
        from utils.error_handler import ErrorHandler
        from converters import AVAILABLE_CONVERTERS
        
        self.logger.info("Inizializzazione convertitori in background...")
        
        # Inizializza moduli
        self.registry = get_registry()
        self.dependency_checker = DependencyChecker()
        self.file_handler = FileHandler()
        self.error_handler = ErrorHandler()
        
        # Registra convertitori
        for converter_class in AVAILABLE_CONVERTERS:
            try:
                self.registry.register(converter_class)
            except Exception as e:
                self.logger.error(f"Errore registrazione convertitore: {e}")
        
        self.logger.info(f"Convertitori registrati: {len(self.registry)}")
        self.status_bar.showMessage("Pronto - Convertitori caricati")
    
    def _init_ui(self):
        """Inizializza l'interfaccia utente"""
        # Configurazione finestra
        self.setWindowTitle(f"{Settings.APP_NAME} v{Settings.APP_VERSION}")
        self.setMinimumSize(Settings.WINDOW_MIN_WIDTH, Settings.WINDOW_MIN_HEIGHT)
        self.resize(Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT)
        
        # 🎨 Imposta icona app (barra applicazioni)
        icon_path = Settings.BASE_DIR / "assets" / "icon.ico"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
            self.logger.info(f"✅ Icona caricata: {icon_path}")
        else:
            self.logger.warning(f"⚠️ Icona non trovata: {icon_path}")
        
        # Applica tema
        self.setStyleSheet(get_dark_theme())
        
        # Widget centrale
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principale
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Header
        header = self._create_header()
        main_layout.addWidget(header)
        
        # Splitter per area file e log
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Area file
        file_area = self._create_file_area()
        splitter.addWidget(file_area)
        
        # Area log
        log_area = self._create_log_area()
        splitter.addWidget(log_area)
        
        # Imposta proporzioni iniziali
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)
        
        main_layout.addWidget(splitter)
        
        # Progress bar
        self.progress_bar = AdvancedProgressBar()
        main_layout.addWidget(self.progress_bar)
        
        # Pulsanti azione
        action_buttons = self._create_action_buttons()
        main_layout.addLayout(action_buttons)
        
        central_widget.setLayout(main_layout)
        
        # Menu bar
        self._create_menu_bar()
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Pronto")
    
    def _create_header(self) -> QWidget:
        """Crea l'header con titolo e info"""
        header = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(5)
        
        # Titolo
        title = QLabel("📄 DocConverter")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Sottotitolo
        subtitle = QLabel(tr("app_description"))
        subtitle.setObjectName("infoLabel")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        header.setLayout(layout)
        return header
    
    def _create_file_area(self) -> QGroupBox:
        """Crea l'area di gestione file"""
        group = QGroupBox("Files to Convert" if tr("app_title") else "File da Convertire")
        layout = QVBoxLayout()
        
        # === QUICK CONVERSION (DROPDOWN MENU) ===
        quick_group = QGroupBox(tr("quick_conversion"))
        quick_layout = QVBoxLayout()  # Cambiato a Vertical per meglio responsive
        
        from PyQt6.QtWidgets import QComboBox
        self.quick_combo = QComboBox()
        self.quick_combo.setMinimumHeight(35)  # Altezza minima per visibilità
        self.quick_combo.addItems([
            tr("select_conversion"),
            tr("conversion_word_pdf"),
            tr("conversion_pdf_word"),
            tr("conversion_excel_pdf"),
            tr("conversion_ppt_pdf"),
            tr("conversion_img_pdf"),
            tr("conversion_merge_pdf"),
            tr("conversion_compress_pdf")
        ])
        self.quick_combo.currentTextChanged.connect(self._on_quick_conversion_selected)
        quick_layout.addWidget(self.quick_combo)
        
        quick_group.setLayout(quick_layout)
        layout.addWidget(quick_group)
        
        
        # Separator
        from PyQt6.QtWidgets import QFrame
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separator)
        
        # Lista file con drag & drop
        self.file_list = FileListWidget()
        self.file_list.filesDropped.connect(self._on_files_dropped)
        layout.addWidget(self.file_list)
        
        # Pulsanti gestione file
        file_buttons = QHBoxLayout()
        
        self.btn_add_files = QPushButton(tr("btn_add_files"))
        self.btn_add_files.setToolTip(tr("tooltip_add_files"))
        self.btn_add_files.setShortcut("Ctrl+O")
        self.btn_add_files.clicked.connect(self._on_add_files)
        file_buttons.addWidget(self.btn_add_files)
        
        self.btn_select_output = QPushButton(tr("btn_select_output"))
        self.btn_select_output.clicked.connect(self._on_select_output_dir)
        file_buttons.addWidget(self.btn_select_output)
        
        self.btn_remove_files = QPushButton("🗑️ Remove Selected")
        self.btn_remove_files.clicked.connect(self._on_remove_files)
        file_buttons.addWidget(self.btn_remove_files)
        
        self.btn_clear_files = QPushButton(tr("btn_clear"))
        self.btn_clear_files.setObjectName("clearButton")
        self.btn_clear_files.clicked.connect(self._on_clear_files)
        file_buttons.addWidget(self.btn_clear_files)
        
        layout.addLayout(file_buttons)
        
        # Label output directory
        self.output_dir_label = QLabel("Output: same folder as input files")
        self.output_dir_label.setObjectName("infoLabel")
        layout.addWidget(self.output_dir_label)
        
        group.setLayout(layout)
        return group
    
    def _create_log_area(self) -> QGroupBox:
        """Crea l'area log"""
        group = QGroupBox("Operations Log")
        layout = QVBoxLayout()
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)
        layout.addWidget(self.log_text)
        
        group.setLayout(layout)
        return group
    
    def _create_action_buttons(self) -> QHBoxLayout:
        """Crea i pulsanti di azione principali"""
        layout = QHBoxLayout()
        
        self.btn_convert = QPushButton(tr("btn_convert_all"))
        self.btn_convert.setObjectName("convertButton")
        self.btn_convert.setToolTip(tr("tooltip_convert"))
        self.btn_convert.setShortcut("Ctrl+Return")
        self.btn_convert.clicked.connect(self._on_convert)
        self.btn_convert.setEnabled(False)
        layout.addWidget(self.btn_convert)
        
        return layout
    
    def _create_menu_bar(self):
        """Crea la menu bar"""
        menubar = self.menuBar()
        
        # Menu File
        file_menu = menubar.addMenu("&File")
        
        add_action = QAction(tr("menu_add_files"), self)
        add_action.setShortcut("Ctrl+O")
        add_action.setStatusTip(tr("menu_add_files"))
        add_action.triggered.connect(self._on_add_files)
        file_menu.addAction(add_action)
        
        clear_action = QAction(tr("menu_clear_list"), self)
        clear_action.setShortcut("Ctrl+L")
        clear_action.setStatusTip(tr("menu_clear_list"))
        clear_action.triggered.connect(self._on_clear_files)
        file_menu.addAction(clear_action)
        
        file_menu.addSeparator()
        
        convert_action = QAction(tr("menu_convert"), self)
        convert_action.setShortcut("Ctrl+Return")
        convert_action.setStatusTip(tr("menu_convert"))
        convert_action.triggered.connect(self._on_convert)
        file_menu.addAction(convert_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction(tr("menu_exit"), self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip(tr("menu_exit"))
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Menu Language
        lang_menu = menubar.addMenu("🌍 &Language")
        
        from PyQt6.QtGui import QActionGroup
        lang_group = QActionGroup(self)
        lang_group.setExclusive(True)
        
        current_lang = get_language()  # Get current language
        
        for lang_code, lang_name in get_available_languages().items():
            lang_action = QAction(lang_name, self)
            lang_action.setCheckable(True)
            if lang_code == current_lang:  # Check current language
                lang_action.setChecked(True)
            lang_action.triggered.connect(lambda checked, code=lang_code: self._change_language(code))
            lang_group.addAction(lang_action)
            lang_menu.addAction(lang_action)
        
        # Menu Tools
        tools_menu = menubar.addMenu(tr("menu_tools"))
        
        merge_action = QAction(tr("menu_merge_pdf"), self)
        merge_action.setShortcut("Ctrl+M")
        merge_action.setStatusTip(tr("menu_merge_pdf"))
        merge_action.triggered.connect(self._merge_pdfs)
        tools_menu.addAction(merge_action)
        
        compress_action = QAction(tr("menu_compress_pdf"), self)
        compress_action.setShortcut("Ctrl+Shift+C")
        compress_action.setStatusTip(tr("menu_compress_pdf"))
        compress_action.triggered.connect(lambda: self._quick_conversion('.pdf', '.pdf', compress=True))
        tools_menu.addAction(compress_action)
        
        # Menu Help
        help_menu = menubar.addMenu(tr("menu_help"))
        
        about_action = QAction(tr("menu_about"), self)
        about_action.setShortcut("F1")
        about_action.setStatusTip(tr("menu_about"))
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
        
        deps_action = QAction(tr("menu_check_deps"), self)
        deps_action.setStatusTip(tr("menu_check_deps"))
        deps_action.triggered.connect(self._check_dependencies)
        help_menu.addAction(deps_action)
    
    def _quick_conversion(self, input_ext: str, output_ext: str, compress: bool = False):
        """Conversione rapida con selezione file guidata"""
        # Definisci filtri in base al tipo
        filter_map = {
            '.docx': "Documenti Word (*.doc *.docx)",
            '.pdf': "Documenti PDF (*.pdf)",
            '.xlsx': "Fogli Excel (*.xlsx *.xls)",
            '.pptx': "Presentazioni PowerPoint (*.pptx *.ppt)",
            '.png': "Immagini (*.png *.jpg *.jpeg *.bmp *.gif)"
        }
        
        file_filter = filter_map.get(input_ext, "Tutti i file (*.*)")
        
        # Se è compressione PDF, usa convertitore speciale
        if compress and input_ext == '.pdf':
            files, _ = QFileDialog.getOpenFileNames(
                self,
                "Seleziona PDF da comprimere",
                "",
                "Documenti PDF (*.pdf);;Tutti i file (*.*)"
            )
            
            if files:
                self._compress_pdfs(files)
            return
        
        files, _ = QFileDialog.getOpenFileNames(
            self,
            f"Seleziona file per conversione {input_ext}→{output_ext}",
            "",
            f"{file_filter};;Tutti i file (*.*)"
        )
        
        if files:
            self._add_files_to_list(files)
            # Se ci sono file, converti automaticamente
            if not self.file_list.is_empty():
                self.log(f"🎯 Conversione rapida: {input_ext}→{output_ext}")
                QTimer.singleShot(200, self._on_convert)
    
    def _on_add_files(self):
        """Gestisce l'aggiunta di file"""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Seleziona File da Convertire",
            "",
            "Word (*.doc *.docx);;PDF (*.pdf);;Excel (*.xlsx *.xls);;"
            "PowerPoint (*.pptx *.ppt);;Immagini (*.png *.jpg *.jpeg *.bmp);;Tutti (*.*)"
        )
        
        if files:
            self._add_files_to_list(files)
    
    def _on_files_dropped(self, files: List[str]):
        """Gestisce file droppati"""
        self._add_files_to_list(files)
    
    def _add_files_to_list(self, files: List[str]):
        """Aggiunge file alla lista con validazione"""
        # Assicura inizializzazione
        if not self.file_handler:
            from utils.file_handler import FileHandler
            self.file_handler = FileHandler()
        if not self.registry:
            from core.converter_registry import get_registry
            self.registry = get_registry()
        
        valid_files = []
        invalid_files = []
        
        for file_path in files:
            # Valida file
            is_valid, error = self.file_handler.validate_file(file_path)
            
            if is_valid:
                # Verifica se il formato è supportato
                if self.registry.is_format_supported(
                    self.file_handler.get_file_extension(file_path)
                ):
                    valid_files.append(file_path)
                else:
                    invalid_files.append((file_path, "Formato non supportato"))
            else:
                invalid_files.append((file_path, error))
        
        # Aggiungi file validi
        if valid_files:
            self.file_list.add_files(valid_files)
            self.log(f"✓ Aggiunti {len(valid_files)} file")
            self._update_ui_state()
        
        # Mostra errori
        if invalid_files:
            error_msg = "File non validi:\n\n"
            for file_path, error in invalid_files[:5]:  # Max 5 errori
                error_msg += f"• {Path(file_path).name}: {error}\n"
            
            if len(invalid_files) > 5:
                error_msg += f"\n... e altri {len(invalid_files) - 5}"
            
            QMessageBox.warning(self, "File Non Validi", error_msg)
    
    def _on_remove_files(self):
        """Rimuove file selezionati"""
        removed = self.file_list.remove_selected_files()
        if removed:
            self.log(f"✓ Rimossi {len(removed)} file")
            self._update_ui_state()
    
    def _on_clear_files(self):
        """Pulisce tutta la lista"""
        if self.file_list.is_empty():
            return
        
        reply = QMessageBox.question(
            self,
            "Conferma",
            "Rimuovere tutti i file dalla lista?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            count = self.file_list.get_file_count()
            self.file_list.clear_all_files()
            self.log(f"✓ Lista pulita ({count} file rimossi)")
            self._update_ui_state()
    
    def _on_select_output_dir(self):
        """Seleziona directory di output"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Seleziona Cartella di Output"
        )
        
        if directory:
            self.output_directory = directory
            self.output_dir_label.setText(f"Output: {directory}")
            self.log(f"✓ Cartella output: {directory}")
    
    def _on_convert(self):
        """Avvia conversione"""
        files = self.file_list.get_all_file_paths()
        
        if not files:
            QMessageBox.warning(self, "Attenzione", "Nessun file da convertire")
            return
        
        # Reset UI
        self.file_list.reset_all_statuses()
        self.progress_bar.reset()
        self.progress_bar.clear_state_style()
        
        # Disabilita UI durante conversione
        self._set_ui_enabled(False)
        
        self.log(f"🚀 Avvio conversione di {len(files)} file...")
        
        # Crea e avvia thread
        self.conversion_thread = ConversionThread(files, self.output_directory)
        self.conversion_thread.progress_updated.connect(self._on_progress_updated)
        self.conversion_thread.file_completed.connect(self._on_file_completed)
        self.conversion_thread.all_completed.connect(self._on_all_completed)
        self.conversion_thread.start()
    
    def _on_progress_updated(self, percentage: int, message: str):
        """Aggiorna progresso"""
        self.progress_bar.set_progress(percentage, message)
        self.status_bar.showMessage(message)
    
    def _on_file_completed(self, file_path: str, success: bool, message: str):
        """Gestisce completamento singolo file"""
        # Aggiorna lista
        status_icon = "✓" if success else "✗"
        color = "#2ecc71" if success else "#e74c3c"
        self.file_list.update_item_status(file_path, status_icon, color)
        
        # Log
        self.log(f"{Path(file_path).name}: {message}")
    
    def _on_all_completed(self, successes: int, failures: int):
        """Gestisce completamento totale"""
        self._set_ui_enabled(True)
        
        total = successes + failures
        
        if failures == 0:
            self.progress_bar.set_success_state(f"✓ {successes}/{total} convertiti!")
            self.log(f"✅ Conversione completata: {successes} successi")
            
            QMessageBox.information(
                self,
                "Completato",
                f"Conversione completata con successo!\n\n"
                f"File convertiti: {successes}/{total}"
            )
        else:
            self.progress_bar.set_error_state(f"Completato con {failures} errori")
            self.log(f"⚠️ Conversione completata: {successes} successi, {failures} errori")
            
            QMessageBox.warning(
                self,
                "Completato con Errori",
                f"Conversione completata con alcuni errori.\n\n"
                f"Successi: {successes}\n"
                f"Errori: {failures}\n\n"
                f"Controlla il log per dettagli."
            )
    
    def _update_ui_state(self):
        """Aggiorna stato UI in base ai file presenti"""
        has_files = not self.file_list.is_empty()
        self.btn_convert.setEnabled(has_files)
        
        count = self.file_list.get_file_count()
        if count > 0:
            self.status_bar.showMessage(f"{count} file pronti per la conversione")
        else:
            self.status_bar.showMessage("Pronto")
    
    def _set_ui_enabled(self, enabled: bool):
        """Abilita/disabilita UI durante conversione"""
        self.btn_add_files.setEnabled(enabled)
        self.btn_remove_files.setEnabled(enabled)
        self.btn_clear_files.setEnabled(enabled)
        self.btn_select_output.setEnabled(enabled)
        self.btn_convert.setEnabled(enabled and not self.file_list.is_empty())
    
    def _merge_pdfs(self):
        """Unisce più PDF in uno solo"""
        from pathlib import Path
        
        # Seleziona PDF da unire
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Seleziona PDF da unire (in ordine)",
            "",
            "Documenti PDF (*.pdf)"
        )
        
        if not files or len(files) < 2:
            if len(files) == 1:
                QMessageBox.warning(
                    self,
                    "Attenzione",
                    "Seleziona almeno 2 file PDF da unire"
                )
            return
        
        # Chiedi nome file output
        output_file, _ = QFileDialog.getSaveFileName(
            self,
            "Salva PDF unificato",
            "merged.pdf",
            "PDF (*.pdf)"
        )
        
        if not output_file:
            return
        
        try:
            from converters.pdf_merge import PDFMergeConverter
            
            self.log(f"📑 Unione di {len(files)} file PDF...")
            self._set_ui_enabled(False)
            self.progress_bar.reset()
            
            # Crea convertitore e unisci
            merger = PDFMergeConverter()
            pdf_paths = [Path(f) for f in files]
            
            success = merger.merge_pdfs(
                pdf_paths,
                Path(output_file),
                progress_callback=self._on_progress_updated
            )
            
            self._set_ui_enabled(True)
            
            if success:
                self.progress_bar.set_success_state("✓ PDF unificato!")
                self.log(f"✅ PDF unificato salvato: {output_file}")
                QMessageBox.information(
                    self,
                    "Completato",
                    f"PDF unificato con successo!\n\n"
                    f"File: {Path(output_file).name}\n"
                    f"PDF uniti: {len(files)}"
                )
            else:
                self.progress_bar.set_error_state("Errore")
                self.log("❌ Errore durante l'unione")
        
        except Exception as e:
            self._set_ui_enabled(True)
            self.progress_bar.set_error_state("Errore")
            self.log(f"❌ Errore: {str(e)}")
            QMessageBox.critical(
                self,
                "Errore",
                f"Errore durante l'unione PDF:\n\n{str(e)}"
            )
    
    def _compress_pdfs(self, files: list):
        """Comprime PDF selezionati"""
        from pathlib import Path
        from converters.pdf_compress import PDFCompressConverter
        
        if not files:
            return
        
        # Chiedi cartella output
        output_dir = QFileDialog.getExistingDirectory(
            self,
            "Seleziona cartella per PDF compressi"
        )
        
        if not output_dir:
            return
        
        try:
            self.log(f"🗜️ Compressione di {len(files)} PDF...")
            self._set_ui_enabled(False)
            self.progress_bar.reset()
            
            compressor = PDFCompressConverter()
            successes = 0
            failures = 0
            
            for i, file_path in enumerate(files):
                try:
                    input_path = Path(file_path)
                    output_path = Path(output_dir) / f"{input_path.stem}_compressed.pdf"
                    
                    progress = int((i / len(files)) * 100)
                    self.progress_bar.set_progress(
                        progress,
                        f"Compressione {i+1}/{len(files)}: {input_path.name}"
                    )
                    
                    success = compressor.convert(input_path, output_path)
                    
                    if success:
                        successes += 1
                        self.log(f"✓ Compresso: {input_path.name}")
                    else:
                        failures += 1
                        self.log(f"✗ Errore: {input_path.name}")
                
                except Exception as e:
                    failures += 1
                    self.log(f"✗ Errore {Path(file_path).name}: {str(e)}")
            
            self._set_ui_enabled(True)
            
            if failures == 0:
                self.progress_bar.set_success_state(f"✓ {successes} PDF compressi!")
                self.log(f"✅ Compressione completata: {successes} file")
                QMessageBox.information(
                    self,
                    "Completato",
                    f"Compressione completata!\n\n"
                    f"File compressi: {successes}\n"
                    f"Cartella: {output_dir}"
                )
            else:
                self.progress_bar.set_error_state(f"Completato con {failures} errori")
                self.log(f"⚠️ Completato: {successes} successi, {failures} errori")
                QMessageBox.warning(
                    self,
                    "Completato con errori",
                    f"Successi: {successes}\nErrori: {failures}"
                )
        
        except Exception as e:
            self._set_ui_enabled(True)
            self.progress_bar.set_error_state("Errore")
            self.log(f"❌ Errore: {str(e)}")
            QMessageBox.critical(
                self,
                "Errore",
                f"Errore durante la compressione:\n\n{str(e)}"
            )
    
    def _on_quick_conversion_selected(self, text: str):
        """Gestisce selezione dal menu a tendina conversione rapida"""
        if text == "Seleziona...":
            return
        
        # Reset combo
        self.quick_combo.setCurrentIndex(0)
        
        # Esegui conversione in base alla selezione
        if "Word → PDF" in text:
            self._quick_conversion('.docx', '.pdf')
        elif "PDF → Word" in text:
            self._quick_conversion('.pdf', '.docx')
        elif "Excel → PDF" in text:
            self._quick_conversion('.xlsx', '.pdf')
        elif "PowerPoint → PDF" in text:
            self._quick_conversion('.pptx', '.pdf')
        elif "Immagini → PDF" in text:
            self._quick_conversion('.png', '.pdf')
        elif "Unisci PDF" in text:
            self._merge_pdfs()
        elif "Comprimi PDF" in text:
            self._quick_conversion('.pdf', '.pdf', compress=True)
    
    def _change_language(self, lang_code: str):
        """Change application language"""
        from config.user_settings import get_user_settings
        
        # Save language preference
        user_settings = get_user_settings()
        user_settings.set_language(lang_code)
        
        set_language(lang_code)
        
        self.logger.info(f"Language changed to: {lang_code}")
        
        # Show message - requires restart
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.information(
            self,
            "Language Changed" if lang_code == "en" else "Lingua Cambiata",
            "Please restart the application to apply language changes." if lang_code == "en" 
            else "Riavvia l'applicazione per applicare la lingua."
        )
    
    def _check_dependencies(self):
        """Verifica dipendenze sistema"""
        # Assicura inizializzazione
        if not self.dependency_checker:
            from core.dependency_checker import DependencyChecker
            self.dependency_checker = DependencyChecker()
        
        self.log("🔍 Controllo dipendenze...")
        
        results = self.dependency_checker.check_all_dependencies()
        
        message = "Stato Dipendenze:\n\n"
        all_ok = True
        
        for dep_name, (is_available, path_or_msg) in results.items():
            if is_available:
                message += f"✓ {dep_name}: OK\n  Path: {path_or_msg}\n\n"
                self.log(f"✓ {dep_name}: disponibile")
            else:
                message += f"✗ {dep_name}: NON TROVATO\n  {path_or_msg}\n\n"
                self.log(f"✗ {dep_name}: non disponibile")
                all_ok = False
        
        if all_ok:
            QMessageBox.information(self, "Dipendenze OK", message)
        else:
            QMessageBox.warning(self, "Dipendenze Mancanti", message)
    
    def _show_about(self):
        """Mostra dialog about"""
        # Assicura inizializzazione
        if not self.registry:
            from core.converter_registry import get_registry
            self.registry = get_registry()
        
        about_text = f"""
        <h2>{Settings.APP_NAME}</h2>
        <p><b>Versione:</b> {Settings.APP_VERSION}</p>
        <p><b>Descrizione:</b> Software professionale per conversione documenti</p>
        <br>
        <p><b>Convertitori disponibili:</b></p>
        <ul>
        """
        
        for converter in self.registry.get_all_converters():
            info = converter.get_info()
            about_text += f"<li>{info['name']}: "
            about_text += f"{', '.join(info['input_formats'])} → "
            about_text += f"{info['output_format']}</li>"
        
        about_text += """
        </ul>
        <br>
        <p>Sviluppato con ❤️ usando Python e PyQt6</p>
        """
        
        QMessageBox.about(self, "Informazioni", about_text)
    
    def log(self, message: str):
        """Aggiunge messaggio al log"""
        self.log_text.append(message)
        # Auto-scroll
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )
    
    def closeEvent(self, event):
        """Gestisce chiusura finestra"""
        # Se conversione in corso, chiedi conferma
        if self.conversion_thread and self.conversion_thread.isRunning():
            reply = QMessageBox.question(
                self,
                "Conversione in Corso",
                "Una conversione è in corso. Vuoi interromperla e uscire?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.conversion_thread.stop()
                self.conversion_thread.wait()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()
