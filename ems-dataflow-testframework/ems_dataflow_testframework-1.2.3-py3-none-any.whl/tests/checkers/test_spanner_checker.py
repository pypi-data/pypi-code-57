from unittest.mock import patch, Mock

import pytest
from spanner.ems_spanner_client import EmsSpannerClient
from tenacity import RetryError

from testframework.checkers.spanner_checker import SpannerChecker


@patch('testframework.checkers.spanner_checker.ems_spanner_client')
def test_execute_sql(spanner_client_module_mock):
    ems_client_mock = Mock(EmsSpannerClient)
    spanner_client_module_mock.EmsSpannerClient.return_value = ems_client_mock
    spanner_client = SpannerChecker('some-project-id', 'instance-id', 'db')
    expected = ['a', 'b']
    ems_client_mock.execute_sql.return_value = expected

    assert spanner_client.execute_sql('some sql') == expected


@patch('testframework.checkers.spanner_checker.ems_spanner_client')
def test_has_row_for_returns_false_if_no_matching_row_found(spanner_client_module_mock):
    ems_client_mock = Mock(EmsSpannerClient)
    spanner_client_module_mock.EmsSpannerClient.return_value = ems_client_mock
    spanner_client = SpannerChecker('some-project-id', 'instance-id', 'db')
    spanner_client.WAIT_FIXED = 1
    spanner_client.STOP_AFTER_ATTEMPT_SECS = 1
    ems_client_mock.execute_sql.return_value = [[0]]

    with pytest.raises(RetryError):
        spanner_client.has_row_for("table_name", {"column_name": "column_value"})


@patch('testframework.checkers.spanner_checker.ems_spanner_client')
def test_has_row_for_returns_true_if_matching_row_found(spanner_client_module_mock):
    ems_client_mock = Mock(EmsSpannerClient)
    spanner_client_module_mock.EmsSpannerClient.return_value = ems_client_mock
    spanner_client = SpannerChecker('some-project-id', 'instance-id', 'db')
    ems_client_mock.execute_sql.return_value = [[1]]

    assert spanner_client.has_row_for("table_name", {"column_name": "column_value"})


@patch('testframework.checkers.spanner_checker.ems_spanner_client')
def test_has_row_for_returns_true_if_matching_row_found_for_int_value(spanner_client_module_mock):
    ems_client_mock = Mock(EmsSpannerClient)
    spanner_client_module_mock.EmsSpannerClient.return_value = ems_client_mock
    spanner_client = SpannerChecker('some-project-id', 'instance-id', 'db')
    ems_client_mock.execute_sql.return_value = [[1]]

    assert spanner_client.has_row_for("table_name", {"column_name": 123})
