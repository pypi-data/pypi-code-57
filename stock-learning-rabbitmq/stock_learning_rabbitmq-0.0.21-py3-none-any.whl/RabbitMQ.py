from ast import literal_eval
from json import dumps, loads
from threading import Thread
from pika import BlockingConnection, ConnectionParameters


class RabbitMQ(object):
    def __init__(self, queue_name, rabbitmq_connection_string):
        self.queue_name = queue_name
        self.rabbit_connection_string = rabbitmq_connection_string
        self.message_handlers = {}

        self.connection = BlockingConnection(ConnectionParameters(self.rabbit_connection_string))
        self._channel = self.connection.channel()
        self._channel.queue_declare(queue=self.queue_name)

        self._channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self.callback_method,
            auto_ack=True
        )

    def callback_method(self, ch, method, properties, body):
        try:
            message = self._binary_to_dict(body)
            if not (('primitive' in message and 'content' in message) and (isinstance(message['primitive'], str) and isinstance(message['content'], dict))):
                raise Exception()
            print(f'Message being handled. {message}')
            self._handle_message(message)
        except Exception as e:
            print(f'Cannot handle message. {message} {e}')
            raise e

    def _handle_message(self, message: dict):
        if self.message_handlers and message['primitive'] in self.message_handlers:
            self.message_handlers[message['primitive']](message['content'])
        else:
            print(f'No implementation for {message} found!')

    def _binary_to_dict(self, binary_json):
        return literal_eval(binary_json.decode('utf-8'))

    def start_listening(self):
        self._channel.start_consuming()

    def stop_listening(self):
        self._channel.stop_consuming()

    def register(self, primitive_handler):

        if not hasattr(primitive_handler, 'primitive_name'):
            raise Exception('Primitive Handler does not have the "primitive_handler" attribute')

        if not hasattr(primitive_handler, 'consume') or not callable(getattr(primitive_handler, 'consume')):
            raise Exception('Primitive Handler does not have the "consume" method')

        if primitive_handler.primitive_name in self.message_handlers:
            return False
        else:
            self.message_handlers[primitive_handler.primitive_name] = primitive_handler.consume
            return True
    
    def send_message(self, queue, primitive, content):
        content = { 'primitive': primitive, 'content': content }
        print(f'Sending {content} to {queue}')
        self._channel.basic_publish(exchange='', routing_key=queue, body=dumps(content))
