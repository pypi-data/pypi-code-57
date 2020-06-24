from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound, HttpResponseServerError

def page_not_found_view(request, exception=None):
    return HttpResponseNotFound('Page not found')

def error_view(request):
    return HttpResponseServerError('Internal server error')


def permission_denied_view(request, exception=None):
    return HttpResponseForbidden('Permission denied')


def bad_request_view(request, exception=None):
    return HttpResponseBadRequest('Bad request')

