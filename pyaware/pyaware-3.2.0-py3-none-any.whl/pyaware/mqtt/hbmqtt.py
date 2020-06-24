import datetime
import logging.handlers
import asyncio
from pyaware import events
import hbmqtt.client
from hbmqtt.mqtt.constants import QOS_1
from pyaware.mqtt import models, transformations, factories, log_to_file
import pyaware.config
import uuid

try:
    import rapidjson as json
except ImportError:
    import json

log = logging.getLogger(__file__)


# Patch the client to handle reconnect logic
class MQTTClient(hbmqtt.client.MQTTClient):
    def __init__(self, client_id=None, config=None, loop=None):
        self._on_connect = None
        self.uri_gen = None
        self.disconnect_after = 0
        self._on_connect_task = None
        self.connect_params = {}
        super().__init__(client_id, config, loop)

    @property
    def on_connect(self):
        """If implemented, called when the broker responds to our connection
        request."""
        return self._on_connect

    @on_connect.setter
    def on_connect(self, func):
        """ Define the connect callback implementation.

        Expected signature is:
            connect_callback()
        """
        self._on_connect = func

    @asyncio.coroutine
    def connect(self,
                uri=None,
                cleansession=None,
                cafile=None,
                capath=None,
                cadata=None,
                extra_headers=None):
        if extra_headers is None:
            extra_headers = {}
        self.connect_params = {
            "uri": uri,
            "cleansession": cleansession,
            "cafile": cafile,
            "capath": capath,
            "cadata": cadata
        }
        try:
            return (yield from self._do_connect())
        except BaseException as be:
            self.logger.warning("Connection failed: %r" % be)
            auto_reconnect = self.config.get('auto_reconnect', False)
            if not auto_reconnect:
                raise
            else:
                return (yield from self.reconnect())

    @asyncio.coroutine
    def _do_connect(self):
        if self.uri_gen:
            uri = self.uri_gen()
        else:
            uri = self.connect_params["uri"]
        cleansession = self.connect_params["cleansession"]
        cafile = self.connect_params["cafile"]
        capath = self.connect_params["capath"]
        cadata = self.connect_params["cadata"]
        self.session = self._initsession(uri, cleansession, cafile, capath, cadata)
        return_code = yield from self._connect_coro()
        self._disconnect_task = asyncio.ensure_future(self.handle_connection_close(), loop=self._loop)
        if self.disconnect_after:
            async def disconnect_later():
                await asyncio.sleep(self.disconnect_after)
                log.warning("Scheduled mqtt disconnect")
                await self.disconnect()
                log.warning("Scheduled mqtt reconnect")
                await self.reconnect(self.connect_params.get("clean_session", True))

            asyncio.ensure_future(disconnect_later(), loop=self._loop)
        if return_code == 0 and self.on_connect:
            self._on_connect_task = asyncio.ensure_future(self.on_connect(), loop=self._loop)
        return return_code


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
        self.connecting = asyncio.Event()
        self.evt_setup = asyncio.Event()
        self.client = MQTTClient(self.config.client_id,
                                 config={"default_qos": self.config.publish_qos, "auto_reconnect": True,
                                         "reconnect_max_interval": 60,
                                         "reconnect_retries": -1, "keep_alive": self.config.keepalive})
        self.client.uri_gen = self.gen_uri
        if self.config.token_life > 1:
            self.client.disconnect_after = self.config.token_life * 60 - 60
        else:
            self.client.disconnect_after = 0
        self.client.on_connect = self.setup
        self.topic_loggers = {}
        self.log_messages = True
        self.sub_handles = {}

    async def setup(self):
        while True:
            if pyaware.evt_stop.is_set():
                raise RuntimeError("Pyaware is stopped")
            try:
                await self._setup()
                self.evt_setup.set()
                log.info(f"Setup gateway mqtt {self.config.device_id}")
                break
            except (asyncio.CancelledError, RuntimeError, GeneratorExit):
                raise
            except BaseException as e:
                log.exception(e)
            await asyncio.sleep(1)

    async def _setup(self):
        """
        Get config if it exists. Then set up attached devices from the config
        :param device_ids: List of device ids belonging to this client
        :return:
        """
        device_attaches = [
            self.publish(f"/devices/{device_id}/attach", json.dumps({'authorization': ""}),
                         QOS_1) for device_id in self.gateway_config.get("devices", [])]
        await asyncio.gather(*device_attaches)
        sub_topics = [
            (f"/devices/{self.config.device_id}/config", 1),
            (f"/devices/{self.config.device_id}/errors", 0),
            (f"/devices/{self.config.device_id}/commands/#", 0),
        ]
        sub_topics.extend([(f"/devices/{device_id}/config", 1) for device_id in self.gateway_config.get("devices", [])])
        sub_topics.extend([(f"/devices/{device_id}/errors", 0) for device_id in self.gateway_config.get("devices", [])])
        sub_topics.extend(
            [(f"/devices/{device_id}/commands/#", 0) for device_id in self.gateway_config.get("devices", [])])
        self.sub_handles = [
            (f"config", self.handle_config),
            (f"errors", self.handle_errors),
            (f"commands/system/stop", self.handle_stop),
            (f"commands", self.handle_commands),
        ]
        await self.client.subscribe(sub_topics)

    async def connect(self):
        if self.config.authentication_required:
            await self.client.connect(
                uri=None,
                cleansession=self.config.clean_session,
                cafile=self.config.ca_certs_path)
        else:
            await self.client.connect(
                uri=f"mqtt://{self.config.host}:{self.config.port}",
                cleansession=self.config.clean_session)

    def gen_uri(self):
        if self.config.authentication_required:
            return f"mqtts://unused:{self.config.jwt_token.decode('utf-8')}@{self.config.host}:{self.config.port}"
        else:
            return f"mqtt://{self.config.host}:{self.config.port}"

    async def loop(self):
        while True:
            if pyaware.evt_stop.is_set():
                log.info(f"Stopping event loop for hbmqtt client {self.config.device_id}")
                break
            try:
                msg = await self.client.deliver_message(timeout=1)
            except asyncio.TimeoutError:
                continue
            except (AttributeError, IndexError):
                await asyncio.sleep(1)
                continue
            except BaseException as e:
                log.exception(e)
                continue
            asyncio.get_event_loop().run_in_executor(None, self.sub_handler, msg)
            log.info("Message Received")

    def sub_handler(self, msg):
        for handle_str, handle in self.sub_handles:
            if handle_str in msg.topic:
                try:
                    if handle is not None:
                        handle(msg)
                        break
                except BaseException as e:
                    log.exception(e)

    @events.subscribe(topic=f"trigger_send/#", parse_topic=True)
    async def send(self, *, data: dict, topic_type: str, topic: str, **kwargs):
        device_id = topic.split("trigger_send/")[-1]
        if pyaware.evt_stop.is_set():
            raise RuntimeError("Pyaware is stopped")
        try:
            await asyncio.wait_for(self.evt_setup.wait(), 10)
        except asyncio.TimeoutError:
            log.warning(f"Could not send telemetry from {self} as it is not setup")
            return
        payload = self.form_message(data=data, topic_type=topic_type, **kwargs)
        await self.publish(f"/devices/{device_id}/events/telemetry", payload,
                           qos=self.config.publish_qos)

    async def publish(self, topic, payload, qos):
        try:
            payload = payload.encode()
        except AttributeError:
            pass
        uid = self.mqtt_log(topic, payload)
        await self.client.publish(topic, payload, qos)
        self.mqtt_log(topic, payload, uid)

    def form_message(self, data: dict, topic_type: str, **kwargs) -> bytes:
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

    def mqtt_log(self, topic, payload, mid=None):
        if log_to_file:
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
            if mid:
                mqtt_log.info(f"Resolved {self.config.host} {mid}")
                return
            mqtt_log.info(f"Publishing {self.config.host} {mid}:\n{payload}")
            return uuid.uuid4()

    async def subscribe(self, topic, callback, qos):
        await self.client.subscribe([(topic, qos)])
        self.sub_handles[topic] = callback

    async def unsubscribe(self, topic):
        if self.client._connected_state.is_set():
            await self.client.unsubscribe([topic])
            self.sub_handles.pop(topic, None)

    def handle_config(self, msg):
        """
        If the gateway handle config to update devices and set up remaining pyaware config
        :return:
        """
        if msg.topic == f"/devices/{self.config.device_id}/config":
            """
            Check if new config is different to the old config
            If so, override config cache present and restart pyaware cleanly
            """
            log.info("Gateway config received: {}".format(msg.data))
            if msg.data:
                new_config_raw = msg.data.decode()
                if new_config_raw != pyaware.config.load_config_raw(pyaware.config.config_main_path):
                    pyaware.config.save_config_raw(pyaware.config.config_main_path, new_config_raw)
                    log.warning("New gateway configuration detected. Stopping process")
                    pyaware.stop()
        else:
            log.info(f"Device config {msg.topic} received: {msg.data}")

    def handle_errors(self, mid):
        try:
            log.warning(f"Error received from gcp\n{mid.data.decode('utf-8')}")
        except:
            log.warning(f"Error received from gcp\n{mid.data}")

    def handle_commands(self, mid):
        try:
            msg = json.loads(mid.payload)
        except AttributeError:
            # Ignore commands with no payload
            return
        except json.JSONDecodeError as e:
            log.exception(e)
            return
        self.cmds_active.add(msg["id"])
        pyaware.events.publish(f"mqtt_command/{self.device_id}", data=msg,
                               timestamp=datetime.datetime.utcnow())

    def handle_stop(self, mid):
        pyaware.stop()

    # TODO this needs to have a instance ID as any more than one MQTT device will break here (eg. 2 imacs)
    @events.subscribe(topic=f"mqtt_command_response")
    async def publish_command_response(self, data, timestamp: datetime.datetime):
        data["timestamp"] = f"{timestamp.isoformat()}"
        if data["id"] not in self.cmds_active:
            return
        for param, value in data.get("data", {}).items():
            if isinstance(value, datetime.datetime):
                data["data"][param] = f"{value.isoformat()}"
        log.debug("Publishing command response")
        if self.evt_setup.is_set():
            await self.mqtt.publish(self.base_topic + "events/telemetry/commands", payload=json.dumps(data),
                                    qos=self.mqtt.config.publish_qos)
            log.debug("Sent command response")
        else:
            log.warning("Could not send command response from {} as it is not setup".format(self))
        if data["type"] > 1:
            self.cmds_active.remove(data["id"])
