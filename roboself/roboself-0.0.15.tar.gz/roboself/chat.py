import logging

from roboself.client import Client

log = logging.getLogger(__name__)


class Chat:
    """Chat implementation on top of a RPC Client"""
    def __init__(self, client: Client):
        self.client = client

    def utter(self, utterance, **params):
        """Utters a message."""

        self.client.request("/chat/utter", {
            "utterance": utterance,
            "params": params
        })

    def ask(self, utterance, **params):
        """Asks the user a message."""

        return self.client.request("/chat/ask", {
            "utterance": utterance,
            "params": params
        })
