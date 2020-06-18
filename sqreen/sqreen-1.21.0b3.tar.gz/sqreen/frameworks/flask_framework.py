# -*- coding: utf-8 -*-
# Copyright (c) 2016 - 2020 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#
""" Flask specific WSGI HTTP Request / Response stuff
"""

import sys
from logging import getLogger
from traceback import format_stack

from ..utils import to_unicode_safe
from .base import BaseResponse
from .wsgi import BaseWSGIRequest

if sys.version_info[0] >= 3:
    import urllib.parse as urlparse
else:
    import urlparse


LOGGER = getLogger(__name__)


class FlaskRequest(BaseWSGIRequest):

    def __init__(self, request, storage=None):
        super(FlaskRequest, self).__init__(storage=storage)
        self.request = request

        # Cache for params
        self._query_params = None
        self._form_params = None
        self._cookies_params = None
        self._json_params = None

    def preload_data(self):
        """ Some Flask properties consume the stream without keeping
        a cache of the input data. We must call preload_data first,
        otherwise get_json will eventually fail.
        """
        if hasattr(self.request, "_cached_data"):
            return True
        length = self.content_length
        # Safety, do not preload data if the body is too heavy
        # XXX: this should be a parameter.
        if length is None or length > (1024 * 1024):  # 1MB
            return False
        try:
            # Fill request._cached_data
            self.request.get_data()
            if self.is_flask_api:
                # Flask-API redefines several properties such as data and form
                # but they all depend on the _stream attribute. We reset it
                # in order to allow further input processing by the framework.
                self.request._stream = self.request._get_stream_for_parsing()
        except Exception:
            LOGGER.debug("couldn't get request.data from the framework",
                         exc_info=True)
            return False
        else:
            return True

    @property
    def query_params(self):
        if self._query_params is None:
            try:
                # Convert flask QueryDict to a normal dict with values as list
                self._query_params = dict(self.request.args.lists())
            except Exception:
                LOGGER.debug("couldn't get request.args from the framework",
                             exc_info=True)
                self._query_params = super(FlaskRequest, self).query_params
        return self._query_params

    @property
    def body(self):
        """ Get the HTTP input body from the framework cache or the
        WSGI input preview.
        """
        try:
            if self.preload_data():
                return self.request.get_data()
        except Exception:
            LOGGER.debug("couldn't get request.data from the framework",
                         exc_info=True)
        return super(FlaskRequest, self).body

    @property
    def form_params(self):
        if self._form_params is None:
            try:
                if self.preload_data():
                    self._form_params = dict(self.request.form.lists())
                    return self._form_params
            except Exception:
                LOGGER.debug("couldn't get request.form from framework",
                             exc_info=True)
            self._form_params = super(FlaskRequest, self).form_params
        return self._form_params

    @property
    def cookies_params(self):
        if self._cookies_params is None:
            try:
                self._cookies_params = dict(self.request.cookies)
            except Exception:
                LOGGER.debug("couldn't get request.cookies from framework",
                             exc_info=True)
                self._cookies_params = super(FlaskRequest, self).cookies_params
        return self._cookies_params

    @property
    def json_params(self):
        if self._json_params is None:
            try:
                if self.preload_data():
                    self._json_params = self.request.get_json(silent=True)
                    return self._json_params
            except Exception:
                LOGGER.debug("couldn't get request.json from the framework",
                             exc_info=True)
            self._json_params = super(FlaskRequest, self).json_params
        return self._json_params

    @property
    def remote_addr(self):
        """Remote IP address."""
        return to_unicode_safe(self.get_raw_header("REMOTE_ADDR"))

    @property
    def hostname(self):
        try:
            url = self.request.url_root
            return urlparse.urlparse(url).netloc
        except Exception:
            LOGGER.debug("couldn't get request.get_host from the framework",
                         exc_info=True)
            return None

    @property
    def method(self):
        return to_unicode_safe(self.request.method)

    @property
    def referer(self):
        return self.request.referrer

    @property
    def client_user_agent(self):
        return to_unicode_safe(self.request.user_agent.string)

    @property
    def route(self):
        """Request route."""
        url_rule = getattr(self.request, "url_rule", None)
        # If a custom rule_class is used in the app, the rule attribute might
        # be missing.
        return getattr(url_rule, "rule", None)

    @property
    def path(self):
        return self.request.path

    @property
    def scheme(self):
        return to_unicode_safe(self.request.scheme)

    @property
    def server_port(self):
        return to_unicode_safe(self.get_raw_header("SERVER_PORT"))

    @property
    def remote_port(self):
        return to_unicode_safe(self.get_raw_header("REMOTE_PORT"))

    @property
    def raw_headers(self):
        return self.request.environ

    @property
    def caller(self):
        return format_stack()

    @property
    def view_params(self):
        return self.request.view_args

    @property
    def is_flask_api(self):
        """ Detect a Flask API request. """
        return hasattr(self.request, "empty_data_class") \
            and "flask_api" in sys.modules

    @staticmethod
    def is_debug():
        try:
            from flask import current_app

            return bool(current_app.debug)
        except Exception:
            LOGGER.debug("couldn't get current_app.debug", exc_info=True)
            return False


class FlaskResponse(BaseResponse):

    def __init__(self, response):
        self.response = response

    @property
    def status_code(self):
        return self.response.status_code

    @property
    def content_type(self):
        return self.response.headers.get("Content-Type")

    @property
    def content_length(self):
        try:
            return int(self.response.headers.get("Content-Length"))
        except (ValueError, TypeError):
            return None
