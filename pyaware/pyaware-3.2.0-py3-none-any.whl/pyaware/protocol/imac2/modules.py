from __future__ import annotations
import aiohttp
import logging
import ipaddress
import typing
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os
import asyncio
from enum import Enum
from dataclasses import dataclass
import pyaware.commands
from pyaware import events, async_swap, async_threaded
from pyaware.protocol.imac2.exceptions import FailedAddressDiscover
from pyaware.triggers import process_triggers
from pyaware.protocol.imac2 import commands, ModuleStatus
from pyaware.protocol.imac2 import exceptions
from pyaware.protocol.modbus import modbus_exception_codes
from pyaware.data_types import AddressMapUint16, Param, ParamBits, ParamText, ParamMask, ParamCType, \
    ParamTimestampAmp, ParamBoolArray, ParamMaskScale, ParamDict, ParamLookup, ParamMaskBool
from pyaware.store import storage
import pyaware.aggregations

try:
    import rapidjson as json
except:
    import json

if typing.TYPE_CHECKING:
    from pyaware.protocol.imac2.protocol import Imac2Protocol

log = logging.getLogger(__file__)


class Units(Enum):
    percent = 0
    ppm = 1


number = typing.Union[int, float]


@dataclass
class Detector:
    symbol: str
    type: str
    units: str
    span: number
    zero: number = 0
    fault_ranges = {2800: "detector-low-soft-fault",
                    3200: "detector-under-range",
                    20800: "detector-over-range",
                    21200: "detector-high-soft-fault"
                    }

    def decode(self, data: number) -> dict:
        faults = {
            "detector-low-soft-fault": False,
            "detector-under-range": False,
            "detector-over-range": False,
            "detector-high-soft-fault": False
        }
        try:
            faults[self.fault_ranges[data]] = True
        except KeyError:
            pass
        decoded = {
            "detector-units": self.units,
            "detector-zero": self.zero,
            "detector-span": self.span,
            "detector-symbol": self.symbol,
            "detector-sensor-type": self.type
        }

        if not any(faults.values()):
            decoded["detector-gas-analog"] = data
            decoded["detector-gas-value"] = (data - 4000) / 16000 * (self.span + self.zero)
        else:
            decoded["detector-gas-value"] = -2000
        decoded.update(faults)
        return decoded


@events.enable
class ImacModule:
    specs: dict = None
    name = "Unknown iMAC Module"
    blocks = [0]
    module_type = "imac-module-unknown"
    config_name = "imac_module_parameter_spec.yaml"

    def __init__(self, protocol: Imac2Protocol, _async=False, dev_id=""):
        self.protocol = protocol
        self.parameters = {"poll": {}, "block": {}}
        self.block_specs = {
            "address-single": Param(0x40e, "address-single", block=0),
            "param2": Param(0x40f, "param2", block=0),
            "param3": Param(0x410, "param3", block=0),
            "param4": Param(0x411, "param4", block=0),
        }
        self.current_state = {"dev-id": dev_id}
        self.read_state = {}
        self.store_state = {}
        self.send_state = {}
        self.event_state = {}
        self.commands = pyaware.commands.Commands({
            "set-imac-address": [
                pyaware.commands.ValidateIn(range(256)),
                commands.WriteParam("address-single"),
                commands.ReadParam("address-single"),
                commands.ValidateParam("address-single"),
                commands.UpdateMeta("address-single"),
                commands.UpdateSpecs()
            ],
            "set-parameters": [
                commands.WriteAndValidateParams()
            ]
        }, meta_kwargs={"imac_module": self})
        self._async = _async
        self.store_timestamp = datetime.utcfromtimestamp(0)
        self.send_timestamp = datetime.utcfromtimestamp(0)
        self.triggers = pyaware.triggers.build_from_device_config(
            os.path.join(os.path.dirname(__file__), self.config_name))
        self.aggregates = pyaware.aggregations.build_from_device_config(
            os.path.join(os.path.dirname(__file__), self.config_name))
        self.l1_status = ModuleStatus.NEVER_ONLINE  # TODO load from stored state
        self.parameter_handlers = {"block": self.parameter_block_reader}

    @events.subscribe(topic="imac_module_data")
    async def process_module_data_triggers(self, data, timestamp):
        dev_data = data.get(self.current_state["dev-id"])
        if dev_data is None:
            return
        store_data, send_data, event_data = await asyncio.gather(
            process_triggers(self.store_state, dev_data, self.triggers.get("process", {}).get("store", []),
                             timestamp),
            process_triggers(self.send_state, dev_data, self.triggers.get("process", {}).get("send", []),
                             timestamp),
            process_triggers(self.event_state, dev_data, self.triggers.get("process", {}).get("event", []),
                             timestamp),
        )
        if store_data:
            storage.update(store_data, topic=f"{self.protocol.device_id}/{self.current_state['dev-id']}")
            self.update_store_state(store_data)
        if send_data:
            storage.update(send_data, topic=f"{self.protocol.device_id}/{self.current_state['dev-id']}")
            cached_data = storage.pop(f"{self.protocol.device_id}/{self.current_state['dev-id']}")
            aggregated_data = pyaware.aggregations.aggregate(cached_data, self.aggregates)
            events.publish(f"trigger_send/{self.protocol.device_id}", data=aggregated_data, meta=self.dict(),
                           timestamp=timestamp, topic_type="telemetry")
            self.update_send_state(cached_data)
        if event_data:
            for param, value in event_data.items():
                events.publish(f"parameter_trigger/{self.current_state['dev-id']}/{param}",
                               data=next(iter(value.values())),
                               timestamp=timestamp)
            self.update_event_state(event_data)

    def update_specs(self):
        address = self.current_state.get("address-single")
        if address:
            self.parameters["poll"]["data"] = Param(address, "data")
            self.parameters["poll"]["status"] = ParamBits(address + 0x100, {
                "status-on-scan-bit": 0,
                "status-l1-clash-bit": 1,
                "status-global-bit": 2,
                "status-l1-own-bit": 3,
                "status-l2-own-bit": 4,
                "status-sys-own-bit": 5,
                "status-l2-clash-bit": 6,
                "status-high-byte-bit": 7,
                "status-valid-offline": 8,
                "status-valid-online": 9,
                "status-valid-iso-request": 10,
                "status-iso-req-filter": 12,
                "status-iso-here": 13,
                "status-iso-there": 14,
                "status-iso-neither": 15
            })
            self.parameters["poll"]["resistance"] = Param(address + 0x200, "resistance")
            self.parameters["poll"]["error-offline-count"] = ParamMask(address + 0x300, "error-offline-count",
                                                                       mask=0xff)
            self.parameters["poll"]["error-clashes-count"] = ParamMask(address + 0x300, "error-clashes-count",
                                                                       mask=0xff00, rshift=8)
        else:
            # If the address is 0, then there is no module data
            self.parameters["poll"].clear()

    def update_from_roll_call(self, serial_number, generation_id, imac_address, version, module_type, **kwargs):
        """
        Check if the module is the same as last roll call, if no then update internal representation
        :param serial_number:
        :param generation_id:
        :param imac_address:
        :param version:
        :param module_type:
        :return:
        """
        new_params = {
            "serial_number": serial_number,
            "generation_id": generation_id,
            "address-single": imac_address,
            "module_type": module_type,
            "version": version,
            "software_version": (version & 0xf00) >> 8,
            "hardware_version": (version & 0xf000) >> 12,
            "dev-id": f"{serial_number}-G{generation_id + 1}"
        }

        self.current_state.update(new_params)
        events.publish("imac_module_data", data={self.current_state["dev-id"]: new_params}, timestamp=datetime.utcnow())
        self.update_specs()
        for trig in self.triggers.get("collect", {}).get("read", []):
            try:
                trig.device = self.current_state["dev-id"]
            except AttributeError:
                pass

    def __repr__(self):
        return f"{self.name} <Serial {self.current_state.get('serial_number')}" \
               f"-G{self.current_state.get('generation_id', -2) + 1} " \
               f"@ address {self.current_state.get('address-single')}>"

    async def read_all_parameters(self):
        parameters = {}
        for block in self.blocks:
            addr_map = await self.read_parameter_block(block)
            for spec in self.block_specs.values():
                parameters.update(spec.decode(addr_map, block))
        return parameters

    async def parameter_block_reader(self, data):
        blocks = {spec.block for spec in self.block_specs.values() if spec.keys().intersection(data)}
        parameters = {}
        for block in blocks:
            try:
                addr_map = await self.read_parameter_block(block)
                for spec in self.block_specs.values():
                    parameters.update(spec.decode(addr_map, block))
            except (ValueError, IOError) as e:
                log.error(f"Failed to read {self.current_state['dev-id']}: block {block}")
        return parameters

    async def read_parameter_block(self, block):
        return await self.protocol.read_by_serial_number(self.current_state['serial_number'],
                                                         self.current_state['generation_id'], block)

    async def write_parameter_block(self, block, addr_map: AddressMapUint16):
        await self.protocol.write_by_serial_number(self.current_state['serial_number'],
                                                   self.current_state['generation_id'],
                                                   block, addr_map)

    async def write_parameters(self, data: dict):
        """
        :param data: Dictionary of form parameter: value
        :return:
        """
        blocks = {spec.block for spec in self.block_specs.values() if spec.keys().intersection(data.keys())}
        for block in blocks:
            addr_map = await self.read_parameter_block(block)
            addr_map = self.build_parameter_writes(data, addr_map, block)
            await self.write_parameter_block(block, addr_map)

    async def read_parameters(self, data: set, exact=False):
        """
        :param data: A set of parameter values to read
        :param exact: If true will only return the parameters that were in the original data set
        :return:
        """
        parameters = {}
        for source in self.parameters:
            if source == "poll":
                continue
            parameters.update(await self.parameter_handlers[source](data))
        if exact:
            parameters = {key: parameters[key] for key in data}
        timestamp = datetime.utcnow()
        self.update_read_state(data.union(parameters), timestamp)
        self.current_state.update(parameters)
        events.publish("imac_module_data", data={self.current_state["dev-id"]: parameters}, timestamp=timestamp)
        return parameters

    def build_parameter_writes(self, data: dict, addr_map: AddressMapUint16, block: int) -> AddressMapUint16:
        """
        Builds up the data to be written in
        :return: Updated address map
        """
        for spec in self.block_specs.values():
            if spec.block == block:
                spec.encode(data, addr_map)
        return addr_map

    @async_threaded
    def process_module_data(self, addr_map: AddressMapUint16, timestamp: datetime = None):
        """
        Porcesses the module data from an address map to determine the valid parameter data from the module
        :param addr_map:
        :param timestamp:
        :return:
        """
        parameters = {}
        for param_spec in self.parameters["poll"].values():
            if isinstance(param_spec.address, int):
                addresses = [param_spec.address]
            else:
                addresses = param_spec.address
                if addresses is None:
                    addresses = []
            for addr in addresses:
                if addr > 0x100 or self.protocol.parse_status(addr_map[addr + 0x100]) in [ModuleStatus.ONLINE,
                                                                                          ModuleStatus.SYSTEM]:
                    parameters.update({k: v for k, v in param_spec.decode(addr_map).items()})
        return parameters

    def diff_module_data(self, parameters: dict):
        """
        Compare a subset of parameter values against the module state
        :param parameters:
        :return:
        """
        return {k: parameters[k] for k in parameters if self.current_state.get(k) != parameters[k]}

    def update_current_state(self, parameters: dict):
        """
        Update the state used to run diff module data against
        :param parameters: Parameter dictionary to update the state
        :return:
        """
        self.current_state.update(parameters)

    def update_store_state(self, parameters: dict):
        """
        Update the state the module has represented in the cache database
        :param parameters: Parameter dictionary to update the state
        :return:
        """
        self.store_state.update(parameters)

    def update_send_state(self, parameters: dict):
        """
        Update the state used the module has represented from queued mqtt messages
        :param parameters: Parameter dictionary to update the state
        :return:
        """
        self.send_state.update(parameters)

    def update_read_state(self, parameters: set, timestamp: datetime):
        """
        Update the timestamp since the last read parameters
        :param parameters: Parameter dictionary to update the state
        :return:
        """
        for trig in self.triggers.get("collect", {}).get("read", []):
            if trig.parameter in parameters:
                trig.timestamp = timestamp

    def update_event_state(self, parameters: dict):
        """
        Update the state used the module has represented from queued mqtt messages
        :param parameters: Parameter dictionary to update the state
        :return:
        """
        self.event_state.update(parameters)

    def identify_addresses(self) -> dict:
        try:
            return {"address-single": self.current_state["address-single"]}
        except KeyError:
            return {}

    @events.subscribe(topic="imac_module_status")
    def update_l1_status(self, data, timestamp):
        addresses = list(self.identify_addresses().values())
        if any(addresses) and all(
                data["address-status"][addr] in [ModuleStatus.ONLINE, ModuleStatus.SYSTEM] for addr in addresses if
                addr is not 0):
            if self.l1_status != ModuleStatus.ONLINE:
                self.l1_status = ModuleStatus.ONLINE
                log.info(f"Adding device schedule {self.module_type} - {self.current_state['dev-id']}")
                log.info(f"Adding triggers {self.triggers.get('collect', {}).get('read', [])}")
                self.protocol.schedule_read_list.update(self.triggers.get("collect", {}).get("read", []))
        else:
            if self.l1_status != ModuleStatus.OFFLINE:
                self.l1_status = ModuleStatus.OFFLINE
                log.info(f"Removing device schedule {self.module_type} - {self.current_state['dev-id']}")
                self.protocol.remove_device_from_schedule(self.current_state["dev-id"])

    async def disconnect(self):
        await self.write_parameters({"address-single": 0})
        await self.read_parameters({"address-single"})

    def identify(self):
        response = self.dict()
        response["values"] = self.identify_addresses()
        return response

    def dict(self):
        response = {"type": self.module_type}
        if self.current_state.get('dev-id'):
            response["serial"] = self.current_state.get("dev-id")
        return response

    async def find_missing_addresses(self):
        """
        :return:
        """


@events.enable
class RTS(ImacModule):
    name = "Remote Tripping Station"
    module_type = 'imac-controller-rts'
    config_name = "rts_parameter_spec.yaml"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.poll_interval = 5
        self.commands.update({
            "boundary-enable": [
                pyaware.commands.ValidateHandle(lambda x: len(x) == 40),
                pyaware.commands.TopicTask(f"boundary_enable/{id(self)}", {"data": "value"})
            ],
            "remote-bypass": [
                pyaware.commands.ValidateIn(range(2)),
                pyaware.commands.TopicTask(f"remote_bypass/{id(self)}", {"data": "value"})
            ],
            "remote-trip": [
                pyaware.commands.ValidateIn(range(2)),
                pyaware.commands.TopicTask(f"remote_trip/{id(self)}", {"data": "value"})
            ],
            "trip-reset": [
                pyaware.commands.TopicTask(f"trip_reset/{id(self)}")
            ],
            "set-ip-address-serial": [
                pyaware.commands.TopicTask(f"set_ip_address_serial/{id(self)}", {"data": "value"})
            ],
            "set-ip-address-ethernet": [
                pyaware.commands.ValidateAnyHandle([ipaddress.ip_address]),
                pyaware.commands.TopicTask(f"set_ip_address_ethernet/{id(self)}", {"data": "value"})
            ],
        })
        self.config = {}
        self.client_ser = None
        self.client_eth = None
        self.unit = 1
        self.data_point_blocks = self._modbus_ranges((0, 0x47f), (0x500, 0x580), (0x600, 0x6a2))
        self.rest_data = {}
        self.controller_data = {}
        self.serial_validated = False
        self.ethernet_validated = False
        asyncio.create_task(self.trigger_poll())

    @events.subscribe(topic="remote_bypass/{id}")
    async def remote_bypass(self, data):
        await self.protocol.write_bit(0x52a, self.current_state["logical-number"] - 1, data)

    @events.subscribe(topic="remote_trip/{id}")
    async def remote_trip(self, data):
        await self.protocol.write_bit(0x52b, self.current_state["logical-number"] - 1, data)

    @events.subscribe(topic="trip_reset/{id}")
    async def trip_reset(self):
        """
        Perform a remote trip reset. This will change in V2 to individually reset the RTS
        :return:
        """
        await self.protocol.trip_reset()

    def update_from_roll_call(self, imac_address, dev_id, **kwargs):
        """
        Check if the module is the same as last roll call, if no then update internal representation
        :param imac_address:
        :param dev_id:
        :return:
        """
        schema = self.protocol.address_schema_match(imac_address)
        if schema["name"] not in ["rts-config-0", "rts-config-1", "rts-config-2"]:
            log.info(f"Schema Violation: RTS address {imac_address} not in schema")
        _, fieldbus_address, logical_number = dev_id.split('-')
        new_params = {
            f"address-{schema['name']}": imac_address,
            "dev-id": dev_id,
            "fieldbus-address": int(fieldbus_address),
            "logical-number": int(logical_number)
        }
        self.current_state.update(new_params)
        self.update_specs()
        events.publish("imac_module_data", data={self.current_state["dev-id"]: new_params},
                       timestamp=datetime.utcnow())
        self.load_from_config()

    def load_from_config(self, changes=None):
        dev_id = self.current_state["dev-id"]
        new_config = pyaware.config.load_config(pyaware.config.aware_path / "config" / f"{dev_id.lower()}.yaml")
        if not self.config:
            self.config = new_config or {}
            changes = "serial ethernet"
        elif not changes:
            changes = pyaware.config.config_changes(self.config, new_config).to_json()
            self.config = new_config
        if "serial" in changes:
            if self.client_ser:
                self.client_ser.stop()
            log.info(f"Attempting to connect to serial for {self.current_state['dev-id']}")
            self.client_ser = pyaware.config.parse_communication(
                communication=[x for x in self.config.get("communication", [{}]) if x.get("name") == "serial"]).get(
                "serial")
            self.serial_validated = False
        if "ethernet" in changes:
            if self.client_eth:
                self.client_eth.stop()
            log.info(f"Attempting to connect to ethernet for {self.current_state['dev-id']}")
            self.client_eth = pyaware.config.parse_communication(
                communication=[x for x in self.config.get("communication", [{}]) if x.get("name") == "ethernet"]).get(
                "ethernet")
            self.ethernet_validated = False

    def save_config(self):
        dev_id = self.current_state["dev-id"]
        pyaware.config.save_config(pyaware.config.aware_path / "config" / f"{dev_id.lower()}.yaml", self.config)

    @events.subscribe(topic="set_ip_address_serial/{id}")
    async def set_ip_address_serial(self, data):
        try:
            ipaddress.ip_address(data)
            payload = {
                "type": "modbus_tcp",
                "name": "serial",
                "params": {
                    "host": {
                        "type": "value",
                        "value": data
                    },
                }
            }
        except:
            if "tty" in data or "COM" in data:
                payload = {
                    "type": "modbus_rtu",
                    "name": "serial",
                    "params": {"port": {"type": "value", "value": data},
                               "baudrate": {"type": "value", "value": 9600},
                               "parity": {"type": "value", "value": "N"},
                               "stopbits": {"type": "value", "value": 1, }}
                }
            else:
                raise pyaware.commands.ValidationError("Data is not a valid ip address or serial port")
        await self.update_config("serial", payload)

    @events.subscribe(topic="set_ip_address_ethernet/{id}")
    async def set_ip_address_ethernet(self, data):
        payload = {
            "type": "modbus_tcp",
            "name": "ethernet",
            "params": {
                "host":
                    {
                        "type": "value",
                        "value": data
                    },
                "client_port":
                    {
                        "type": "value",
                        "value": True
                    }
            }
        }
        await self.update_config("ethernet", payload)

    async def validate_connection(self, client):
        """
        Validates the connection against known RTS fields
        The Field-bus Address at iMAC Address (and modbus address) 254 indicates which iMAC master it is listening on
        The Rotary switch at modbus address 0x401 which indicates which logical RTS it is (indexed from 0)
        These must match the data read from the iMAC master which will place the fieldbus address at iMAC address 254
        and the logical address of the RTS which is determined by the addressing schema RTS logical 1 at iMAC address
        216 and RTS logical 12 at iMAC address 227
        :param client:
        :return:
        """
        if client is None:
            raise IOError("No Valid client connected")
        addr_map = await self.read(client, 254)
        addr_map.merge(await self.read(client, 0x401))
        fieldbus_address = addr_map[254]
        if fieldbus_address != self.current_state["fieldbus-address"]:
            msg = "RTS Interface Fieldbus Mismatch read " \
                  f"{fieldbus_address} expected {self.current_state['fieldbus-address']}"
            log.info(msg)
            raise exceptions.InterfaceValidationError(msg)
        rotary_switch = addr_map[0x401] & 0xf
        if rotary_switch != int(self.current_state["logical-number"]) - 1:
            msg = "RTS Interface Logical Mismatch read " \
                  f"{rotary_switch + 1} expected {self.current_state['logical-number']}"
            log.info(msg)
            raise exceptions.InterfaceValidationError(msg)

    async def validate_ethernet_connection(self):
        """
        Validates the ethernet connection against known RTS fields
        The Field-bus Address at iMAC Address (and modbus address) 254 indicates which iMAC master it is listening on
        The Rotary switch at modbus address 0x401 which indicates which logical RTS it is (indexed from 0)
        These must match the data read from the iMAC master which will place the fieldbus address at iMAC address 254
        and the logical address of the RTS which is determined by the addressing schema RTS logical 1 at iMAC address
        216 and RTS logical 12 at iMAC address 227
        :param client:
        :return:
        """
        if all([self.client_eth.protocol, self.current_state.get("ethernet-comms-status"), self.ethernet_validated]):
            return
        try:
            await self.validate_connection(self.client_eth.protocol)
            self.ethernet_validated = True
        except exceptions.InterfaceValidationError:
            self.ethernet_validated = False
            events.publish("imac_module_data",
                           data={self.current_state["dev-id"]: {"ethernet-comms-status": True,
                                                                "interface-mismatch-ethernet": True}},
                           timestamp=datetime.now())
            raise
        except IOError:
            self.ethernet_validated = False
            events.publish("imac_module_data",
                           data={self.current_state["dev-id"]: {"ethernet-comms-status": False,
                                                                "interface-mismatch-ethernet": True}},
                           timestamp=datetime.now())
            raise

    async def validate_serial_connection(self):
        """
        Validates the serial connection against known RTS fields
        The Field-bus Address at iMAC Address (and modbus address) 254 indicates which iMAC master it is listening on
        The Rotary switch at modbus address 0x401 which indicates which logical RTS it is (indexed from 0)
        These must match the data read from the iMAC master which will place the fieldbus address at iMAC address 254
        and the logical address of the RTS which is determined by the addressing schema RTS logical 1 at iMAC address
        216 and RTS logical 12 at iMAC address 227
        :param client:
        :return:
        """
        if all([self.client_ser.protocol, self.current_state.get("serial-comms-status"), self.serial_validated]):
            return
        try:
            await self.validate_connection(self.client_ser.protocol)
            self.serial_validated = True
        except exceptions.InterfaceValidationError:
            self.serial_validated = False
            events.publish("imac_module_data",
                           data={self.current_state["dev-id"]: {"serial-comms-status": True,
                                                                "interface-mismatch-serial": True}},
                           timestamp=datetime.now())
            raise
        except IOError:
            self.serial_validated = False
            events.publish("imac_module_data",
                           data={self.current_state["dev-id"]: {"serial-comms-status": False,
                                                                "interface-mismatch-serial": True}},
                           timestamp=datetime.now())
            raise

    async def update_config(self, target, payload):

        log.info(f"Updating configuration for {self.current_state['dev-id']}")
        replace_item = None
        if "communication" not in self.config:
            self.config["communication"] = []
        for index, comm in enumerate(self.config["communication"]):
            if comm["name"] == target:
                replace_item = index
                break
        if replace_item is not None:
            self.config["communication"][replace_item] = payload
        else:
            self.config["communication"].append(payload)
        self.save_config()
        self.load_from_config(target)

    async def trigger_poll(self):
        loop = asyncio.get_running_loop()
        start = loop.time()
        log.info(f"Starting {self.current_state['dev-id']} bus polling")
        while True:
            if pyaware.evt_stop.is_set():
                log.info(f"Closing {self.current_state['dev-id']} polling")
                return
            try:
                await asyncio.sleep(start - loop.time() + self.poll_interval)
                start = loop.time()
                await self.poll_pipeline()
            except asyncio.CancelledError:
                if not pyaware.evt_stop.is_set():
                    log.warning(f"iMAC {self.current_state['dev-id']} cancelled without stop signal")
                    raise
            except BaseException as e:
                if not pyaware.evt_stop.is_set():
                    log.exception(e)

    async def process_rest_data(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"http://{self.client_eth.host}/cgi-bin/deviceinfo.cgi") as response:
                    text_obj = await response.read()
                    json_obj = json.loads(text_obj.decode('utf-8', 'ignore'))
                    parameters = {}
                    for param_spec in self.rest_data.values():
                        parameters.update({k: v for k, v in param_spec.decode(json_obj).items()})
                    return parameters
        except AttributeError:
            pass
        except BaseException as e:
            log.error(e)
        return {}

    def update_specs(self):
        self.parameters["poll"] = {
            "remote-bypass-status": ParamBits(0x52a, bitmask={
                "remote-bypass-status": self.current_state["logical-number"] - 1}),
            "remote-trip-status": ParamBits(0x52b, bitmask={
                "remote-trip-status": self.current_state["logical-number"] - 1}),
        }
        self.controller_data = {
            "rotary-sw": ParamMask(0x401, "rotary-sw", mask=0xf),
            "system-status": ParamBits(0x100, bitmask={
                "control-relay-state": 8,
                "auxiliary-relay-state": 9,
                "l1-short-circuit-status": 12,
            }),
            # Generic iMAC Controller data
            "serial-protocol": ParamLookup(0x500, "serial-protocol", mask=0xff, table={
                0: "not-configured",
                1: "modbus-master",
                2: "modbus-slave",
                3: "ip2-protocol",
                4: "l1-maintenance",
                5: "l2-maintenance",
            }, table_reversed={
                "modbus-master": 1,
                "modbus-slave": 2,
                "ip2-protocol": 3,
                "l1-maintenance": 4,
                "l2-maintenance": 5,
            }),
            "serial-baud-rate": ParamLookup(0x500, "serial-baud-rate", mask=0xff00, rshift=8, table={
                0: 9600,
                1: 0,
                2: 600,
                3: 1200,
                4: 2400,
                5: 4800,
                6: 9600,
                7: 19200
            }, table_reversed={
                600: 2,
                1200: 3,
                2400: 4,
                4800: 5,
                9600: 6,
                1920: 7,
            }),
            "serial-parity": ParamLookup(0x501, "serial-parity", mask=0xff, table={
                0: "even",
                1: "none",
                2: "even",
                3: "odd"
            }, table_reversed={
                "none": 1,
                "even": 2,
                "odd": 3,
                "n": 1,
                "e": 2,
                "o": 3,
                "N": 1,
                "E": 2,
                "O": 3,
            }),
            "serial-stop-bits": ParamLookup(0x501, "serial-stop-bits", mask=0xff00, rshift=8, table={
                0: 1,
                1: 1,
                2: 2
            }, table_reversed={
                1: 1,
                2: 2
            }),
            "serial-mode": ParamLookup(0x502, "serial-mode", mask=0xff, table={
                0: "RS232",
                1: "RS485/RS422"
            }, table_reversed={
                "RS232": 0,
                "RS485": 1,
                "RS422": 2,
                "RS485/RS422": 3
            }),
            "serial-slave-address": ParamMask(0x502, "serial-slave-address", mask=0xff00, rshift=8),
            "controller-hardware-flags": ParamBits(0x600, bitmask={
                "rtc-fault": 0,
                "i2c-fault": 1,
                "sc-card-fault": 2
            }),
            "controller-temperature": Param(0x601, "controller-temperature", scale=0.01),
            "controller-tag-name": ParamText(0x638, "controller-tag-name", length=19, padding=b"\xa5", swap_bytes=True),
            "legacy-hardware-version": ParamText(0x64c, "legacy-hardware-version", length=10, padding=b"\xa5",
                                                 swap_bytes=True),
            "legacy-firmware-version": ParamText(0x656, "legacy-firmware-version", length=10, padding=b"\xa5",
                                                 swap_bytes=True),
            "legacy-software-version": ParamText(0x660, "legacy-software-version", length=10, padding=b"\xa5",
                                                 swap_bytes=True),
            "slp-version": ParamText(0x66a, "slp-version", length=10, padding=b"\xa5",
                                     swap_bytes=True),
            "log-bootloader-name": ParamText(0x674, "log-bootloader-name", length=8, padding=b"\x00", swap_bytes=True),
            "log-bootloader-version": ParamText(0x67c, "log-bootloader-version", length=3, padding=b"\xa5",
                                                swap_bytes=True),
            "log-hardware-name": ParamText(0x67f, "log-hardware-name", length=8, padding=b" ", swap_bytes=True,
                                           strip_lagging=" "),
            "log-hardware-version": ParamText(0x689, "log-hardware-version", length=3, padding=b"\xa5",
                                              swap_bytes=True),
            "serial-number": ParamText(0x68a, "serial-number", length=8, padding=b"\xa5", swap_bytes=True,
                                       strip_leading="0"),
            "log-application-name": ParamText(0x692, "log-application-name", length=8, padding=b"\x00",
                                              swap_bytes=True),
            "log-application-version": ParamText(0x69a, "log-application-version", length=8, padding=b"\x00",
                                                 swap_bytes=True),
            "master-fieldbus-number": Param(0x523, "master-fieldbus-number"),

            "config-boundary-detectors": ParamBoolArray((0x520, 0x521, 0x522), "config-boundary-detectors", length=40,
                                                        block="serial"),
            "plc-activity-word": Param(0x524, "plc-activity-word", block="serial"),
            "gas-trip": ParamMask(0x527, "gas-trip", 0x01, block="serial"),
            "last-trip-boundary-detectors": ParamBoolArray((0x528, 0x529, 0x52a), "last-trip-boundary-detectors",
                                                           length=40, block="serial"),
            "last-trip": ParamBits(0x52a, {
                "last-trip-clash-boundary": 10,
                "last-trip-offline-boundary": 11,
                "last-trip-l2-timeout": 13,
                "last-trip-no-boundary-enabled": 14,
                "last-trip-no-boundary-online": 15,
            }, block="serial"),
        }
        self.rest_data = {
            "ethernet-dhcp": ParamDict("P_DHCP", "ethernet-dhcp", table={"No": False, "Yes": True}),
            "ethernet-ip-address": ParamDict("P_IP_Address", "ethernet-ip-address"),
            "ethernet-ip-mask": ParamDict("P_IP_Mask", "ethernet-ip-mask"),
            "ethernet-ip-gateway": ParamDict("P_Gateway", "ethernet-ip-gateway"),
            "ethernet-mac-address": ParamDict("P_MAC_Address", "ethernet-mac-address"),
        }

        try:
            config_addresses = [self.current_state[f"address-rts-config-{x}"] for x in range(3) if
                                f"address-rts-config-{x}" in self.current_state]
            self.parameters["poll"]["boundary-detectors"] = ParamBoolArray(config_addresses, "boundary-detectors",
                                                                           length=40)
            self.parameters["poll"]["rts-status-bits"] = ParamBits(config_addresses[-1], bitmask={
                "mcb-nc": 10,
                "mcb-no": 11,
                "mcb-bypass": 12,
                "tmr-trip": 13,
                "ar-state": 14,
                "gas-trip": 15,
            })
        except KeyError:
            pass

        for index, address in [(x, self.current_state.get(f"address-rts-config-{x}")) for x in range(3) if
                               self.current_state.get(f"address-rts-config-{x}") is not None]:
            self.parameters["poll"][f"resistance-rts-config-{index}"] = \
                Param(address + 0x200, f"resistance-rts-config-{index}")
            self.parameters["poll"][f"error-offline-count-rts-config-{index}"] = \
                ParamMask(address + 0x300, f"error-offline-count-rts-config-{index}", mask=0xff)
            self.parameters["poll"][f"error-clashes-count-rts-config-{index}"] = \
                ParamMask(address + 0x300, f"error-clashes-count-rts-config-{index}", mask=0xff00, rshift=8)

    async def poll_pipeline(self):
        """
        Pipeline that begins when a pipeline is published
        :param data:
        :return:
        """
        addr_map, timestamp = await self.poll_once()
        controller_data, rest_data = await asyncio.gather(
            self.process_controller_data(addr_map, timestamp),
            self.process_rest_data())
        data = {**controller_data, **rest_data}
        events.publish("imac_module_data", data={f"{self.current_state['dev-id']}": data}, timestamp=timestamp)

    @async_threaded
    def process_controller_data(self, addr_map: AddressMapUint16, timestamp: datetime):
        """
        Process
        :param addr_map:
        :param timestamp:
        :return:
        """
        parameters = {}
        for param_spec in self.controller_data.values():
            try:
                parameters.update({k: v for k, v in param_spec.decode(addr_map).items()})
            except KeyError:
                pass
        return parameters

    async def poll_once(self) -> typing.Union[typing.Tuple[AddressMapUint16, datetime], typing.Awaitable]:
        """
        Perform a complete poll of the imac data
        :requires: client_eth to be available
        :return:
        """
        addr_map = AddressMapUint16()
        if self.client_eth:
            for address, count in self.data_point_blocks:
                addr_map.merge(await self.read_eth(address, count))
        else:
            events.publish("imac_module_data",
                           data={f"{self.current_state['dev-id']}": {"ethernet-comms-status": False}},
                           timestamp=datetime.utcnow())

        if self.client_ser:
            asyncio.create_task(self.read_ser_single(0))  # Get the serial comms status to update
        else:
            events.publish("imac_module_data",
                           data={f"{self.current_state['dev-id']}": {"serial-comms-status": False}},
                           timestamp=datetime.utcnow())

        return addr_map, datetime.utcnow()

    async def read(self, client, address: int, count: int = 1) -> typing.Union[AddressMapUint16, typing.Awaitable]:
        """
        Reads modbus holding registers and returns an address map of the response
        :param address:
        :param count:
        :return:
        """
        rr = await client.read_holding_registers(address, count, unit=self.unit)
        if rr.isError():
            raise modbus_exception_codes.get(rr.exception_code, IOError)(
                f"Failed to read {self.current_state['dev-id']}")
        addr_map = AddressMapUint16()
        addr_map[address: address + count] = rr.registers
        return addr_map

    async def read_eth(self, address: int, count: int = 1) -> AddressMapUint16:
        """
        Reads modbus holding registers and returns an address map of the response
        :param address:
        :param count:
        :return:
        """
        await self.validate_ethernet_connection()
        try:
            res = await self.read(self.client_eth.protocol, address, count)
            events.publish("imac_module_data",
                           data={f"{self.current_state['dev-id']}": {"ethernet-comms-status": True}},
                           timestamp=datetime.utcnow())
            return res
        except BaseException as e:
            events.publish("imac_module_data",
                           data={f"{self.current_state['dev-id']}": {"ethernet-comms-status": False}},
                           timestamp=datetime.utcnow())
            if self.client_eth.connected:
                log.exception(e)
            raise

    async def read_ser_single(self, address) -> int:
        read = await self.read_ser(address, 1)
        return read[address]

    async def write_bit(self, address, bit, value):
        if hasattr(self.client_ser, 'protocol'):
            client = self.client_ser.protocol
        else:
            client = self.client_ser
        await self.validate_serial_connection()
        wr = await client.write_coil(address * 16 + bit, value, unit=self.unit)
        if wr.isError():
            events.publish("imac_module_data",
                           data={f"{self.current_state['dev-id']}": {"serial-comms-status": False}},
                           timestamp=datetime.utcnow())
            raise modbus_exception_codes.get(wr.exception_code, IOError)(
                f"Failed to write to {self.current_state['dev-id']}")
        events.publish("imac_module_data", data={f"{self.current_state['dev-id']}": {"serial-comms-status": True}},
                       timestamp=datetime.utcnow())

    async def process_nvm(self):
        addr_map, timestamp = await self.read_nvm(self.client_eth or self.client_ser)
        module_data = await self.process_module_data(addr_map, timestamp)
        events.publish("imac_module_data", data={f"{self.current_state['dev-id']}": module_data}, timestamp=timestamp)

    async def read_nvm(self, client):
        try:
            client = client.protocol
        except AttributeError:
            pass
        rr = await client.read_holding_registers(0x520, count=11, unit=0)
        if rr.isError():
            raise modbus_exception_codes.get(rr.exception_code, IOError)(
                f"Failed to read {self.current_state['dev-id']}")
        addr_map = AddressMapUint16()
        addr_map[0x520: 0x520 + 11] = rr.registers
        return addr_map, datetime.now()

    def identify_addresses(self) -> dict:
        return {x: self.current_state.get(x) for x in
                ["address-rts-config-0", "address-rts-config-1", "address-rts-config-2"] if
                self.current_state.get(x) is not None}

    async def find_missing_addresses(self):
        """
        :return:
        """
        missing = {k for k in ["address-rts-config-0", "address-rts-config-1", "address-rts-config-2"] if
                   self.current_state.get(k) is None}
        for address in missing:
            try:
                schema = self.protocol.address_schema_match_by_name(address.split("address-")[-1])
                self.current_state[address] = schema["range"][0] + self.current_state["logical-number"] - 1
            except ValueError:
                raise FailedAddressDiscover("Failed to match RTS schema for address")
            events.publish("imac_module_data",
                           data={f"{self.current_state['dev-id']}": {address: self.current_state[address]}},
                           timestamp=datetime.now())
        self.update_specs()

    @events.subscribe(topic="boundary_enable/{id}")
    async def boundary_enable(self, data):
        """
        :param data: 40 bit sequence in an array corresponding to detectors 1-40
        :param timestamp:
        :return:
        """
        assert len(data) == 40
        addr_map = AddressMapUint16()
        addr_map[0x520: 0x523] = 0, 0, 0
        for index, bit in enumerate(data):
            address = 0x520 + index // 16
            addr_map[address] |= bit << (index % 16)
        await self.write_ser(0x520, *addr_map[0x520:0x523])
        resp = await self.read_ser(0x520, 3)
        if resp[0x520: 0x523] != addr_map[0x520:0x523]:
            raise ValueError("Read back boundary data did not match write")

    async def write(self, client, address, *values):
        wr = await client.write_registers(address, values, unit=self.unit)
        if wr.isError():
            raise modbus_exception_codes.get(wr.exception_code, IOError)(
                f"Failed to write to {self.current_state['dev-id']}")

    async def write_ser(self, address, *values):
        await self.validate_serial_connection()
        try:
            res = await self.write(self.client_ser.protocol, address, *values)
            events.publish("imac_module_data",
                           data={f"{self.current_state['dev-id']}": {"serial-comms-status": True}},
                           timestamp=datetime.utcnow())
            return res
        except BaseException as e:
            events.publish("imac_module_data",
                           data={f"{self.current_state['dev-id']}": {"serial-comms-status": False}},
                           timestamp=datetime.utcnow())
            if self.client_eth.connected:
                log.exception(e)
            raise

    def _modbus_ranges(self, *ranges, max_block=125):
        return [(x, min([max_block, stop - x])) for start, stop in ranges for x in range(start, stop, max_block)]

    async def read_ser(self, address: int, count: int = 1) -> AddressMapUint16:
        """
        Reads modbus holding registers and returns an address map of the response
        :param address:
        :param count:
        :return:
        """

        await self.validate_serial_connection()
        try:
            res = await self.read(self.client_ser.protocol, address, count)
            events.publish("imac_module_data",
                           data={f"{self.current_state['dev-id']}": {"serial-comms-status": True}},
                           timestamp=datetime.utcnow())
            return res
        except BaseException as e:
            events.publish("imac_module_data",
                           data={f"{self.current_state['dev-id']}": {"serial-comms-status": False}},
                           timestamp=datetime.utcnow())
            if self.client_eth.connected:
                log.exception(e)
            raise


@events.enable
class Di4(ImacModule):
    name = "DI4 Module"
    module_type = "imac-module-di4"
    config_name = "di4_parameter_spec.yaml"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.block_specs.update({
            "invert-status": Param(0x40f, "invert-status", block=0),
            "invert-status-bits": ParamBits(0x40f, bitmask={
                "invert-status-1": 0,
                "invert-status-2": 1,
                "invert-status-3": 2,
                "invert-status-4": 3,
            }, block=0),
            "voltage-l1": Param(0x411, "voltage-l1", block=0, scale=0.1),
        })
        self.commands.update({
            "set-parameters": [
                pyaware.commands.ValidateGroup([
                    pyaware.commands.ValidateIn(range(0x10), key="invert-status"),
                    pyaware.commands.ValidateIn(range(2), key="invert-status-1"),
                    pyaware.commands.ValidateIn(range(2), key="invert-status-2"),
                    pyaware.commands.ValidateIn(range(2), key="invert-status-3"),
                    pyaware.commands.ValidateIn(range(2), key="invert-status-4"),
                    pyaware.commands.ValidateRange(8.0, 21.5, key="voltage-l1")]
                ),
                commands.WriteAndValidateParams()
            ]
        })

    def update_from_roll_call(self, serial_number, generation_id, imac_address, version, module_type, **kwargs):
        super().update_from_roll_call(serial_number, generation_id, imac_address, version, module_type, **kwargs)
        events.subscribe(self.update_io_feedback,
                         topic=f"parameter_trigger/{self.current_state['dev-id']}/switch-status-raw-1")
        events.subscribe(self.update_io_feedback,
                         topic=f"parameter_trigger/{self.current_state['dev-id']}/switch-status-raw-2")
        events.subscribe(self.update_io_feedback,
                         topic=f"parameter_trigger/{self.current_state['dev-id']}/switch-status-raw-3")
        events.subscribe(self.update_io_feedback,
                         topic=f"parameter_trigger/{self.current_state['dev-id']}/switch-status-raw-4")
        events.subscribe(self.update_io_feedback,
                         topic=f"parameter_trigger/{self.current_state['dev-id']}/invert-status-1")
        events.subscribe(self.update_io_feedback,
                         topic=f"parameter_trigger/{self.current_state['dev-id']}/invert-status-2")
        events.subscribe(self.update_io_feedback,
                         topic=f"parameter_trigger/{self.current_state['dev-id']}/invert-status-3")
        events.subscribe(self.update_io_feedback,
                         topic=f"parameter_trigger/{self.current_state['dev-id']}/invert-status-4")

    def update_specs(self):
        address = self.current_state.get("address-single", 0)
        if address:
            self.parameters["poll"]["data"] = Param(address, "data")
            self.parameters["poll"]["switches-status-raw"] = ParamBits(address, bitmask={
                "switch-status-raw-1": 0,
                "switch-status-raw-2": 1,
                "switch-status-raw-3": 2,
                "switch-status-raw-4": 3,
            })
        else:
            self.parameters["poll"].clear()

    def update_io_feedback(self, data, timestamp):
        try:
            resp = {f"switch-status-{x}":
                        self.current_state[f"switch-status-raw-{x}"] ^ self.current_state[f"invert-status-{x}"]
                    for x in range(1, 5)}
        except KeyError:
            return
        events.publish("imac_module_data", data={f"{self.current_state['dev-id']}": resp}, timestamp=timestamp)

    async def find_missing_addresses(self):
        """
        :return:
        """
        missing = {k for k in [f"invert-status-{x}" for x in range(1, 5)] if self.current_state.get(k) is None}
        if missing:
            params = await self.read_parameters(missing)
            if not params:
                raise FailedAddressDiscover("Failed to read DI4 parameters")
            self.current_state.update(params)
            self.update_specs()


@events.enable
class Lim(ImacModule):
    name = "LIM Module"
    module_type = "imac-module-lim"


@events.enable
class SimP(ImacModule):
    name = "SIM-P Module"
    module_type = "imac-module-sim-p"
    config_name = "simp_parameter_spec.yaml"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.block_specs.update({
            "modbus-slave-address": Param(0x40f, "modbus-slave-address", block=0),
            "modbus-start-address": Param(0x410, "modbus-start-address", block=0),
            "modbus-register-count": Param(0x411, "modbus-register-count", block=0),
        })
        self.commands.update({
            "set-parameters": [
                pyaware.commands.ValidateGroup([
                    pyaware.commands.ValidateIn(range(256), key="modbus-slave-address"),
                    pyaware.commands.ValidateIn(range(1 << 16), key="modbus-start-address"),
                    pyaware.commands.ValidateIn(range(1, 17), key="modbus-register-count"),
                ]),
                commands.WriteAndValidateParams()
            ]
        })

    def update_specs(self):
        address = int(self.current_state.get("address-single", 0))
        register_count = int(self.current_state.get("modbus-register-count", 0))
        self.parameters["poll"].clear()
        if address:
            self.parameters["poll"]["comms-error"] = ParamMaskBool(address, "comms-error", mask=1 << 15)
            self.parameters["poll"]["comms-error-count"] = ParamMask(address, "comms-error-count", mask=0x7fff)
            if register_count:
                self.parameters["poll"].update(
                    {f"raw-word-{x}": Param(address + x + 1, f"raw-word-{x}") for x in
                     range(register_count)})

    def identify_addresses(self) -> dict:
        addrs = super().identify_addresses()
        addrs.update(
            {param.idx: param.address for param in self.parameters["poll"].values() if
             param.idx.startswith("raw-word")})
        return addrs

    async def find_missing_addresses(self):
        """
        :return:
        """
        missing = {k for k in ["modbus-start-address", "modbus-register-count"] if
                   self.current_state.get(k) is None}
        params = await self.read_parameters(missing)
        self.current_state.update(params)
        self.update_specs()


@events.enable
class Rtd1(ImacModule):
    name = "RTD-1 Module"
    module_type = "imac-module-rtd1"
    config_name = "rtd1_parameter_spec.yaml"
    types = {
        54: "flags",
        55: "temp"
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.block_specs = {
            "address-flags": Param(0x40e, "address-flags", block=0),
            "voltage-l1": Param(0x411, "voltage-l1", block=0, scale=0.1),
            "address-temp": Param(0x40e, "address-flags", block=1),
            "set-point-low": ParamCType(0x40f, "set-point-low", block=1),
            "set-point-high": ParamCType(0x411, "set-point-high", block=1),

        }
        self.commands.update({
            "set-parameters": [
                pyaware.commands.ValidateGroup([
                    pyaware.commands.ValidateIn(range(256), key="address-flags"),
                    pyaware.commands.ValidateRange(8.0, 21.5, key="voltage-l1"),
                    pyaware.commands.ValidateIn(range(256), key="address-temp"),
                    pyaware.commands.ValidateRange(-19, 299, key="set-point-low"),
                    pyaware.commands.ValidateRange(-19, 299, key="set-point-high"),
                ]),
                commands.WriteAndValidateParams()
            ]
        })

    def update_from_roll_call(self, serial_number, generation_id, imac_address, version, module_type, **kwargs):
        new_params = {
            "serial_number": serial_number,
            "generation_id": generation_id,
            f"address-{self.types[module_type]}": imac_address,
            f"module_type-{self.types[module_type]}": module_type,
            "detector-type": version,
            "dev-id": f"{serial_number}-G{generation_id + 1}"
        }
        if module_type in [54, 55]:
            new_params.pop("detector-type")
        if self.types[module_type] == "flags":
            new_params["address"] = imac_address
        self.current_state.update(new_params)
        for trig in self.triggers.get("collect", {}).get("read", []):
            trig.device = self.current_state["dev-id"]
        events.publish("imac_module_data", data={self.current_state["dev-id"]: new_params},
                       timestamp=datetime.utcnow())
        self.update_specs()

    def update_specs(self):
        for mod_type in self.types.values():
            address = self.current_state.get(f"address-{mod_type}")
            if mod_type == "flags":
                if address:
                    self.parameters["poll"]["data-flags"] = ParamBits(address, {
                        "alarm-temp-high": 5,
                        "alarm-temp-low": 4,
                        "alarm-temp-out-of-range": 3,
                        "rtd-sense-wire-fault": 2,
                        "rtd-open-circuit": 1,
                        "rtd-short-circuit": 0,
                    })
                else:
                    self.parameters["poll"].pop("data-flags", None)
            if mod_type == "temp":
                if address:
                    self.parameters["poll"][f"temperature"] = ParamCType(address, f"temperature", data_type="short")
                else:
                    self.parameters["poll"].pop("temperature", None)

    def identify_addresses(self) -> dict:
        return {x: self.current_state.get(x) for x in
                ["address-flags", "address-temp"] if
                self.current_state.get(x) is not None}


@events.enable
class SimT(ImacModule):
    name = "SIM-T Module"
    module_type = "imac-module-sim-t"


@events.enable
class SimG(ImacModule):
    name = "SIM-G Module"
    module_type = "imac-module-sim-g"

    def update_specs(self):
        super().update_specs()
        address = self.current_state.get("address")
        if address == 0:
            # There is no module data when the address is 0
            self.parameters["poll"].clear()
            return
        self.parameters["poll"].update({
            "data": ParamBits(address, bitmask={
                "channel-1-low-fault": 0,
                "channel-1-alarm-1": 1,
                "channel-1-alarm-2": 2,
                "channel-1-alarm-3": 3,
                "channel-1-high-fault": 4,
                "channel-2-low-fault": 9,
                "channel-2-alarm-1": 10,
                "channel-2-alarm-2": 11,
                "channel-2-alarm-3": 12,
                "channel-2-high-fault": 13
            }),
            "invert_status": Param(0x40f, "invert_status")
        })


@events.enable
class Ro4(ImacModule):
    name = "RO4 Module"
    module_type = "imac-module-ro4"
    config_name = "ro4_parameter_spec.yaml"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.block_specs.update({
            "invert-status": Param(0x40f, "invert-status", block=0),
            "invert-status-bits": ParamBits(0x40f, bitmask={
                "invert-status-1": 0,
                "invert-status-2": 1,
                "invert-status-3": 2,
                "invert-status-4": 3,
            }, block=0),
            "relays-de-energize-mask": ParamMask(0x40f, "relays-de-energize-mask", mask=0xf, block=0),
            "relays-de-energize-timer": ParamMaskScale(0x40f, "relays-de-energize-timer", block=0, scale=0.2),
            "relays-energize-mask": ParamMask(0x410, "relays-energize-mask", mask=0xf, block=0),
            "relays-energize-timer": ParamMaskScale(0x410, "relays-energize-timer", block=0, scale=0.2),
        })
        self.commands.update({
            "set-parameters": [
                pyaware.commands.ValidateGroup([
                    pyaware.commands.ValidateIn(range(0x10), key="invert-status"),
                    pyaware.commands.ValidateIn(range(2), key="invert-status-1"),
                    pyaware.commands.ValidateIn(range(2), key="invert-status-2"),
                    pyaware.commands.ValidateIn(range(2), key="invert-status-3"),
                    pyaware.commands.ValidateIn(range(2), key="invert-status-4"),
                    pyaware.commands.ValidateIn(range(0x10), key="relays-de-energize-mask"),
                    pyaware.commands.ValidateRange(0.2, 51, key="relays-de-energize-timer", allow_zero=True),
                    pyaware.commands.ValidateIn(range(0x10), key="relays-energize-mask"),
                    pyaware.commands.ValidateRange(0.2, 51, key="relays-energize-timer", allow_zero=True),
                ]),
                commands.WriteAndValidateParams()
            ]
        })

    def update_from_roll_call(self, serial_number, generation_id, imac_address, version, module_type, **kwargs):
        super().update_from_roll_call(serial_number, generation_id, imac_address, version, module_type, **kwargs)
        events.subscribe(self.update_io_feedback,
                         topic=f"parameter_trigger/{self.current_state['dev-id']}/relay-status-raw-1")
        events.subscribe(self.update_io_feedback,
                         topic=f"parameter_trigger/{self.current_state['dev-id']}/relay-status-raw-2")
        events.subscribe(self.update_io_feedback,
                         topic=f"parameter_trigger/{self.current_state['dev-id']}/relay-status-raw-3")
        events.subscribe(self.update_io_feedback,
                         topic=f"parameter_trigger/{self.current_state['dev-id']}/relay-status-raw-4")
        events.subscribe(self.update_io_feedback,
                         topic=f"parameter_trigger/{self.current_state['dev-id']}/invert-status-1")
        events.subscribe(self.update_io_feedback,
                         topic=f"parameter_trigger/{self.current_state['dev-id']}/invert-status-2")
        events.subscribe(self.update_io_feedback,
                         topic=f"parameter_trigger/{self.current_state['dev-id']}/invert-status-3")
        events.subscribe(self.update_io_feedback,
                         topic=f"parameter_trigger/{self.current_state['dev-id']}/invert-status-4")

    def update_specs(self):
        address = self.current_state.get("address-single", 0)
        if address:
            self.parameters["poll"]["data"] = Param(address, "data")
            self.parameters["poll"]["relay-status-raw"] = ParamBits(address, bitmask={
                "relay-status-raw-1": 0,
                "relay-status-raw-2": 1,
                "relay-status-raw-3": 2,
                "relay-status-raw-4": 3,
            })
        else:
            self.parameters["poll"].clear()

    def update_io_feedback(self, data, timestamp):
        try:
            resp = {f"relay-status-{x}":
                        self.current_state[f"relay-status-raw-{x}"] ^ self.current_state[f"invert-status-{x}"]
                    for x in range(1, 5)}
        except KeyError:
            return
        events.publish("imac_module_data", data={f"{self.current_state['dev-id']}": resp}, timestamp=timestamp)

    async def find_missing_addresses(self):
        """
        :return:
        """
        missing = {k for k in [f"invert-status-{x}" for x in range(1, 5)] if self.current_state.get(k) is None}
        if missing:
            params = await self.read_parameters(missing)
            if not params:
                raise FailedAddressDiscover("Failed to read RO4 parameters")
            self.current_state.update(params)
            self.update_specs()


@events.enable
class GasGuard2(ImacModule):
    name = "Gasguard 2"
    module_type = "imac-module-gg2"
    config_name = "gasguard2_parameter_spec.yaml"
    types = {
        61: "flags",
        62: "analog",
        63: "power"
    }
    blocks = [0, 1, 2, 3, 4, 5, 6, 7]
    current_state = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.analog_conversion = {
            0: Detector("unknown", "unknown", "%", 0, 0),
            1: Detector("CH4", "catalytic", "%", 5, 0),
            2: Detector("CH4", "infra-red", "%", 5, 0),
            3: Detector("CH4", "infra-red", "%", 100, 0),
            4: Detector("CO2", "infra-red", "%", 2, 0),
            5: Detector("CO2", "infra-red", "%", 5, 0),
            6: Detector("CO", "infra-red", "ppm", 50, 0),
            7: Detector("CO", "infra-red", "ppm", 100, 0),
            8: Detector("O2", "electrochemical", "%", 25, 0),
            10: Detector("NO2", "electrochemical", "ppm", 10, 0),
            11: Detector("H2S", "electrochemical", "ppm", 50, 0),
            12: Detector("H2S", "electrochemical", "ppm", 100, 0),
        }
        self.parameters["poll"] = {}
        self.commands.update(commands.gasguard_2)
        self.block_specs = {
            "address-flags": Param(0x40e, "address-flags", block=0),
            "exception-trigger": Param(0x40f, "exception-trigger", block=0),
            # "catalytic-reset-address": ParamMask(0x410, "catalytic-reset-address", mask=0xff, block=0),
            # "catalytic-reset-command": ParamMask(0x410, "catalytic-reset-command", mask=0xff00, rshift=8, block=0),
            "address-bypass": ParamMask(0x411, "address-bypass", mask=0xff, block=0),
            "aim-compatibility-mode": ParamMask(0x411, "aim-compatibility-mode", mask=0x100, rshift=8, block=0),
            "address-analog": Param(0x40e, "address-analog", block=1),
            "set-point-1": Param(0x40f, "set-point-1", block=1),
            "set-point-2": Param(0x410, "set-point-2", block=1),
            "set-point-3": Param(0x411, "set-point-3", block=1),
            "address-power": Param(0x40e, "address-power", block=2),
            "hysteresis-config": ParamMask(0x411, "hysteresis-config", mask=0b1111 << 12, rshift=12, block=2),
            "healthy-config": ParamMask(0x411, "healthy-config", mask=0b111 << 9, rshift=9, block=2),
            "warmup-config": ParamMask(0x411, "warmup-config", mask=1 << 8, rshift=8, block=2),
            "address-rtc": ParamMask(0x411, "address-rtc", block=2, mask=0xff),
            # TODO TBD with AIM mode complicating it for param 2
            "detector-temperature": Param(0x40e, "detector-temperature", block=3),
            "detector-pressure": Param(0x40f, "detector-pressure", block=3),
            "detector-humidity": Param(0x410, "detector-humidity", block=3),
            # "detector-gas-reading-permyriad": Param(0x411, "detector-gas-reading-permyriad", block=3),
            "command-register-code": ParamMask(0x411, "command-register-code", mask=0xff00, rshift=8, block=3),
            "command-register-result": ParamMask(0x411, "command-register-result", mask=0xff, block=3),
            "last-t90-test-result": Param(0x40e, "last-t90-test-result", block=4),
            "last-nata-cal-hours": Param(0x40f, "last-nata-cal-hours", block=4),
            "last-cal-cup-seconds": Param(0x410, "last-cal-cup-seconds", block=4),
            "power-supply-voltage": ParamMaskScale(0x411, "power-supply-voltage", mask=0xff00, rshift=8, scale=0.1,
                                                   block=4, significant_figures=3),
            # "misc-flags": ParamBits(0x40f, bitmask={
            #     "bypass_status": 0,
            #     "catalytic-detector-latch": 1,
            #     "detector-warmup": 2
            # }, block=5),
            "postbox-selection": ParamMask(0x40e, "postbox-selection", mask=0b111, block=5),
            "detector-type": ParamMask(0x40f, "detector-type", mask=0xff00, rshift=8, block=5),
            "cal-cup-alarm-28-days": ParamMask(0x40f, "cal-cup-alarm-28-days", mask=1 << 4, rshift=4, block=5),
            "linearity-test-alarm-14-days": ParamMask(
                0x40f, "linearity-test-alarm-14-days", mask=1 << 3, rshift=3, block=5),
            "linearity-test-last-points": ParamMask(0x40e, "linearity-test-last-points", mask=0b111, block=5),
            "postbox-timestamp": ParamTimestampAmp(0x410, "postbox-timestamp", block=5),
            "detector-serial-number": ParamCType(0x40f, "detector-serial-number", data_type="uint", block=6),
            "detector-software-version": Param(0x411, "detector-software-version", block=6),
            "display-serial-number": ParamCType(0x40e, "display-serial-number", data_type="uint", block=7),
            "display-base-software-version": ParamMask(0x410, "display-base-software-version", block=7, mask=0xff),
            "display-application-version-lua": ParamMask(0x411, "display-application-version-lua", block=7,
                                                         mask=0xff),
        }
        self.postbox_lock = asyncio.Lock()
        self.parameters["postbox"] = {
            "linearity-test-time": 0b00,
            "t90-test-time": 0b10,
            "telemetry-test-time": 0b01,
            "rtc-time": 0b11,
        }
        self.parameter_handlers["postbox"] = self.parameter_postbox_reader

    def update_from_roll_call(self, serial_number, generation_id, imac_address, version, module_type, **kwargs):
        # TODO version is broken into sensor type
        # TODO make sure we get aim compatibility mode and senor type
        new_params = {
            "serial_number": serial_number,
            "generation_id": generation_id,
            f"address-{self.types[module_type]}": imac_address,
            f"module_type-{self.types[module_type]}": module_type,
            "detector-type": version,
            "dev-id": f"{serial_number}-G{generation_id + 1}"
        }
        if module_type in [61, 62]:
            new_params.pop("detector-type")
        if self.types[module_type] == "flags":
            new_params["address"] = imac_address
        self.current_state.update(new_params)
        for trig in self.triggers.get("collect", {}).get("read", []):
            trig.device = self.current_state["dev-id"]
        events.subscribe(self.update_analog_units,
                         topic=f"parameter_trigger/{self.current_state['dev-id']}/data-analog")
        events.subscribe(self.linearity_due,
                         topic=f"parameter_trigger/{self.current_state['dev-id']}/linearity-test-time")
        events.publish("imac_module_data", data={self.current_state["dev-id"]: new_params},
                       timestamp=datetime.utcnow())

        self.update_specs()

    def update_specs(self):
        for mod_type in self.types.values():
            address = self.current_state.get(f"address-{mod_type}")
            if address:
                if mod_type == "flags":
                    self.parameters["poll"][f"data-{mod_type}"] = ParamBits(address, {
                        # "di4-bypass": 15,
                        "telemetry-test": 14,
                        "hardware-fault": 13,
                        "ch4-over-range-ndir-incomplete-calibration": 12,
                        "linearity-test-overdue": 11,
                        "detector-warm-up-busy": 10,
                        "gas-value-invalid": 9,
                        "cal-cup-on": 8,
                        "detector-data-invalid": 7,
                        "power-alarm-trip": 6,
                        "power-alarm-warn": 5,
                        "set-point-2-not-3": 4,
                        "set-point-not-1-not-2": 3,
                        "set-point-alarm-3": 2,
                        "set-point-alarm-2": 1,
                        "set-point-alarm-1": 0,
                    })
                    self.parameters["poll"][f"trip-status"] = ParamMaskBool(address, "trip-status", 0b0011111011000101)
                else:
                    self.parameters["poll"][f"data-{mod_type}"] = Param(address, f"data-{mod_type}")

                self.parameters["poll"][f"status-{mod_type}"] = ParamBits(address + 0x100, bitmask={
                    f"status-{mod_type}-on-scan-bit": 0,
                    f"status-{mod_type}-l1-clash-bit": 1,
                    f"status-{mod_type}-global-bit": 2,
                    f"status-{mod_type}-l1-own-bit": 3,
                    f"status-{mod_type}-l2-own-bit": 4,
                    f"status-{mod_type}-sys-own-bit": 5,
                    f"status-{mod_type}-l2-clash-bit": 6,
                    f"status-{mod_type}-high-byte-bit": 7,
                    f"status-{mod_type}-valid-offline": 8,
                    f"status-{mod_type}-valid-online": 9,
                    f"status-{mod_type}-valid-iso-request": 10,
                    f"status-{mod_type}-iso-req-filter": 12,
                    f"status-{mod_type}-iso-here": 13,
                    f"status-{mod_type}-iso-there": 14,
                    f"status-{mod_type}-iso-neither": 15
                })
                self.parameters["poll"][f"resistance-{mod_type}"] = Param(address + 0x200, f"status-{mod_type}")
                self.parameters["poll"][f"error-offline-count-{mod_type}"] = ParamMask(
                    address + 0x300, f"error-offline-count-{mod_type}", mask=0xff)
                self.parameters["poll"][f"error-clashes-count-{mod_type}"] = ParamMask(
                    address + 0x300, f"error-clashes-count-{mod_type}", mask=0xff00, rshift=8)
            else:
                # If there is no address, then there is no module data to compute
                self.parameters["poll"].pop(f"data-{mod_type}", None)
                self.parameters["poll"].pop(f"status-{mod_type}", None)
                self.parameters["poll"].pop(f"resistance-{mod_type}", None)
                self.parameters["poll"].pop(f"error-offline-count-{mod_type}", None)
                self.parameters["poll"].pop(f"error-clashes-count-{mod_type}", None)

            if self.current_state.get("aim-compatibility-mode"):
                self.block_specs["power-point-alarm"] = ParamMaskScale(0x40f, "power-point-alarm", block=2, scale=0.01,
                                                                       significant_figures=4)
                self.block_specs["power-point-trip"] = ParamMaskScale(0x410, "power-point-trip", block=2, scale=0.01,
                                                                      significant_figures=4)
            else:
                self.block_specs["power-point-alarm"] = ParamMaskScale(0x410, "power-point-alarm", mask=0xff00,
                                                                       rshift=8, block=2, scale=0.1,
                                                                       significant_figures=3)
                self.block_specs["power-point-trip"] = ParamMaskScale(0x410, "power-point-trip", mask=0xff, block=2,
                                                                      scale=0.1,
                                                                      significant_figures=3)
        bypass_address = self.current_state.get(f"address-bypass")
        if bypass_address:
            self.parameters["poll"]["di4"] = ParamBits(bypass_address, {
                "bypass-remote": 8,
                "bypass-local": 0,
            })
        else:
            self.parameters["poll"].pop("bypass-remote", None)
            self.parameters["poll"].pop("bypass-local", None)

    def __repr__(self):
        return f"{self.name} <Serial {self.current_state.get('serial_number')}" \
               f"-G{self.current_state.get('generation_id', -2) + 1}: " \
               f"flags @ {self.current_state.get('address-flags', 'unknown')} " \
               f"analog @ {self.current_state.get('address-analog', 'unknown')} " \
               f"power @ {self.current_state.get('address-power', 'unknown')}>" \
               f"bypass @ {self.current_state.get('address-bypass', 'unknown')}>"

    async def find_missing_addresses(self):
        """
        :return:
        """
        missing = {k for k in ["address-flags", "address-analog", "address-power", "address-bypass"] if
                   self.current_state.get(k) is None}
        if missing:
            params = await self.read_parameters(missing)
            if not params:
                raise FailedAddressDiscover("Failed to read GG2 parameters")
            self.current_state.update(params)
            self.update_specs()

    def identify_addresses(self) -> dict:
        return {x: self.current_state.get(x) for x in
                ["address-flags", "address-analog", "address-power"] if
                self.current_state.get(x) is not None}

    async def parameter_postbox_reader(self, data):
        postboxes = {postbox: code for postbox, code in self.parameters["postbox"].items() if postbox in data}
        parameters = {}
        for postbox, code in postboxes.items():
            async with self.postbox_lock:
                try:
                    await self.write_parameters({"postbox-selection": code})
                    await asyncio.sleep(2)
                    data = await self.read_parameters({"postbox-timestamp"})
                    parameters = data
                    parameters[postbox] = data["postbox-timestamp"]
                except (ValueError, IOError) as e:
                    log.error(f"Failed to read {self.current_state['dev-id']}: {postbox.idx}")
        return parameters

    def update_analog_units(self, data, timestamp):
        converted = self.analog_conversion[self.current_state.get("detector-type", 0)].decode(data)
        self.update_current_state(converted)
        events.publish("imac_module_data", data={self.current_state["dev-id"]: converted}, timestamp=timestamp)

    def linearity_due(self, data, timestamp):
        converted = {"linearity-test-time-due": data + relativedelta(months=6)}
        self.update_current_state(converted)
        events.publish("imac_module_data", data={self.current_state["dev-id"]: converted}, timestamp=timestamp)

    async def disconnect(self):
        reset_values = {k: 0 for k in ["address-flags", "address-analog", "address-power", "address-bypass"] if
                        self.current_state.get(k) not in [None, 0]}
        await self.write_parameters(reset_values)
        await self.read_parameters(set(reset_values))


module_types = {
    # 0: "Reserved",
    # 1: "Controller",
    # 2: "TCD2 DIPSwitch",
    # 3: "EOL Module",
    # 4: "SQM Module",
    # 5: "DI2/4 Module",
    # 6: "IIM-OLC Module",
    7: Lim,
    # 8: "TCD4 Long",
    # 9: "TCD4 Module",
    # 10: "RTD3 Flags",
    # 11: "RTD3 Temp 1",
    # 12: "RTD3 Temp 2",
    # 13: "RTD3 Temp 3",
    # 14: "DI4L Module",
    15: Di4,
    # 16: "IIM Module",
    # 17: "PGM-A Programr",
    # 18: "MEOL Module",
    # 19: "Undefined",
    # 20: "SSW Flags",
    # 21: "SSW Control",
    # 22: "SSW % Slip",
    # 23: "SSW % Speed",
    # 24: "SSW Linr Speed",
    # 25: "Undefined",
    # 26: "Undefined",
    # 27: "GAI3 Flags",
    # 28: "GAI3 Analogue #1",
    # 29: "GAI3 Analogue #2",
    # 30: "GAI3 Analogue #3",
    # 31: "RKM Keypad",
    # 32: "LED4 Module",
    # 33: "EMM Module",
    # 34: "Undefined #34",
    35: SimP,
    36: SimT,
    37: SimG,
    # 38: "DI5 Module",
    39: Ro4,
    # 40: "DO4",
    # 41: "GCA Flags",
    # 42: "GCA 15Min Tally",
    # 43: "GCA 8Hr Tally",
    # 44: "GCA 24Hr Tally",
    # 45: "GCA Raw Count",
    # 46: "DI8 Module",
    # 47: "RIS Module",
    # 48: "AIM Flags",
    # 49: "AIM Analog",
    # 50: "AIM PwrSupply",
    # 51: "CRM Module",
    # 52: "ARM Module",
    # 53: "GRM Module",
    54: Rtd1,
    55: Rtd1,
    # 56: "SIM-G2 Module",
    # 57: "FCP DigInputs",
    # 58: "FCP DigOutputs",
    # 59: "FCP AnaInputs",
    # 60: "FCP AnaOutputs",
    61: GasGuard2,  # Gasguard2Flags,
    62: GasGuard2,  # Gasguard2Analog,
    63: GasGuard2,  # Gasguard2PowerSupply,
    "rts": RTS
}
