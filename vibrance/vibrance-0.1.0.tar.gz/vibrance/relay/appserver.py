import socket
import subprocess
import atexit
import time
import json
import os
import selectors
import tempfile
import logging
from multiprocessing.dummy import Pool as ThreadPool


class AppServer:
    """Server allowing clients to connect and receive updates."""

    # Constants used to indicate socket type when used with selectors:
    SERVER = 0  # server socket
    WAITING = 1  # awaiting authentication
    CLIENT = 2  # connected client

    def __init__(self, cert=None, key=None, unix_socket=True):
        """Creates an AppServer. If cert and key are specified, uses SSL."""

        self.logger = logging.getLogger(__name__)
        self.logger.info("Starting application server")

        self.selector = selectors.DefaultSelector()

        if unix_socket:
            tempdir = os.path.join(tempfile.gettempdir(), "vibrance_relay")

            if not os.path.exists(tempdir):
                os.mkdir(tempdir)

            sockpath = os.path.join(tempdir, "sock")

            if os.path.exists(sockpath):
                os.remove(sockpath)

            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.bind(sockpath)
            sock.listen(16)
            self.selector.register(sock, selectors.EVENT_READ,
                                   AppServer.SERVER)

            websockify_target = f"--unix-target={sockpath}"

            self.logger.info("UNIX socket established")

        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(("localhost", 9001))
            sock.listen(16)
            self.selector.register(sock, selectors.EVENT_READ,
                                   AppServer.SERVER)

            websockify_target = "localhost:9001"

            self.logger.info("Server TCP socket established")

        websockify_ssl_args = []
        if cert is not None and key is not None:
            websockify_ssl_args.append(f"--cert={cert}")
            websockify_ssl_args.append(f"--key={key}")
            websockify_ssl_args.append("--ssl-only")

        self.websockify_proc = subprocess.Popen(["websockify", "9000",
                                                 websockify_target]
                                                + websockify_ssl_args,
                                                stdout=subprocess.DEVNULL,
                                                stderr=subprocess.DEVNULL)
        self.logger.info("Websockify server started")

        atexit.register(self.websockify_proc.terminate)

        self.clients = {}
        self.lastMessage = {}

        self.pool = ThreadPool(32)

        self.messages = {}

    def accept(self, server):
        """Accepts a new client on the given server socket."""
        new_client, addr = server.accept()
        self.selector.register(new_client, selectors.EVENT_READ,
                               AppServer.WAITING)
        self.lastMessage[new_client] = time.time()

    def addToZone(self, client):
        try:
            data = client.recv(1024)
        except OSError:
            self.logger.debug("Removing client: expected zone, "
                              "received OSError")
            self.remove(client)
            return

        if len(data) == 0:
            self.logger.debug("Removing client: expected zone, "
                              "received disconnect")
            self.remove(client)
            return

        zone = data.decode("utf-8", "ignore")

        self.selector.modify(client, selectors.EVENT_READ, AppServer.CLIENT)
        self.clients[client] = zone
        self.lastMessage[client] = time.time()

        self.logger.debug("Client added to zone")

    def remove(self, client):
        """Removes a client from all lists and closes it if possible."""
        try:
            self.selector.unregister(client)
        except KeyError:
            pass
        try:
            del self.clients[client]
        except KeyError:
            pass
        try:
            del self.lastMessage[client]
        except KeyError:
            pass
        try:
            client.close()
        except OSError:
            pass

    def handleMessage(self, client):
        """Handles an incoming message from a client."""
        try:
            data = client.recv(1024)
        except OSError:
            self.remove(client)
            self.logger.debug("Removing client: expected check-alive, "
                              "received OSError")
            return
        if len(data) == 0:  # Client disconnected
            self.remove(client)
            self.logger.debug("Removing client: expected check-alive, "
                              "received disconnect")
            return

        msg = data.decode("utf-8", "ignore")

        if msg == "OK":
            self.lastMessage[client] = time.time()
            self.logger.debug("Check-alive successful")
        else:
            self.remove(client)
            self.logger.debug("Removing client: expected check-alive, "
                              "received other data")
            return

    def run(self):
        """Monitors for new client connections or messages and handles them
        appropriately."""
        while True:
            events = self.selector.select()
            for key, mask in events:
                sock = key.fileobj
                type = key.data

                self.logger.debug("New message from socket")

                if type == AppServer.SERVER:
                    self.logger.debug("Accepting new client connection")
                    self.accept(sock)
                elif type == AppServer.WAITING:
                    self.logger.debug("Adding socket to zone")
                    self.addToZone(sock)
                elif type == AppServer.CLIENT:
                    self.logger.debug("Handling inbound check-alive message")
                    self.handleMessage(sock)

    def handleCheckAlive(self):
        """Periodically checks each client to ensure they are still alive
        and sending messages."""
        while True:
            clients = list(self.clients.keys())
            for client in clients:
                try:
                    if time.time() - self.lastMessage[client] > 20:
                        self.logger.debug("Removing client, no check-alive "
                                          "messages recently")
                        self.remove(client)
                except KeyError:  # Client was already removed
                    pass
                time.sleep(10 / len(clients))

    def broadcastToClient(self, item):
        """Broadcasts the appropriate current message to a single client."""
        client, zone = item
        if zone not in self.messages:
            return
        msg = json.dumps(self.messages[zone])
        try:
            client.send(msg.encode("utf-8"))
        except OSError:
            self.remove(client)

    def broadcast(self, messages):
        """Broadcasts the given messages to all clients."""
        ts = time.time()
        self.messages = messages
        self.pool.map(self.broadcastToClient, self.clients.items())
        telemetry = {"clients": len(self.clients),
                     "latency": int((time.time() - ts)*1000)}
        return telemetry
