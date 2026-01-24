"""
User Settings Manager
Saves and loads user preferences (language, etc.)
"""
import json
from pathlib import Path
from typing import Optional


class UserSettings:
    """Manages user preferences and settings"""
    
    def __init__(self):
        self.settings_file = Path.home() / ".docconverter" / "user_settings.json"
        self.settings_file.parent.mkdir(parents=True, exist_ok=True)
        self._settings = self._load()
    
    def _load(self) -> dict:
        """Load settings from file"""
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        
        # Default settings
        return {
            'language': 'en',
            'last_output_dir': None,
        }
    
    def _save(self):
        """Save settings to file"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self._settings, f, indent=2)
        except Exception:
            pass
    
    def get_language(self) -> str:
        """Get saved language"""
        return self._settings.get('language', 'en')
    
    def set_language(self, lang: str):
        """Save language preference"""
        self._settings['language'] = lang
        self._save()
    
    def get_last_output_dir(self) -> Optional[str]:
        """Get last used output directory"""
        return self._settings.get('last_output_dir')
    
    def set_last_output_dir(self, path: str):
        """Save last output directory"""
        self._settings['last_output_dir'] = path
        self._save()


# Global instance
_user_settings = None


def get_user_settings() -> UserSettings:
    """Get singleton instance of UserSettings"""
    global _user_settings
    if _user_settings is None:
        _user_settings = UserSettings()
    return _user_settings
