import logging
from typing import Any

from roboself.client import Client

log = logging.getLogger(__name__)


class Chat:
    """A chat interface connected to a running assistant.

    The chat interface allows you to send a message back to the user or ask a question
    and wait for the response.
    """
    def __init__(self, client: Client):
        """ Constructor.

        :param client: The RoboSelf client to use for the connection to the runtime.
        """
        self.client = client

    def utter(self, utterance: str, **params):
        """ Utters a message to the user.

        Example:

        .. code-block::

           chat.utter("say_hi", name="John")

        :param utterance: The name of pre-registered utterance or a text message.
        :param params: A dict with parameters used inside the utterance.
        """

        self.client.request("/chat/utter", {
            "utterance": utterance,
            "params": params
        })

    def ask(self, utterance: str, **params) -> Any:
        """ Asks the user a question and waits for the response.

        Example:

        .. code-block::

           name = chat.ask("question_what_is_your_name")


        :param utterance: The name of pre-registered utterance or a text message.
        :param params: A dict with parameters used inside the utterance.
        :return: The value entered by the user.
        """

        return self.client.request("/chat/ask", {
            "utterance": utterance,
            "params": params
        })
