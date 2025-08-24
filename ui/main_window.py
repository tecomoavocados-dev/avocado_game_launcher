import os
import subprocess
from PyQt6.QtWidgets import (
    QMainWindow, QListWidget, QListWidgetItem,
    QPushButton, QVBoxLayout, QWidget,
    QFileDialog, QHBoxLayout, QLabel, QMessageBox
)
from PyQt6.QtGui import QIcon, QPixmap, QFont
from core.manager import resource_path, load_games, save_games
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


        # Menu bar
        menubar = self.menuBar()

        # Import menu
        import_menu = menubar.addMenu(t("menu.import"))
        action_local = import_menu.addAction(t("menu.import_local"))
        action_folder = import_menu.addAction(t("menu.import_folder"))
        action_local.triggered.connect(self.add_game)
        action_folder.triggered.connect(lambda: QMessageBox.information(
            self, t("menu.folder"), t("feature_not_implemented")
        ))

        # Help menu
        help_menu = menubar.addMenu(t("menu.help"))
        action_about = help_menu.addAction(t("menu.about"))
        action_about.triggered.connect(lambda: QMessageBox.information(
            self, t("title.about"), "Avocado Game Launcher\nVersion 1.0\n\nDeveloped by tecomoavocados__"
        ))
        help_menu.addAction(action_about)

        # Central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Load games
        self.load_games_in_ui()

    # --------------------------
    # Add Local Game
    # --------------------------
    def add_game(self):
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

    # --------------------------
    # Load Games into UI
    # --------------------------
    def load_games_in_ui(self):
        self.games_list.clear()
        self.games = load_games()

        # Remove duplicates by name
        seen_names = set()
        unique_games = []
        for g in self.games:
            name = g.get("name")
            if name and name not in seen_names:
                seen_names.add(name)
                unique_games.append(g)

        installed_games = [g for g in unique_games if g.get("installed")]
        self.add_games_to_list(installed_games)

    # --------------------------
    # Add Games to List
    # --------------------------
    def add_games_to_list(self, games):
        self.games_list.clear()

        for g in games:
            name = g.get("name", "Unknown")
            path = g.get("path")
            icon_url = g.get("icon")

            item_widget = QWidget()
            layout = QHBoxLayout()
            layout.setContentsMargins(5, 5, 5, 5)

            # Game icon
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

            # Game name
            label_name = QLabel(name)
            font = QFont("Arial", 14)
            label_name.setFont(font)
            layout.addWidget(label_name)

            # Launch button
            btn_launch = QPushButton(t("button.launch_game"))
            btn_launch.clicked.connect(lambda checked, p=path: self.launch_game(p))
            layout.addWidget(btn_launch)

            # Delete button
            btn_delete = QPushButton(t("button.delete"))
            btn_delete.clicked.connect(lambda checked, n=name: self.delete_game(n))
            layout.addWidget(btn_delete)

            layout.addStretch()
            item_widget.setLayout(layout)

            item = QListWidgetItem()
            item.setSizeHint(item_widget.sizeHint())
            self.games_list.addItem(item)
            self.games_list.setItemWidget(item, item_widget)

    # --------------------------
    # Delete Game
    # --------------------------
    def delete_game(self, game_name):
        current_games = load_games()
        updated_games = [g for g in current_games if g.get("name") != game_name]
        save_games(updated_games)
        self.load_games_in_ui()

    # --------------------------
    # Launch Game
    # --------------------------
    def launch_game(self, path):
        if path and os.path.exists(path):
            try:
                subprocess.Popen(path, shell=True)
            except Exception as e:
                print(f"Failed to launch {path}: {e}")
