from unittest.mock import Mock

import pytest
from google.api_core.exceptions import AlreadyExists, GoogleAPICallError, NotFound
from google.cloud.pubsub import PublisherClient, SubscriberClient

from testframework.exceptions.pubsub_creator_error import PubsubCreatorError
from testframework.pubsub.pubsub_creator import PubsubCreator


class TestPubsubCreator:

    def setup_method(self, method):
        self.__mock_publisher_client = Mock(PublisherClient)
        self.__mock_subscriber_client = Mock(SubscriberClient)
        self.__mock_publisher_client.topic_path.return_value = "projects/some_project/topics/some_topic"
        self.__mock_subscriber_client.subscription_path.side_effect = ["projects/some_project/subscriptions/some_subscription", "projects/some_project/subscriptions/some_other_subscription"]
        self.__creator = PubsubCreator("some_project", self.__mock_publisher_client, self.__mock_subscriber_client)

    def test_create_topic_if_needed_creates_a_topic(self):
        self.__mock_publisher_client.create_topic.return_value = {}

        self.__creator.create_topic("some_topic")
        self.__mock_publisher_client.create_topic.assert_called_with("projects/some_project/topics/some_topic")

    def test_create_topic_consumes_error_if_topic_already_exists(self):
        self.__mock_publisher_client.create_topic.side_effect = AlreadyExists("Already exists.")

        self.__creator.create_topic("some_topic")
        self.__mock_publisher_client.create_topic.assert_called_with("projects/some_project/topics/some_topic")

    def test_create_topic_wrapps_error(self):
        self.__mock_publisher_client.create_topic.side_effect = GoogleAPICallError("Something went wrong.")

        with pytest.raises(PubsubCreatorError):
            self.__creator.create_topic("some_topic")

    def test_create_subscription_raises_error_if_topic_is_not_found(self):
        self.__mock_subscriber_client.create_subscription.side_effect = NotFound("Topic not found.")

        with pytest.raises(PubsubCreatorError):
            self.__creator.create_subscription("some_topic", "some_subscription")

    def test_create_subscription_creates_a_subscription(self):
        self.__creator.create_subscription("some_topic", "projects/some_project/subscriptions/some_subscription")
        self.__mock_subscriber_client.create_subscription.assert_called_with("projects/some_project/subscriptions/some_subscription",
                                                                             "projects/some_project/topics/some_topic",
                                                                             ack_deadline_seconds=60)

    def test_create_subscription_consumes_error_if_subscription_already_exists(self):
        self.__mock_subscriber_client.create_subscription.side_effect = AlreadyExists("Already exists.")

        self.__creator.create_subscription("some_topic", "projects/some_project/subscriptions/some_subscription")
        self.__mock_subscriber_client.create_subscription.assert_called_with("projects/some_project/subscriptions/some_subscription",
                                                                             "projects/some_project/topics/some_topic",
                                                                             ack_deadline_seconds=60)
