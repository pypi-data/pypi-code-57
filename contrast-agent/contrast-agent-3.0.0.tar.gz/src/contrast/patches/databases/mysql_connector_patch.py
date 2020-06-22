# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.extern.wrapt import register_post_import_hook

from contrast.patches.databases import dbapi2
from contrast.patches.databases.pymysql_patch import patch_connect


MYSQL_CONNECTOR = "mysql.connector"


def instrument_mysql_connector(mysql_connector):
    """
    Add patches for mysql.connector

    mysql.connector.cursor.MySQLCursor is the type returned by connect. However, we
    also patch mysql.connector.curstor.CursorBase just to cover our bases (ha!). This
    could potentially be useful if there are other cursor types that inherit
    CursorBase. However, patching that alone does not appear to be sufficient for
    instrumenting MySQLCursor, which is why we have both.
    """
    patch_connect(MYSQL_CONNECTOR, mysql_connector)

    dbapi2.instrument_cursor(MYSQL_CONNECTOR, mysql_connector.cursor.CursorBase)
    dbapi2.instrument_cursor(MYSQL_CONNECTOR, mysql_connector.cursor.MySQLCursor)


def register_patches():
    register_post_import_hook(instrument_mysql_connector, MYSQL_CONNECTOR)
