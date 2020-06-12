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
from iqs_client.api.demo_api import DemoApi  # noqa: E501
from iqs_client.rest import ApiException


class TestDemoApi(unittest.TestCase):
    """DemoApi unit test stubs"""

    def setUp(self):
        self.api = iqs_client.api.demo_api.DemoApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_delete_model_compartment_from_index(self):
        """Test case for delete_model_compartment_from_index

        Delete modelCompartment from selected indexes.  # noqa: E501
        """
        pass

    def test_get_repository_structure(self):
        """Test case for get_repository_structure

        Get repository structure separated by repository types  # noqa: E501
        """
        pass

    def test_list_indexed_model_compartments(self):
        """Test case for list_indexed_model_compartments

        List model compartment stored by the index  # noqa: E501
        """
        pass

    def test_repository_structure_compartment_details(self):
        """Test case for repository_structure_compartment_details

        Returns detailed information about the given model compartment.  # noqa: E501
        """
        pass

    def test_update_model_compartment_index(self):
        """Test case for update_model_compartment_index

        Store modelCompartment in selected indexes.  # noqa: E501
        """
        pass

    def test_update_repository_structure(self):
        """Test case for update_repository_structure

        Update complete repository structure  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
