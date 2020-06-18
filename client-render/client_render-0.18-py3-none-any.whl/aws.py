import os
from pathlib import PurePath

import boto3
from botocore.exceptions import ClientError


class S3Path:
    subdir = 'artifacts'

    def __init__(self):
        self.base = PurePath(os.environ["KEY_PREFIX"])

    def _create_path(self, prefix, path):
        return self.base / self.subdir / prefix / str(path)

    def complex_path(self, path):
        return self._create_path("complex", path)

    def builder_path(self, path):
        return self._create_path("builder", path)

    def task_path(self, path):
        return self._create_path("tasks", path)


class S3:
    DEFAULT_CONTENT_TYPE = 'application/binary'
    EXT_TO_CONTENT_TYPE = {
        '.jpeg': 'image/jpeg',
        '.jpg': 'image/jpeg',
        '.svg': 'image/svg+xml',
        '.png': 'image/png',
        '.txt': 'text/plain'
    }

    def __init__(self, bucket, *args, **kwargs):
        self.bucket = bucket
        self.client = boto3.client('s3', *args, **kwargs)

    def upload(self, path: PurePath, content):
        key = str(path)
        if not self.is_exists(key):
            self.client.put_object(
                Bucket=self.bucket,
                Key=key,
                Body=content,
                ContentType=self.EXT_TO_CONTENT_TYPE.get(
                    path.suffix, self.DEFAULT_CONTENT_TYPE),
                ACL="public-read"
            )
        return key

    def is_exists(self, key):
        try:
            self.client.head_object(
                Bucket=self.bucket,
                Key=key
            )
        except ClientError as e:
            if e.response['Error']['Code'] == "404":
                return False
            raise
        return True
