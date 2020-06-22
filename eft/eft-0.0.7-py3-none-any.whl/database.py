import sqlalchemy
import pymysql
from pyhive import hive


def create_mysql_connection(user, passwd, host, port, database):
    engine_template = "mysql+pymysql://{user}:{passwd}@{host}:{port}/{database}?charset={charset}"
    engine_string = engine_template.format(**{"user": user,
                                              "passwd": passwd,
                                              "host": host,
                                              "port": port,
                                              "database": database,
                                              "charset": "utf8mb4"})
    return sqlalchemy.create_engine(engine_string)


def create_sqlite_connection(database_path):
    return sqlalchemy.create_engine(database_path)


def create_pymysql_connection(user, passwd, host, port, database):
    """在对大型表逐行扫表时使用(和sscursor配合使用)"""
    return pymysql.connect(host, user, passwd, database, port, charset="utf8mb4")


def create_hive_connection(user, host, port, database):
    return hive.Connection(host=host, port=port, username=user, database=database)