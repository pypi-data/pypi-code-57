
import json
import pytest
import time
from datetime import datetime
from kombunicator import RPCClient

from test import get_random_string


@pytest.mark.timeout(60)
def test_rpc_with_default_processor(conn_param, tmpdir, rpc_key):
    f_name = f'{tmpdir}/rpc_file.json'

    def answer_processor(data):
        data['answer_received'] = str(datetime.now())
        with open(f_name, 'w') as fh:
            fh.write(json.dumps(data))

    rpc_client = RPCClient(
        connection_parameter=conn_param,
        request_key=rpc_key,
        default_callback=answer_processor
    )

    test_message = {
        'data': get_random_string(),
        'issued': str(datetime.now())
    }
    rpc_client.request(test_message)

    # wait for receptions
    time.sleep(2)

    with open(f_name) as fh:
        received_message = json.loads(fh.read())

    # assert test_arg == argument
    assert received_message['data'] == test_message['data']
    assert 'answer_received' in received_message
    assert 'processed' in received_message


class Test_rpc_with_default_processor_method():
    @pytest.fixture(autouse=True)
    def _conn_param(self, conn_param):
        self.conn_param = conn_param

    @pytest.fixture(autouse=True)
    def _f_name(self, tmpdir):
        self.f_name = f'{tmpdir}/rpc_file.json'

    @pytest.fixture(autouse=True)
    def _rpc_key(self, rpc_key):
        self.rpc_key = rpc_key

    def configure(self):
        self.rpc_client = RPCClient(
            connection_parameter=self.conn_param,
            request_key=self.rpc_key,
            default_callback=self.answer_processor
        )
        self.test_message = {
            'data': get_random_string(),
            'issued': str(datetime.now())
        }

    def answer_processor(self, data):
        data['answer_received'] = str(datetime.now())
        with open(self.f_name, 'w') as fh:
            fh.write(json.dumps(data))

    def test_with_callback_method(self):
        self.configure()
        self.rpc_client.request(self.test_message)
        time.sleep(2)
        with open(self.f_name) as fh:
            received_message = json.loads(fh.read())

        assert received_message['data'] == self.test_message['data']
        assert 'answer_received' in received_message
        assert 'processed' in received_message


@pytest.mark.timeout(60)
def test_rpc_with_dynamic_processor(conn_param, tmpdir, rpc_key):
    f_name = f'{tmpdir}/rpc_file.json'
    argument = get_random_string()

    rpc_client = RPCClient(
        connection_parameter=conn_param,
        request_key=rpc_key
    )

    test_data = {
        'data': get_random_string(),
        'issued': str(datetime.now())
    }

    # RPC client configuration
    def answer_processor(data, arg=''):
        data['arg'] = arg
        with open(f_name, 'w') as fp:
            fp.write(json.dumps(data))

    rpc_client.request(test_data, callback=answer_processor, arg=argument)

    # wait for receptions
    time.sleep(2)

    with open(f_name) as fp:
        received_message = json.loads(fp.read())

    assert received_message.get('arg', '') == argument
    assert received_message.get('data', '') == test_data['data']
    # from the RPC server
    assert 'processed' in received_message
    # from the answer processor
    assert 'arg' in received_message


@pytest.mark.timeout(60)
def test_rpc_with_headers(conn_param, tmpdir, rpc_key_headers):
    f_name = f'{tmpdir}/rpc_file.json'
    argument = get_random_string()

    rpc_client = RPCClient(
        connection_parameter=conn_param,
        request_key=rpc_key_headers
    )

    test_data = {
        'data': get_random_string(),
        'issued': str(datetime.now())
    }

    # RPC client configuration
    def answer_processor(data, arg=''):
        data['arg'] = arg
        with open(f_name, 'w') as fp:
            fp.write(json.dumps(data))

    headers = {"custom_header_key": "custom_header_value"}
    rpc_client.request(test_data, headers=headers, callback=answer_processor, arg=argument)

    # wait for receptions
    time.sleep(2)

    with open(f_name) as fp:
        received_message = json.loads(fp.read())

    assert received_message.get('arg', '') == argument
    assert received_message.get('data', '') == test_data['data']
    assert received_message.get('headers', '') == headers

    # from the RPC server
    assert 'processed' in received_message
    # from the answer processor
    assert 'arg' in received_message


@pytest.mark.timeout(60)
def test_rpc_headers_must_json_serializable(conn_param, tmpdir, rpc_key_headers):

    f_name = f'{tmpdir}/rpc_file.json'
    argument = get_random_string()

    rpc_client = RPCClient(
        connection_parameter=conn_param,
        request_key=rpc_key_headers
    )

    test_data = {
        'data': get_random_string(),
        'issued': str(datetime.now())
    }

    # RPC client configuration
    def answer_processor(data, arg=''):
        data['arg'] = arg
        with open(f_name, 'w') as fp:
            fp.write(json.dumps(data))

    from datetime import datetime as some_class
    for data in [some_class, b'custom_header_value', lambda x: x ** 2, answer_processor]:
        headers = {"custom_header_key": data}
        with pytest.raises(TypeError):
            rpc_client.request(test_data, headers=headers, callback=answer_processor, arg=argument)


@pytest.mark.timeout(200)
def test_rpc_multi_requests(conn_param, tmpdir, rpc_key):
    number_requests = 10

    rpc_client = RPCClient(
        connection_parameter=conn_param,
        request_key=rpc_key
    )

    toc = dict()
    for i in range(number_requests):
        toc[f'f_name_{i}'] = f'{tmpdir}/rpc_file_{i}.json'
        toc[f'data_{i}'] = get_random_string()
        toc[f'arg_{i}'] = get_random_string()

        def answer_processor(data, arg=''):
            data['arg'] = arg
            with open(toc[f'f_name_{i}'], 'w') as fp:
                fp.write(json.dumps(data))

        test_data = {
            'data': toc[f'data_{i}'],
            'issued': str(datetime.now())
        }

        rpc_client.request(test_data, callback=answer_processor, arg=toc[f'arg_{i}'])
        time.sleep(2)

    # now check the results
    for i in range(number_requests):
        with open(toc[f'f_name_{i}']) as fp:
            received_message = json.loads(fp.read())

        assert received_message.get('data', '') == toc[f'data_{i}']
        assert received_message.get('arg', '') == toc[f'arg_{i}']
        # from the RPC server
        assert 'processed' in received_message
