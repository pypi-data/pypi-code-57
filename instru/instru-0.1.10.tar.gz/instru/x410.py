"""
X-410 from https://www.controlbyweb.com/
Refer to the manual page 73-80
"""
import pymodbus as mb
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder, Endian
from time import sleep

RED_SET_ADDR = 18
RED_GET_ADDR = 30
GREEN_SET_ADDR = 32
GREEN_GET_ADDR = 34
YELLOW_SET_ADDR = 36
YELLOW_GET_ADDR = 38
TEST_GET_ADDR = 40

cmd_dict = {'RED_ON': 88, 'RED_OFF': 77,
            'GREEN_ON': 22, 'GREEN_OFF': 11,
            'YELLOW_ON': 66, 'YELLOW_OFF': 55,
            'TEST_ON': 44, 'TEST_OFF': 33,
            }

builder = BinaryPayloadBuilder(byteorder=Endian.Big,
                               wordorder=Endian.Big)


cmd_reg_dict = {}
for key in cmd_dict:
    builder.add_32bit_float(cmd_dict[key])
    cmd_reg_dict[key] = builder.to_registers()
    builder.reset()


class WebRelayX410:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def __enter__(self):
        self.webctrl = mb.client.sync.ModbusTcpClient(self.host, self.port)
        self.webctrl.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.webctrl.close()

    @property
    def red(self):
        payload = self.webctrl.read_holding_registers(RED_GET_ADDR, count=2).registers
        decoder = BinaryPayloadDecoder.fromRegisters(payload, byteorder=Endian.Big, wordorder=Endian.Big)
        return decoder.decode_32bit_float()

    @red.setter
    def red(self, value):
        return self.webctrl.write_registers(RED_SET_ADDR, value)

    @property
    def green(self):
        payload = self.webctrl.read_holding_registers(GREEN_GET_ADDR, count=2).registers
        decoder = BinaryPayloadDecoder.fromRegisters(payload, byteorder=Endian.Big, wordorder=Endian.Big)
        return decoder.decode_32bit_float()

    @green.setter
    def green(self, value):
        return self.webctrl.write_registers(GREEN_SET_ADDR, value)

    @property
    def yellow(self):
        payload = self.webctrl.read_holding_registers(YELLOW_GET_ADDR, count=2).registers
        decoder = BinaryPayloadDecoder.fromRegisters(payload, byteorder=Endian.Big, wordorder=Endian.Big)
        return decoder.decode_32bit_float()

    @yellow.setter
    def yellow(self, value):
        return self.webctrl.write_registers(YELLOW_SET_ADDR, value)

    # read only property
    @property
    def test(self):
        payload = self.webctrl.read_holding_registers(TEST_GET_ADDR, count=2).registers
        decoder = BinaryPayloadDecoder.fromRegisters(payload, byteorder=Endian.Big, wordorder=Endian.Big)
        return decoder.decode_32bit_float()


if __name__ == '__main__':
    with WebRelayX410('192.168.153.220', '502') as wrx:
        while True:
            # wrx.red = cmd_reg_dict['RED_ON']
            # print(f'The RED_GET_REG content is:::::::::{wrx.red}')
            # sleep(2)
            # wrx.red = cmd_reg_dict['RED_OFF']
            # print(f'The RED_GET_REG content is:::::::::{wrx.red}')
            # sleep(2)
            #
            # wrx.green = cmd_reg_dict['GREEN_ON']
            # print(f'The GREEN_GET_REG content is:::::::::{wrx.green}')
            # sleep(2)
            # wrx.green = cmd_reg_dict['GREEN_OFF']
            # print(f'The GREEN_GET_REG content is:::::::::{wrx.green}')
            # sleep(2)
            #
            # wrx.yellow = cmd_reg_dict['YELLOW_ON']
            # print(f'The YELLOW_GET_REG content is:::::::::{wrx.yellow}')
            # sleep(2)
            # wrx.yellow = cmd_reg_dict['YELLOW_OFF']
            # print(f'The YELLOW_GET_REG content is:::::::::{wrx.yellow}')
            # sleep(2)

            print(f'The TEST_GET_REG content is:::::::::{wrx.test}')
