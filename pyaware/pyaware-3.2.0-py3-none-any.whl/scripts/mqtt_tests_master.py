"""
Script for simulating the MQTT messages coming from pyaware master.
Interactively send commands to a destination. Serial number is the destination
"""
import uuid
import json
import pyaware.mqtt
import pyaware.mqtt.config
import logging

import pyaware.mqtt.paho

log = logging.getLogger("master")
logging.basicConfig(level=logging.DEBUG)


def print_message(client, userdata, msg):
    log.debug(f"topic: {msg.topic} data: {json.loads(msg.payload)}")


def command_form(cmd, data, destination="1805-G2"):
    formed_command = {"id": str(uuid.uuid4()), "name": cmd}
    if destination:
        formed_command["destination"] = destination
    if data:
        data = eval(data)
        if isinstance(data, int):
            data = {"value": data}
        formed_command["data"] = data
    return formed_command


if __name__ == "__main__":
    config = pyaware.mqtt.config.LocalConfig("test_send", "test")
    client = pyaware.mqtt.paho.Mqtt(config)
    client.client_reinit()
    client.subscribe("/devices/test/events/telemetry/commands", print_message, qos=1)
    client.subscribe("/devices/test/events/telemetry/topology", print_message, qos=1)
    client.subscribe("/devices/test/events/telemetry", print_message, qos=1)
    while True:
        destination = input("Destination Please")
        cmd_str = input("Command Please")
        data = input("Data Please")
        # destination = input("Destination Please")
        cmd = command_form(cmd_str, data, destination)
        # cmd = command_form(cmd_str, data)
        client.publish("/devices/test/commands", payload=cmd, qos=1)
        print(cmd)
