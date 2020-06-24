import sqlalchemy as alc
import logging
import pandas as pd
import datetime as dt

class Session:
    def __init__(self, user, password, host, db='Test'):
        """ Initialize connection to database

            args:
                user ---- name of user to connect as
                password ---- password for specified user
                host ---- host ip to connect to

            kwargs:
                db ---- database to connect to (defaults to test)
        """
        self.engine = alc.create_engine("mysql+pymysql://{}:{}@{}/{}".format(user, password, host, db), echo=True)

        self.meta = alc.MetaData(self.engine)

        self.conn = self.engine.connect()

        self.type_dict = {float : alc.types.Float, int : alc.types.Integer, str : alc.types.String(length=32)}

    def execute_SQL(self, filename):
        """ execute .SQL file of commands 
        
            args:
                filename ---- path of file to execute (must be .sql)
        """

        # open file

        file = open(filename, 'r', encoding='utf-8-sig')
        sql = file.read()
        file.close()

        # get commands
        commands = sql.split(';')
        commands.pop()
        
        results = []

        # execute commands
        for command in commands:
            command = command.strip()
            try:
                results.append(self.conn.execute(alc.sql.text(command)))
            except:
                logging.error('Operation \"' + command + '\" failed, skipping...')

        return results

    def insert(self, table, columns, rows):
        """ insert given rows into given table.
            Creates table if it doesn't already exist.
        
            args:
                table ---- name of table to insert into
                columns ---- list of column names
                rows ---- list of lists of values to put into corresponding columns

                len(columns) MUST EQUAL len(rows)
        """

        types = []
        for item in rows[0]:
            type(item)

        # create dataframe
        df = pd.DataFrame(data=rows, columns=columns)

        # if table doesn't exist, create
        if not self.engine.has_table(table):
            self.create_table(table, columns, types)
        
        # insert
        try:
            df.to_sql(table, self.conn, if_exists='append', index=False)
        except ValueError as e:
            print(e)
            quit()

    def insert_from_CSV(self, filename, table):
        """ Inserts entire CSV file into specified table.
            Creates table if it doesn't already exist.

            args:
                filename ---- file path of data to upload
                table ---- name of table to insert into

        """

        # create 
        df = pd.read_csv(filename)

        types = []
        print(df.iloc[0])
        for item in df.iloc[0]:
            types.append(type(item))

        print(types)

        if not self.engine.has_table(table):
            self.create_table(table, df.columns, types)

        try:
            df.to_sql(table, self.engine, if_exists='append', index=False)
        except ValueError as e:
            print(e)
            quit() 

    def create_table(self, table, columns, types):
        """ create table from given dataframe

            args:
                dataframe ---- dataframe to base table off of
        """
        
        # create table with dataframe data
        sql_table = alc.Table(
            table, self.meta,
            alc.Column('id', alc.Integer, primary_key=True),
            *(alc.Column(column_name, self.type_dict[column_type]) for column_name, column_type in zip(columns, types)))

        # create table in database
        self.meta.create_all(self.engine)