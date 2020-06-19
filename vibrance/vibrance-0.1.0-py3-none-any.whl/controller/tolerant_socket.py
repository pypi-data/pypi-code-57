import socket
import logging
import json


class TolerantSocket:
    def __init__(self, debug_level=logging.CRITICAL):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(debug_level)
        self.logger.info("Created tolerant socket")

        self.health = "inactive"
        self.message = "Not Connected"

    def connect(self, host, port, psk=None, ssl_context=None):
        self.logger.info("Set target at %s:%i", host, port)
        self.host = host
        self.port = port
        self.psk = psk
        self.context = ssl_context

        self.makeSocket()

    def makeSocket(self):
        self.logger.info("Creating new socket object...")
        unwrapped = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        unwrapped.settimeout(2)

        if self.context:
            self.socket = self.context.wrap_socket(unwrapped,
                                                   server_hostname=self.host)
        else:
            self.socket = unwrapped

        try:
            self.socket.connect((self.host, self.port))
        except OSError:  # ConnectionError:
            self.close(f"Connection to {self.host} failed")
        except socket.timeout:
            self.close(f"Connection to {self.host} timed out")
        except socket.gaierror:
            self.close(f"{self.host} is not a valid address")
        else:
            if self.psk:
                if self.authenticate():
                    self.health = "success"
                    self.message = f"Connected to {self.host}"
            else:
                self.health = "success"
                self.message = f"Connected to {self.host}"

    def authenticate(self):
        self.logger.info("Attempting auth...")
        self.send(self.psk.encode("utf-8"))
        if self.socket:
            try:
                data = self.socket.recv(1024)
            except ConnectionError:
                self.close(f"Connection to {self.host} failed")
            except socket.timeout:
                self.close(f"Connection to {self.host} timed out")
            else:
                if data == b"OK":
                    return True
                else:
                    self.close("Authentication failed")
        return False

    def send(self, data):
        if self.socket:
            try:
                self.socket.send(data)
            except ConnectionError:
                self.close(f"Connection to {self.host} failed")
            except socket.timeout:
                self.close(f"Connection to {self.host} timed out")
            else:
                self.logger.debug("Send successful")
        else:
            self.logger.error("Failed to send, not connected")

    def recv(self, length):
        if self.socket:
            try:
                data = self.socket.recv(length)
            except ConnectionError:
                self.close(f"Connection to {self.host} failed")
            except socket.timeout:
                self.close(f"Connection to {self.host} timed out")
            else:
                if len(data) == 0:
                    self.logger.error("Socket disconnected")
                    self.close(f"Connection to {self.host} failed")
                else:
                    self.logger.debug("Recv successful, returned %s", data)
                    return data
        else:
            self.logger.error("Failed to recv, not connected")

    def repair(self):
        if not self.socket:
            self.logger.info("Attempting repair...")
            self.makeSocket()

    def recvJSON(self, length=1024):
        data = self.recv(length)
        if data:
            try:
                data = data.decode("utf-8")
            except UnicodeDecodeError:
                self.logger.error("Invalid UTF-8 received")
                return None
            else:
                try:
                    data = json.loads(data)
                except json.JSONDecodeError:
                    self.logger.error("Invalid JSON received")
                    return None
                else:
                    return data

    def close(self, reason=None):
        self.logger.info("Closing socket: %s",
                         (reason if reason is not None else "No errors"))
        if self.socket:
            self.socket.close()
            self.socket = None

        if reason is not None:
            self.health = "failure"
            self.message = reason
        else:
            self.health = "inactive"
            self.message = "Not Connected"

    def getStatus(self):
        return {"health": self.health, "message": self.message}
