"""
Datatosk's main interface.

Examples:
    MySQL:
    >>> import datatosk
    >>> source = datatosk.mysql(source_name="dope_db")
    >>> source.read("SELECT * FROM dope_table")
       dope_column  other_dope_column
    0            1                  3
    1            2                  4
"""

from . import sources

# pylint: disable=invalid-name
mysql = sources.databases.mysql.MySQLSource
gbq = sources.databases.google_big_query.GBQSource
pickle = sources.files.PickleSource
requests = sources.network.RequestsSource
