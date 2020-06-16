from .util import get_data_yaml_dict
from sqlalchemy import create_engine
import pandas as pd


class MYSQL:
    def __init__(self):
        self.connections = get_data_yaml_dict(type(self).__name__.lower())

    def get_query_results(self, query, connection, database=None):
        c = self.connections[connection]
        database = c['database'] if 'database' in c else database
        db_connection_str = f'mysql+pymysql://{c["username"]}:{c["password"]}@{c["host"]}:{c["port"]}/{database}'
        db_connection = create_engine(db_connection_str)
        return pd.read_sql(query, con=db_connection)

