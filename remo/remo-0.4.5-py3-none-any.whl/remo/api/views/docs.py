import os
from pathlib import PureWindowsPath

from django.conf import settings
from remo_app.remo.api.views.local_files import serve_file
from remo_app.remo.utils.utils import is_windows


def serve_docs(request, path):
    path = os.path.join(settings.DOCS_DIR, path)

    if is_windows():
        path = str(PureWindowsPath(path))

    if os.path.isdir(path):
        path = os.path.join(path, 'index.html')

    return serve_file(path)

