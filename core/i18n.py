from core.manager import load_settings, save_settings

DEFAULT_LANG = "en"

TRANSLATIONS = {
    "es": {
        "app.title": "Avocado Game Launcher - Gestor de Juegos",
        "menu.import": "Importar juego",
        "menu.import_local": "Importar",
        "your.games": "Tus juegos",
        "information.games":"Información del juego",
        "import.steam": "Importar de Steam",
        "steam.username": "Inserta tu nombre de usuario de Steam",
        "not_found_steam": "No se encontraron juegos de Steam",
        "import.success": "Se importaron {count} juegos instalados.",
        "info.game": "Selecciona un juego para ver su información",
        "menu.settings": "Configuración",
        "menu.settings.configure": "Configurar",
        "title.save": "Guardar",
        "title.cancel": "Cancelar",
        "release.date": "Fecha de lanzamiento",
        "lang.title": "Idioma",
        "menu.help": "Ayuda",
        "menu.about": "Acerca de",
        "menu.report_issue": "Informar de un problema",
        "current_version": "Versión actual",
        "check_for_updates": "Buscar actualizaciones",
        "username": "Nombre de usuario",
        "msg.tray_info": "La aplicación se está ejecutando en segundo plano.",
        "title.restore": "Restaurar",
        "title.exit": "Salir",
        "release.date": "Fecha de lanzamiento",
        "settings.tray_icon": "Minimizar a la bandeja",
        "publisher": "Editor",
        "developer": "Desarrollado por",
        "author": "Autor",
        "app.title.settings": "Avocado Game Launcher - Configuración",
        "settings.saved": "Configuración guardada, es necesario reiniciar la aplicación para que los cambios surtan efecto.",
        "title.settings": "Configuración",
        "steam.id": "ID de Steam",
        "steam.username.settings": "Nombre de usuario de Steam",
        "genres.game": "Géneros del juego",
        "update_available": "Actualización disponible",
        "contact": "Contacto",
        "new_version_available": "Nueva versión disponible",
        "visit_github_to_download": "Visita GitHub para descargar",
        "no_updates": "No hay actualizaciones",
        "you_have_latest_version": "Tienes la última versión",
        "network_error": "Error de red",
        "check_internet_connection": "Verifica tu conexión a Internet",
        "error": "Error"
    },
    "en": {
        "app.title": "Avocado Game Launcher - Game Library Manager",
        "menu.import": "Import a Game",
        "menu.import_local": "Import",
        "your.games": "Your games",
        "information.games":"Game Information",
        "import.steam": "Import from Steam",
        "steam.username": "Enter your Steam username",
        "not_found_steam": "No installed games found on Steam.",
        "import.success": "Imported {count} installed games.",
        "info.game": "Select game to see information",
        "menu.settings": "Settings",
        "menu.settings.configure": "Configure",
        "release.date": "Release Date",
        "title.save": "Save",
        "title.cancel": "Cancel",
        "lang.title": "Language",
        "menu.help": "Help",
        "menu.about": "About",
        "menu.report_issue": "Report an Issue",
        "current_version": "Current Version",
        "check_for_updates": "Check for Updates",
        "username": "Username",
        "msg.tray_info": "The application is running in the background.",
        "title.restore": "Restore",
        "title.exit": "Exit",
        "release.date": "Release Date",
        "settings.tray_icon": "Minimize to Tray",
        "publisher": "Publisher",
        "developer": "Developer by",
        "author": "Author",
        "app.title.settings": "Avocado Game Launcher - Settings",
        "settings.saved": "Settings saved. Please restart the application for changes to take effect.",
        "title.settings": "Settings",
        "steam.id": "Steam ID",
        "steam.username.settings": "Steam Username",
        "genres.game": "Game Genres",
        "update_available": "Update Available",
        "contact": "Contact",
        "new_version_available": "New Version Available",
        "visit_github_to_download": "Visit GitHub to Download",
        "no_updates": "No Updates Available",
        "you_have_latest_version": "You have the latest version",
        "network_error": "Network Error",
        "check_internet_connection": "Check your internet connection",
        "error": "Error"
    },
}



def get_language() -> str:
    settings = load_settings()
    lang = settings.get("language", DEFAULT_LANG)
    return lang if lang in TRANSLATIONS else DEFAULT_LANG

def set_language(lang_code: str):
    """ Set the application language and save it to settings."""
    if lang_code not in TRANSLATIONS:
        return
    settings = load_settings()
    settings["language"] = lang_code
    from core.manager import save_settings
    save_settings(settings)


def t(key: str) -> str:
    lang = get_language()
    return TRANSLATIONS.get(lang, TRANSLATIONS[DEFAULT_LANG]).get(key, key)