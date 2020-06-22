# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import logging

logger = logging.getLogger("contrast")


from . import (
    cs_cstringio,
    cs_io,
    cs_open,
    os_patch,
    subprocess_patch,
    httplib_patches,
    xml_sax_patch,
    cs_logging,
    xml_pulldom_patch,
    cs_re,
    threading_patch,
    exec_and_eval,
    lxml_patch,
    pickle_patch,
    pycryptodome_patch,
    pyyaml_patch,
)
from .databases import (
    mongodb_patch,
    mysql_connector_patch,
    pymysql_patch,
    psycopg2_patch,
    pycassa_patch,
    sqlalchemy_patch,
    sqlite3_patch,
)


COMMON_PATCH_MODULES = (
    cs_open,
    xml_sax_patch,
    cs_logging,
    xml_pulldom_patch,
    threading_patch,
    lxml_patch,
    # pycrypto_patch,
    pycryptodome_patch,
    # pycryptodomex_patch,
    sqlalchemy_patch,
    # our sqlite3_patch also contains the import hook for pysqlite2.dbapi2
    sqlite3_patch,
    mysql_connector_patch,
    pymysql_patch,
    psycopg2_patch,
    pycassa_patch,
)


PROTECT_PATCH_MODULES = (
    # These patches are handled by policy on the assess side
    # TODO: These are good first candidates for protect policy
    os_patch,
    subprocess_patch,
    httplib_patches,
    mongodb_patch,
    pickle_patch,
    pyyaml_patch,
)


ASSESS_PATCH_MODULES = (
    cs_cstringio,
    cs_io,
    cs_re,
    exec_and_eval,
)


def register_module_patches(module, patch_group):
    logger.debug("registering %s patches for %s", patch_group, module.__name__)

    try:
        module.register_patches()
    except Exception:
        logger.exception("failed to register patches for %s", module.__name__)


def register_common_patches():
    for module in COMMON_PATCH_MODULES:
        register_module_patches(module, "common")


def register_protect_patches():
    for module in PROTECT_PATCH_MODULES:
        register_module_patches(module, "protect")


def register_assess_patches():
    for module in ASSESS_PATCH_MODULES:
        register_module_patches(module, "assess")
