from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from . import __title__

from .app_settings import (
    AA_DISCORDFORMATTER_ADDITIONAL_PING_TARGETS,
    AA_DISCORDFORMATTER_ADDITIONAL_FLEET_TYPES,
    AA_DISCORDFORMATTER_ADDITIONAL_PING_WEBHOOKS
)


@login_required
@permission_required('discordpingformatter.basic_access')
def index(request):
    context = {
        'title': __title__,
        'additionalPingTargets': AA_DISCORDFORMATTER_ADDITIONAL_PING_TARGETS,
        'additionalFleetTypes': AA_DISCORDFORMATTER_ADDITIONAL_FLEET_TYPES,
        'additionalPingWebhooks': AA_DISCORDFORMATTER_ADDITIONAL_PING_WEBHOOKS
    }

    return render(request, 'discordpingformatter/index.html', context)
