# coding: utf-8
import uuid

import os, time
from django.conf import settings
import logging

from django.core.files.storage import FileSystemStorage

logger = logging.getLogger('system')


def upload_aliyun_oss(folder):

    import oss2
    AccessKeyId = settings.ALIYUN_OSS["AccessKeyId"]
    AccessKeySecret = settings.ALIYUN_OSS["AccessKeySecret"]
    Endpoint = settings.ALIYUN_OSS["Endpoint"]
    BucketName = settings.ALIYUN_OSS["BucketName"]

    if settings.UPLOAD_ALIYUN_OSS:
        auth = oss2.Auth(AccessKeyId, AccessKeySecret)
        bucket = oss2.Bucket(auth, Endpoint, BucketName)

        p = os.path.join(settings.MEDIA_ROOT, folder)
        aliyun_path = "{}/{}".format(settings.MEDIA_URL.replace("/", ""), folder).replace("\\", "/")
        try:
            with open(p, 'rb') as fileobj:
                result = bucket.put_object(aliyun_path, fileobj)
            if result.status == 200:
                return 'success', p
            else:
                return 'fail', ''
        except Exception as e:
            logger.error(e)
            return 'fail', ''


class ImageStorage(FileSystemStorage):
    from django.conf import settings

    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
        # 初始化
        super(ImageStorage, self).__init__(location, base_url)

    # 重写 _save方法
    def _save(self, name, content):
        import os, time, random
        # 文件扩展名
        ext = os.path.splitext(name)[1]
        # 文件目录
        d = os.path.dirname(name)
        # 定义文件名
        fn = str(uuid.uuid4())
        # 重写合成文件名
        name = os.path.join(d, fn + ext)
        # 调用父类方法
        fn = super(ImageStorage, self)._save(name, content)
        if hasattr(settings, 'ALIYUN_OSS'):
            upload_aliyun_oss(fn)
        return fn


def get_absolute_url(url):
    if not url:
        return url
    if url.startswith("http://") or url.startswith("https://"):
        return url

    if hasattr(settings,'UPLOAD_ALIYUN_OSS') and settings.UPLOAD_ALIYUN_OSS:
        return "{}{}".format(settings.IMGHOST, url)
    else:
        return "{}{}".format(settings.HOST, url)
