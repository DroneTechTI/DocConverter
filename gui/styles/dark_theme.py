"""
Tema scuro moderno per DocConverter
"""


def get_dark_theme() -> str:
    """
    Ritorna il foglio di stile CSS per il tema scuro.
    
    Returns:
        Stringa QSS (Qt Style Sheet)
    """
    return """
    /* ===== GENERALE ===== */
    QWidget {
        background-color: #1e1e1e;
        color: #e0e0e0;
        font-family: "Segoe UI", "Ubuntu", "Arial", sans-serif;
        font-size: 10pt;
    }
    
    /* ===== FINESTRA PRINCIPALE ===== */
    QMainWindow {
        background-color: #1e1e1e;
    }
    
    /* ===== PULSANTI ===== */
    QPushButton {
        background-color: #0d7377;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: bold;
        min-width: 100px;
    }
    
    QPushButton:hover {
        background-color: #14a085;
    }
    
    QPushButton:pressed {
        background-color: #0a5f63;
    }
    
    QPushButton:disabled {
        background-color: #3a3a3a;
        color: #707070;
    }
    
    QPushButton#convertButton {
        background-color: #2ecc71;
        font-size: 11pt;
        padding: 12px 30px;
        min-height: 40px;
    }
    
    QPushButton#convertButton:hover {
        background-color: #27ae60;
    }
    
    QPushButton#convertButton:pressed {
        background-color: #229954;
    }
    
    QPushButton#clearButton {
        background-color: #e74c3c;
    }
    
    QPushButton#clearButton:hover {
        background-color: #c0392b;
    }
    
    /* ===== LISTE ===== */
    QListWidget {
        background-color: #2b2b2b;
        border: 2px solid #3a3a3a;
        border-radius: 5px;
        padding: 10px;
        outline: none;
    }
    
    QListWidget::item {
        padding: 8px;
        border-radius: 3px;
        margin: 2px 0px;
    }
    
    QListWidget::item:hover {
        background-color: #3a3a3a;
    }
    
    QListWidget::item:selected {
        background-color: #0d7377;
        color: white;
    }
    
    /* ===== BARRA DI PROGRESSO ===== */
    QProgressBar {
        border: 2px solid #3a3a3a;
        border-radius: 5px;
        text-align: center;
        background-color: #2b2b2b;
        color: white;
        font-weight: bold;
        min-height: 25px;
    }
    
    QProgressBar::chunk {
        background-color: qlineargradient(
            x1:0, y1:0, x2:1, y2:0,
            stop:0 #0d7377,
            stop:1 #14a085
        );
        border-radius: 3px;
    }
    
    /* ===== LABEL ===== */
    QLabel {
        color: #e0e0e0;
        background: transparent;
    }
    
    QLabel#titleLabel {
        font-size: 18pt;
        font-weight: bold;
        color: #14a085;
        padding: 10px;
    }
    
    QLabel#infoLabel {
        color: #a0a0a0;
        font-size: 9pt;
        font-style: italic;
    }
    
    QLabel#statusLabel {
        color: #14a085;
        font-weight: bold;
    }
    
    /* ===== TEXT EDIT (LOG) ===== */
    QTextEdit {
        background-color: #1a1a1a;
        border: 2px solid #3a3a3a;
        border-radius: 5px;
        padding: 10px;
        color: #d0d0d0;
        font-family: "Consolas", "Monaco", "Courier New", monospace;
        font-size: 9pt;
    }
    
    /* ===== GROUP BOX ===== */
    QGroupBox {
        border: 2px solid #3a3a3a;
        border-radius: 5px;
        margin-top: 10px;
        padding-top: 15px;
        font-weight: bold;
        color: #14a085;
    }
    
    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 5px 10px;
        color: #14a085;
    }
    
    /* ===== LINE EDIT ===== */
    QLineEdit {
        background-color: #2b2b2b;
        border: 2px solid #3a3a3a;
        border-radius: 5px;
        padding: 8px;
        color: #e0e0e0;
    }
    
    QLineEdit:focus {
        border: 2px solid #0d7377;
    }
    
    /* ===== COMBO BOX ===== */
    QComboBox {
        background-color: #2b2b2b;
        border: 2px solid #3a3a3a;
        border-radius: 5px;
        padding: 8px;
        color: #e0e0e0;
        min-width: 150px;
    }
    
    QComboBox:hover {
        border: 2px solid #0d7377;
    }
    
    QComboBox::drop-down {
        border: none;
        width: 30px;
    }
    
    QComboBox::down-arrow {
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 5px solid #e0e0e0;
        width: 0;
        height: 0;
    }
    
    QComboBox QAbstractItemView {
        background-color: #2b2b2b;
        border: 2px solid #0d7377;
        selection-background-color: #0d7377;
        color: #e0e0e0;
    }
    
    /* ===== SCROLL BAR ===== */
    QScrollBar:vertical {
        background-color: #2b2b2b;
        width: 12px;
        border-radius: 6px;
    }
    
    QScrollBar::handle:vertical {
        background-color: #0d7377;
        border-radius: 6px;
        min-height: 20px;
    }
    
    QScrollBar::handle:vertical:hover {
        background-color: #14a085;
    }
    
    QScrollBar::add-line:vertical,
    QScrollBar::sub-line:vertical {
        height: 0px;
    }
    
    QScrollBar:horizontal {
        background-color: #2b2b2b;
        height: 12px;
        border-radius: 6px;
    }
    
    QScrollBar::handle:horizontal {
        background-color: #0d7377;
        border-radius: 6px;
        min-width: 20px;
    }
    
    QScrollBar::handle:horizontal:hover {
        background-color: #14a085;
    }
    
    /* ===== MENU BAR ===== */
    QMenuBar {
        background-color: #252525;
        color: #e0e0e0;
        padding: 5px;
    }
    
    QMenuBar::item {
        padding: 5px 10px;
        background: transparent;
    }
    
    QMenuBar::item:selected {
        background-color: #0d7377;
    }
    
    QMenu {
        background-color: #2b2b2b;
        border: 2px solid #3a3a3a;
        color: #e0e0e0;
    }
    
    QMenu::item {
        padding: 8px 25px;
    }
    
    QMenu::item:selected {
        background-color: #0d7377;
    }
    
    /* ===== TOOLTIPS ===== */
    QToolTip {
        background-color: #2b2b2b;
        border: 2px solid #0d7377;
        color: #e0e0e0;
        padding: 5px;
        border-radius: 3px;
    }
    
    /* ===== SEPARATORI ===== */
    QFrame[frameShape="4"],
    QFrame[frameShape="5"] {
        color: #3a3a3a;
    }
    
    /* ===== STATUS BAR ===== */
    QStatusBar {
        background-color: #252525;
        color: #a0a0a0;
        border-top: 1px solid #3a3a3a;
    }
    """


def get_light_theme() -> str:
    """
    Ritorna il foglio di stile CSS per il tema chiaro.
    
    Returns:
        Stringa QSS (Qt Style Sheet)
    """
    return """
    /* Tema chiaro - Da implementare se richiesto */
    QWidget {
        background-color: #f5f5f5;
        color: #2c3e50;
    }
    
    QPushButton {
        background-color: #3498db;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: bold;
    }
    
    QPushButton:hover {
        background-color: #2980b9;
    }
    """
