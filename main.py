import sys
import os
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from core.db import init_db
from core.i18n import set_language
from core.manager import load_settings, save_settings
from ui.language_dialog import LanguageDialog

def load_stylesheet(app, path):
    base_path = os.path.dirname(__file__)
    full_path = os.path.join(base_path, path)
    with open(full_path, "r") as f:
        app.setStyleSheet(f.read())

if __name__ == "__main__":
    app = QApplication(sys.argv)

    settings = load_settings()
    lang = settings.get("language")

    # If no language set, show dialog
    if not lang:
        from ui.language_dialog import LanguageDialog
        dialog = LanguageDialog()
        if dialog.exec():  # User selected a language
            lang = load_settings().get("language")  # Save 
        else:
            lang = "es"  # Default spanish if dialog cancelled
            settings["language"] = lang
            save_settings(settings)

    # Apply the selected language
    set_language(lang)

    # Load stylesheet
    load_stylesheet(app, "assets/styles.qss")

    window = MainWindow()
    window.show()
    init_db()

    sys.exit(app.exec())
