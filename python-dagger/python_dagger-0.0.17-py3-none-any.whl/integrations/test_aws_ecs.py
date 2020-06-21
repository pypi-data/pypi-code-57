import os
import unittest
from unittest.mock import patch, MagicMock, call

from dagger import wrap

TEST_EXECUTION_ENV = {
    'DockerId': 'docker-id',
    'Name': 'container-name', 
    'DockerName': 'docker-name', 
    'Image': 'docker-image', 
    'ImageID': 'image-id', 
    'Labels': {
        'com.amazonaws.ecs.cluster': 'test-cluster', 
        'com.amazonaws.ecs.container-name': 'test-container-name', 
        'com.amazonaws.ecs.task-arn': 'arn:aws:ecs:us-west-2:123412341234:task/3c319a48-91d2-4ec5-9973-123412341234',
        'com.amazonaws.ecs.task-definition-family': 'test-task-definition-family', 
        'com.amazonaws.ecs.task-definition-version': 'test-task-definition-version'
    },
    'DesiredStatus': 'RUNNING', 
    'KnownStatus': 'RUNNING', 
    'Limits': {'CPU': 0, 'Memory': 2048}, 
    'CreatedAt': '2020-06-07T16:07:45.321115096Z', 
    'StartedAt': '2020-06-07T16:08:10.522444681Z', 
    'Type': 'NORMAL', 
    'Networks': [{'NetworkMode': 'awsvpc', 'IPv4Addresses': ['10.0.21.154']}]
}

def mock_requests(url):
    mock_response = MagicMock()
    mock_response.json.return_value = TEST_EXECUTION_ENV
    return mock_response

@patch('dagger.integrations.aws_ecs.requests.get', side_effect=mock_requests)
class TestAWSECSIntegration(unittest.TestCase):
    def tearDown(self):
        remove_env_variables = ['AWS_REGION', 'ECS_CONTAINER_METADATA_URI']
        for env_variable_name in remove_env_variables:
            if env_variable_name in os.environ:
                del os.environ[env_variable_name]

    @patch('dagger.integrations.aws_ecs.__main__')
    @patch('dagger.integrations.aws_ecs.Task')
    def test_wrapFunction(self, mock_task, mock_main, mock_request_get):
        mock_main.__file__ = 'something/something/test.py'

        mock_dagger_api = MagicMock()
        mock_main_func = MagicMock()

        wrapped_func = wrap(mock_dagger_api, mock_main_func, integration='aws_ecs')

        mock_input = MagicMock()
        wrapped_func(mock_input, asdf=mock_input)

        mock_main_func.assert_called_with(mock_input, asdf=mock_input)

        mock_task.assert_called_with(
            'test.py',
            '3c319a48-91d2-4ec5-9973-123412341234'
        )

        print(mock_task.return_value.update.mock_calls)

        assert mock_task.return_value.update.mock_calls[0] == call(
            task_logs={
                'type': 'aws_cloudwatch', 
                'data': {'log_group_name': '/ecs/test-task-definition-family', 'log_stream_name': 'ecs/test-container-name/3c319a48-91d2-4ec5-9973-123412341234'}
            }, 
            task_metadata={'task_id': '3c319a48-91d2-4ec5-9973-123412341234', 'region': None, 'execution_env': None, 'ecs_container_metadata': {'DockerId': 'docker-id', 'Name': 'container-name', 'DockerName': 'docker-name', 'Image': 'docker-image', 'ImageID': 'image-id', 'Labels': {'com.amazonaws.ecs.cluster': 'test-cluster', 'com.amazonaws.ecs.container-name': 'test-container-name', 'com.amazonaws.ecs.task-arn': 'arn:aws:ecs:us-west-2:123412341234:task/3c319a48-91d2-4ec5-9973-123412341234', 'com.amazonaws.ecs.task-definition-family': 'test-task-definition-family', 'com.amazonaws.ecs.task-definition-version': 'test-task-definition-version'}, 'DesiredStatus': 'RUNNING', 'KnownStatus': 'RUNNING', 'Limits': {'CPU': 0, 'Memory': 2048}, 'CreatedAt': '2020-06-07T16:07:45.321115096Z', 'StartedAt': '2020-06-07T16:08:10.522444681Z', 'Type': 'NORMAL', 'Networks': [{'NetworkMode': 'awsvpc', 'IPv4Addresses': ['10.0.21.154']}]}}, 
            task_system='aws_ecs'
        )

    @patch('dagger.integrations.aws_ecs.__main__')
    @patch('dagger.integrations.aws_ecs.Task')
    def test_wrapFunction_random_additional_key(self, mock_task, mock_main, mock_request_get):
        mock_main.__file__ = 'something/something/test.py'

        mock_dagger_api = MagicMock()
        mock_main_func = MagicMock()

        wrapped_func = wrap(mock_dagger_api, mock_main_func, integration='aws_ecs', random_other_key='asdf')

        mock_input = MagicMock()
        wrapped_func(mock_input, asdf=mock_input)

        mock_main_func.assert_called_with(mock_input, asdf=mock_input)

        mock_task.assert_called_with(
            'test.py',
            '3c319a48-91d2-4ec5-9973-123412341234'
        )

        print(mock_task.return_value.update.mock_calls)

        assert mock_task.return_value.update.mock_calls[0] == call(
            random_other_key='asdf',
            task_logs={
                'type': 'aws_cloudwatch', 
                'data': {'log_group_name': '/ecs/test-task-definition-family', 'log_stream_name': 'ecs/test-container-name/3c319a48-91d2-4ec5-9973-123412341234'}
            }, 
            task_metadata={'task_id': '3c319a48-91d2-4ec5-9973-123412341234', 'region': None, 'execution_env': None, 'ecs_container_metadata': {'DockerId': 'docker-id', 'Name': 'container-name', 'DockerName': 'docker-name', 'Image': 'docker-image', 'ImageID': 'image-id', 'Labels': {'com.amazonaws.ecs.cluster': 'test-cluster', 'com.amazonaws.ecs.container-name': 'test-container-name', 'com.amazonaws.ecs.task-arn': 'arn:aws:ecs:us-west-2:123412341234:task/3c319a48-91d2-4ec5-9973-123412341234', 'com.amazonaws.ecs.task-definition-family': 'test-task-definition-family', 'com.amazonaws.ecs.task-definition-version': 'test-task-definition-version'}, 'DesiredStatus': 'RUNNING', 'KnownStatus': 'RUNNING', 'Limits': {'CPU': 0, 'Memory': 2048}, 'CreatedAt': '2020-06-07T16:07:45.321115096Z', 'StartedAt': '2020-06-07T16:08:10.522444681Z', 'Type': 'NORMAL', 'Networks': [{'NetworkMode': 'awsvpc', 'IPv4Addresses': ['10.0.21.154']}]}}, 
            task_system='aws_ecs'
        )
