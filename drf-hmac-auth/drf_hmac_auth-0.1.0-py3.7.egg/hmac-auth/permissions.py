from rest_framework.permissions import BasePermission
from .models import Token
from .HMACToken import HmacToken, TokenPeriod
#from django.conf import settings

#loginHeader = settings.VARIABLE.get('HmacToken', 'HMAC-Token')

class TokenPermission(BasePermission):
    message = 'Wrong or expired temporary token'

    def has_object_permission(self, request, view, user):
        if 'HMAC-Login' not in request.headers or 'HMAC-Times' not in request.headers or 'HMAC-Token' not in request.headers:
            return False
        token = request.headers['HMAC-Token']
        login = request.headers['HMAC-Login']
        times = request.headers['HMAC-Times']
        tokens = Token.objects.get(user=user).all() 
        if len(tokens) == 0:
            return False
        crypt = HmacToken(tokens[0].token, TokenPeriod.day)
        return crypt.checkToken(login, times, token)
        

