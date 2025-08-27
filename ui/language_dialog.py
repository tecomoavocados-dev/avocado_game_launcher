from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from core.manager import load_settings, save_settings
from core.i18n import TRANSLATIONS # Import TRANSLATIONS to validate language codes
from PyQt6.QtGui import QIcon
from core.manager import resource_path

class LanguageDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select Language / Seleccionar idioma")
        self.setFixedSize(320, 160)
        self.setWindowIcon(QIcon(resource_path("assets/icon.ico")))


        layout = QVBoxLayout(self)

        label = QLabel("Choose your language / Elige tu idioma:")
        layout.addWidget(label)

        btn_es = QPushButton("Español")
        btn_en = QPushButton("English")

        btn_es.clicked.connect(lambda: self.choose("es"))
        btn_en.clicked.connect(lambda: self.choose("en"))

        layout.addWidget(btn_es)
        layout.addWidget(btn_en)

    def choose(self, lang: str):
        settings = load_settings()
        settings["language"] = lang
        save_settings(settings)
        self.accept()