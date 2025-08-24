import os, json
import sys

CONFIG_DIR = os.path.join(os.getenv("APPDATA") or os.path.expanduser("~"), "Avocado Game Launcher")
CONFIG_FILE = os.path.join(CONFIG_DIR, "settings.json")
GAMES_FILE = os.path.join(CONFIG_DIR, "games.json")

os.makedirs(CONFIG_DIR, exist_ok=True)


# Load and save settings
def load_settings():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_settings(settings):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4)

# ----------

# Resource path for PyInstaller compatibility
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# Load and save games
def load_games():
    if os.path.exists(GAMES_FILE):
        with open(GAMES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_games(games):
    with open(GAMES_FILE, "w", encoding="utf-8") as f:
        json.dump(games, f, indent=4)