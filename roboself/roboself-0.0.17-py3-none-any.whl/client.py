import logging
import uuid
from threading import Event

import socketio

log = logging.getLogger(__name__)


class Client:
    """Client for connecting to an assistant runtime."""

    def __init__(self,
                 api_key,
                 api_endpoint="https://api.roboself.com"):
        """ Constructor.

        :param api_key: The API KEY to use for the connection.
        :param api_endpoint: The endpoint to connect to. Defaults to https://api.roboself.com.
        """
        self.api_key = api_key
        self.api_endpoint = api_endpoint

        # We generate a random client id, it just needs to be unique
        self.client_key = str(uuid.uuid4())
        self.socketio_url = f'{api_endpoint}?api_key={api_key}&client_key={self.client_key}'
        self.sio = socketio.Client()
        self.sio.connect(self.socketio_url, transports=['websocket'])

        # This will be sent once the initialization is finished
        self.initialized = Event()

        # The handler for incoming requests
        self.handler: callable = None

        @self.sio.event
        def connect():
            log.info(f"Connected to {self.socketio_url}")
            self.initialized.set()

        @self.sio.event
        def connect_error(error):
            log.warning(f"The connection to {self.socketio_url} failed!: {error}")

        @self.sio.event
        def disconnect():
            log.warning(f"Disconnected from {self.socketio_url}")

        @self.sio.event
        def request(data):
            log.debug(f"Got request from runtime: {data}")
            return self._handle_runtime_request(data)

    def request(self, path, data=None, timeout=30):
        """Sends a request to the runtime.

        :param path: The path for the request. See API reference for details.
        :param data: A dict with any additional data needed for the request.
        :param timeout: The number of seconds to wait until a timeout.
        """
        # Make sure we wait for the client to be initialized before making the request
        self.initialized.wait()

        return self.sio.call("request", {
            "path": path,
            "data": data
        }, timeout=timeout)

    def register_handler(self, handler: callable):
        """ Registers the handler for the incoming requests.

        **Important**: the handler will be called on a different thread.

        :param handler: A function that will be called for every request.
        :return:
        """
        self.handler = handler

    def _handle_runtime_request(self, data):
        """Handles a request coming from the roboself runtime."""
        if not isinstance(data, dict):
            raise Exception(f"Unknown data format {data}")

        # We handle by default the /ping path
        if data.get("path") == "/ping":
            return "pong"
        else:
            if not self.handler:
                log.warning(f"No handler registered for: {data}")
                return f"No handler registered for: {data}"

            return self.handler(data)

