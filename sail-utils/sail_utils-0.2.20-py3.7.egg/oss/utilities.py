# -*- coding: utf-8 -*-
"""
oss utilities module
"""

from io import BytesIO
from pathlib import Path
from typing import List

from lockfile import LockFile
import oss2
from sail_utils import LOGGER


class OSSUtility:
    """
    class for connect with aliyun oss
    """

    def __init__(self,
                 access_key_id: str,
                 access_key_secret: str,
                 bucket: str,
                 endpoint: str):
        self._bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret),
                                   endpoint,
                                   bucket)

    def put_binary(self, key: str, buffer: bytes):
        """
        put a binary file to aliyun oss
        :param key:
        :param buffer:
        :return:
        """
        with BytesIO(buffer) as writer:
            self._bucket.put_object(key, writer)
        LOGGER.info(f"saved file: <{key}>")

    def put_text(self, key: str, text: str):
        """
        put a plain text file to aliyun oss
        :param key:
        :param text:
        :return:
        """
        self._bucket.put_object(key, text)
        LOGGER.info(f"saved file: <{key}>")

    def get_object(self, key: str) -> bytes:
        """
        get file object from oss
        :param key:
        :return:
        """
        result = self._bucket.get_object(key)
        return b"".join(chunk for chunk in result)

    def list(self, prefix: str) -> List[str]:
        """
        list all the files under this folder
        :param prefix:
        :return:
        """
        is_truncated = True
        next_marker = ''
        while is_truncated:
            results = self._bucket.list_objects(prefix=prefix,
                                                marker=next_marker,
                                                max_keys=1000)
            is_truncated = results.is_truncated
            next_marker = results.next_marker
            for result in results.object_list:
                yield result.key

    def exists(self, key) -> bool:
        """
        check whether some key exists
        :param key:
        :return:
        """
        return self._bucket.object_exists(key)

    def download(self, key: str, file_name: str):
        """
        download a file from an existing oss2 bucket
        """
        file_name = Path(file_name)
        key = Path(key).as_posix()
        with LockFile(file_name.as_posix() + '.lock'):
            if not file_name.exists():
                LOGGER.info(f'downloading <{key}> '
                            f'from <{self._bucket.endpoint}/{self._bucket.bucket_name}> '
                            f'to <{file_name}>')
                try:
                    oss2.resumable_download(self._bucket, key, file_name.as_posix(),
                                            multiget_threshold=200 * 1024,
                                            part_size=100 * 1024)
                except oss2.exceptions.NotFound:
                    LOGGER.warning(f'<{key}> not found on the oss')
                    raise
            else:
                LOGGER.info(f'<{file_name}> already exists. Omit downloading')
