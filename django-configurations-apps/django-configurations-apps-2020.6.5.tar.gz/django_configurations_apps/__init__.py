import os

from configurations import Configuration, values
import django_find_apps

def getlist(path):
    return list(filter(
        None,map(lambda s:s.strip(),open(path).read().splitlines() if path else [])
    ))

class AppsConfiguration(Configuration):
    INSTALLED_APPS = values.ListValue([])
    INSTALLED_APPS_FILE = values.Value(None)
    INSTALLED_APPS_FIND = bool(os.getenv('INSTALLED_APPS_FIND','').lower() in ('yes', 'y', 'true', '1'))

    @classmethod
    def setup(cls):
        super(AppsConfiguration, cls).setup()
        for app in getlist(cls.INSTALLED_APPS_FILE):
            if app not in cls.INSTALLED_APPS:
                cls.INSTALLED_APPS.append(app)
        if cls.INSTALLED_APPS_FIND:
            path = cls.BASE_DIR if hasattr(cls,'BASE_DIR') else os.getcwd()
            for app in django_find_apps.find_apps(path):
                if app not in cls.INSTALLED_APPS:
                    cls.INSTALLED_APPS.append(app)
