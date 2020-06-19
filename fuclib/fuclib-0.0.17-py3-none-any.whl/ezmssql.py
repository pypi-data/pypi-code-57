# file: ezmssql.py
# Author: eamonn
import pymssql


class SqlServer(object):
    """A lightweight wrapper around SqlServer.
    """

    def __init__(self, host, user, password, database):

        self.__conn_list = pymssql.connect(host=host, user=user, password=password, database=database,
                                         charset="utf8")

        self.__conn_dict = pymssql.connect(host=host, user=user, password=password, database=database,
                                         charset="utf8", as_dict=True)

    def execute(self, sql):
        with self.__conn_list.cursor() as cursor:
            cursor.execute(sql)
            self.__conn_list.commit()

    def get(self, sql):
        with self.__conn_list.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchone()

    def get_dict(self, sql):
        with self.__conn_dict.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchone()

    def query(self, sql):
        with self.__conn_list.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

    def query_dict(self, sql):
        with self.__conn_dict.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

    def __insert(self, sql, values=None):
        with self.__conn_list.cursor() as cursor:

            if values:
                cursor.execute(sql, values)
            else:
                cursor.execute(sql)
            self.__conn_list.commit()

    def insert(self, table_name, item):
        keys, values = zip(*item.items())
        try:
            sql = "INSERT INTO %s (%s) VALUES (%s)" % (table_name, ",".join(keys), ",".join(["%s"] * len(values)))
            self.__insert(sql, values)
        except Exception as e:
            print(sql)
            print(e)

    def insert_many(self, table_name, items):
        if isinstance(items, list):
            for item in items:
                self.insert(table_name, item)
