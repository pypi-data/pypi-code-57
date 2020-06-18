from django.http import HttpResponse
from django.shortcuts import render
from django.core import management

from webspace.cms import constants


def index(request):
    return render(
        request,
        '%s/bakery.html' % constants.ADMIN_TEMPLATES_PATH,
        {'cache_icon': 'cog'}
    )


def build(request):
    try:
        management.call_command('build')
        return HttpResponse("Build just finished !")
    except Exception:
        return HttpResponse("Une erreur est survenue")
