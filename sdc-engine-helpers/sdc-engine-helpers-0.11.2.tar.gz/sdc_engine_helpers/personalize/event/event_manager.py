"""
    Personalize event manager module
"""
import json
import time
from sdc_helpers.query_helper import QueryHelper
from sdc_helpers.redis_helper import RedisHelper
import boto3
import sdc_engine_helpers.helpers as helpers


class EventManager:
    """
        Manage real-time events to AWS personalize for a given set of parameters
    """
    service = None
    query_helper = None
    redis_helper = None
    parameters = None

    def __init__(self, **kwargs):
        self.query_helper = QueryHelper()
        self.redis_helper = RedisHelper()
        self.service = self.query_helper.get_service(slug='recommend')
        self.parameters = kwargs

    def __del__(self):
        del self.query_helper
        del self.redis_helper

    def get_client(self, api_key_id: str):
        """
            Determine the client with the supplied parameters

            returns:
                client (dict): The determined client

        """
        client = None

        client_id = self.parameters.get('client_id', None)
        if client_id is not None:
            client = self.query_helper.get_client(client_id=client_id)

        api_key_id = self.parameters.get('api_key_id', None)
        if api_key_id is not None:
            client = self.query_helper.get_client(api_key_id=api_key_id)

        if client is None:
            raise Exception('ClientError: Could not determine client for this request')

        return client

    def get_tracking_id(
            self,
            *,
            client_id: int
    ):
        """
            Get tracking for the given client and service

            args:
                client_id (int): The client id

            returns:
                tracking_id (string): The determined tracking id

        """
        tracking_id = None
        subscription_properties = self.query_helper.get_subscription_properties(
            client_id=client_id,
            service_id=self.service['id']
        )

        if subscription_properties:
            engine = helpers.get_engine(
                properties=subscription_properties,
                slug='personalize'
            )

            if engine is not None:
                dataset = helpers.get_dataset(
                    engine=engine,
                    label='tracking'
                )

                tracking_id = dataset.get('identifier', None)

        if not tracking_id:
            raise Exception(
                'ServerError: Could not determine tracking_id for this client'
            )

        return tracking_id

    def track_event(self):
        """
            Track the personalise event from the event
            dictionary provided by lambda

            returns:
                results (dict): A dict for logging the event

        """
        client = self.get_client(
            api_key_id=self.parameters.get('api_key_id')
        )

        event_type = self.parameters.get('eventType', 'listingView')

        tracking_id = self.get_tracking_id(
            client_id=client['id']
        )

        item_id = self.parameters.get('itemId')
        user_id = self.parameters.get('userId')
        timestamp = self.parameters.get('timestamp', int(time.time()))

        try:
            personalize_events = boto3.client('personalize-events')

            personalize_events.put_events(
                trackingId=tracking_id,
                userId=user_id,
                sessionId=user_id,
                eventList=[
                    {
                        'sentAt': timestamp,
                        'eventType': event_type,
                        'properties': json.dumps(
                            {
                                'itemId': item_id,
                            }
                        )
                    }
                ]
            )
        except Exception as ex:
            raise Exception(
                'ServerError: {exception}'.format(exception=str(ex))
            )

        print('Successful put event')

        results = {
            'client': client['name'],
            'context': self.parameters.get('context', None),
            'user_id': user_id,
            'item_id': item_id
        }
        print(results)

        return results
