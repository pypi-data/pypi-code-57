""" connection gate class module.

"""

import json
import socket

from mindstone.control.gates.gate import GateABC


class CommunicationGate(GateABC):
    """ communication gate class.

    The communication gate, when triggered, sends and receives data from the local
    agent. That data is then passed onto the next gate or returned.
    """

    def __init__(self, host: str):
        self.host = host
        super().__init__()
        self._socket = None

    def next(self):
        return self.children[0] if len(self.children) > 0 else None

    @property
    def socket(self) -> socket.socket:
        if self._socket is None:
            raise NotImplementedError("Connection object for this gate has not been set.")
        return self._socket

    @socket.setter
    def socket(self, s):
        self._socket = s

    def send(self, parcel: dict) -> dict:
        """Sends data to the agent driver and returns its response."""
        to_send = bytes(json.dumps(parcel).encode("utf-8"))
        self.socket.sendall(to_send)
        received_data = self.socket.recv(1024).decode("utf-8")
        return json.loads(received_data)

    def trigger(self, parcel: dict) -> tuple:
        received_data = self.send(parcel)
        return received_data, self.next()
