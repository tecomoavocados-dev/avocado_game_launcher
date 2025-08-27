# 🥑 Avocado Game Launcher

Avocado Game Launcher is a cross-platform game launcher built with **Python** and **PyQt6**, designed to manage and launch your Steam games with ease.  
It stores metadata, covers, and user preferences locally, providing a smooth and customizable experience.

---

## ✨ Features

- 🎮 Import installed games from **Steam**
- 📂 Local **SQLite database** for persistence
- 🖼️ Automatic game covers from **RAWG API**
- 🌍 Multi-language support (currently: `en`, `es`)
- ⚙️ Settings window with system tray toggle and language switch
- 📌 Lightweight and portable

---

## 📦 Requirements

- Python **3.10+**
- Steam account (for game import)
- RAWG API key (for covers)

---

## ⚙️ Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/tuusuario/avocado-game-launcher.git
   cd avocado-game-launcher
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux / Mac
   venv\Scripts\activate      # Windows
   pip install -r requirements.txt
   ```
3. Configure your RAWG API key:
   ```bash
   RAWG_API_KEY=your_api_key_here
   ```
4. Run the launcher
   ```bash
   python main.py
   ```
---

## 📂 Project Structure

   ```
avocado-game-launcher/
│
├── assets/                 # Static assets (icons, etc.)
├── core/                   # Core logic
│   ├── db.py               # SQLite database manager
│   ├── covers.py           # RAWG API and covers handler
│   ├── steam.py            # Steam, info games
│   ├── steam_manifest.py   # Steam, games install
│   ├── i18n.py             # Translation system
│   ├── manager.py          # Import and settings manager
│
├── ui/                     # User interface
│   ├── main_window.py      # Main window
│   ├── settings_window.py  # Settings dialog
│   ├── about_dialog.py     # About, check updates
│
├── requirements.txt        # Python dependencies
├── main.py                 # App entrypoint
├── README.md               # Documentation
```
---

## 🗂️ AppData Storage

All persistent data is stored in the user’s Roaming folder:

   ```
%APPDATA%/Avocado Launcher/
│
├── settings.json       # User settings
├── data/
│   ├── games.db        # SQLite database
│   └── covers/         # Downloaded cover images (WEBP)
```

--- 

## 🌍 Translations

- English (en)
- Spanish (es)

## 🚧 Roadmap
```
[] Add support for non-Steam games
[] Add more languages
[] Improve cover search (fallbacks)
[] Automatic updates
```

--- 

## 📝 License

MIT License.
Feel free to use and modify this project!