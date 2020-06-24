import logging
from datetime import datetime as dt
from typing import Any

from kombu.message import MessageStateError
from kombu.mixins import ConsumerMixin
from kombu.transport.pyamqp import Message


class BaseConsumer(ConsumerMixin):

    def __init__(self):
        self._add_handler_to_logger()
        super().__init__()

    def get_consumers(self, Consumer, channel):
        consumers = list()
        consumer = Consumer(queues=self.queue,
                            accept=self.accept,
                            callbacks=[self._handle_message])
        consumers.append(consumer)
        return consumers

    def _handle_message(self, body, message: Message):
        cid = message.properties.get('correlation_id', 'unknown')
        try:
            # Acknowledge this message as being processed.
            message.ack()
        except MessageStateError:  # If the message has already been acknowledged/requeued/rejected.
            self.__create_log_msg__(True, cid, message, body)
        else:
            self.process_message(message.payload, message.headers, message.properties)

    def process_message(self, payload, headers, properties):
        """
        Must be overwritten by subclass.
        """
        raise NotImplementedError('Subclass responsibility.')

    def _add_handler_to_logger(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
        fh = logging.FileHandler(f'/tmp/{self.__class__.__name__}.log')
        fh.setLevel(logging.INFO)
        self.logger.addHandler(fh)

    def __create_log_msg__(self, error: bool, cid: str, message: Message, body: Any = None):
        msg = '\n\t'.join([f'{k}: {v}' for k, v in message.payload.items()])
        msg += '\n\t'.join([f'{k}: {v}' for k, v in message.headers.items()])
        msg += '\n\t'.join([f'{k}: {v}' for k, v in message.properties.items()])
        if body is not None:
            msg += '\n\t'.join([f'{k}: {v}' for k, v in body.items()])

        log_time = dt.utcnow().replace(microsecond=0)
        if error:
            self.logger.info(f'{log_time}: Message {cid} has already been processed, rejected or requeued.')
        else:
            self.logger.info(f'{log_time}: Message with cid="{cid}" will be processed: \n\t {msg}')
