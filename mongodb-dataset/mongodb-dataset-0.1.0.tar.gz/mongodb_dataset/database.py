import pymongo
from typing import Optional


class Database:
    def __init__(self, uri="", db_name="database"):
        self.client = pymongo.MongoClient(uri)
        self.db_name = db_name

    def __getitem__(self, table):
        return Table(self.client, db_name=self.db_name, table_name=table)


class Table:
    def __init__(self, client, db_name: str = "database", table_name: str = "table"):
        self.client = client
        self.db_name = db_name
        self.table_name = table_name
        self.table = self.client[self.db_name][self.table_name]

    def insert(self, row: dict):
        """
        Inserts row
        """
        return self.table.insert_one(row)

    def find_one(self, **row) -> dict:
        """
        Returns the first match
        """
        return dict(self.table.find_one(row))

    def find(self, **row) -> list:
        """
        Searches. Does not support comparison operators yet.
        """
        return list(self.table.find(row, projection=None))

    def all(self):
        """
        Returns everything in the table
        """
        raise NotImplementedError()

    def delete(self, **row):
        """
        Deletes everything that matches
        """
        self.table.delete_many(row)

    def count(self, filter_expr: dict) -> int:
        """
        Counts the number of items that match the filter expression
        """
        return int(self.table.count_documents(filter_expr))
