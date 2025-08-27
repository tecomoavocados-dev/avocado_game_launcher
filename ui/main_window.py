from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QListWidget, QLabel, QVBoxLayout, QFrame, QInputDialog, QMessageBox, QListWidgetItem, QPushButton, QSystemTrayIcon, QApplication, QMenu
from PyQt6.QtGui import QAction, QIcon, QPixmap
from PyQt6.QtCore import Qt
from core.i18n import t
from core.manager import resource_path, import_games_from_steam, load_settings, quick_refresh, save_settings
import os, requests
from core.db import load_games, init_db
from ui.about_dialog import AboutDialog
from ui.settings_window import SettingsWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        init_db()
        
        # Window 
        self.setWindowTitle(t("app.title"))
        self.setGeometry(200, 200, 1400, 700)
        self.setFixedSize(1500, 800)


        # Setup system tray
        self.tray_icon = QSystemTrayIcon(QIcon(resource_path("assets/icon.ico")), self)
        self.setup_tray()

        # Main icon
        self.setWindowIcon(QIcon(resource_path("assets/icon.ico")))

        # Menu bar
        menubar = self.menuBar()

        # Import menu
        import_menu = menubar.addMenu(t("menu.import"))
        action_local = QAction(t("menu.import_local"), self)
        action_local.triggered.connect(lambda: print("Hola"))
        import_menu.addAction(action_local)

        action_steam = QAction("Steam", self)  
        action_steam.setIcon(QIcon(resource_path("assets/icons/steam.ico")))

        # connect to steam
        action_steam.triggered.connect(self.handle_import_steam)

        import_menu.addAction(action_steam)


        # Settings menu
        settings_menu = menubar.addMenu(t("menu.settings"))
        settings_action = QAction(t("menu.settings"), self)
        settings_action.triggered.connect(self.open_settings_window)
        settings_menu.addAction(settings_action)

        # Help menu
        help_menu = menubar.addMenu(t("menu.help"))
        action_about = QAction(t("menu.about"), self)
        action_about.triggered.connect(lambda: AboutDialog().exec())
        help_menu.addAction(action_about)
        report_issue_action = QAction(t("menu.report_issue"), self)
        report_issue_action.triggered.connect(
            lambda: os.startfile("https://github.com/tecomoavocados-dev/issues/issues/new")
        )
        
        help_menu.addAction(report_issue_action)


        # Icons and Buttons
        action_local.setIcon(QIcon(resource_path("assets/icons/file.png")))
        settings_action.setIcon(QIcon(resource_path("assets/icons/settings.png")))
        action_about.setIcon(QIcon(resource_path("assets/icons/about.png")))
        report_issue_action.setIcon(QIcon(resource_path("assets/icons/report_problem.png")))


        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)

        # ---- Left column ----
        left_layout = QVBoxLayout()

        # Row: "Your Games" + Update button
        title_row = QHBoxLayout()

        title_games = QLabel(t("your.games"))
        title_games.setObjectName("TitleYourGames")

        self.refresh_btn = QPushButton("Update Library")
        self.refresh_btn.setObjectName("RefreshButton")
        self.refresh_btn.clicked.connect(self.refresh_library)

        title_row.addWidget(title_games)
        title_row.addStretch()
        title_row.addWidget(self.refresh_btn)

        left_layout.addLayout(title_row)

        # Frame with game list
        self.games_panel = QFrame()
        self.games_panel.setObjectName("GamesPanel")
        self.games_panel_layout = QVBoxLayout(self.games_panel)

        self.games_list = QListWidget()
        self.games_list.setObjectName("GamesList")
        self.games_panel_layout.addWidget(self.games_list)

        left_layout.addWidget(self.games_panel)

        main_layout.addLayout(left_layout)



        # ---- Right Column ----
        right_layout = QVBoxLayout()

        # Title
        title_info = QLabel(t("information.games"))
        title_info.setObjectName("Title")
        right_layout.addWidget(title_info)
        right_layout.addWidget(title_info, 0) 

        # Information panel
        self.info_panel = QFrame()
        self.info_panel.setObjectName("InfoPanel")
        info_layout = QVBoxLayout(self.info_panel)
        right_layout.addWidget(self.info_panel, 1)

        # Details
        placeholder = QLabel(t("info.game"))
        info_layout.addWidget(placeholder)

        right_layout.addWidget(self.info_panel)

        # ---- Add main layout ----
        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 3)


        games = load_games()
        self.populate_games(games)
        self.games_list.itemClicked.connect(self.show_game_info)


    def handle_import_steam(self):
        """Triggered when user clicks 'Import from Steam'."""
        username, ok = QInputDialog.getText(
            self, t("import.steam"), t("steam.username")
        )
        if not ok or not username:
            return

        # Get games from Steam API
        all_games = import_games_from_steam(username)

        # Keep only installed ones
        games = all_games

        self.populate_games(games)
        QMessageBox.information(
        self,
        "Steam",
        t("import.success").format(count=len(games))
        )


    def populate_games(self, games: list[dict]):
        """Fill the game panel with imported games."""
        self.games_list.clear()

        for game in games:
            item = QListWidgetItem(game['name'])

            cover = game.get("cover")
            if cover and os.path.exists(cover):
                pixmap = QPixmap(cover)
                icon = QIcon(pixmap.scaled(64, 64))
                item.setIcon(icon)
            else:
                print(f"[DEBUG] No local cover for {game['name']}")

            item.setData(1000, game)
            self.games_list.addItem(item)

    def refresh_library(self):
        """Update DB + UI without re-downloading existing covers."""
        try:
            settings = load_settings()
            username = settings.get("username")
            if not username:
                QMessageBox.warning(self, "Error", "Set your Steam username in settings.")
                return

            updated_games = quick_refresh(username)
            self.populate_games(updated_games)
            QMessageBox.information(self, "Library updated",
                                    f"Found {len(updated_games)} games (changes applied).")
        except Exception as e:
            QMessageBox.critical(self, "Error while updating", str(e))

    def show_game_info(self, item):
        """Show selected game details in the right panel."""
        game = item.data(1000)
        appid = game["appid"]

        from core.manager import fetch_game_info
        details = fetch_game_info(appid)

        layout = self.info_panel.layout()
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        if not details:
            layout.addWidget(QLabel("No se pudo obtener información del juego."))
            return

        # ---- Title ----
        title = QLabel(details.get("name", ""))
        title.setObjectName("GameTitle")
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignLeft)

        # ---- Header Image ----
        if details.get("header_image"):
            try:
                pixmap = QPixmap()
                pixmap.loadFromData(requests.get(details["header_image"]).content)
                img = QLabel()
                img.setPixmap(pixmap.scaledToWidth(600, Qt.TransformationMode.SmoothTransformation))
                img.setAlignment(Qt.AlignmentFlag.AlignCenter)
                layout.addWidget(img)
            except Exception as e:
                print("[DEBUG] No se pudo cargar header_image:", e)


        # ---- Description ----
        desc = QLabel(details.get("description", ""))
        desc.setWordWrap(True)
        desc.setObjectName("GameDescription")
        layout.addWidget(desc)


        desc = QLabel()
        desc.setWordWrap(True)
        desc.setObjectName("GameDescription")
        desc.setTextFormat(Qt.TextFormat.RichText)

        layout.addWidget(desc)

        # ---- Metadata ----
        meta_frame = QFrame()
        meta_frame.setObjectName("InfoCard")
        meta_layout = QVBoxLayout(meta_frame)

        # ---- Genres ----
        genres = []
        genres_data = details.get("genres")

        if isinstance(genres_data, list):
            genres = [g.get("description", "") for g in genres_data if isinstance(g, dict)]
        elif isinstance(genres_data, str):
            genres = [genres_data]

        if genres:
            lbl = QLabel(t("genres.games") +  f":{', '.join(genres)}")
            lbl.setObjectName("GameMeta")
            meta_layout.addWidget(lbl)

        # ---- Devs / Publishers ----
        devs = details.get("developers") or []
        if isinstance(devs, str):
            devs = [devs]

        pubs = details.get("publishers") or []
        if isinstance(pubs, str):
            pubs = [pubs]

        if devs:
            lbl = QLabel(t("developer") + f": {', '.join(devs)}")
            lbl.setObjectName("GameMeta")
            meta_layout.addWidget(lbl)

        if pubs:
            lbl = QLabel(t("publisher") + f": {', '.join(pubs)}")
            lbl.setObjectName("GameMeta")
            meta_layout.addWidget(lbl)

        # ---- Release Date ----
        release_text = None
        release_data = details.get("release_date")

        if isinstance(release_data, dict):
            release_text = release_data.get("date")
        elif isinstance(release_data, str):
            release_text = release_data

        if release_text:
            lbl = QLabel(t("release.date") + f": {release_text}")
            lbl.setObjectName("GameMeta")
            meta_layout.addWidget(lbl)


        layout.addWidget(meta_frame)

     # Open Settings
    def open_settings_window(self):
        settings_window = SettingsWindow()
        settings_window.exec()

    # Setup system tray
    def setup_tray(self):
        """Setup the system tray icon and menu."""
        tray_menu = QMenu()
        self.tray_icon.setToolTip("Avocado Game Launcher")

        restore_action = QAction(t("title.restore"), self)
        restore_action.triggered.connect(self.show)  # Open main window
        tray_menu.addAction(restore_action)

        quit_action = QAction(t("title.exit"), self)
        quit_action.triggered.connect(QApplication.instance().quit)  # Close app
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        self.tray_icon.show()



    def closeEvent(self, event):
        """Minimize to tray or close app depending on settings."""
        settings = load_settings()
        if settings.get("tray_icon", False):
            # Minimize to tray
            event.ignore()
            self.hide()
            self.tray_icon.showMessage(
                "Avocado Game Launcher",
                t("msg.tray_info"),
                QSystemTrayIcon.MessageIcon.Information,
                3000
            )
        else:
            # Close completely
            event.accept()

    def on_tray_icon_activated(self, reason):
        """Restore window on tray double click."""
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show()
            self.raise_()
            self.activateWindow()