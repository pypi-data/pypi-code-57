# -*- coding: utf-8 -*-
# Copyright (c) 2016 - 2020 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#
""" Pyramid specific WSGI HTTP Request / Response stuff
"""
from logging import getLogger

from ..utils import is_json_serializable
from .base import BaseResponse
from .wsgi import BaseWSGIRequest

LOGGER = getLogger(__name__)


class PyramidRequest(BaseWSGIRequest):

    def __init__(self, request, storage=None):
        super(PyramidRequest, self).__init__(storage=storage)
        self.request = request

        # Cache for params
        self._query_params = None
        self._form_params = None
        self._cookies_params = None
        self._json_params = None

    @property
    def query_params(self):
        if self._query_params is None:
            try:
                # Convert pyramid MultiDict to a normal dict with values as list
                self._query_params = dict(self.request.GET.dict_of_lists())
            except Exception:
                LOGGER.debug("couldn't get request.GET from the framework",
                             exc_info=True)
                self._query_params = super(PyramidRequest, self).query_params
        return self._query_params

    @property
    def body(self):
        try:
            return self.request.body
        except Exception:
            LOGGER.debug("couldn't get request.body from the framework",
                         exc_info=True)
            return super(PyramidRequest, self).body

    @property
    def form_params(self):
        if self._form_params is None:
            try:
                # Convert pyramid MultiDict to a normal dict with values as list
                form_params = {}
                post_params = self.request.POST
                for param_name in post_params:
                    values = post_params.getall(param_name)
                    # Ignore any non json serializable value as we don't know
                    # how to process them (like cgi.FieldStorage)
                    form_params[param_name] = list(
                        filter(is_json_serializable, values)
                    )
                self._form_params = form_params
            except Exception:
                LOGGER.debug("couldn't get request.POST from framework",
                             exc_info=True)
                self._form_params = super(PyramidRequest, self).form_params
        return self._form_params

    @property
    def cookies_params(self):
        if self._cookies_params is None:
            try:
                self._cookies_params = dict(self.request.cookies)
            except Exception:
                LOGGER.debug("couldn't get request.cookies from framework",
                             exc_info=True)
                self._cookies_params = super(PyramidRequest, self).cookies_params
        return self._cookies_params

    @property
    def remote_addr(self):
        """Remote IP address."""
        return self.request.remote_addr

    @property
    def hostname(self):
        return self.request.host

    @property
    def method(self):
        return self.request.method

    @property
    def referer(self):
        return self.get_raw_header("HTTP_REFERER")

    @property
    def client_user_agent(self):
        return self.request.user_agent

    @property
    def route(self):
        """Request route."""
        route = getattr(self.request, "matched_route", None)
        pattern = getattr(route, "pattern", None)
        return pattern

    @property
    def path(self):
        return self.request.path

    @property
    def scheme(self):
        return self.request.scheme

    @property
    def server_port(self):
        return self.get_raw_header("SERVER_PORT")

    @property
    def remote_port(self):
        return self.get_raw_header("REMOTE_PORT")

    @property
    def view_params(self):
        return self.request.matchdict

    @property
    def json_params(self):
        if self._json_params is None:
            try:
                self._json_params = self.request.json_body
            except Exception:
                LOGGER.debug("couldn't get request.json_body from the framework",
                             exc_info=True)
                self._json_params = super(PyramidRequest, self).json_params
        return self._json_params

    @property
    def raw_headers(self):
        return self.request.environ


class PyramidResponse(BaseResponse):

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
            return int(self.response.content_length)
        except (ValueError, TypeError):
            return None
