from typing import Any, Dict

import boto3

import botocore

from jeffy.encoding import Encoding
from jeffy.encoding.json import JsonEncoding
from jeffy.sdk import SdkBase


class Kinesis(SdkBase):
    """Kinesis Client."""

    _resource = None

    def __init__(self, encoding: Encoding = JsonEncoding()):
        """
        Initialize Kinesis client.

        Parameters
        ----------
        encoding: jeffy.encoding.Encoding
        """
        super(Kinesis, self).__init__(encoding)

    @classmethod
    def get_resource(self) -> botocore.client.BaseClient:
        """
        Get boto3 client for Kinesis.

        Usage::
            >>> from jeffy.sdk.kinesis import Kinesis
            >>> Kinesis.get_resource().put_record(...)
        """
        if Kinesis._resource is None:
            Kinesis._resource = boto3.client('kinesis')
        return Kinesis._resource

    def put_record(
        self,
        stream_name: str,
        data: Any,
        partition_key: str,
        correlation_id: str = ''
    ) -> Dict:
        """
        Put recourd to Kinesis Stream with correlation_id.

        Usage::
            >>> from jeffy.sdk.kinesis import Kinesis
            >>> Kinesis().put_record(...)
        """
        return self.get_resource().put_record(
            StreamName=stream_name,
            Data=self.convert_to_encoded_data(data, correlation_id),
            PartitionKey=partition_key,
        )
