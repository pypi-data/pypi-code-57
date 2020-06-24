"""
Mocks modbus reads so you don't have to have a modbus slave configured
"""
import random
import logging

log = logging.getLogger(__name__)


class MockReadRegistersResponse:
    '''
    Base class for responsing to a modbus register read
    '''

    _rtu_byte_count_pos = 2

    def __init__(self, values, **kwargs):
        ''' Initializes a new instance

        :param values: The values to write to
        '''
        self.registers = values or []

    def encode(self):
        ''' Encodes the response packet

        :returns: The encoded packet
        '''

    def decode(self, data):
        ''' Decode a register response packet

        :param data: The request to decode
        '''

    def getRegister(self, index):
        ''' Get the requested register

        :param index: The indexed register to retrieve
        :returns: The request register
        '''
        return self.registers[index]

    def isError(self):
        """Checks if the error is a success or failure"""
        return False

    def __str__(self):
        ''' Returns a string representation of the instance

        :returns: A string representation of the instance
        '''
        return "ReadRegisterResponse (%d)" % len(self.registers)


class ModbusBaseMock:
    def __init__(self, *args, **kwargs):
        self.mock_spec = {}

    def add_to_mock_spec(self, mock_spec):
        """
        Adds to the existing mock spec
        Values that are not specified in the mock spec default to random numbers
        :param mock_spec: Dictionary of form {'unit': {'address': handle, args, kwargs}}
        :return:
        """
        for unit in mock_spec:
            if unit not in self.mock_spec:
                self.mock_spec[unit] = mock_spec[unit]
            else:
                for address in mock_spec[unit]:
                    self.mock_spec[unit][address] = mock_spec[unit][address]

    def run_spec_handlers(self, address, words, unit, boolean=False):
        resp = []
        for addr in range(address, address + words):
            try:
                handle, args, kwargs = self.mock_spec[unit][addr]
            except KeyError:
                if boolean:
                    resp.append(random.choice([True, False]))
                else:
                    resp.append(random.randint(0, (1 << 16) - 1))
                continue
            try:
                # Try to run the handle as a generator first
                resp.append(next(handle))
            except TypeError:
                # Run the handler with the appropriate arguments
                resp.append(handle(*args, **kwargs))
        return MockReadRegistersResponse(resp)


class ModbusAsyncProtocolMock(ModbusBaseMock):

    async def read_holding_registers(self, address, words, unit=0):
        return self.run_spec_handlers(address, words, unit)

    async def read_input_registers(self, address, words, unit=0):
        return self.run_spec_handlers(address, words, unit)

    async def write_coil(self, address, value, unit=0):
        log.debug(f"Writing coil @ {address}: {value}")

    async def write_register(self, address, value, unit=0):
        log.debug(f"Writing register @ {address}: {value}")


class ModbusSyncClientMock(ModbusBaseMock):
    def read_holding_registers(self, address, words, unit=None):
        return self.run_spec_handlers(address, words, unit)

    def read_input_registers(self, address, words, unit=None):
        return self.run_spec_handlers(address, words, unit)

    def write_coil(self, address, value, unit=0):
        log.info(f"Writing coil @ {address}: {value}")

    def write_register(self, address, value, unit=0):
        log.info(f"Writing register @ {address}: {value}")


class ModbusAsyncClientMock:
    """

    """

    def __init__(self):
        self.protocol = ModbusAsyncProtocolMock()

    def __getattr__(self, item):
        return self.protocol.__getattribute__(item)
