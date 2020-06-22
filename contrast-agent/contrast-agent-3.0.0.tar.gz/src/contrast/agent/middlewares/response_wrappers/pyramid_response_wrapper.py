# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.extern.six import PY2

from contrast.agent.middlewares.response_wrappers.base_response_wrapper import (
    BaseResponseWrapper,
)


class PyramidResponseWrapper(BaseResponseWrapper):
    def __init__(self, response):
        self.response = response

        self.body = response.body
        self.code = response.status_int
        self.status = 0

        self.headers = response.headers

    def set_code(self, code):
        self.response.status_int = int(code)
        self.response.status_code = int(code)
        self.code = code

    def set_status(self, status):
        self.response.status = status
        self.status = status

    def set_body(self, body):
        if PY2:
            self.response.body = body
        else:
            self.response.text = body

    def set_header(self, header_name, header_value):
        """
        Pyramid headers are attributes of the response.
        https://docs.pylonsproject.org/projects/pyramid/en/latest/api/response.html
        """
        header_name = header_name.replace("-", "_").lower()

        if hasattr(self.response, header_name):
            setattr(self.response, header_name, header_value)
