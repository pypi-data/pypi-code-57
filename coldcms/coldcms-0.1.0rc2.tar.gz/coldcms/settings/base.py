# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from os.path import abspath, dirname, join

PROJECT_DIR = dirname(dirname(abspath(__file__)))
BASE_DIR = dirname(PROJECT_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# Application definition

INSTALLED_APPS = [
    "coldcms.blocks",
    "coldcms.home",
    "coldcms.legal_notice",
    "coldcms.simple_page",
    "coldcms.contact",
    "coldcms.generic_page",
    "coldcms.faq",
    "coldcms.partners",
    "coldcms.site_settings",
    "coldcms.blog",
    "coldcms.wagtail_customization",
    "svg",
    "django_assets",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.admin",
    "wagtail.core",
    "wagtail.contrib.modeladmin",
    "wagtail.contrib.settings",
    "modelcluster",
    "taggit",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
    "bakery",
    "wagtailbakery",
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "wagtail.core.middleware.SiteMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

ROOT_URLCONF = "coldcms.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [join(PROJECT_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "wagtail.contrib.settings.context_processors.settings",
            ]
        },
    }
]

WSGI_APPLICATION = "coldcms.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    "default": {"ENGINE": "django.contrib.gis.db.backends.postgis", "NAME": "coldcms"}
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators
DCAPV = "django.contrib.auth.password_validation"
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": DCAPV + ".UserAttributeSimilarityValidator"},
    {"NAME": DCAPV + ".MinimumLengthValidator"},
    {"NAME": DCAPV + ".CommonPasswordValidator"},
    {"NAME": DCAPV + ".NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = "fr-fr"
LANGUAGES = [("fr", "Français"), ("en", "English")]

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = [join(PROJECT_DIR, "locale")]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [join(PROJECT_DIR, "static")]

# ManifestStaticFilesStorage is recommended in production, to prevent outdated
# Javascript / CSS assets being served from cache (e.g. after a Wagtail
# upgrade).
# See https://docs.djangoproject.com/en/2.1/ref/contrib/staticfiles/
# #manifeststaticfilesstorage
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

STATIC_ROOT = join(BASE_DIR, "static")
STATIC_URL = "/static/"

MEDIA_ROOT = join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# Config django-assets
ASSETS_MODULES = ["coldcms.assets"]
ASSETS_ROOT = STATICFILES_DIRS[0]

# Wagtail settings
WAGTAIL_SITE_NAME = "coldcms"
WAGTAILIMAGES_JPEG_QUALITY = 80
WAGTAIL_ALLOW_UNICODE_SLUGS = False

# Base URL to use when referring to full URLs within the Wagtail admin backend
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = "http://example.com"

# Wagtail-bakery config
BUILD_DIR = join(BASE_DIR, "build")
BAKERY_VIEWS = ("wagtailbakery.views.AllPublishedPagesView",)

# SVG settings
SVG_DIRS = [
    join(STATICFILES_DIRS[0], "svg", path)
    for path in [
        "",
        "fontawesome/solid/",
        "fontawesome/regular/",
        "fontawesome/brands/",
    ]
]
