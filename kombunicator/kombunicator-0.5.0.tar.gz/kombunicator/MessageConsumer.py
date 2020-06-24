
from threading import Thread
from types import FunctionType, MethodType

from kombu import Connection
from strongtyping.strong_typing import match_typing

from kombunicator.DirectConsumer import DirectConsumer
from kombunicator.TopicConsumer import TopicConsumer


class MessageConsumer(Thread):

    @match_typing
    def __init__(self, connection_parameter: dict = {}, consumer_type: str = 'direct', exchange_name='',
                 binding_keys: list = [], q_unique=None, accept: list = ['json'],
                 _thread_ready=None):
        super().__init__()
        self.daemon = True

        self.connection_parameter = connection_parameter
        self.consumer_type = consumer_type
        self.binding_keys = binding_keys
        self.accept = accept
        self._thread_ready = _thread_ready

        if self.consumer_type == 'topic':
            assert type(exchange_name) is str, f"'exchange_name' must be string"
            assert type(q_unique) is str, f"'q_unique' must be string"

        self.exchange_name = exchange_name
        self.q_unique = q_unique

    def register_message_handler(self, msg_handler):
        assert type(msg_handler) is FunctionType or MethodType, "'msg_handler' must be function or method"
        self.msg_handler = msg_handler

    def _create_consumer(self, connection):

        consumer_base_params = {
            'connection': connection,
            'accept': self.accept
        }

        if self.consumer_type == 'topic':
            self.consumer = TopicConsumer(
                exchange_name=self.exchange_name,
                binding_keys=self.binding_keys,
                q_unique=self.q_unique,
                **consumer_base_params
            )
            self.consumer.process_message = MethodType(self.msg_handler, TopicConsumer)

        elif self.consumer_type == 'direct':
            self.consumer = DirectConsumer(binding_key=self.binding_keys[0],
                                           **consumer_base_params)
            self.consumer.process_message = self.msg_handler

        else:
            raise ValueError("consumer_type must be either 'direct' or 'topic'")

        # set ready event of cnsumer is ready to accept messages
        def _on_consume_ready(connection, channel, consumers, th_ready=self._thread_ready):
            th_ready.set()

        self.consumer.on_consume_ready = _on_consume_ready

    def run(self):
        """
        Starts the RabbitMQ consumer. This call will be blocking.
        """
        with Connection(**self.connection_parameter) as conn:
            self._create_consumer(conn)
            self.consumer.run()

    def stop(self):
        """
        Causes the RabbitMQ consumer to stop consuming
        and return. After that, the thread can be joined.
        """
        self.consumer.should_stop = True
