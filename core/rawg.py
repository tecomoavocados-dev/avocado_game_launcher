import os
import requests
from PIL import Image
import io
from pathlib import Path
from dotenv import load_dotenv

# Load API key
load_dotenv()
RAWG_API_KEY = os.getenv("RAWG_API_KEY")

# Base folder in Roaming
APPDATA_DIR = Path(os.getenv("APPDATA")) / "Avocado Game Launcher" / "data"
COVERS_DIR = APPDATA_DIR / "covers"
COVERS_DIR.mkdir(parents=True, exist_ok=True)


def get_game_cover(game_name: str, appid: int) -> str | None:
    """
    Search RAWG API for a game cover image by its name.
    Downloads it and saves as WEBP locally.
    Returns the file path or None if not found.
    """
    url = "https://api.rawg.io/api/games"
    params = {
        "key": RAWG_API_KEY,
        "search": game_name,
        "page_size": 1
    }

    print(f"[INFO] Searching RAWG for cover: {game_name}")
    response = requests.get(url, params=params, timeout=10)

    # Check if already cached
    cover_file = COVERS_DIR / f"{appid}.webp"
    if cover_file.exists():
        return str(cover_file)

    if response.status_code != 200:
        print(f"[ERROR] RAWG request failed: {response.status_code}")
        return None

    data = response.json()
    results = data.get("results", [])
    if not results:
        print(f"[WARNING] No results found in RAWG for {game_name}")
        return None

    cover_url = results[0].get("background_image")
    if not cover_url:
        print(f"[WARNING] No cover URL found in RAWG for {game_name}")
        return None

    try:
        # Download the cover image
        resp = requests.get(cover_url, timeout=10)
        if resp.status_code == 200:
            return save_image_as_webp(resp.content, appid)
        else:
            print(f"[ERROR] Failed to download cover for {game_name}, status {resp.status_code}")
    except Exception as e:
        print(f"[ERROR] Exception downloading cover for {game_name}: {e}")

    return None


def save_image_as_webp(content: bytes, appid: int) -> str:
    """
    Convert downloaded image bytes into WEBP and save locally.
    Returns the local file path.
    """
    try:
        img = Image.open(io.BytesIO(content))
        file_path = COVERS_DIR / f"{appid}.webp"
        img.save(file_path, "WEBP", quality=80, optimize=True)
        print(f"[INFO] Optimized cover saved: {file_path}")
        return str(file_path)
    except Exception as e:
        print(f"[ERROR] Failed to convert image for {appid}: {e}")
        return None
