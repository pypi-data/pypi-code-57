import __main__
import os
from dataclasses import dataclass

import requests

ENV_ECS_CONTAINER_METADATA_URI = 'ECS_CONTAINER_METADATA_URI'

def isECS():
    return os.environ(ENV_ECS_CONTAINER_METADATA_URI, None) is not None

@dataclass
class ECSInfo:
    full_info: dict
    task_definition_family: str
    container_name: str
    task_id: str

def getInfoFromECS():
    res = requests.get(os.getenv('ECS_CONTAINER_METADATA_URI'))
    full_info = res.json()

    task_definition_family = full_info['Labels']['com.amazonaws.ecs.task-definition-family']
    container_name = full_info['Labels']['com.amazonaws.ecs.container-name']
    task_id = full_info['Labels']['com.amazonaws.ecs.task-arn'].split('/')[-1]

    return ECSInfo(
        full_info=full_info,
        task_definition_family=task_definition_family,
        container_name=container_name,
        task_id=task_id
    )

def getTaskMetadataFromECS(ecs_info):
    return dict(
        task_id=ecs_info.task_id,
        region=os.getenv('AWS_REGION', None),
        execution_env=os.getenv('AWS_EXECUTION_ENV', None),
        ecs_container_metadata=ecs_info.full_info
    )

def getTaskLogsFromECS(ecs_info):
    log_group_name = '/ecs/' + ecs_info.task_definition_family
    log_stream_name = 'ecs/' + ecs_info.container_name + '/' + ecs_info.task_id

    return {
        'type': 'aws_cloudwatch',
        'data': {
            'log_group_name': log_group_name,
            'log_stream_name': log_stream_name
        }
    }

def wrapMainFunction(dagger_api, func, task_name=None, task_run_id=None):
    if task_name is None:
        task_name = os.path.split(__main__.__file__)[-1]

    ecs_info = getInfoFromECS()
    task_metadata = getTaskMetadataFromECS(ecs_info)
    task_logs = getTaskLogsFromECS(ecs_info)

    if task_run_id is None:
        task_run_id = ecs_info.task_id

    def _wrapper(*args, **kwargs):
        task = None
        try:
            task_input = dict(
                args=args,
                kwargs=kwargs
            )

            task = dagger_api.createTask(
                task_name,
                task_run_id,
                task_input=task_input,
                task_metadata=task_metadata,
                task_logs=task_logs,
                task_system='aws_ecs'
            )
        except Exception as e:
            print('Failed to initialize dagger')
            print(e)

        try:
            task_output = func(*args, **kwargs)
            task.update(task_status='succeeded', task_output=task_output)
            return task_output
        except Exception as e:
            print('Task failed')
            print(e)
            if task is not None:
                task.update(task_status='failed', task_output=str(e))

    return _wrapper
