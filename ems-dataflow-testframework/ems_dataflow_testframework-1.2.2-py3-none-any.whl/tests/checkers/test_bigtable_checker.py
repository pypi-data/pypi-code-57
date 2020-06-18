from unittest.mock import Mock, call, MagicMock

import pytest
from google.cloud.bigtable.row import Row
from google.cloud.bigtable.row_data import PartialRowsData, PartialRowData, Cell
from google.cloud.bigtable.table import Table

from testframework.checkers.bigtable_checker import BigtableChecker
from testframework.checkers.bigtable_matchers import AbstractBigtableRowMatcher
from testframework.checkers.checker_message import CheckerMessage

RETRY_ATTEMPTS = 9
NO_WAIT = 0


class TestBigtableChecker:
    class ConstantBtMatcher(AbstractBigtableRowMatcher):

        def __init__(self, matches) -> None:
            self.value = matches

        def matches(self, key: str, column_family: str, qualifier: str, value: str) -> bool:
            return self.value

    def setup_method(self):
        self.bigtable_key = "some_bigtable_key_a"
        self.bigtable_key_end = "some_bigtable_key_b"
        self.mock_message = Mock(CheckerMessage)
        self.mock_message.get_bigtable_key.return_value = self.bigtable_key
        self.table_mock = Mock(Table)
        self.scan_mock = MagicMock(PartialRowsData)

    def test_has_row_for_ifMessageFoundWithKey_returnsTrue(self):
        self.row_mock = Mock(Row)
        self.table_mock.read_row.return_value = self.row_mock

        checker = BigtableChecker(self.table_mock)
        result = checker.has_row_for(self.mock_message)

        self.mock_message.get_bigtable_key.assert_called_once()
        self.table_mock.read_row.assert_called_once_with(self.bigtable_key.encode(checker.ENCODING))
        assert result is True

    def test_has_row_for_retriesCallForMessageFound3TimesAnd(self):
        self.table_mock.read_row.return_value = None
        checker = BigtableChecker(self.table_mock)

        with pytest.raises(Exception):
            checker.has_row_for(self.mock_message, max_attempts=RETRY_ATTEMPTS, wait_seconds=NO_WAIT)

        calls = [call(self.bigtable_key.encode(checker.ENCODING))] * RETRY_ATTEMPTS
        self.table_mock.read_row.assert_has_calls(calls)

    def test_has_single_row_in_scan_matching_ifMessageFoundMatching_returnsTrue(self):
        self.table_mock.read_rows.return_value = self.scan_mock

        partial_row_data = self.create_mocked_row_data(b"some_bigtable_key", "cf", b"qualifier", b"value")
        self.scan_mock.__iter__ = Mock(return_value=iter([partial_row_data]))

        checker = BigtableChecker(self.table_mock)
        assert checker.has_single_row_in_scan_matching(self.bigtable_key, self.ConstantBtMatcher(True), max_attempts=RETRY_ATTEMPTS, wait_seconds=NO_WAIT)

    def create_mocked_row_data(self, bt_key: bytes, column_family: str, qualifier: bytes, cell_value: bytes):
        partial_row_data = Mock(PartialRowData)
        cell = Mock(Cell)
        cell.value = cell_value
        partial_row_data.cells = {column_family: {qualifier: [cell]}}
        partial_row_data.row_key = bt_key
        return partial_row_data

    def test_has_single_row_in_scan_matching_ifTwoMessageFoundMatching_returnsFalse(self):
        self.table_mock.read_rows.return_value = self.scan_mock
        partial_row_data = self.create_mocked_row_data(b"some_bigtable_key", "cf", b"qualifier", b"value")
        partial_row_data2 = self.create_mocked_row_data(b"some_bigtable_key2", "cf", b"qualifier2", b"value2")
        self.scan_mock.__iter__ = Mock(return_value=iter([partial_row_data, partial_row_data2]))

        checker = BigtableChecker(self.table_mock)
        assert not checker.has_single_row_in_scan_matching(self.bigtable_key, self.ConstantBtMatcher(True), max_attempts=RETRY_ATTEMPTS, wait_seconds=NO_WAIT)

    def test_has_single_row_in_scan_matching_ifMessageNotFoundAfterRetrying_throwsException(self):
        self.table_mock.read_rows.return_value = self.scan_mock
        checker = BigtableChecker(self.table_mock)
        partial_row_data = self.create_mocked_row_data(self.bigtable_key.encode(checker.ENCODING), "cf", b"qualifier", b"value")
        self.scan_mock.__iter__ = Mock(return_value=iter([partial_row_data]))

        with pytest.raises(Exception):
            checker.has_single_row_in_scan_matching(self.bigtable_key, self.ConstantBtMatcher(False), max_attempts=RETRY_ATTEMPTS, wait_seconds=NO_WAIT)

        calls = [call(start_key=self.bigtable_key.encode(checker.ENCODING), end_key=self.bigtable_key_end.encode(checker.ENCODING))] * RETRY_ATTEMPTS
        self.table_mock.read_rows.assert_has_calls(calls, any_order=True)

    def test_has_single_row_in_scan_for_ifMessageFoundWithMatchingKey_returnsTrue(self):
        self.table_mock.read_rows.return_value = self.scan_mock
        checker = BigtableChecker(self.table_mock)
        partial_row_data = self.create_mocked_row_data(self.bigtable_key.encode(checker.ENCODING), "cf", b"qualifier", b"value")
        self.scan_mock.__iter__ = Mock(return_value=iter([partial_row_data]))

        result = checker.has_single_row_in_scan_for(self.mock_message, max_attempts=RETRY_ATTEMPTS, wait_seconds=NO_WAIT)

        self.mock_message.get_bigtable_key.assert_called_once()
        self.table_mock.read_rows.assert_called_once_with(start_key=self.bigtable_key.encode(checker.ENCODING), end_key=self.bigtable_key_end.encode(checker.ENCODING))
        assert result is True

    def test_has_single_row_in_scan_for_ifMessageFoundWithMultipleMatchingRows_returnsFalse(self):
        self.table_mock.read_rows.return_value = self.scan_mock
        partial_row_data = self.create_mocked_row_data(b"some_bigtable_key", "cf", b"qualifier", b"value")
        partial_row_data2 = self.create_mocked_row_data(b"some_bigtable_key2", "cf", b"qualifier2", b"value2")
        self.scan_mock.__iter__ = Mock(return_value=iter([partial_row_data, partial_row_data2]))

        checker = BigtableChecker(self.table_mock)
        result = checker.has_single_row_in_scan_for(self.mock_message, max_attempts=RETRY_ATTEMPTS, wait_seconds=NO_WAIT)

        assert result is False

    def test_has_single_row_in_scan_for_retriesCall(self):
        self.table_mock.read_rows.return_value = self.scan_mock
        self.scan_mock.rows = {}

        checker = BigtableChecker(self.table_mock)

        with pytest.raises(Exception):
            checker.has_single_row_in_scan_for(self.mock_message, max_attempts=RETRY_ATTEMPTS, wait_seconds=NO_WAIT)

        calls = [call(start_key=self.bigtable_key.encode(checker.ENCODING), end_key=self.bigtable_key_end.encode(checker.ENCODING))] * RETRY_ATTEMPTS
        self.table_mock.read_rows.assert_has_calls(calls, any_order=True)
