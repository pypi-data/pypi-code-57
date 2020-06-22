# import pyodbc 
import traceback
import pymysql
from .settings import Settings
from .helpers import Helpers
from datetime import datetime, timedelta





class _Model():
    DBConnection = None
    DBCursor = None
    __user: str
    __pass: str
    __database: str
    __host: str


    def __execute(self, query, retry = True):
        try:
            self.DBCursor.execute(query)
        except (pymysql.err.OperationalError, pymysql.err.InterfaceError) as e:
            self.console(f"An issue with the connection was identified.\nERR:{str(e)}\n\nTraceback:\n{traceback.format_exc()}")
            if retry:
                self.console(" - Attempting to resolve by rebooting connection... Standby...")
                self.__reconnect()
                self.console(f"Attempting to retry query:\n{query}")
                self.__execute(query, False)
                self.console("Query executed successfully.")
            else:
                self.console(f" - Was unable to resolve the issue, query cannot be executed. Query:\n{query}")
        except pymysql.Error as e:
            if e.args[0] == 2013 or e.args[0] == 2006:
                self.console(f"A timeout issue with the connection was identified.\nERR:{str(e)}\n\nTraceback:\n{traceback.format_exc()}")
                if retry:
                    self.console(" - Attempting to resolve by rebooting connection... Standby...")
                    self.__reconnect()
                    self.console(f"Attempting to retry query:\n{query}")
                    self.__execute(query, False)
                    self.console("Query executed successfully.")
                else:
                    self.console(f" - Was unable to resolve the issue, query cannot be executed. Query:\n{query}")
            else:
                self.console("An unexpected error occurred")
                self.console(traceback.format_exc())
                raise e

    def insert(self, query):
        """Insert data into the database"""
        self.DBCursor.execute(query)
        self.DBConnection.commit()

    def truncate(self, query):
        """Truncate a table in the database"""
        self.DBCursor.execute(query)
        self.DBConnection.commit()

    def update(self, query):
        """Insert data into the database"""
        self.DBCursor.execute(query)
        self.DBConnection.commit()
    
    def delete(self, query):
        """Delete data from the database"""
        self.DBCursor.execute(query)
        self.DBConnection.commit()

    def fetchOne(self, query):
        """Return the first record from the query"""
        self.__execute(query)
        self.DBConnection.commit()
        return self.DBCursor.fetchone()
    
    def fetchAll(self, query):
        """Return all records from the query"""
        self.__execute(query)
        self.DBConnection.commit()
        return self.DBCursor.fetchall()

    def get_timestamp_from_datetime(self, timestamp: datetime):
        """return a formatted date string for a given timestamp"""
        return Helpers().get_timestamp_from_datetime(timestamp)
        
    def get_timestamp(self):
        return Helpers().get_timestamp()
    
    def get_utc_timestamp(self):
        return Helpers().get_utc_timestamp()

    def utc_from_timestamp(self, utc_timestamp):
        return Helpers().utc_from_timestamp(utc_timestamp)

    def utc_from_timestamp_to_localtime_timestamp(self, utc_timestamp: str):
        return Helpers().utc_from_timestamp_to_localtime_timestamp(utc_timestamp)
    
    def sanitise(self, target):
        """Sanitise the input from undesirable data"""
        return target.replace("'", "''").replace("\"", "\"\"").replace("--", "- -")


    def console(self, message):
        print(f"[DB Connector]: {message}")


    def __init__(self, user, password, database="jarvis", host="127.0.0.1"):
        self.DBConnection = pymysql.connect(host=host, 
                                    charset='utf8mb4',
                                    user=user, 
                                    password=password, 
                                    db=database,
                                    connect_timeout=300,
                                    autocommit=True)
        self.DBCursor = self.DBConnection.cursor()
        self.__user = user
        self.__pass = password
        self.__database = database
        self.__host = host

    def __reconnect(self):
        self.DBConnection = pymysql.connect(host=self.__host, 
                                    charset='utf8mb4',
                                    user=self.__user, 
                                    password=self.__pass, 
                                    db=self.__database,
                                    connect_timeout=600,
                                    autocommit=True)
        self.DBCursor = self.DBConnection.cursor()



class Model(_Model):
    """Default Model Class for Jarvis, preconfigured"""
    def __init__(self, user=None, password=None, database="jarvis"):
        if user is None: 
            settings = Settings()
            user = settings.get_setting("database.user")
            password = settings.get_setting("database.pass")
            database = settings.get_setting("database.name")
        _Model.__init__(self, user, password, database=database)