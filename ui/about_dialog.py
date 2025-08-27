import requests
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QMessageBox
)
from PyQt6.QtGui import QIcon
from core.i18n import t
from core.manager import resource_path

APP_VERSION = "1.0.1"
AUTHOR = "tecomoavocados__"


class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(t("menu.about"))
        self.setFixedSize(400, 200)
        self.setWindowIcon(QIcon(resource_path("assets/icon.ico")))
        layout = QVBoxLayout(self)
        
        version_layout = QHBoxLayout()
        self.version_label = QLabel(f"{t('current_version')}: {APP_VERSION}")
        self.update_btn = QPushButton(t("check_for_updates"))
        self.update_btn.clicked.connect(self.check_update)

        version_layout.addWidget(self.version_label)
        version_layout.addWidget(self.update_btn)

        layout.addLayout(version_layout)

        # Autor
        self.author_label = QLabel(f"{t('author')}: {AUTHOR}")
        layout.addWidget(self.author_label)

        # Contact
        self.contact_label = QLabel(f"{t('contact')}: tecomoavocados.dev@gmail.com")
        layout.addWidget(self.contact_label)

    def check_update(self):
        try:
            url = "https://api.github.com/repos/tecomoavocados-dev/avocado-game-launcher/releases/latest"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            latest = response.json().get("tag_name", "").replace("v", "")

            if latest and latest != APP_VERSION:
                self.update_btn.setText(t("update_available"))
                QMessageBox.information(
                    self,
                    t("update_available"),
                    t("new_version_available").format(latest=latest)
                    + "\n" + t("visit_github_to_download"),
                )
            else:
                QMessageBox.information(
                    self, t("no_updates"), t("you_have_latest_version")
                )
        except requests.exceptions.RequestException:
            QMessageBox.warning(self, t("network_error"), t("check_internet_connection"))
        except Exception as e:
            QMessageBox.warning(self, t("error"), str(e))

