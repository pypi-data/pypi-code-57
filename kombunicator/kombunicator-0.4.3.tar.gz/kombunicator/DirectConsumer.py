
import uuid

from kombu import Queue
from strongtyping.strong_typing import match_typing

from kombunicator.BaseConsumer import BaseConsumer


class DirectConsumer(BaseConsumer):

    @match_typing
    def __init__(self, connection, binding_key: str = '', accept: list = ['json']):
        super().__init__()

        self.connection = connection
        self.accept = accept

        if binding_key == '':
            self.binding_key = uuid.uuid4().hex
        else:
            self.binding_key = binding_key

        self.queue = Queue(
            name=self.binding_key,
            auto_delete=True
        )
