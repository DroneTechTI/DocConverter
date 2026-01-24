"""
Widget lista file con supporto drag & drop
"""
from PyQt6.QtWidgets import QListWidget, QListWidgetItem, QAbstractItemView
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QDragEnterEvent, QDropEvent
from pathlib import Path
from typing import List

from utils.logger import get_logger


class FileListWidget(QListWidget):
    """
    Lista di file con supporto drag & drop.
    
    Signals:
        filesDropped: Emesso quando file vengono droppati (list[str])
        filesRemoved: Emesso quando file vengono rimossi (list[str])
    """
    
    filesDropped = pyqtSignal(list)
    filesRemoved = pyqtSignal(list)
    
    def __init__(self, parent=None):
        """Inizializza la lista file"""
        super().__init__(parent)
        
        self.logger = get_logger("FileListWidget")
        
        # Configura drag & drop
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.DragDropMode.DropOnly)
        
        # Configura selezione multipla
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        
        # Tooltip
        self.setToolTip("Trascina file qui o usa 'Aggiungi File'")
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Gestisce l'ingresso del drag"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()
    
    def dragMoveEvent(self, event):
        """Gestisce il movimento del drag"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()
    
    def dropEvent(self, event: QDropEvent):
        """Gestisce il drop dei file"""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            files = []
            
            for url in urls:
                file_path = url.toLocalFile()
                
                # Verifica che sia un file (non directory)
                if Path(file_path).is_file():
                    files.append(file_path)
                    self.logger.info(f"File droppato: {file_path}")
            
            if files:
                self.filesDropped.emit(files)
                event.acceptProposedAction()
            else:
                self.logger.warning("Nessun file valido droppato")
                event.ignore()
        else:
            event.ignore()
    
    def add_files(self, file_paths: List[str]):
        """
        Aggiunge file alla lista.
        
        Args:
            file_paths: Lista di path da aggiungere
        """
        for file_path in file_paths:
            # Evita duplicati
            if self.find_item_by_path(file_path):
                self.logger.debug(f"File già presente: {file_path}")
                continue
            
            # Crea item
            item = QListWidgetItem()
            
            # Mostra solo il nome del file
            file_name = Path(file_path).name
            item.setText(file_name)
            
            # Salva path completo nei dati
            item.setData(Qt.ItemDataRole.UserRole, file_path)
            
            # Tooltip con path completo
            item.setToolTip(file_path)
            
            self.addItem(item)
            self.logger.info(f"File aggiunto: {file_path}")
    
    def remove_selected_files(self) -> List[str]:
        """
        Rimuove i file selezionati.
        
        Returns:
            Lista di path rimossi
        """
        removed = []
        
        for item in self.selectedItems():
            file_path = item.data(Qt.ItemDataRole.UserRole)
            removed.append(file_path)
            self.takeItem(self.row(item))
            self.logger.info(f"File rimosso: {file_path}")
        
        if removed:
            self.filesRemoved.emit(removed)
        
        return removed
    
    def clear_all_files(self) -> List[str]:
        """
        Rimuove tutti i file.
        
        Returns:
            Lista di path rimossi
        """
        removed = self.get_all_file_paths()
        self.clear()
        
        if removed:
            self.filesRemoved.emit(removed)
            self.logger.info(f"Rimossi {len(removed)} file")
        
        return removed
    
    def get_all_file_paths(self) -> List[str]:
        """
        Ottiene tutti i path dei file nella lista.
        
        Returns:
            Lista di path
        """
        paths = []
        for i in range(self.count()):
            item = self.item(i)
            file_path = item.data(Qt.ItemDataRole.UserRole)
            paths.append(file_path)
        
        return paths
    
    def find_item_by_path(self, file_path: str) -> QListWidgetItem:
        """
        Trova un item per path.
        
        Args:
            file_path: Path da cercare
        
        Returns:
            Item trovato o None
        """
        for i in range(self.count()):
            item = self.item(i)
            if item.data(Qt.ItemDataRole.UserRole) == file_path:
                return item
        return None
    
    def update_item_status(self, file_path: str, status: str, color: str = None):
        """
        Aggiorna lo stato di un item.
        
        Args:
            file_path: Path del file
            status: Testo dello stato (es. "✓ Completato", "✗ Errore")
            color: Colore del testo (opzionale)
        """
        item = self.find_item_by_path(file_path)
        
        if item:
            file_name = Path(file_path).name
            item.setText(f"{file_name} - {status}")
            
            if color:
                from PyQt6.QtGui import QColor
                item.setForeground(QColor(color))
    
    def reset_all_statuses(self):
        """Reset tutti gli status degli item"""
        for i in range(self.count()):
            item = self.item(i)
            file_path = item.data(Qt.ItemDataRole.UserRole)
            file_name = Path(file_path).name
            item.setText(file_name)
            
            # Reset colore
            from PyQt6.QtGui import QColor
            item.setForeground(QColor("#e0e0e0"))
    
    def get_file_count(self) -> int:
        """Ritorna il numero di file nella lista"""
        return self.count()
    
    def is_empty(self) -> bool:
        """Verifica se la lista è vuota"""
        return self.count() == 0
