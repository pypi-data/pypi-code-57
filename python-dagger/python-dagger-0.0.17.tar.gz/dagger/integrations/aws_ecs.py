import __main__
import os
from dataclasses import dataclass

import requests

from dagger.Task import Task
from dagger.integrations.base import Integration

ENV_ECS_CONTAINER_METADATA_URI = 'ECS_CONTAINER_METADATA_URI'

class AWSECSIntegration(Integration):
    def isInIntegration(self):
        return os.getenv(ENV_ECS_CONTAINER_METADATA_URI, None) is not None

    @dataclass
    class ECSInfo:
        full_info: dict
        task_definition_family: str
        container_name: str
        task_id: str

    @classmethod
    def getInfoFromECS(cls):
        res = requests.get(os.getenv('ECS_CONTAINER_METADATA_URI'))
        full_info = res.json()

        task_definition_family = full_info['Labels']['com.amazonaws.ecs.task-definition-family']
        container_name = full_info['Labels']['com.amazonaws.ecs.container-name']
        task_id = full_info['Labels']['com.amazonaws.ecs.task-arn'].split('/')[-1]

        return cls.ECSInfo(
            full_info=full_info,
            task_definition_family=task_definition_family,
            container_name=container_name,
            task_id=task_id
        )

    @classmethod
    def getTaskMetadataFromECS(cls, ecs_info):
        return dict(
            task_id=ecs_info.task_id,
            region=os.getenv('AWS_REGION', None),
            execution_env=os.getenv('AWS_EXECUTION_ENV', None),
            ecs_container_metadata=ecs_info.full_info
        )

    @classmethod
    def getTaskLogsFromECS(cls, ecs_info):
        log_group_name = '/ecs/' + ecs_info.task_definition_family
        log_stream_name = 'ecs/' + ecs_info.container_name + '/' + ecs_info.task_id

        return {
            'type': 'aws_cloudwatch',
            'data': {
                'log_group_name': log_group_name,
                'log_stream_name': log_stream_name
            }
        }

    def getStaticTask(self, task_name=None, task_run_id=None, **task_kwargs):
        if task_name is None:
            task_name = os.path.split(__main__.__file__)[-1]

        ecs_info = self.getInfoFromECS()
        task_metadata = self.getTaskMetadataFromECS(ecs_info)
        task_logs = self.getTaskLogsFromECS(ecs_info)

        if task_run_id is None:
            task_run_id = ecs_info.task_id

        task = Task(
            task_name,
            task_run_id,
        )

        task.update(
            task_metadata=task_metadata,
            task_logs=task_logs,
            task_system='aws_ecs',
            **task_kwargs
        )

        return task
