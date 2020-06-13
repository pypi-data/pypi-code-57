
import serial


class SerialWithLog(serial.Serial):
    def __init__(self, port, baud, parity, stop_bits):
        self._read_log = b''
        self._write_log = b''

        super().__init__(port, baud, parity=parity, stopbits=stop_bits, timeout=0, write_timeout=0)

    def read(self, size=1):
        data = super().read(size)
        self._read_log += data

        return data

    def read_available(self):
        data = b''
        while self.is_open:
            available = self.in_waiting
            if not available:
                break

            data += self.read(available)

        return data

    def write(self, data):
        self._write_log += data

        return super().write(data)

    def reset_log(self):
        self._read_log = b''
        self._write_log = b''

    @property
    def read_log(self):
        return self._read_log

    @property
    def write_log(self):
        return self._write_log
