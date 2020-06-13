import os
import sys
from unittest import TestCase
from unittest.mock import patch, MagicMock

from dagger import DaggerAPI, initDagger, initLambda
from dagger.constants import DAGGER_URL

@patch('dagger.DaggerAPI.requests')
class DaggerTestCase(TestCase):
    def tearDown(self):
        if 'AWS_REGION' in os.environ:
            del os.environ['AWS_REGION']
        if '_HANDLER' in os.environ:
            del os.environ['_HANDLER']

    @patch('dagger.DaggerAPI')
    def test_initDagger_lambda(self, mock_api, requests):
        os.environ['_HANDLER'] = 'test'

        mock_bootstrap = MagicMock()
        sys.modules['bootstrap'] = mock_bootstrap

        mock_event = MagicMock()
        mock_context = MagicMock()

        def _handle_event_request(lambda_runtime_client, request_handler, *args, **kwargs):
            request_handler(mock_event, mock_context)
        mock_bootstrap.handle_event_request = _handle_event_request

        initDagger('testkey')

        mock_api.assert_called_once()

        mock_request_handler = MagicMock()
        mock_bootstrap.handle_event_request(MagicMock(), mock_request_handler)

        mock_request_handler.assert_called_once_with(mock_event, mock_context)

        assert len(mock_api.return_value.createTask.mock_calls) == 2
        assert len(mock_api.return_value.createTask.return_value.update.mock_calls) == 1
