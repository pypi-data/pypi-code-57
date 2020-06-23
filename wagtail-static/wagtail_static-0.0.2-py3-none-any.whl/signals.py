from wagtail.core.signals import page_published, page_unpublished

from .local_files import create_static_file, get_local_filepath


def static_creation_on_publish(sender, **kwargs):
    page = kwargs['instance']
    if page.is_static:
        create_static_file(page)


page_published.connect(static_creation_on_publish)


def destroy_static_file(sender, **kwargs):
    page = kwargs['instance']
    if page.is_static:
        path = get_local_filepath(page)
        path.unlink(missing_ok=True)


page_unpublished.connect(destroy_static_file)