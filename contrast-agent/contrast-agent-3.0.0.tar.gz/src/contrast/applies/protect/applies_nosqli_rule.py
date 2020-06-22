# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import json
import contrast
from contrast.extern import six
from contrast.utils.decorators import fail_safely

import logging

logger = logging.getLogger("contrast")


@fail_safely("Failed to convert nosql input to JSON")
def nosql_to_json(nosql):
    return json.dumps(nosql)


@fail_safely("Failed to run protect NoSQLi Rule")
def apply_rule(database, action, sql):
    context = contrast.CS__CONTEXT_TRACKER.current()

    if sql is None or context is None:
        return

    context.activity.query_count += 1
    context.activity.technologies[database] = True

    from contrast.agent.settings_state import SettingsState

    rule = SettingsState().defend_rules["nosql-injection"]

    if rule is None or not rule.enabled:
        logger.debug("No nosql-injection rule to apply!")
        return

    if not isinstance(sql, (str, bytes)):
        sql = nosql_to_json(sql)
        if sql is None:
            return

    log_sql_query(action, sql)

    return rule.infilter(context, sql, database=database)


@fail_safely("Failed to log query for protect NoSQLi Rule", log_level="debug")
def log_sql_query(action, sql_query):
    """
    Attempt to log the sql query but do not fail if unable to do so.
    """
    logger.debug(
        "Applying Nosql injection rule %s=%s",
        action,
        six.ensure_str(sql_query, errors="replace"),
    )
