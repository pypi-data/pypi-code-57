import boto3

import botocore

from jeffy.encoding import Encoding
from jeffy.encoding.bytes import BytesEncoding
from jeffy.sdk import SdkBase


class S3(SdkBase):
    """S3 Client."""

    _resource = None

    def __init__(self, encoding: Encoding = BytesEncoding()):
        """
        Initialize S3 client.

        Parameters
        ----------
        encoding: jeffy.encoding.Encoding
        """
        super(S3, self).__init__(encoding)

    @classmethod
    def get_resource(self) -> botocore.client.BaseClient:
        """
        Get boto3 client for S3.

        Usage::
            >>> from jeffy.sdk.sns import S3
            >>> S3.get_resource().upload_file(...)
        """
        if S3._resource is None:
            S3._resource = boto3.client('s3')
        return S3._resource

    def upload_file(
        self,
        file_path: str,
        bucket_name: str,
        key: str,
        correlation_id: str = ''
    ) -> None:
        """
        Upload file to S3 bucket with correlationid.

        Usage::
            >>> from jeffy.sdk.s3 import S3
            >>> S3().upload_file(...)
        """
        if correlation_id == '':
            correlation_id = self.app.correlation_id
        self.get_resource().upload_file(
            Filename=file_path,
            Bucket=bucket_name,
            Key=key,
            ExtraArgs={
                'Metadata': {
                    self.app.correlation_attr_name: correlation_id
                }
            }
        )
