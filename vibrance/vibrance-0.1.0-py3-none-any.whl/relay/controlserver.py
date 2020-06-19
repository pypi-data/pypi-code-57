import socket
import json
import ssl
import selectors
import logging


class ControlServer:
    """Server allowing controllers to connect and submit updates."""

    # Constants used to indicate socket type when used with selectors:
    SERVER = 0  # server socket
    WAITING = 1  # awaiting authentication
    CLIENT = 2  # connected client

    def __init__(self, appServer, psk=None, cert=None, key=None):
        """Creats a ControlServer with the specified ClientServer to
        broadcast updates to. If psk is provided, password-protects the server.
        If cert and key are provided, encrypts the server with SSL."""

        self.logger = logging.getLogger(__name__)
        self.logger.info("Starting control server")

        self.appServer = appServer
        self.psk = psk

        if cert is not None and key is not None:
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            ssl_context.load_default_certs()
            ssl_context.load_cert_chain(cert, key)
        else:
            ssl_context = None

        unwrapped = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        unwrapped.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        unwrapped.bind(("0.0.0.0", 9999))
        unwrapped.listen(16)

        if ssl_context:
            self.sock = ssl_context.wrap_socket(unwrapped, server_side=True)
        else:
            self.sock = unwrapped

        self.logger.info("Server socket established")

        self.selector = selectors.DefaultSelector()
        self.selector.register(self.sock, selectors.EVENT_READ,
                               ControlServer.SERVER)

    def accept(self):
        """Accepts a new controller client."""
        new_client, addr = self.sock.accept()
        if self.psk is not None:
            self.selector.register(new_client,
                                   selectors.EVENT_READ,
                                   ControlServer.WAITING)
        else:
            self.selector.register(new_client,
                                   selectors.EVENT_READ,
                                   ControlServer.CLIENT)

    def remove(self, client):
        """Removes a controller client from all lists and closes it if
        possible."""

        self.selector.unregister(client)
        try:
            client.close()
        except OSError:
            pass

    def authenticate(self, client):
        """Handles messages from a controller client that needs to
        authenticate."""

        try:
            data = client.recv(1024)
        except OSError:
            self.logger.warning("Unable to read from authenticating client")
            self.remove(client)
            return
        if len(data) == 0:
            self.logger.warning("Authenticating client disconnected")
            self.remove(client)
            return

        msg = data.decode("utf-8", "ignore")
        if msg == self.psk:
            self.logger.info("Client authenticated successfully")
            self.selector.modify(client, selectors.EVENT_READ,
                                 ControlServer.CLIENT)
            client.send(b"OK")
        else:
            self.logger.warning("Client failed authentication")
            self.remove(client)

    def handleUpdate(self, client):
        """Handles update messages from a connected controller client."""
        try:
            data = client.recv(2**18)
        except OSError:
            self.logger.warning("Unable to read update from client")
            self.remove(client)
            return
        if len(data) == 0:
            self.logger.warning("Client disconnected")
            self.remove(client)
            return

        msg = data.decode("utf-8", "ignore")

        try:
            messages = json.loads(msg.split("\n")[0])
        except json.JSONDecodeError:
            self.logger.warning("Invalid JSON in update")
            self.remove(client)
            return

        telemetry = self.appServer.broadcast(messages)
        client.send(json.dumps(telemetry).encode("utf-8"))

    def run(self):
        """Monitors for new connections or updates from controller clients and
        handles them appropriately."""

        while True:
            events = self.selector.select()

            for key, mask in events:
                client = key.fileobj
                type = key.data

                self.logger.debug("New message from socket")

                if type == ControlServer.SERVER:
                    self.logger.debug("Accepting new client connection")
                    self.accept()
                elif type == ControlServer.WAITING:
                    self.logger.debug("Handling authentication")
                    self.authenticate(client)
                elif type == ControlServer.CLIENT:
                    self.logger.debug("Handling inbound update")
                    self.handleUpdate(client)
