import os

from .dev import *  # NOQA

DOCKER_TEST = os.environ.get("DOCKER_TEST", "")
if DOCKER_TEST == "True":
    DATABASES = {
        "default": {
            "ENGINE": "django.contrib.gis.db.backends.postgis",
            "NAME": "postgres",
            "USER": "postgres",
            "PASSWORD": "mysecretpassword",
            "HOST": "mdillon__postgis",
            "PORT": "5432",
        }
    }
