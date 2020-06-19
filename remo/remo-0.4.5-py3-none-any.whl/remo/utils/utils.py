import os
import shutil
from io import BytesIO
import logging
import requests
from django.conf import settings
from rest_framework.response import Response

from remo_app.remo.api.constants import default_status

logger = logging.getLogger('remo_app')


def make_dir(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
            logger.debug(f'mkdir -p {path}')
        except Exception:
            pass


def remove_dir(dir_path):
    logger.debug(f'rm -rf {dir_path}')
    shutil.rmtree(dir_path)


def human_size(num, suffix='b'):
    num = float(num)
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            if not unit:
                return "%.0f %s" % (num, suffix)
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0

    return "%.1f %s%s" % (num, 'Y', suffix)


def disk_free_space(path):
    total, used, free = shutil.disk_usage(path)
    return free


def file_size(path):
    return os.path.getsize(path)


def is_system_file(path):
    filename = os.path.basename(path)
    return filename.startswith('.')


def is_tool_exists(tool):
    return bool(shutil.which(tool))


def get_image_content(path_to_image, image_url=None):
    if settings.STORAGE == 'local':
        # images in media folder
        with open('{}/{}'.format(settings.MEDIA_ROOT, path_to_image), 'rb') as f:
            image_content = f.read()

    elif settings.STORAGE == 'aws':
        response = requests.get(image_url)
        if response.status_code != 200:
            logger.error('image does not exist {} {}'.format(response.status_code, image_url))
            return Response({'error': True, 'annotation_info': [], 'status': default_status.name})
        image_content = BytesIO(response.content).getvalue()

    return image_content


def is_windows():
    return os.name == 'nt'
