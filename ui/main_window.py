import os
from PyQt6.QtWidgets import (
    QMainWindow, QListWidget, QListWidgetItem,
    QPushButton, QVBoxLayout, QWidget,
    QInputDialog, QMessageBox, QFileDialog, QApplication, QHBoxLayout, QLabel
)
from PyQt6.QtGui import QIcon, QPixmap, QFont
from core.manager import load_settings, save_settings, resource_path, load_games, save_games
from core.i18n import t
from core.rawg import fetch_rawg_image
import requests


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle(t("app.title"))
        self.setGeometry(200, 200, 1080, 700)

        # Main icon
        self.setWindowIcon(QIcon(resource_path("assets/icon.ico")))

        # Main layout
        self.games_list = QListWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.games_list)

        # Buttons
        btn_add = QPushButton(t("button.add_game"))
        btn_add.clicked.connect(self.add_game)
        layout.addWidget(btn_add)

        btn_launch = QPushButton(t("button.launch_game"))
        layout.addWidget(btn_launch)

        # Central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Load games
        self.load_games_in_ui()


        # Add Local Game
    def add_game(self):
        """Add a local game by selecting an exe file and fetch RAWG cover."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, t("button.add_game"), "", "Executables (*.exe)"
        )
        if file_path:
            name = os.path.splitext(os.path.basename(file_path))[0]
            icon_url = fetch_rawg_image(name)

            game_data = {
                "name": name,
                "path": file_path,
                "installed": True,
                "icon": icon_url
            }

            current_games = load_games()
            current_games.append(game_data)

            # Remove duplicates by path
            seen_paths = set()
            unique_games = [
                g for g in current_games if not (g.get("path") in seen_paths or seen_paths.add(g.get("path")))
            ]

            save_games(unique_games)
            self.load_games_in_ui()


    def load_games_in_ui(self):
        """Load all games into the list widget, avoiding duplicates."""
        self.games_list.clear()
        self.games = load_games()

        # Remove duplicates safely
        seen_names = set()
        unique_games = []
        for g in self.games:
            name = g.get("name")
            if name and name not in seen_names:
                seen_names.add(name)
                unique_games.append(g)

        # Only installed games
        installed_games = [g for g in unique_games if g.get("installed")]
        self.add_games_to_list(installed_games)



    def add_games_to_list(self, games):
        """Add games to the list with custom widget (icon + name + delete button)."""
        self.games_list.clear()

        for g in games:
            name = g.get("name", "Unknown")
            icon_url = g.get("icon")

            item_widget = QWidget()
            layout = QHBoxLayout()
            layout.setContentsMargins(5, 5, 5, 5)

            label_icon = QLabel()
            if icon_url:
                try:
                    response = requests.get(icon_url, timeout=5)
                    response.raise_for_status()
                    pixmap = QPixmap()
                    if pixmap.loadFromData(response.content):
                        pixmap = pixmap.scaled(64, 64)
                        label_icon.setPixmap(pixmap)
                except Exception as e:
                    print(f"Failed to load icon for {name}: {e}")
            layout.addWidget(label_icon)

            label_name = QLabel(name)
            font = QFont("Arial", 14)  
            label_name.setFont(font)
            layout.addWidget(label_name)

            btn_delete = QPushButton()
            btn_delete.setIcon(QIcon(resource_path("assets/icons/trash_red.png")))
            btn_delete.setFixedSize(32, 32)
            btn_delete.clicked.connect(lambda checked, n=name: self.delete_game(n))
            layout.addWidget(btn_delete)

            layout.addStretch()
            item_widget.setLayout(layout)

            item = QListWidgetItem()
            item.setSizeHint(item_widget.sizeHint())
            self.games_list.addItem(item)
            self.games_list.setItemWidget(item, item_widget)

    def delete_game(self, game_name):
        current_games = load_games()
        updated_games = [g for g in current_games if g.get("name") != game_name]
        save_games(updated_games)
        self.load_games_in_ui()
