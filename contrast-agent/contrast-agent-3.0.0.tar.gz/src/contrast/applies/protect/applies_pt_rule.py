# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import os

from contrast.extern import six

from contrast.agent.protect.rule.path_traversal_rule import PathTraversal
from contrast.utils.decorators import fail_safely

import logging

logger = logging.getLogger("contrast")


PARENT_CHECK = ".."
SLASH = "/"

SAFE_PATHS = ["tmp", "public", "docs", "static", "template", "templates"]


def possible_write(args, kwargs):
    if "w" in kwargs.get("mode", ""):
        return True

    return len(args) > 1 and args[1] is not None and "w" in args[1]


def get_user_input(args, kwargs):
    """
    io.open uses the kwarg file in both PY2/PY3
    builtin.open uses kwarg file in PY3 but kwarg name in PY2
    """
    if args:
        return args[0]
    if kwargs:
        return kwargs.get("file") or kwargs.get("name")


@fail_safely("Failed to run protect Path Traversal Rule")
def apply_rule(context, method, args, kwargs):
    """
    Find the user_supplied path among args or kwargs and run infilter.
    SecurityException will be thrown if an attacker is found

    :param context: RequestContext
    :param method: Method vulnerable to path traversal
    :param args: original method args, tuple
    :param kwargs: original method kwargs, dict
    """
    path = get_user_input(args, kwargs)

    if not path or not isinstance(path, six.string_types):
        return

    write = possible_write(args, kwargs)

    if six.PY2:
        # convert to str from unicode
        path = path.encode("utf-8")

    if not applies_to(path, write):
        return

    from contrast.agent.settings_state import SettingsState

    rule = SettingsState().defend_rules[PathTraversal.NAME]

    if not rule or not rule.enabled:
        return

    rule.infilter(context, path, method=method)


def applies_to(path, possible_write):
    # any write is a risk
    if possible_write:
        return True
    # check for moving up directory structure
    if path.find(PARENT_CHECK) > -1:
        return True

    if "/contrast/" in path or "/site-packages/" in path:
        return False

    if path.startswith(SLASH):
        for prefix in safer_abs_paths():
            if path.startswith(prefix):
                return False
    else:
        for prefix in SAFE_PATHS:
            if path.startswith(prefix):
                return False

    return True


def safer_abs_paths():
    pwd = os.getcwd()

    return ["{}/{}".format(pwd, item) for item in SAFE_PATHS] if pwd else []
