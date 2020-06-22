# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.extern.wrapt import register_post_import_hook

import contrast
from contrast.patches.databases import dbapi2
from contrast.utils.inventory_utils import InventoryUtils
from contrast.utils.patch_utils import patch_cls_or_instance

import logging

logger = logging.getLogger("contrast")


SQLITE3 = "sqlite3"
PYSQLITE2_DBAPI2 = "pysqlite2.dbapi2"


def patch_connect(adapter_name, module):
    def _connect(orig_func, patch_policy=None, *args, **kwargs):
        """Record DB inventory for SQLite3 connection"""
        try:
            context = contrast.CS__CONTEXT_TRACKER.current()
            if context is not None:
                # sqlite does not use a server, so no need for host/port
                database = kwargs.get("database") or (
                    args[0] if len(args) > 0 else "unknown"
                )
                db_inventory = dict(adapter=adapter_name, database=database)
                InventoryUtils.append_db_config(context.activity, db_inventory)
        except Exception:
            logger.exception("Failed to add inventory for %s", adapter_name)

        return orig_func(*args, **kwargs)

    patch_cls_or_instance(module, "connect", _connect)


def instrument_sqlite_dbapi2(sqlite3):
    dbapi2.instrument_cursor(SQLITE3, sqlite3.Cursor)
    dbapi2.instrument_executescript(SQLITE3, sqlite3.Cursor)
    patch_connect(SQLITE3, sqlite3)


def instrument_pysqlite2_dbapi2(pysqlite2):
    """Supports the older pysqlite module in Py2"""
    dbapi2.instrument_cursor(PYSQLITE2_DBAPI2, pysqlite2.Cursor)
    dbapi2.instrument_executescript(PYSQLITE2_DBAPI2, pysqlite2.Cursor)
    patch_connect(PYSQLITE2_DBAPI2, pysqlite2)


def register_patches():
    register_post_import_hook(instrument_sqlite_dbapi2, SQLITE3)
    register_post_import_hook(instrument_pysqlite2_dbapi2, PYSQLITE2_DBAPI2)
