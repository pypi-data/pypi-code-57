# Stdlib
import json
import logging

# Pypi: Pika
import pika

# Django
from django.conf import settings

# Project
from .config import get_config

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

job_methods = {}


class JobClient(object):
    def __init__(self):
        if settings.ENVIRONMENT != 'test':
            param = get_config()
            self.connection = pika.BlockingConnection(param)
            self.channel = self.connection.channel()

    def call(self, routing_key, body=None,
             exchange='default', exchange_type='direct'):
        if settings.ENVIRONMENT == 'test':
            return job_without_async(routing_key, body)

        self.channel.exchange_declare(
            exchange=exchange,
            exchange_type=exchange_type
        )

        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=json.dumps(body, default=str)
        )

    def __del__(self):
        if hasattr(self, 'channel'):
            self.channel.close()


class JobServer(object):
    job_methods = {}

    def __init__(self, channel, methods):
        self.channel = channel
        self.job_methods = methods

    def __del__(self):
        self.channel.close()

    def start(self):
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        queue_task = self.job_methods[method.routing_key]
        func = queue_task['func']
        kwargs = queue_task['kwargs']
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return func(json.loads(body), **kwargs)

    def job_register(self):
        for key in self.job_methods.keys():
            result = self.channel.queue_declare(queue=settings.APP_NAME)
            queue_name = result.method.queue

            queue_task = self.job_methods[key]

            self.channel.exchange_declare(
                exchange=queue_task['exchange'],
                exchange_type=queue_task['exchange_type']
            )

            self.channel.queue_bind(
                exchange=queue_task['exchange'],
                queue=queue_name,
                routing_key=queue_task['routing_key']
            )

            self.channel.basic_consume(
                queue=queue_name,
                on_message_callback=self.callback
            )


def job_without_async(routing_key, body):
    if job_methods.get(routing_key):
        func = job_methods[routing_key]['func']
        data = json.dumps(body)
        func(json.loads(data))


def job_tasks(routing_key, exchange='default', exchange_type='direct',
              **kwargs):
    def wrapper(func):
        data = {
            'func': func,
            'routing_key': routing_key,
            'exchange': exchange,
            'exchange_type': exchange_type,
            'kwargs': kwargs
        }

        job_methods[routing_key] = data

    return wrapper
