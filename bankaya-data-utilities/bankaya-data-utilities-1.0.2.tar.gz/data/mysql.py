from .util import get_data_yaml_dict
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
import pandas as pd


class MYSQL:
    pool_connections = {}

    @classmethod
    def initialize_connections(cls):
        connections = get_data_yaml_dict(cls.__name__.lower())
        for connection in connections.keys():
            c = connections[connection]
            db_url = {
                'drivername': 'mysql+pymysql',
                'username': c['username'],
                'password': c['password'],
                'host': c['host'],
                'database': c['database'],
                'query': {'charset': 'UTF8MB4'},
            }
            MYSQL.pool_connections[connection] = create_engine(URL(**db_url),
                                                            pool_size=int(c['pool_size']),
                                                            max_overflow=int(c['max_overflow']),
                                                            pool_timeout=int(c['pool_timeout']))

    def get_query_results(self, query, connection):
        return pd.read_sql(query, con=MYSQL.pool_connections[connection])

