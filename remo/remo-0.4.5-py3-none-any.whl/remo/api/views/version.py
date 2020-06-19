from django.http import JsonResponse, Http404
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from remo_app import __version__
from remo_app.remo.models.downloads import UserVersion
from remo_app.remo.stores.version_store import Version as VersionStore


class Version(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]

        return request.META.get('REMOTE_ADDR', '')

    def get(self, request):
        platform = request.query_params.get('electron-app-platform')
        if not platform:
            version = request.query_params.get('check-updates-for-version')
            if version:
                # save statistics
                UserVersion(client_ip=self.client_ip(request), version=version).save()
            return self.json_resp('remo', __version__)

        latest, _ = VersionStore.latest_electron_app(platform)
        if not latest:
            raise Http404(f'Electron app for platform: {platform} - not found')

        return self.json_resp('electron-app', latest)

    @staticmethod
    def json_resp(app, version, msg=''):
        data = {
            'app': app,
            'version': version
        }
        if msg:
            data['msg'] = msg
        return JsonResponse(data)
