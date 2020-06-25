import json
import logging

from roboself.chat import Chat
from roboself.client import Client
from roboself.config import RawConfig
from roboself.graph import Graph, Node
from roboself.types import ActionContext

log = logging.getLogger(__name__)


class Runtime:
    """A local skill runtime that connects to a live assistant runtime.


    """
    def __init__(self, client: Client, raw_config: RawConfig):
        """ Ctor.

        :param client: A pre-configured client to use for the communication.
        :param raw_config: A raw skill configuration.
        """
        self.client = client
        self.raw_config = raw_config

        # Register our handler with the Client
        self.client.register_handler(self.handle_request)

        # initialize the chat
        self.chat = Chat(self.client)
        self.kb = Graph(self.client)

    def handle_request(self, request):
        """Handles an incoming request from the assistant runtime."""
        if request["path"] == "/action":
            data = request["data"]
            action_name = data["name"]
            parameters = data["parameters"]

            # TODO: improve this
            for action in self.raw_config.action_objects:
                if action.__name__ == action_name:
                    # Create the action context
                    ctx = ActionContext(chat=self.chat, kb=self.kb)

                    # We need to transform the graph nodes to actual instances
                    for k, v in parameters.items():
                        if isinstance(v, dict) and (v.get("_id") is not None or v.get("_ref") is not None):
                            parameters[k] = Node(self.kb, v)
                        elif isinstance(v, list) and len(v) > 0:
                            first = v[0]
                            if isinstance(first, dict) and \
                                    (first.get("_id") is not None or first.get("_ref") is not None):
                                parameters[k] = [Node(self.kb, x) for x in v]

                    return action(**{
                        **parameters,
                        "ctx": ctx
                    })

        # Whenever we receive a log from the assistant runtime
        if request["path"] == "/log":
            data = request["data"]
            print(data["text"])

    def connect(self):
        """Connects the skill to the runtime.

        Sends the raw config and waits for confirmation.
        """
        config_json = self.raw_config.to_json()

        log.debug(f"Sending raw config: {json.dumps(config_json, indent=2)}")
        res = self.client.request("/skill/connect", {
            "config": config_json,
            "client_key": self.client.client_key
        })

        if not res == {"status": "ok"}:
            log.error(f"Error connecting skill: {res}")
        else:
            log.info(f"Connection successful.")

    def train(self):
        res = self.client.request("/skill/train", {
            "client_key": self.client.client_key
        }, timeout=10 * 60)

        if not res == {"status": "ok"}:
            log.error(f"Error training model: {res}")
        else:
            log.info(f"Training successful.")
