from typing import Callable, Dict

from medusa_protocol.binary.BinaryRequest import BinaryRequest
from medusa_protocol.binary.BinaryResponse import BinaryResponse

from medusa_network.Exceptions import RouterException


class Router(object):
    """
    Router class for TCP and UDP server

    """
    _actions: Dict[str, Callable[[BinaryRequest], BinaryResponse]] = {}

    def add(self, action: str, callback: Callable[[BinaryRequest], BinaryResponse]) -> None:
        """
        Add a new Route
        The callback function must have as a parameter a @BinaryRequest and must return @BinaryResponse
        :param action: string
        :param callback: a callback function
        :return: None
        """
        if action not in self._actions:
            self._actions[action] = callback

    def get(self, action: str) -> Callable[[BinaryRequest], BinaryResponse]:
        """
        Method that return a callback function if the action exit or raise a @RouterException
        :param action:
        :return:
        """
        if action in self._actions:
            # the action exist
            return self._actions[action]
        raise RouterException("Invalid Action")
