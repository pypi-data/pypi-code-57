from typing import List

from google.api_core.exceptions import NotFound, GoogleAPICallError
from google.cloud.pubsub import PublisherClient, SubscriberClient

from testframework.exceptions.pubsub_checker_error import PubsubCheckerError


class PubsubChecker:

    def __init__(self, project_id, publisher_client: PublisherClient = None, subscriber_client: SubscriberClient = None):
        self.__project_id = project_id
        self.__publisher_client = publisher_client
        if self.__publisher_client is None:
            self.__publisher_client = PublisherClient()
        self.__subscriber_client = subscriber_client
        if self.__subscriber_client is None:
            self.__subscriber_client = SubscriberClient()

    def topic_exists(self, topic_name: str):
        topic_path = self.topic_path(topic_name)
        try:
            topic = self.__publisher_client.get_topic(topic_path)
            return topic is not None
        except NotFound:
            return False
        except Exception as e:
            raise PubsubCheckerError(e)

    def subscriptions_exist(self, topic_name: str, subscription_names: List[str], topic_project_id: str = None, subscription_project_id: str = None):
        topic_path = self.topic_path(topic_name, topic_project_id)
        subscription_paths = map(lambda x: self.subscription_path(x, subscription_project_id), subscription_names)
        try:
            actual_subscription_names = list(self.__publisher_client.list_topic_subscriptions(topic_path))
            return self._is_subset_of(subscription_paths, actual_subscription_names)
        except GoogleAPICallError as e:
            raise PubsubCheckerError(e)

    def topics_exist(self, topic_names: List[str]) -> (bool, List[str]):
        topic_paths = map(lambda x: self.topic_path(x), topic_names)
        try:
            actual_topic_names = map(lambda x: x.name, self.__publisher_client.list_topics(self.__project_id))
            return self._is_subset_of(topic_paths, actual_topic_names)
        except GoogleAPICallError as e:
            raise PubsubCheckerError(e)

    def _is_subset_of(self, subset, full_set):
        missing = []
        for element in subset:
            if element not in full_set:
                missing.append(element)
        return len(missing) == 0, missing

    def topic_path(self, topic_name: str, project_id: str = None):
        if project_id is None:
            project_id = self.__project_id
        return self.__publisher_client.topic_path(project_id, topic_name)

    def subscription_path(self, subscription_name, project_id):
        if project_id is None:
            project_id = self.__project_id
        return self.__subscriber_client.subscription_path(project_id, subscription_name)
