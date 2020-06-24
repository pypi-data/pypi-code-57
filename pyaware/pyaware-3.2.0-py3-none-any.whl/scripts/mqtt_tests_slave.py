"""
Script for simulating the MQTT messages coming from pyaware slave. Using imac2 as a base.
Responds to the commands being sent to it on local mqtt broker.
Has CLI interface for setting options
"""
import logging
import threading
import uuid
import asyncio
from datetime import datetime
import pymodbus.client.sync
from concurrent.futures import TimeoutError
import argparse
import pyaware.events
import pyaware.mqtt
import pyaware.mqtt.config
import pyaware.mqtt.paho
from pyaware.protocol.imac2.protocol import Imac2Protocol
from pyaware.protocol.modbus import AsyncWrapper

log = logging.getLogger("mqtt_tests")
logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(description="Sets up a minimal pyaware slave for imac to respond to mqtt commands")
parser.add_argument("-p", "--port", help="The com port of the imac if directly talking to it. If not provided, will "
                                         "default to mock the interface")
parser.add_argument("-i", "--ip", help="The ip address for the modbus TCP data")


def print_message(msg):
    log.info(f" topic: {msg.topic} data: {msg.payload}")


def command_form(cmd, data, destination="1805-G2"):
    if data is not '':
        return {"id": str(uuid.uuid4()), "destination": destination, "data": int(data), "name": cmd}
    else:
        return {"id": str(uuid.uuid4()), "destination": destination, "name": cmd}


async def main(args):
    pyaware.events.start()
    stop_evt = threading.Event()
    loop = asyncio.get_event_loop()
    if args.ip:
        # TODO find out why the async client isn't working
        from pymodbus.client.asynchronous.asyncio import ReconnectingAsyncioModbusTcpClient
        tcp_client = ReconnectingAsyncioModbusTcpClient()
        await tcp_client.start(args.ip)
        # _, tcp_client = tcp.AsyncModbusTCPClient(schedulers.ASYNC_IO, host=args.ip, loop=loop)
        # tcp_client = tcp_client.protocol
        # tcp_client = AsyncWrapper(pymodbus.client.sync.ModbusTcpClient(host=args.ip))
    else:
        tcp_client = None
    if args.port:
        if "tty" in args.port or "COM" in args.port:
            client = AsyncWrapper(
                pymodbus.client.sync.ModbusSerialClient(port=args.port, method="rtu", baudrate=9600, stopbits=1,
                                                        parity='N', timeout=1, strict=False),
                loop=loop)

        # from pymodbus.client.asynchronous.asyncio import AsyncioModbusSerialClient
        # from pymodbus.transaction import ModbusRtuFramer
        # from pymodbus.factory import ClientDecoder
        # client = AsyncioModbusSerialClient(args.port, framer=ModbusRtuFramer(ClientDecoder()), baudrate=9600,
        #                                    stopbits=2, parity="E")
        # await client.connect()
        # client = client.protocol
        else:
            from pymodbus.client.asynchronous.asyncio import ReconnectingAsyncioModbusTcpClient
            client = ReconnectingAsyncioModbusTcpClient()
            await client.start("10.1.1.21")
        imac = Imac2Protocol(client, client_eth=tcp_client, stop_evt=stop_evt, unit=1, _async=True, device_id="test")
    else:
        import simulations.imac2
        imac = simulations.imac2.MockImac2Protocol(
            roll_call=simulations.imac2.simulate_gg2(serial_number=1805, generation_id=1, number=1),
            eth_client=tcp_client, _async=True, device_id="test")
    config = pyaware.mqtt.config.LocalConfig("test_receive", "test")
    client = pyaware.mqtt.paho.Mqtt(config)
    client.client_reinit()

    async def printtopic():
        while True:
            try:
                print(await pyaware.events.wait("trigger_send", 3))
            except TimeoutError:
                print("Timeout on topic")

    # loop.create_task((printtopic()))

    @pyaware.events.subscribe(topic="trigger_send", in_thread=True)
    def module_data(data, timestamp):
        payload = []
        if isinstance(list(data.values())[0], dict):
            # Module data
            for serial, module_data in data.items():
                values = []
                for name, value in module_data.items():
                    if isinstance(value, datetime):
                        value = value.isoformat()
                    values.append({"name": name, "latest": value, "samples": 1})

                payload.append({
                    "version": 2,
                    "serial": serial,
                    "type": "imac-module-gg2",
                    "timestamp": f"{timestamp.isoformat()[:-3]}Z",
                    "values": values
                })
        else:
            values = []
            for name, value in data.items():
                if isinstance(value, datetime):
                    value = value.isoformat()
                values.append({"name": name, "latest": value, "samples": 1})

            payload.append({
                "version": 2,
                "type": "imac-controller",
                "timestamp": f"{timestamp.isoformat()[:-3]}Z",
                "values": values
            })

        client.devices["test"].publish_telemetry(payload)

    @pyaware.events.subscribe(topic="topology", in_thread=True)
    def topology(data, timestamp):
        for serial, devices in data.items():
            payload = {
                "version": 1,
                "serial": serial,
                "type": "imac-controller",
                "timestamp": f"{timestamp.isoformat()[:-3]}Z",
                "children": devices
            }
            client.devices["test"].publish_topic(payload, "topology")

    if args.ip:
        pyaware.events.publish("trigger_collect")
    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main(parser.parse_args()))
