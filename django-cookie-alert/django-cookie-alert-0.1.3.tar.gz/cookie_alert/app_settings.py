from django.conf import settings

DEFAULTS = {
    'POLICY_REVERSE_ID': 'privacy-policy',  # url reverse name or reverse page id if used together with CMS
    'WITH_ANALYSIS_CHOICE': True,
}


class Settings:
    def __init__(self, site_settings=None, defaults=None):
        self.site_settings = site_settings
        self.defaults = defaults

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError("Invalid setting key: '%s'" % attr)
        return self.site_settings.get(attr, self.defaults[attr])

    def get_all(self):
        return [(k, getattr(self, k)) for k in self.defaults.keys()]


cookie_alert_settings = Settings(getattr(settings, 'COOKIE_ALERT', {}), DEFAULTS)
