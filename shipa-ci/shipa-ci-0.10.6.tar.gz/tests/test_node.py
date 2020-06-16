import unittest

from shipa.client.client import ShipaClient, ShipaException, CONST_TEST_TOKEN, CONST_TEST_SERVER
from shipa.client.http import MockResponse, MockClient


class ShipaNodeTestCase(unittest.TestCase):

    def test_node_add(self):
        try:
            response = MockResponse(code=201, text='{"status": "success", "repository_url": "repository_url"}')
            http = MockClient(response=response)
            client = ShipaClient(server=CONST_TEST_SERVER, client=http, token=CONST_TEST_TOKEN)
            client.node_add(pools=tuple('test-app'), address="http://localhost", iaas="dockermachine", driver="generic")

        except ShipaException as e:
            assert e is None, str(e)

    def test_node_add_failed(self):
        try:
            response = MockResponse(code=400, text='{"Message":"","Error":"Node address shouldn\'t repeat"}')
            http = MockClient(response=response)
            client = ShipaClient(server=CONST_TEST_SERVER, client=http, token=CONST_TEST_TOKEN)
            client.node_add(pools=tuple('test-app'))
            assert False, 'failed to add a node!'

        except ShipaException:
            pass
