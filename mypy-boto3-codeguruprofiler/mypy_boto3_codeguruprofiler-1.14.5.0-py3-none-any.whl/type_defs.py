"""
Main interface for codeguruprofiler service type definitions.

Usage::

    ```python
    from mypy_boto3_codeguruprofiler.type_defs import AgentConfigurationTypeDef

    data: AgentConfigurationTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import List

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AgentConfigurationTypeDef",
    "AgentOrchestrationConfigTypeDef",
    "AggregatedProfileTimeTypeDef",
    "ProfileTimeTypeDef",
    "ProfilingGroupDescriptionTypeDef",
    "ProfilingStatusTypeDef",
    "ConfigureAgentResponseTypeDef",
    "CreateProfilingGroupResponseTypeDef",
    "DescribeProfilingGroupResponseTypeDef",
    "GetPolicyResponseTypeDef",
    "GetProfileResponseTypeDef",
    "ListProfileTimesResponseTypeDef",
    "ListProfilingGroupsResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PutPermissionResponseTypeDef",
    "RemovePermissionResponseTypeDef",
    "UpdateProfilingGroupResponseTypeDef",
)

AgentConfigurationTypeDef = TypedDict(
    "AgentConfigurationTypeDef", {"periodInSeconds": int, "shouldProfile": bool}
)

AgentOrchestrationConfigTypeDef = TypedDict(
    "AgentOrchestrationConfigTypeDef", {"profilingEnabled": bool}
)

AggregatedProfileTimeTypeDef = TypedDict(
    "AggregatedProfileTimeTypeDef",
    {"period": Literal["P1D", "PT1H", "PT5M"], "start": datetime},
    total=False,
)

ProfileTimeTypeDef = TypedDict("ProfileTimeTypeDef", {"start": datetime}, total=False)

ProfilingGroupDescriptionTypeDef = TypedDict(
    "ProfilingGroupDescriptionTypeDef",
    {
        "agentOrchestrationConfig": "AgentOrchestrationConfigTypeDef",
        "arn": str,
        "createdAt": datetime,
        "name": str,
        "profilingStatus": "ProfilingStatusTypeDef",
        "updatedAt": datetime,
    },
    total=False,
)

ProfilingStatusTypeDef = TypedDict(
    "ProfilingStatusTypeDef",
    {
        "latestAgentOrchestratedAt": datetime,
        "latestAgentProfileReportedAt": datetime,
        "latestAggregatedProfile": "AggregatedProfileTimeTypeDef",
    },
    total=False,
)

ConfigureAgentResponseTypeDef = TypedDict(
    "ConfigureAgentResponseTypeDef", {"configuration": "AgentConfigurationTypeDef"}
)

CreateProfilingGroupResponseTypeDef = TypedDict(
    "CreateProfilingGroupResponseTypeDef", {"profilingGroup": "ProfilingGroupDescriptionTypeDef"}
)

DescribeProfilingGroupResponseTypeDef = TypedDict(
    "DescribeProfilingGroupResponseTypeDef", {"profilingGroup": "ProfilingGroupDescriptionTypeDef"}
)

GetPolicyResponseTypeDef = TypedDict("GetPolicyResponseTypeDef", {"policy": str, "revisionId": str})

_RequiredGetProfileResponseTypeDef = TypedDict(
    "_RequiredGetProfileResponseTypeDef", {"contentType": str, "profile": bytes}
)
_OptionalGetProfileResponseTypeDef = TypedDict(
    "_OptionalGetProfileResponseTypeDef", {"contentEncoding": str}, total=False
)


class GetProfileResponseTypeDef(
    _RequiredGetProfileResponseTypeDef, _OptionalGetProfileResponseTypeDef
):
    pass


_RequiredListProfileTimesResponseTypeDef = TypedDict(
    "_RequiredListProfileTimesResponseTypeDef", {"profileTimes": List["ProfileTimeTypeDef"]}
)
_OptionalListProfileTimesResponseTypeDef = TypedDict(
    "_OptionalListProfileTimesResponseTypeDef", {"nextToken": str}, total=False
)


class ListProfileTimesResponseTypeDef(
    _RequiredListProfileTimesResponseTypeDef, _OptionalListProfileTimesResponseTypeDef
):
    pass


_RequiredListProfilingGroupsResponseTypeDef = TypedDict(
    "_RequiredListProfilingGroupsResponseTypeDef", {"profilingGroupNames": List[str]}
)
_OptionalListProfilingGroupsResponseTypeDef = TypedDict(
    "_OptionalListProfilingGroupsResponseTypeDef",
    {"nextToken": str, "profilingGroups": List["ProfilingGroupDescriptionTypeDef"]},
    total=False,
)


class ListProfilingGroupsResponseTypeDef(
    _RequiredListProfilingGroupsResponseTypeDef, _OptionalListProfilingGroupsResponseTypeDef
):
    pass


PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

PutPermissionResponseTypeDef = TypedDict(
    "PutPermissionResponseTypeDef", {"policy": str, "revisionId": str}
)

RemovePermissionResponseTypeDef = TypedDict(
    "RemovePermissionResponseTypeDef", {"policy": str, "revisionId": str}
)

UpdateProfilingGroupResponseTypeDef = TypedDict(
    "UpdateProfilingGroupResponseTypeDef", {"profilingGroup": "ProfilingGroupDescriptionTypeDef"}
)
