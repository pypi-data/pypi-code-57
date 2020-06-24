# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin,unused-import
"""
Main interface for robomaker service client paginators.

Usage::

    ```python
    import boto3

    from mypy_boto3_robomaker import RoboMakerClient
    from mypy_boto3_robomaker.paginator import (
        ListDeploymentJobsPaginator,
        ListFleetsPaginator,
        ListRobotApplicationsPaginator,
        ListRobotsPaginator,
        ListSimulationApplicationsPaginator,
        ListSimulationJobBatchesPaginator,
        ListSimulationJobsPaginator,
    )

    client: RoboMakerClient = boto3.client("robomaker")

    list_deployment_jobs_paginator: ListDeploymentJobsPaginator = client.get_paginator("list_deployment_jobs")
    list_fleets_paginator: ListFleetsPaginator = client.get_paginator("list_fleets")
    list_robot_applications_paginator: ListRobotApplicationsPaginator = client.get_paginator("list_robot_applications")
    list_robots_paginator: ListRobotsPaginator = client.get_paginator("list_robots")
    list_simulation_applications_paginator: ListSimulationApplicationsPaginator = client.get_paginator("list_simulation_applications")
    list_simulation_job_batches_paginator: ListSimulationJobBatchesPaginator = client.get_paginator("list_simulation_job_batches")
    list_simulation_jobs_paginator: ListSimulationJobsPaginator = client.get_paginator("list_simulation_jobs")
    ```
"""
from typing import Iterator, List

from botocore.paginate import Paginator as Boto3Paginator

from mypy_boto3_robomaker.type_defs import (
    FilterTypeDef,
    ListDeploymentJobsResponseTypeDef,
    ListFleetsResponseTypeDef,
    ListRobotApplicationsResponseTypeDef,
    ListRobotsResponseTypeDef,
    ListSimulationApplicationsResponseTypeDef,
    ListSimulationJobBatchesResponseTypeDef,
    ListSimulationJobsResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "ListDeploymentJobsPaginator",
    "ListFleetsPaginator",
    "ListRobotApplicationsPaginator",
    "ListRobotsPaginator",
    "ListSimulationApplicationsPaginator",
    "ListSimulationJobBatchesPaginator",
    "ListSimulationJobsPaginator",
)


class ListDeploymentJobsPaginator(Boto3Paginator):
    """
    [Paginator.ListDeploymentJobs documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.10/reference/services/robomaker.html#RoboMaker.Paginator.ListDeploymentJobs)
    """

    def paginate(
        self, filters: List[FilterTypeDef] = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListDeploymentJobsResponseTypeDef]:
        """
        [ListDeploymentJobs.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.10/reference/services/robomaker.html#RoboMaker.Paginator.ListDeploymentJobs.paginate)
        """


class ListFleetsPaginator(Boto3Paginator):
    """
    [Paginator.ListFleets documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.10/reference/services/robomaker.html#RoboMaker.Paginator.ListFleets)
    """

    def paginate(
        self, filters: List[FilterTypeDef] = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListFleetsResponseTypeDef]:
        """
        [ListFleets.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.10/reference/services/robomaker.html#RoboMaker.Paginator.ListFleets.paginate)
        """


class ListRobotApplicationsPaginator(Boto3Paginator):
    """
    [Paginator.ListRobotApplications documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.10/reference/services/robomaker.html#RoboMaker.Paginator.ListRobotApplications)
    """

    def paginate(
        self,
        versionQualifier: str = None,
        filters: List[FilterTypeDef] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListRobotApplicationsResponseTypeDef]:
        """
        [ListRobotApplications.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.10/reference/services/robomaker.html#RoboMaker.Paginator.ListRobotApplications.paginate)
        """


class ListRobotsPaginator(Boto3Paginator):
    """
    [Paginator.ListRobots documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.10/reference/services/robomaker.html#RoboMaker.Paginator.ListRobots)
    """

    def paginate(
        self, filters: List[FilterTypeDef] = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListRobotsResponseTypeDef]:
        """
        [ListRobots.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.10/reference/services/robomaker.html#RoboMaker.Paginator.ListRobots.paginate)
        """


class ListSimulationApplicationsPaginator(Boto3Paginator):
    """
    [Paginator.ListSimulationApplications documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.10/reference/services/robomaker.html#RoboMaker.Paginator.ListSimulationApplications)
    """

    def paginate(
        self,
        versionQualifier: str = None,
        filters: List[FilterTypeDef] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListSimulationApplicationsResponseTypeDef]:
        """
        [ListSimulationApplications.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.10/reference/services/robomaker.html#RoboMaker.Paginator.ListSimulationApplications.paginate)
        """


class ListSimulationJobBatchesPaginator(Boto3Paginator):
    """
    [Paginator.ListSimulationJobBatches documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.10/reference/services/robomaker.html#RoboMaker.Paginator.ListSimulationJobBatches)
    """

    def paginate(
        self, filters: List[FilterTypeDef] = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListSimulationJobBatchesResponseTypeDef]:
        """
        [ListSimulationJobBatches.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.10/reference/services/robomaker.html#RoboMaker.Paginator.ListSimulationJobBatches.paginate)
        """


class ListSimulationJobsPaginator(Boto3Paginator):
    """
    [Paginator.ListSimulationJobs documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.10/reference/services/robomaker.html#RoboMaker.Paginator.ListSimulationJobs)
    """

    def paginate(
        self, filters: List[FilterTypeDef] = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListSimulationJobsResponseTypeDef]:
        """
        [ListSimulationJobs.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.10/reference/services/robomaker.html#RoboMaker.Paginator.ListSimulationJobs.paginate)
        """
