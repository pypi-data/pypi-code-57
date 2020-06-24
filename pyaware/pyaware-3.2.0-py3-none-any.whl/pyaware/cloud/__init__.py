import os
import datetime
import pprint
import logging
import json

import pyaware.mqtt
import pyaware.mqtt.config
import pyaware.mqtt.paho

log = logging.getLogger(__file__)


def mock_return(data):
    return data


MSG_QUEUE = []


def json_v1(data):
    """
    Forms the Report data into a set of messages for MQTT V1 API
    Where
      topic is device_id, device_type
    and
      message is of the form
    {
        "dateTime": get_timestamp(),
        "parameterValues": [
            {
                "parameterName": "xxxxx",
                "data": {
                    "<aggregate1>": <number>,
                    "<aggregate2>": <number>,
                    ...
                }
            },
            {
                "parameterName": "xxxxx",
                "data": {
                    "<aggregate3>": <number>,
                    "<aggregate2>": <number>,
                    ...
                }
            }
        ]
    }
    :param data: Response from Report.report(data)
    :return: A list of MQTT messages to send of form
    [{"topic": <topic>, "msg": <message>}]
    """
    msgs = []
    for dev_id, dev_data in data.items():
        topic = {"device_id": dev_id, "device_type": dev_data["device_type"]}
        msg = {"dateTime": "{}Z".format(datetime.datetime.utcnow().isoformat()[:-3]),
               "parameterValues": [{"parameterName": field, "data": value} for field, value in
                                   dev_data["data"].items()]}
        msgs.append({"topic": topic, "msg": msg})

    return msgs


def json_v2(data):
    """
    Returns a single telemetry message to send via MQTT.
    Assumes data is of the form {"data": {<parameterName>: [<data points>]}
    :param data: Response from Report.report(data)[<device_id>]
    :return: A list of MQTT messages to send of form
    {<device_id>: <message>}
    """
    return {"dateTime": "{}Z".format(datetime.datetime.utcnow().isoformat()[:-3]),
            "parameterValues": [{"parameterName": field, "data": value} for field, value in
                                data["data"].items()]}


def json_v3(data):
    """
    Returns a single telemetry message to send via MQTT.
    Assumes data is of the form {"data": {<parameterName>: [<data points>]}
    :param data: Response from Report.report(data)[<device_id>]
    :return: A list of MQTT messages to send of form
    {<device_id>: <message>}
    :return JSON string
    """
    return json.dumps({"dateTime": "{}Z".format(datetime.datetime.utcnow().isoformat()[:-3]),
                       "parameterValues": [{"parameterName": field, "data": value} for field, value in
                                           data["data"].items()]})


def sample_count(data):
    samples = 0
    for dev_id, dev_data in data.items():
        for field, values in dev_data["data"].items():
            samples += values["samples"]
    return samples


def ibm_cloud_v1(data, client):
    """
    Connect to IBM MQTT via credentials

    :return:
    """
    import ibmiotf.gateway
    global MSG_QUEUE
    MSG_QUEUE.extend(data)
    options = ibmiotf.gateway.ParseConfigFile(os.path.join(os.getenv("AWAREPATH"), "credentials", "GatewayCredentials"))
    client = ibmiotf.gateway.Client(options)
    try:
        client.connect()
    except ibmiotf.ConnectionException as e:
        log.info(e)
        raise
    # TODO clean this up with proper message queuing
    # https://stackoverflow.com/questions/26413613/asyncio-is-it-possible-to-cancel-a-future-been-run-by-an-executor
    try:
        while True:

            try:
                msg = MSG_QUEUE.pop()
            except IndexError:
                # Finished messages
                break
            try:
                log.debug("Publishing to {}:{}".format(msg["topic"]["device_type"], msg["topic"]["device_id"]))
                if not client.publishDeviceEvent(msg["topic"]["device_type"], msg["topic"]["device_id"],
                                                 "parameterValues", "json", msg["msg"]):
                    # Message failed, put it at the end of the queue to resend
                    log.warning("Failed publishing to {}:{} queuing message for next scheduled report".format(
                        msg["topic"]["device_type"], msg["topic"]["device_id"]))
                    MSG_QUEUE.append(msg)

            except:
                # Message failed, put it at the end of the queue to resend
                log.warning("Failed publishing to {}:{} queuing message for next scheduled report".format(
                    msg["topic"]["device_type"], msg["topic"]["device_id"]))
                MSG_QUEUE.append(msg)
                raise
    finally:
        client.disconnect()


def ibm_cloud_v2_cloud_connect():
    import ibmiotf.gateway
    options = ibmiotf.gateway.ParseConfigFile(
        os.path.join(os.getenv("AWAREPATH"), "credentials", "gateway"))
    log.info("IBM Config Parsed")
    client = ibmiotf.gateway.Client(options)
    while True:
        try:
            if not client.connectEvent.is_set():
                log.info("Connecting to IBM cloud")
                client.connect()
                log.info("Connected to IBM cloud")
            else:
                break
        except BaseException as e:
            log.warning(e)
            client.connectEvent.wait(1)
    return client


def ibm_cloud_v2(data, client):
    """
    Connect to IBM MQTT via credentials

    :return:
    """
    connect_attempts = 1
    while True:
        try:
            if not client.connectEvent.is_set():
                log.info("Connecting to IBM cloud")
                client.connect()
                log.info("Connected to IBM cloud")
            else:
                break
        except BaseException as e:
            log.warning(e)
            if connect_attempts < 10:
                client.connectEvent.wait(1)
            else:
                raise
            connect_attempts += 1

    def publish_cbf(msg):
        def tmp():
            log.debug(msg)

        return tmp

    for msg in data:
        log.debug("Publishing to {}:{}".format(msg["topic"]["device_type"], msg["topic"]["device_id"]))
        if not client.publishDeviceEvent(
                msg["topic"]["device_type"], msg["topic"]["device_id"], "parameterValues", "json", msg["msg"],
                qos=1,
                on_publish=publish_cbf(
                    "Successfully published to {}:{}".format(msg["topic"]["device_type"],
                                                             msg["topic"]["device_id"]))):
            # Message failed, put it at the end of the queue to resend
            log.warning("Failed publishing to {}:{}".format(msg["topic"]["device_type"], msg["topic"]["device_id"]))


def gcp_v1_publish(data, client):
    """
    :param data:
    :return:
    """
    client.connect()
    for msg in data:
        log.debug("Publishing to {}:{}".format(msg["topic"]["device_type"], msg["topic"]["device_id"]))
        client[msg["topic"]["device_id"]].publish_telemetry(msg["msg"])


def gcp_v1_config():
    config = pyaware.config.load_config(os.path.join(os.getenv("AWAREPATH"), "config", "cloud.yaml"))
    config = pyaware.mqtt.config.GCPCloudConfig(**config)
    gateway_config = pyaware.config.load_config(
        os.path.join(os.getenv("AWAREPATH"), "config", "gateway.yaml"))
    client = pyaware.mqtt.paho.Mqtt(config, gateway_config)
    client.setup()
    return client


def gcp_v2_config(aware_path):
    config = pyaware.config.load_config(aware_path / "config" / "cloud.yaml")
    config = pyaware.mqtt.config.GCPCloudConfig(**config)
    gateway_config = pyaware.config.load_config(aware_path / "config" / "gateway.yaml")
    client = pyaware.mqtt.paho.Mqtt(config, gateway_config)
    client.client_reinit()
    return client


def ibm_cloud_v2_sub(callback):
    client = ibm_cloud_v2_cloud_connect()
    client.subscribeToDeviceCommands(deviceId="+", deviceType="+")
    client.commandCallback = callback
    client.deviceCommandCallback = callback


def get_api(api_version):
    API = {
        "MOCK_V1": {
            "data_parser": mock_return,
            "cloud_publish": pprint.PrettyPrinter(indent=4).pprint
        },
        "MOCK_V2": {
            "data_parser": json_v1,
            "cloud_publish": pprint.PrettyPrinter(indent=4).pprint
        },
        "MOCK_SAMPLES": {
            "data_parser": sample_count,
            "cloud_publish": print
        },
        "IBMIOTF_V1": {
            "data_parser": json_v1,
            "cloud_publish": ibm_cloud_v1
        },
        "IBMIOTF_V2": {
            "data_parser": json_v1,
            "cloud_publish": ibm_cloud_v2,
            "cloud_subscribe": ibm_cloud_v2_sub,
        },
        "GCP_V1": {
            "data_parser": json_v3,
            "cloud_publish": gcp_v1_publish,
            "cloud_config": gcp_v1_config
        }

    }
    api = API[api_version]
    return api


def get_client(api_version):
    if api_version == "IBMIOTF_V1":
        import ibmiotf.gateway
        options = ibmiotf.gateway.ParseConfigFile(
            os.path.join(os.getenv("AWAREPATH"), "credentials", "GatewayCredentials"))
        return ibmiotf.gateway.Client(options)
    elif api_version == "IBMIOTF_V2":
        import ibmiotf.gateway
        options = ibmiotf.gateway.ParseConfigFile(
            os.path.join(os.getenv("AWAREPATH"), "credentials", "gateway"))
        log.info("IBM Config Parsed")
        return ibmiotf.gateway.Client(options)
    elif api_version == "GCP_V1":
        client = gcp_v1_config()
        client.set_telemetry_parser(get_api(api_version)["data_parser"])
        return client
    elif api_version == "MOCK_V2":
        import unittest.mock
        class MockAPI(unittest.mock.MagicMock):
            def publish_telemetry(self, telemetry):
                pprint.PrettyPrinter(indent=4).pprint(telemetry)

        return MockAPI()


def publish(data, api_version, client=None):
    api = get_api(api_version)
    parsed_data = api["data_parser"](data)
    return api["cloud_publish"](parsed_data, client)


def subscribe(callback_handler, api_version):
    api = get_api(api_version)
    api["cloud_subscribe"](callback_handler)
