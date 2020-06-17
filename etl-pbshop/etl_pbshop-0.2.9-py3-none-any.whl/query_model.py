

class QueryFactory(object):

    def __init__(self, table_name='table', schema='dw'):
        self.table_name = table_name
        self.schema = schema
        self.full_tablename = f"{self.schema}.{self.table_name}"


    MODEL = {
        "INSERT": """
            INSERT INTO {table}
                ({column})
            VALUES
                ({values});""",
        "INSERT_ALL": """
            INSERT INTO {table}
                ({column})
            VALUES
                {values};""",
        "UPDATE": """
            UPDATE {table}
            SET
                {key}
            WHERE
                {condition_number};""",
        "DROP": """
            DELETE 
            FROM
                {table}
            WHERE
                {condition_number};""",
        "DROP_ALL": """
            DELETE 
            FROM
                {table};""",
        "SELECT": """
            SELECT 
                {column}
            FROM
                {table};""",
        "SELECT_WHERE": """
            SELECT 
                {column}
            FROM
                {table}
            WHERE
                {condition_number};"""
    }


class DataBaseModel(object):
    def all(self):
        pass
