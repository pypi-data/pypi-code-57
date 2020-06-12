import socket
from .protocol import send_data, ProtocolType, scan
from .bytecodes import *
from typing import List

LD686_PORT = 5577

class LD686:
    def __init__(self, host):
        self.host = host

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, LD686_PORT))

        self._on = False
        self._white = 0
        self._white2 = 0
        self._rgb = (0, 0, 0)
        self._program = 0
        self._program_speed = 0

    @property
    def on(self) -> bool:
        return self._on

    @property
    def rgb(self) -> List[int]:
        return self._rgb

    @property
    def white(self) -> int:
        return self._white

    @property
    def white2(self) -> int:
        return self._white2

    @property
    def program(self) -> int:
        return self._program

    @property
    def program_speed(self) -> int:
        return self._program_speed

# ====== Setters

    @on.setter
    def on(self, value: bool) -> None:
        self._on = value
        self._push_power()

    @rgb.setter
    def rgb(self, value: int) -> None:
        self._rgb = value
        self._push_color()

    @white.setter
    def white(self, value: int) -> None:
        self._white = value
        self._push_color()

    @white2.setter
    def white2(self, value: int) -> None:
        self._white2 = value
        self._push_color()

    @program.setter
    def program(self, value: int) -> None:
        self._program = value
        self._push_program()

    @program_speed.setter
    def program_speed(self, value: int) -> int:
        self._program_speed = value
        self._push_program()

# ====== Raw Access

    def send_raw(self, *args):
        self._send(*args)

# ====== Push State

    def _push_color(self):
        self._send(BYTE_MSGTYPE_COLOR, self._rgb[0], self._rgb[1], self._rgb[2], self._white, self._white2, BYTE_END)

    def _push_program(self):
        self._send(BYTE_MSGTYPE_PROGRAM, self._program, self._program_speed)

    def _push_power(self):
        self._send(BYTE_MSGTYPE_POWER, BYTE_POWER_ON if self._on else BYTE_POWER_OFF)

    def _send(self, *args):
        send_data(bytes(args), ProtocolType.LD686, self.sock)

    @staticmethod
    def scan(seconds: int) -> dict:
        return scan(seconds)

        