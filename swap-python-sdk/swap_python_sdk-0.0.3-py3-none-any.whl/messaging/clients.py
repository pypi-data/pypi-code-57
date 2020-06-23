import requests
from google.cloud import pubsub_v1
from swap.common.config import Settings
from urllib.parse import urljoin


class MessagePublisherClient:
    def __init__(self, config, publisher=pubsub_v1.PublisherClient()):
        self.project = config.project
        self.topic = config.topic
        self.publisher = publisher
        self.topic_path = f'projects/{self.project}/topics/{self.topic}'

    def publish(self, message, message_type):
        self.publisher.publish(self.topic_path, message, message_type=message_type)


class MessageSubscriberClient:
    def __init__(
        self,
        project,
        topic,
        subscription,
        subscriber=pubsub_v1.SubscriberClient()
    ):
        self.project = project
        self.topic = topic
        self.subscription = subscription
        self.subscriber = subscriber

        self.topic_path = f'projects/{project}/topics/{topic}'
        self.subscription_path = f'projects/{project}/subscriptions/{subscription}'

    def subscribe(self, callback):
        return self.subscriber.subscribe(self.subscription_path, callback)


class DASClient:
    def __init__(self):
        self.base_url = Settings.DAS_URL

    def url(self, path):
        return urljoin(self.base_url, path)

    def get(self, path, params):
        joined_url = self.url(path)
        response = requests.get(joined_url, params=params)

        return response.text

    def redeem_token(self, token):
        params = {'dataToken': token, 'connectionDetails': 'True'}
        return self.get(path='/data', params=params)
