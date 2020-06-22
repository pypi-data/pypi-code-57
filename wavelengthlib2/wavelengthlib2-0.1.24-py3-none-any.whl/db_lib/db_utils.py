''' 
    db_utils.py is a set of utility functions and a class intended for SQL Server DB access
    The SQLDBConn class requires an instance of WLAppEnv or WLAzAppEnv to be past to its constructor
'''  
import pyodbc
import pandas as pd
from datetime import datetime
import calendar

def get_sql_formatted_datetime(dt):
    ''' Get a SQL acceptable datetime string given a python datetime type (uo to miliseconds)

    Args:
        dt (datetime): datetime to be converted
        
    Returns:
        sql datetime sting
    '''  
    return f'{dt.day}-{calendar.month_name[dt.month][0:3]}-{dt.year} {dt.hour}:{dt.minute}:{dt.second}.{round(dt.microsecond/1000.0)}'

def get_sql_formatted_date(dt):
    ''' Get a SQL acceptable date string given a python date 

    Args:
        dt (date): date to be converted
        
    Returns:
        sql date sting
    '''  
    return f'{dt.day}-{calendar.month_name[dt.month][0:3]}-{dt.year}'

def sql_strfield_arg(arg_obj):
    ''' Take a native python type and return a string representation of it which is 
        acceptable as an argument to a stored procedure or function in SQL 

    Args:
        arg_obj (native python type): argument object
        
    Returns:
        sql arg sting
    '''  
    if arg_obj is None:
        sql_arg_str = 'NULL'
    else:
        if isinstance(arg_obj, str):
            if str.strip(arg_obj) == '':
                sql_arg_str = 'NULL'
            else:
                sql_arg_str = '\'' + (str.strip(arg_obj)).replace('\'','\'\'') + '\''
        elif isinstance(arg_obj, int):
            sql_arg_str = str(arg_obj)
        elif isinstance(arg_obj, datetime):
            sql_arg_str = '\'' + get_sql_formatted_datetime(arg_obj) + '\''
        elif isinstance(arg_obj, float):
            sql_arg_str = str(arg_obj)
        else:
            sql_arg_str = str(arg_obj)
    return sql_arg_str

class SQLDBConn:

    def __init__(self, app_env, db_name=None):
        ''' Initialise SQL DB connection.
            Uses app_env to get connection string info.
            Success or otherwise of DB connection is written to the app_env log

        Args:
            n/a
            
        Returns:
            n/a
        '''  
        self.env = app_env
        self.server = app_env.get_parameter('DBServer')
        if db_name:
            self.database = db_name
        else:
            self.database = app_env.get_parameter('DataBase')
        self.driver =  app_env.get_parameter('DBDriver')
        self.authmode = app_env.get_parameter('DBAuthMode')
        self.is_connected = False

        if self.authmode == 'TRUSTED':
            db_conn_str = r'Driver='+self.driver+';Server='+self.server+';Database='+self.database+';Trusted_Connection=yes;'
        else:
            usr = app_env.get_parameter('DBusername')
            pwd = app_env.get_parameter('DBpwd')
            db_conn_str = r'DRIVER='+self.driver+';SERVER='+self.server+';PORT=1433;DATABASE='+self.database+';UID='+usr+';PWD='+ pwd

        self.env.log_message(f'Connecting with [{db_conn_str}]')
        try:
            self.db_connection = pyodbc.connect(db_conn_str)
            self.is_connected = True
        except pyodbc.Error as ex:
            sqlstate = ex.args[1]
            self.is_connected = False
        
        if self.is_connected:
            self.env.log_message('Connected to SQL Server successfully')
        else:
            self.env.log_message(f'Failed to conect to SQL Server - [{sqlstate}]')

        return

    def conn_ok(self):
        return self.is_connected

    def get_connection(self):
        return self.db_connection

    def execute_stored_proc(self, proc_name, arg_list):
        ''' Execute a SQL stored procedure and return the result
            Only intended for use with stored procedures which update data, 
            use fetch_sql_query() instead for stored procedures which simply fetch data
            Assumes that all stored procedures have a last arument as an OUTPUT argument 
            containing error messages and they retrun an int status value

        Args:
            proc_name (str): the name of the stored procedure
            arg_list (list): the list of the stored procedure arguments (must not include OUTPUT last argument)
            
        Returns:
            (return_status,return_error) (tuple): 
                return_status (int) : >= 0 for success <0 for failure
                return_error (str): '' for success and containing an error message if failed
        '''  
        if self.is_connected:
            sql_arg_list = []
            for arg in arg_list:
                sql_arg_list.append(sql_strfield_arg(arg))
            arg_str = ','.join(sql_arg_list)

            sql_proc_stmt = f'exec @ret = {proc_name} {arg_str},@err OUTPUT; '
            #print(f'sql_proc_stmt={sql_proc_stmt}')
            sql_proc_top = 'declare @ret int, @err varchar(255); '
            sql_tail_tail = 'select @ret as StatusReturn, @err as ErrorMessage;'

            sql_command = sql_proc_top + sql_proc_stmt + sql_tail_tail
            
            cursor = self.db_connection.cursor()
            cursor.execute(sql_command)
            while 1:
                row = cursor.fetchone()
                if row is not None:
                    return_status = row[0]
                    return_error = row[1]                
                else:               
                    break

            self.db_connection.commit()
        else:
            return_status = -1
            return_error = 'DB not connected.'

        return (return_status,return_error)

    def fetch_sql_query(self,sql_query):
        ''' Execute a SQL query which fetches data and return the result as a dataframe
            The SQL query must only return a single dataset result

        Args:
            sql_query (str): the SQL query string
            
        Returns:
            ret_df (dataframe): the query result data set
        '''  
        if self.is_connected:
            cursor = self.db_connection.cursor()
            cursor.execute(sql_query)
            dataset = cursor.fetchall()
            dataset_info = cursor.description
            query_cols = []
            for col in dataset_info:
                query_cols.append(col[0])
            ret_df = pd.DataFrame.from_records(dataset, columns = query_cols)
        else:
            ret_df = None
        return ret_df

    def disconnect(self):
        ''' Disconnect from the database. Use when finished querying otherwise connection will remain.
            Write outcome to app_env log
        '''  
        if self.is_connected:
            self.env.log_message('Disconnecting from SQL Server')
            self.db_connection.close()
            self.is_connected = False
        else:
            self.env.log_message('Cannot disconnect from DB as not currently connected.')
        return

    def __del__(self):
        ''' Code added to class destructor to make sure that instances of this object
            disconnect from the DB when they go out of scope
        '''  
        if self.is_connected:
            self.env.log_message('Disconnecting from SQL Server')
            self.db_connection.close()
            self.is_connected = False
        return