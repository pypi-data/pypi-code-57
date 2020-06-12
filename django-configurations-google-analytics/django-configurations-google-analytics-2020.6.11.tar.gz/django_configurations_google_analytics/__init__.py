import os

from configurations import Configuration, values

APP = 'django_configurations_google_analytics'

class GoogleAnalyticsConfiguration(Configuration):
    GA_ID = values.Value(None)

    @classmethod
    def setup(cls):
        super(GoogleAnalyticsConfiguration, cls).setup()
        if APP not in cls.INSTALLED_APPS:
            cls.INSTALLED_APPS.append(APP)
