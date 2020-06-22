
import time
from datetime import datetime
from threading import Event
from test import broker_connection_parameter, celery_app

from kombunicator import RPCServer


data_processor_name = 'request_processor'
@celery_app.task(name=data_processor_name)
def process_request(data):
    data['processed'] = str(datetime.now())
    return data


data_processor_name_headers = 'request_processor_headers'
@celery_app.task(name=data_processor_name_headers)
def process_request_with_headers(data, headers):
    data['processed'] = str(datetime.now())
    data['headers'] = headers
    return data


if __name__ == '__main__':
    celery_app.finalize()

    server_one_ready = Event()
    server_one = RPCServer(
        connection_parameter=broker_connection_parameter,
        listening_key='rpc_server_key',
        celery_app=celery_app,
        processing_task_name=data_processor_name,
        ready=server_one_ready
    )

    server_two_ready = Event()
    server_two = RPCServer(
        connection_parameter=broker_connection_parameter,
        listening_key='rpc_server_key_headers',
        celery_app=celery_app,
        processing_task_name=data_processor_name_headers,
        ready=server_two_ready
    )
    server_one.start()
    server_one_ready.wait()

    server_two.start()
    server_two_ready.wait()

    while True:
        time.sleep(1)
