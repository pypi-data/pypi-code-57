# -*- coding: utf-8 -*-
"""
Django settings for remo_app project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
from __future__ import absolute_import, unicode_literals

import os
from pathlib import Path
import environ
import platform
import base64


ROOT_DIR = environ.Path(__file__) - 4  # (remo_app/remo_app/config/standalone/settings.py - 4 = remo_app/)
APPS_DIR = ROOT_DIR.path('remo_app')

DOCS_DIR = os.path.abspath(str(APPS_DIR.path('staticfiles/docs')))

env = environ.Env()

RUNNING_MODE = 'standalone'
REMO_HOME = env('REMO_HOME', default=str(Path.home().joinpath('.remo')))
DEMO_USERNAME = None

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
s = "{}-142-{}".format(platform.platform(), 'remo')
SECRET_KEY = env('DJANGO_SECRET_KEY', default=str(base64.urlsafe_b64encode(s.encode("utf-8")), "utf-8"))

# APP CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)
THIRD_PARTY_APPS = (
    'django_filters',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    # PROFILER_ON: uncomment
    # 'silk',
)

# Apps specific for this project go here.
LOCAL_APPS = (
    'remo_app.template_filters.apps.TemplateFiltersConfig',
    'remo_app.remo.apps.RemoConfig',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
# PROFILER_ON: for silk change to MIDDLEWARE [] instead of MIDDLEWARE_CLASSES ()
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'remo_app.remo.api.middleware.LocalUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware', - needed to comment for embeding to Jupyter Notebook
    # PROFILER_ON: uncomment
    # 'silk.middleware.SilkyMiddleware',
]

# Determine profiling setting
# PROFILER_ON: uncomment
# SILKY_META = True
# SILKY_PYTHON_PROFILER = True
# SILKY_PYTHON_PROFILER_BINARY = True
# SILKY_PYTHON_PROFILER_RESULT_PATH = '/app/profiling'
#
# PROFILING_SQL_QUERIES = True
# PROFILING_LOGGER_NAME = 'remo_app'

# MIGRATIONS CONFIGURATION
# ------------------------------------------------------------------------------
# MIGRATION_MODULES = {
# }

# DEBUG
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool('DJANGO_DEBUG', False)

# Used inside migrations
# INSIDE_TEST = False

# FIXTURE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
# FIXTURE_DIRS = (
#     str(APPS_DIR.path('fixtures')),
# )

# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')

SENDGRID_API_KEY = env('SENDGRID_API_KEY',
                       default='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')

EMAIL_LIST = env('EMAIL_LIST', default=['andrea.larosa@rediscovery.io', 'volodymyr@remo.ai', 'pooja@remo.ai'])

# MANAGER CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
# TODO: change to remo email
# ADMINS = (
#     ('remo', 'notification@remo'),
# )

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
# MANAGERS = ADMINS

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': env.db('DATABASE_URL', default='postgres:///remo'),
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(REMO_HOME, 'remo_db.sqlite3'),
#     }
# }
# DATABASES['default']['ATOMIC_REQUESTS'] = True
# DATABASES['default']['OPTIONS'] = dict(timeout=30)

# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'UTC'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-us'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        'DIRS': [
            str(APPS_DIR.path('templates')),
        ],
        'OPTIONS': {
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            'debug': DEBUG,
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                # Your stuff: custom template context processors go here
            ],
        },
    },
]

# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(APPS_DIR('staticfiles'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    str(ROOT_DIR.path('remo_app/static')),
    str(ROOT_DIR.path('rediscovery_client/static')),
)

# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = os.path.join(REMO_HOME, 'media')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'

# URL Configuration
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'remo_app.config.standalone.urls'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'remo_app.config.standalone.wsgi.application'

# Your common stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------
LOGIN_URL = 'rest_login'
LOGOUT_URL = 'rest_logout'
LOGIN_REDIRECT_URL = 'home'

# Logging
# ---------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s RemoApp] %(levelname)s - %(message)s',
            'datefmt': '%H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'remo_app': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'django.security.DisallowedHost': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

# DJANGO REST FRAMEWORK SETTINGS
# ------------------------------
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        # basic auth for swagger
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 32,

    # 'DEFAULT_THROTTLE_CLASSES': [
    #     'rest_framework.throttling.AnonRateThrottle',
    #     'rest_framework.throttling.UserRateThrottle',
    #     'rest_framework.throttling.ScopedRateThrottle',
    # ],
    # 'DEFAULT_THROTTLE_RATES': {
    #     'anon': '2/second',
    #     'user': '10/second',
    #     'uploads': '5/second'
    # }
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'remo_app.remo.api.views.backend.CustomModelBackend'
]

THUMBNAIL_SIZE = (50, 50)
PREVIEW_SIZE = (225, 225)
VIEW_SIZE = (1000, 1000)
VIEW_QUALITY = 60
PREVIEW_QUALITY = 60
THUMBNAIL_QUALITY = 95
HIGH_RESOLUTION = (3840, 2160)
HIGH_RESOLUTION_QUALITY = 60
HIGH_RESOLUTION_THRESHOLD = int(HIGH_RESOLUTION[0] * HIGH_RESOLUTION[1] * 1.3) # +30%
HIGH_RESOLUTION_FILE_SIZE_THRESHOLD = 10 * 1024**2   # 10MB
CACHE_RETENTION_PERIOD = 120    # seconds
CACHE_IMAGES_LIMIT = 2

TMP_DIR = os.path.join(REMO_HOME, 'tmp')

IMAGE_MIME_TYPES = {
    'image/jpeg', 'image/png', 'image/jpg', 'image/tiff'
}

IMAGE_FILE_EXTENSIONS = {
    '.jpeg', '.png', '.jpg', '.tiff', '.tif'
}

ANNOTATION_MIME_TYPES = {
    'application/json', 'text/xml', 'text/csv'
}

ANNOTATION_FILE_EXTENSIONS = {
    '.json', '.xml', '.csv'
}

ARCHIVE_MIME_TYPES = {
    'application/zip', 'application/gzip', 'application/x-bzip2', 'application/x-tar', 'application/x-xz'
}

ARCHIVE_FILE_EXTENSIONS = {
    '.zip', '.gz', '.tar', '.tgz', '.tar.gz', '.bz2', '.tar.bz2', '.xz'
}

REST_AUTH_SERIALIZERS = {
    'LOGIN_SERIALIZER': 'remo_app.remo.api.serializers.LoginSerializer'
}

# 5 GB max file size for upload
MAX_FILE_SIZE = 5 * 1024**3
DATA_UPLOAD_MAX_MEMORY_SIZE = MAX_FILE_SIZE  # to override django default value

# Maximum image size (in bytes) which are automatically downloaded
# from external resource. For example, during annotations upload
MAX_EXTERNAL_DOWNLOAD_IMAGE_SIZE = MAX_FILE_SIZE

# Hubspot API KEY authorization
# Set HUBSPOT_API_KEY to None to disable Hubspot requests
HUBSPOT_API_KEY = env('HUBSPOT_API_KEY', default='5aeb26cd-2515-4681-b2f4-68248ff651a2')
HUBSPOT_API_THROTTLING_RETRIES = 10

KNOWLEDGE_GRAPH_API_KEY = env('KNOWLEDGE_GRAPH_API_KEY', default='AIzaSyC48ajVnypsGl5MnVCp_c2xRVxAUxl0HfM')
USE_KNOWLEDGE_GRAPH_API = env('USE_KNOWLEDGE_GRAPH_API', default=False)
# IMAGE_UPLOADING_THREADS = env('IMAGE_UPLOADING_THREADS', default=max(multiprocessing.cpu_count() - 1, 1))
IMAGE_UPLOADING_THREADS = env('IMAGE_UPLOADING_THREADS', default=1)
FEEDBACKS_ACCESS_KEY = env('FEEDBACKS_ACCESS_KEY', default='golden_age')
LOCAL_FILES = '/local-files'
ALLOWED_HOSTS = ['.localhost']
STORAGE = 'local'
