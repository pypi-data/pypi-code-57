""" Basic interface to a `PostgreSQL <https://www.postgresql.org/>`_ database.

The module consists of a main class :class:`Database <Database>` which
implements methods for connection and disconnection, table verification
and data insertion.

The database settings are set with a
:doc:`config file<../examples/conf/conf_database>`
and the standard library :obj:`configparser`.
"""

# Imports
import configparser
from os.path import abspath, expanduser
from enum import Enum

# Third party
from psycopg2 import (
    sql,
    Error as PSQL_Error,
    DatabaseError,
    IntegrityError,
    OperationalError,
    DataError,
    connect,
)
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT  # see https://stackoverflow.com/a/34484185

# Local packages
from lab_utils.custom_logging import getLogger


class DataType(Enum):
    """ List of accepted data types for new columns.
    The types are hard-coded for safety reasons: SQL
    insertions are potentially dangerous. See
    `here <https://www.postgresqltutorial.com/postgresql-data-types/>`_
    for more information.
    """

    bool = 'BOOLEAN'        #: Boolean
    short = 'SMALLINT'      #: Integer (2 bytes, range is -32,768 to +32,767)
    int = 'INTEGER'         #: Integer (4 bytes, range is -2,147,483,648 to +2,147,483,647)
    long = 'BIGINT'         #: Integer (8 bytes, range is -9,223,372,036,854,775,808 to +9,223,372,036,854,775,807)
    float = 'FLOAT(24)'     #: Floating-point number, 4 bytes
    double = 'FLOAT(53)'    #: Floating-point number, 8 bytes
    string = 'TEXT'         #: String, unlimited length
    time = 'TIMESTAMPTZ'    #: Time stamp, with time zone information

    def __str__(self) -> str:
        """ Parses the data type as an SQL string.

        Returns
        -------
        str
            The SQL query
        """
        return str(self.value)


class Constraint(Enum):
    """ List of accepted constraints for new columns.
    The constraints are hard-coded for safety reasons:
    SQL insertions are potentially dangerous.
    """
    positive = ''' CHECK({column_name} >= 0) '''            #: The variable must be greater or equal to 0
    positive_strict = ''' CHECK({column_name} > 0) '''      #: The variable must be strictly positive

    def __str__(self) -> str:
        """ Parses the constraint as an SQL string.

        Returns
        -------
        str
            The SQL query
        """
        return str(self.value)


class Database:
    """Manages connections and operations with a PostgreSQL database.
    The class is based on the :obj:`psycopg2` library and
    on this `tutorial
    <https://www.postgresqltutorial.com/postgresql-python/>`_.
    """

    host: str = 'localhost'         #: The host name where the database is located
    port: int = 5432                #: Connection port
    database: str = 'beam'          #: The database name to connect to
    user: str = 'cw-beam'           #: User name
    passfile: str = '~/.pgpass'     #: Location of the pgpass file with the credentials

    connection = None               #: Connection object returned by psycopg2.connect()
    db_version: str = ''            #: Database version
    cursor = None                   #: Cursor provided by connection.cursor() to execute an SQL query

    # List of predefined SQL queries
    _query_createDatabase = '''
        CREATE DATABASE {db_name}
        WITH OWNER %(owner)s
        ;
    '''
    _query_createTimeTable = '''
        CREATE TABLE {table_name} (
            time TIMESTAMPTZ NOT NULL {default}
        );
    '''
    _query_makeTimescaleHypertable = '''
        SELECT create_hypertable (
            %(table_name)s,
            %(key)s
        );
    '''
    _query_createAggregateView = '''
        CREATE VIEW {table_name}_10s
        WITH (timescaledb.continuous)
        AS
        SELECT
            time_bucket('10 s', time) as time,
            {aggregate_list}
        FROM
        {table_name}
        GROUP BY 1;
        
        
        CREATE VIEW {table_name}_1min
        WITH (timescaledb.continuous)
        AS
        SELECT
            time_bucket('1 min', time) as time,
            {aggregate_list}
        FROM
        {table_name}
        GROUP BY 1;
        
        
        CREATE VIEW {table_name}_10min
        WITH (timescaledb.continuous)
        AS
        SELECT
            time_bucket('10 min', time) as time,
            {aggregate_list}
        FROM
        {table_name}
        GROUP BY 1;
    '''
    _query_checkColumn = '''
        SELECT EXISTS
        (SELECT 1
        FROM information_schema.columns
        WHERE
        table_schema = %(table_schema)s
        AND
        table_name = %(table_name)s
        AND
        column_name = %(column_name)s
        );
    '''
    _query_checkTable = '''
        SELECT EXISTS
        (SELECT 1
        FROM information_schema.columns
        WHERE
        table_schema = %(table_schema)s
        AND
        table_name = %(table_name)s
        )
        ;
    '''
    _query_addColumn = '''
        ALTER TABLE {table_name}
        ADD COLUMN {column_name}
        {data_type}
        {checks}
        ;
    '''
    _query_insertData = '''
        INSERT INTO {table_name} ({columns})
        VALUES ({data})
        ;
    '''
    _query_retrieveViews = '''
        SELECT schemaname, viewname
        FROM pg_catalog.pg_views
        WHERE schemaname = 'public'
        ;
    '''
    _query_dropView = '''
        DROP VIEW {view}
        CASCADE;
    '''
    _query_retrieveColumns = '''
        SELECT attrelid::regclass AS tbl,
               attname            AS col,
               atttypid::regtype  AS datatype
        FROM   pg_attribute
        WHERE  attrelid = %(full_table_id)s::regclass
        AND    attnum > 0
        AND    NOT attisdropped
        ORDER  BY attnum;
     '''  # from https://dba.stackexchange.com/a/22420

    def __init__(self,
                 config_file: str = None,
                 host: str = None,
                 port: int = None,
                 database: str = None,
                 user: str = None,
                 passfile: str = None,
                 ):
        """ Initializes the :class:`Database` object. If a
        :paramref:`configuration file name<Database.__init__.config_file>`
        is given, the constructor calls the method
        :meth:`~.Database.config` and overrides the default attributes

        Parameters
        ----------
        config_file : str, optional
            Configuration file name, default is `None`. See
            :doc:`here<../../../examples/conf/conf_database>`
            for a configuration file example.

        host : str, optional
            Database host.

        port : int, optional
            Database port.

        database : str, optional
            Database name.

        user : str, optional
            Database user.

        passfile : str, optional
            Local file with PostgreSQL password.

        Raises
        ------
        :class:`configparser.Error`
            If a configuration file name was given, the method
            :meth:`config` can fail raising this exception.
        """

        # Read config file, if given
        if config_file is not None:
            self.config(config_file)

        # Override config file if other arguments are given
        if host is not None:
            self.host = host

        if port is not None:
            self.port = port

        if database is not None:
            self.database = database

        if user is not None:
            self.user = user

        if passfile is not None:
            self.passfile = abspath(expanduser(passfile))

    def __del__(self):
        """ Closes the connection to the database, if it was ever open.

        Raises
        ------
        :class:`psycopg2.Error`
            Base exception for all kind of database errors
        """
        self.close()

    def config(self, config_file: str):
        """ Loads the configuration.

        Reads the :paramref:`config_file` using the
        :obj:`configparser` library. The structure
        of the file is shown in the
        :ref:`examples section<configuration-files>`.

        Parameters
        ----------
        config_file : str
            Configuration file name.

        Raises
        ------
        :class:`configparser.Error`
            Error while parsing the file, e.g. no file was found,
            a parameter is missing or it has an invalid value.
        """

        try:
            # Expand configuration file path
            config_file = abspath(expanduser(config_file))
            getLogger().info("Loading configuration file %s", config_file)

            # Initialize config parser and read file
            config_parser = configparser.ConfigParser()
            config_parser.read(config_file)

            # Assign values to class attributes
            self.host = config_parser.get(section='Overall', option='host')
            self.port = config_parser.getint(section='Overall', option='port')
            self.database = config_parser.get(section='Overall', option='database')
            self.user = config_parser.get(section='Overall', option='user')
            self.passfile = config_parser.get(section='Overall', option='passfile')

            # Expand passfile path
            self.passfile = abspath(expanduser(self.passfile))

        except configparser.Error as e:
            getLogger().error("{}: {}".format(type(e).__name__, e))
            raise

        except BaseException as e:
            # Undefined exception, full traceback to be printed
            getLogger().exception("{}: {}".format(type(e).__name__, e))
            raise

        else:
            getLogger().info('Configuration loaded')

    def connect(self, print_version: bool = False):
        """ Connects to the database.

        If the connection was successful and the flag
        :paramref:`~Database.connect.print` was set, it also
        prints the database version as a connection check.

        Parameters
        ----------
        print_version : bool, optional
            Print the database version, default is 'False'.

        Raises
        ------
        :class:`psycopg2.Error`
            Base exception for all kind of database errors
        """
        getLogger().info(
            'Connecting to database <%s> on host <%s> over port <%d> as user <%s>',
            self.database,
            self.host,
            self.port,
            self.user
        )

        try:
            # Connect to the database
            self.connection = connect(
                dbname=self.database,
                user=self.user,
                host=self.host,
                port=self.port,
                passfile=self.passfile
            )

            # Read database version, serves as connection check
            self.cursor = self.connection.cursor()
            self.cursor.execute('SELECT version()')
            self.db_version = self.cursor.fetchone()

        except PSQL_Error as e:
            getLogger().error("{}: {}".format(type(e).__name__, e))
            raise

        except BaseException as e:
            # Undefined exception, full traceback to be printed
            getLogger().exception("{}: {}".format(type(e).__name__, e))
            raise

        else:
            if print_version:
                getLogger().info('Connection successful, database version: %s', self.db_version)
            else:
                getLogger().info('Connection successful')
                getLogger().debug('Database version: %s', self.db_version)

    def close(self):
        """ Closes the connection to the database.

        Raises
        ------
        :class:`psycopg2.Error`
            Base exception for all kind of database errors
        """

        # Close, if the connection had been opened
        if self.connection is not None:
            getLogger().info('Closing connection to database <%s>', self.database)
            try:
                self.connection.close()
            except PSQL_Error as e:
                getLogger().error("{}: {}".format(type(e).__name__, e))
                raise
            except BaseException as e:
                # Undefined exception, full traceback to be printed
                getLogger().exception("{}: {}".format(type(e).__name__, e))
                raise
            else:
                getLogger().info('Connection to database <%s> closed', self.database)
            finally:
                self.connection = None

    def create_database(self,
                        db_name: str,
                        owner: str = 'postgres',
                        ):
        """ Creates a database named
        :paramref:`~Database.create_database.db_name`. If
        :paramref:`~Database.create_database.timescaledb_extension`
        is set (default is 'True'), the TimescaleDB extension
        is installed in the database to allow TimescaleDB
        hypertables.

        Parameters
        ----------
        db_name : str
            The name of the database to be created

        owner : str, optional
            Database owner, default is 'postgres'.

        Raises
        ------
        :class:`psycopg2.Error`
            Base exception for all kind of database errors
        """

        logger = getLogger()

        # Check database status
        if self.connection is None:
            raise DatabaseError('Trying to access database without initialization')

        try:
            # Set autocommit level, see https://stackoverflow.com/a/34484185
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

            # Prepare query for table creation
            logger.info('Creating database <%s>', db_name)
            query = self._query_createDatabase.format(
                db_name=db_name
            )

            # Create the table table
            logger.debug('Query: %s', self.cursor.mogrify(query).decode())
            self.cursor.execute(
                query,
                {
                    'owner': owner
                }
            )
            self.connection.commit()
            logger.info('Database <%s> created', db_name)

        except PSQL_Error as e:
            logger.error("{}: {}".format(type(e).__name__, e))
            raise

        except BaseException as e:
            logger.exception("{}: {}".format(type(e).__name__, e))
            raise

    def create_timescale_db(self,
                            table_name: str,
                            default_now: bool = True):
        """ Creates a
        `TimescaleDB <https://docs.timescale.com/latest/main>`_ table.

        The table has a single column named 'time'
        with type 'TIMESTAMPTZ'. If the flag
        :paramref:`~Database.create_timescale_db.default_now`
        is set (default is 'True'), the column 'time'
        will default to 'NOW()'

        Parameters
        ----------
        table_name : str
            The name of the table to be checked
        default_now : bool, optional
            Set the 'time' column default to 'NOW()', default is `True`.

        Raises
        ------
        :class:`psycopg2.Error`
            Base exception for all kind of database errors
        """

        logger = getLogger()

        # Check database status
        if self.connection is None:
            raise DatabaseError('Trying to access database without initialization')

        try:
            # Prepare query for table creation
            if default_now:
                logger.info('Creating TimescaleDB table <%s> with default <time> NOW()', table_name)
                query = sql.SQL(self._query_createTimeTable.format(
                    table_name=table_name,
                    default=sql.SQL('DEFAULT NOW()').as_string(self.connection)
                ))
            else:
                logger.info('Creating TimescaleDB table <%s> without default <time>', table_name)
                query = sql.SQL(self._query_createTimeTable.format(
                    table_name=table_name,
                    default=''
                ))

            # Create the table
            logger.debug('Query: %s', self.cursor.mogrify(query).decode())
            self.cursor.execute(query)

            # Make the table a TimescaleDB Hypertable
            logger.debug('Sending query: %s', self.cursor.mogrify(
                self._query_makeTimescaleHypertable,
                {
                    'table_name':   table_name,
                    'key':          'time'
                }
            ).decode())
            self.cursor.execute(
                self._query_makeTimescaleHypertable,
                {
                    'table_name':   table_name,
                    'key':          'time'
                }
            )

            # Commit queries
            self.connection.commit()
            logger.info('TimescaleDB table <%s> created', table_name)

        except PSQL_Error as e:
            logger.error("{}: {}".format(type(e).__name__, e))
            raise

        except BaseException as e:
            logger.exception("{}: {}".format(type(e).__name__, e))
            raise

    def check_table(self, table_name) -> bool:
        """ Checks if a table exists.

        Parameters
        ----------
        table_name : str
            The name of the table to be checked

        Returns
        -------
        bool:
            `True` if the table exists, `False` otherwise.

        Raises
        ------
        :class:`psycopg2.Error`
            Base exception for all kind of database errors
        """

        logger = getLogger()

        # Check database status
        if self.connection is None:
            raise DatabaseError('Trying to access database without initialization')

        try:
            logger.debug('Checking if table <%s> exists', table_name)
            logger.debug('Query: %s', self.cursor.mogrify(
                self._query_checkTable,
                {'table_schema':    'public',
                 'table_name':      table_name,
                 }
            ).decode())
            self.cursor.execute(
                self._query_checkTable,
                {'table_schema':    'public',
                 'table_name':      table_name,
                 }
            )
            reply = self.cursor.fetchone()
            if reply[0]:
                logger.debug('Table <%s> does exist', table_name)
                return True
            else:
                logger.debug('Table <%s> does not exist', table_name)
                return False

        except PSQL_Error as e:
            logger.error("{}: {}".format(type(e).__name__, e))
            raise

        except BaseException as e:
            logger.exception("{}: {}".format(type(e).__name__, e))
            raise

    def check_column(self, table_name, column_name) -> bool:
        """ Checks if a column exists in a given table.

        Parameters
        ----------
        table_name : str
            The table where the column has to be checked
        column_name : str
            The column to be checked

        Returns
        -------
        bool:
            `True` if the column exists, `False` otherwise.

        Raises
        ------
        :class:`psycopg2.Error`
            Base exception for all kind of database errors
        """

        logger = getLogger()

        # Check database status
        if self.connection is None:
            raise DatabaseError('Trying to access a database without initialization')

        try:
            logger.debug('Checking if column <%s> exists in table <%s>', column_name, table_name)
            logger.debug('Query: %s', self.cursor.mogrify(
                self._query_checkColumn,
                {'table_schema':    'public',
                 'table_name':      table_name,
                 'column_name':     column_name,
                 }
            ).decode())
            self.cursor.execute(
                self._query_checkColumn,
                {'table_schema':    'public',
                 'table_name':      table_name,
                 'column_name':     column_name,
                 }
            )
            reply = self.cursor.fetchone()
            if reply[0]:
                logger.debug('Column <%s> does exist in table <%s>', column_name, table_name)
                return True
            else:
                logger.debug('Column <%s> does not exist in table <%s>', column_name, table_name)
                return False

        except PSQL_Error as e:
            logger.error("{}: {}".format(type(e).__name__, e))
            raise

        except BaseException as e:
            logger.exception("{}: {}".format(type(e).__name__, e))
            raise

    def new_column(
            self,
            table_name: str,
            column_name: str,
            data_type: DataType,
            constraints: list = None,
    ):
        """ Creates a new column in a given table.

        If the column already exists, it just returns.
        If the table does not exist or the column could not
        be created, it raises a :class:`psycopg2.Error`.

        Parameters
        ----------
        table_name : str
            Name of the table where the column has to be created
        column_name : str
            Name of the column to be created
        data_type : :class:`DataType`
            Data type of the new column
        constraints : list, optional
            List of :class:`Constraints<Constraint>`, default is 'None'

        Raises
        ------
        :class:`TypeError`
            Invalid constraint or data type
        :class:`ValueError`
            Invalid constraint or data type
        :class:`psycopg2.Error`
            Base exception for all kind of database errors
        """

        logger = getLogger()

        # Check database status
        if self.connection is None:
            raise DatabaseError('Trying to access database without initialization')

        # Check if the table exists
        if not self.check_table(table_name):
            raise IntegrityError(
                'Trying to create a column in table <%s>, which does not exist'.format(table_name))

        # Check if the column already exists
        if self.check_column(table_name, column_name):
            logger.info('Column <%s> already exists in table <%s>', column_name, table_name)
            return

        # Now let's send the SQL query
        logger.info('Creating column <%s> in table <%s>', column_name, table_name)
        try:
            if constraints is None:
                constraint_list = sql.SQL(' ')
            else:
                constraint_list = sql.SQL(' ').join(
                    sql.SQL(str(k).format(
                        table_name=table_name,
                        column_name=column_name,
                    )) for k in constraints
                )

            query = sql.SQL(self._query_addColumn.format(
                    table_name=table_name,
                    column_name=column_name,
                    data_type=str(data_type),
                    checks=constraint_list.as_string(self.connection),
                )
            )
            logger.debug('Query: %s', self.cursor.mogrify(query).decode())

            self.cursor.execute(query)
            self.connection.commit()

            # Check if the column was created
            if self.check_column(table_name, column_name):
                logger.info('Column <%s> successfully created in table <%s>', column_name, table_name)
            else:
                raise OperationalError(
                    'Column <%s> could not be created in table <%s>', column_name, table_name
                )

        except (PSQL_Error, TypeError, ValueError, KeyError) as e:
            logger.error("{}: {}".format(type(e).__name__, e))
            raise

        except BaseException as e:
            # Undefined exception, full traceback to be printed
            logger.exception("{}: {}".format(type(e).__name__, e))
            raise

    def new_entry(
            self,
            table_name: str,
            columns: list,
            data: list,
            check_columns: bool = False,
    ):
        """ Inserts data into a given table.

        See :doc:`this example<../../../examples/ex_database>`
        for usage examples

        Parameters
        ----------
        table_name : str
            Name of the table where the data has to be inserted
        columns : list[str]
            List of columns names corresponding to the data
        data : list
            Values of the new data entry
        check_columns : bool, optional
            Check that columns exist before insertion, default is False

        Raises
        ------
        :class:`TypeError`
            Invalid data
        :class:`ValueError`
            Invalid data
        :class:`psycopg2.Error`
            Base exception for all kind of database errors
        """

        logger = getLogger()

        if self.connection is None:
            raise DatabaseError('Trying to access database without initialization')

        # Check the list sizes are the same
        if len(data) != len(columns):
            raise DataError('Data and column lists have different sizes')

        # Check the list sizes are not zero
        if len(data) == 0:
            raise DataError('Empty data')

        logger.debug('Inserting data into table <%s>: ', table_name)
        for c, d in zip(columns, data):
            logger.debug('\t{:<25}{}'.format(c, d))

        # Check if the table and the columns exist
        if check_columns:
            if not self.check_table(table_name):
                raise IntegrityError(
                    'Table {} does not exist'.format(table_name))

            for column in columns:
                if not self.check_column(table_name, column):
                    raise IntegrityError('Column <%s> does not exist in table <%s>', column, table_name)

        # Now let's send the SQL query
        try:
            column_list = sql.SQL(', ').join(
                sql.Identifier(n) for n in columns
            )

            values_list = sql.SQL(', ').join(
                sql.Placeholder() for __ in columns
            )

            query = sql.SQL(self._query_insertData.format(
                    table_name=table_name,
                    columns=column_list.as_string(self.connection),
                    data=values_list.as_string(self.connection),
                )
            )
            logger.debug('Query: %s', self.cursor.mogrify(query, data).decode())

            self.cursor.execute(query, data)
            self.connection.commit()

        except (PSQL_Error, TypeError, ValueError) as e:
            logger.error("{}: {}".format(type(e).__name__, e))
            raise

        except BaseException as e:
            logger.exception("{}: {}".format(type(e).__name__, e))
            raise

        else:
            logger.debug('Data successfully committed')

    def create_aggregate_view(self,
                              table_name: str,
                              index_name: str = 'time',
                              recreate: bool = True,
                              ):
        """ Creates a set of
        `aggregate views <https://docs.timescale.com/latest/using-timescaledb/continuous-aggregates>`_
        in a given table.

        Parameters
        ----------
        table_name : str
            Name of the table where the column has to be created.


        index_name : str, optional
            Column to be used as index for the aggregate view, default is 'time'.

        recreate : bool, optional
            Recreate the aggregate view if it exists, default is 'True'.

        Raises
        ------
        :class:`psycopg2.Error`
            Base exception for all kind of database errors. In particular,
            it is raised if the table does not exist or the aggregate view
            could not be created.
        """

        logger = getLogger()

        # Check database status
        if self.connection is None:
            raise DatabaseError('Trying to access database without initialization')

        # Check if the table exists
        if not self.check_table(table_name):
            raise IntegrityError(
                'Trying to create aggregate views for table <{}>, which does not exist'.format(table_name))

        try:
            # Retrieve list of columns
            logger.debug('Retrieving list of columns from table <%s>', table_name)
            logger.debug('Query: %s', self.cursor.mogrify(
                self._query_retrieveColumns,
                {'full_table_id':    'public.{}'.format(table_name)}
            ).decode())
            self.cursor.execute(
                self._query_retrieveColumns,
                {'full_table_id':    'public.{}'.format(table_name)}
            )
            reply = self.cursor.fetchall()
            list_of_columns = [[row[1], row[2]] for row in reply]
            logger.debug('List of columns: %s', list_of_columns)

            # Check index column is present
            found = False
            for col in list_of_columns:
                if col[0] == index_name:
                    found = True
                    list_of_columns.remove(col)
                    break
            if not found:
                raise IntegrityError('Index column <{}> not found in table <{}>'.format(index_name, table_name))

            # Check that at least one numeric column was found
            valid_data_types = [
                'integer',
                'double precision',
                'real',
            ]

            found = False
            for col in list_of_columns:
                if col[1] in valid_data_types:
                    found = True
                    break
            if not found:
                raise IntegrityError('Cannot create an aggregate view without any column')

            # Create list of aggregates, picking only numeric variables
            aggregate_list = ', '.join(
               ['AVG({column_name}) AS {column_name}_avg'.format(column_name=col[0])
                for col in list_of_columns
                if col[1] in valid_data_types]
            )

            # Check if aggregate views already exist, and drop them
            if recreate:
                self.cursor.execute(self._query_retrieveViews)
                reply = self.cursor.fetchall()
                for view in [row[1] for row in reply]:
                    if table_name in view:
                        query = sql.SQL(self._query_dropView.format(
                            view=view,
                        ))
                        logger.debug('Dropping view <%s>', view)
                        logger.debug('Query: %s', self.cursor.mogrify(query).decode())
                        self.cursor.execute(query)

            # Create aggregate view
            query = sql.SQL(self._query_createAggregateView.format(
                table_name=table_name,
                aggregate_list=aggregate_list,
            ))
            logger.debug('Creating aggregate views')
            logger.debug('Query: %s', self.cursor.mogrify(query).decode())
            self.cursor.execute(query)
            self.connection.commit()

        except PSQL_Error as e:
            logger.error("{}: {}".format(type(e).__name__, e))
            raise

        except BaseException as e:
            logger.exception("{}: {}".format(type(e).__name__, e))
            raise
