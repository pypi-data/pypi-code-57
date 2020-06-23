import random
import string

import pytest
from kombunicator import ConsumerConfigurator
from kombunicator import MessageProducer

from test import broker_connection_parameter
from test import get_random_string


@pytest.fixture
def conn_param():
    return broker_connection_parameter


@pytest.fixture
def producer(conn_param):
    return MessageProducer(conn_param)


@pytest.fixture
def random_string(length=10):
    """Generate a random string of fixed length """
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))


@pytest.fixture
def rpc_key():
    return 'rpc_server_key'


@pytest.fixture
def rpc_key_headers():
    return 'rpc_server_key_headers'


@pytest.fixture
def base_test_consumer(conn_param):
    exchange_name = 'kombunicator_single_producer'
    binding_keys = ['bk_test_single_producer']

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
            pass

    return TestConsumer
