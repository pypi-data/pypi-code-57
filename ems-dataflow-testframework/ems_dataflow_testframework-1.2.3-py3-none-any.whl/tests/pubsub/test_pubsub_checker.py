from unittest.mock import Mock

import pytest
from google.api_core.exceptions import NotFound, GoogleAPICallError
from google.cloud.pubsub import PublisherClient, SubscriberClient

from testframework.exceptions.pubsub_checker_error import PubsubCheckerError
from testframework.pubsub.pubsub_checker import PubsubChecker


class TestPubsubChecker:

    def setup_method(self, method):
        self.__mock_publisher_client = Mock(PublisherClient)
        self.__mock_subscriber_client = Mock(SubscriberClient)
        self.__mock_publisher_client.topic_path.return_value = "projects/some_project/topics/some_topic"
        self.__mock_subscriber_client.subscription_path.side_effect = ["projects/some_project/subscriptions/some_subscription", "projects/some_project/subscriptions/some_other_subscription"]
        self.__checker = PubsubChecker("some_project", self.__mock_publisher_client, self.__mock_subscriber_client)

    def test_topic_exists_return_false_if_topic_not_exists(self):
        self.__mock_publisher_client.get_topic.side_effect = NotFound("Not Found")
        assert not self.__checker.topic_exists("some_topic")

    def test_topic_exists_return_true_if_topic_exists(self):
        self.__mock_publisher_client.get_topic.return_value = {}
        assert self.__checker.topic_exists("some_topic")

    def test_topic_exists_wraps_api_errors(self):
        self.__mock_publisher_client.get_topic.side_effect = GoogleAPICallError("Error message")
        with pytest.raises(PubsubCheckerError):
            self.__checker.topic_exists("some_topic")

    def test_subscriptions_exist_throws_error_if_topic_does_not_exist(self):
        self.__mock_publisher_client.list_topic_subscriptions.side_effect = NotFound("Not Found")
        with pytest.raises(PubsubCheckerError):
            self.__checker.subscriptions_exist("some_topic", ["some_subscription"])

    def test_subscriptions_exist_returns_false_if_a_subscription_does_not_exist(self):
        self.__mock_publisher_client.list_topic_subscriptions.return_value = ["projects/some_project/subscriptions/some_subscription"]
        result, missing_subscriptions = self.__checker.subscriptions_exist("some_topic", ["some_subscription", "some_other_subscription"])
        assert not result
        assert missing_subscriptions == ["projects/some_project/subscriptions/some_other_subscription"]

    def test_subscriptions_exist_returns_true_if_all_subscriptions_exist(self):
        self.__mock_publisher_client.list_topic_subscriptions.return_value = ["projects/some_project/subscriptions/some_subscription", "projects/some_project/subscriptions/some_other_subscription"]
        result, missing_subscriptions = self.__checker.subscriptions_exist("some_topic", ["some_subscription", "some_other_subscription"])
        assert result
        assert len(missing_subscriptions) == 0

    def test_topics_exist_return_false_if_a_topic_not_exists(self):
        return_topic = Mock()
        return_topic.name = "projects/some_project/topics/some_other_topic"
        self.__mock_publisher_client.list_topics.return_value = [return_topic]
        result, missing_topics = self.__checker.topics_exist(["some_topic"])
        assert not result
        assert missing_topics == ["projects/some_project/topics/some_topic"]
