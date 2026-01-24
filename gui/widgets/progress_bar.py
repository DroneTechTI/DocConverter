"""
Barra di progresso avanzata con stato
"""
from PyQt6.QtWidgets import QProgressBar, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, pyqtSignal

from utils.logger import get_logger


class AdvancedProgressBar(QWidget):
    """
    Barra di progresso con etichetta di stato.
    
    Combina una progress bar con un'etichetta che mostra
    informazioni dettagliate sullo stato corrente.
    """
    
    # Signals
    completed = pyqtSignal()
    
    def __init__(self, parent=None):
        """Inizializza la progress bar avanzata"""
        super().__init__(parent)
        
        self.logger = get_logger("AdvancedProgressBar")
        
        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        
        # Label stato
        self.status_label = QLabel("Pronto")
        self.status_label.setObjectName("statusLabel")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%p%")
        layout.addWidget(self.progress_bar)
        
        self.setLayout(layout)
    
    def set_progress(self, value: int, message: str = None):
        """
        Aggiorna il progresso.
        
        Args:
            value: Valore percentuale (0-100)
            message: Messaggio di stato opzionale
        """
        self.progress_bar.setValue(value)
        
        if message:
            self.status_label.setText(message)
        
        # Emetti signal se completato
        if value >= 100:
            self.completed.emit()
            self.logger.debug("Progress completato al 100%")
    
    def set_status(self, message: str):
        """
        Aggiorna solo il messaggio di stato.
        
        Args:
            message: Messaggio da visualizzare
        """
        self.status_label.setText(message)
    
    def reset(self):
        """Reset della progress bar"""
        self.progress_bar.setValue(0)
        self.status_label.setText("Pronto")
        self.logger.debug("Progress bar resettata")
    
    def set_indeterminate(self, active: bool = True):
        """
        Attiva/disattiva modalità indeterminata.
        
        Args:
            active: True per attivare modalità indeterminata
        """
        if active:
            self.progress_bar.setMinimum(0)
            self.progress_bar.setMaximum(0)
        else:
            self.progress_bar.setMinimum(0)
            self.progress_bar.setMaximum(100)
    
    def set_error_state(self, message: str = "Errore"):
        """
        Imposta stato di errore.
        
        Args:
            message: Messaggio di errore
        """
        self.status_label.setText(f"❌ {message}")
        self.status_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
    
    def set_success_state(self, message: str = "Completato"):
        """
        Imposta stato di successo.
        
        Args:
            message: Messaggio di successo
        """
        self.status_label.setText(f"✓ {message}")
        self.status_label.setStyleSheet("color: #2ecc71; font-weight: bold;")
    
    def clear_state_style(self):
        """Rimuove gli stili di stato"""
        self.status_label.setStyleSheet("")
    
    def get_value(self) -> int:
        """Ritorna il valore corrente della progress bar"""
        return self.progress_bar.value()
    
    def is_complete(self) -> bool:
        """Verifica se il progresso è completato"""
        return self.progress_bar.value() >= 100
