from pathlib import Path


class Settings(object):
    LOCALES = {
        "en": "English",
        "ru": "Русский",
    }
    SECRET_KEY = "kjmhg345bjknhg7jhKGM98KNJKv1nMKJH3YNG2bjvn326jmh"

    SITE_TITLE = "FogStone"
    CONTENT_DIR = Path(__file__).parent / Path("data")
    TEMPLATE_FOLDER = Path("templates")
    STATIC_FOLDER = Path("static")

    TRANSLIT_PERMALINKS = False
    TRANSLIT_CODE = "ru"
    TRANSLIT_REVERSE = True
    SEARCH_ENABLED = False
