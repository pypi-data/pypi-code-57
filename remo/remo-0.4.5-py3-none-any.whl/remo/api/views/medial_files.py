import os

from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from remo_app.remo.api.views.local_files import serve_file


class MediaFiles(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        fullpath = request.get_full_path()
        real_path = os.path.join(settings.MEDIA_ROOT, fullpath[len(settings.MEDIA_URL):])
        return serve_file(real_path)
