from unittest import TestCase
from unittest.mock import Mock

import pytest
from google.api_core.exceptions import NotFound, GoogleAPICallError
from google.cloud.pubsub import PublisherClient, SubscriberClient
from tenacity import RetryError

from testframework.checkers.checker_message import CheckerMessage
from testframework.checkers.pubsub_message_receiver import PubsubMessageReceiver
from testframework.checkers.pubsub_topic_checker import PubsubTopicChecker


class TestPubsubTopicChecker(TestCase):

    def setup_method(self, method):
        self.mock_publisher_client = Mock(PublisherClient)
        self.mock_subscriber_client = Mock(SubscriberClient)
        self.mock_receiver = Mock(PubsubMessageReceiver)

    def test_init_creates_subscription(self):
        PubsubTopicChecker(self.mock_publisher_client, self.mock_subscriber_client, "some_project", "some_topic_name", self.mock_receiver)

        self.mock_subscriber_client.create_subscription.assert_called_once()

    def test_init_with_non_existent_topic_raises_error(self):
        self.mock_subscriber_client.create_subscription.side_effect = NotFound("Not found.")

        with pytest.raises(RetryError):
            PubsubTopicChecker(self.mock_publisher_client, self.mock_subscriber_client, "some_project", "invalid_topic_name", self.mock_receiver)

    def test_init_retries_subscription_creation_on_error_3_times(self):
        self.mock_subscriber_client.create_subscription.side_effect = GoogleAPICallError("Error")

        with pytest.raises(RetryError):
            PubsubTopicChecker(self.mock_publisher_client, self.mock_subscriber_client, "some_project", "some_topic_name", self.mock_receiver)

        assert len(self.mock_subscriber_client.create_subscription.mock_calls) == 3

    def test_close_calls_subscription_delete(self):
        checker = PubsubTopicChecker(self.mock_publisher_client, self.mock_subscriber_client, "some_project", "some_topic_name", self.mock_receiver)
        checker.close()

        self.mock_subscriber_client.delete_subscription.assert_called_once()

    def test_close_retries_on_error_three_times_if_cannot_delete_subscription(self):
        self.mock_subscriber_client.delete_subscription.side_effect = Exception

        with pytest.raises(Exception):
            checker = PubsubTopicChecker(self.mock_publisher_client, self.mock_subscriber_client, "some_project", "some_topic_name", self.mock_receiver)
            checker.close()

        assert len(self.mock_subscriber_client.delete_subscription.mock_calls) == 3

    def test_receive_if_no_message_received_returns_none(self):
        mock_message = Mock(CheckerMessage)

        self.mock_receiver.receive.return_value = []

        checker = PubsubTopicChecker(self.mock_publisher_client, self.mock_subscriber_client, "some_project", "some_topic_name", self.mock_receiver)
        message = checker.received(mock_message)

        assert message is None

    def test_receive_if_single_message_received_and_does_not_match_with_expected_returns_none(self):
        mock_message = Mock(CheckerMessage)
        mock_message.matches_message_dict.side_effect = [False, True]

        message_1 = "{\"some_json_key_1\":\"some_json_value_1\"}"
        message_2 = "{\"some_json_key_2\":\"some_json_value_2\"}"

        self.mock_receiver.receive.return_value = [message_1, message_2]

        checker = PubsubTopicChecker(self.mock_publisher_client, self.mock_subscriber_client, "some_project", "some_topic_name", self.mock_receiver)
        received_message = checker.received(mock_message)

        assert received_message["some_json_key_2"] == "some_json_value_2"
