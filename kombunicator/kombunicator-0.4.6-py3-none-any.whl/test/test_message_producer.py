import json
import pathlib
import pytest
import time

import kombunicator
from kombunicator import ConsumerConfigurator

from test import get_random_string

msg_handler_result = {}


@pytest.mark.timeout(60)
def test_message_producer(tmpdir, base_test_consumer, producer):
    exchange_name = 'kombunicator_single_producer'
    binding_keys = ['bk_test_single_producer']

    # name of the result file
    tmp_file = pathlib.Path(f'{tmpdir}/test_single_consumer.tmp')

    # define a topic consumer
    class TestConsumer(base_test_consumer):

        @classmethod
        def message_handler(cls, payload, headers, properties):
            result = dict()
            result['processed'] = True
            result['payload'] = payload
            result['headers'] = headers
            with tmp_file.open('w') as fh:
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
    with tmp_file.open('r') as fh:
        received_message = json.loads(fh.read())

    assert test_message['message'] == received_message['payload']['message']
    assert test_headers['data'] == received_message['headers']['data']
    assert 'processed' in received_message

    kombunicator.shutdown_consumers()


@pytest.mark.timeout(60)
def test_message_producer_multi_binding_keys(base_test_consumer, producer):
    exchange_name = 'kombunicator_single_producer'
    sub_binding_keys = ['bk_test.num_5', 'bk_test.num_5.sub_1']
    range_keys = range(1, 5)
    binding_keys = list(f'bk_test_{i}' for i in range_keys)
    binding_keys.extend(sub_binding_keys)

    # define a topic consumer
    class TestConsumer(base_test_consumer):
        def configure(self):
            super().configure()
            self.binding_keys = binding_keys

        @classmethod
        def message_handler(cls, payload, headers, properties):
            result = dict()
            result['processed'] = True
            result['payload'] = payload
            result['headers'] = headers
            msg_handler_result[properties.get('correlation_id', headers['data'])] = result

    kombunicator.register_message_consumer(TestConsumer)
    messages, headers = [], []

    for binding_key in binding_keys:
        # produce messages to consumer
        test_message = {'message': get_random_string()}
        test_headers = {'data': get_random_string()}

        producer.publish(
            message=test_message,
            headers=test_headers,
            exchange=exchange_name,
            routing_key=binding_key,
            correlation_id=f'test_{binding_key}'
        )
        messages.append(test_message)
        headers.append(test_headers)

    # make sure to receive answer messages.
    time.sleep(0.1)
    kombunicator.shutdown_consumers()

    for i in range_keys:
        bk = f'test_bk_test_{i}'
        assert msg_handler_result[bk]['payload'] == messages[i - 1]
        assert msg_handler_result[bk]['headers'] == headers[i - 1]

    for index, key in enumerate(reversed(sub_binding_keys), start=1):
        assert msg_handler_result[f'test_{key}']['payload'] == messages[-index]
        assert msg_handler_result[f'test_{key}']['headers'] == headers[-index]
