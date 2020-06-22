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

PYMYSQL = "pymysql"


def patch_connect(adapter_name, module):
    def _connect(orig_func, patch_policy=None, *args, **kwargs):
        """Record DB inventory for MySQL"""
        try:
            context = contrast.CS__CONTEXT_TRACKER.current()
            if context is not None:
                db_inventory = dict(
                    adapter=adapter_name,
                    host=kwargs.get("host"),
                    port=kwargs.get("port"),
                    database=kwargs.get("db"),
                )
                InventoryUtils.append_db_config(context.activity, db_inventory)
        except Exception:
            logger.exception("Failed to add inventory for %s", adapter_name)

        return orig_func(*args, **kwargs)

    patch_cls_or_instance(module, "connect", _connect)


def instrument_pymysql(pymysql):
    """
    Note: Unlike other sql drivers, pymysql does not have an executescript method.
    """
    patch_connect(PYMYSQL, pymysql)
    dbapi2.instrument_cursor(PYMYSQL, pymysql.cursors.Cursor)


def register_patches():
    register_post_import_hook(instrument_pymysql, PYMYSQL)
