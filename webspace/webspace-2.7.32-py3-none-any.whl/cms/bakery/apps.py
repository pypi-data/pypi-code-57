import fs
from django.conf import settings
from django.apps import AppConfig
from .signal_handlers import register_signal_handlers


class BakeryConfig(AppConfig):
    name = 'bakery'
    verbose_name = "Bakery"
    filesystem_name = getattr(settings, 'BAKERY_FILESYSTEM', "osfs:///")
    filesystem = fs.open_fs(filesystem_name)

    def ready(self):
        register_signal_handlers()
