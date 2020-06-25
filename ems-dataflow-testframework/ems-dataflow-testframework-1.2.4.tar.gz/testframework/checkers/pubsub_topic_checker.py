import json
import logging
import uuid

from google.api_core.exceptions import GoogleAPICallError
from google.cloud.pubsub import PublisherClient, SubscriberClient
from tenacity import retry, stop_after_attempt, wait_fixed

from testframework.checkers.pubsub_message import PubsubMessage
from testframework.checkers.pubsub_message_receiver import PubsubMessageReceiver
from testframework.checkers.pubsub_topic_matchers import AbstractPubsubMessageMatcher
from testframework.exceptions.pubsub_creator_error import PubsubCreatorError


class PubsubTopicChecker:

    def __init__(self, publisher_client: PublisherClient, subscriber_client: SubscriberClient, project_name: str, topic_name: str, receiver: PubsubMessageReceiver):
        self.__publisher = publisher_client
        self.__subscriber = subscriber_client
        self.__project_id = project_name
        self.__topic_path = self.__subscriber.topic_path(self.__project_id, topic_name)
        self.__receiver = receiver
        self.__subscription_name = "{}-{}".format(self.__class__.__name__.lower(), uuid.uuid1())

        self.__initialize_output_subscription()

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
    def close(self):
        self.__subscriber.delete_subscription(self.__subscription_path())

    def received_matching(self, matcher: AbstractPubsubMessageMatcher, timeout_seconds=90):
        json_messages = self.__receiver.receive(self.__subscription_path(), timeout_seconds)

        for json_message in json_messages:
            if matcher.matches(json.loads(json_message)):
                logging.debug("Pulled matching msg: {}".format(json_message))

                return PubsubMessage(json_message)

            logging.debug("Pulled not matching msg: {}".format(json_message))

        logging.debug("Couldn't find match for mathcer: {}".format(matcher))

        return None

    def received(self, message, timeout_seconds=90):
        json_messages = self.__receiver.receive(self.__subscription_path(), timeout_seconds)

        for json_message in json_messages:
            if message.matches_message_dict(json.loads(json_message)):
                logging.info("Pulled matching msg: {}".format(json_message))

                return PubsubMessage(json_message)

            logging.info("Pulled not matching msg: {}".format(json_message))

        logging.info("Couldn't find match for: {}".format(message.get_message_as_json()))

        return None

    def __initialize_output_subscription(self, ):
        try:
            self.__create_subscription()
        except GoogleAPICallError as e:
            raise PubsubCreatorError(e)

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
    def __create_subscription(self):
        self.__subscriber.create_subscription(self.__subscription_path(), self.__topic_path, ack_deadline_seconds=60)

    def __subscription_path(self):
        return self.__subscriber.subscription_path(self.__project_id, self.__subscription_name)
