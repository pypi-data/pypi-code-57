
import os

from cbsettings import DjangoDefaults


class BasementSettings(DjangoDefaults):

    BASE_DIR = NotImplemented
    DB_NAME = NotImplemented
    DEV_EMAIL = NotImplemented
    DOMAIN = NotImplemented

    ROOT_URLCONF = 'core.urls'

    ALLOWED_HOSTS = ['*']

    WSGI_APPLICATION = 'core.wsgi.application'

    TIME_ZONE = 'Europe/Kiev'

    USE_TZ = True

    EMAIL_USE_TLS = True

    SITE_ID = 1

    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]

    SILENCED_SYSTEM_CHECKS = ['mysql.E001', 'mysql.W002']

    USE_I18N = True
    USE_L10N = True

    @property
    def LOCALE_PATHS(self):
        return [os.path.join(self.BASE_DIR, 'locale')]

    @property
    def EMAIL_SUBJECT_PREFIX(self):
        return '{} |'.format(self.DOMAIN.title())

    @property
    def DEFAULT_FROM_EMAIL(self):
        return '{} <noreply@{}>'.format(self.DOMAIN.upper(), self.DOMAIN)

    @property
    def ADMINS(self):
        return ('Dev', self.DEV_EMAIL),

    @property
    def MANAGERS(self):
        return ('Dev', self.DEV_EMAIL),

    @property
    def MIDDLEWARE(self):
        return [
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.middleware.locale.LocaleMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ]

    @property
    def INSTALLED_APPS(self):
        return [
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.sites',
            'django.contrib.sitemaps'
        ]

    @property
    def DATABASES(self):
        return {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': self.DB_NAME,
                'USER': 'dev'
            }
        }

    @property
    def TEMPLATES(self):
        return [{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': self.TEMPLATE_DIRS,
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': self.CONTEXT_PROCESSORS
            }
        }]

    @property
    def TEMPLATE_DIRS(self):
        return [
            os.path.join(self.BASE_DIR, 'templates')
        ]

    @property
    def CONTEXT_PROCESSORS(self):
        return [
            'django.template.context_processors.i18n',
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.template.context_processors.media',
            'django.template.context_processors.static',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ]


class LocalSettingsMixin(object):

    DEBUG = True

    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'

    @property
    def EMAIL_FILE_PATH(self):
        return os.path.join(self.BASE_DIR, 'tmp')


class ProductionSettingsMixin(object):

    DEBUG = False

    EMAIL_PORT = 587
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'

    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    @property
    def STATICFILES_DIRS(self):
        return [os.path.join(self.BASE_DIR, 'static')]

    @property
    def STATIC_ROOT(self):
        return '/home/dev/sites/{}/public/static'.format(self.DOMAIN)

    @property
    def MEDIA_ROOT(self):
        return '/home/dev/sites/{}/public/media'.format(self.DOMAIN)