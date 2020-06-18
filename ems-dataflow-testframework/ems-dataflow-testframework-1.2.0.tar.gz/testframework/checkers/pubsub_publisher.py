import logging

from google.api_core.exceptions import NotFound
from google.cloud.pubsub import PublisherClient
from pytest import fixture
from tenacity import wait_fixed, retry, stop_after_attempt

from testframework.checkers.checker_message import CheckerMessage


class PubsubPublisher:
    def __init__(self, pubsub_client: PublisherClient, project_id: str, input_topic_name: str):
        self.__publisher = pubsub_client
        self.__topic_path = self.__publisher.topic_path(project_id, input_topic_name)
        try:
            self.__publisher.get_topic(self.__topic_path)
        except NotFound as e:
            raise AssertionError(e)

    def publish_message(self, msg: CheckerMessage) -> None:
        self.__publish_msg(msg.get_message_as_json())
        pass

    def publish_string_message(self, msg: str) -> None:
        self.__publish_msg(msg)
        pass

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
    def __publish_msg(self, msg: str) -> None:
        logging.debug("Publishing to topic: {}, message {}".format(self.__topic_path, msg))
        self.__publisher.publish(self.__topic_path, msg.encode("utf-8")).result()


@fixture(scope="module")
def pubsub_publisher(request):
    pubsub_client, project_id, input_topic_name = request.param
    checker = PubsubPublisher(pubsub_client, project_id, input_topic_name)

    return checker
