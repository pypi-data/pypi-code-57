from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render

from .Confirm import sendConfirm, verifyToken
from .errors import NotAllFieldCompiled


# Create your views here.
def verify(request, email, email_token):
    try:
        template = settings.EMAIL_PAGE_TEMPLATE
        return render(request, template, {'success': verifyToken(email, email_token)})
    except AttributeError:
        raise NotAllFieldCompiled('EMAIL_PAGE_TEMPLATE field not found')


def send(request):
    email = request.POST.get('email', '')
    user = get_user_model().objects.get(email=email)
    sendConfirm(user)
    return HttpResponse('ok')
