
import json
import pytest
import random

import kombunicator
from kombunicator import ConsumerConfigurator

from test import get_random_string


# run multiple consumer threads
@pytest.mark.timeout(60)
def test_multi_consumer_setup(tmpdir, conn_param, producer):
    accept = ['json']

    number_of_consumers = random.randint(5, 20)
    number_of_error_consumers = random.randint(10, 30)

    # fire up some topic consumers
    for n in range(number_of_consumers):
        exchange_name = f'test_exchange_name_{n}'
        binding_keys = [f'test_key_{n}']
        f_name = f'{tmpdir}/test_kombunicator_{n}.tmp'

        class TConsumer(ConsumerConfigurator):
            def configure(self):
                self.connection_parameter = conn_param
                self.exchange_name = exchange_name
                self.consumer_type = 'topic'
                self.binding_keys = binding_keys
                self.q_unique = get_random_string()
                self.accept = accept

            @classmethod
            def message_handler(cls, payload, headers, properties):
                fn = payload.get('f_name', f'{tmpdir}/test_kombunicator_default_{n}.tmp')
                payload['processed'] = True
                with open(fn, 'w') as fh:
                    fh.write(json.dumps(payload))

        kombunicator.register_message_consumer(TConsumer)

        # produce messages to consumer
        test_message = dict(message=get_random_string(), f_name=f_name)
        producer.publish(
            message=test_message,
            exchange=exchange_name,
            routing_key=binding_keys[0]
        )

    for n in range(number_of_error_consumers):
        exchange_name = f'test_error_exchange_name_{n}'
        binding_keys = [f'test_error_key_{n}']

        class TConsumerError(ConsumerConfigurator):
            def configure(self):
                self.connection_parameter = conn_param
                self.exchange_name = exchange_name
                self.consumer_type = 'topic'
                self.binding_keys = binding_keys
                self.q_unique = get_random_string()
                self.accept = accept

            @classmethod
            def message_handler(cls, payload, headers, properties):
                fn = payload.get('f_name', f'{tmpdir}/test_kombunicator_default_{n}.tmp')
                payload['malformed'] = True
                with open(fn, 'w') as fh:
                    # explicitly dump malformed data into result file
                    fh.write(json.dumps({"message": "Wrong Handler"}))

        kombunicator.register_message_consumer(TConsumerError)

    for n in range(number_of_consumers):
        # load consumed content
        with open(f_name, 'r') as fh:
            received_message = json.loads(fh.read())

        assert test_message['message'] == received_message['message']
        assert 'processed' in received_message
        assert 'malformed' not in received_message

    kombunicator.shutdown_consumers()
