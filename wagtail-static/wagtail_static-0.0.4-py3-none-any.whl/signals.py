from django.conf import settings
from wagtail.core.signals import page_published, page_unpublished

from .local_files import create_static_file, get_local_filepath


def static_creation_on_publish(sender, **kwargs):
    page = kwargs['instance']
    if getattr(page, 'is_static', False) \
         and getattr(settings, 'STATIC_PAGE_SERVING', False):
        create_static_file(page)


page_published.connect(static_creation_on_publish)


def destroy_static_file(sender, **kwargs):
    page = kwargs['instance']
    if getattr(page, 'is_static', False) and \
         getattr(settings, 'STATIC_PAGE_SERVING', False):
        path = get_local_filepath(page)
        path.unlink(missing_ok=True)


page_unpublished.connect(destroy_static_file)
