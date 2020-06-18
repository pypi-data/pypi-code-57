from django.template.response import SimpleTemplateResponse
from wagtail.core.views import serve as wagtail_serve

from .utils import activate_amp_mode


def serve(request, path):
    with activate_amp_mode():
        response = wagtail_serve(request, path)
        if isinstance(response, SimpleTemplateResponse):
            response.render()
        return response
