from django.http import HttpResponse
from django.conf import settings
from wagtail.core import hooks

from .local_files import create_static_file, get_local_filepath


@hooks.register('before_serve_page')
def static_serve(page, request, serve_args, serve_kwargs):
    if page.is_static and \
        getattr(settings, 'STATIC_PAGE_SERVING', False) and \
            not getattr(request, 'static_generation', False):
        static_filepath = get_local_filepath(page)
        if not static_filepath.exists():
            static_filepath = create_static_file(page)
        return HttpResponse(static_filepath.read_bytes())
