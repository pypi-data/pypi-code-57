import hashlib
import os
import shutil
import tempfile
from urllib.request import urlopen

from yqn_common.oss_func import oss_calculate_file_crc64


def download_url_to_file(url, dst, crc=None):
    file_size = None
    # We use a different API for python2 since urllib(2) doesn't recognize the CA
    # certificates in older Python
    u = urlopen(url)
    meta = u.info()
    if hasattr(meta, 'getheaders'):
        content_length = meta.getheaders("Content-Length")
    else:
        content_length = meta.get_all("Content-Length")
    if content_length is not None and len(content_length) > 0:
        file_size = int(content_length[0])

    dst = os.path.expanduser(dst)
    dst_dir = os.path.dirname(dst)
    f = tempfile.NamedTemporaryFile(delete=False, dir=dst_dir)

    try:
        while True:
            buffer = u.read(8192)
            if len(buffer) == 0:
                break
            f.write(buffer)
        f.close()
        if crc is not None:
            file_crc = oss_calculate_file_crc64(f.name)
            if str(file_crc) != crc:
                raise RuntimeError('invalid hash value (expected "{}", got "{}")'
                                   .format(crc, file_crc))
        shutil.move(f.name, dst)
    finally:
        f.close()
        if os.path.exists(f.name):
            os.remove(f.name)
