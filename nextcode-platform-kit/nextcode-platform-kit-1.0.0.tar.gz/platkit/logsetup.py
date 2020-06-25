#!/usr/bin/env python

"""
Set up logging for the flask app via logstash-compatible json into file
"""

import os
import sys
import json
import uuid
import logging
import logging.config
from logging.handlers import WatchedFileHandler

from flask import request, current_app, g
from platkit.middleware.logstash_formatter import LogstashFormatterV1
from platkit.auth import unpack_user_jwt
import logging
import sentry_sdk

log = logging.getLogger("platkit")

JWT_FIELDS_TO_LOG = ["name", "email", "preferred_username", "jti"]


def setup(app):
    """Quick and dirty logstash-compliant logging implementation.
    app.log_formatter is modified in before_request to add context info.
    TODO: Allow logging to be fully configured via config file?
    """

    log_level = app.config.get("LOG_LEVEL", "INFO")
    log_dir = app.config.get("LOG_FOLDER", "/var/log/nextcode")
    log_filename = app.config.get("LOG_FILENAME")

    logger = logging.getLogger()
    formatter = LogstashFormatterV1()
    app.log_formatter = formatter

    # if we have no filename to log to we will direct the logs to stream
    if not log_filename:
        logger.setLevel(log_level)
        # make sure this is our only stream handler
        logger.handlers = []
        handler = logging.StreamHandler()
    else:
        logging.basicConfig(
            level=log_level, format="%(asctime)s - %(name)-14s %(levelname)-5s: %(message)s"
        )
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, log_filename)
        handler = WatchedFileHandler(log_path)

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # cut down noisy loggers
    logging.getLogger("boto3").setLevel(logging.WARNING)
    logging.getLogger("botocore").setLevel(logging.WARNING)

    @app.before_request
    def _setup_logging():
        return setup_logging(app)


def get_user_context():
    jwt_context = {}
    try:
        current_user = unpack_user_jwt() or {}
        for k, v in current_user.items():
            if k.lower() in set(JWT_FIELDS_TO_LOG):
                key = "{}".format(k)
                jwt_context[key] = v
    except Exception:
        pass
    return jwt_context


def get_log_defaults():
    defaults = {}

    defaults["build_info"] = current_app.config.get("BUILD_INFO")

    defaults["user"] = get_user_context()

    # add Client-Log-Context" request headers to the logs
    client = None
    try:
        client = request.headers.get("Client-Log-Context", None)
        defaults["client"] = json.loads(client)
    except Exception:
        defaults["client"] = client
    defaults["request"] = {
        "request_id": request.request_id,
        "url": request.url,
        "method": request.method,
        "remote_addr": request.remote_addr,
        "path": request.path,
        "user_agent": request.headers.get("User-Agent"),
    }
    defaults["request"].update(request.view_args or {})
    return defaults


def setup_logging(app):
    """Inject a tracking identifier into the request and set up context-info
    for all debug logs
    """
    g.log_defaults = None
    request_id = request.headers.get("Request-ID", None)
    if not request_id:
        default_request_id = str(uuid.uuid4())
        request_id = request.headers.get("X-Request-ID", default_request_id)
    request.request_id = request_id

    g.log_defaults = get_log_defaults()

    app.log_formatter.defaults.update(g.log_defaults)
    with sentry_sdk.configure_scope() as scope:
        scope.set_tag("request_id", request_id)
        scope.user = get_user_context()


def log_sentry(msg, *args, **kwargs):
    """Write a custom 'error' log event to sentry. Behaves like normal loggers
    Batches messages that have the same signature. Please use '"hello %s", "world"', not '"hello %s" % "world"'
    Example usage: log_sentry("Hello %s", "world", extra={"something": "else"})
    """
    try:
        # also log out an error for good measure
        log.error(msg, *args)
        if not current_app:
            return

        extra = kwargs.get("extra", {})
        if getattr(g, "log_defaults", None):
            extra.update(g.log_defaults)
        # get info on the caller
        f_code = sys._getframe().f_back.f_code
        extra["method"] = f_code.co_name
        extra["line"] = f_code.co_firstlineno
        extra["file"] = f_code.co_filename

        with sentry_sdk.push_scope() as scope:
            for k, v in extra.items():
                scope.set_extra(k, v)
            scope.level = "warning"
            sentry_sdk.capture_message(msg % args)

    except Exception as e:
        log.exception(e)
