from .util import get_data_yaml_dict
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
import pandas as pd


class MYSQL:
    def __init__(self):
        self.connections = get_data_yaml_dict(type(self).__name__.lower())

    def get_query_results(self, query, connection, database=None):
        c = self.connections[connection]
        database = c['database'] if 'database' in c else database
        db_url = {
            'drivername': 'mysql+pymysql',
            'username': c['username'],
            'password': c['password'],
            'host': c['host'],
            'database': database,
            'query': {'charset': 'UTF8MB4'},
        }
        db_connection = create_engine(URL(**db_url))
        return pd.read_sql(query, con=db_connection)

