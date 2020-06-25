#!/usr/bin/env python

import os
from datetime import date
import logging
from http import HTTPStatus

import yaml
from pathlib import Path
from decouple import AutoConfig
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.backends import default_backend

from flask import current_app, url_for
from flask.json import JSONEncoder
from flask_restx import abort

log = logging.getLogger(__name__)


class CustomJSONEncoder(JSONEncoder):
    """Extend the JSON encoder to treat date-time objects as strict
    rfc3339 types.
    """

    def default(self, obj):  # pylint: disable=E0202
        if isinstance(obj, date):
            return obj.isoformat() + "Z"
        # backwards-compatibility fix for models
        elif hasattr(obj, "as_dict"):
            return obj.as_dict()
        else:
            return JSONEncoder.default(self, obj)


def get_build_info(root_path):
    """Return build info from package yaml file called .build_info.yml which is generated from the
    build process and at the very least return the version from the package..
    """
    directory = os.path.dirname(root_path)
    parent_directory = os.path.abspath(os.path.join(directory, ".."))
    version = None
    version_filename = os.path.join(parent_directory, "VERSION")

    # backwards compatibility
    if not os.path.exists(version_filename):
        version_filename = os.path.join(directory, "VERSION")
    try:
        with open(version_filename, "r") as f:
            version = f.readline().strip()
    except Exception:
        pass
    ret = {}
    build_info_path = os.path.join(parent_directory, ".build_info.yml")
    try:
        with open(build_info_path) as build_info_file:
            ret = yaml.safe_load(build_info_file) or {}
    except Exception:
        pass
    ret["version"] = version
    return ret


def get_autoconfig(path):
    """Utility method to wrap autoconfig from settings file one folder up from the __file__ caller
    """
    base_dir = Path(os.path.abspath(path)).parent.parent
    ret = AutoConfig(str(base_dir))
    return ret


def unpack_user_jwt():
    # for temporary backwards-compatibility
    from platkit.auth import unpack_user_jwt as _unpack_user_jwt

    return _unpack_user_jwt()


def get_root_endpoints():
    """
    Returns a dictionary of endpoints (usually resource collections) that should
    be exposed in the root endpoint in a consistent way between services.
    To use this add `root_endpoint = True` to your endpoint class
    """

    # default endpoints for all services
    endpoints = {
        "documentation": url_for("api.specs", _external=True),
        "swaggerui": url_for("api.doc", _external=True),
    }
    for k, v in current_app.view_functions.items():
        if hasattr(v, "view_class") and getattr(v.view_class, "root_endpoint", False):
            endpoints[v.__name__.split("_")[1]] = url_for(k, _external=True)
    return endpoints


def format_public_key(key):
    """
    format a pem public key correctly in a multiline format that the ssl library expected with
    correct header/footer and each line no more than 80 characters
    this method performs no validation on the public key and any ssh-formatted key
    is returned unchanged.
    The input key can include header/footer or it will be added.
    """
    if not key or key.startswith("ssh "):
        return key
    chunk_size = 79
    BEGIN_MARKER = "-----BEGIN PUBLIC KEY-----"
    END_MARKER = "-----END PUBLIC KEY-----"
    ret = key.replace("\\n", "").replace("\n", "").replace(BEGIN_MARKER, "").replace(END_MARKER, "")
    lst = [ret[i : i + chunk_size] for i in range(0, len(ret), chunk_size)]
    lst.insert(0, BEGIN_MARKER)
    lst.append(END_MARKER)
    ret = "\n".join([l for l in lst if l])
    return ret


def check_database(session, table=None):
    # Check whether database is reachable and contains objects
    try:
        if table:
            sql = f"COMMIT; SELECT * FROM {table} LIMIT 1;"
        else:
            sql = "COMMIT; SELECT current_date"
        session.execute(sql)
    except Exception as e:
        log.exception("Error communicating with database: %s", e)
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, message="Database is not reachable: {0}".format(e))


def check_public_key():
    # Check if public key is valid
    if not current_app.config.get("SKIPAUTH"):
        public_key = current_app.config.get("PUBLIC_KEY")
        if not public_key.startswith("ssh ") and public_key.replace("\n", "").count("PUBLIC") != 2:
            log.exception("PUBLIC_KEY is malformed: %s", public_key)
            abort(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                message="Config is invalid: Public key is malformed",
                PUBLIC_KEY=public_key,
            )
        try:
            load_pem_public_key(public_key.encode(), backend=default_backend())
        except ValueError:
            log.exception("PUBLIC_KEY could not be loaded: %s", public_key)
            abort(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                message="Config is invalid: Public key could not be loaded",
                PUBLIC_KEY=public_key,
            )
