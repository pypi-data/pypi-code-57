"""
The Wofs class supports uploading and downloading files from write-once file systems such as
Amazon S3, Google Storage, or local files.

Filenames that begin with "s3://<bucket>/..." are on Amazon S3.
Filenames that begin with "gs://<bucket>/..." are on Google Storage.
Local files can use any name not containing "://".

A Wofs instance stores credentials use to read or write the write-once file systems via the
upload() and download() methods.
"""
import os
import shutil

import boto3
# import google.cloud.storage

# from bytegain.zap.utils import gcs
from typing import Optional

class Wofs(object):

    _KNOWN_FS = ('gs', 's3')

    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None, aws_profile_name=None,
                 gcs_project=None):
        # type: (Optional[str], Optional[str], Optional[str], Optional[str]) -> Wofs
        """
        :param aws_access_key_id: Used for access to S3
        :param aws_secret_access_key: Used for access to S3
        :param aws_profile_name: Used for access to S3
        :param gcs_project: GCS project name to use to create client
        """
        self._aws_access_key_id = aws_access_key_id
        self._aws_secret_access_key = aws_secret_access_key
        self._aws_profile_name = aws_profile_name
        self._gcs_project = gcs_project
        self._boto_session = None
        self._gcs_client = None

    def download(self, src_path, dst_local_path):
        # type: (str, str) -> None
        """
        Copies the file at src_path to dst_local_path
        :param src_path: A file name to be copied to dst_local_path
        :param dst_local_path: A local file name to be written
        :return:
        """
        fs, bucket, key = Wofs._get_fs_bucket_key(src_path)
        if fs == 'gs':
            gcs.download_to_local_file(src_path, local_file=dst_local_path, client=self._get_gcs_client())
        elif fs == 's3':
            session = self._get_boto_session()
            s3 = session.client('s3')
            with open(dst_local_path, "wb") as f:
                response = s3.get_object(Bucket=bucket, Key=key)
                body = response['Body']
                data = body.read()
                f.write(data)
        elif fs == 'local':
            shutil.copyfile(src_path, dst_local_path)
        else:
            raise Exception("Invalid fs '%s' returned by _get_fs_bucket_key()" % fs)

    def upload(self, src_local_path, dst_path):
        # type: (str, str) -> None
        """
        Copies the file at src_local_path to dst_path.
        :param src_local_path: A valid local file name to be copied to dst_path
        :param dst_path: A file name to be written
        :return:
        """
        fs, bucket, key = Wofs._get_fs_bucket_key(dst_path)
        if fs == 'gs':
            if os.path.basename(dst_path) != os.path.basename(src_local_path):
                raise RuntimeError('Wofs.upload() to a gs:// target requires identical basename of src and dst')
            gcs.upload_local_files(src_local_path, os.path.dirname(dst_path), client=self._get_gcs_client())
        elif fs == 's3':
            session = self._get_boto_session()
            s3 = session.client('s3')
            with open(src_local_path, "rb") as f:
                s3.put_object(Bucket=bucket, Key=key, Body=f)
        elif fs == 'local':
            dirname = os.path.dirname(key)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            shutil.copy(src_local_path, key )
        else:
            raise Exception("Invalid fs '%s' returned by _get_fs_bucket_key" % fs)

    def _get_gcs_client(self):
        if not self._gcs_client:
            self._gcs_client = google.cloud.storage.Client() \
                if self._gcs_project is None else google.cloud.storage.Client(project=self._gcs_project)
        return self._gcs_client

    def _get_boto_session(self):
        # type: () -> boto3.Session
        if not self._boto_session:
            self._boto_session = boto3.Session(profile_name=self._aws_profile_name,
                                               aws_access_key_id=self._aws_access_key_id,
                                               aws_secret_access_key=self._aws_secret_access_key)
        return self._boto_session

    @staticmethod
    def _get_fs_bucket_key(path):
        # type: (str) -> (str, Union[str, None], str)
        """
        Decomposes path into the filesystem and bucket (if any)
        :param path: A file path name stored as a string.
        :return: file system, bucket, key
        """
        fs_rest = path.split('://', 1)
        if len(fs_rest) == 1:
            return 'local', None, path
        fs, rest = fs_rest
        if fs not in Wofs._KNOWN_FS:
            raise Exception('Unsupported file system: %s in path %s' % (fs, path))
        bucket_key = rest.split('/', 1)
        if len(bucket_key) == 1:
            raise Exception('Missing bucket in path %s' % path)
        bucket, key = bucket_key
        return fs, bucket, key


class GlobalWofs(object):
    _default_upload_wofs = Wofs()
    _default_download_wofs = Wofs()

    @staticmethod
    def upload(src_local_path, dst_path):
        # type: (str, str) -> None
        GlobalWofs._default_upload_wofs.upload(src_local_path, dst_path)

    @staticmethod
    def default_download(src_path, dst_local_path):
        # type: (str, str) -> None
        GlobalWofs._default_download_wofs.download(src_path, dst_local_path)
