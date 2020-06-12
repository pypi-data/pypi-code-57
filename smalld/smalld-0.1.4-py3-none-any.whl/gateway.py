import json

from attrdict import AttrDict
from websocket import ABNF, WebSocket, WebSocketException

from .exceptions import NetworkError
from .logger import logger

WebSocketError = (WebSocketException, OSError)


class CloseReason:
    def __init__(self, code, reason):
        self.code = code
        self.reason = reason

    def __str__(self):
        return f"{code}: {reason}"

    @staticmethod
    def parse(data):
        code = int.from_bytes(data[:2], "big")
        reason = data[2:].decode("utf-8")
        return CloseReason(code, reason)


class Gateway:
    def __init__(self, url):
        self.url = url
        self.ws = WebSocket()
        self.close_reason = None

    def __iter__(self):
        try:
            self.ws.connect(self.url)
        except WebSocketError:
            raise NetworkError

        while self.ws.connected:
            try:
                with self.ws.readlock:
                    opcode, data = self.ws.recv_data()
            except WebSocketError:
                return

            if data and opcode == ABNF.OPCODE_CLOSE:
                self.close_reason = CloseReason.parse(data)
                return

            if data and opcode == ABNF.OPCODE_TEXT:
                decoded_data = data.decode("utf-8")
                yield AttrDict(json.loads(decoded_data))

        logger.info("Gateway Closed: %s", self.close_reason)

    def send(self, data):
        try:
            self.ws.send(data)
        except WebSocketError:
            raise NetworkError

    def close(self):
        self.ws.close()
