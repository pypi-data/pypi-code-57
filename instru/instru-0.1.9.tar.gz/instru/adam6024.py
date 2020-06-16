"""
ADAM-6024 module
Refer to the manual page 211-212
"""

from pymodbus.client.sync import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder
from time import sleep

builder = BinaryPayloadBuilder(byteorder=Endian.Big)


class Adam6024:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def __enter__(self):
        self.adam = ModbusTcpClient(self.host, self.port)
        self.adam.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.adam.close()

    def send_write_ao(self, address, value):
        # scale to 0-10V with 12-bit full range
        payload = round((value/10)*0xFFF)
        return self.adam.write_register(address, payload)

    def send_read_aio(self, address, count=1):
        return self.adam.read_holding_registers(address, count)  # Fixed count 1

    def send_write_do(self, address, value):
        return self.adam.write_coil(address, value)

    def send_read_do(self, address, value):
        return self.adam.read_coil(address, value)

    @property
    def ao0(self):
        return self.send_read_aio(10).registers[0]

    @ao0.setter
    def ao0(self, value):
        self.send_write_ao(10, value)  # address 10 maps to 4X 40011

    @property
    def ao1(self):
        return self.send_read_aio(11).registers[0]

    @ao1.setter
    def ao1(self, value):
        self.send_write_ao(11, value)  # address 11 maps to 4X 40012

    @property
    def ai0(self):
        # scale back to -10-10V with 16-bit full range
        payload = self.send_read_aio(0).registers[0]
        value = (payload / 0xFFFF) * 20 - 10
        return value

    @property
    def do0(self):
        return self.send_read_do(16)

    @do0.setter
    def do0(self, value):
        self.send_write_do(16, value)  # address 16 maps to 0X 00017


if __name__ == '__main__':
    with Adam6024('192.168.1.201', '502') as adam:  # default address at 192.168.1.201
        adam.ao0 = 9.8
        sleep(1)
        adam.ao1 = 0.2
        sleep(1)
        print(f'The ai0 readout value is::::::: {adam.ai0}')
        sleep(1)
        adam.do0 = 1
        sleep(1)
        adam.do0 = 0
