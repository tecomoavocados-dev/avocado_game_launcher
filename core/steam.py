import os
import requests
from dotenv import load_dotenv
import vdf

# Load API KEY from .env
load_dotenv()
STEAM_API_KEY = os.getenv("STEAM_API_KEY")

BASE_URL = "http://api.steampowered.com"


def resolve_username(username: str) -> str | None:
    """
    Convert a Steam vanity URL username into steamid64 using ResolveVanityURL.
    Returns None if not found.
    """
    url = f"{BASE_URL}/ISteamUser/ResolveVanityURL/v0001/"
    params = {
        "key": STEAM_API_KEY,
        "vanityurl": username
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()
    if data.get("response", {}).get("success") == 1:
        return data["response"]["steamid"]
    return None


def get_owned_games(steamid: str) -> list[dict]:
    """
    Fetch all owned games for a given SteamID64.
    Returns a list of dicts with appid, name, playtime, and cover URL.
    """
    url = f"{BASE_URL}/IPlayerService/GetOwnedGames/v0001/"
    params = {
        "key": STEAM_API_KEY,
        "steamid": steamid,
        "format": "json",
        "include_appinfo": 1,
        "include_played_free_games": 1,
    }

    resp = requests.get(url, params=params)
    resp.raise_for_status()
    raw_games = resp.json().get("response", {}).get("games", [])

    games = []
    for g in raw_games:
        games.append({
            "appid": g["appid"],
            "name": g["name"],
            "playtime": g.get("playtime_forever", 0),
            # Official Steam cover (always header.jpg)
            "cover": f"https://cdn.cloudflare.steamstatic.com/steam/apps/{g['appid']}/header.jpg"
        })

    print(f"[DEBUG] Found {len(games)} games in Steam library")
    
    return games


def get_game_info(app_id):
    """Get game information from Steam API using the app ID."""
    if not STEAM_API_KEY:
        return None
        
    url = f"http://store.steampowered.com/api/appdetails?appids={app_id}"
    try:
        resp = requests.get(url, timeout=5).json()
        if resp and str(app_id) in resp and resp[str(app_id)]['success']:
            return resp[str(app_id)]['data']
    except requests.RequestException as e:
        print(f"Error en la petición a la API de Steam: {e}")
        return None
    return None


def get_installed_games(steam_path):
    """Get games install"""
    installed = []
    library_folders = vdf.load(open(os.path.join(steam_path, "steamapps", "libraryfolders.vdf")))["libraryfolders"]

    for lib_id, lib_data in library_folders.items():
        path = lib_data["path"]
        steamapps = os.path.join(path, "steamapps")

        for file in os.listdir(steamapps):
            if file.startswith("appmanifest") and file.endswith(".acf"):
                manifest_path = os.path.join(steamapps, file)
                manifest = vdf.load(open(manifest_path, encoding="utf-8"))
                appid = manifest["AppState"]["appid"]
                installdir = manifest["AppState"]["installdir"]
                installed.append({
                    "appid": appid,
                    "name": manifest["AppState"]["name"],
                    "path": os.path.join(path, "steamapps", "common", installdir)
                })
    return installed