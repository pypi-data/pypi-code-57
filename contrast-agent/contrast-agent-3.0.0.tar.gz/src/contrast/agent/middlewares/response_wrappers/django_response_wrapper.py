# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.middlewares.response_wrappers.base_response_wrapper import (
    BaseResponseWrapper,
)


class DjangoResponseWrapper(BaseResponseWrapper):
    def __init__(self, response):
        self.response = response
        self.headers = response._headers
        self.streaming_cache = None

    def set_header(self, header_name, header_value):
        self.response[header_name] = header_value

    @property
    def body(self):
        if self.is_streaming():
            return self.handle_streaming_response()
        return self.response.content

    def set_body(self, body):
        self.response.content = body

    @property
    def code(self):
        return self.response.status_code

    def set_code(self, code):
        self.response.status_code = code

    @property
    def status(self):
        return self.response.reason_phrase

    def set_status(self, status):
        self.response.reason_phrase = status

    def is_streaming(self):
        if hasattr(self.response, "streaming_content") or self.response.streaming:
            self.streaming_cache = None
            return True
        return False

    def handle_streaming_response(self):
        _response_class = type(self.response)
        if not self.streaming_cache:
            body = bytes()
            for item in self.response.streaming_content:
                body += item

            self.streaming_cache = body
            self.response = _response_class(self.recreate_streaming_response(body))
            self.response._headers = self.headers
            return body

        return self.streaming_cache

    def recreate_streaming_response(self, body):
        yield body
