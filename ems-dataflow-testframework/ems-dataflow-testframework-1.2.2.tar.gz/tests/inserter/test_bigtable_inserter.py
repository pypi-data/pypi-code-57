from unittest.mock import Mock, call, MagicMock

from google.cloud.bigtable.row import Row
from google.cloud.bigtable.table import Table

from testframework.inserter.bigtable_inserter import BigtableInserter


class TestBigtableInserter:
    def setup_method(self):
        self.bigtable_key = "some_bigtable_key_a"
        self.bigtable_key_end = "some_bigtable_key_b"
        self.column_family = "column_family"
        self.qualifier = "qualifier"
        self.table_mock = Mock(Table)
        self.value = "value"

    def test_insert_row_commitCalled(self):
        self.table_mock.read_row.return_value = None
        inserter = BigtableInserter(self.table_mock)

        row_mock = Mock(Row)
        row_mock.set_cell = MagicMock()
        row_mock.commit = MagicMock()
        self.table_mock.direct_row.return_value = row_mock

        inserter.insert_row(self.bigtable_key, self.column_family, self.qualifier, self.value)

        exptected_set_cell_calls = [call(self.column_family, self.qualifier, self.value, None)]
        row_mock.set_cell.assert_has_calls(exptected_set_cell_calls)
        row_mock.commit.assert_has_calls([call()])
