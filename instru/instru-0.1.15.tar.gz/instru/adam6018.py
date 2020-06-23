"""
ADAM-6018 module
Refer to the manual page 220-223
"""

from pymodbus.client.sync import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder
from time import sleep

builder = BinaryPayloadBuilder(byteorder=Endian.Big)


class Adam6018:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def __enter__(self):
        self.adam = ModbusTcpClient(self.host, self.port)
        self.adam.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.adam.close()

    def send_read_ai(self, address, count=1):
        return self.adam.read_holding_registers(address, count)  # Fixed count 1

    @property
    def ai0(self):  # type T thermal couple with range of -100 ~ +400 C degree
        return (self.send_read_ai(0).registers[0] / 0xFFFF) * 500 - 100

    @property
    def ai1(self):
        return (self.send_read_ai(1).registers[0] / 0xFFFF) * 500 - 100

    @property
    def ai2(self):
        return (self.send_read_ai(2).registers[0] / 0xFFFF) * 500 - 100

    @property
    def ai3(self):
        return (self.send_read_ai(3).registers[0] / 0xFFFF) * 500 - 100

    @property
    def ai4(self):
        return (self.send_read_ai(4).registers[0] / 0xFFFF) * 500 - 100

    @property
    def ai5(self):
        return (self.send_read_ai(5).registers[0] / 0xFFFF) * 500 - 100

    @property
    def ai6(self):
        return (self.send_read_ai(6).registers[0] / 0xFFFF) * 500 - 100

    @property
    def ai7(self):
        return (self.send_read_ai(7).registers[0] / 0xFFFF) * 500 - 100


if __name__ == '__main__':
    with Adam6018('192.168.153.190', '502') as adam:
        for i in range(8):
            print(f"The ai{i} readout value is::::::: {getattr(adam, f'ai{i}')}")


