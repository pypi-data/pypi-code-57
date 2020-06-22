
import json
import os
import pytest
import sys
import time

import kombunicator
from kombunicator import ConsumerConfigurator

from test import get_random_string


@pytest.mark.timeout(60)
def test_message_producer(tmpdir, conn_param, producer):
    exchange_name = 'kombunicator_single_producer'
    binding_keys = ['bk_test_single_producer']

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
            result = dict()
            result['processed'] = True
            result['payload'] = payload
            result['headers'] = headers
            with open(f_name, 'w') as fh:
                fh.write(json.dumps(result))

    kombunicator.register_message_consumer(TestConsumer)

    # produce messages to consumer
    test_message = dict(message=get_random_string())
    test_headers = dict(data=get_random_string())

    producer.publish(
        message=test_message,
        headers=test_headers,
        exchange=exchange_name,
        routing_key=binding_keys[0]
    )

    # make sure to receive answer messages.
    time.sleep(0.1)

    # load consumed content
    with open(f_name, 'r') as fh:
        received_message = json.loads(fh.read())

    assert test_message['message'] == received_message['payload']['message']
    assert test_headers['data'] == received_message['headers']['data']
    assert 'processed' in received_message

    kombunicator.shutdown_consumers()
