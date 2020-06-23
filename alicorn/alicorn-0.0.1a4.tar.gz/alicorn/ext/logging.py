#  Copyright (c) 2020 Chris Stranex
#  See LICENSE for licencing information.
#
#  There is NO WARRANTY, to the extent permitted by law.
#
#
#  There is NO WARRANTY, to the extent permitted by law.
#
import time
import logging

import grpc
import grpc._server

from alicorn._ctx import GrpcContext
from alicorn.extension import Extension


def create_logger(name, logging_config):
    """Create a new logging instance with the given name and configuration"""

    logger = logging.getLogger(name)

    if logging_config:
        pass

    return logger


class LoggingRequestExtension(Extension):
    """A logging extension that logs all requests to the server"""

    name = ''
    app = None
    logger = None

    def __init__(self):
        self._handlers = {}
        self.logger = logging.getLogger(__name__)

    def register(self, app):
        self.name = app.name
        self.app = app
        self.logger = logging.getLogger(self.name)
        app.before_request(self.before_request)
        app.after_request(self.after_request)
        app.add_context_handler(lambda: {
            'log': None,
            'start_time': 0
        })
        app.register_signal_handler('alicorn.server_start', self.on_server_start)

    def on_server_start(self):
        self.load_handlers(self.app._server)

    def load_handlers(self, server):
        for service in server._state.generic_handlers:
            for path, method in service._method_handlers.items():
                self._handlers[
                    method.unary_unary or
                    method.unary_stream or
                    method.stream_unary or
                    method.stream_stream
                    ] = (path, method)

    def after_request(self, context: GrpcContext):
        """Output the log"""
        if not context.alicorn.log:
            return

        peer, method_type, method, user_agent = context.alicorn.log

        req_time = time.time() - context.alicorn.start_time

        code = grpc.StatusCode(context._state.code or grpc.StatusCode.OK)

        if not context._state.code:
            if context._state.aborted:
                code = grpc.StatusCode.ABORTED
            elif context._state.client == grpc._server._CANCELLED:
                code = grpc.StatusCode.CANCELLED

        self.logger.info(
            "[%s] %s %s %s - %.4f - (%s)",
            peer,
            method_type,
            str(code.value),
            method,
            req_time,
            user_agent
        )

    def before_request(self, request, context: GrpcContext):
        context.alicorn.start_time = time.time()
        user_agent = ''
        for key, value in context.invocation_metadata():
            if key == 'user-agent':
                user_agent = value
                break

        method_type = ''
        method = ''

        if context.alicorn.original_handler in self._handlers:
            # give additional information
            method, rpc_method_handler = self._handlers[context.alicorn.original_handler]
            if rpc_method_handler.request_streaming and rpc_method_handler.response_streaming:
                method_type = 'STREAM'
            elif rpc_method_handler.request_streaming:
                method_type = 'STREAM-UNARY'
            elif rpc_method_handler.response_streaming:
                method_type = 'UNARY-STREAM'
            else:
                method_type = 'UNARY'

        context.alicorn.log = (
            context.peer(),
            method_type,
            method,
            user_agent
        )

        if method_type == 'UNARY-STREAM' or method_type == 'STREAM':
            self.logger.info(
                "[%s] %s %s STARTED",
                context.peer(),
                method_type,
                method,
            )
