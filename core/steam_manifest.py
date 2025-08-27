import os
import re
from pathlib import Path

def _default_steam_root() -> Path:
    """Return a best-guess Steam root on Windows."""
    # You can improve this reading registry if you want. This covers the common path.
    return Path(r"C:\Program Files (x86)\Steam")

def _parse_libraryfolders(vdf_path: Path) -> list[Path]:
    """
    Parse libraryfolders.vdf and return all library paths as Path objects.
    Supports the modern VDF where entries are:
      "0" { "path" "X:\SteamLibrary" ... }
    """
    libs = []
    if not vdf_path.exists():
        return libs

    text = vdf_path.read_text(encoding="utf-8", errors="ignore")
    # Find blocks like: "123" { "path" "X:\\SteamLibrary" ... }
    # We’ll capture the path lines.
    for match in re.finditer(r'"\d+"\s*\{[^}]*?"path"\s*"([^"]+)"', text, re.IGNORECASE | re.DOTALL):
        raw = match.group(1)
        try:
            libs.append(Path(raw))
        except Exception:
            pass
    return libs

def get_installed_appids(steam_root: Path | None = None) -> set[int]:
    """
    Return a set of installed appids by scanning ALL Steam libraries.
    We verify installation by checking that the 'installdir' folder exists under 'common'.
    """
    if steam_root is None:
        steam_root = _default_steam_root()

    libraries: list[Path] = [steam_root]  # include main Steam root
    # Read extra libraries from libraryfolders.vdf
    vdf = steam_root / "steamapps" / "libraryfolders.vdf"
    libraries += _parse_libraryfolders(vdf)

    installed: set[int] = set()

    for lib in libraries:
        steamapps = lib / "steamapps"
        common = steamapps / "common"
        if not steamapps.exists():
            continue

        for fname in os.listdir(steamapps):
            if not fname.startswith("appmanifest_") or not fname.endswith(".acf"):
                continue

            acf_path = steamapps / fname
            try:
                data = acf_path.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue

            appid_match = re.search(r'"appid"\s*"(\d+)"', data)
            installdir_match = re.search(r'"installdir"\s*"([^"]+)"', data)

            if not appid_match:
                continue

            appid = int(appid_match.group(1))
            installdir = installdir_match.group(1) if installdir_match else None

            # Confirm the folder exists in /common to avoid stale manifests
            if installdir:
                install_path = common / installdir
                if install_path.is_dir():
                    installed.add(appid)
                    print(f"[MANIFEST] Installed: {appid} @ {install_path}")
                else:
                    print(f"[MANIFEST] Skipped (folder missing): {appid} -> {install_path}")
            else:
                # Fallback: if installdir missing, treat presence of manifest as installed
                # (very rare, but keep it conservative)
                installed.add(appid)
                print(f"[MANIFEST] Installed (no installdir field): {appid}")

    print(f"[MANIFEST] Total installed detected: {len(installed)}")
    return installed
