# core/manager.py
import os, json, sys
from core.db import save_games
from core.steam import get_owned_games, resolve_username, get_game_info
from core.rawg import get_game_cover
from core.steam_manifest import get_installed_appids
from core.db import load_games, save_games

CONFIG_DIR = os.path.join(os.getenv("APPDATA") or os.path.expanduser("~"), "Avocado Game Launcher")
CONFIG_FILE = os.path.join(CONFIG_DIR, "settings.json")

# Load and save settings
def load_settings():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_settings(settings):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4)

# Resource path for PyInstaller compatibility
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

icon_path = resource_path("assets/icon.ico")
env_path = resource_path(".env")
about_image_path = resource_path("assets/icons/about.png")
import_file_path = resource_path("assets/icons/file.png")
steam_icon_path = resource_path("assets/icons/steam.ico")
report_problem_icon_path = resource_path("assets/icons/report_problem.png")
settings_icon_path = resource_path("assets/icons/settings.png")


def import_games_from_steam(username: str) -> list[dict]:
    """
    Import ONLY installed Steam games into the DB.
    """
    settings = load_settings()
    steamid = settings.get("steamid")

    if not steamid:
        steamid = resolve_username(username)
        if not steamid:
            raise ValueError("Could not resolve SteamID from username.")

        settings["steamid"] = steamid
        settings["username"] = username
        save_settings(settings)

    print(f"[STEAM] Resolving owned games for steamid: {steamid}")
    games = get_owned_games(steamid)
    print(f"[STEAM] Owned games: {len(games)}")

    installed_ids = get_installed_appids()  # <-- checks all libraries
    print(f"[STEAM] Installed appids: {len(installed_ids)}")

    formatted = []
    for g in games:
        appid = g.get("appid")
        if appid not in installed_ids:  
            continue  # <-- skip if not installed

        name = g.get("name", "Unknown")
        playtime = g.get("playtime_forever", 0)

        cover_path = get_game_cover(name, appid)  # returns local file or None

        formatted.append({
            "appid": appid,
            "name": name,
            "playtime": playtime,
            "cover": cover_path,
            "installed": True,
        })

    # Save ONLY installed games to DB
    save_games(formatted)
    print(f"[STEAM] Import complete. Saved {len(formatted)} installed games to DB.")

    return formatted



def quick_refresh(username: str) -> list[dict]:
    """Lightweight refresh: only keep installed games in DB."""
    settings = load_settings()
    steamid = resolve_username(username)
    if not steamid:
        raise ValueError("Could not resolve SteamID")

    # Fetch current Steam library (basic info only)
    new_games = get_owned_games(steamid)
    installed_ids = get_installed_appids()

    # Load old games from DB
    old_games = load_games()
    old_map = {g["appid"]: g for g in old_games}

    changed = False
    merged = []

    for g in new_games:
        appid = g["appid"]
        if appid not in installed_ids:
            continue  # <-- keep only installed

        name = g.get("name", "Unknown")
        playtime = g.get("playtime_forever", 0)

        if appid in old_map:
            # Existing game → keep old data, update playtime
            old = old_map[appid]
            if old.get("playtime") != playtime:
                changed = True
            merged.append({
                **old,
                "installed": True,
                "playtime": playtime
            })
        else:
            # New installed game → fetch cover
            cover_path = get_game_cover(name, appid)
            merged.append({
                "appid": appid,
                "name": name,
                "cover": cover_path,
                "installed": True,
                "playtime": playtime
            })
            changed = True

    # Save only if something has changed
    if changed:
        save_games(merged)

    return merged


# Get game info Steam
def fetch_game_info(appid: int) -> dict:
    """Wrapper to safely fetch detailed game info from Steam API."""
    data = get_game_info(appid)
    if not data:
        return {}
    
    return {
        "name": data.get("name"),
        "description": data.get("short_description"),
        "header_image": data.get("header_image"),
        "genres": [g["description"] for g in data.get("genres", [])],
        "developers": data.get("developers", []),
        "publishers": data.get("publishers", []),
        "release_date": data.get("release_date", {}).get("date"),
    }