import random

import pytest
from unittest.mock import Mock, call

import time

from google.cloud.pubsub import SubscriberClient
from google.cloud.pubsub_v1.proto.pubsub_pb2 import PullResponse

from testframework.checkers.pubsub_message_receiver import PubsubMessageReceiver


class TestPubsubMessageReceiver:
    def setup_method(self, setup_method):
        self.time_mock = Mock(time)
        self.time_mock.time.side_effect = [0, 10, 31]
        self.mock_subscriber_client = Mock(SubscriberClient)
        self.subscription_path = "projects/some_project/subscriptions/some_subscription"
        self.mock_subscriber_client.pull.return_value = Mock(PullResponse)

    def test_receive_subscriptionIsEmpty_returnsEmptyMessagesList(self):
        self.__set_pull_return_value([])

        receiver = PubsubMessageReceiver(self.time_mock, self.mock_subscriber_client)
        message_generator = receiver.receive(self.subscription_path)
        messages = list(message_generator)

        self.mock_subscriber_client.acknowledge.assert_not_called()
        assert [] == messages

    def test_receive_subscriptionContainsOneMessage_acknowledgesAndReturnsMessageList(self):
        ack_id = "some_ack_id"
        message_text = "some_message_bytes"
        message_bytes = bytes(message_text, "utf-8")
        message_data = Mock()
        message_data.data = message_bytes
        pulled = [(Mock(ack_id=ack_id, message=message_data))]
        self.__set_pull_return_value(pulled)

        receiver = PubsubMessageReceiver(self.time_mock, self.mock_subscriber_client)
        message_generator = receiver.receive(self.subscription_path)
        messages = [next(message_generator)]

        self.mock_subscriber_client.pull.assert_called_once_with(self.subscription_path, max_messages=1000, return_immediately=True)
        self.mock_subscriber_client.acknowledge.assert_called_once_with(self.subscription_path, [ack_id])

        self.time_mock.sleep.assert_not_called()

        assert [message_text] == messages

    def __set_pull_return_value(self, pulled):
        self.mock_subscriber_client.pull.return_value = Mock(received_messages=pulled)

    def test_receive_subscriptionContainsTwoMessages_returnsMessagesList(self):
        ack_id_1 = "some_ack_id_1"
        ack_id_2 = "some_ack_id_2"

        message_text_1 = "some_message_bytes_1"
        message_bytes_1 = bytes(message_text_1, "utf-8")
        message_data_1 = Mock()
        message_data_1.data = message_bytes_1

        message_text_2 = "some_message_bytes_2"
        message_bytes_2 = bytes(message_text_2, "utf-8")
        message_data_2 = Mock()
        message_data_2.data = message_bytes_2

        pulled = [
            Mock(ack_id=ack_id_1, message=message_data_1),
            Mock(ack_id=ack_id_2, message=message_data_2)
        ]
        self.__set_pull_return_value(pulled)

        receiver = PubsubMessageReceiver(self.time_mock, self.mock_subscriber_client)
        message_generator = receiver.receive(self.subscription_path)
        messages = list(message_generator)

        assert [message_text_1, message_text_2] == messages

    def test_receive_pull_retries_on_error_three_times(self):
        self.mock_subscriber_client.pull.side_effect = Exception

        self.time_mock.side_effect = []
        receiver = PubsubMessageReceiver(self.time_mock, self.mock_subscriber_client)

        with pytest.raises(Exception):
            message_generator = receiver.receive(self.subscription_path)
            next(message_generator)

        calls = [call(self.subscription_path, max_messages=1000, return_immediately=True)] * 3
        self.mock_subscriber_client.pull.assert_has_calls(calls)

    def test_receive_pulledCalledWhileTimeoutIsNotExceeded_returnsMessagesList(self):
        batch_size = 1

        message_text_1 = "some_message_bytes_1"
        message_bytes_1 = bytes(message_text_1, "utf-8")
        message_data_1 = Mock()
        message_data_1.data = message_bytes_1

        pulled = [Mock(ack_id="some_ack_id_1", message=message_data_1)]

        self.__set_pull_return_value(pulled)

        self.time_mock.time.side_effect = [0, 10, 15, 31]
        sleep_seconds = random.randint(0, 100)
        receiver = PubsubMessageReceiver(self.time_mock, self.mock_subscriber_client, batch_size)
        message_generator = receiver.receive(self.subscription_path, sleep_seconds=sleep_seconds)

        messages = list(message_generator)

        calls = [call(self.subscription_path, max_messages=batch_size, return_immediately=True)] * 2
        self.mock_subscriber_client.pull.assert_has_calls(calls)
        calls_for_sleep = [call(sleep_seconds)] * 2
        self.time_mock.sleep.assert_has_calls(calls_for_sleep)
        assert [message_text_1, message_text_1] == messages
