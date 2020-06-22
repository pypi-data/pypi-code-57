# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.extern import six
from contrast.utils.decorators import fail_safely

import logging

logger = logging.getLogger("contrast")


@fail_safely("Failed to run protect SQLi Rule")
def apply_rule(context, database, action, sql):
    if sql is None:
        return

    if not isinstance(sql, (str, bytes)):
        sql = str(sql)

    context.activity.query_count += 1
    context.activity.technologies[database] = True

    from contrast.agent.settings_state import SettingsState

    rule = SettingsState().defend_rules["sql-injection"]

    if rule is None or not rule.enabled:
        logger.debug("No sql-injection rule to apply!")
        return

    log_sql_query(action, sql)

    return rule.infilter(context, sql, database=database)


@fail_safely("Failed to log query for protect SQLi Rule", log_level="debug")
def log_sql_query(action, sql_query):
    """
    Attempt to log the sql query but do not fail if unable to do so.
    """
    logger.debug(
        "Applying sql injection rule %s=%s",
        action,
        six.ensure_str(sql_query, errors="replace"),
    )
