"""
    Personalize event manager module
"""
import json
import time
import boto3
from sdc_engine_helpers.personalize.manager import Manager


class EventManager(Manager):
    """
        Manage real-time events to AWS personalize for a given set of parameters
    """

    def track_event(self):
        """
            Track the personalise event from the event
            dictionary provided by lambda

            returns:
                results (dict): A dict for logging the event

        """
        client = self.get_client()

        event_type = self.parameters.get('eventType', 'listingView')

        dataset_kwargs = {'label': 'tracking'}

        dataset = self.query_helper.get_dataset(
            client_id=client.id,
            service_id=self.service.id,
            engine_slug=self.engine_slug,
            **dataset_kwargs
        )

        if dataset is None:
            raise Exception('ServerError: Could not determine tracking dataset for this client')

        tracking_id = dataset.get('identifier', None)
        if tracking_id is None:
            raise Exception('ServerError: Identifier is not populated in tracking dataset')

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
            'client': client.name,
            'context': self.parameters.get('context', None),
            'user_id': user_id,
            'item_id': item_id
        }
        print(results)

        return results
