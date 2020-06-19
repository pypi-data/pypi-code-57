from django.conf import settings
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from remo_app.remo.use_cases import is_remo_local


class Settings(APIView):
    permission_classes = (AllowAny,)
    enable_login = 'enable_login'
    running_mode = 'running_mode'
    viewer = 'viewer'
    demo = 'demo'

    @staticmethod
    def is_electron_client(request):
        try:
            return 'Electron' in request.META.get('HTTP_USER_AGENT', '')
        except Exception:
            return False

    def get(self, request):
        remo_settings = {
            self.enable_login: True,
            self.running_mode: settings.RUNNING_MODE,
            self.viewer: 'browser',
            self.demo: self.request.user.username == settings.DEMO_USERNAME
        }

        if is_remo_local():
            remo_settings[self.enable_login] = False

        if self.is_electron_client(request):
            remo_settings[self.viewer] = 'electron'

        return JsonResponse(remo_settings)
