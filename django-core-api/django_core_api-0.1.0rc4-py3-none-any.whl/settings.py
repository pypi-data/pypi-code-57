# pylint: disable=W0614

import logging
import os
import sys

import dj_database_url
from django.conf import settings

from envparse import env

from django_core_api import parse_app_name

core_settings = sys.modules[__name__]


def add_to_settings(setting_name, value):
    current_value = getattr(settings, setting_name, None)
    if current_value:
        if isinstance(current_value, list):
            setattr(core_settings, setting_name, value + current_value)
        elif isinstance(current_value, dict):
            current_value.update(value)
        else:
            setattr(core_settings, setting_name, value)
    else:
        setattr(core_settings, setting_name, value)


APP_NAME, ENV, VERSION = parse_app_name()

# Security
DEBUG = env.bool('DEBUG', default=True)
USE_X_FORWARDED_HOST = True


# Logging
LOG_LEVEL = env.str('LOG_LEVEL', default=logging.DEBUG if DEBUG else logging.WARNING)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
            'propagate': False
        },
    },
}

logger = logging.getLogger(APP_NAME)


# RestFul
REST_FRAMEWORK = {
    'PAGE_SIZE': env.int('PAGE_SIZE', default=50),
    'DEFAULT_FILTER_BACKENDS': (
        'django_core_api.filters.CoreFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DATETIME_FORMAT': '%Y-%m-%dT%H:%M:%SZ',
    'SEARCH_PARAM': 'q',
    'ORDERING_PARAM': 'sort',
}


# Application
SITE_NAME = APP_NAME.replace('_', ' ').title()
SITE_URL = env.str('SITE_URL', default=f'http://local.{APP_NAME}.com.br')
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'storages',
    'rest_framework',
    'django_filters',
]
ROOT_URLCONF = f'{APP_NAME}.urls'
WSGI_APPLICATION = f'{APP_NAME}.wsgi.application'


# Internationalization
LANGUAGE_CODE = 'en'
ADMIN_LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'UTC'
ADMIN_TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Database
os.environ.setdefault('DATABASE_URL', f'postgres://postgres@127.0.0.1:5432/{APP_NAME}')
DATABASES = {
    'default': dj_database_url.config(
        env='DATABASE_URL',
        conn_max_age=60,
    ),
}
DATABASE_ROUTERS = []


__database_name = env.str('DATABASE_URL').split('/')[-1]
if __database_name != APP_NAME:
    logger.info(f"Database name {__database_name} inconsistent with APP NAME {APP_NAME}")


READ_DATABASE_URL = env.str('READ_DATABASE_URL', default=None)
if READ_DATABASE_URL:
    DATABASES['replica'] = dj_database_url.config(
        env='READ_DATABASE_URL',
        conn_max_age=60,
    )
    DATABASES['replica']['TEST'] = {
        'MIRROR': 'default',
    }
    DATABASE_ROUTERS.append('django_core_api.routers.ReaderDatabaseRouter')


DATABASE_ROUTERS.append('django_core_api.routers.DefaultDatabaseRouter')


# Templates & Static
MEDIA_ROOT = os.path.join(settings.BASE_DIR, 'media')
STATIC_ROOT = os.path.join(settings.BASE_DIR, 'staticfiles')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# Cache
if 'REDIS_URL' in os.environ:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": env.str('REDIS_URL'),
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient"
            },
            "KEY_PREFIX": f"{APP_NAME}#"
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }

CACHE_TTL = env.int('CACHE_TTL', default=5 * 60)
REST_FRAMEWORK_EXTENSIONS = {
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': CACHE_TTL,
    'DEFAULT_CACHE_ERRORS': False,
    'DEFAULT_CACHE_KEY_FUNC': 'django_core_api.cache.cache_key_constructor',
    'DEFAULT_OBJECT_CACHE_KEY_FUNC': 'django_core_api.cache.cache_key_constructor',
    'DEFAULT_LIST_CACHE_KEY_FUNC': 'django_core_api.cache.cache_key_constructor',
}


# Middlewares
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_core_api.middleware.AdminLocaleURLMiddleware',
]


# Google Cloud Storage
if env.str("GS_BUCKET_NAME", None):
    GS_BUCKET_NAME = env.str("GS_BUCKET_NAME")
    DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
    STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
    GS_DEFAULT_ACL = "publicRead"
else:
    logger.warning("You're using a local storage for media files.")
    MEDIA_URL = f'{MEDIA_ROOT}/'
    STATIC_URL = '/static/'


# DEBUG environment
if DEBUG:
    ALLOWED_HOSTS = ['*']


def collect_settings():
    all_settings = []
    for setting_name in [item for item in dir(core_settings) if not item.startswith("__")]:
        value = getattr(core_settings, setting_name)
        add_to_settings(setting_name, value)
        all_settings.append(setting_name)
    return all_settings


# because we can't trust None, that could mean
# "not set yet" or "set as None:
UNSET = object()

__all__ = collect_settings()
