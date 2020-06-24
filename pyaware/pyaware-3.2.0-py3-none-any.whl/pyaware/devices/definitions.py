import asyncio
import logging
import typing
from threading import Lock
import math
import async_timeout
from pymodbus.constants import Endian
from pymodbus.exceptions import ConnectionException
from pymodbus.payload import BinaryPayloadDecoder, BinaryPayloadBuilder

log = logging.getLogger(__file__)
number = typing.Union[int, float]


class DATATYPES:
    """
    Data types as defined in BinaryPayloadDecoder
    """
    UINT16 = "16bit_uint"
    UINT32 = "32bit_uint"
    UINT64 = "64bit_uint"
    SINT16 = "16bit_int"
    SINT32 = "32bit_int"
    SINT64 = "64bit_int"
    FLOAT32 = "32bit_float"
    FLOAT64 = "64bit_float"


class EIPCommands:
    description = "Logix PLC read tags with pylogix"

    def __init__(self, tag_name):
        self.tag_name = tag_name

    def sync_read(self, client):
        """
        :param client: The EIP client to use
        :return:
        """
        response = client.Read(self.tag_name)
        return response

    def sync_write(self, client, unit, value):
        """
        write EIP Tag
        """


class EnumConverter:
    def __init__(self, enum_dec: dict, *args, **kwargs):
        self.enum_dec = enum_dec

    def decode(self, payload):
        try:
            return self.enum_dec.get(payload)
        except KeyError:
            return None

    def encode(self, data: dict):
        '''
        TODO: Test this function
        This has not been tested
        :param data: Input dictionary containing values to encode with their parameters
        :return: Output dictionary containing encoded values to be sent to the device
        '''
        output = {}
        new_enum = dict((v, k) for k, v in self.enum_dec.items())
        for k, v in data:
            try:
                output[k] = new_enum.get(v)
            except KeyError:
                output[k] = None
        return output


class ModbusRegister:
    description = "Modbus Register"
    status_or_command = "Status"  # "Status" or "Command"
    device_write = True  # Can this receive writes?

    def __init__(self, address, words, data_type, byteorder=Endian.Big, wordorder=Endian.Big, scale: number = 1,
                 converter=None, nan_convert=math.nan):
        """
        :param address: Modbus Address
        :param words: How many 2 byte words this data represents
        :param data_type: datatype as specified in DATATYPES global
        :param byteorder: Endian for the bytes
        :param wordorder: Endian of the words
        WX YZ byte order by default. Big endian bytes and words
        :param scale_multiplier: Multiplier when converting the numbers. IE if frequency reads as 50000 for 50Hz
          then scale = 0.01
        :param converter: Object that has encode and decode to cast the result into the appropriate data format
        """
        self.address = address
        self.words = words
        self.byteorder = byteorder
        self.wordorder = wordorder
        self.parameter_type = data_type
        self._decode_handle = "decode_{}".format(data_type)
        self.scale_multiplier = scale
        self.converter = converter
        self.nan_convert = nan_convert

    def decode(self, payload):
        log.debug("Attemting to decode the register")
        log.debug("{}".format(payload))
        decoder = BinaryPayloadDecoder.fromRegisters(payload, byteorder=self.byteorder, wordorder=self.wordorder)
        log.debug("Decoder retrieved")
        raw = getattr(decoder, self._decode_handle)()
        try:
            if math.isnan(raw):
                raw = self.nan_convert
        except TypeError:
            pass
        converted = raw * self.scale_multiplier
        if self.converter:
            converted = self.converter.decode(converted)
        return converted

    def encode(self, value):
        log.debug("Attemting to encode the register")
        log.debug("{}".format(value))
        if self.converter:
            value = self.converter.encode(value)
        raw = value // self.scale_multiplier
        encoder = BinaryPayloadBuilder(byteorder=self.byteorder, wordorder=self.wordorder)
        getattr(encoder, "add_{}".format(self.parameter_type))(raw)
        return encoder.to_registers()

    def sync_read(self, client, unit):
        raise NotImplementedError

    async def async_read(self, client, unit, timeout=1):
        raise NotImplementedError

    def sync_write(self, client, unit, value):
        raise NotImplementedError

    async def async_write(self, client, unit, value):
        raise NotImplementedError

    def sync_update(self, client, unit: int, reg_id: str, value: bool):
        raise NotImplementedError

    async def async_update(self, client, unit: int, reg_id: str, value: bool):
        raise NotImplementedError

    def __repr__(self):
        return "<{} address: {} words: {} type: {}>".format(self.__class__.__name__, self.address, self.words,
                                                            self.parameter_type)


class ModbusHolding(ModbusRegister):
    """
    Big endian
    """
    description = "Modbus Holding Register"
    status_or_command = "Status"  # "Status" or "Command"
    device_write = True  # Can this receive writes?

    def sync_read(self, client, unit):
        """
        :param client: The modbus client to use
        :param unit: int. The unit or slave address to read
        :return:
        """
        response = client.read_holding_registers(self.address, self.words, unit=unit)
        if response.isError():
            log.warning("Invalid reads for address {} unit {}\nMessage:{}".format(self.address, unit, response))
        else:
            return self.decode(response.registers)

    async def async_read(self, client, unit, timeout=1):
        cm = None
        try:
            log.debug("About to await")
            with async_timeout.timeout(timeout) as cm:
                response = await client.protocol.read_holding_registers(self.address, self.words, unit=unit)
        except asyncio.TimeoutError:
            if cm is not None and cm.expired:
                log.debug("Async read expired")
            raise
        except AttributeError as e:
            if "NoneType" in e.args[0] and "read_holding_registers" in e.args[0]:
                log.debug("No connection present")
                return None
            else:
                raise
        except ConnectionException as e:
            log.exception(e)
            return None
        if response.isError():
            log.warning("Invalid reads for address {} unit {}\nMessage:{}".format(self.address, unit, response))
        else:
            log.debug("Read holding registers {} complete".format(self.address))
            return self.decode(response.registers)

    def sync_write(self, client, unit, value):
        client.write_register(self.address, value, unit=unit)
        return self.sync_read(client, unit=unit) == value

    async def async_write(self, client, unit, value):
        await client.write_register(self.address, value, unit=unit)
        return await self.async_read(client, unit=unit) == value

    def sync_update(self, client, unit: int, reg_id: str, value: bool):
        return self.sync_write(client, unit=unit, value=value)

    async def async_update(self, client, unit: int, reg_id: str, value: bool):
        return await self.async_write(client, unit=unit, value=value)


class ModbusInput(ModbusRegister):
    """
    Big endian
    """
    description = "Modbus Input Register"
    status_or_command = "Status"  # "Status" or "Command"
    device_write = False  # Can this receive writes?

    def sync_read(self, client, unit):
        """
        :param client: The modbus client to use
        :param unit: int. The unit or slave address to read
        :return:
        """
        response = client.read_input_registers(self.address, self.words, unit=unit)
        if response.isError():
            log.warning("Invalid reads for address {} unit {}\nMessage:{}".format(self.address, unit, response))
        else:
            return self.decode(response.registers)

    async def async_read(self, client, unit, timeout=1):
        cm = None
        try:
            log.debug("About to await")
            with async_timeout.timeout(timeout) as cm:
                response = await client.protocol.read_input_registers(self.address, self.words, unit=unit)
        except asyncio.TimeoutError:
            if cm is not None and cm.expired:
                log.debug("Async read expired")
            raise
        except AttributeError as e:
            if "NoneType" in e.args[0] and "read_holding_registers" in e.args[0]:
                log.debug("No connection present")
                return None
            else:
                raise
        except ConnectionException as e:
            log.exception(e)
            return None
        if response.isError():
            log.warning("Invalid reads for address {} unit {}\nMessage:{}".format(self.address, unit, response))
        else:
            log.debug("Read holding registers {} complete".format(self.address))
            return self.decode(response.registers)


class ModbusBitMask_Input(ModbusInput):
    def __init__(self, *args, bitmask: dict, **kwargs):
        """
        :param bitmask Dictionary for sparse mapping of bits to bitshifted value
        eg. {"Status": 0, "Connection Status": 5}
        Would be 1 << 0 as "Status" and 1 << 5 as "Connection Status"
        Also needs the params for the parent ModbusHolding
        """
        if kwargs.get("scale", 1) != 1:
            raise ValueError("Bit masks are bitwise registers and cannot scale")

        class Converter:
            def encode(self, value: dict):
                converted = 0
                try:
                    return value["_raw"]
                except KeyError:
                    pass
                for k, v in value.items():
                    converted |= bitmask[k] << v
                return converted

            def decode(self, payload):
                converted = {k: bool(payload & 1 << v) for k, v in bitmask.items()}
                converted["_raw"] = payload
                return converted

        handle = kwargs.pop("convert_handle", Converter())

        super().__init__(*args, converter=handle, **kwargs)
        self.bitmask = bitmask

    def sync_update(self, client, unit: int, bit_id: str, value: bool):
        mask = 1 << self.bitmask[bit_id]
        try:
            v = self.sync_read(client, unit=unit)["_raw"]
        except TypeError:
            log.warning(
                "No value read from address {}\n"
                "Cannot write bit to this register without knowing the original value".format(self.address)
            )
            return None
        v &= ~mask
        if value:
            v |= mask
        return self.sync_write(client, unit=unit, value=v)

    async def async_update(self, client, unit: int, bit_id: str, value: bool):
        mask = 1 << self.bitmask[bit_id]
        v = int(await self.async_read(client, unit=unit))
        v &= ~mask
        if value:
            v |= mask
        return await self.async_write(client, unit=unit, value=v)


class ModbusBitMask(ModbusHolding):
    def __init__(self, *args, bitmask: dict, **kwargs):
        """
        :param bitmask Dictionary for sparse mapping of bits to bitshifted value
        eg. {"Status": 0, "Connection Status": 5}
        Would be 1 << 0 as "Status" and 1 << 5 as "Connection Status"
        Also needs the params for the parent ModbusHolding
        """
        if kwargs.get("scale", 1) != 1:
            raise ValueError("Bit masks are bitwise registers and cannot scale")

        class Converter:
            def encode(self, value: dict):
                converted = 0
                try:
                    return value["_raw"]
                except KeyError:
                    pass
                for k, v in value.items():
                    converted |= bitmask[k] << v
                return converted

            def decode(self, payload):
                converted = {k: bool(payload & 1 << v) for k, v in bitmask.items()}
                converted["_raw"] = payload
                return converted

        handle = kwargs.pop("convert_handle", Converter())

        super().__init__(*args, converter=handle, **kwargs)
        self.bitmask = bitmask

    def sync_update(self, client, unit: int, bit_id: str, value: bool):
        mask = 1 << self.bitmask[bit_id]
        try:
            v = self.sync_read(client, unit=unit)["_raw"]
        except TypeError:
            log.warning(
                "No value read from address {}\n"
                "Cannot write bit to this register without knowing the original value".format(self.address)
            )
            return None
        v &= ~mask
        if value:
            v |= mask
        return self.sync_write(client, unit=unit, value=v)

    async def async_update(self, client, unit: int, bit_id: str, value: bool):
        mask = 1 << self.bitmask[bit_id]
        v = int(await self.async_read(client, unit=unit))
        v &= ~mask
        if value:
            v |= mask
        return await self.async_write(client, unit=unit, value=v)


class Device:
    read_timeout = None
    data_info = None
    port_id = ""

    def __init__(self, dev_id: str, dev_type: str = "", read_timeout=None, data_info=None):
        if data_info:
            self.data_info = data_info
        if self.data_info is None:
            self.data_info = {}
        self.dev_id = dev_id
        if read_timeout is not None:
            self.read_timeout = read_timeout
        # Initialise data
        self.data = {k: [] for k in self.data_info}
        if dev_type:
            self.dev_type = dev_type
        else:
            self.dev_type = self.__class__.__name__

    def sync_read_data(self, lock=None):
        """
        Read data from the device and store in a buffer until next report_data is called
        :return: None
        """

    async def async_read_data(self, lock=None):
        """
        Reads the modbus addresses and buffers them until the next report_data call
        :return:
        """

    def iter_data(self):
        for k, v in self.data.items():
            yield self.dev_id, self.dev_type, k, v


class EIPDevice(Device):

    def __init__(self, client=None, *args, lock=None, **kwargs):
        """
        :param dev_id: device id as reported to the cloud
        :param lock: lock is a threading or asyncio lock. Required for EIP as the library is not threadsafe.
        Recommend that you directly use a EIPNursery to manage the locking.
        """
        super().__init__(*args, **kwargs)
        self.client = client
        self.lock = lock

    def set_client(self, client):
        """
        :param client: The EIP client to use
        :return:
        """
        self.client = client

    def sync_read_data(self, lock=None):
        """
        Reads the EIP Data and buffers them until the next report_data call
        :return:
        """
        for ident, info in self.data_info.items():
            lock = lock or self.lock
            if lock:
                with lock:
                    resp = info.sync_read(self.client)
            else:
                resp = info.sync_read(self.client)
            if resp is not None:
                if isinstance(resp, dict):
                    self.data[ident].append(resp.pop("_raw"))
                    for k, v in resp.items():
                        try:
                            self.data[k].append(v)
                        except KeyError:
                            self.data[k] = [v]
                else:
                    self.data[ident].append(resp)

    async def async_read_data(self, lock=None):
        """
        """
        loop = asyncio.get_event_loop()
        loop.run_in_executor(None, self.sync_read_data, lock)


class ModbusDevice(Device):

    def __init__(self, unit=0, client=None, *args, **kwargs):
        """
        :param unit: slave address
        :param dev_id: device id as reported to the cloud
        """
        super().__init__(*args, **kwargs)
        self.unit = unit
        self.client = client

    def set_client(self, client):
        """
        :param client: The modbus client to use
        :return:
        """
        self.client = client

    def sync_read_data(self, lock=None):
        """
        Reads the modbus addresses and buffers them until the next report_data call
        :return:
        """
        for ident, info in self.data_info.items():
            resp = info.sync_read(self.client, self.unit)
            if resp is not None:
                if isinstance(resp, dict):
                    self.data[ident].append(resp.pop("_raw"))
                    for k, v in resp.items():
                        try:
                            self.data[k].append(v)
                        except KeyError:
                            self.data[k] = [v]
                else:
                    self.data[ident].append(resp)

    async def async_read_data(self, lock=None):
        """
        Reads the modbus addresses and buffers them until the next report_data call
        :return:
        """
        for ident, info in self.data_info.items():
            try:
                resp = await info.async_read(self.client, self.unit, self.read_timeout)
            except asyncio.TimeoutError:
                log.info("Device {} timed out, skipping remaining modbus reads".format(self.dev_id))
                break
            if resp is not None:
                if isinstance(resp, dict):
                    self.data[ident].append(resp.pop("_raw"))
                    for k, v in resp.items():
                        try:
                            self.data[k].append(v)
                        except KeyError:
                            self.data[k] = [v]
                else:
                    log.debug("read {} from slave {} address {}".format(resp, self.unit, info.address))
                    self.data[ident].append(resp)

    def sync_update(self, register_id, value):
        reg = self.get_modbus_id(register_id)
        return reg.sync_update(self.client, self.unit, register_id, value)

    async def async_update(self, register_id, value):
        reg = self.get_modbus_id(register_id)
        return await reg.async_update(self.client, self.unit, register_id, value)

    def get_modbus_id(self, item):
        try:
            return self.data_info[item]
        except KeyError:
            for itm in self.data_info.values():
                if isinstance(itm, ModbusBitMask):
                    if item in itm.bitmask:
                        return itm
            raise

    def __getitem__(self, item):
        self.get_modbus_id(item)


class ModbusRTU(ModbusDevice):
    pass


class ModbusTCP(ModbusDevice):
    pass


class DeviceGroup:
    """
    Base class to indicate a grouping of devices to schedule together
    """
    port_id = ""

    def __init__(self, client=None):
        self.client = client
        self.devices = []

    def set_client(self, client):
        self.client = client
        for device in self.devices:
            device.set_client(self.client)

    def add_devices(self, *args):
        """
        :param args: Devices to add of type ModbusDevice
        :return:
        """
        self.devices.extend(args)
        self.set_client(self.client)

    def iter_data(self):
        for device in self.devices:
            yield from device.iter_data()


class EIPNursery(DeviceGroup):
    def __init__(self, client=None):
        super().__init__(client)
        self.lock = Lock()

    def sync_read_data(self):
        for device in self.devices:
            device.sync_read_data(lock=self.lock)

    async def async_read_data(self):
        for device in self.devices:
            await device.async_read_data(lock=self.lock)


class ModbusNursery(DeviceGroup):
    """
    Nursery for grouping modbus devices.
    Used for when devices share a common resource such as a serial port.
    """

    def __init__(self, client=None, timeout=0.3):
        super().__init__(client)
        self.read_timeout = timeout

    def sync_read_data(self):
        for device in self.devices:
            device.sync_read_data()

    async def async_read_data(self):
        for device in self.devices:
            await device.async_read_data()


def build_data_reads(parameters, device_type):
    data_reads = {}
    for param in parameters:
        param_data = device_type[param]["device-level"]
        base_class = globals()[param_data.pop("class")]
        data_reads[param] = base_class(**param_data)
    return data_reads


def build_commands():
    pass


def build_events():
    pass


def offset_modbus(offset: int, device: Device) -> Device:
    for register in device.data_info.values():
        register.address += offset
    return device


class MOCKREGISTER(ModbusRTU):
    read_timeout = 0.5
    data_info = {
        "Status Trips": ModbusHolding(address=0, words=1, data_type=DATATYPES.UINT16),
    }


class MOCKBIGDEVICE(ModbusRTU):
    read_timeout = 0.5
    data_info = {"Status Trips {}".format(x): ModbusHolding(address=x, words=1, data_type=DATATYPES.UINT16) for x in
                 range(1000)}


protocol_map = {
    "modbus_rtu": ModbusRTU,
    "modbus_tcp": ModbusTCP,
}
