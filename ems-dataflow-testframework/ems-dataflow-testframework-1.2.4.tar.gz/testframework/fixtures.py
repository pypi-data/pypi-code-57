import logging
import time

import pytest
from bigquery.ems_bigquery_client import EmsBigqueryClient
from google.cloud import bigtable
from google.cloud import bigquery
from google.cloud.pubsub_v1 import PublisherClient, SubscriberClient
from testframework.checkers.bigquery_checker import BigqueryChecker
from testframework.checkers.bigquery_table_checker import BigqueryTableChecker
from testframework.checkers.bigtable_checker import BigtableChecker
from testframework.checkers.checker_message_factory import CheckerMessageFactory
from testframework.checkers.pubsub_message_receiver import PubsubMessageReceiver
from testframework.checkers.pubsub_publisher import PubsubPublisher
from testframework.checkers.pubsub_topic_checker import PubsubTopicChecker
from testframework.checkers.spanner_checker import SpannerChecker
from testframework.config.environment import get_gcp_project_id, get_bigtable_project_id, get_gcp_backup_project_id
from testframework.inserter.bigtable_inserter import BigtableInserter
from testframework.util.sql_handler import SqlHandler

PROJECT_ID = get_gcp_project_id()
BIGTABLE_PROJECT_ID = get_bigtable_project_id()
BACKUP_PROJECT_ID = get_gcp_backup_project_id()


def publisher_client():
    return PublisherClient()


def subscriber_client():
    return SubscriberClient()


def subscribe_to_topic(topic_name) -> PubsubTopicChecker:
    request = current_request_provider.get()
    receiver = PubsubMessageReceiver(time, subscriber_client())
    checker = PubsubTopicChecker(publisher_client(), subscriber_client(), PROJECT_ID, topic_name, receiver)
    request.addfinalizer(checker.close)
    return checker


def pubsub_publisher_for(topic_name: str) -> PubsubPublisher:
    return PubsubPublisher(publisher_client(), PROJECT_ID, topic_name)


def bigquery_client():
    client = bigquery.Client(PROJECT_ID)
    logging.info("Bigquery project: {}".format(client.project))
    return client


def bigquery_backup_client():
    client = bigquery.Client(BACKUP_PROJECT_ID)
    logging.info("Bigquery backup project: {}".format(client.project))
    return client


def bigquery_checker():
    bigquery_helper = BigqueryHelper(bigquery_client())
    return BigqueryChecker(bigquery_helper, SqlHandler())


def bigquery_table(dataset_name: str = None, table_name: str = None) -> BigqueryTableChecker:
    checker_message_factory = CheckerMessageFactory()
    return BigqueryTableChecker(bigquery_checker(), dataset_name, table_name, checker_message_factory)


def bigquery_backup_table(dataset_name: str = None, table_name: str = None) -> BigqueryTableChecker:
    checker_message_factory = CheckerMessageFactory()
    bigquery_helper = BigqueryHelper(bigquery_backup_client())
    bigquery_backup_checker = BigqueryChecker(bigquery_helper, SqlHandler())
    return BigqueryTableChecker(bigquery_backup_checker, dataset_name, table_name, checker_message_factory)


def bigquery_error_table(table_name: str = None):
    checker_message_factory = CheckerMessageFactory()
    bigquery_helper = BigqueryHelper(bigquery_client())
    bigquery_error_checker = BigqueryChecker(bigquery_helper, SqlHandler())
    return BigqueryTableChecker(bigquery_error_checker, "dataflow_errors", table_name, checker_message_factory)


def bigtable_table(table_name: str):
    bigtable_client = bigtable.Client(BIGTABLE_PROJECT_ID)
    instance = bigtable_client.instance(BIGTABLE_PROJECT_ID)
    table = instance.table(table_name)
    return BigtableChecker(table)


def spanner(project_id: str, instance_id: str, db_name: str):
    return SpannerChecker(project_id, instance_id, db_name)


def bigtable_table_inserter(table_name: str):
    bigtable_client = bigtable.Client(BIGTABLE_PROJECT_ID)
    instance = bigtable_client.instance(BIGTABLE_PROJECT_ID)
    table = instance.table(table_name)
    return BigtableInserter(table)


def bt_table(request):
    bigtable_client = bigtable.Client(BIGTABLE_PROJECT_ID)
    instance = bigtable_client.instance(BIGTABLE_PROJECT_ID)
    try:
        BIGTABLE_TABLE_NAME = request.param
    except AttributeError:
        BIGTABLE_TABLE_NAME = "EMAIL_SENDS"
    logging.info("Communicating with table {} in project {}".format(BIGTABLE_TABLE_NAME, BIGTABLE_PROJECT_ID))
    table = instance.table(BIGTABLE_TABLE_NAME)
    return table


def bt_instance():
    bigtable_client = bigtable.Client(BIGTABLE_PROJECT_ID, admin=True)
    instance = bigtable_client.instance(BIGTABLE_PROJECT_ID)
    return instance


def send_event_from(other_event):
    return CheckerMessageFactory().get_event_as_send(other_event)


def old_event_from(event):
    return CheckerMessageFactory().get_old_event_from(event)


class CurrentRequestProvider:

    def __init__(self):
        self._request = None

    def set(self, request):
        self._request = request

    def get(self):
        return self._request


current_request_provider = CurrentRequestProvider()


@pytest.fixture(scope="module")
def register_request(request):
    current_request_provider.set(request)

    return request


class BigqueryHelper:
    def __init__(self, bq_client):
        self._bq_client = bq_client
        self.__ems_bq_client = EmsBigqueryClient(bq_client.project)

    def execute_sync_query(self, query_str):
        return list(self.__ems_bq_client.run_sync_query(query_str))
