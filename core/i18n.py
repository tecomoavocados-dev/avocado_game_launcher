from core.manager import load_settings

DEFAULT_LANG = "en"

TRANSLATIONS = {
    "es": {
        "app.title": "Avocado - Gestor de Juegos",
        "button.add_game": "Agregar Juego",
        "button.launch_game": "Iniciar Juego",
        "button.delete": "Eliminar",
        "menu.import": "Importar",
        "menu.import_local": "Desde Archivo Local",
        "menu.help": "Ayuda",
        "menu.about": "Acerca de",
        "title.about": "Acerca de",
        "feature_not_implemented": "Funcionalidad no implementada aún.",
        "menu.folder": "Importar carpeta.",
        "menu.import_folder": "Desde Carpeta",
        "menu.settings": "Configuración",
        "button.profile": "Mi Perfil",
        "title.save": "Guardar",
        "title.exit": "Salir",
        "settings.saved": "Configuración guardada exitosamente, reinicie la aplicación si es necesario.",
        "lang.title": "Idioma",
        "menu.report_issue": "Reportar un problema",
    },
    "en": {
        "app.title": "Avocado - Game Library Manager",
        "button.add_game": "Add Game",
        "button.launch_game": "Launch Game",
        "button.delete": "Delete",
        "menu.import": "Import",
        "menu.import_local": "From Local File",
        "menu.help": "Help",
        "menu.about": "About",
        "title.about": "About",
        "feature_not_implemented": "Feature not implemented yet.",
        "menu.folder": "Import folder.",
        "menu.import_folder": "From Folder",
        "menu.settings": "Settings",
        "button.profile": "My Profile",
        "title.save": "Save",
        "title.exit": "Exit",
        "settings.saved": "Settings saved successfully, please restart the app if needed.",
        "lang.title": "Language",
        "menu.report_issue": "Report an issue",

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
