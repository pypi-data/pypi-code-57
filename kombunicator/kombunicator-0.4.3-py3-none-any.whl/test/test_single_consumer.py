
import json
import pytest
import time

import kombunicator
from kombunicator import ConsumerConfigurator

from test import get_random_string


def test_consumer_class_fails_not_implemented():

    class TestConsumer(ConsumerConfigurator):
        pass

    with pytest.raises(NotImplementedError):
        TestConsumer()


def test_consumer_class_fails_not_implemented_message_handler():

    class TestConsumer(ConsumerConfigurator):

        def configure(self):
            self.exchange_name = 'exchange_name'
            self.connection_parameter = {}
            self.binding_keys = ['_key1', '_key2']
            self.consumer_type = 'topic'
            self.q_unique = get_random_string()
            self.accept = ['json']

    with pytest.raises(NotImplementedError):
        TestConsumer()


def test_consumer_class_fails_not_all_members():
    class TestConsumer(ConsumerConfigurator):

        def configure(self):
            """
            exchange_name is missing
            """
            self.connection_parameter = {}
            self.binding_keys = ['_key1', '_key2']
            self.consumer_type = 'topic'
            self.q_unique = get_random_string()
            self.accept = ['json']

        @classmethod
        def message_handler(cls, payload, headers, properties):
            pass

    with pytest.raises(NotImplementedError):
        TestConsumer()


def test_consumer_class_fails_not_correct_type():
    class TestConsumer(ConsumerConfigurator):

        def configure(self):
            """
            consumer_type must be str
            """
            self.exchange_name = 'exchange_name'
            self.connection_parameter = {}
            self.binding_keys = ['_key1', '_key2']
            self.consumer_type = ['topic', 'topic2']
            self.q_unique = get_random_string()
            self.accept = ['json']

        @classmethod
        def message_handler(cls, payload, headers, properties):
            pass

    with pytest.raises(TypeError):
        TestConsumer()


@pytest.mark.timeout(60)
def test_single_consumer(tmpdir, conn_param, producer):
    exchange_name = 'kombunicator_single_consumer'
    binding_keys = ['bk_test_single_consumer']

    # name of the result file
    f_name = f'{tmpdir}/test_single_consumer.tmp'

    # define a topic consumer
    class TestConsumer(ConsumerConfigurator):
        def configure(self):
            self.connection_parameter = conn_param
            self.exchange_name = exchange_name
            self.binding_keys = binding_keys
            self.consumer_type = 'topic'
            self.q_unique = get_random_string()
            self.accept = ['json']

        @classmethod
        def message_handler(cls, payload, headers, properties):
            payload['processed'] = True
            with open(f_name, 'w') as fh:
                fh.write(json.dumps(payload))

    kombunicator.register_message_consumer(TestConsumer)

    # produce messages to consumer
    test_message = dict(message=get_random_string())
    producer.publish(
        message=test_message,
        exchange=exchange_name,
        routing_key=binding_keys[0]
    )

    # make sure to receive message.
    time.sleep(0.2)

    # load consumed content
    with open(f_name, 'r') as fh:
        received_message = json.loads(fh.read())

    assert test_message['message'] == received_message['message']
    assert 'processed' in received_message

    kombunicator.shutdown_consumers()
