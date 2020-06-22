
import json
from datetime import datetime

from kombunicator import RPCClient

from test import broker_connection_parameter


def answer_processor(data, indent=2):
    print(json.dumps(data, indent=indent))


client = RPCClient(
    connection_parameter=broker_connection_parameter,
    request_key='rpc_server_key',
    default_callback=answer_processor
)


if __name__ == "__main__":
    data = {
        'some': 'values',
        'issued': str(datetime.now())
    }

    # request with default callback processor
    client.request(data)

    # request with a non default callback processor and an additional argument
    client.request(data, callback=answer_processor, indent=4)

    # request with headers set
    headers = {"custom_header_key": "custom_header_value"}
    client.request(data, headers)
