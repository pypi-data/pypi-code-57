from django.apps import AppConfig


class WagtailStaticConfig(AppConfig):
    name = 'wagtailstatic'
    label = 'wagtailstatic'
    verbose_name = 'Wagtail Static'

    def ready(self):
        import wagtailstatic.signals