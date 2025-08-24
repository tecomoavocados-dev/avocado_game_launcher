from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QFormLayout
)
from core.manager import load_settings, resource_path, save_settings
from core.i18n import t
from PyQt6.QtGui import QIcon


class SettingsWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Avocado Launcher - Ajustes")
        self.setFixedSize(400, 200)
        icon_path = resource_path("assets/icon.ico")
        self.setWindowIcon(QIcon(icon_path))

        main_layout = QVBoxLayout(self)

        # Config load
        self.settings = load_settings()

        # Form layout
        form_layout = QFormLayout()

        # Steam ID
        self.steam_input = QLineEdit()
        self.steam_input.setText(self.settings.get("steam_id", ""))
        self.steam_input.setReadOnly(True)
        form_layout.addRow(QLabel("Steam ID:"), self.steam_input)

        # Language
        self.lang_input = QLineEdit()
        self.lang_input.setText(self.settings.get("language", "es"))
        form_layout.addRow(QLabel(t("lang.title") + ":"), self.lang_input)

        main_layout.addLayout(form_layout)

        # Buttons
        save_btn = QPushButton(t("title.save"))
        save_btn.clicked.connect(self.save_settings)
        main_layout.addWidget(save_btn)

        close_btn = QPushButton(t("title.exit"))
        close_btn.clicked.connect(self.close)
        main_layout.addWidget(close_btn)

    def save_settings(self):
        steam_id = self.steam_input.text().strip()
        language = self.lang_input.text().strip()

        if language not in ("es", "en"):
            QMessageBox.warning(self, "Error", t("err.invalid_language"))
            return

        self.settings["steam_id"] = steam_id
        self.settings["language"] = language
        save_settings(self.settings)
        QMessageBox.information(self, t("title.settings"), t("settings.saved"))
        self.accept()
