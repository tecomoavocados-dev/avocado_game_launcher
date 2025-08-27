import sqlite3
from pathlib import Path
import os

# Base folder in Roaming
APPDATA_DIR = Path(os.getenv("APPDATA")) / "Avocado Game Launcher" / "data"
DB_PATH = APPDATA_DIR / "games.db"
COVERS_DIR = APPDATA_DIR / "covers"

def init_db():
    """Initialize the database and folders if they don't exist."""
    APPDATA_DIR.mkdir(parents=True, exist_ok=True)  # Ensure data/ exists
    COVERS_DIR.mkdir(parents=True, exist_ok=True)  # Ensure covers/ exists

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            appid INTEGER UNIQUE,
            name TEXT NOT NULL,
            playtime INTEGER DEFAULT 0,
            cover TEXT,
            installed INTEGER DEFAULT 0
        )
    """)

    # Add 'installed' column if missing
    try:
        cursor.execute("ALTER TABLE games ADD COLUMN installed INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass

    conn.commit()
    conn.close()

def save_games(games: list[dict]):
    """
    Insert or update games in the database.
    Store the local cover path (inside Roaming/data/covers) and installation status.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for game in games:
        print(f"[DB] Saving game: {game.get('name')} ({game.get('appid')})")

        # If the cover exists locally, normalize path under covers/
        cover_path = game.get("cover")
        if cover_path and not cover_path.startswith(str(COVERS_DIR)):
            cover_path = str(COVERS_DIR / f"{game.get('appid')}.jpg")

        cursor.execute("""
            INSERT INTO games (appid, name, playtime, cover, installed)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(appid) DO UPDATE SET
                name = excluded.name,
                playtime = excluded.playtime,
                cover = excluded.cover,
                installed = excluded.installed
        """, (
            game.get("appid"),
            game.get("name"),
            game.get("playtime", 0),
            cover_path,
            1 if game.get("installed") else 0 
        ))

    conn.commit()
    conn.close()

def load_games() -> list[dict]:
    """Load all games from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT appid, name, playtime, cover, installed FROM games")
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "appid": r[0],
            "name": r[1],
            "playtime": r[2],
            "cover": r[3],
            "installed": bool(r[4])
        }
        for r in rows
    ]

def delete_game(appid: int):
    """Delete a game by appid from database and its cover if exists."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM games WHERE appid = ?", (appid,))
    conn.commit()
    conn.close()

    cover_file = COVERS_DIR / f"{appid}.jpg"
    if cover_file.exists():
        cover_file.unlink()
