from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from rest_auth.app_settings import TokenSerializer, create_token
from rest_auth.models import TokenModel
from rest_auth.utils import jwt_encode
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class DemoAccessViewSet(APIView):
    permission_classes = (AllowAny,)
    token_model = TokenModel

    def get(self, request, *args, **kwargs):
        user = authenticate(username=settings.DEMO_USERNAME, password=settings.DEMO_PWD)

        if getattr(settings, 'REST_USE_JWT', False):
            token = jwt_encode(user)
        else:
            token = create_token(self.token_model, user, TokenSerializer)

        if getattr(settings, 'REST_SESSION_LOGIN', True):
            django_login(self.request, user)

        return Response({'key': str(token)})
