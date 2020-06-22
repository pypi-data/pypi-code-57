# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.extern.six import PY2
from contrast.agent.middlewares.response_wrappers.base_response_wrapper import (
    BaseResponseWrapper,
)


class WsgiResponseWrapper(BaseResponseWrapper):
    def __init__(self, response):
        """
        :param response: `webob.Response` object wrapping the wsgi_application's response
        """
        self._response = response

    def set_header(self, header_name, header_value):
        self._response.headers[header_name] = header_value

    def set_body(self, body):
        """
        @param body: string containing the new body. The type should be `str` in whichever
            version of python is being used.
        """
        if PY2:
            self._response.body = body
        else:
            self._response.text = body

    def set_code(self, code):
        self._response.status_code = code

    def set_status(self, status):
        self._response.status = status

    # TODO: we will turn these into standalone properties soon. See CONTRAST-37883

    def get_code(self):
        return self._response.status_code

    code = property(get_code, set_code)

    def get_headers(self):
        return self._response.headers

    def set_headers(self, headers):
        # TODO: this should probably never happen, as headers should be set one at a time. Revisit in CONTRAST-37883
        self._response.headers = headers

    headers = property(get_headers, set_headers)

    def get_body(self):
        return self._response.body

    body = property(get_body, set_body)

    def get_status(self):
        return self._response.status

    status = property(get_status, set_status)
