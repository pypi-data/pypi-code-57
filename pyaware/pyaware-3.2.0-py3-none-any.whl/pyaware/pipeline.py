"""
Infrastructure for supporting the data telemetry pipeline

For Example
If we want to read two modbus TCP blocks from a device and publish to the cloud. We might want to.

Read data until both block of reads are complete ->
Load the data into a data structure (Say a sparse dict indexed by address) ->
Filter only the data we need to monitor ->
Decode the data according to a device spec (Eg. this is unint32 and 2 decimal places, SI unit conversion)->
Store the values in SQLlite ->
Produce diff from last sent state ->
Evaluate triggers to see if the data should be sent to cloud (Sink or push through to next stage) ->
Publish the data to the cloud ->
On success mark in SQLlite as sent to cloud (Sink)

Branching models should be considered to handle different circumstances such as
Read data until both block of reads are complete (On Error) ->
Evaluate triggers to see if error should be sent to cloud ->
Publish device state to cloud indicating comms offline
"""
from __future__ import annotations
from concurrent import futures
import threading
from functools import partial
import struct
import rx
import rx.scheduler
import rx.subject
from rx import operators as ops

from pyaware.data_types import endian, data_types, AddressMap
from pyaware.resources import rm
from pymodbus.client.sync import ModbusTcpClient
import multiprocessing


class ModbusHoldingPipeline(threading.Thread):
    def __init__(self, client, *blocks, unit=0, spec=None):
        super().__init__()
        self.sub_read = rx.subject.Subject()
        self.sub_diff = rx.subject.Subject()
        self._stop_event = threading.Event()
        self.client = client
        self.blocks = blocks
        self.state = {}
        if spec is not None:
            self.spec = spec
        else:
            self.spec = {}

        self.unit = unit
        self.init()

    def init(self):
        self.sub_read.pipe(
            ops.filter(lambda x: bool(x)),
            ops.map(partial(filter_parameters, spec=self.spec)),
            ops.map(partial(diff_dicts, state_dict=self.state)),
            ops.filter(lambda x: bool(x))
        ).subscribe(self.sub_diff)

    def stop(self) -> None:
        self._stop_event.set()

    def run(self) -> None:
        while not self._stop_event.is_set():
            try:
                self.sub_read.on_next(self._read())
            except Exception:
                import traceback
                traceback.print_exc()
                # self.sub_read.on_error(e)
        self.sub_read.on_completed()

    def _read(self):
        addr_map = AddressMap()
        futs = {}
        for address, words in self.blocks:
            fut = self.client.read_holding_registers(address, words, unit=self.unit)
            futs[fut] = address
        completed, pending = futures.wait(futs, timeout=1)
        for fut, address in futs.items():
            if fut in completed:
                register_response = fut.result()
                if register_response.isError():
                    continue
                addr_map.save_block(address, register_response.registers)
        return addr_map


def filter_bits(parameter_value, bitmask):
    return {value: bool(parameter_value & (1 << bit)) for value, bit in bitmask.items()}


def filter_parameters(addr_map: AddressMap, spec: dict, byte_order="big", word_order="little"):
    parameters = {}
    byte_order = endian.get(byte_order, ">")
    word_order = endian.get(word_order, "<")
    for parameter, args in spec.items():
        param_type = data_types[args.get("data_type", "ushort")]
        # TODO What happens if the address map address size is not 16bit? Always 16bit for modbus
        data = addr_map[args["address"]: args["address"] + (param_type.size + 1) // 2]
        if any((x is None for x in data)):
            continue
        # Do word order swap here
        if word_order != byte_order:
            data = data[::-1]
        data_bytes = struct.pack(byte_order + "H" * len(data), *data)
        if byte_order == endian["big"]:
            data_bytes = data_bytes[len(data_bytes) - param_type.size:]
        else:
            data_bytes = data_bytes[:param_type.size]
        param = struct.unpack(f"{byte_order}{param_type.format}", data_bytes)[0]
        param &= args.get("mask", int("0x" + "F" * len(data_bytes) * 2, 16))  # Apply mask
        param = param >> args.get("rshift", 0)
        parameters[parameter] = param
        if args.get("bits"):
            parameters.update(filter_bits(parameters[parameter], args["bits"]))

    return parameters


def diff_dicts(new_dict, state_dict):
    """
    :param state_dict:
    :param new_dict:
    :return: A new subset of new_dict where the values differ from base_dict
    """
    diff = {k: new_dict[k] for k in new_dict if state_dict.get(k) != new_dict[k]}
    state_dict.update(diff)
    return diff


def block_reads(running_evt: threading.Event, *blocks, unit=0, timeout=3,
                resource_id="modbus_client"):
    client = rm[resource_id]
    error_cnt = 0
    while not running_evt.is_set():
        try:
            yield from _block_reads(client, *blocks, unit=unit, timeout=timeout)
            error_cnt = 0
        except BaseException as e:
            print(e)
            error_cnt += 1
            if error_cnt > 100:
                print("ABORTING")
                running_evt.set()


def _block_reads(client, *blocks, unit=0, timeout=3):
    addr_map = AddressMap()
    futs = {}
    for address, words in blocks:
        fut = client.read_holding_registers(address, words, unit=unit)
        futs[fut] = address
    completed, pending = futures.wait(futs, timeout=timeout)
    for fut, address in futs.items():
        if fut in completed:
            register_response = fut.result()
            if register_response.isError():
                continue
            addr_map.save_block(address, register_response.registers)
    if addr_map:
        yield addr_map


def imac2_blocks():
    return [(x, 125) for x in range(0, 0x3ff, 125)] + [(0x600, 125), (0x7d, 36)]


def pipeline_test(running_evt):
    # import pyaware.modbus_mock
    # client = pyaware.modbus_mock.ModbusSyncClientMock()
    client = ModbusTcpClient("192.168.16.190")
    rm.add_resource(client, "modbus_client")
    rm["modbus_client"].connect()
    spec = {
        "param1": {
            "address": 1,
            "data_type": "uchar"},
        "param2": {
            "address": 2,
            "data_type": "uint",
            "bits": {f"bit{x}": x for x in range(1, 17)}
        }
    }
    scheduler = rx.scheduler.ThreadPoolScheduler(multiprocessing.cpu_count())
    pipeline = rx.from_(block_reads(running_evt, *imac2_blocks()), scheduler=scheduler)
    state = {}
    diff_pipeline = pipeline.pipe(
        ops.map(partial(filter_parameters, spec=spec)),
        ops.map(partial(diff_dicts, state_dict=state)),
        ops.filter(lambda x: bool(x))
        # Add to SQLite

    )
    branch_subject = rx.subject.Subject()
    diff_pipeline.subscribe(branch_subject)

    branch_subject.subscribe(lambda x: print(x))
    branch_subject.subscribe(lambda x: print(x))
    input("Press to exit")
    # running.set()


def pipeline_test_2():
    import logging
    client = ModbusTcpClient("192.168.16.190")
    rm.add_resource(client, "modbus_client")
    imac2 = ModbusHoldingPipeline(rm["modbus_client"], *imac2_blocks(), spec={
        "param1": {
            "address": 0x97,
            "data_type": "uchar"},
    })
    # imac2.sub_read.subscribe(print)
    imac2.sub_diff.subscribe(logging.warning)
    imac2.start()
    input("EXIT")
    imac2.stop()


if __name__ == "__main__":
    pipeline_test_2()
