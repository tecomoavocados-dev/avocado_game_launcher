import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from core.i18n import set_language
from core.manager import load_settings, save_settings

def main():
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

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
