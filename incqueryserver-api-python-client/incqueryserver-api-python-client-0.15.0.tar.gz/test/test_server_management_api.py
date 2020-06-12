# coding: utf-8

"""
    IncQuery Server Web API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    OpenAPI spec version: 0.15.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import iqs_client
from iqs_client.api.server_management_api import ServerManagementApi  # noqa: E501
from iqs_client.rest import ApiException


class TestServerManagementApi(unittest.TestCase):
    """ServerManagementApi unit test stubs"""

    def setUp(self):
        self.api = iqs_client.api.server_management_api.ServerManagementApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_get_server_info(self):
        """Test case for get_server_info

        Retrieve information related to the server, including configuration details and available features  # noqa: E501
        """
        pass

    def test_get_server_status(self):
        """Test case for get_server_status

        Retrieve status of the IncQuery Server  # noqa: E501
        """
        pass

    def test_get_server_tasks(self):
        """Test case for get_server_tasks

        Retrieve the list of tasks running currently on the server  # noqa: E501
        """
        pass

    def test_list_compartment_operation_states(self):
        """Test case for list_compartment_operation_states

        Retrieve the operation states currently running on a specific compartment  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
