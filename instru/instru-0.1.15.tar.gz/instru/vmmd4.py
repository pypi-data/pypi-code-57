"""
ViewMarq MD4-0424 module from http://www.automationdirect.com/
"""

from pymodbus.client.sync import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder
from time import sleep

CMD_STRING_BUFFER_ADDR = 411000 - 400001

what = 100

TEST_STRING = f"<ID 1><CLR><WIN 0 0 287 31><POS 0 0><LJ><BL N><CS 0><GRN><T>AOGGGG!!!???:{what}</T><POS 0 8><LJ><T>DISPLAY</T><POS 0 16><LJ><T>TEST</T><POS 0 24><LJ><T>OK</T>\r"


class VmMd40424:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def __enter__(self):
        self.vm = ModbusTcpClient(self.host, self.port)
        self.vm.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.vm.close()

    @property
    def command_string_buffer(self):
        pass
        # result = self.vm.read_holding_registers(CMD_STRING_BUFFER_ADDR, 117)
        # decoder = BinaryPayloadDecoder.fromRegisters(result.registers,
        #                                              byteorder=Endian.Big, wordorder=Endian.Little)
        #
        # return decoder.decode_string(234)

    @command_string_buffer.setter
    def command_string_buffer(self, value):
        builder = BinaryPayloadBuilder(byteorder=Endian.Big, repack=True)
        builder.add_string(value)
        payload = builder.to_registers()
        # use individual write to work around max 255 restriction bought by write_registers
        for index, each_payload in enumerate(payload):
            result = self.vm.write_register(CMD_STRING_BUFFER_ADDR+index, each_payload)
            print(f'write {each_payload} at index of {index} with result of {result}')


if __name__ == '__main__':
    with VmMd40424('192.168.153.250', '502') as vm:
        vm.command_string_buffer = TEST_STRING
