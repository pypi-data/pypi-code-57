# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.extern import six

import logging

logger = logging.getLogger("contrast")


class ResponseMixin(object):
    # TODO: PYT-817 should change this from a mixin to a dedicated class

    def initialize_response(self, response=None):
        self.response = response

    def response_code(self):
        return self.response.code

    def response_header(self, key):
        if not self._response_headers():
            return

        value = self._response_headers().get(key.lower())
        if isinstance(value, tuple):
            return value[1]
        return value

    def response_body(self):
        """
        Get the response body associated with this request

        Callers should be aware that the response body may not always be a
        a string. An attempt is made to decode the response body as utf-8, but
        if the data is pure binary (e.g. image, video, etc.), this method will
        return a bytes object.
        """
        return self._extract_response_body(self.response.body)

    def _response_headers(self):
        return self.response.headers

    def _extract_response_body(self, body):
        if not body:
            return

        if isinstance(body, list):
            obj = [self._read_or_string(item) for item in body]
            return "\n".join(obj)

        return self._read_or_string(body)

    def _read_or_string(self, obj):
        if not obj:
            return ""

        if hasattr(obj, "read") or "read" in dir(obj):
            read = obj.read()

            obj.seek(0)

            obj = read

        try:
            return six.ensure_str(obj)
        except UnicodeDecodeError:
            logger.debug("Unable to decode response body; returning binary")
            return obj
        except Exception:
            logger.exception("Failed to decode obj of type %s", type(obj))
            return ""
