import os
from time import time

import portalocker

PROJECT_ROOT = os.path.abspath(os.getcwd())
if "pfs" not in PROJECT_ROOT:
    print("\033[1;31mThis package must be run within the TJREVERB pFS directory!\033[0;0m")
    print("\033[1;33mAssuming this is being run as a test of the package, output to folder `pfs-output`\033[0;0m")
    PROJECT_ROOT = os.path.join(PROJECT_ROOT, "pfs-output")
else:
    while not PROJECT_ROOT.endswith("pfs"):
        PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)
    PROJECT_ROOT = os.path.join(PROJECT_ROOT, "pfs-output")


class SerialException(Exception):
    pass


class Serial:

    def __init__(self, port=None, buadrate=9600, timeout=float('inf')):
        self.port = port
        self.baudrate = buadrate
        self.timeout = timeout

        self.read_filename = None
        self.write_filename = None

        if not os.path.exists(PROJECT_ROOT):
            os.makedirs(PROJECT_ROOT)

        if self.port:
            self.open()

    @property
    def is_open(self):
        return not (self.read_filename is None and self.write_filename is None)

    def open(self):
        if self.port is None:
            raise SerialException('Port must be configured before it can be used.')

        self.read_filename = os.path.join(PROJECT_ROOT, self.port + '_pfs_rx.serial')
        self.write_filename = os.path.join(PROJECT_ROOT, self.port + '_pfs_tx.serial')

    def close(self):
        if self.is_open:
            self.read_filename = None
            self.write_filename = None

    def flushInput(self):
        if not self.is_open:
            raise SerialException("Attempting to use a port that is not open")

        with portalocker.Lock(self.read_filename, 'w') as rx:
            pass

    def flushOutput(self):
        if not self.is_open:
            raise SerialException("Attempting to use a port that is not open")

        with portalocker.Lock(self.write_filename, 'w') as tx:
            pass

    def write(self, message):
        if not self.is_open:
            raise SerialException("Attempting to use a port that is not open")

        if type(message) != bytes:
            raise SerialException("Send the serial port bytes")

        with portalocker.Lock(self.write_filename, 'a') as tx:
            tx.write(message.decode('utf-8'))

    def read(self, size=1):
        if not self.is_open:
            raise SerialException("Attempting to use a port that is not open")

        if size > 1:
            print("\033[1;33mOnly one byte/call with reverb-serial\033[0;0m")

        start = time()
        while time() - start < self.timeout:
            rx_content = None
            with portalocker.Lock(self.read_filename, 'r', timeout=self.timeout) as rx:
                rx_content = rx.read()

            if rx_content:
                nb = rx_content[0].encode('utf-8')
                with portalocker.Lock(self.read_filename, 'w') as rx:
                    rx.write(rx_content[1:])
                return nb

        return b''
