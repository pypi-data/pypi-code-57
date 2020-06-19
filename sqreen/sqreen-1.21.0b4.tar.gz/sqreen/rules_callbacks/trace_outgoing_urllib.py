# -*- coding: utf-8 -*-
# Copyright (c) 2016 - 2020 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#
""" Callback for tracing outgoing urllib requests
"""
import uuid

from ..constants import ACTIONS
from .trace import Trace


class TraceOutgoingUrllib(Trace):

    # Hook http.client.HTTPConnection._send_request

    def pre(self, instance, args, kwargs, **options):
        try:
            host_ip, host_port = instance.sock.getpeername()
        except Exception:
            host_ip, host_port = None, None

        tracing_identifier_prefix = self.runner.settings.tracing_identifier_prefix
        if tracing_identifier_prefix is not None:
            request_identifier = uuid.uuid4()
            tracing_identifier = "{}.{}".format(tracing_identifier_prefix, request_identifier)
        else:
            tracing_identifier = None
            request_identifier = None

        options["host_ip"] = host_ip
        options["host_port"] = host_port
        options["tracing_identifier_prefix"] = tracing_identifier_prefix
        options["tracing_identifier"] = tracing_identifier
        options["request_identifier"] = request_identifier

        super(TraceOutgoingUrllib, self).pre(instance, args, kwargs, **options)

        options = self.data.get("options", {})
        if options.get("propagate_tracing_identifier", False) and tracing_identifier is not None:
            method, url, body, headers, encode_chunked = args
            new_headers = dict(headers)
            header_name = options.get("header_name", "X-Sqreen-Trace-Identifier")
            new_headers[header_name] = tracing_identifier
            return {
                "status": ACTIONS["MODIFY_ARGS"],
                "args": ((method, url, body, new_headers, encode_chunked), {}),
            }
