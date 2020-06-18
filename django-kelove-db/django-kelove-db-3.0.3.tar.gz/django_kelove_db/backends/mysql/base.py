"""
MySQL database backend for Django.
"""

from django.db.backends.mysql.base import *

from .schema import DatabaseSchemaEditor as MySqlDatabaseSchemaEditor


class DatabaseWrapper(DatabaseWrapper):
    SchemaEditorClass = MySqlDatabaseSchemaEditor
