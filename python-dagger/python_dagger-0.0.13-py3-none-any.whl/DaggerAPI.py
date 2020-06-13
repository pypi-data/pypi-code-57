import os

import requests

from dagger.constants import DAGGER_URL
from dagger.Task import TaskListener, Task

class DaggerAPI(TaskListener):
    def __init__(self, api_token, verbose=True):
        self.api_token = api_token
        self.verbose = verbose

    def createTask(self, task_name, task_run_id, initial_status='started', **update_kwargs):
        return Task(self, task_name, task_run_id).update(task_status=initial_status, **update_kwargs)

    # def sendTaskStatus(self, status, task_name, task_run_id, task_input, task_output, task_metadata, task_logs):
    def sendTaskStatus(self, task):
        body = dict(
            status=task.task_status,
            task_name=task.task_name,
            id=task.task_run_id,
            input=dict(input=task.task_input),
            output=dict(output=task.task_output),
            logs=task.task_logs,
            metadata=task.task_metadata,
            language=task.task_language,
            system=task.task_system,
            api_token=self.api_token
        )

        if self.verbose:
            print('Dagger request')
            print(DAGGER_URL, body)

        response = requests.post(
            DAGGER_URL,
            json=body
        )

        if self.verbose:
            print('Dagger response')
            print(response)
            print(response.content)

    def onTaskUpdate(self, task):
        self.sendTaskStatus(
            task
        )
