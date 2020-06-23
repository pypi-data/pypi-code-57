from typing import Any, Dict

import boto3

import botocore

from jeffy.encoding import Encoding
from jeffy.encoding.json import JsonEncoding
from jeffy.sdk import SdkBase


class Sns(SdkBase):
    """SNS Client."""

    _resource = None

    def __init__(self, encoding: Encoding = JsonEncoding()):
        """
        Initialize SNS client.

        Parameters
        ----------
        encoding: jeffy.encoding.Encoding
        """
        super(Sns, self).__init__(encoding)

    @classmethod
    def get_resource(self) -> botocore.client.BaseClient:
        """
        Get boto3 client for SNS.

        Usage::
            >>> from jeffy.sdk.sns import Sns
            >>> Sns.get_resource().publish(...)
        """
        if Sns._resource is None:
            Sns._resource = boto3.client('sns')
        return Sns._resource

    def publish(
        self,
        topic_arn: str,
        message: Any,
        subject: str,
        correlation_id: str = ''
    ) -> Dict:
        """
        Send message to SNS Topic with correlationid.

        Usage::
            >>> from jeffy.sdk.sns import Sns
            >>> Sns().publish(...)
        """
        if correlation_id == '':
            correlation_id = self.app.correlation_id
        return self.get_resource().publish(
            TopicArn=topic_arn,
            Message=self.convert_to_encoded_data(message, correlation_id).decode('utf-8'),
            Subject=subject)
