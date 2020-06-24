import asyncio
import datetime
import json
import logging.handlers
import ssl
import threading
import time

import ruamel.yaml
import gmqtt

import pyaware.config
import pyaware.events
from pyaware import events
from pyaware.mqtt import factories, transformations, models
from pyaware.mqtt.exceptions import DeviceAttachError

log = logging.getLogger(__file__)


@events.enable
class Mqtt:
    """
    Class for setting up google mqtt protocol.
    Assumes that Key Certificates are already generated and the device is created with the associated public key
    """

    def __init__(self, config, gateway_config: dict = None, _async: bool = False):
        """
        :param config: Config dictionary. Must have at least the device_id specified
        """
        self.config = config
        self.gateway_config = gateway_config or {}
        self.mqtt_promises = {}
        self.devices = {}
        self.connected = asyncio.Event()
        self.connecting = asyncio.Event()
        self.client = gmqtt.Client(self.config.client_id, clean_session=False)
        self.topic_loggers = {}
        self.log_messages = True
        self.running = True
        self.sub_handles = {}
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        self.client.on_subscribe = self.on_subscribe

    def add_devices(self, *device_ids):
        """
        Add devices according to gateway configuration device ids
        :param device_ids:
        :return:
        """
        self.devices.update({d_id: Device(self, d_id) for d_id in device_ids})

    async def setup(self):
        """
        Get config if it exists. Then set up attached devices from the config
        :param device_ids: List of device ids belonging to this client
        :return:
        """
        self.add_devices(self.config.device_id)
        await asyncio.wait([dev.setup() for dev in self.devices.values()], return_when=asyncio.ALL_COMPLETED)

    def disconnect(self):
        self.running = False
        for dev in self.devices.values():
            dev.disconnect()
        for promise in self.mqtt_promises:
            try:
                promise.wait_for_publish()
            except AttributeError:
                pass
        self.client.disconnect()

    async def connect(self):
        if not self.running:
            raise RuntimeError("Client is not running, cannot connect")
        if self.connected.is_set():
            return
        self.connecting.set()
        self.client.set_auth_credentials("unused", self.config.jwt_token)
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        ssl_context.load_verify_locations(self.config.ca_certs_path)
        ssl_context = False
        await self.client.connect(self.config.host, self.config.port, ssl=ssl_context)
        await self.setup()
        self.connected.set()

    def publish(self, topic, payload, qos):
        msg = self.client.publish(topic, payload, qos)
        self.mqtt_log(msg.mid, topic, payload)
        self.mqtt_promises[msg.mid] = msg
        return msg.mid

    def form_message(self, data: dict, topic_type: str, **kwargs) -> str:
        parsers = self.config.parsers.get(topic_type, {})
        if parsers:
            factory = parsers.get("factory")
            if factory:
                factory = factories.get_factory(factory)
                msg = factory(data=data, **kwargs)
            else:
                msg = data
            for transform in parsers["transforms"]:
                msg = transformations.get_transform(**transform)(msg)
            msg = models.get_model(parsers["model"]).parse_obj(msg).json(exclude_none=True)
        else:
            msg = json.dumps(data)
        return msg

    def mqtt_log(self, mid, topic, payload):
        if self.log_messages:
            try:
                mqtt_log = self.topic_loggers[topic]
            except KeyError:
                mqtt_log = logging.getLogger(topic)
                mqtt_log.setLevel(logging.INFO)
                log_dir = pyaware.config.aware_path / "mqtt_log"
                log_dir.mkdir(parents=True, exist_ok=True)
                formatter = logging.Formatter('%(asctime)-15s %(message)s')
                handler = logging.handlers.TimedRotatingFileHandler(
                    log_dir / f"{topic.replace('/', '_')}.log", "h",
                    backupCount=2)
                handler.setFormatter(formatter)
                mqtt_log.addHandler(handler)
                mqtt_log.propagate = False
                self.topic_loggers[topic] = mqtt_log
            try:
                mqtt_log.info(f"Publishing {mid} {topic}:\n{json.dumps(json.loads(payload), indent=4, sort_keys=True)}")
            except:
                mqtt_log.info(f"Publishing {mid} {topic}:\n{payload}")

    def publish_telemetry(self, telemetry):
        for dev_id in telemetry:
            if dev_id in self.devices:
                self.devices[dev_id].publish_telemetry(self.parser(telemetry[dev_id]))

    def wait_on_promise(self, mid, timeout=5):
        start = time.time()
        while mid in self.mqtt_promises:
            if time.time() - start > timeout:
                raise TimeoutError("Failed to receive confirmation for msg id {} in {} seconds".format(mid, timeout))
            time.sleep(0.1)

    def subscribe(self, topic, callback, qos):
        self.client.subscribe(topic, qos)
        self.sub_handles[topic] = callback

    def on_message(self, client, topic, payload, qos, properties):
        handle = self.sub_handles.get(topic)
        if handle:
            handle(payload)

    def unsubscribe(self, topic):
        if self.connected.is_set():
            code, msg = self.client.unsubscribe(topic)
            if code != 0:
                log.warning(error_string(code))

    def unhandled_message(self, client, userdata, msg):
        """
        :param client:
        :param userdata:
        :param msg:
        :return:
        """
        log.warning("Unhandled Message on topic {}:\n{}".format(msg.topic, msg.payload))

    def on_connect(self, client, flags, rc, properties):
        log.info(f"Mqtt client {self.config.device_id} connected")
        self.connecting.clear()
        if rc == 0:
            self.connected.set()
        else:
            self.connected.clear()
            self.config.token_exp = datetime.datetime.utcnow()
            if self.running:
                asyncio.create_task(self.connect())

    def on_disconnect(self, client, packet, exc=None):
        log.info(f"Mqtt client {self.config.device_id} disconnected: Reason {exc}")
        self.connected.clear()
        if self.running:
            asyncio.create_task(self.connect())

    def __getitem__(self, item):
        return self.devices[item]

    def set_telemetry_parser(self, func):
        """
        Set the json parser for telemetry messages
        :param func:
        :return:
        """
        self.parser = func

    def on_subscribe(self, client, mid, qos, properties):
        # in order to check if all the subscriptions were successful, we should first get all subscriptions with this
        # particular msg (from one subscription request)
        subscriptions = client.get_subscriptions_by_mid(mid)
        for subscription, granted_qos in zip(subscriptions, qos):
            # in case of bad suback code, we can resend  subscription
            if granted_qos >= gmqtt.constants.SubAckReasonCode.UNSPECIFIED_ERROR.value:
                logging.info(
                    f"[RETRYING SUB {client._client_id}] mid {mid}, reason code: {granted_qos}, properties {properties}")
                client.resubscribe(subscription)
            logging.info(f"[SUBSCRIBED {client._client_id}] mid {mid}, QOS: {granted_qos}, properties {properties}")


@events.enable
class Device:
    """
    Abstracted device to keep messaging specific to a device or gateway contained in an object
    """
    device_id = ""

    def __init__(self, mqtt: Mqtt, device_id: str, _async: bool = False):
        self.mqtt = mqtt
        self.device_id = device_id
        self.base_topic = "/devices/{device_id}/".format(device_id=device_id)
        self._async = _async
        self.cmds_active = set([])
        if self.mqtt.config.device_id == self.device_id:
            self.is_gateway = True
            self.config = self.mqtt.gateway_config
            if self.config:
                self.mqtt.add_devices(*self.config.get("devices", []))
        else:
            self.is_gateway = False
            self.config = None
        if self._async:
            self.evt_setup = asyncio.Event()
        else:
            self.evt_setup = threading.Event()
        events.subscribe(self.send, topic=f"trigger_send/{self.device_id}")

    def __repr__(self):
        return "<Device {}>".format(self.device_id)

    async def setup(self):
        """
        Set up the topic subscriptions and published topics
        :return:
        """
        if self.is_gateway:
            log.info(f"Subscribing {self.device_id}/commands/system/stop")
            self.mqtt.subscribe(self.base_topic + "commands/system/stop", self.handle_stop, qos=1)
        else:
            log.info(f"Attaching to gateway {self.device_id}")
            self.mqtt.publish(self.base_topic + "attach", payload=json.dumps({'authorization': ""}),
                              qos=1)
        log.info(f"Subscribing {self.device_id}/config")
        self.mqtt.subscribe(self.base_topic + "config", self.handle_config, qos=1)
        log.info(f"Subscribing {self.device_id}/errors")
        self.mqtt.subscribe(self.base_topic + "errors", self.handle_errors, qos=1)
        log.info(f"Subscribing {self.device_id}/commands/#")
        self.mqtt.subscribe(self.base_topic + "commands/#", self.handle_commands, qos=1)
        self.evt_setup.set()
        log.info(f"Setup {self.device_id}")

    def subscribe(self, topic, callback, qos=1):
        """
        :param topic: Topic after the base topic of /devices/device_id/
        :param callback:
        :param qos:
        :return:
        """
        self.mqtt.subscribe(self.base_topic + topic, callback, qos=qos)

    def send(self, *, data: dict, topic_type: str, **kwargs):
        """
        This is the main entry point for publishing data from pyaware triggers.
        It is subscribed to f"trigger_send/{device_id}".
        It should pull out the device destination, the topic and the do the appropriate data transformations for the
        destination
        :param data:
        :param timestamp:
        :return:
        """
        if self.evt_setup.is_set():
            payload = self.mqtt.form_message(data=data, topic_type=topic_type, **kwargs)
            self.mqtt.publish(self.base_topic + "events/telemetry", payload, qos=1)
        else:
            log.warning(f"Could not send telemetry from {self} as it is not setup")

    def publish_state(self, msg):
        """
        This should be a snapshot of the device state. This should be a representation of the device and not a complete
        parameter values static.
        :param msg:
        :return:
        """
        if self.evt_setup.is_set():
            self.mqtt.publish(self.base_topic + "state", payload=msg, qos=1)
        else:
            log.warning("Could not send telemetry from {} as it is not setup".format(self))

    def publish_telemetry(self, msg):
        log.debug("Publishing telemetry")
        log.debug(self.mqtt.client)
        if self.evt_setup.is_set():
            mid = self.mqtt.publish(self.base_topic + "events/telemetry", payload=msg, qos=1)
            log.debug("Sent telemetry {}".format(mid))
        else:
            log.warning("Could not send telemetry from {} as it is not setup".format(self))

    @events.subscribe(topic="mqtt_topic_send")
    def publish_topic(self, msg, mqtt_topic):
        log.debug(f"Publishing {mqtt_topic}")
        log.debug(self.mqtt.client)
        if self.evt_setup.is_set():
            parsers = self.mqtt.config.parsers.get(mqtt_topic, {})
            if parsers:
                for transform in parsers["transforms"]:
                    msg = transformations.get_transform(**transform)(msg)
                msg = models.get_model(parsers["model"]).parse_obj(msg).json(exclude_none=True)
            mid = self.mqtt.publish(f"{self.base_topic}{mqtt_topic}", payload=msg, qos=1)
            log.debug(f"Sent {mqtt_topic} {mid}")
        else:
            log.warning(f"Could not send telemetry from {self} as it is not setup")

    # TODO this needs to have a instance ID as any more than one MQTT device will break here (eg. 2 imacs)
    @events.subscribe(topic=f"mqtt_command_response")
    def publish_command_response(self, data, timestamp: datetime.datetime):
        data["timestamp"] = f"{timestamp.isoformat()}"
        if data["id"] not in self.cmds_active:
            return
        for param, value in data.get("data", {}).items():
            if isinstance(value, datetime.datetime):
                data["data"][param] = f"{value.isoformat()}"
        log.debug("Publishing command response")
        if self.evt_setup.is_set():
            mid = self.mqtt.publish(self.base_topic + "events/telemetry/commands", payload=json.dumps(data), qos=1)
            log.debug("Sent command response {}".format(mid))
        else:
            log.warning("Could not send command response from {} as it is not setup".format(self))
        if data["type"] > 1:
            self.cmds_active.remove(data["id"])

    def disconnect(self):
        self.mqtt.unsubscribe(self.base_topic + "config")
        self.mqtt.unsubscribe(self.base_topic + "errors")
        self.mqtt.unsubscribe(self.base_topic + "commands/#")
        if self.is_gateway:
            self.mqtt.unsubscribe(self.base_topic + "commands/system/stop")

    def handle_config(self, unused_client, unused_userdata, mid):
        """
        If the gateway handle config to update devices and set up remaining pyaware config
        :return:
        """
        if self.is_gateway:
            """
            Check if new config is different to the old config
            If so, override config cache present and restart pyaware cleanly
            """
            log.debug("Gateway config received: {}".format(mid.payload))
            new_config = ruamel.yaml.safe_load(mid.payload.decode())
            # if new_config:
            #     if pyaware.config.config_changes(self.mqtt.gateway_config, new_config):
            #         with open(pyaware.config.aware_path / "config" / "gateway.yaml", 'w') as f:
            #             ruamel.yaml.dump(new_config, f)
            #         log.warning("New gateway configuration detected. Stopping process")
            #         pyaware.stop()
        else:
            log.debug("Device config received: {}".format(mid.payload))
            self.config = ruamel.yaml.safe_load(mid.payload.decode())

    def handle_errors(self, unused_client, unused_userdata, mid):
        pass

    def handle_commands(self, unused_client, unused_userdata, mid):
        try:
            msg = json.loads(mid.payload.decode('utf-8'))
        except AttributeError:
            # Ignore commands with no payload
            return
        except json.decoder.JSONDecodeError as e:
            log.exception(e)
            return
        self.cmds_active.add(msg["id"])
        pyaware.events.publish(f"mqtt_command/{self.device_id}", data=msg,
                               timestamp=datetime.datetime.utcnow())

    def handle_stop(self, unused_client, unused_userdata, mid):
        pyaware.stop()
