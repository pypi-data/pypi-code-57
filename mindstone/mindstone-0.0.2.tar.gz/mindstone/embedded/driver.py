""" driver module.

"""

import json
import time

from mindstone.connection import tcp_serve
from mindstone.embedded.coordinator import Coordinator
from mindstone.embedded.platforms import get_current_platform
from mindstone.embedded.reporting import \
    get_reported_errors, get_reported_messages, clear_reported_messages, \
    clear_reported_errors, report_error, display

FALLBACK_PORT = 5000
FALLBACK_HOSTNAME = ""


class Driver(object):
    """ driver class.

    The driver acts an interface between the controller and the platform.
    With the help of a coordinator, it interfaces with components and communicates
    their states back to the controller.
    """

    coordinator = Coordinator()

    @staticmethod
    def new_channel(channel_id: int, channel_type: str, **parameters):
        """ register new channel with the current operating platform. """
        get_current_platform().new_channel(channel_id, channel_type, **parameters)

    @staticmethod
    def decode_received_data(data: bytes) -> dict:
        return json.loads(data.decode("utf-8"))

    @staticmethod
    def encode_feedback_data(data: dict) -> bytes:
        return bytes(json.dumps(data).encode("utf-8"))

    @staticmethod
    def end():
        get_current_platform().cleanup()

    def on_receive(self, received_data: bytes) -> bytes:
        decoded_received_data = self.decode_received_data(received_data)
        message_type = decoded_received_data["type"]
        message_data = dict(**decoded_received_data["data"])

        feedback = {
            "output": None
        }

        # handle the received message
        display("Receiving new communication from control.")
        try:
            if message_type == "config":
                display("\tReceived new configuration.")
                self.coordinator.update(message_data)
                # get feedback observations after the new configuration
                # has been implemented.
                feedback["output"] = self.coordinator.observations()

            elif message_type == "boot":
                display("\tReceived new boot data.")
                for component_name, value in message_data.items():
                    component_type, kwargs = tuple(value)
                    self.coordinator.add_component(component_name, component_type, **kwargs)
                    display("\t\t Added new component '{}': {}".format(component_name, component_type))
                feedback["output"] = self.coordinator.properties()

            elif message_type == "end":
                self.end()
                display("\tDriver ended.")

            else:
                raise RuntimeError("Message type ({}) is invalid.".format(message_type))
        except Exception as e:
            report_error("{}: {}".format(e.__class__.__name__, str(e)))
        feedback.update({
            "messages": get_reported_messages(),
            "errors": get_reported_errors(),
            "timestamp": int(time.time())
        })
        clear_reported_errors()
        clear_reported_messages()

        return self.encode_feedback_data(feedback)

    def start(self, hostname: str = FALLBACK_HOSTNAME, port: int = FALLBACK_PORT, persist: bool = True):
        tcp_serve(hostname, port, on_receive=self.on_receive, on_close=self.end, persist=persist)
