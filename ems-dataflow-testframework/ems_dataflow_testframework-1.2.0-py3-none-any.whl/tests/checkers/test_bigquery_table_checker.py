import datetime
from unittest.mock import Mock, patch

from testframework.checkers.bigquery_checker import BigqueryChecker
from testframework.checkers.bigquery_table_checker import BigqueryTableChecker
from testframework.checkers.checker_message import CheckerMessage
from testframework.checkers.checker_message_factory import CheckerMessageFactory


class TestBigqueryTableChecker:

    def setup_method(self):
        self.message_factory_mock = Mock(CheckerMessageFactory)

    def test_common_table_has_row_for_callsBigQueryCheckerMessageFound(self):
        dataset_name = "some_dataset_name"
        table_prefix = "some_table_prefix"

        bigquery_checker_mock = Mock(BigqueryChecker)
        bigquery_checker_mock.table_has_row_for.return_value = True

        event = CheckerMessage(
            {
                "message_id": 0,
                "customer_id": 123,
                "campaign_id": 0,
                "bounce_type": "some_type",
                "event_time": ""
            }
        )

        bigquery_table_checker = BigqueryTableChecker(bigquery_checker_mock,
                                                      dataset_name, table_prefix,
                                                      self.message_factory_mock)
        table_has_row_for = bigquery_table_checker.common_table_has_row_for(event)

        bigquery_checker_mock.table_has_row_for.assert_called_once_with(dataset_name, table_prefix, event)
        assert table_has_row_for is True

    def test_customer_table_has_row_for_callsBigQueryCheckerMessageFoundWithAppropriateParams(self):
        customer_id = 123
        dataset_name = "some_dataset_name"
        table_prefix = "some_table_prefix"

        bigquery_checker_mock = Mock(BigqueryChecker)
        bigquery_checker_mock.table_has_row_for.return_value = True

        event = CheckerMessage(
            {
                "message_id": 0,
                "customer_id": customer_id,
                "campaign_id": 0,
                "bounce_type": "some_type",
                "event_time": ""
            }
        )

        bigquery_table_checker = BigqueryTableChecker(bigquery_checker_mock,
                                                      dataset_name,
                                                      table_prefix,
                                                      self.message_factory_mock)
        table_has_row_for = bigquery_table_checker.customer_table_has_row_for(event)

        bigquery_checker_mock.table_has_row_for.assert_called_once_with(dataset_name,
                                                                        table_prefix + "_" + str(customer_id),
                                                                        event)
        assert table_has_row_for is True

    def test_waiting_table_has_row_for_callsBigQueryCheckerTableHasRowWithAppropriateParams(self):
        mock_now = datetime.datetime(2018, 1, 4, 11, 7, 49, 344122)
        with patch("datetime.datetime") as datetime_patch:
            datetime_patch.utcnow.return_value = mock_now

            self.message_factory_mock.get_event_as_waiting.return_value = "it_should_be_a_waiting_checker_message"

            dataset_name = "dataflow_waiting_events"
            table_name = "waiting_events_*"
            event_type = "some_event_type"
            checker_mock = Mock(BigqueryChecker)
            original_event = CheckerMessage(
                {
                    "message_id": 0,
                    "customer_id": 0,
                    "campaign_id": 0,
                    "bounce_type": "some_type",
                    "event_time": ""
                }
            )

            filter = ("_TABLE_SUFFIX IN ('{}', '{}', '{}')" +
                      " AND REGEXP_CONTAINS(event_json, r\".*{}.*\")" +
                      " AND REGEXP_CONTAINS(event_json, r\".*{}.*\")" +
                      " AND REGEXP_CONTAINS(event_json, r\".*{}.*\")") \
                .format(
                (mock_now - datetime.timedelta(hours=1)).strftime("%Y%m%d_%H"),
                mock_now.strftime("%Y%m%d_%H"),
                (mock_now + datetime.timedelta(hours=1)).strftime("%Y%m%d_%H"),
                original_event["customer_id"],
                original_event["campaign_id"],
                original_event["message_id"]
            )

            table_checker = BigqueryTableChecker(checker_mock, dataset_name, table_name, self.message_factory_mock)
            table_checker.has_waiting_row_for(original_event, event_type)

            self.message_factory_mock.get_event_as_waiting.assert_called_once_with(original_event, event_type)
            checker_mock.table_has_row_for.assert_called_once_with(dataset_name,
                                                                   table_name,
                                                                   "it_should_be_a_waiting_checker_message",
                                                                   False,
                                                                   filter)

    def test_common_table_returns_row_for_callsBigQueryCheckerTableReturnsRowWithAppropriateParams(self):
        mock_bigquery_checker = Mock(BigqueryChecker)
        dataset_name = "some_dataset_name"
        table_name = "some_table_name"
        mock_event = Mock(CheckerMessage)
        mock_factory = Mock(CheckerMessageFactory)

        table_checker = BigqueryTableChecker(mock_bigquery_checker, dataset_name, table_name, mock_factory)
        table_checker.common_table_returns_row_for(mock_event)

        mock_bigquery_checker.table_returns_row_for.assert_called_once_with(dataset_name,
                                                                            table_name,
                                                                            mock_event)
