import os
from secrets import token_hex

from .base import *  # noqa

DEBUG = False
SECRET_KEY = os.getenv("SECRET_KEY", token_hex(64))
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
if os.getenv("ALLOWED_HOSTS"):
    ALLOWED_HOSTS += os.getenv("ALLOWED_HOSTS").split(",")

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": os.getenv("DB_NAME", "coldcms"),
        "USER": os.getenv("DB_USER", "coldcms"),
    }
}
if os.getenv("DB_HOST"):
    DATABASES["default"]["HOST"] = os.getenv("DB_HOST")
if os.getenv("DB_PASSWORD"):
    DATABASES["default"]["PASSWORD"] = os.getenv("DB_PASSWORD")

BUILD_DIR = os.getenv("BUILD_DIR", "/srv/app/coldcms/build/")
MEDIA_ROOT = os.path.join(BUILD_DIR, "media")
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static")  # noqa
WAGTAIL_ENABLE_UPDATE_CHECK = False
WAGTAILDOCS_SERVE_METHOD = 'direct'
