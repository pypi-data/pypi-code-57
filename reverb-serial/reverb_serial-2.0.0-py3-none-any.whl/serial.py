import os
from time import time
from socket import socket, AF_INET, SOCK_DGRAM
from random import randint


class SerialException(Exception):
    pass


class Serial:
    UDP_PORT = {
        '/dev/ttyACM0': 5005,
        '/dev/serial0': 6005,
    }

    def __init__(self, port=None, baudrate=9600, timeout=None, invert=False):
        if port is None:
            self.name = port
            self.port = port
        else:
            self.name = port
            self.port = self.UDP_PORT[port] if port in self.UDP_PORT else randint(5000, 600)

        self.rx = socket(AF_INET, SOCK_DGRAM)
        if timeout:
            self.rx.settimeout(timeout)
        self.tx = socket(AF_INET, SOCK_DGRAM)
        self.move = 1 if invert else -1

        self.is_open = False
        self.binded = False
        self.error = False

        self.input_buffer = b''

        if self.port:
            self.open()

    def open(self):
        if self.port is None:
            raise SerialException('Port must be configured before it can be used.')

        if self.is_open:
            raise SerialException('Port is already open.')

        if self.error:
            raise SerialException(f'Serial port {self.name} has disconnected')

        self.is_open = True

        if not self.binded:
            self.binded = True
            self.rx.bind(('127.0.0.1', self.port - self.move))

    def close(self):
        if self.error:
            raise SerialException(f'Serial port {self.name} has disconnected')

        self.is_open = False

    def flushInput(self):
        if not self.is_open:
            raise SerialException("Attempting to use a port that is not open")

        if self.error:
            raise SerialException(f'Serial port {self.name} has disconnected')

        self.input_buffer = b''

    def flushOutput(self):
        if not self.is_open:
            raise SerialException("Attempting to use a port that is not open")

        if self.error:
            raise SerialException(f'Serial port {self.name} has disconnected')

    def write(self, message):
        if not self.is_open:
            raise SerialException("Attempting to use a port that is not open")

        if self.error:
            raise SerialException(f'Serial port {self.name} has disconnected')

        if type(message) != bytes:
            raise SerialException("Send the serial port bytes")

        try:
            self.tx.sendto(message, ('127.0.0.1', self.port + self.move))
        except Exception as exception:
            raise SerialException(str(exception))

    def read(self, size=1):
        if not self.is_open:
            raise SerialException("Attempting to use a port that is not open")

        if self.error:
            raise SerialException(f'Serial port {self.name} has disconnected')

        if len(self.input_buffer) >= size:
            r = self.input_buffer[0:size]
            self.input_buffer = self.input_buffer[size:]
            return r

        try:
            data, address = self.rx.recvfrom(1024)
            self.input_buffer += data
            r = self.input_buffer[0:size]
            self.input_buffer = self.input_buffer[size:]
            return r

        except Exception as exception:
            if 'timed out' in str(exception):
                return b''

            raise SerialException(str(exception))
