import os
import json

import requests

from dagger.logger import logger
from dagger.config import DAGGER_URL
from dagger.Task import TaskListener, Task

class _NoFailJSONEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            return json.JSONEncoder.default(self, o)
        except TypeError:
            return 'Dagger was unable to serialize this value (%s)' % (o)

class DaggerAPI(TaskListener):
    def __init__(self, api_token):
        self.api_token = api_token

    def createTask(self, task_name, task_run_id, initial_status='started', **update_kwargs):
        return Task(task_name, task_run_id, listener=self).update(task_status=initial_status, **update_kwargs)

    def registerTask(self, task):
        task.setListener(self)

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

        # dumps/loads to remove any unserializable things from the body
        body = json.loads(json.dumps(body, skipkeys=True, cls=_NoFailJSONEncoder))

        logger.debug('Dagger request')
        logger.debug(DAGGER_URL)
        logger.debug(body)

        response = requests.post(
            DAGGER_URL,
            json=body
        )

        logger.debug('Dagger response')
        logger.debug(response)
        logger.debug(response.content)

    def onTaskUpdate(self, task):
        self.sendTaskStatus(
            task
        )
