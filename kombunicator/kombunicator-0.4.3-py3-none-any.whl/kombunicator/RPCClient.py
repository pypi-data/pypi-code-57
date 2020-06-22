import json
import uuid
from threading import Event
from types import FunctionType

from kombu import Connection, Producer
from strongtyping.strong_typing import match_typing

from kombunicator.MessageConsumer import MessageConsumer


class RPCClient:

    @match_typing
    def __init__(self, connection_parameter: dict, request_key: str, default_callback: FunctionType = None):
        self.connection_parameter = connection_parameter
        self.request_key = request_key
        self.default_callback = default_callback

    @property
    def _unique_string(self):
        return str(uuid.uuid4().hex)

    @match_typing(excep_raise=TypeError)
    def request(self, message: dict, headers=None, **kwargs):
        """Requests data from a remote PRC server.

        Parameters
        ----------
        message : dict
            representation of data to be processed remotely
        headers: dict
            additional, optional headers set to the message
        kwargs : dict
            - Can have a 'callback' key with a callable attached.
              Then, the callable will be used as callback to process the
              answer received from the remote RPC server. Otherwise
              the default_callback defined in the __init__() method will
              be used.
            - all other KV pairs of kwargs will be passed
              to the callback as parameters.

        Raises
        ------
            ValueError
        """
        reply_callback = kwargs.pop('callback', self.default_callback)
        if not isinstance(reply_callback, FunctionType):
            raise ValueError('Callback must be a function type.')

        try:
            json.dumps(headers)
        except TypeError:
            raise TypeError('Headers is not JSON serializable')

        message_correlation_id = self._unique_string
        result_queue_name = self._unique_string
        _ready = Event()

        # create a threaded direct message consumer
        self.consumer_thread = MessageConsumer(
            connection_parameter=self.connection_parameter,
            consumer_type='direct',
            binding_keys=[result_queue_name],
            _thread_ready=_ready
        )

        def _callback(payload, headers, properties):
            if properties['correlation_id'] == message_correlation_id:
                reply_callback(payload, **kwargs)
                self.consumer_thread.stop()
            else:
                # TODO: report bad message routing and/or wrong correlation id
                pass

        self.consumer_thread.register_message_handler(_callback)
        self.consumer_thread.start()
        _ready.wait()

        with Connection(**self.connection_parameter) as connection:
            with Producer(connection) as producer:
                producer.publish(
                    body=message,
                    exchange='',
                    routing_key=self.request_key,
                    reply_to=result_queue_name,
                    correlation_id=message_correlation_id,
                    headers=headers
                )
