# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import io

from contrast.extern.six.moves.urllib.parse import urlencode

from contrast.test import helper


class RequestBuilder(object):
    def __init__(self, environ=None):
        if environ:
            self.environ = environ
        else:
            self.environ = helper.get_simple_request()
        self._POST = {}

    @property
    def POST(self):
        """
        Some frameworks - specifically pyramid - have a property on a request object
        to receive the post data. This intends to mimic that for testing.
        """
        return self._POST

    def url(self, url):
        self.environ["HTTP_HOST"] = url

        return self

    def path(self, path):
        self.environ["PATH_INFO"] = "/" + path if path[0] != "/" else path

        return self

    def params(self, params):
        self.environ["QUERY_STRING"] = urlencode(params)

        return self

    def query_string(self, query_string):
        self.environ["QUERY_STRING"] = query_string

        return self

    def cookie(self, cookie):
        self.environ["HTTP_COOKIE"] = cookie

        return self

    def header(self, header, header_value):
        self.environ[header] = header_value

        return self

    def body(self, body):
        self.environ["wsgi.input"] = io.BytesIO(body)
        self.environ["CONTENT_LENGTH"] = len(body)

        return self

    def set_post_form(self, body):
        self.environ["REQUEST_METHOD"] = "POST"

        if "CONTENT_TYPE" not in self.environ or not self.environ["CONTENT_TYPE"]:
            self.environ["CONTENT_TYPE"] = "application/x-www-form-urlencoded"

        self.environ["CONTENT_LENGTH"] = len(body)

        self.environ["wsgi.input"] = io.BytesIO(body)

        return self

    def get_request_method(self):
        return self.environ.get("REQUEST_METHOD", "")

    def get_path(self):
        return self.environ.get("PATH_INFO", "")

    def path_info(self):
        return self.get_path()

    def host_url(self):
        return self.environ.get("HTTP_HOST", "")

    def remote_addr(self):
        return self.environ.get("REMOTE_ADDR", "")

    def text(self):
        return ""

    def to_request(self):
        return self.environ
