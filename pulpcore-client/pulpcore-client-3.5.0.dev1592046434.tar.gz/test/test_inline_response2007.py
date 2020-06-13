# coding: utf-8

"""
    Pulp 3 API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: v3
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import pulpcore.client.pulpcore
from pulpcore.client.pulpcore.models.inline_response2007 import InlineResponse2007  # noqa: E501
from pulpcore.client.pulpcore.rest import ApiException

class TestInlineResponse2007(unittest.TestCase):
    """InlineResponse2007 unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test InlineResponse2007
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = pulpcore.client.pulpcore.models.inline_response2007.InlineResponse2007()  # noqa: E501
        if include_optional :
            return InlineResponse2007(
                count = 56, 
                next = '0', 
                previous = '0', 
                results = [
                    pulpcore.client.pulpcore.models.task_read.TaskRead(
                        pulp_href = '0', 
                        pulp_created = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        state = '0', 
                        name = '0', 
                        started_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        finished_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        error = {
                            'key' : None
                            }, 
                        worker = '0', 
                        parent_task = '0', 
                        child_tasks = [
                            '0'
                            ], 
                        task_group = '0', 
                        progress_reports = [
                            pulpcore.client.pulpcore.models.progress_report.ProgressReport(
                                message = '0', 
                                code = '0', 
                                state = '0', 
                                total = 56, 
                                done = 56, 
                                suffix = '0', )
                            ], 
                        created_resources = [
                            '0'
                            ], 
                        reserved_resources_record = [
                            pulpcore.client.pulpcore.models.reserved_resources.ReservedResources()
                            ], )
                    ]
            )
        else :
            return InlineResponse2007(
                count = 56,
                results = [
                    pulpcore.client.pulpcore.models.task_read.TaskRead(
                        pulp_href = '0', 
                        pulp_created = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        state = '0', 
                        name = '0', 
                        started_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        finished_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        error = {
                            'key' : None
                            }, 
                        worker = '0', 
                        parent_task = '0', 
                        child_tasks = [
                            '0'
                            ], 
                        task_group = '0', 
                        progress_reports = [
                            pulpcore.client.pulpcore.models.progress_report.ProgressReport(
                                message = '0', 
                                code = '0', 
                                state = '0', 
                                total = 56, 
                                done = 56, 
                                suffix = '0', )
                            ], 
                        created_resources = [
                            '0'
                            ], 
                        reserved_resources_record = [
                            pulpcore.client.pulpcore.models.reserved_resources.ReservedResources()
                            ], )
                    ],
        )

    def testInlineResponse2007(self):
        """Test InlineResponse2007"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
