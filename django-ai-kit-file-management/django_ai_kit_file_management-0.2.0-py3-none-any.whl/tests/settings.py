import os
from rest_framework.permissions import AllowAny


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = "SLIDFHVsdkjlr3lrnnlrvnker"

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.admin",
    "rest_framework",
    "ai_kit_file_management",
)


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
}

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
ROOT_URLCONF = "ai_kit_file_management.urls"


AI_KIT_FILE_MANAGEMENT = {
    # intentionally small so we can test this setting easily
    "MAX_FILE_SIZE_KB": 1,
    "ALLOWED_FORMATS": [
        "image/jpeg",
        "image/png",
        "application/pdf",
        "application/zip",
        "text/comma-separated-values",
        "text/plain",
    ],
    "PERMISSION_CLASSES": (AllowAny,),
    "FILESERVER_BACKEND": "dev",
}
