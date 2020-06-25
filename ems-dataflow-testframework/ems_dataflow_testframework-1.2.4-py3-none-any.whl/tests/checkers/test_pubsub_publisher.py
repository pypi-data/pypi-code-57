from concurrent.futures import Future
from unittest.mock import Mock, call, patch

import pytest
from google.api_core.exceptions import NotFound, GoogleAPICallError
from google.cloud.pubsub import PublisherClient

from testframework.checkers.checker_message import CheckerMessage
from testframework.checkers.pubsub_publisher import PubsubPublisher


class TestPubsubPublisher:

    def setup(self):
        self.mock_publisher_client = Mock(PublisherClient)
        self.mock_message = Mock(CheckerMessage)
        self.message_in_json = '{"some_json":"some_value"}'
        self.mock_message.get_message_as_json.return_value = self.message_in_json
        self.mock_publisher_client.topic_path.return_value = "projects/some_project/topics/valid_topic_name"

    def test_init_calls_create_topic_on_publischer_client(self):
        PubsubPublisher(self.mock_publisher_client, "some_project", "valid_topic_name")

        self.mock_publisher_client.get_topic.assert_called_once()

    def test_init_withNon_existing_topic_raisesAssertionError(self):
        self.mock_publisher_client.get_topic.side_effect = NotFound("Not Found.")
        with pytest.raises(AssertionError):
            PubsubPublisher(self.mock_publisher_client, "some_project", "invalid_topic_name")

    def test_publish_checkerMessagePublishedIntoTopic(self):
        publisher = PubsubPublisher(self.mock_publisher_client, "some_project", "valid_topic_name")
        publisher.publish_message(self.mock_message)

        self.mock_message.get_message_as_json.assert_called_once()
        self.mock_publisher_client.publish.assert_called_once_with("projects/some_project/topics/valid_topic_name", self.message_in_json.encode("utf-8"))

    def test_publish_stringMessagePublishedIntoTopic(self):
        TEST_STRING_MESSAGE = "test string message"

        publisher = PubsubPublisher(self.mock_publisher_client, "some_project", "valid_topic_name")
        publisher.publish_string_message(TEST_STRING_MESSAGE)

        self.mock_publisher_client.publish.assert_called_once_with("projects/some_project/topics/valid_topic_name", TEST_STRING_MESSAGE.encode("utf-8"))

    @patch('time.sleep', return_value=None)
    def test_publish_retriesOnErrorThreeTimes(self, patched_time_sleep):
        mock_future = Mock(Future)
        mock_future.result.side_effect = GoogleAPICallError("Some error")
        self.mock_publisher_client.publish.return_value = mock_future
        publisher = PubsubPublisher(self.mock_publisher_client, "some_project", "valid_topic_name")

        with pytest.raises(Exception):
            publisher.publish_message(self.mock_message)

        calls = [call("projects/some_project/topics/valid_topic_name", self.message_in_json.encode("utf-8"))]*3
        self.mock_publisher_client.publish.assert_has_calls(calls, any_order=True)
