#!/usr/bin/env python
from http import HTTPStatus


class InvalidUsage(Exception):
    code = HTTPStatus.BAD_REQUEST

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.name = message
        if status_code:
            self.code = status_code
        self.payload = payload
        self.description = None

    def __str__(self):
        return self.name
