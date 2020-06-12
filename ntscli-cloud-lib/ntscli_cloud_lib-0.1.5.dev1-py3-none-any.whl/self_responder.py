#  Copyright (c) 2020 Netflix.
#  All rights reserved.
import uuid
from threading import Event

from kaiju_mqtt_py import KaijuMqtt
from kaiju_mqtt_py import MqttPacket

# Implementation libs
from ntscli_cloud_lib.log import logger
from ntscli_cloud_lib.session import IOT_BASE_PATTERN

PING_REQUEST = {"status": 200, "self_test": True}


def responder(topic: str, msg: MqttPacket, *args, **kwargs):
    """Respond to self-ping formatted messages by returning an object."""
    logger.debug("User responder called")
    response = True
    if {"request": "something"} != msg.payload:
        response = False
    return {"status": 200, "body": {"response": response}}


class SelfResponder:
    """
    Connection checking through pub/sub.

    Can I subscribe and publish messages on a remote cloud broker, with no external services?
    """

    def __init__(self):
        """Constructor."""
        self.happened = Event()
        self.kaiju = KaijuMqtt()
        self.topic = ""

    def start(self, configuration_name):
        """Start a unique handler for this client connection."""
        logger.debug(f"SelfResponder connecting to broker {configuration_name}")
        self.kaiju.connect(configuration_name)
        self.topic = IOT_BASE_PATTERN.format(self.kaiju.certificate_id) + "/client_self_responder/" + str(uuid.uuid4())
        logger.debug(f"SelfResponder registering to handle topic: {self.topic}")
        self.kaiju.handle(self.topic, responder)

    def check_request(self):
        """
        Send a request to the remote broker, and check that we sent it.

        If the response is not sent back to us, we will typically get a timeout message,
        which will fail these assert checks.
        """
        logger.debug("SelfResponder requesting a response")
        response = self.kaiju.request(self.topic, {"request": "something"})
        logger.debug(f"SelfResponder response: {response}")
        if "status" not in response or 200 != response["status"] or "body" not in response:
            raise ValueError("The response did not have the expected format.")

    def stop(self):
        """Tear down our handler."""
        self.kaiju.close()
