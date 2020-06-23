from typing import Any, Dict

import boto3

import botocore

from jeffy.encoding import Encoding
from jeffy.encoding.json import JsonEncoding
from jeffy.sdk import SdkBase


class Sqs(SdkBase):
    """SQS Client."""

    _resource = None

    def __init__(self, encoding: Encoding = JsonEncoding()):
        """
        Initialize SQS client.

        Parameters
        ----------
        encoding: jeffy.encoding.Encoding
        """
        super(Sqs, self).__init__(encoding)

    @classmethod
    def get_resource(self) -> botocore.client.BaseClient:
        """
        Get boto3 client for SQS.

        Usage::
            >>> from jeffy.sdk.sqs import Sqs
            >>> Sqs.get_resource().send_message(...)
        """
        if Sqs._resource is None:
            Sqs._resource = boto3.client('sqs')
        return Sqs._resource

    def send_message(
        self,
        message: Any,
        queue_url: str,
        correlation_id: str = ''
    ) -> Dict:
        """
        Send message to SQS Queue with correlationid.

        Usage::
            >>> from jeffy.sdk.sqs import Sqs
            >>> Sqs().send_message(...)
        """
        if correlation_id == '':
            correlation_id = self.app.correlation_id
        return self.get_resource().send_message(
            QueueUrl=queue_url,
            MessageBody=self.convert_to_encoded_data(message, correlation_id).decode('utf-8')
        )
