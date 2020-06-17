import json
from datetime import timedelta
from typing import Dict, Any, Optional, Union

import backoff
from arcane.core.exceptions import GOOGLE_EXCEPTIONS_TO_RETRY
from google.cloud.tasks_v2 import CloudTasksClient
from google.protobuf import duration_pb2
from google.oauth2 import service_account


class Client(CloudTasksClient):
    def __init__(self, adscale_key,project=None):
        self.project = project
        self.credentials = service_account.Credentials.from_service_account_file(adscale_key)
        self.adscale_key = adscale_key
        super().__init__(credentials=self.credentials)
    
    @backoff.on_exception(backoff.expo, GOOGLE_EXCEPTIONS_TO_RETRY, max_tries=5)
    def publish_task(self,
                    queue: str,
                    method: str="POST",
                    queue_region: str="europe-west1",
                    url: str=None,
                    max_response_time: Optional[timedelta]=None, # if rounded to the closest second. If not precised, use cloud task default value
                    task_name: str=None,
                    body: Optional[Union[Dict[str, Any], str, int]]=None,
                    raw_body: Optional[bytes] = None) -> None:
        _task_queue = self.queue_path(project=self.project, location=queue_region, queue=queue)
        with open(self.adscale_key) as _credentials_file:
            _credentials = json.load(_credentials_file)
        _client_email = _credentials['client_email']
        http_request = dict(http_method=method,
                            url=url,
                            headers={'Content-Type': "application/json"},
                            oidc_token={'service_account_email': _client_email}
                            )
        if body is not None:
            if raw_body is not None:
                raise ValueError("either body or raw_body should be specified, not both at ")

            http_request.update(body=json.dumps(body).encode('utf-8'))
        elif raw_body is not None:
            http_request.update(body=raw_body)

        task = dict(http_request=http_request)
        if max_response_time is not None:
            task.update(dispatch_deadline=duration_pb2.Duration(seconds=max_response_time.seconds))
        if task_name:
            task.update(name=self.task_path(self.project, queue_region, queue, task_name))
        created_task = self.create_task(_task_queue,task)
        print(f'Queuing task:{created_task}')
