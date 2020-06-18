from google.cloud.bigtable.table import Table


class BigtableInserter:

    def __init__(self, bt_table: Table) -> None:
        self.__table = bt_table
        self.ENCODING = "utf-8"

    def insert_row(self, row_key, column_family, qualifier, value, version=None):
        row = self.__table.direct_row(row_key)
        row.set_cell(column_family, qualifier, value, version)
        row.commit()
