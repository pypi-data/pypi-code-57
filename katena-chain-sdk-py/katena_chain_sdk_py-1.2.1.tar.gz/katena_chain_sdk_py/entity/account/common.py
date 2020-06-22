"""
Copyright (c) 2020, TransChain.

This source code is licensed under the Apache 2.0 license found in the
LICENSE file in the root directory of this source tree.
"""

NAMESPACE = "account"
TYPE_KEY = "key"
TYPE_COMPANY = "company"
TYPE_CREATE = "create"
TYPE_ROTATE = "rotate"
TYPE_REVOKE = "revoke"
DEFAULT_ROLE_ID = "default"
COMPANY_ADMIN_ROLE_ID = "company_admin"


def get_key_id_key() -> str:
    return "{}.{}".format(NAMESPACE, TYPE_KEY)


def get_key_create_v1_type() -> str:
    return "{}.{}.{}".format(get_key_id_key(), TYPE_CREATE, "v1")


def get_key_rotate_v1_type() -> str:
    return "{}.{}.{}".format(get_key_id_key(), TYPE_ROTATE, "v1")


def get_key_revoke_v1_type() -> str:
    return "{}.{}.{}".format(get_key_id_key(), TYPE_REVOKE, "v1")
