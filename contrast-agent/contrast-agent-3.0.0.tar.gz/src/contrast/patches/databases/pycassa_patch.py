# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""
Patches and rule applicators for Cassandra

Cassandra is sufficiently different from our other SQL databases that custom
rule applicators have been implemented here.
"""
import logging

from contrast.extern.wrapt import register_post_import_hook

import contrast
from contrast.agent.assess.policy.methods import skip_analysis
from contrast.agent.settings_state import SettingsState
from contrast.applies import DATABASE_CASSANDRA
from contrast.applies.sqli import assess_rule
from contrast.applies.protect.applies_sqli_rule import log_sql_query
from contrast.utils.decorators import fail_safely
from contrast.utils.inventory_utils import InventoryUtils
from contrast.utils.patch_utils import patch_cls_or_instance


logger = logging.getLogger("contrast")


PYCASSA = "pycassa"

GET = "get"
INIT = "__init__"
INSERT = "insert"
MULTIGET = "multiget"
REMOVE = "remove"

COLUMNS = "columns"

# This is the default host/port pycassa uses
DEFAULT_DB = "localhost:9160"


def _extract_cql_vectors(method_name, args, kwargs):
    """
    Extract vectors for analysis from pycassa method call args/kwargs
    """
    if method_name == "get":
        return [args[1]] + kwargs.get(COLUMNS, [])
    if method_name == "insert":
        return [args[1]] + list(args[2].keys()) + list(args[2].values())
    if method_name == "multiget":
        return args[1] + kwargs.get(COLUMNS, [])
    if method_name == "remove":
        return [args[1]] + kwargs.get(COLUMNS, [])

    raise ValueError("Invalid cql method name: " + method_name)


@fail_safely("Error running Cassandrda SQLi protect rule")
def _protect_rule(context, method_name, args, kwargs):
    """
    Apply SQLi protect rule for Cassandra
    """
    context.activity.query_count += 1
    context.activity.technologies[DATABASE_CASSANDRA] = True

    rule = SettingsState().defend_rules["sql-injection"]

    if rule is None or not rule.enabled:
        logger.debug("No sql-injection rule to apply!")
        return

    try:
        cql_vectors = _extract_cql_vectors(method_name, args, kwargs)
    except Exception as e:
        # This is not necessarily an error: it could be caused if the
        # application passes arguments to pycassa incorrectly.
        logger.warning(
            "Failed to extract cql vectors from pycassa query: %s",
            method_name,
            exc_info=e,
        )
        return

    for vector in cql_vectors:
        log_sql_query(method_name, vector)
        rule.infilter(context, vector, database=DATABASE_CASSANDRA)


def apply_rule(method_name, orig_func, args, kwargs):
    """
    Top-level SQLi rule applicator for Cassandra
    """
    context = contrast.CS__CONTEXT_TRACKER.current()

    if context is not None and SettingsState().is_protect_enabled():
        _protect_rule(context, method_name, args, kwargs)

    try:
        result = orig_func(*args, **kwargs)
    except Exception:
        result = None
        raise
    finally:
        if not skip_analysis(context):
            assess_rule(context, PYCASSA, method_name, result, args, kwargs)

    return result


def get(original_get, patch_policy=None, *args, **kwargs):
    """
    This method checks for vulnerabilities and sql injection in get calls to Cassandra
    Arg[0]: ColumnFamily object
    Arg[1]: key to table
    kwarg['columns']: columns in family to retrieve

    Example method call:
        result = self.cf.get('test_table', columns=['name'])
    """
    return apply_rule(GET, original_get, args, kwargs)


def insert(original_insert, patch_policy=None, *args, **kwargs):
    """
    This method checks for vulnerabilities and sql injection in inset calls to Cassandra
    Arg[0]: ColumnFamily object
    Arg[1]: key to table
    Arg[2]: dict of items to insert

    Example method call:
        result = self.cf.insert('test_table', {'name': 'tim'})
    """
    return apply_rule(INSERT, original_insert, args, kwargs)


def multiget(original_multiget, patch_policy=None, *args, **kwargs):
    """
    This method checks for vulnerabilities and sql injection in multiget calls to Cassandra
    Arg[0]: ColumnFamily object
    Arg[1]: key to table
    kwarg['columns']: columns in family to retrieve

    Example method call:
        result = self.cf.get('test_table', columns=['name'])
    """
    return apply_rule(MULTIGET, original_multiget, args, kwargs)


def remove(original_remove, patch_policy=None, *args, **kwargs):
    """
    This method checks for vulnerabilities and sql injection in remove calls to Cassandra
    Arg[0]: ColumnFamily object
    Arg[1]: key to table
    kwarg['columns']: columns in family to retrieve

    Example method call:
        result = self.cf.get('test_table', columns=['name'])
    """
    return apply_rule(REMOVE, original_remove, args, kwargs)


def init(orig_init, patch_policy=None, *args, **kwargs):
    """
    Patch for ConnectionPool.__init__ used for inventory reporting
    """
    try:
        context = contrast.CS__CONTEXT_TRACKER.current()
        if context is not None:
            # TODO: `server_list` is a list of strings that indicate host:port
            # combinations for RPC connections. Right now we're being a bit
            # cheap and simply reporting a stringified version of the list if
            # it exists, or just the pycassa default otherwise. However, it
            # might make more sense in the future to iterate over `server_list`
            # and parse it into host and port and to report a db config for
            # each. Since we currently don't have a great idea of how this is
            # actually used, we'll do the simple thing for now.
            database = str(kwargs.get("server_list", DEFAULT_DB))
            db_inventory = dict(adapter=PYCASSA, database=database)
            InventoryUtils.append_db_config(context.activity, db_inventory)
    except Exception:
        if context is not None:
            logger.exception("Failed to add inventory for pycassa")

    return orig_init(*args, **kwargs)


def instrument_pycassa(pycassa_module):
    patch_cls_or_instance(pycassa_module.pool.ConnectionPool, INIT, init)
    patch_cls_or_instance(pycassa_module.columnfamily.ColumnFamily, GET, get)
    patch_cls_or_instance(pycassa_module.columnfamily.ColumnFamily, INSERT, insert)
    patch_cls_or_instance(pycassa_module.columnfamily.ColumnFamily, MULTIGET, multiget)
    patch_cls_or_instance(pycassa_module.columnfamily.ColumnFamily, REMOVE, remove)


def register_patches():
    register_post_import_hook(instrument_pycassa, PYCASSA)
