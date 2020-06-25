import logging

from pytest import fixture

from testframework.pubsub.pubsub_checker import PubsubChecker
from testframework.pubsub.pubsub_creator import PubsubCreator


class PubsubClientChecker:

    def __init__(self, pubsub_creator: PubsubCreator, pubsub_checker: PubsubChecker):
        self.__pubsub_creator = pubsub_creator
        self.__pubsub_checker = pubsub_checker
        logging.info("Project is: {}".format(self.__pubsub_creator.project()))

    def create_topics_and_subscriptions(self, topics_subscriptions_map: dict, subscription_project_id=None):
        for topic_name, subscription_list in topics_subscriptions_map.items():
            self.__create_topic(topic_name)

            self.__create_subscriptions(subscription_list, topic_name, subscription_project_id)

    def __create_topic(self, topic_name):
        if not self.__pubsub_checker.topic_exists(topic_name):
            topic_path = self.__pubsub_creator.topic_path(topic_name)
            logging.info("Creating topic: {}".format(topic_path))
            self.__pubsub_creator.create_topic(topic_name)

    def __create_subscriptions(self, subscription_list, topic_name, subscription_project_id=None):
        result, missing_subscriptions = self.__pubsub_checker.subscriptions_exist(topic_name, subscription_list, subscription_project_id=subscription_project_id)

        for missing_subscription in missing_subscriptions:
            logging.info("Creating subscription {} for topic {} in project {}".format(missing_subscription, topic_name, self.__pubsub_creator.project()))
            self.__pubsub_creator.create_subscription(topic_name, missing_subscription)


@fixture(scope="function")
def pubsub_client_checker(request):
    pubsub_creator, pubsub_checker = request.param
    checker = PubsubClientChecker(
        pubsub_creator,
        pubsub_checker)
    return checker
