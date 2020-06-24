from __future__ import annotations
import asyncio
import logging
import socket
import struct
from datetime import datetime
from functools import partial
import typing
from pyaware import events
import pyaware.triggers
import pyaware.data_types
import pyaware.aggregations
import pyaware.config
from pyaware.store import storage

log = logging.getLogger(__file__)

if typing.TYPE_CHECKING:
    from pathlib import Path


class RequestException(ValueError):
    pass


class IllegalFunction(RequestException):
    pass


class IllegalDataAddress(RequestException):
    pass


class IllegalDataValue(RequestException):
    pass


class MemoryParityError(IOError):
    pass


class SlaveDeviceFailure(IOError):
    pass


class AcknowledgeError(IOError):
    pass


class DeviceBusy(IOError):
    pass


class NegativeAcknowledgeError(IOError):
    pass


class GatewayPathUnavailable(IOError):
    pass


class GatewayDeviceFailedToRespond(IOError):
    pass


modbus_exception_codes = {
    1: IllegalFunction,
    2: IllegalDataAddress,
    3: IllegalDataValue,
    4: SlaveDeviceFailure,
    5: AcknowledgeError,
    6: DeviceBusy,
    7: NegativeAcknowledgeError,
    8: MemoryParityError,
    10: GatewayPathUnavailable,
    11: GatewayDeviceFailedToRespond,
    12: ConnectionError,
}


class ModbusException(IOError):
    pass


class AsyncWrapper:
    def __init__(self, client, loop=None):
        self.client = client
        self.lock = asyncio.Lock()
        self.loop = loop or asyncio.get_event_loop()

    async def _async(self, func, *args, **kwargs):
        func = partial(func, *args, **kwargs)
        async with self.lock:
            resp = await self.loop.run_in_executor(None, func)
            if resp.isError():
                raise ModbusException(f"{modbus_exception_codes.get(getattr(resp, 'exception_code', 12))}")
            return resp

    async def read_coils(self, address, count=1, **kwargs):
        '''

        :param address: The starting address to read from
        :param count: The number of coils to read
        :param unit: The slave unit this request is targeting
        :returns: A deferred response handle
        '''
        return await self._async(self.client.read_cols, address, count, **kwargs)

    async def read_discrete_inputs(self, address, count=1, **kwargs):
        '''

        :param address: The starting address to read from
        :param count: The number of discretes to read
        :param unit: The slave unit this request is targeting
        :returns: A deferred response handle
        '''
        return await self._async(self.client.read_discrete_inputs, address, count, **kwargs)

    async def write_coil(self, address, value, **kwargs):
        '''

        :param address: The starting address to write to
        :param value: The value to write to the specified address
        :param unit: The slave unit this request is targeting
        :returns: A deferred response handle
        '''
        return await self._async(self.client.write_coil, address, value, **kwargs)

    async def write_coils(self, address, values, **kwargs):
        '''

        :param address: The starting address to write to
        :param values: The values to write to the specified address
        :param unit: The slave unit this request is targeting
        :returns: A deferred response handle
        '''
        return await self._async(self.client.write_coils, address, values, **kwargs)

    async def write_register(self, address, value, **kwargs):
        '''

        :param address: The starting address to write to
        :param value: The value to write to the specified address
        :param unit: The slave unit this request is targeting
        :returns: A deferred response handle
        '''
        return await self._async(self.client.write_register, address, value, **kwargs)

    async def write_registers(self, address, values, **kwargs):
        '''

        :param address: The starting address to write to
        :param values: The values to write to the specified address
        :param unit: The slave unit this request is targeting
        :returns: A deferred response handle
        '''
        return await self._async(self.client.write_registers, address, values, **kwargs)

    async def read_holding_registers(self, address, count=1, **kwargs):
        '''

        :param address: The starting address to read from
        :param count: The number of registers to read
        :param unit: The slave unit this request is targeting
        :returns: A deferred response handle
        '''
        return await self._async(self.client.read_holding_registers, address, count, **kwargs)

    async def read_input_registers(self, address, count=1, **kwargs):
        '''

        :param address: The starting address to read from
        :param count: The number of registers to read
        :param unit: The slave unit this request is targeting
        :returns: A deferred response handle
        '''
        return await self._async(self.client.read_input_registers, address, count, **kwargs)

    async def readwrite_registers(self, *args, **kwargs):
        '''

        :param read_address: The address to start reading from
        :param read_count: The number of registers to read from address
        :param write_address: The address to start writing to
        :param write_registers: The registers to write to the specified address
        :param unit: The slave unit this request is targeting
        :returns: A deferred response handle
        '''
        return await self._async(self.client.readwrite_registers, *args, **kwargs)

    async def mask_write_register(self, *args, **kwargs):
        '''

        :param address: The address of the register to write
        :param and_mask: The and bitmask to apply to the register address
        :param or_mask: The or bitmask to apply to the register address
        :param unit: The slave unit this request is targeting
        :returns: A deferred response handle
        '''
        return await self._async(self.client.mask_write_register, *args, **kwargs)


class ModbusAsyncSerialClient:
    def __init__(self, port, stopbits, parity, baudrate, bytesize=8, timeout=3, loop=None):
        from pymodbus.client.sync import ModbusSerialClient
        client = ModbusSerialClient(method="rtu", port=port, stopbits=stopbits, parity=parity, baudrate=baudrate,
                                    bytesize=bytesize, timeout=timeout, strict=False)
        self.protocol = AsyncWrapper(client, loop)
        client.connect()
        self.connected = asyncio.Event()
        self.connected.set()

    def stop(self):
        self.protocol.client.close()


class ModbusAsyncTcpClient:
    """
    Client to connect to modbus device repeatedly over TCP/IP."
    """
    #: Minimum delay in milli seconds before reconnect is attempted.
    DELAY_MIN_MS = 1000
    #: Maximum delay in milli seconds before reconnect is attempted.
    DELAY_MAX_MS = 1000

    def __init__(self, host, port=502, client_port=0):
        from pymodbus.client.asynchronous.asyncio import ModbusClientProtocol
        self.host = host
        self.port = port
        self.client_port = client_port
        #: Protocol used to talk to modbus device.
        self.protocol_class = ModbusClientProtocol
        #: Current protocol instance.
        self.protocol = None
        #: Event loop to use.
        self.loop = asyncio.get_event_loop()
        self.connected = asyncio.Event()
        #: Reconnect delay in milli seconds.
        self.delay_ms = self.DELAY_MIN_MS

    def reset_delay(self):
        """
        Resets wait before next reconnect to minimal period.
        """
        self.delay_ms = self.DELAY_MIN_MS

    async def start(self):
        """
        Initiates connection to start client
        :param host:
        :param port:
        :return:
        """
        # force reconnect if required:
        if self.connected.is_set():
            if self.protocol:
                if self.protocol.transport:
                    self.protocol.transport.close()

        log.debug('Connecting to %s:%s.' % (self.host, self.port))

        await self._connect()

    def stop(self):
        """
        Stops client
        :return:
        """
        # prevent reconnect:
        self.host = None

        if self.connected.is_set():
            if self.protocol:
                if self.protocol.transport:
                    self.protocol.transport.close()

    def disconnect(self):
        self.stop()

    def _create_protocol(self):
        """
        Factory function to create initialized protocol instance.
        """
        protocol = self.protocol_class(source_address=("", self.client_port))
        protocol.factory = self
        return protocol

    async def _connect(self):
        log.debug('Connecting.')
        if self.host is None:
            return
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # https://stackoverflow.com/questions/6439790/sending-a-reset-in-tcp-ip-socket-connection
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack("ii", 1, 0))
            sock.settimeout(10)
            socket_config_path = pyaware.config.aware_path / ".." / f"{self.host}.yaml"
            self.client_port = pyaware.config.load_config(socket_config_path)
            if not self.client_port:
                sock.bind(('', 0))
                self.client_port = sock.getsockname()[1]
            else:
                sock.bind(('', self.client_port))
            pyaware.config.save_config(socket_config_path, self.client_port)
            sock.setblocking(False)
            await asyncio.wait_for(asyncio.get_event_loop().sock_connect(sock, (self.host, self.port)), timeout=1)
            # sock.connect((self.host, self.port))
            await asyncio.wait_for(self.loop.create_connection(self._create_protocol,
                                                               # self.host,
                                                               # self.port,
                                                               sock=sock,
                                                               # local_addr=('', self.client_port)
                                                               ), timeout=1)
        except Exception as ex:
            log.warning('Failed to connect: %s' % ex)
            asyncio.create_task(self._reconnect())
        else:
            log.info('Connected to %s:%s.' % (self.host, self.port))
            self.reset_delay()

    def protocol_made_connection(self, protocol):
        """
        Protocol notification of successful connection.
        """
        log.info('Protocol made connection.')
        if not self.connected.is_set():
            self.connected.set()
            self.protocol = protocol

            events.publish("imac_controller_data", data={"ethernet-comms-status": True}, timestamp=datetime.utcnow())
        else:
            log.error('Factory protocol connect '
                      'callback called while connected.')

    def protocol_lost_connection(self, protocol):
        """
        Protocol notification of lost connection.
        """
        if events.evt_stop.is_set():
            self.stop()
            return
        events.publish("imac_controller_data", data={"ethernet-comms-status": False}, timestamp=datetime.utcnow())
        if self.connected.is_set():
            log.info('Protocol lost connection.')
            if protocol is not self.protocol:
                log.error('Factory protocol callback called '
                          'from unexpected protocol instance.')
            try:
                self.protocol.transport.close()
            except AttributeError:
                pass
            self.connected.clear()
            self.protocol = None
            if self.host:
                asyncio.create_task(self._reconnect())
        else:
            log.error('Factory protocol disconnect callback called while not connected.')

    async def _reconnect(self):
        log.debug(f"Waiting {self.delay_ms} ms before next connection attempt.")
        await asyncio.sleep(self.delay_ms / 1000)
        self.delay_ms = min(2 * self.delay_ms, self.DELAY_MAX_MS)
        await self._connect()


class ModbusDevice:
    name = "Modbus Device"
    module_type = 'modbus-device'

    def __init__(self, client, device_id: str, config: Path, unit=0, address_shift=0):
        self.client = client
        self.device_id = device_id
        self.store_state = {}
        self.send_state = {}
        self.event_state = {}
        self.current_state = {}
        self.unit = unit
        self.config = pyaware.config.load_config(config)
        self.parameters = pyaware.data_types.parse_data_types(self.config["parameters"])
        if address_shift:
            for param in self.parameters.values():
                try:
                    param.address += address_shift
                except KeyError:
                    continue
        self.triggers = pyaware.triggers.build_from_device_config(config)
        self.aggregates = pyaware.aggregations.build_from_device_config(config)
        for name, source_config in self.config["sources"].items():
            if source_config.get("type", "poll") == "poll":
                asyncio.create_task(self.trigger_poll(name, address_shift=address_shift))

    async def trigger_poll(self, source, address_shift=0):
        try:
            poll_interval = self.config["sources"][source]["poll_interval"]
        except KeyError:
            poll_interval = 5
        if address_shift:
            modbus_blocks = []
            for start, end in self.config["sources"][source]["blocks"]:
                modbus_blocks.append([start + address_shift, end + address_shift])
        else:
            modbus_blocks = self.config["sources"][source]["blocks"]

        loop = asyncio.get_running_loop()
        start = loop.time()
        log.info(f"Waiting for connection for {self.device_id}")
        await self.client.connected.wait()
        log.info(f"Starting poll pipeline for {self.device_id}")

        # TODO remove and move to aiomodbus exclusively
        if any(isinstance(self.client, x) for x in (ModbusAsyncTcpClient, ModbusAsyncSerialClient)):
            read_handles = {
                "holding": self._read_pymodbus_factory(self.client.protocol.read_holding_registers),
                "input": self._read_pymodbus_factory(self.client.protocol.read_input_registers),
            }
        else:
            read_handles = {
                "holding": self._read_aiomodbus_factory(self.client.read_holding_registers),
                "input": self._read_aiomodbus_factory(self.client.read_input_registers),
            }
        read_handle = read_handles[self.config["sources"][source].get("handle", "holding")]

        while True:
            if pyaware.evt_stop.is_set():
                log.info(f"Closing modbus device {self.device_id} polling")
                return
            try:
                start = loop.time()
                await self.poll_pipeline(modbus_blocks, source, read_handle)
            except asyncio.CancelledError:
                if not pyaware.evt_stop.is_set():
                    log.warning(f"Modbus device {self.device_id} cancelled without stop signal")
                    continue
            except BaseException as e:
                if not pyaware.evt_stop.is_set():
                    log.exception(e)
            sleep_time = start - loop.time() + poll_interval
            if sleep_time > 0:
                await asyncio.sleep(start - loop.time() + poll_interval)

    async def poll_pipeline(self, blocks, source, read_handle):
        addr_map = pyaware.data_types.AddressMapUint16()
        for start, end in blocks:
            count = len(range(start, end))
            addr_map.merge(await read_handle(start, count))
        timestamp = datetime.utcnow()
        if timestamp is None:
            timestamp = datetime.utcnow()
        device_data = {}
        for k, v in self.config["parameters"].items():
            if v.get("source") == source:
                try:
                    device_data.update(self.parameters[k].decode(addr_map))
                except KeyError:
                    pass
        processed_data = await self.process_data(device_data, timestamp)
        self.current_state.update(device_data)

    def _read_pymodbus_factory(self, handle: typing.Callable):
        async def read(address: int, count: int):
            f"""
            Read from pymodbus via {handle} 
            :param address: 
            :param count: 
            :return: 
            """
            addr_map = pyaware.data_types.AddressMapUint16()
            rr = await handle(address, count, unit=self.unit)
            if rr.isError():
                raise modbus_exception_codes.get(rr.exception_code, IOError)
            addr_map[address: address + count] = rr.registers
            return addr_map

        return read

    def _read_aiomodbus_factory(self, handle: typing.Callable):
        async def read(address: int, count: int):
            f"""
            Read from aiomodbus via {handle} 
            :param address: 
            :param count: 
            :return: 
            """
            addr_map = pyaware.data_types.AddressMapUint16()
            addr_map[address: address + count] = await handle(address, count, unit=self.unit)
            return addr_map

        return read

    async def process_data(self, data, timestamp):
        store_data, send_data, event_data = await asyncio.gather(
            pyaware.triggers.process_triggers(self.store_state, data, self.triggers.get("process", {}).get("store", []),
                                              timestamp),
            pyaware.triggers.process_triggers(self.send_state, data, self.triggers.get("process", {}).get("send", []),
                                              timestamp),
            pyaware.triggers.process_triggers(self.event_state, data, self.triggers.get("process", {}).get("event", []),
                                              timestamp),
        )
        if store_data:
            storage.update(store_data, topic=f"{self.device_id}")
            self.store_state.update(store_data)
        if send_data:
            storage.update(send_data, topic=f"{self.device_id}")
            cached_data = storage.pop(f"{self.device_id}")
            aggregated_data = pyaware.aggregations.aggregate(cached_data, self.aggregates)
            events.publish(f"trigger_send/{self.device_id}", data=aggregated_data, meta=self.dict(),
                           timestamp=timestamp, topic_type="telemetry")
            self.send_state.update(cached_data)
        if event_data:
            for param, value in event_data.items():
                events.publish(f"parameter_trigger/{self.device_id}/{param}",
                               data=next(iter(value.values())),
                               timestamp=timestamp)
            self.event_state.update(event_data)
        return send_data

    def identify(self):
        return self.dict()

    def dict(self):
        response = {"type": self.module_type}
        return response
