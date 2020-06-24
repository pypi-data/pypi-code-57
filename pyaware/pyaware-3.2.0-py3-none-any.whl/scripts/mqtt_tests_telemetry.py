import logging
import asyncio
import json
import argparse
import pyaware
import pyaware.mqtt
import pyaware.mqtt.config
import pyaware.mqtt.paho

log = logging.getLogger("mqtt_tests")
logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(description="Sets up a minimal pyaware slave for imac to respond to mqtt commands")
parser.add_argument("-p", "--port", help="The com port of the imac if directly talking to it. If not provided, will "
                                         "default to mock the interface")


async def main(args):
    config = pyaware.mqtt.config.LocalConfig("test_receive", "test")
    client = pyaware.mqtt.paho.Mqtt(config)
    client.client_reinit()
    client.devices["test"].publish_telemetry(json.loads("{\"values\": [{\"name\":\"Bob\", \"data\": {\"value\":2}}]}"))

    await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main(parser.parse_args()))
