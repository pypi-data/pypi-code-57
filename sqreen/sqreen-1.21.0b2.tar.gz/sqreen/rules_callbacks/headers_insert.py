# -*- coding: utf-8 -*-
# Copyright (c) 2016 - 2020 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#
""" Insert X-Protected-By header
"""
import logging

from ..exceptions import InvalidArgument
from ..rules import RuleCallback
from ..utils import Mapping

LOGGER = logging.getLogger(__name__)


def convert_to_str(headers):
    """ Encode a list of headers tuples into latin1
    """
    for header_name, header_value in headers:
        header_name = str(
            header_name.encode("latin-1", errors="replace").decode("latin-1")
        )
        header_value = str(
            header_value.encode("latin-1", errors="replace").decode("latin-1")
        )
        yield (header_name, header_value)


class BaseHeadersInsertCB(RuleCallback):
    """ Base class for header insertion callbacks
    """

    def __init__(self, *args, **kwargs):
        super(BaseHeadersInsertCB, self).__init__(*args, **kwargs)

        if not isinstance(self.data, Mapping):
            msg = "Invalid data type received: {}"
            raise InvalidArgument(msg.format(type(self.data)))

        try:
            self.values = self.data["values"]
        except KeyError:
            msg = "No key 'values' in data (had {})"
            raise InvalidArgument(msg.format(self.data.keys()))

        self._headers = None

    @property
    def headers(self):
        """ Cached property to defer headers data conversio,n
        """
        if self._headers is None:
            self._headers = dict(convert_to_str(self.values))
        return self._headers


class HeadersInsertCB(BaseHeadersInsertCB):
    """ Callback that add the custom sqreen header in WSGI
    """

    def pre(self, instance, args, kwargs, **options):
        new_args = list(args)
        headers_to_add = dict(self.headers)
        new_headers = []
        current_headers = args[1]
        for item in current_headers:
            header = headers_to_add.pop(item[0], None)
            if header is not None:
                new_headers.append((item[0], header))
            else:
                new_headers.append(item)
        for item in headers_to_add.items():
            new_headers.append(item)

        new_args[1] = new_headers
        return {"status": "modify_args", "args": [new_args, kwargs]}
