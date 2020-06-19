import logging

from django.conf import settings
from django.http import Http404
from django.views.static import serve
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from remo_app import __version__
from remo_app.remo.models import Download
from remo_app.remo.stores.version_store import Version

logger = logging.getLogger('remo_app')


class DownloadFiles(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, path):
        platform = request.query_params.get('platform')
        if path == 'latest':
            if platform:
                return self.serve_electron_app(request, platform)

            return self.serve_pip_wheel(request)

        raise Http404('{} not found'.format(path))

    def serve_electron_app(self, request, platform):
        _, file_name = Version.latest_electron_app(platform)
        if not file_name:
            raise Http404('Electron app not found')
        return self.serve_file(request, file_name)

    def serve_pip_wheel(self, request):
        file_name = 'remo-{}-py3-none-any.whl'.format(self.shorten_version(__version__).replace('-', '_'))
        return self.serve_file(request, file_name)

    def serve_file(self, request, file_name):
        ip = self.client_ip(request)
        logger.info('Client: {}, downloads {}'.format(ip, file_name))

        response = serve(request, file_name, settings.DOWNLOAD_URL)
        response['Content-Disposition'] = 'filename="{}"'.format(file_name)

        # save statistics
        Download(client_ip=ip, file_name=file_name).save()

        return response

    @staticmethod
    def client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]

        return request.META.get('REMOTE_ADDR', '')

    @staticmethod
    def shorten_version(version: str):
        tokens = version.split('-')
        if len(tokens) == 1:
            return tokens[0]
        return '{}.{}'.format(tokens[0], tokens[1])


