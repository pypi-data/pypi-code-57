from .. client_utils import FirestoreClient
import json

DOWNLOAD = 'download'
UPDATE_ITEM = 'updateItem'
PROCESS_UPLOAD = 'processUpload'

def send_task(queue_name, handler, payload, svc_acct_email, useFunction=False):
    '''
    Expectation is that the payload will be a dict... we'll dump that to json, then encode
    '''
    clt = FirestoreClient.getInstance()
    task = {}
    
    if useFunction:
        task['http_request'] = {
            'url': handler,
            'oidc_token': {
               'service_account_email': svc_acct_email,
            },
           'headers': {
               'Content-Type': 'application/json',
           }
        }
        if payload is not None:
            converted_payload = payload.encode()
            task['http_request']['body'] = converted_payload
            task['http_request']['http_method'] = 'POST'
        else:
            task['http_request']['http_method'] = 'GET'
    else:
        task['app_engine_http_request'] = {
            'relative_uri': handler,
            'oidc_token': {
               'service_account_email': svc_acct_email,
            }
        }
        if payload is not None:
            converted_payload = payload.encode()
            task['app_engine_http_request']['body'] = converted_payload
            task['app_engine_http_request']['http_method'] = 'POST'
        else:
            task['app_engine_http_request']['http_method'] = 'GET'


    path = clt.task_queues.get(queue_name,None)
    if path is None:
        raise Exception("Invalid Queue Name")

    response = clt.tasksClient.create_task(path, task)
    print('Created task {}'.format(response.name))
    return response