from google.api_core.exceptions import AlreadyExists, GoogleAPICallError
from google.cloud.pubsub import PublisherClient, SubscriberClient

from testframework.exceptions.pubsub_creator_error import PubsubCreatorError


class PubsubCreator:

    def __init__(self, project_id: str, publisher_client: PublisherClient = None, subscriber_client: SubscriberClient = None):
        self.__project_id = project_id
        self.__publisher_client = publisher_client
        if self.__publisher_client is None:
            self.__publisher_client = PublisherClient()
        self.__subscriber_client = subscriber_client
        if self.__subscriber_client is None:
            self.__subscriber_client = SubscriberClient()

    def project(self):
        return self.__project_id

    def create_topic(self, topic_name: str):
        topic_path = self.topic_path(topic_name)
        try:
            self.__publisher_client.create_topic(topic_path)
        except AlreadyExists:
            pass
        except GoogleAPICallError as e:
            raise PubsubCreatorError(e)

    def create_subscription(self, topic_name: str, subscription_path: str):
        topic_path = self.topic_path(topic_name)
        try:
            self.__subscriber_client.create_subscription(subscription_path, topic_path, ack_deadline_seconds=60)
        except AlreadyExists:
            pass
        except GoogleAPICallError as e:
            raise PubsubCreatorError(e)

    def topic_path(self, topic_name: str):
        return self.__publisher_client.topic_path(self.__project_id, topic_name)

    def subscription_path(self, subscription_name: str):
        return self.__subscriber_client.subscription_path(self.__project_id, subscription_name)
