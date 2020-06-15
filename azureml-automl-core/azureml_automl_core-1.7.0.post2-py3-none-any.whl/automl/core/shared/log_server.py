# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Server for handling logging from multiple processes."""
from typing import Any, Dict, Optional, Set
import logging
import logging.handlers
import os
import pickle
import platform
import random
import socketserver
import struct
import threading

from azureml.telemetry import get_telemetry_log_handler
from azureml.telemetry.contracts import RequiredFieldKeys, StandardFieldKeys
from . import constants
from . import logging_fields
from .telemetry_formatter import AppInsightsPIIStrippingFormatter


HOST_ENV_NAME = 'AUTOML_LOG_HOST'
PORT_ENV_NAME = 'AUTOML_LOG_PORT'
DEFAULT_VERBOSITY = logging.INFO
DEBUG_MODE = False


verbosity = DEFAULT_VERBOSITY
logger_names = set()    # type: Set[str]
handlers = {}   # type: Dict[str, logging.Handler]
custom_dimensions = {
    'app_name': constants.DEFAULT_LOGGING_APP_NAME,
    'automl_client': None,
    'automl_sdk_version': None,
    'child_run_id': None,
    'common_core_version': None,
    'compute_target': None,
    'experiment_id': None,
    'os_info': platform.system(),
    'parent_run_id': None,
    'region': None,
    'service_url': None,
    'subscription_id': None,
    'task_type': None,
    logging_fields.camel_to_snake_case(
        RequiredFieldKeys.COMPONENT_NAME_KEY): logging_fields.TELEMETRY_AUTOML_COMPONENT_KEY,
    logging_fields.camel_to_snake_case(
        StandardFieldKeys.CLIENT_OS_KEY): platform.system()
}  # type: Dict[str, Any]

lock = threading.RLock()


class LogRecordStreamHandler(socketserver.StreamRequestHandler):

    def handle(self):
        """
        Handle an incoming connection.

        :return:
        """
        while True:
            chunk = self.rfile.read(4)
            if len(chunk) < 4:
                break
            slen = struct.unpack('>L', chunk)[0]
            chunk = self.rfile.read(slen)
            while len(chunk) < slen:
                chunk = chunk + self.rfile.read(slen - len(chunk))
            obj = pickle.loads(chunk)
            record = logging.makeLogRecord(obj)
            self.handle_log_record(record)

    def handle_log_record(self, record: logging.LogRecord) -> None:
        """
        Emit the given LogRecord to all specified handlers, updating custom properties as needed.

        :param record: the incoming LogRecord
        :return:
        """
        new_properties = getattr(record, 'properties', {})
        with lock:
            cust_dim_copy = custom_dimensions.copy()
            cust_dim_copy.update(new_properties)
            setattr(record, 'properties', cust_dim_copy)
            try:
                for handler in handlers.values():
                    handler.handle(record)
            except ValueError as e:
                # This is expected if the process is exiting, since the log server is running as a daemon thread.
                if str(e) == 'I/O operation on closed file':
                    pass
                raise
            if DEBUG_MODE:
                try:
                    # Enable propagation to root logger if tests are running so that we can capture logs
                    logging.getLogger().handle(record)
                except Exception:
                    pass


class LogServer(socketserver.ThreadingTCPServer):

    def __init__(self,
                 host: str,
                 port: int):
        """
        Initialize the LogServer.

        :param host: the address this LogServer should listen on
        :param port: the port this LogServer should listen on
        """
        super().__init__((host, port), LogRecordStreamHandler)
        self._thread = None     # type: Optional[threading.Thread]

    def start(self) -> None:
        """
        Start the LogServer.

        :return:
        """
        self.daemon_threads = True
        self._thread = threading.Thread(target=self.serve_forever)
        self._thread.daemon = True
        self._thread.start()

    def stop(self) -> None:
        """
        Stop the LogServer.

        :return:
        """
        self.shutdown()
        self._thread = None


class AutoMLSocketHandler(logging.handlers.SocketHandler):
    def makePickle(self, record: logging.LogRecord) -> bytes:
        """
        Pickles the record in binary format with a length prefix and returns it ready for transmission across the
        socket.

        Note that this implementation is the same as Python's, but we use a higher protocol version than the default
        for performance reasons.

        :param record: the LogRecord object
        :return: the serialized LogRecord
        """
        ei = record.exc_info
        if ei:
            # just to get traceback text into record.exc_text ...
            self.format(record)
        # Add the process ID to the record
        setattr(record, 'pid', os.getpid())
        # If msg or args are objects, they may not be
        # available on the receiving end. So we convert the msg % args
        # to a string, save it as msg and zap the args.
        d = dict(record.__dict__)
        d['msg'] = record.getMessage()
        d['args'] = None
        d['exc_info'] = None
        # Delete 'message' if present: redundant with 'msg'
        d.pop('message', None)
        s = pickle.dumps(d, pickle.HIGHEST_PROTOCOL)
        slen = struct.pack(">L", len(s))
        return slen + s


def install_sockethandler(name: str,
                          host: Optional[str] = None,
                          port: Optional[int] = None) -> None:
    """
    Install an AutoMLSocketHandler for the logger corresponding to the given namespace.

    The logger will have log propagation automatically disabled.

    :param name: the name of the logger
    :param host: the log server hostname to connect to
    :param port: the log server port to connect to
    :return:
    """
    if host is not None:
        actual_host = host
    else:
        actual_host = os.environ.get(HOST_ENV_NAME, server_host)
    actual_port = port or int(os.environ.get(PORT_ENV_NAME, server_port))
    handler = AutoMLSocketHandler(actual_host, actual_port)
    logger = logging.getLogger(name)
    logger.propagate = False
    logger.setLevel(verbosity)
    logger.addHandler(handler)
    logger_names.add(name)


def add_handler(name: str, handler: Optional[logging.Handler], overwrite: bool = True) -> None:
    """
    Add a handler to the handler dict to be used when logging LogRecords.

    Can be used to capture all logs from AutoML by simply passing in a new handler object to intercept logs.

    :param name: name of the handler
    :param handler: the handler object. If None, disables the handler.
    :param overwrite: if set to True, always overwrite the existing handler. Otherwise, only set handler if it doesn't
    already exist.
    :return:
    """
    with lock:
        if handler is None and name in handlers:
            del handlers[name]
        elif handler is not None:
            if name not in handlers or overwrite:
                handlers[name] = handler


def remove_handler(name: str) -> None:
    """
    Remove a handler from the handler dict.

    If the handler with the given name doesn't exist, this function is a no-op.

    :param name: name of the handler
    :return:
    """
    with lock:
        if name in handlers:
            del handlers[name]


def enable_telemetry(key: str) -> None:
    """
    Enable telemetry using the specified key.

    :param key:
    :return:
    """
    if not key:
        if not DEBUG_MODE:
            logging.warning('Instrumentation key was blank. Telemetry will not work.')
    else:
        handler = get_telemetry_log_handler(
            instrumentation_key=key,
            component_name=logging_fields.TELEMETRY_AUTOML_COMPONENT_KEY)
        handler.setFormatter(AppInsightsPIIStrippingFormatter())
        add_handler('telemetry', handler)


def set_log_file(path: Optional[str]) -> None:
    """
    Specify the log file to write logs to.

    :param path: path of the log file. If None, disables logging to file.
    :return:
    """
    with lock:
        if path is None:
            if 'file' in handlers:
                del handlers['file']
            return
        handler = handlers.get('file', None)
        if isinstance(handler, logging.FileHandler):
            if os.path.abspath(handler.baseFilename) == os.path.abspath(path):
                return
        handler = logging.FileHandler(path)
        formatter = logging.Formatter(
            fmt="%(asctime)s.%(msecs)03d - %(levelname)s - %(pid)d - %(name)s.%(funcName)s:%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        add_handler('file', handler)


def set_verbosity(new_verbosity: int) -> None:
    """
    Set verbosity on all attached loggers.

    :param new_verbosity:
    :return:
    """
    with lock:
        global verbosity
        verbosity = new_verbosity
        for logger_name in logger_names:
            logger = logging.getLogger(logger_name)
            logger.setLevel(verbosity)


def update_custom_dimensions(new_dimensions: Dict[str, Any]) -> None:
    """
    Update the custom dimensions used during logging.

    :param new_dimensions: the new custom dimensions
    :return:
    """
    with lock:
        custom_dimensions.update(new_dimensions)


def update_custom_dimension(**kwargs: Any) -> None:
    """
    Update the custom dimensions used during logging.

    :param kwargs: the new custom dimensions
    :return:
    """
    update_custom_dimensions(kwargs)


# Initialize the logging system
# Use a random port to prevent collision with other AutoML processes.
server_host = os.environ.get(HOST_ENV_NAME, 'localhost')
# server_port = int(os.environ.get(PORT_ENV_NAME, logging.handlers.DEFAULT_TCP_LOGGING_PORT))
server_port = int(os.environ.get(PORT_ENV_NAME, random.randint(49152, 65535)))
try:
    server = LogServer(server_host, server_port)    # type: Optional[LogServer]
    if server:
        server.start()
except OSError:
    # If we're in a child process, log server will already be bound to the port.
    # So we can ignore exceptions.
    server = None
