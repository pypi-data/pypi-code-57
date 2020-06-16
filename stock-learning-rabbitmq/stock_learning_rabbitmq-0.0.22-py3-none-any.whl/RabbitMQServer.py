import traceback
from ast import literal_eval
from json import dumps, loads
from threading import Thread

from pika import BlockingConnection, ConnectionParameters


class RabbitMQServer(object):
    def __init__(self, queue_name, rabbitmq_connection_string):
        self._queue_name = queue_name
        self._rabbit_connection_string = rabbitmq_connection_string
        self._message_handlers = {}
        self._heartbeat = True

    
    def register(self, primitive_handler):

        if not hasattr(primitive_handler, 'primitive_name'):
            raise Exception('Primitive Handler does not have the "primitive_handler" attribute')

        if not hasattr(primitive_handler, 'consume') or not callable(getattr(primitive_handler, 'consume')):
            raise Exception('Primitive Handler does not have the "consume" method')

        if primitive_handler.primitive_name in self._message_handlers:
            return False
        else:
            self._message_handlers[primitive_handler.primitive_name] = primitive_handler.consume
            return True
    

    def disable_heartbeat(self):
        self._heartbeat = False

    def start_listening(self):
        try:
            self._connection = BlockingConnection(ConnectionParameters(host=self._rabbit_connection_string, heartbeat=self._heartbeat))
            self._channel = self._connection.channel()
            self._channel.queue_declare(queue=self._queue_name)

            self._channel.basic_consume(
                queue=self._queue_name,
                on_message_callback=self._callback_method,
                auto_ack=True
            )

            self._channel.start_consuming()
        except KeyboardInterrupt as e:
            self._channel.stop_consuming()
            self._channel.close()
            self._connection.close()
            raise e

    def _callback_method(self, ch, method, properties, body):
        try:
            message = self._binary_to_dict(body)
            if not (('primitive' in message and 'content' in message) and (isinstance(message['primitive'], str) and isinstance(message['content'], dict))):
                raise Exception()
            print(f'Message being handled. {message}')
            self._handle_message(message)
        except Exception as e:
            print(f'Cannot handle message. {body} {e}')
            traceback.print_exc()

    def _binary_to_dict(self, binary_json):
        return loads(binary_json, encoding='utf-8')

    def _handle_message(self, message: dict):
        if self._message_handlers and message['primitive'] in self._message_handlers:
            self._message_handlers[message['primitive']](message['content'])
        else:
            print(f'No implementation for {message} found!')

    def send_message(self, queue, primitive, content):
        content = { 'primitive': primitive, 'content': content }
        print(f'Sending {content} to {queue}')
        self._channel.basic_publish(exchange='', routing_key=queue, body=dumps(content))
