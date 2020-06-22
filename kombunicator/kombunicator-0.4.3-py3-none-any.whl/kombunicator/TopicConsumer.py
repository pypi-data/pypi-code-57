
import uuid

from kombu import Exchange, Queue, binding

from kombunicator.BaseConsumer import BaseConsumer


class TopicConsumer(BaseConsumer):

    def __init__(self, connection, exchange_name: str, binding_keys: list, accept: list = ['json'], q_unique=None):
        super().__init__()
        self.connection = connection
        self.exchange_name = exchange_name
        self.binding_keys = binding_keys
        self.accept = accept
        self.q_unique = q_unique

        self.exchange = Exchange(self.exchange_name, type='topic')
        self.q_bindings = [binding(self.exchange, routing_key=key) for key in self.binding_keys]

        if self.q_unique is None:
            self.q_unique = uuid.uuid4().hex
        q_name = f"{exchange_name}:{'|'.join([str(key) for key in binding_keys])}:{q_unique}"
        if len(q_name) > 255:
            raise ValueError("Queue name too long. Maximal 255 characters allowed")

        self.queue = Queue(
            name=q_name,
            exchange=self.exchange,
            bindings=self.q_bindings,
            auto_delete=True,
            expires=2 * 30 * 24 * 60 * 60
        )
