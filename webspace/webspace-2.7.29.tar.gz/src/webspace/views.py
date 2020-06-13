from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.contrib import auth


def logout_user(request):
    auth.logout(request)
    return HttpResponseRedirect('/freelance/connexion')


def robots(request):
    with open('app/www/robots.txt', 'rb') as rb:
        response = HttpResponse(rb.read(), content_type='text/plain')
        return response


def error_404(request, exception):
    return render(request, 'www/404.html', {}, status=404)
