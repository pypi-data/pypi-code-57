from lion_orm.connect import SqliteConnect
from lion_orm.query_builder import QueryBuilder
from lion_orm.query_set import QuerySet


class Query(object):
    def __init__(self, table_name):
        self.connect = SqliteConnect()
        self.cursor = self.connect.cursor
        self.table = table_name

    def commit(self):
        self.connect.connection.commit()

    def execute(self, query, *variables):
        self.cursor.execute(query, variables)
        self.commit()

    def fetchall(self, query):
        self.execute(query)
        result = self.cursor.fetchall()
        return result

    def create_table(self, columns_dict, if_not_exist=False):
        query = QueryBuilder(self.table).create_table(columns_dict, if_not_exist=if_not_exist)
        self.execute(query)

    def select(self, *columns, where=''):
        query = QueryBuilder(self.table).select(*columns, where=where)
        self.execute(query)
        result = self.cursor.fetchall()
        return result

    def insert(self, **values):
        query = QueryBuilder(self.table).insert(values.keys())
        self.execute(query, *(values.values()))

    def update(self, where, **values):
        query = QueryBuilder(self.table).update(where, **values)
        self.execute(query)

    def delete_by_id(self, id):
        where = QueryBuilder.where_equals(id=id)
        query = QueryBuilder(self.table).delete(where)
        self.execute(query)
