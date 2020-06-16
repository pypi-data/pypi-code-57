import json
import logging
import requests
import boto3
from flask import request
from .. import config
from ..constants import responses as rsp
from ..config import NOTIFICATION, SUSCRIPTION
from ..contract import BusNotificationsContract
from ..contract import DataListener


__all__ = (
    'BusNotifications',
)


class BusNotifications(BusNotificationsContract):

    def listener(self) -> DataListener:
        """Endpoint of Suscription and Reception of Notifications of AWS sns.
        Implementation of `listener` of AWS notifications bus
        for flask.

        Returns:
            ..contract.DataListener:
        """
        try:
            data = json.loads(request.data)
        except Exception as e:
            logging.error(str(e))
            return DataListener(
                response=(rsp.AWS_BAD_REQUEST, 400)
            )
        message_type = request.headers.get('X-Amz-Sns-Message-Type')
        topic_arn = request.headers.get('X-Amz-Sns-Topic-Arn')
        if message_type == 'Notification':
            # Receive notification from AWS channel and call decorated function
            result = DataListener(
                message_type=NOTIFICATION,
                message=data['Message'],
                topic_arn=topic_arn,
                response=rsp.AWS_OK,
            )
        elif (message_type == 'SubscriptionConfirmation'
                and 'SubscribeURL' in data):
            # Confirm suscription of AWS channel
            requests.get(data['SubscribeURL'])
            result = DataListener(
                message_type=SUSCRIPTION,
                topic_arn=topic_arn,
                response=rsp.AWS_OK
            )
        else:
            result = DataListener(
                response=(rsp.AWS_BAD_REQUEST, 400)
            )
        return result

    def publisher(
        self,
        topic_arn: str = None,
        message: str = None
    ) -> dict:
        """Method to publish in sns of AWS.
        Implementation of `publisher` to AWS notifications bus
        for Flask.

        Args:
            topic_arn (str)
            message (str)

        Returns:
            dict: Response returned by client sns
        """
        client = boto3.client('sns', region_name=config.REGION)
        # Publish a simple message to the specified SNS topic
        response = client.publish(
            TopicArn=topic_arn,
            Message=message
        )

        return response
