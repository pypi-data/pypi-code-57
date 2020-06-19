from django.apps import AppConfig
from wagtail.core.signals import page_published, page_unpublished


class BlogConfig(AppConfig):
    name = "coldcms.blog"

    def ready(self):
        from coldcms.blog.views import refresh_index_pages

        page_published.connect(refresh_index_pages)
        page_unpublished.connect(refresh_index_pages)
