import psycopg2
import psycopg2.extras

from dataclasses import dataclass


@dataclass
class PostgresAuthData:
    dbname: str
    user: str
    password: str
    host: str
    port: int


def make_dict_rows(rows: list) -> list:
    dict_list = []
    for row in rows:
        dict_list.append(dict(row))
    return dict_list


class DataBase:
    def __init__(self, pg_auth_data: PostgresAuthData):
        self.conn = psycopg2.connect(dbname=pg_auth_data.dbname, user=pg_auth_data.user, password=pg_auth_data.password,
                                     host=pg_auth_data.host, port=pg_auth_data.port)
        self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def request(self, sql_request, args: tuple = None):
        try:
            if args:
                self.cursor.execute(sql_request, args)
                return make_dict_rows(self.cursor.fetchall())
            else:
                self.cursor.execute(sql_request)
                return make_dict_rows(self.cursor.fetchall())
        except psycopg2.ProgrammingError:
            return None

    def commit(self):
        self.conn.commit()
