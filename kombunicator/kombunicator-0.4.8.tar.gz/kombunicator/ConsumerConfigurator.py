
import inspect
import json
from typing import List

from strongtyping.strong_typing import match_typing
from kombunicator.utils import getter_setter

NEEDED_PARAMS = ['_consumer_type', '_connection_parameter', '_exchange_name', '_binding_keys', '_q_unique', '_accept']


class ConsumerConfigurator:

    def __new__(cls, *args, **kwargs):
        if 'NotImplementedError' in inspect.getsource(cls.message_handler):
            raise NotImplementedError('message_handler: Must be overwritten by subclass.')
        return super(ConsumerConfigurator, cls).__new__(cls)

    def __init__(self):
        self.configure()
        self.__check_configure()

    def configure(self):
        """
        This method is called after object creation.
        The following members must be assigned:
        self.consumer_type
        self.connection_parameter
        self.exchange_name
        self.binding_keys
        self.q_unique
        self.accept
        """
        raise NotImplementedError('Must be overwritten by subclass.')

    def __check_configure(self):
        """
        check if really all needed params where overwritten in configure
        """
        if not all(hasattr(self, param) for param in NEEDED_PARAMS):
            raise NotImplementedError('Read docstring of configure method')

    @classmethod
    def message_handler(cls, payload, headers, properties):
        """
        The callback to be executed on a received message.
        This must be overwritten by subclass.
        """
        raise NotImplementedError('Must be overwritten by subclass.')

    @getter_setter
    @match_typing(excep_raise=TypeError)
    def consumer_type(self, _type: str = None):
        """
        Set name of the type from which the consumer should consume.
        """
        if _type is not None:
            self._consumer_type = _type
        return self._consumer_type

    @getter_setter
    @match_typing(excep_raise=TypeError)
    def connection_parameter(self, param: dict = None):
        """
        Set the parameters for establishing a connection
        to a RabbitMQ service.

        :type param: `dict`
        """
        if param is not None:
            self._connection_parameter = param
        return self._connection_parameter

    @getter_setter
    @match_typing(excep_raise=TypeError)
    def exchange_name(self, name: str = None):
        """
        Set name of the subscribed exchange.
        """
        if name is not None:
            if name.startswith("amq."):
                raise ValueError("Exchange names starting with 'amq.' not allowed.")
            self._exchange_name = name
        return self._exchange_name

    @getter_setter
    @match_typing(excep_raise=TypeError)
    def binding_keys(self, keys: List[str] = None):
        """
        Set binding keys for the subscribed topics.
        """
        if keys is not None:
            self._binding_keys = keys
        return self._binding_keys

    @getter_setter
    @match_typing(excep_raise=TypeError)
    def q_unique(self, value: str = None):
        """
        Set queue name addition to make a unique queue naming.
        Default is a UUID4 string.
        """
        if value is not None:
            self._q_unique = value
        return self._q_unique

    @getter_setter
    @match_typing(excep_raise=TypeError)
    def accept(self, value: List[str] = None):
        """
        List of accepted content_types.
        Default is ['json'] only.
        """
        if value is not None:
            self._accept = value
        return self._accept

    def __str__(self):
        result = [f"Connection Parameters:\n    {json.dumps(self.connection_parameter, indent=2)}\n",
                  f"Exchange Name:\n    {self.exchange_name}\n",
                  f"Binding Keys: \n    {self.binding_keys}\n",
                  f"Unique queue: \n    {self.q_unique}\n",
                  f"Accept: \n    {self.accept}\n",
                  f"Message Handler:\n{inspect.getsource(self.message_handler)}"]
        return "".join(result)

    def __repr__(self):
        return self.__str__()
