import fs
from django.apps import AppConfig
from webspace.cms.bakery.signal_handlers import register_signal_handlers


class CmsConfig(AppConfig):
    name = 'webspace.cms'
    label = 'cms'
    verbose_name = 'CMS'
    filesystem_name = "osfs:///"
    filesystem = fs.open_fs(filesystem_name)

    def ready(self):
        register_signal_handlers()
