#  Copyright (c) 2020 Netflix.
#  All rights reserved.
#
import json
import logging
from concurrent.futures import Future
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict
from dataclasses import dataclass
from functools import partial
from pathlib import Path
from threading import Event
from threading import RLock
from threading import Timer
from traceback import format_exc
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from uuid import uuid4

from paho.mqtt.client import Client

# Implementation libs
from kaiju_mqtt_py.mqtt_enum import QOS_AT_LEAST_ONCE
from kaiju_mqtt_py.sslconfig import SslConfig
from kaiju_mqtt_py.sslconfigmanager import SslConfigManager


class MultipleSubscriptionError(Exception):
    def __init__(self, topic):
        super().__init__(f"KaijuMQTTPy only supports a single subscription per topic. Second subscription attempted for " f"topic: {topic}")


class ReturnMe:
    """A value inside a reference-safe object."""

    def __init__(self):
        """Constructor."""
        self.value = None


@dataclass
class MqttPacket:
    """Topic and payload struct."""

    topic: str
    payload: dict


@dataclass
class Subscription:
    """Subscription information"""

    topic: str
    callback: Callable
    options: Dict

    def __eq__(self, other):
        return (
            isinstance(other, Subscription)
            and self.topic == other.topic  # noqa: W503
            and self.callback == other.callback  # noqa: W503
            and frozenset(self.options.items()) == frozenset(other.options.items())  # noqa: W503
        )


class MqttStatusException(Exception):
    """Shaped exception for easier forming of a structured exception."""

    def __init__(self, status: int = 500, message: str = "", extra: dict = None):
        """Constructor."""
        super(MqttStatusException, self).__init__(message)
        if extra is None:
            extra = {}
        self.status = status
        self.extra = extra if isinstance(extra, dict) else {}

    def as_dict(self, trace: Any, request: Dict):
        return {"status": self.status, "body": {"error": {"message": str(self), "trace": trace, **self.extra, "request": request}}}

    def __str__(self):
        return super(MqttStatusException, self).__str__()


@dataclass
class MqttResponse:
    body: str
    status: int


class JsonUnwrapperAroundCallback:
    def __init__(self, callback):
        self.callback = callback

    def __call__(self, client: Client, userdata: "KaijuMqtt", packet: MqttPacket):
        """
        First unwrap strings containing json, then forward to the intended callback.

        :param client:
        :param userdata:
        :param packet:
        :return:
        """
        response = {}
        if packet:
            try:
                response = json.loads(packet.payload)
            except ValueError:
                response = {"error": "failed to parse msg", "msg": str(packet)}
        json_decoded_payload = MqttPacket(topic=packet.topic, payload=response)
        self.callback(client, userdata, json_decoded_payload)


def get_json_unwrapped_callback(callback: Callable):
    """
    Handle the user code after decoding the JSON for them.

    The default message handler must have the client, userdata, packet signature.
    This allows us to call that by creating a closure that already handles the boring json work.

    :param callback: User provided code with the signature def x(client, userdata, packet)
    :return: the new closure to call later
    """

    return JsonUnwrapperAroundCallback(callback)


def get_error_handler_for_client_callback(kaiju: "KaijuMqtt", logger: logging.Logger, topic: str, client_function: Callable):
    """
    Return a closure around the client callback for a handle command

    Handle typical errors by forming an appropriate error structure.
    If the client_function returns a dict, the result will be serialized (and deserialized) automatically to json.
    An MqttStatusException thrown or returned from client_function is an ideal way to respond with errors.
    Other errors will be rewrapped in a shape something like the MqttStatusException and rethrown.

    :param topic:
    :param logger:
    :param kaiju:
    :param client_function: Function in the form of def x(request_topic: Text, msg: MqttPacket) -> dict
    :return: Closure around the client_function with the above error handling done.
    """

    def handle_errors_from_client_code(client: Client, userdata: KaijuMqtt, msg: MqttPacket):
        """
        Closure to capture the intended user message handler and call it on request.

        :param client:
        :param userdata:
        :param msg:
        :return:
        """
        request_topic = msg.topic
        if request_topic is None:
            raise SyntaxError(f"FATAL: Handler for topic {topic} failed to receive request topic.")
        response_topic = f"_response/{request_topic}"

        def send_response(kaiju: Client, response_topic: str, future: Future):
            try:
                result_msg = future.result()
                if not isinstance(result_msg, MqttResponse):
                    result_msg = MqttResponse(status=200, body=result_msg)
                logger.info(f"publishing a response: {response_topic} {result_msg}")
                kaiju.publish(response_topic, result_msg)
            except MqttStatusException as error:
                logger.debug("Got an MqttStatusException, passing along")
                return kaiju.publish(response_topic, error.as_dict(format_exc(), msg.payload))
            except Exception as error:
                logger.exception(
                    error, "Got a normal exception processing handle functions, wrapping in 500 error",
                )
                return kaiju.publish(
                    response_topic,
                    {"status": 500, "body": {"error": {"message": str(error), "trace": format_exc()}, "request": msg.payload}},
                )

        logger.debug("Calling client code for {} message".format(request_topic))
        kaiju.thread_pool.submit(client_function, request_topic, msg).add_done_callback(partial(send_response, kaiju, response_topic))

    return handle_errors_from_client_code


def get_custom_request_responder(logger: logging.Logger, clear_timeout: Callable, return_me: ReturnMe, handled_event: Event):
    """
    Get a custom request handler function that captures some closure data.

    :param logger:
    :param clear_timeout:
    :param return_me:
    :param handled_event:
    :return:
    """

    def handle_response_to_this_request(client: Client, user_data: KaijuMqtt, packet: MqttPacket):
        """
        Set the originally provided ReturnMe.value to the response from the request and set the Event.

        This is the success path : the response has arrived, let the requester know.
        This is a closure around the return_me and handled_event variables to indicate completion and values.

        :param user_data:
        :param client:
        :param packet:
        :return:
        """
        logger.debug("Got response to my request")
        clear_timeout()

        response = packet.payload

        if not isinstance(response, dict) or "status" in response:
            # bare values, or dictionaries in our preferred format
            logger.info(f"Received response: {response}")
            return_me.value = response
            handled_event.set()
            return

        logger.debug(f"Handling unsuccessful response to request: {response}")
        if "body" in response and isinstance(response["body"], str):
            """To return an exception message easily, we can present it like this."""
            response["body"] = {
                "message": response["body"],
                "name": response["body"],
            }
        return_me.value = response
        handled_event.set()

    return handle_response_to_this_request


def on_connect(client: Client, userdata: "KaijuMqtt", flags, rc):
    """Set the connected state and subscribe to existing known topics."""

    userdata.logger.info("KaijuMQTT Connected")
    with userdata.unsub_lock:  # threads might enter here simultaneously. Stop that.
        userdata.connected_event.set()
        userdata.disconnected_event.clear()

        for sub in userdata.subscribe_topic_to_json_wrapped_functions_map.values():
            userdata.subscribe(sub.topic, sub.callback, sub.options, overwrite=True)

    if userdata.user_on_connect is not None:
        userdata.user_on_connect(userdata)


def on_disconnect(client: Client, userdata: "KaijuMqtt", rc):
    """Set the disconnected state."""

    userdata.logger.info("KaijuMQTT Disconnected")
    userdata.connected_event.clear()
    userdata.disconnected_event.set()

    if not userdata.user_requested_close:
        userdata.client.reconnect()

    if userdata.user_on_disconnect is not None:
        userdata.user_on_disconnect(userdata)


def on_message(client: Client, userdata: "KaijuMqtt", packet: MqttPacket):
    """
    Handle MQTT messages that are not directly being looked for.

    :param client:
    :param userdata:
    :param packet:
    :return:
    """
    userdata.logger.debug(
        f"An unexpected message arrived on topic '{packet.topic}'. " "This might be a programming bug or just a very late response."
    )


class KaijuMqtt:
    """
    A pub/sub and request/response protocol over an mqtt session.
    """

    logger: logging.Logger = logging.getLogger(__name__)

    def __init__(self, json_stringify: Callable = json.dumps, user_on_connect=None, user_on_disconnect=None):
        """Construct, but no more."""
        self.handler_unsubscribe_function_list: List[Callable] = []

        self.user_on_connect = user_on_connect
        self.user_on_disconnect = user_on_disconnect

        self.connected_event: Event = Event()
        self.disconnected_event: Event = Event()

        self.client: Client = Client(userdata=self)
        self.thread_pool = ThreadPoolExecutor()

        self.client.enable_logger(self.logger)
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.client.on_disconnect = on_disconnect

        self.subscribe_topic_to_json_wrapped_functions_map: Dict[str, Subscription] = {}
        self.handle_topic_to_function_map: Dict[str, Callable] = {}
        self.request_topic_to_responder_map: Dict[str, Callable] = {}

        self.unsub_lock: RLock = RLock()

        self.json_stringify: Callable = json_stringify

        self.certificate_id: str = ""
        self.host: str = ""
        self.port: int = 1883
        self.user_requested_close: bool = False

    def close(self):
        """
        Call all deferred cleanup functions.

        :return:
        """
        self.user_requested_close = True
        for cleanup in self.handler_unsubscribe_function_list:
            cleanup()
        self._end()
        self.thread_pool.shutdown()

    def connect(self, host: str = "localhost", port: int = 1883):
        """
        Connect to the host and port specified via mqtt.

        :param host: This is the hostname or configuration name to use
        :param port: This is the port to connect to if not determined by the configuration
        :return: None
        """
        self.host = host
        self.port = port
        self.user_requested_close = False

        if not self.connected_event.is_set():
            mgr = SslConfigManager()
            if mgr.has(host):
                self.logger.debug(f"Using SSL configuration {host}")
                conf = mgr.get(host)
                self.use_configuration(conf)
                self.client.connect(conf.host, conf.port)
            else:
                self.logger.debug(f"Connecting to {host}:{port}")
                self.client.connect(host, port)
            self.logger.debug("Waiting for connection to be confirmed...")
            self.client.loop_start()
            self.connected_event.wait(15.0)
            if not self.connected_event.is_set():
                raise Exception("Connect timed out after 15 seconds.")
            self.logger.debug("Connected.")

    def connect_async(self, host: str = "localhost", port: int = 1883):
        """
        Connect to the host and port specified via mqtt.

        In case the underlying session is disconnected without a user request,
        the host and port are preserved for reconnect attempts.

        :param host:
        :param port:
        :return: None
        """
        self.host = host
        self.port = port
        self.user_requested_close = False

        if not self.connected_event.is_set():
            mgr = SslConfigManager()
            if mgr.has(host):
                conf = mgr.get(host)
                self.use_configuration(conf)
                self.client.connect_async(conf.host, conf.port)
            else:
                self.client.connect_async(host, port)
            self.client.loop_start()

    def _end(self):
        """
        End the session.

        :return: None
        """
        if self.connected_event.is_set():
            self.client.loop_stop()
            self.client.disconnect()
            self.disconnected_event.wait(15.0)
            self.logger.debug("Disconnected")

    def subscribe(self, topic: str, callback: Callable, options: Optional[Dict] = None, overwrite=False):
        """
        Call a callback when a matching topic gets a message.

        :param options:
        :param overwrite: Set to True to force overwriting an existing subscription, otherwise this will raise a MultipleSubscriptionError
        :param topic:
        :param callback:
        :return: un-listen un-subscribe function
        """

        if options is None:
            options = {"qos": QOS_AT_LEAST_ONCE}

        self.logger.debug(f"Adding {topic} to the list of topics to subscribe to when we reconnect.")

        if not isinstance(callback, JsonUnwrapperAroundCallback):
            callback = get_json_unwrapped_callback(callback)

        sub = Subscription(topic, callback, options)

        with self.unsub_lock:
            prev_sub = self.subscribe_topic_to_json_wrapped_functions_map.get(topic, None)
            if not overwrite and prev_sub is not None:
                raise MultipleSubscriptionError(topic)

            self.subscribe_topic_to_json_wrapped_functions_map[topic] = sub

            if self.connected_event.is_set():
                self.client.message_callback_add(sub.topic, sub.callback)
                self.client.subscribe(sub.topic, qos=sub.options["qos"])
                self.logger.debug(f"Subscribed to topic {topic} with qos {options['qos']}")

        def undo_subscribe():
            """
            Unsubscribe and remove internal handler state.

            This is called during the close() call, to remove things like the message callbacks and handler functions.
            :return: None
            """
            with self.unsub_lock:  # threads might enter here simultaneously. Stop that.
                if topic in self.subscribe_topic_to_json_wrapped_functions_map.keys():
                    self.client.message_callback_remove(topic)
                    self.client.unsubscribe(topic)

                    del self.subscribe_topic_to_json_wrapped_functions_map[topic]
                    self.logger.debug(f"Unsubscribed from topic {topic}")

        return undo_subscribe

    def publish(self, topic: str, payload: Dict, options: Optional[Dict] = None):
        """
        Publish something to a topic.

        :param options: dict. key "qos" will be looked for.
        :param topic:
        :param payload: json serializable object
        :return:
        """
        self.logger.debug(f"publish on {topic}")
        if options is None:
            options = {"qos": QOS_AT_LEAST_ONCE}
        if "qos" not in options:
            options["qos"] = QOS_AT_LEAST_ONCE

        if isinstance(payload, MqttResponse):
            serialized = self.json_stringify(asdict(payload))
        elif isinstance(payload, MqttStatusException):
            serialized = self.json_stringify(payload)
        else:
            serialized = self.json_stringify(payload)

        self.logger.info(f"Publishing with qos {options['qos']} to topic {topic}: {serialized}")
        self.client.publish(topic, payload=serialized, qos=options["qos"])
        # note to self: do not block on publish state here - it blocks downstream actions

    def request(self, topic: str, payload: Optional[Dict] = None, options: Optional[Dict] = None):  # noqa: C901
        """
        Request a response to a specific payload.

        This is a synchronous call. A request will be sent to the topic <topic>/<uuid>,
        and will wait for a response on topic _responses/<topic>/<uuid> for up to the timeout (passed in via the
        options dict). Timeouts will return an error shaped dictionary, with keys 'status' and 'body'.

        :param topic:
        :param payload: dict, to be delivered as json
        :param options: dict with keys "qos" and "timeoutMs"
        :return:
        """
        # arg defaults take a lot of space!
        self.logger.debug(f"Forming a request on {topic}")
        payload = {} if payload is None else payload
        options = {"qos": QOS_AT_LEAST_ONCE, "timeoutMs": 5000} if options is None else options
        request_id = uuid4()
        timeout_ms = options["timeoutMs"] if "timeoutMs" in options else 5000
        if "qos" not in options:
            options["qos"] = QOS_AT_LEAST_ONCE

        request_topic = f"{topic}/{request_id}"
        response_topic = f"_response/{request_topic}"

        cleanup = None
        timer = None
        handled_event = Event()

        # initialized here for the closures below
        return_me = ReturnMe()

        def unsub_and_fail():
            """
            Unsubscribe, clean up, and return None.

            Closure around the return_me and handled_event variables to indicate completion and values.

            :return:
            """
            if cleanup is not None:
                cleanup()
            clear_timeout()
            self.logger.debug(f"Timed out the request on {request_topic} number {request_id}")
            return_me.value = {"status": 500, "body": {"error": "Timed out."}}
            handled_event.set()

        def clear_timeout():
            """
            If the timer is set, clear it.

            Closure around the timer object.
            :return: None
            """
            if hasattr(timer, "cancel"):
                timer.cancel()

        self.request_topic_to_responder_map[request_topic] = get_custom_request_responder(
            self.logger, clear_timeout, return_me, handled_event
        )
        cleanup = self.subscribe(response_topic, self.request_topic_to_responder_map[request_topic], options=options)

        timer = Timer((timeout_ms / 1000.0), unsub_and_fail)
        timer.start()
        self.logger.debug(f"Publishing request on {request_topic}")
        self.publish(request_topic, payload, options)
        handled_event.wait(timeout=(timeout_ms / 1000.0) + 1.0)
        clear_timeout()
        cleanup()
        return return_me.value

    def handle(self, topic: str, client_function: Callable, options: Optional[Dict] = None):  # noqa: C901
        """
        Handle "topic" events by running "handler". Results of "handler" are posted as a response.

        When messages one layer under "topic" are posted, run handler, and post the result to a response channel.
        Subscribe to topics one layer under "topic" with the new handler func.
        The handler func calls "handler" to get a result message and publishes the response on "responseTopic"

        :param topic:
        :param client_function:
        :return:
        """
        if options is None:
            options = {"qos": QOS_AT_LEAST_ONCE}
        if "qos" not in options:
            options["qos"] = QOS_AT_LEAST_ONCE

        self.logger.debug(f"Registering to handle {topic} messages")

        self.handle_topic_to_function_map[topic] = get_error_handler_for_client_callback(self, self.logger, topic, client_function)
        cleanup = self.subscribe(f"{topic}/+", self.handle_topic_to_function_map[topic], options)
        self.handler_unsubscribe_function_list.append(cleanup)

    def use_configuration(self, conf: "SslConfig"):
        """
        Configure the MQTT client object to use a named SSL configuration.

        This depends on the well-known paths and file names for our SSL Configuration objects,
        which the SSL Manager validates for us.

        :param conf:
        :return:
        """
        if not conf.exists():
            raise ValueError(f"There is no configuration named {conf.dir}")
        if not conf.iscomplete():
            raise ValueError(f"The configuration {conf.dir} is missing a required file.")

        self.client.tls_set(str(conf.rootcert), str(conf.certificate), str(conf.privatekey))
        with Path(conf.certificate_id).open("r") as openfile:
            self.certificate_id = openfile.read().strip()
