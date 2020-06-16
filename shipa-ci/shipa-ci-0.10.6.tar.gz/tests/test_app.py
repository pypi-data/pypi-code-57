import unittest

from shipa.client.client import ShipaClient, ShipaException, CONST_TEST_TOKEN, CONST_TEST_SERVER
from shipa.client.http import MockResponse, MockClient


class ShipaAppTestCase(unittest.TestCase):

    def test_app_create(self):
        try:
            response = MockResponse(code=201, text='{"status": "success", "repository_url": "repository_url"}')
            http = MockClient(response=response)
            client = ShipaClient(server=CONST_TEST_SERVER, client=http, token=CONST_TEST_TOKEN)
            client.app_create(appname='test-app', pool="test", team="admin", platform="python")

        except ShipaException as e:
            assert e is None, str(e)

    def test_app_create_failed_with_error_code(self):
        try:
            response = MockResponse(code=400, text='{"status": "success", "repository_url": "repository_url"}')
            http = MockClient(response=response)
            client = ShipaClient(server=CONST_TEST_SERVER, client=http, token=CONST_TEST_TOKEN)
            client.app_create(appname='test-app', pool="test", team="admin", platform="python")
            assert False, 'failed to create a app!'

        except ShipaException:
            pass

    def test_app_create_failed_with_error_status(self):
        try:
            response = MockResponse(code=201, text='{"status": "failed", "repository_url": "repository_url"}')
            http = MockClient(response=response)
            client = ShipaClient(server=CONST_TEST_SERVER, client=http, token=CONST_TEST_TOKEN)
            client.app_create(appname='test-app', pool="test", team="admin", platform="python")
            assert False, 'failed to create a app!'

        except ShipaException:
            pass

    def test_app_remove(self):
        try:
            response = MockResponse(code=200, text='{"Message": "removed a shipa app"}')
            http = MockClient(response=response)
            client = ShipaClient(server=CONST_TEST_SERVER, client=http, token=CONST_TEST_TOKEN)
            client.app_remove(appname='test-app')

        except ShipaException as e:
            assert e is None, str(e)

    def test_app_remove_failed(self):
        try:
            response = MockResponse(code=400, text='{"Message": "failed to remove a shipa app"}')
            http = MockClient(response=response)
            client = ShipaClient(server=CONST_TEST_SERVER, client=http, token=CONST_TEST_TOKEN)
            client.app_remove(appname='test-app')
            assert False, 'failed to remove a app!'

        except ShipaException:
            pass

    def test_app_deploy(self):
        try:
            response = MockResponse(code=200, text="deployed a app\n OK\n")
            http = MockClient(response=response)
            client = ShipaClient(server=CONST_TEST_SERVER, client=http, token=CONST_TEST_TOKEN)
            client.app_deploy(appname='test-app')

        except ShipaException as e:
            assert e is None, str(e)

    def test_app_deploy_failed(self):
        try:
            response = MockResponse(code=200, text="deployed a app\n FAIL\n")
            http = MockClient(response=response)
            client = ShipaClient(server=CONST_TEST_SERVER, client=http, token=CONST_TEST_TOKEN)
            client.app_deploy(appname='test-app')
            assert False, 'failed to deploy a app!'

        except ShipaException:
            pass

    def test_app_deploy_failed_without_response_text(self):
        try:
            response = MockResponse(code=200)
            http = MockClient(response=response)
            client = ShipaClient(server=CONST_TEST_SERVER, client=http, token=CONST_TEST_TOKEN)
            client.app_deploy(appname='test-app')
            assert False, 'failed to deploy a app!'

        except ShipaException:
            pass

    def test_app_move(self):
        try:
            response = MockResponse(code=200, text="moved a app\n OK\n")
            http = MockClient(response=response)
            client = ShipaClient(server=CONST_TEST_SERVER, client=http, token=CONST_TEST_TOKEN)
            client.app_move(appname='test-app', pool='test-pool')

        except ShipaException as e:
            assert e is None, str(e)

    def test_app_move_failed(self):
        try:
            response = MockResponse(code=200, text="moved a app\n FAIL\n")
            http = MockClient(response=response)
            client = ShipaClient(server=CONST_TEST_SERVER, client=http, token=CONST_TEST_TOKEN)
            client.app_move(appname='test-app', pool='test-pool')
            assert False, 'failed to move a app!'

        except ShipaException:
            pass

    def test_app_move_failed_without_response_text(self):
        try:
            response = MockResponse(code=200)
            http = MockClient(response=response)
            client = ShipaClient(server=CONST_TEST_SERVER, client=http, token=CONST_TEST_TOKEN)
            client.app_move(appname='test-app', pool='test-pool')
            assert False, 'failed to move a app!'

        except ShipaException:
            pass
