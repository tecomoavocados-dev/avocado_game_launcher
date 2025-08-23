import requests
from dotenv import load_dotenv
from core.manager import resource_path
import os

dotenv_path = resource_path('.env')
load_dotenv(dotenv_path=dotenv_path)
RAWG_API_KEY = os.getenv('RAWG_API_KEY')

def fetch_rawg_image(game_name: str) -> str | None:
    """
    Fetch game cover image from RAWG API by game name.
    Returns the image URL or None if not found.
    """
    url = f"https://api.rawg.io/api/games?key={RAWG_API_KEY}&search={game_name}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        results = response.json().get("results")
        if results:
            return results[0].get("background_image")
    except Exception as e:
        print(f"Error fetching image for '{game_name}': {e}")
    return None