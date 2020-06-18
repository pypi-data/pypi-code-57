from typing import List
from unittest.mock import patch, Mock

from spanner.ems_spanner_client import EmsSpannerClient

from testframework.checkers.spanner_checker import SpannerChecker


@patch('testframework.checkers.spanner_checker.ems_spanner_client')
def test_execute_sql(spanner_client_module_mock):
    ems_client_mock = Mock(EmsSpannerClient)
    spanner_client_module_mock.EmsSpannerClient.return_value = ems_client_mock
    spanner_client = SpannerChecker('some-project-id', 'instance-id', 'db')
    expected = ['a', 'b']
    ems_client_mock.execute_sql.return_value = expected

    assert spanner_client.execute_sql('some sql') == expected
