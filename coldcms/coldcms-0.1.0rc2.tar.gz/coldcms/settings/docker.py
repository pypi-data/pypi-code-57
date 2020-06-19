from os.path import join
from secrets import token_hex

from .base import *  # noqa

DEBUG = False
SECRET_KEY = token_hex(64)
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "coldcms",
        "USER": "coldcms",
        "PASSWORD": "coldcms",
        "HOST": "postgres",
        "PORT": "5432",
    }
}
BUILD_DIR = "/srv/static/coldcms_build/"
MEDIA_ROOT = join(BUILD_DIR, "media")
STATIC_ROOT = join(BUILD_DIR, "static")
WAGTAIL_ENABLE_UPDATE_CHECK = False
WAGTAILDOCS_SERVE_METHOD = 'direct'
