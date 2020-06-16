import urllib
import os
import re
import json
import datetime

import sqlalchemy
from sqlalchemy.orm import Session

import pandas as pd
import numpy as np
from jinjasql import JinjaSql


class Connection(object):
    def __init__(self, conn_details, server_warnings=False):
        """ Creates a connection to a sql database using SQLAlchemy session

        Currently supports MySQL,  PostgreSQL, SQL Server (MSSQL), and Oracle.

        Args:
            conn_details (dict): Dictionary with the connection details. E.g.
                                       {"server_type": "mssql",
                                        "ip": "127.0.0.1",
                                        "db": "my_db",
                                        "user": "user",
                                        "pw": "password"}
            server_warnings (boolean): Defaults to False. Server warnings will be displayed when set to True. Has not been implemented!
        
        Returns:
            No value
        """

        conn_details["db"] = conn_details.get("db", "")
        conn_details["connect_args"] = conn_details.get("connect_args", None)

        # Needed for Oracle inserts and updates if the schema is different from the user schema
        self.schema = conn_details.get("schema", None)

        # MySQL
        if conn_details["server_type"] == "mysql":

            conn_details["port"] = conn_details.get("port", 3306)

            conn_string = "mysql+pymysql://{user}:{pw}@{ip}:{port}/{db}".format(
                **conn_details
            )

            self.server_type = "mysql"

        # PostgreSQL
        elif conn_details["server_type"] in ["postgresql", "postgres"]:

            conn_details["port"] = conn_details.get("port", 5432)

            conn_string = "postgresql+psycopg2://{user}:{pw}@{ip}:{port}/{db}".format(
                **conn_details
            )

            self.server_type = "postgresql"

        # MSSQL
        elif conn_details["server_type"] == "mssql":

            conn_details["port"] = conn_details.get("port", 1433)
            conn_details["odbcDriver"] = conn_details.get(
                "odbcDriver", "{ODBC Driver 17 for SQL Server}"
            )

            conn_string = "mssql+pyodbc:///?odbc_connect=" + urllib.parse.quote_plus(
                "DRIVER={odbcDriver};SERVER={ip};DATABASE={db};UID={user};PWD={pw};PORT={port}".format(
                    **conn_details
                )
            )

            self.server_type = "mssql"

        # Oracle
        elif conn_details["server_type"] == "oracle":

            conn_details["port"] = conn_details.get("port", 1521)
            dsn_string = "(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST={ip})(PORT={port}))(CONNECT_DATA=(SERVICE_NAME={service})))".format(
                **conn_details
            )
            conn_details["dsn"] = dsn_string

            conn_string = "oracle://{user}:{pw}@{dsn}".format(**conn_details)

            self.server_type = "oracle"

        else:
            raise Exception(
                "The server_type '{server_type}' is not supported".format(
                    **conn_details
                )
            )

        if conn_details["connect_args"]:
            engine = sqlalchemy.create_engine(
                conn_string, connect_args=conn_details["connect_args"]
            )
        else:
            engine = sqlalchemy.create_engine(conn_string)

        self.session = sqlalchemy.orm.session.Session(bind=engine)
        self.metadata = sqlalchemy.MetaData(bind=engine)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.session.close()

    def commit(self):
        self.session.commit()

    def now(self):
        # gets current datetime from db server
        return self.session.query(sqlalchemy.sql.func.now()).first()[0]

    def query(
        self,
        query,
        commit=False,
        return_type="lists",
        query_type=None,
        insert_id_field=None,
    ):
        """Execute raw sql query 
        
        Args:
            query (str): The SQL query that will be executed
            commit (boolean): Defaults to False. If set to True will use commit command after executing the query.
            return_type (str): Defaults to the value 'lists' (list of lists). Other possible values are 'df' (pandas dataframe) or 'dicts' (list of dictionaries).
            query_type (str): Defaults to None. Used to set the query type. Valid values are 'insert', 'update', and 'select'.
            insert_id_field (str): Defaults to None. Needs to be provided for insert statements for Oracle and PostgreSQL if
                returning the last inserted id is required (will return None if not provided).

        Returns:
            rows (select) or last_insert_id (insert): If the query type is select (SQLAlchemy returns rows) a dataframe, list of lists or 
                list of dicts is returned depending on the specified return_type. If the query_type is insert and the database supports 
                the functionallity to return the last inserted id the system will return the id. If neither of these cases is matched
                None is returned.
        """

        # Check if return_type is valid
        valid_return_types = ["lists", "df", "dicts"]
        if return_type not in valid_return_types:
            raise Exception(
                "'{}' is an invalid value for the variable return_type.".format(
                    return_type
                )
            )

        # If query_type is not provided determine it based on the first word of the query (works for update, insert, select)
        if query_type is None:
            try:
                query_type = re.split(" |\n", query, 1)[0].lower()
                if query_type not in ("select", "insert", "update"):
                    query_type = None
            except:
                query_type = None

        # Inserts for PostgreSQL and Oracle require a modification to the query to retrief the inserted id (todo Oracle)
        if (
            query_type == "insert"
            and self.server_type in ("postgresql", "oracle")
            and insert_id_field
        ):
            if self.server_type == "postgresql":
                query += ' returning "{}"'.format(insert_id_field)

        result = self.session.execute(query)

        if commit:
            self.commit()

        if query_type == "insert":

            if self.server_type == "mysql":
                last_insert_id = result.lastrowid

            elif self.server_type == "mssql":
                last_insert_id = self.session.execute(
                    "select scope_identity()"
                ).fetchone()[0]

            elif self.server_type in ("postgresql"):  # still to do for 'oracle'
                last_insert_id = result.fetchone()[0]

            else:
                last_insert_id = None

            return last_insert_id

        elif result.returns_rows:
            rows = result.fetchall()
            columns = result.keys()

            # Convert rows to desired type
            if return_type == "df":
                rows = pd.DataFrame(rows, columns=columns)

            elif return_type == "dicts":
                rows = convert_to_dicts({"columns": columns, "rows": rows})

            return rows

        else:
            return None

    def jinja_query(self, query_template, parameters):
        """Execute SQL statement using jinja template and parameters (no data is returned)

        Args:
            query_template (str): SQL query with jinja
            parameters (dict): Dictionary of parameters used in query

        Returns:
            No values
        """

        jsql = JinjaSql(param_style="named")

        query, bind_parameters = jsql.prepare_query(query_template, parameters)

        self.session.execute(query, bind_parameters)

    def jinja_select(self, query_template, parameters, return_type="lists"):
        """Select statement using jinja template and parameters

        Args:
            query_template (str): SQL query with jinja
            parameters (dict): Dictionary of parameters used in query
            return_type (str): Defaults to the value 'lists' (list of lists). Other possible values are 'df' (pandas dataframe) or 'dicts' (list of dictionaries).

        Returns:
            rows (list of lists, pandas dataframe or list of dictionaries): Records returned by the query.
        """
        # Check if return_type is valid
        valid_return_types = ["lists", "df", "dicts"]
        if return_type not in valid_return_types:
            raise Exception(
                "'{}' is an invalid value for the variable return_type.".format(
                    return_type
                )
            )

        jsql = JinjaSql(param_style="named")

        query, bind_parameters = jsql.prepare_query(query_template, parameters)

        result = self.session.execute(query, bind_parameters)
        rows = result.fetchall()
        columns = result.keys()

        # Convert rows to desired type
        if return_type == "df":
            rows = pd.DataFrame(rows, columns=columns)

        elif return_type == "dicts":
            rows = convert_to_dicts({"columns": columns, "rows": rows})

        return rows

    def select(self, table, columns, filters={}, return_type="lists"):
        """Select statement
        
        Args:
            table (str): Name of table to select from.
            columns (list): List of columns to select values for.
            filters (dict): The keys indicate which columns should be used for filtering and the associated values are
            used as filter criteria. E.g. {'job' : ['developer'], 'skill': ['python', 'pandas', 'sqlalchemy']}
            return_type (str): Defaults to the value 'lists' (list of lists). Other possible values are 'df' (pandas dataframe) or 'dicts' (list of dictionaries).
            
        Returns:
            rows (list of lists, pandas dataframe or list of dictionaries): Records returned by the query.
        """

        # Check if return_type is valid
        valid_return_types = ["lists", "df", "dicts"]
        if return_type not in valid_return_types:
            raise Exception(
                "'{}' is an invalid value for the variable return_type.".format(
                    return_type
                )
            )

        for key, val in filters.items():
            if isinstance(val, list) is False:
                filters[key] = [val]

        table = sqlalchemy.Table(
            table, self.metadata, autoload=True, schema=self.schema
        )

        rows = (
            self.session.query(*[table.c[col] for col in columns])
            .filter(
                *[table.c[col].in_([val for val in filters[col]]) for col in filters]
            )
            .all()
        )

        # Convert rows to desired type
        if return_type == "df":
            rows = pd.DataFrame(rows, columns=columns)

        elif return_type == "dicts":
            rows = convert_to_dicts({"columns": columns, "rows": rows})

        return rows

    def insert(self, table_name, data, static_values=None):
        """Used to insert records into table.

        Args:
            table_name (str): The table to insert into.
            data (list, dict or df): List of records that will be inserted.
                If a list is provided it needs to be a list of dictionaries (column names as keys). E.g. 
                [{'id':'1','name':'frodo','occ':'none'}, {'id':'2','name':'aragon','occ':'king'}]
                If a dictionary is provided it must contain columns (list) and rows (list of lists). E.g.
                {'columns' : ['id', 'name', 'occ'], 'rows' : [[1, 'frodo', 'none'], [2, 'aragon', 'king']]}
                If a pandas dataframe is provided the headers must be the column names. E.g.                                
                id  |  name  | occ 
                ----|--------|------ 
                1   | frodo  | none 
                2   | aragon | king
            static_values (dict): Defaults to None. This can be used to define values that are the same for each record.
                The key has to match the column name and the value the desired record value. E.g. {'company_name' : 'Google'}

        Returns:
            No value
        """

        data = convert_to_dicts(data)

        if static_values:
            add_to_dicts(data, static_values)

        table = sqlalchemy.Table(
            table_name, self.metadata, autoload=True, schema=self.schema
        )

        if self.server_type == "oracle":
            self.session.execute(table.insert(), data)
        else:
            self.session.execute(table.insert().values(data))

    def update(self, table_name, data, columns, filter_columns, static_values=None):
        """Used to update records for one table.

        When columns that are used in the where clause (filter_columns) are not indexed the update may take significantly longer.

        Args:
            table_name (str): The table to update.
            data (list, dict or df): List of records that will be updated.
                If a list is provided it needs to be a list of dictionaries (column names as keys). E.g. 
                [{'id':'1','name':'frodo','occ':'none'}, {'id':'2','name':'aragon','occ':'king'}]
                If a dictionary is provided it must contain columns (list) and rows (list of lists). E.g.
                {'columns' : ['id', 'name', 'occ'], 'rows' : [[1, 'frodo', 'none'], [2, 'aragon', 'king']]}
                If a pandas dataframe is provided the headers must be the column names. E.g.                                
                id  |  name  | occ 
                ----|--------|------ 
                1   | frodo  | none 
                2   | aragon | king
            columns (list): List of columns that are updated (used in set part of SQL statement)
            filter_columns (list): List of columns that are used to identify the records to update (used in where clause of SQL statement)
            static_values (dict): Defaults to None. This can be used to define values that are the same for each record.
                The key has to match the column name and the value the desired record value. E.g. {'company_name' : 'Google'}

        Returns:
            No value
        """

        data = convert_to_dicts(data)

        if static_values:
            add_to_dicts(data, static_values)

        data = sanitize_column_names(data, columns + filter_columns)

        table = sqlalchemy.Table(
            table_name, self.metadata, autoload=True, schema=self.schema
        )

        # Solution from stackoverflow.com/questions/48096902
        stmt = (
            table.update()
            .where(
                sqlalchemy.and_(
                    *[
                        table.c[col] == sqlalchemy.bindparam("b_" + col)
                        for col in filter_columns
                    ]
                )
            )
            .values({col: sqlalchemy.bindparam("b_" + col) for col in columns})
        )

        self.session.execute(stmt, data)

    def upsert(
        self,
        table_name,
        data,
        key_columns,
        ignore_columns=None,
        static_update_vals=None,
        static_insert_vals=None,
    ):
        """Used to upsert records for one table.

        Compares the values of the provided records (data) to the values currently stored in the table.
        Updates records that exists in the table if at least one value is different.
        Inserts a new record if no record is found using the provided keys.
        When comparing the new data to the current data in the table the static values are not considered.

        Args:
            table_name (str): The name of the table to perform upsert on.
            data (list, dict or df): List of records that will be upserted (updated or insered).
                If a list is provided it needs to be a list of dictionaries (column names as keys). E.g. 
                [{'id':'1','name':'frodo','occ':'none'}, {'id':'2','name':'aragon','occ':'king'}]
                If a dictionary is provided it must contain columns (list) and rows (list of lists). E.g.
                {'columns' : ['id', 'name', 'occ'], 'rows' : [[1, 'frodo', 'none'], [2, 'aragon', 'king']]}
                If a pandas dataframe is provided the headers must be the column names. E.g.                                
                id  |  name  | occ 
                ----|--------|------
                1   | frodo  | none 
                2   | aragon | king
            key_columns (list): List of columns that are used to uniquely identify a record for the upsert.
                These columns don't have to be actual keys in the database.
            ignore_columns (list): Defaults to None. List of columns that will not be inserted for new records.
            static_update_vals (dict): Defaults to None. This can be used to define values that are the same for each record.
                The key has to match the column name and the value the desired record value. E.g. {'company_name' : 'Google'}
                Will be used for any records that are being updated. Will not be considered when comparing current to new data.
            static_insert_vals (dict): Defaults to None. This can be used to define values that are the same for each record.
                The key has to match the column name and the value the desired record value. E.g. {'company_name' : 'Google'}
                Will be used for any records that are being inserted. Will not be considered when comparing current to new data.

        Returns:
            total_rows (int): Number of records that were provided.
            inserted_rows (int): Number of records that were inserted.
            updated_rows (int): Number of records that were updated.
        """

        data = convert_to_dicts(data)

        # Assumes that all dictionaries in the list have exactly the same keys
        columns = [key for key in data[0]]

        table = sqlalchemy.Table(
            table_name, self.metadata, autoload=True, schema=self.schema
        )

        # Get current records
        if self.server_type in ("postgresql", "mysql") and len(key_columns) > 1:
            # Filter records using tuple of keys (only supported by SQLAlchemy for PostgreSQL and MySQL)
            current_data = (
                self.session.query(*[table.c[col] for col in columns])
                .filter(
                    sqlalchemy.tuple_(*[table.c[col] for col in key_columns]).in_(
                        [[row[keyCol] for keyCol in key_columns] for row in data]
                    )
                )
                .all()
            )

        else:
            # Filter records using multiple IN statements (one for each key)
            # This seems to run faster for mysql as well
            current_data = (
                self.session.query(*[table.c[col] for col in columns])
                .filter(
                    *[
                        table.c[col].in_([row[col] for row in data])
                        for col in key_columns
                    ]
                )
                .all()
            )

        # Compare current to new records
        insert_data = []
        update_data = []

        if len(current_data) > 0:
            current_data = convert_to_dicts({"columns": columns, "rows": current_data})

            # Generate dictionaries using a concatenation of the key values as unique key for each record
            data_dict = {
                "_".join([str(row[key]) for key in key_columns]): row for row in data
            }
            current_data_dict = {
                "_".join([str(row[key]) for key in key_columns]): row
                for row in current_data
            }

            for key, val in data_dict.items():
                if key in current_data_dict:
                    if val != current_data_dict[key]:
                        update_data.append(val)
                else:
                    if ignore_columns:
                        for key in ignore_columns:
                            del val[key]
                    insert_data.append(val)

        else:
            if ignore_columns:
                for row in data:
                    for key in ignore_columns:
                        del row[key]

            insert_data = data

        # Insert new records
        inserted_rows = len(insert_data)
        if inserted_rows > 0:
            self.insert(table_name, insert_data, static_values=static_insert_vals)

        # Update existing records
        updated_rows = len(update_data)
        if updated_rows > 0:
            update_columns = list(set(columns) - set(key_columns))
            self.update(
                table_name,
                update_data,
                update_columns,
                key_columns,
                static_values=static_update_vals,
            )

        total_rows = len(data)

        return total_rows, inserted_rows, updated_rows


def sanitize_column_names(list_of_dicts, keys=None):
    """Add b_ prefix to keys in list_of_dicts (list of dicts)
    
    Args: 
        list_of_dicts (list of dicts): List of records.
        keys (list): Defaults to None.
    
    Returns:
        list_of_dicts (list of dicts): Sanitized list_of_dicts
    """

    if keys is None:
        for row in list_of_dicts:
            for key in row:
                row["b_" + key] = row.pop(key)

    else:
        keys = list(set(keys))

        for row in list_of_dicts:
            for key in keys:
                row["b_" + key] = row.pop(key)

    return list_of_dicts


def convert_to_dicts(data):
    """Converts the provided data to a list of dictionaries
    
    Args: 
        data (list, dict or df): List of records.
    
    Returns:
        data (list of dicts): Provided data converted to list of dictionaries.
    """

    if isinstance(data, dict):

        columns = data["columns"]
        rows = data["rows"]

        list_of_dicts = [dict(zip(columns, values)) for values in rows]

    elif isinstance(data, list):

        list_of_dicts = data

    elif isinstance(data, pd.DataFrame):

        # Only reset index if a named index exists
        if len(data.index.names) == 1 and data.index.name is None:
            pass
        else:
            data = data.reset_index()

        # Convert NaN to None. This is required because by default to_dict converts NaN to the string nan.
        data = data.replace({np.nan: None})
        list_of_dicts = data.to_dict("records")

    else:
        raise Exception(
            "The provided type for data is not supported ({})".format(type(data))
        )

    return list_of_dicts


def add_to_dicts(list_of_dicts, add_dict):
    """Add key/value set to all dictionaries in list
    
    Args: 
        list_of_dicts (list of dicts): List of dictionaries.
        add_dict (dict): Key/ values to add to the provided list of dictionaries
    
    Returns:
        list_of_dicts (list of dicts): Provided list of dictionaries with additional key/values sets.
    """

    for item in list_of_dicts:
        item.update(add_dict)

    return list_of_dicts
