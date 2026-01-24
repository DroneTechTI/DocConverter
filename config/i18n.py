"""
Internationalization (i18n) module
Multi-language support: Italian and English
"""
import json
from pathlib import Path
from typing import Dict

# Default language
_current_language = "en"

# Translations
TRANSLATIONS = {
    "en": {
        # Application
        "app_title": "DocConverter",
        "app_description": "Professional Document Converter",
        
        # Menu
        "menu_file": "&File",
        "menu_tools": "&Tools",
        "menu_help": "&Help",
        "menu_add_files": "Add Files",
        "menu_clear_list": "Clear List",
        "menu_convert": "Convert",
        "menu_exit": "Exit",
        "menu_merge_pdf": "Merge PDF",
        "menu_compress_pdf": "Compress PDF",
        "menu_about": "About",
        "menu_check_deps": "Check Dependencies",
        
        # UI Elements
        "quick_conversion": "Quick Conversion",
        "select_conversion": "Select conversion type...",
        "conversion_word_pdf": "📝 Word → PDF",
        "conversion_pdf_word": "📄 PDF → Word",
        "conversion_excel_pdf": "📊 Excel → PDF",
        "conversion_ppt_pdf": "🎨 PowerPoint → PDF",
        "conversion_img_pdf": "🖼️ Images → PDF",
        "conversion_merge_pdf": "📑 Merge PDF",
        "conversion_compress_pdf": "🗜️ Compress PDF",
        
        # Buttons
        "btn_add_files": "📁 Add Files",
        "btn_clear": "🧹 Clear All",
        "btn_select_output": "📂 Output Folder",
        "btn_convert_all": "🚀 Convert All",
        
        # Messages
        "files_added": "Added {count} file(s)",
        "conversion_started": "Starting conversion of {count} file(s)...",
        "conversion_completed": "Conversion completed: {success} successes, {failures} errors",
        "select_output_folder": "Select Output Folder",
        "output_folder": "Output folder",
        "no_files": "No files to convert",
        "add_files_first": "Please add files first",
        
        # Tooltips
        "tooltip_add_files": "Add files to convert (Ctrl+O)",
        "tooltip_convert": "Start conversion (Ctrl+Enter)",
        
        # About
        "about_title": "About DocConverter",
        "about_text": """DocConverter v{version}

Professional document converter

Features:
• 8 converters available
• PDF Merge & Compress
• Auto-install dependencies
• Perfect formatting

Developer: {author}
License: MIT""",
        
        # Errors
        "error_title": "Error",
        "warning_title": "Warning",
        "info_title": "Information",
        "success_title": "Success",
        
        # UI Groups
        "files_to_convert": "Files to Convert",
        "operations_log": "Operations Log",
    },
    
    "it": {
        # Applicazione
        "app_title": "DocConverter",
        "app_description": "Convertitore Documenti Professionale",
        
        # Menu
        "menu_file": "&File",
        "menu_tools": "&Strumenti",
        "menu_help": "&Aiuto",
        "menu_add_files": "Aggiungi File",
        "menu_clear_list": "Pulisci Lista",
        "menu_convert": "Converti",
        "menu_exit": "Esci",
        "menu_merge_pdf": "Unisci PDF",
        "menu_compress_pdf": "Comprimi PDF",
        "menu_about": "Informazioni",
        "menu_check_deps": "Verifica Dipendenze",
        
        # Elementi UI
        "quick_conversion": "Conversione Rapida",
        "select_conversion": "Seleziona tipo conversione...",
        "conversion_word_pdf": "📝 Word → PDF",
        "conversion_pdf_word": "📄 PDF → Word",
        "conversion_excel_pdf": "📊 Excel → PDF",
        "conversion_ppt_pdf": "🎨 PowerPoint → PDF",
        "conversion_img_pdf": "🖼️ Immagini → PDF",
        "conversion_merge_pdf": "📑 Unisci PDF",
        "conversion_compress_pdf": "🗜️ Comprimi PDF",
        
        # Pulsanti
        "btn_add_files": "📁 Aggiungi File",
        "btn_clear": "🧹 Pulisci",
        "btn_select_output": "📂 Seleziona Cartella Output",
        "btn_convert_all": "🚀 Converti Tutto",
        
        # Messaggi
        "files_added": "Aggiunti {count} file",
        "conversion_started": "Avvio conversione di {count} file...",
        "conversion_completed": "Conversione completata: {success} successi, {failures} errori",
        "select_output_folder": "Seleziona Cartella Output",
        "output_folder": "Cartella output",
        "no_files": "Nessun file da convertire",
        "add_files_first": "Aggiungi prima dei file",
        
        # Tooltip
        "tooltip_add_files": "Aggiungi file da convertire (Ctrl+O)",
        "tooltip_convert": "Avvia conversione (Ctrl+Enter)",
        
        # Informazioni
        "about_title": "Informazioni su DocConverter",
        "about_text": """DocConverter v{version}

Convertitore documenti professionale

Funzionalità:
• 8 convertitori disponibili
• Unisci e Comprimi PDF
• Auto-installazione dipendenze
• Formattazione perfetta

Sviluppatore: {author}
Licenza: MIT""",
        
        # Errori
        "error_title": "Errore",
        "warning_title": "Attenzione",
        "info_title": "Informazione",
        "success_title": "Successo",
    }
}


def set_language(lang: str):
    """Set application language (en or it)"""
    global _current_language
    if lang in TRANSLATIONS:
        _current_language = lang


def get_language() -> str:
    """Get current language"""
    return _current_language


def tr(key: str, **kwargs) -> str:
    """
    Translate key to current language
    
    Args:
        key: Translation key
        **kwargs: Format parameters
        
    Returns:
        Translated string
    """
    translations = TRANSLATIONS.get(_current_language, TRANSLATIONS["en"])
    text = translations.get(key, key)
    
    if kwargs:
        try:
            return text.format(**kwargs)
        except KeyError:
            return text
    
    return text


def get_available_languages() -> Dict[str, str]:
    """Get available languages"""
    return {
        "en": "English",
        "it": "Italiano"
    }
