# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from functools import partial

from contrast.extern.wrapt import register_post_import_hook

from contrast.applies import DATABASE_SQL_ALCHEMY
from contrast.applies.common.applies_sqli_rule import apply_rule_sqlalchemy
from contrast.utils.patch_utils import patch_cls_or_instance

EXECUTE = "execute"
FROM_STATEMENT = "from_statement"

ORM_MODULE = "sqlalchemy.orm"
SESSION_MODULE = "{}.session".format(ORM_MODULE)
SCOPING_MODULE = "{}.scoping".format(ORM_MODULE)

ENGINE_BASE_MODULE = "sqlalchemy.engine.base"


def execute(orig_func, patch_policy=None, *args, **kwargs):
    """
    This patch gives us coverage in applications that are using SQLAlchemy
    where we may not necessarily support the underlying database but still
    need to test for SQL injection attacks that involve raw database
    queries.
    """
    # check if original function is a module-level function or bound method
    if not bool(getattr(orig_func, "__self__", None)):
        self = args[0]
        orig_func = partial(orig_func, self)
        args = args[1:]
    else:
        self = None

    return apply_rule_sqlalchemy(
        DATABASE_SQL_ALCHEMY, EXECUTE, orig_func, args[0], self, args, kwargs
    )


def patch_sqlalchemy_base_execute(query_module):
    patch_cls_or_instance(query_module.Connection, EXECUTE, execute)


def patch_sqlalchemy_scoping(scoping_module):
    patch_cls_or_instance(scoping_module.scoped_session, EXECUTE, execute)


def register_patches():
    register_post_import_hook(patch_sqlalchemy_base_execute, ENGINE_BASE_MODULE)
    register_post_import_hook(patch_sqlalchemy_scoping, SCOPING_MODULE)
