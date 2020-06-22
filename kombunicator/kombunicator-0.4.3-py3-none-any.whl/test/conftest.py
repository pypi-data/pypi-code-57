import random
import string

import pytest

from kombunicator import MessageProducer

from test import broker_connection_parameter


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
