import datetime
from unittest.mock import Mock, MagicMock, patch, call

import pytest

from testframework.checkers import bigquery_checker
from testframework.checkers.bigquery_checker import BigqueryChecker
from testframework.checkers.checker_message import CheckerMessage
from testframework.util.assertion import undecorated_module
from testframework.util.sql_handler import SqlHandler

RETRY_COUNT = 8
ZERO_SECONDS = 0


class TestBigqueryChecker:

    def test_table_returns_row_for_callsGetMessagesAndReturnsFirstRow(self):
        is_partitioned = True
        where = "some_where_filter"
        returned_rows = ["row1", "row2"]

        self.bq_helper_mock.execute_sync_query.side_effect = [[1]]
        self.checker = BigqueryChecker(self.bq_helper_mock, self.sql_handler_mock)

        with patch.object(self.checker, 'get_messages', wraps=self.checker.message_found):
            self.checker.get_messages.return_value = returned_rows

            assert returned_rows[0] == self.checker.table_returns_row_for(self.dataset_name, self.table_name, self.message_mock, is_partitioned, where)
            self.checker.get_messages.assert_called_once_with(self.dataset_name, self.table_name, self.message_mock, is_partitioned, where, True, "loaded_at")

    def test_table_returns_row_for_retriesCallForMessageFound3Times(self):
        self.bq_helper_mock.execute_sync_query.side_effect = [[1]]
        self.checker = BigqueryChecker(self.bq_helper_mock, self.sql_handler_mock)

        with patch.object(self.checker, 'get_messages', wraps=self.checker.message_found):
            self.checker.get_messages.return_value = None

            with pytest.raises(Exception):
                self.checker.table_returns_row_for(self.dataset_name, self.table_name, self.message_mock, max_attempts=RETRY_COUNT, wait_seconds=ZERO_SECONDS)

            calls = [call(self.dataset_name, self.table_name, self.message_mock, True, None, True, "loaded_at")] * RETRY_COUNT
            self.checker.get_messages.assert_has_calls(calls)

    def test_table_has_row_for_callsMessageFound(self):
        is_partitioned = True
        where = "some_where_filter"

        self.bq_helper_mock.execute_sync_query.side_effect = [[1]]
        self.checker = BigqueryChecker(self.bq_helper_mock, self.sql_handler_mock)

        with patch.object(self.checker, 'message_found', wraps=self.checker.message_found):
            self.checker.message_found.return_value = True

            assert self.checker.table_has_row_for(self.dataset_name, self.table_name, self.message_mock, is_partitioned, where)
            self.checker.message_found.assert_called_once_with(self.dataset_name, self.table_name, self.message_mock, is_partitioned, where, True, "loaded_at")

    @undecorated_module(bigquery_checker, 'tenacity.retry')
    def test_tableHasRowFor_rowNotFound_raisesTimeoutError(self):
        self.bq_helper_mock.execute_sync_query.side_effect = [[1]]
        self.checker = bigquery_checker.BigqueryChecker(self.bq_helper_mock, self.sql_handler_mock)
        with patch.object(self.checker, 'message_found', wraps=self.checker.message_found):
            self.checker.message_found.return_value = False

            with pytest.raises(TimeoutError):
                self.checker.table_has_row_for(self.dataset_name, self.table_name, self.message_mock)

    def test_get_messages_with_is_partitioned_true_query_executed_with_correctly_formatted_query(self):
        utcnow = datetime.datetime(2017, 9, 14, 11, 47, 42)

        self.bq_client_mock.project = "testing"

        sql_handler = SqlHandler()
        with patch("datetime.datetime"), patch.object(sql_handler, 'build_query',
                                                      wraps=sql_handler.build_query) as sql_handler_build_query:
            datetime.datetime.utcnow.return_value = utcnow

            self.checker = BigqueryChecker(self.bq_helper_mock, sql_handler)
            self.checker.get_messages(self.dataset_name, self.table_name, self.message_mock)

            params_for_query = {"gcp_project_id": self.bq_client_mock.project,
                                "dataset_name": self.dataset_name,
                                "table_name": self.table_name}

            partition_filter_sql = ("(_PARTITIONTIME IS NULL OR _PARTITIONTIME" + \
                                    " BETWEEN TIMESTAMP_ADD(TIMESTAMP('{partition_day}'), INTERVAL -1 DAY)" + \
                                    " AND TIMESTAMP_ADD(TIMESTAMP('{partition_day}'), INTERVAL 1 DAY))").format(
                partition_day="2017-09-14")
            where_params = {
                "filter": "CAST(customer_id AS STRING) = '123'",
                "partition_filter": partition_filter_sql,
                "where": "loaded_at is not null"
            }

            expected_sql_to_run = \
                ("SELECT * FROM `{gcp_project_id}.{dataset_name}.{table_name}` " + \
                 "WHERE ({partition_filter}) " + \
                 "AND ({filter}) " + \
                 "AND ({where})").format(**{**params_for_query, **where_params})

            datetime.datetime.utcnow.assert_called_once()
            self.message_mock.get_unique_fields.assert_called_once()
            sql_handler_build_query.assert_has_calls(
                [call({**params_for_query, **where_params})])
            self.bq_helper_mock.execute_sync_query.assert_called_once_with(expected_sql_to_run)

    def test_get_messages_with_is_partitioned_false_query_executed_with_correctly_formatted_query(self):
        utcnow = datetime.datetime(2017, 9, 14, 11, 47, 42)

        self.bq_client_mock.project = "testing"
        self.sql_handler_mock.build_query.return_value = "valid_query"

        self.checker = BigqueryChecker(self.bq_helper_mock, self.sql_handler_mock)

        with patch("datetime.datetime"):
            datetime.datetime.utcnow.return_value = utcnow
            self.checker.get_messages(self.dataset_name, self.table_name, self.message_mock, False)

            params_for_query = {"gcp_project_id": self.bq_client_mock.project,
                                "dataset_name": self.dataset_name,
                                "table_name": self.table_name}
            where_params = {
                "filter": "CAST(customer_id AS STRING) = '123'",
                "partition_filter": "true",
                "where": "loaded_at is not null"
            }

            datetime.datetime.utcnow.assert_not_called()
            self.message_mock.get_unique_fields.assert_called_once()
            self.sql_handler_mock.build_query.assert_called_once_with({**params_for_query, **where_params})
            self.bq_helper_mock.execute_sync_query.assert_called_once_with("valid_query")

    def test_get_messages_with_is_partitioned_false_and_where_conditions_query_executed_with_correctly_formatted_query(
            self):
        utcnow = datetime.datetime(2017, 9, 14, 11, 47, 42)
        where = "loaded_at is not null"

        self.bq_client_mock.project = "testing"
        self.sql_handler_mock.build_query.return_value = "valid_query"

        self.checker = BigqueryChecker(self.bq_helper_mock, self.sql_handler_mock)

        with patch("datetime.datetime"):
            datetime.datetime.utcnow.return_value = utcnow
            self.checker.get_messages(self.dataset_name, self.table_name, self.message_mock, False)

            params_for_query = {"gcp_project_id": self.bq_client_mock.project,
                                "dataset_name": self.dataset_name,
                                "table_name": self.table_name}
            where_params = {
                "filter": "CAST(customer_id AS STRING) = '123'",
                "partition_filter": "true",
                "where": where
            }

            datetime.datetime.utcnow.assert_not_called()
            self.message_mock.get_unique_fields.assert_called_once()
            self.sql_handler_mock.build_query.assert_called_once_with({**params_for_query, **where_params})
            self.bq_helper_mock.execute_sync_query.assert_called_once_with("valid_query")

    def test_get_messages_returns_rows(self):
        self.bq_helper_mock.execute_sync_query.side_effect = [[1, 2]]
        self.checker = BigqueryChecker(self.bq_helper_mock, self.sql_handler_mock)

        assert [1, 2] == self.checker.get_messages(self.dataset_name, self.table_name, self.message_mock)

    def test_message_found_returns_results(self):
        self.bq_helper_mock.execute_sync_query.side_effect = [[1]]
        self.checker = BigqueryChecker(self.bq_helper_mock, self.sql_handler_mock)

        with patch.object(self.checker, 'get_messages', wraps=self.checker.get_messages):
            self.checker.get_messages.return_value = ['row1']

            assert self.checker.message_found(self.dataset_name, self.table_name, self.message_mock)
            self.checker.get_messages.assert_called_once_with(self.dataset_name, self.table_name, self.message_mock,
                                                              True, None, True, "loaded_at")

    def setup_method(self):
        self.dataset_name = "test_dataset"
        self.table_name = "test_table"
        self.source = {self.dataset_name: [self.table_name]}

        self.message_mock = Mock(CheckerMessage)
        self.bq_helper_mock = Mock()

        self.bq_client_mock = self.bq_helper_mock._bq_client
        self.message_mock.get_unique_fields.return_value = {"customer_id": 123}

        self.bq_helper_mock.execute_sync_query = MagicMock()

        self.sql_handler_mock = Mock(SqlHandler)
