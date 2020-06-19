import mimetypes
import os
import stat
import urllib.parse
from pathlib import PureWindowsPath

from django.conf import settings
from django.http import Http404, HttpResponse, FileResponse
from django.utils.http import http_date
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from remo_app.remo.models import Image
from remo_app.remo.utils.utils import is_windows


def serve_file(path):
    stats = os.stat(path)

    content_type, encoding = mimetypes.guess_type(path)
    content_type = content_type or 'application/octet-stream'
    response = FileResponse(open(path, 'rb'), content_type=content_type)
    response["Last-Modified"] = http_date(stats[stat.ST_MTIME])
    response["Content-Length"] = stats[stat.ST_SIZE]
    if encoding:
        response["Content-Encoding"] = encoding

    return response


class LocalFiles(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        fullpath = request.get_full_path()
        fullpath = urllib.parse.unquote(fullpath)
        real_path = fullpath[len(settings.LOCAL_FILES):]

        if is_windows():
            real_path = real_path.lstrip('/')
            real_path = str(PureWindowsPath(real_path))

        img = Image.objects.filter(local_image=real_path).first()
        if not img:
            return Http404()

        return serve_file(real_path)
