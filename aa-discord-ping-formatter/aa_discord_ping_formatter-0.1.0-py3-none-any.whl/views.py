from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from . import __title__


@login_required
@permission_required('discordpingformatter.basic_access')
def index(request):
    context = {
        'title': __title__
    }

    return render(request, 'discordpingformatter/index.html', context)
