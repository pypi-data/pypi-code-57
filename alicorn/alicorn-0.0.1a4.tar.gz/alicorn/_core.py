import importlib
from functools import wraps
from typing import Optional, Dict, Type, Callable, Union
import inspect
import logging

import grpc
from grpc._utilities import RpcMethodHandler
from google.protobuf import symbol_database

from alicorn._config import Config, _global_config, get_defaults
from alicorn._ctx import AlicornContext
from alicorn.discover import auto_discover
from alicorn.exception import AlicornConfigurationException, AlicornSignalNotFound, AlicornStatusException
from alicorn import _rpc
from alicorn._ctx import GrpcContext
from alicorn.ext.logging import create_logger, LoggingRequestExtension
from alicorn.port import Port, InsecurePort, SecurePort
from alicorn.util import lazy_property
from .dependency import inject
from .signal import Signal
from ._type import ProtobufMessage, RequestType

_sym_db = symbol_database.Default()


class Alicorn:

    def __init__(self, name='alicorn', config=None):
        """
        Construct an Alicorn instance that manages grpc services

        :param name: The name of this Alicorn instance
        :param config: If not None, a dict with default configuration values
        """
        self._interceptors = []
        self._extensions = []
        self._server = None
        self._before_request_handlers = []
        self._after_request_handlers = []
        self._after_teardown_handlers = []
        self._context_handlers = []
        self._rpc_services: Dict[str, Type] = {}
        self._services: Dict[Type, Type] = {}
        self._handlers: Dict[str, _rpc.MethodHandlers] = {}
        self._dependencies = {}
        self._signals = {}
        self._service_mappings = {}
        self.name = name
        self.config = Config(get_defaults(), global_config=_global_config)
        if config:
            self.config.load_from_dict(config)
        self.register_signal('alicorn.server_start')
        self.register_signal('alicorn.server_stop')

    @property
    def debug(self) -> bool:
        """Debug mode"""
        return self.config.get('debug')

    @debug.setter
    def debug(self, v: bool):
        self.config['debug'] = v

    @lazy_property
    def logger(self):
        """Return a cached logger instance"""
        return create_logger(self.name, self.config.get('logging'))

    def interceptor(self, f: Callable):
        """Adds an interceptor to the server"""
        if f not in self._interceptors:
            self._interceptors.append(f)

    def before_request(self, f: Callable[[RequestType, GrpcContext, Callable], RequestType]):
        """Register a callback that runs before a request is passed to the service method but after the request has
        been accepted. Called with the request message (or generator), context and a reference to the original
        method. The request can be re-written and returned.

        This will run in the same thread as the service's method.

        If you are needing to run a callback before the request has been set-up then add middleware instead.
        """
        if f not in self._before_request_handlers:
            self._before_request_handlers.append(f)

    def after_request(self, f: Callable[[GrpcContext, Callable], None]):
        """Register a callback that runs after a request has finished being processed by the service method but
        before the context has been torn down. Called with the context and a reference to the original method.
        As the request has already been served no response can be read or sent.

        This will run in the same thread as the service's method.
        """
        if f not in self._after_request_handlers:
            self._after_request_handlers.append(f)

    def after_request_teardown(self, f: Callable):
        """Register a callback that runs after a request has been served and marked as complete. This is the
        equivalent of adding a done callback to the context. Does not receive any parameters.

        This will run in the main thread.
        """
        if f not in self._after_teardown_handlers:
            self._after_teardown_handlers.append(f)

    def add_extension(self, extension: 'alicorn.extension.Extension'):
        """Adds an extension to this Alicorn instance"""
        if extension in self._extensions:
            return
        extension.register(self)
        self._extensions.append(extension)

    def add_context_handler(self, handler: Callable[[], Dict]):
        """Add a handler that is called when an AlicornContext is created. The handler should
        return a dict that is added into the context during the request."""
        if handler in self._context_handlers:
            return
        self._context_handlers.append(handler)

    def dependency(self, f: Union[str, Callable]):
        """Adds a named dependency for use with `Depends`

        Examples:
            Create a named dependency called name.

            >>> @dependency("name")
            ... def test():
            ...     pass

            Create a named dependency called test2.

            >>> @dependency
            ... def test2():
            ...     pass
        """
        if isinstance(f, str):
            def wrapper(func):
                self.add_dependency(f, func)
                return func

            return wrapper
        else:
            self.add_dependency(f.__name__, f)
            return f

    def add_dependency(self, name: str, f: Callable):
        """Add a named dependency"""
        self._dependencies[name] = self.inject(f)

    def inject(self, f: Callable):
        """Inject dependencies into this method or function.

        See Also:
            `alicorn.dependency.inject`
        """
        return inject(self)(f)

    def rpc_service(self, service_name: str = None):
        """Like the @service decorator but works on generic python classes. To define service methods use the
        @rpc_method_* decorators.
        """

        def wrap(cls):
            name = service_name or cls.__name__
            self._rpc_services[name] = cls

            return cls

        return wrap

    def rpc_method_unary(self, request: ProtobufMessage, response: ProtobufMessage, name: str = None):
        """Decorator for a unary-unary method"""
        return _rpc.method(request, response, 'unary', 'unary', name, self._handlers, self._request_handler)

    def rpc_method_unary_stream(self, request: ProtobufMessage, response: ProtobufMessage, name: str = None):
        """Decorator for a unary-stream method"""
        return _rpc.method(request, response, 'unary', 'stream', name, self._handlers, self._request_handler)

    def rpc_method_stream_unary(self, request: ProtobufMessage, response: ProtobufMessage, name: str = None):
        """Decorator for a stream-unary method"""
        return _rpc.method(request, response, 'stream', 'unary', name, self._handlers, self._request_handler)

    def rpc_method_stream(self, request: ProtobufMessage, response: ProtobufMessage, name: str = None):
        """Decorator for a stream-stream method"""
        return _rpc.method(request, response, 'stream', 'stream', name, self._handlers, self._request_handler)

    def service(self, cls):
        """A decorator for a Servicer class to add the service to the Alicorn instance. Automatically applies
        the injector decorator to all methods in the class.

        Raises:
            TypeError: If the class does not inherit from a grpc servicer class
        """

        servicer = None
        for _cls in inspect.getmro(cls):
            # Try determine if we inherit from a grpc servicer class. Unfortunately there is not base class
            # so we have to use the generated python file's name. Failing that, try see if it has been registered
            # in the symbol database
            if 'pb2_grpc' not in _cls.__module__:
                continue
            servicer = _cls
            break

        if not servicer:
            # Look up the inherited class names in the symbol db to try and find the service descriptor
            for _cls in inspect.getmro(cls):
                name = _cls.__name__.replace('Servicer', '')
                try:
                    _sym_db.pool.FindServiceByName(name)
                    servicer = _cls
                    break
                except KeyError:
                    pass

        if not servicer:
            raise TypeError("Class does not inherit from a grpc servicer class")

        for name, method in inspect.getmembers(cls, inspect.isfunction):
            if not hasattr(servicer, name):
                # If the grpc servicer does not have this method then don't wrap it in request_handler
                continue

            handler = self._request_handler(inject(self)(method))
            setattr(cls, name, handler)

        self._services[cls] = servicer

        return cls

    def register_signal(self, name: str) -> Signal:
        """Registers a signal that can be listened to and called.
        See alicorn.signal.Signal"""
        s = Signal(name)
        self._signals[name] = s
        return s

    def unregister_signal(self, name: str):
        """Unregister a signal

        Raises:
            AlicornSignalNotFound: If the signal does not exist
        """
        try:
            del self._signals[name]
        except KeyError:
            raise AlicornSignalNotFound(f'{name} is not a registered signal')

    def get_signal(self, name: str) -> Signal:
        """Return a registered Signal object

        Raises:
            AlicornSignalNotFound: If the signal does not exist
        """
        try:
            return self._signals[name]
        except KeyError:
            raise AlicornSignalNotFound(f'{name} is not a registered signal')

    def register_signal_handler(self, name: str, f: Callable):
        """Registers the handler to the given signal name"""
        self.get_signal(name).append(f)

    def unregister_signal_handler(self, name: str, f: Callable):
        """Removes the handler from the signal"""
        self.get_signal(name).remove(f)

    def _create_rpc_services(self):
        """Instantiate any rpc service classes and return them to be added to the servicer"""
        for service_name, service_class in self._rpc_services.items():

            handlers = self._handlers.get(service_class.__name__, {}).items()
            instance = self._service_mappings[service_name] = service_class()

            rpc_method_handlers = {}
            for name, handler in handlers:
                method = getattr(instance, handler.method_name)
                rpc_method_handlers[name] = RpcMethodHandler(
                    handler.request_type == 'stream',
                    handler.response_type == 'stream',
                    getattr(handler.request, 'FromString'),
                    getattr(handler.response, 'SerializeToString'),
                    method if handler.request_type == 'unary' and handler.response_type == 'unary' else None,
                    method if handler.request_type == 'unary' and handler.response_type == 'stream' else None,
                    method if handler.request_type == 'stream' and handler.response_type == 'unary' else None,
                    method if handler.request_type == 'stream' and handler.response_type == 'stream' else None,
                )

            yield grpc.method_handlers_generic_handler((service_name, rpc_method_handlers))

    def _create_services(self):
        """Instantiate any servicer classes and return them to be added to the server."""

        class MockServer:
            """A mock implementation of the server to get the generic rpc handlers"""
            handler = None

            def add_generic_rpc_handlers(self, handler):
                self.handler = handler[0]

        for service_class, servicer_class in self._services.items():
            instance = service_class()

            # Since the class generated by grpc protoc doesn't have any message information in it,
            # we must rely on the add_SERVICE_to_server helper function it generates. It should always
            # be in the same module as the Servicer class, so we import the module the class belongs to,
            # and call the function. It is pretty hacky so it would definitely be better to remove the need
            # to call the add_to_server function entirely.

            mock_server = MockServer()

            servicer_module = importlib.import_module(servicer_class.__module__)
            func = f'add_{servicer_class.__name__}_to_server'
            getattr(servicer_module, func)(instance, mock_server)

            self._service_mappings[mock_server.handler.service_name()] = instance

            yield mock_server.handler

    def _create_context(self, original_handler):
        """Creates a new Alicorn context that is added to the grpc context. Mostly useful for extensions or pre request
        handlers to inject information"""
        context = AlicornContext(self)
        context.original_handler = original_handler

        for handler in self._context_handlers:
            context._add(handler())

        return context

    def _request_handler(self, f):
        """Handles every grpc request by running before/after request handlers and creating an Alicorn context object"""

        @wraps(f)
        def request_wrapper(ins, request, context: GrpcContext, *args, **kwargs):
            if not inspect.ismethod(f):
                instance_method = getattr(ins, f.__name__)
            else:
                instance_method = f

            context.alicorn = self._create_context(instance_method)

            for callback in self._after_teardown_handlers:
                # After teardown handlers run after the thread is closed and does not have access to the
                # Alicorn context
                context.add_callback(callback)

            response = None
            for handler in self._before_request_handlers:
                # Before request handlers are given the request and context as a request starts. If they return
                # a response then the request will be considered handled otherwise the request is then passed
                # on to the original handler. This is similar to the grpc interceptors except the handler
                # receivers the context and request instead of just the call details.
                try:
                    response = handler(request, context, *args, **kwargs)
                    if response is not None:
                        break
                except AlicornStatusException as e:
                    # Abort processing if we received a status exception
                    context.abort(e.code, e.reason)

            if not response:
                response = f(ins, request, context, *args, **kwargs)

            if inspect.isgenerator(response) or hasattr(response, '__iter__'):
                # If response returns a generator than yield all responses first before running the after request
                # handlers before the thread and context is lost. Otherwise, run the request handlers and return
                # the unary response afterwards.
                def gen():
                    try:
                        yield from response
                        for handler in self._after_request_handlers:
                            handler(context)
                    except AlicornStatusException as e:
                        # Abort processing if we received a status exception
                        context.abort(e.code, e.reason)

                return gen()
            else:
                try:
                    for handler in self._after_request_handlers:
                        handler(context)
                except AlicornStatusException as e:
                    # Abort processing if we received a status exception
                    context.abort(e.code, e.reason)
                return response

        return request_wrapper

    def _cleanup(self):
        """Clean-Up the Alicorn instance"""
        self.get_signal('alicorn.server_stop')()

    def get_handlers(self):
        """Return a dictionary of handlers for use with grpc-testing"""

        list(self._create_services())
        list(self._create_rpc_services())

        mapping = {}
        for name, instance in self._service_mappings.items():
            # FIXME: Python-based services can't generate a descriptor, so we have to skip those for now
            try:
                mapping[_sym_db.pool.FindServiceByName(name)] = instance
            except KeyError:
                pass
        return mapping

    def stop(self, grace: Optional[int] = None):
        """Stop the server. This method returns immediately with a threading Event that indicates when all the
        requests have finished been processed"""
        return self._server.stop(grace)

    def run(self, listen: Optional[Port] = None):
        """Start the grpc server. If no ports have been configured then use the host and port parameters to create
        an insecure port if specified. If not specified then raise an error.

        Raises:
            AlicornConfigurationException: If no ports have been specified and listen is None
        """

        # if debug is True then update the logger and ensure the logging middleware is enabled
        if self.debug:
            self.logger.setLevel(logging.DEBUG)
            self.config.set('extensions.logging', {
                'enabled': True,
                'detailed_logging': True
            })

        ports = self.config.get('grpc.ports')
        if not ports and not listen:
            raise AlicornConfigurationException("At least one port must be defined")
        elif not ports:
            ports = [listen]

        # Add internal extensions to the instance
        for extension, options in self.config.get('extensions').items():
            if isinstance(options, bool):
                if not options:
                    continue
            else:
                if not options or not options.get('enabled'):
                    continue

            if extension == 'logging':
                # TODO: Check this has not been added already
                self.add_extension(LoggingRequestExtension())

        self._server = grpc.server(
            self.config.get('grpc.thread_pool'),
            None,
            self._interceptors,
            self.config.get('grpc.options', {}).items(),
            self.config.get('grpc.maximum_concurrent_rpcs', None, int),
            self.config.get('grpc.compression', False)
        )

        for rpc_method_handlers in self._create_rpc_services():
            self._server.add_generic_rpc_handlers(rpc_method_handlers)

        for rpc_method_handlers in self._create_services():
            self._server.add_generic_rpc_handlers((rpc_method_handlers,))

        self.get_signal('alicorn.server_start')()

        for port in ports:
            if isinstance(port, InsecurePort):
                self._server.add_insecure_port(f'{port.host}:{port.port}')
            elif isinstance(port, SecurePort):
                self._server.add_secure_port(f'{port.host}:{port.port}', port.credentials)

        self.logger.info("Starting server...")
        self._server.start()
        for port in ports:
            self.logger.info("Listening on %s...", port)
        try:
            self._server.wait_for_termination()
        except KeyboardInterrupt:
            self.logger.info("Stopping server.. waiting for shutdown")
            self._server.stop(grace=self.config.get('grpc.shutdown_grace', 5, int))

        self._cleanup()

        self.logger.info("Server shutting down")


Alicorn.auto_discover = auto_discover
