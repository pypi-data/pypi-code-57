# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin,unused-import
"""
Main interface for codebuild service client paginators.

Usage::

    ```python
    import boto3

    from mypy_boto3_codebuild import CodeBuildClient
    from mypy_boto3_codebuild.paginator import (
        DescribeTestCasesPaginator,
        ListBuildsPaginator,
        ListBuildsForProjectPaginator,
        ListProjectsPaginator,
        ListReportGroupsPaginator,
        ListReportsPaginator,
        ListReportsForReportGroupPaginator,
        ListSharedProjectsPaginator,
        ListSharedReportGroupsPaginator,
    )

    client: CodeBuildClient = boto3.client("codebuild")

    describe_test_cases_paginator: DescribeTestCasesPaginator = client.get_paginator("describe_test_cases")
    list_builds_paginator: ListBuildsPaginator = client.get_paginator("list_builds")
    list_builds_for_project_paginator: ListBuildsForProjectPaginator = client.get_paginator("list_builds_for_project")
    list_projects_paginator: ListProjectsPaginator = client.get_paginator("list_projects")
    list_report_groups_paginator: ListReportGroupsPaginator = client.get_paginator("list_report_groups")
    list_reports_paginator: ListReportsPaginator = client.get_paginator("list_reports")
    list_reports_for_report_group_paginator: ListReportsForReportGroupPaginator = client.get_paginator("list_reports_for_report_group")
    list_shared_projects_paginator: ListSharedProjectsPaginator = client.get_paginator("list_shared_projects")
    list_shared_report_groups_paginator: ListSharedReportGroupsPaginator = client.get_paginator("list_shared_report_groups")
    ```
"""
import sys
from typing import Iterator

from botocore.paginate import Paginator as Boto3Paginator

from mypy_boto3_codebuild.type_defs import (
    DescribeTestCasesOutputTypeDef,
    ListBuildsForProjectOutputTypeDef,
    ListBuildsOutputTypeDef,
    ListProjectsOutputTypeDef,
    ListReportGroupsOutputTypeDef,
    ListReportsForReportGroupOutputTypeDef,
    ListReportsOutputTypeDef,
    ListSharedProjectsOutputTypeDef,
    ListSharedReportGroupsOutputTypeDef,
    PaginatorConfigTypeDef,
    ReportFilterTypeDef,
    TestCaseFilterTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = (
    "DescribeTestCasesPaginator",
    "ListBuildsPaginator",
    "ListBuildsForProjectPaginator",
    "ListProjectsPaginator",
    "ListReportGroupsPaginator",
    "ListReportsPaginator",
    "ListReportsForReportGroupPaginator",
    "ListSharedProjectsPaginator",
    "ListSharedReportGroupsPaginator",
)


class DescribeTestCasesPaginator(Boto3Paginator):
    """
    [Paginator.DescribeTestCases documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.10/reference/services/codebuild.html#CodeBuild.Paginator.DescribeTestCases)
    """

    def paginate(
        self,
        reportArn: str,
        filter: TestCaseFilterTypeDef = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[DescribeTestCasesOutputTypeDef]:
        """
        [DescribeTestCases.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.10/reference/services/codebuild.html#CodeBuild.Paginator.DescribeTestCases.paginate)
        """


class ListBuildsPaginator(Boto3Paginator):
    """
    [Paginator.ListBuilds documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.10/reference/services/codebuild.html#CodeBuild.Paginator.ListBuilds)
    """

    def paginate(
        self,
        sortOrder: Literal["ASCENDING", "DESCENDING"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListBuildsOutputTypeDef]:
        """
        [ListBuilds.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.10/reference/services/codebuild.html#CodeBuild.Paginator.ListBuilds.paginate)
        """


class ListBuildsForProjectPaginator(Boto3Paginator):
    """
    [Paginator.ListBuildsForProject documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.10/reference/services/codebuild.html#CodeBuild.Paginator.ListBuildsForProject)
    """

    def paginate(
        self,
        projectName: str,
        sortOrder: Literal["ASCENDING", "DESCENDING"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListBuildsForProjectOutputTypeDef]:
        """
        [ListBuildsForProject.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.10/reference/services/codebuild.html#CodeBuild.Paginator.ListBuildsForProject.paginate)
        """


class ListProjectsPaginator(Boto3Paginator):
    """
    [Paginator.ListProjects documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.10/reference/services/codebuild.html#CodeBuild.Paginator.ListProjects)
    """

    def paginate(
        self,
        sortBy: Literal["NAME", "CREATED_TIME", "LAST_MODIFIED_TIME"] = None,
        sortOrder: Literal["ASCENDING", "DESCENDING"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListProjectsOutputTypeDef]:
        """
        [ListProjects.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.10/reference/services/codebuild.html#CodeBuild.Paginator.ListProjects.paginate)
        """


class ListReportGroupsPaginator(Boto3Paginator):
    """
    [Paginator.ListReportGroups documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.10/reference/services/codebuild.html#CodeBuild.Paginator.ListReportGroups)
    """

    def paginate(
        self,
        sortOrder: Literal["ASCENDING", "DESCENDING"] = None,
        sortBy: Literal["NAME", "CREATED_TIME", "LAST_MODIFIED_TIME"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListReportGroupsOutputTypeDef]:
        """
        [ListReportGroups.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.10/reference/services/codebuild.html#CodeBuild.Paginator.ListReportGroups.paginate)
        """


class ListReportsPaginator(Boto3Paginator):
    """
    [Paginator.ListReports documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.10/reference/services/codebuild.html#CodeBuild.Paginator.ListReports)
    """

    def paginate(
        self,
        sortOrder: Literal["ASCENDING", "DESCENDING"] = None,
        filter: ReportFilterTypeDef = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListReportsOutputTypeDef]:
        """
        [ListReports.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.10/reference/services/codebuild.html#CodeBuild.Paginator.ListReports.paginate)
        """


class ListReportsForReportGroupPaginator(Boto3Paginator):
    """
    [Paginator.ListReportsForReportGroup documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.10/reference/services/codebuild.html#CodeBuild.Paginator.ListReportsForReportGroup)
    """

    def paginate(
        self,
        reportGroupArn: str,
        sortOrder: Literal["ASCENDING", "DESCENDING"] = None,
        filter: ReportFilterTypeDef = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListReportsForReportGroupOutputTypeDef]:
        """
        [ListReportsForReportGroup.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.10/reference/services/codebuild.html#CodeBuild.Paginator.ListReportsForReportGroup.paginate)
        """


class ListSharedProjectsPaginator(Boto3Paginator):
    """
    [Paginator.ListSharedProjects documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.10/reference/services/codebuild.html#CodeBuild.Paginator.ListSharedProjects)
    """

    def paginate(
        self,
        sortBy: Literal["ARN", "MODIFIED_TIME"] = None,
        sortOrder: Literal["ASCENDING", "DESCENDING"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListSharedProjectsOutputTypeDef]:
        """
        [ListSharedProjects.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.10/reference/services/codebuild.html#CodeBuild.Paginator.ListSharedProjects.paginate)
        """


class ListSharedReportGroupsPaginator(Boto3Paginator):
    """
    [Paginator.ListSharedReportGroups documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.10/reference/services/codebuild.html#CodeBuild.Paginator.ListSharedReportGroups)
    """

    def paginate(
        self,
        sortOrder: Literal["ASCENDING", "DESCENDING"] = None,
        sortBy: Literal["ARN", "MODIFIED_TIME"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListSharedReportGroupsOutputTypeDef]:
        """
        [ListSharedReportGroups.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.10/reference/services/codebuild.html#CodeBuild.Paginator.ListSharedReportGroups.paginate)
        """
