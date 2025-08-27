from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QFormLayout, QCheckBox
)
from core.manager import load_settings, resource_path, save_settings
from core.i18n import t
from PyQt6.QtGui import QIcon


class SettingsWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(t("app.title.settings"))
        self.setFixedSize(400, 220)
        self.setWindowIcon(QIcon(resource_path("assets/icon.ico")))

        main_layout = QVBoxLayout(self)

        # Load config
        self.settings = load_settings()

        # Form layout
        form_layout = QFormLayout()

        # Steam username (read only)
        self.steam_user_input = QLineEdit()
        self.steam_user_input.setText(self.settings.get("username", ""))
        self.steam_user_input.setReadOnly(True)
        form_layout.addRow(QLabel(t("steam.username.settings") + ":"), self.steam_user_input)

        # Steam ID (read only)
        self.steam_input = QLineEdit()
        self.steam_input.setText(self.settings.get("steamid", ""))
        self.steam_input.setReadOnly(True)
        form_layout.addRow(QLabel(t("steam.id") + ":"), self.steam_input)

        # Language
        self.lang_input = QLineEdit()
        self.lang_input.setText(self.settings.get("language", "es"))
        form_layout.addRow(QLabel(t("lang.title") + ":"), self.lang_input)

        # System Tray toggle
        self.tray_icon_checkbox = QCheckBox(t("settings.tray_icon"))
        self.tray_icon_checkbox.setChecked(self.settings.get("tray_icon", True))
        form_layout.addRow(self.tray_icon_checkbox)

        main_layout.addLayout(form_layout)

        # Save button
        save_btn = QPushButton(t("title.save"))
        save_btn.clicked.connect(self.save_settings)
        main_layout.addWidget(save_btn)

        # Close button
        close_btn = QPushButton(t("title.exit"))
        close_btn.clicked.connect(self.close)
        main_layout.addWidget(close_btn)

    def save_settings(self):
        """Save user settings to disk."""
        steam_id = self.steam_input.text().strip()
        language = self.lang_input.text().strip()

        if language not in ("es", "en"):
            QMessageBox.warning(self, "Error", t("err.invalid_language"))
            return

        # Save updated values
        self.settings["steamid"] = steam_id
        self.settings["language"] = language
        self.settings["tray_icon"] = self.tray_icon_checkbox.isChecked()

        save_settings(self.settings)
        QMessageBox.information(self, t("title.settings"), t("settings.saved"))
        self.accept()
