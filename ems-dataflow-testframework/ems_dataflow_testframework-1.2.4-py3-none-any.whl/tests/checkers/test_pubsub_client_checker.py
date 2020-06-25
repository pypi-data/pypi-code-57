from unittest.mock import Mock

from testframework.checkers.pubsub_client_checker import PubsubClientChecker
from testframework.pubsub.pubsub_checker import PubsubChecker
from testframework.pubsub.pubsub_creator import PubsubCreator

SINGLE_SUBSCRIPTION = {
    "some_topic":  ["some_subscription"]
}


class TestPubsubClientChecker:

    def setup_method(self, method):
        self.mock_pubsub_creator = Mock(PubsubCreator)
        self.mock_pubsub_checker = Mock(PubsubChecker)
        self.__checker = PubsubClientChecker(self.mock_pubsub_creator, self.mock_pubsub_checker)

    def test_create_input_topics_and_subscriptions_subscriptionExists(self):
        self.mock_pubsub_checker.topic_exists.return_value = True
        self.mock_pubsub_checker.subscriptions_exist.return_value = (True, [])

        self.__checker.create_topics_and_subscriptions(SINGLE_SUBSCRIPTION)

        self.mock_pubsub_creator.create_subscription.assert_not_called()
        self.mock_pubsub_creator.create_topic.assert_not_called()

    def test_create_input_topics_and_subscriptions_subscription_is_missing(self):
        self.mock_pubsub_checker.topic_exists.return_value = True
        self.mock_pubsub_checker.subscriptions_exist.return_value = (False, ["project/some_project/subscription/some_subscription"])

        self.__checker.create_topics_and_subscriptions(SINGLE_SUBSCRIPTION)

        self.mock_pubsub_creator.create_subscription.assert_called_once()
        self.mock_pubsub_creator.create_topic.assert_not_called()

    def test_create_input_topics_and_subscriptions_topicIsMissing(self):
        self.mock_pubsub_checker.topic_exists.return_value = False
        self.mock_pubsub_checker.subscriptions_exist.return_value = (True, [])

        self.__checker.create_topics_and_subscriptions(SINGLE_SUBSCRIPTION)

        self.mock_pubsub_creator.create_topic.assert_called_once()
        self.mock_pubsub_creator.create_subscription.assert_not_called()
