# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin,too-many-locals,unused-import
"""
Main interface for codeguruprofiler service client

Usage::

    ```python
    import boto3
    from mypy_boto3_codeguruprofiler import CodeGuruProfilerClient

    client: CodeGuruProfilerClient = boto3.client("codeguruprofiler")
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Type, Union

from botocore.exceptions import ClientError as Boto3ClientError

from mypy_boto3_codeguruprofiler.paginator import ListProfileTimesPaginator
from mypy_boto3_codeguruprofiler.type_defs import (
    AgentOrchestrationConfigTypeDef,
    ConfigureAgentResponseTypeDef,
    CreateProfilingGroupResponseTypeDef,
    DescribeProfilingGroupResponseTypeDef,
    GetPolicyResponseTypeDef,
    GetProfileResponseTypeDef,
    ListProfileTimesResponseTypeDef,
    ListProfilingGroupsResponseTypeDef,
    PutPermissionResponseTypeDef,
    RemovePermissionResponseTypeDef,
    UpdateProfilingGroupResponseTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("CodeGuruProfilerClient",)


class Exceptions:
    ClientError: Type[Boto3ClientError]
    ConflictException: Type[Boto3ClientError]
    InternalServerException: Type[Boto3ClientError]
    ResourceNotFoundException: Type[Boto3ClientError]
    ServiceQuotaExceededException: Type[Boto3ClientError]
    ThrottlingException: Type[Boto3ClientError]
    ValidationException: Type[Boto3ClientError]


class CodeGuruProfilerClient:
    """
    [CodeGuruProfiler.Client documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.10/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client)
    """

    exceptions: Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Client.can_paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.10/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.can_paginate)
        """

    def configure_agent(
        self, profilingGroupName: str, fleetInstanceId: str = None
    ) -> ConfigureAgentResponseTypeDef:
        """
        [Client.configure_agent documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.10/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.configure_agent)
        """

    def create_profiling_group(
        self,
        clientToken: str,
        profilingGroupName: str,
        agentOrchestrationConfig: "AgentOrchestrationConfigTypeDef" = None,
    ) -> CreateProfilingGroupResponseTypeDef:
        """
        [Client.create_profiling_group documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.10/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.create_profiling_group)
        """

    def delete_profiling_group(self, profilingGroupName: str) -> Dict[str, Any]:
        """
        [Client.delete_profiling_group documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.10/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.delete_profiling_group)
        """

    def describe_profiling_group(
        self, profilingGroupName: str
    ) -> DescribeProfilingGroupResponseTypeDef:
        """
        [Client.describe_profiling_group documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.10/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.describe_profiling_group)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Client.generate_presigned_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.10/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.generate_presigned_url)
        """

    def get_policy(self, profilingGroupName: str) -> GetPolicyResponseTypeDef:
        """
        [Client.get_policy documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.10/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.get_policy)
        """

    def get_profile(
        self,
        profilingGroupName: str,
        accept: str = None,
        endTime: datetime = None,
        maxDepth: int = None,
        period: str = None,
        startTime: datetime = None,
    ) -> GetProfileResponseTypeDef:
        """
        [Client.get_profile documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.10/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.get_profile)
        """

    def list_profile_times(
        self,
        endTime: datetime,
        period: Literal["P1D", "PT1H", "PT5M"],
        profilingGroupName: str,
        startTime: datetime,
        maxResults: int = None,
        nextToken: str = None,
        orderBy: Literal["TimestampAscending", "TimestampDescending"] = None,
    ) -> ListProfileTimesResponseTypeDef:
        """
        [Client.list_profile_times documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.10/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.list_profile_times)
        """

    def list_profiling_groups(
        self, includeDescription: bool = None, maxResults: int = None, nextToken: str = None
    ) -> ListProfilingGroupsResponseTypeDef:
        """
        [Client.list_profiling_groups documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.10/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.list_profiling_groups)
        """

    def post_agent_profile(
        self,
        agentProfile: Union[bytes, IO[bytes]],
        contentType: str,
        profilingGroupName: str,
        profileToken: str = None,
    ) -> Dict[str, Any]:
        """
        [Client.post_agent_profile documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.10/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.post_agent_profile)
        """

    def put_permission(
        self,
        actionGroup: Literal["agentPermissions"],
        principals: List[str],
        profilingGroupName: str,
        revisionId: str = None,
    ) -> PutPermissionResponseTypeDef:
        """
        [Client.put_permission documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.10/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.put_permission)
        """

    def remove_permission(
        self, actionGroup: Literal["agentPermissions"], profilingGroupName: str, revisionId: str
    ) -> RemovePermissionResponseTypeDef:
        """
        [Client.remove_permission documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.10/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.remove_permission)
        """

    def update_profiling_group(
        self, agentOrchestrationConfig: "AgentOrchestrationConfigTypeDef", profilingGroupName: str
    ) -> UpdateProfilingGroupResponseTypeDef:
        """
        [Client.update_profiling_group documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.10/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.update_profiling_group)
        """

    def get_paginator(
        self, operation_name: Literal["list_profile_times"]
    ) -> ListProfileTimesPaginator:
        """
        [Paginator.ListProfileTimes documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.10/reference/services/codeguruprofiler.html#CodeGuruProfiler.Paginator.ListProfileTimes)
        """
