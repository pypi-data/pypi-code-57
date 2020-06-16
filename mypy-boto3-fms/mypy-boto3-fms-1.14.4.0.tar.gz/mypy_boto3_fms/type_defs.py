"""
Main interface for fms service type definitions.

Usage::

    ```python
    from mypy_boto3_fms.type_defs import ComplianceViolatorTypeDef

    data: ComplianceViolatorTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "ComplianceViolatorTypeDef",
    "EvaluationResultTypeDef",
    "PolicyComplianceDetailTypeDef",
    "PolicyComplianceStatusTypeDef",
    "PolicySummaryTypeDef",
    "PolicyTypeDef",
    "ResourceTagTypeDef",
    "SecurityServicePolicyDataTypeDef",
    "TagTypeDef",
    "GetAdminAccountResponseTypeDef",
    "GetComplianceDetailResponseTypeDef",
    "GetNotificationChannelResponseTypeDef",
    "GetPolicyResponseTypeDef",
    "GetProtectionStatusResponseTypeDef",
    "ListComplianceStatusResponseTypeDef",
    "ListMemberAccountsResponseTypeDef",
    "ListPoliciesResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PutPolicyResponseTypeDef",
)

ComplianceViolatorTypeDef = TypedDict(
    "ComplianceViolatorTypeDef",
    {
        "ResourceId": str,
        "ViolationReason": Literal[
            "WEB_ACL_MISSING_RULE_GROUP",
            "RESOURCE_MISSING_WEB_ACL",
            "RESOURCE_INCORRECT_WEB_ACL",
            "RESOURCE_MISSING_SHIELD_PROTECTION",
            "RESOURCE_MISSING_WEB_ACL_OR_SHIELD_PROTECTION",
            "RESOURCE_MISSING_SECURITY_GROUP",
            "RESOURCE_VIOLATES_AUDIT_SECURITY_GROUP",
            "SECURITY_GROUP_UNUSED",
            "SECURITY_GROUP_REDUNDANT",
        ],
        "ResourceType": str,
    },
    total=False,
)

EvaluationResultTypeDef = TypedDict(
    "EvaluationResultTypeDef",
    {
        "ComplianceStatus": Literal["COMPLIANT", "NON_COMPLIANT"],
        "ViolatorCount": int,
        "EvaluationLimitExceeded": bool,
    },
    total=False,
)

PolicyComplianceDetailTypeDef = TypedDict(
    "PolicyComplianceDetailTypeDef",
    {
        "PolicyOwner": str,
        "PolicyId": str,
        "MemberAccount": str,
        "Violators": List["ComplianceViolatorTypeDef"],
        "EvaluationLimitExceeded": bool,
        "ExpiredAt": datetime,
        "IssueInfoMap": Dict[Literal["AWSCONFIG", "AWSWAF", "AWSSHIELD_ADVANCED", "AWSVPC"], str],
    },
    total=False,
)

PolicyComplianceStatusTypeDef = TypedDict(
    "PolicyComplianceStatusTypeDef",
    {
        "PolicyOwner": str,
        "PolicyId": str,
        "PolicyName": str,
        "MemberAccount": str,
        "EvaluationResults": List["EvaluationResultTypeDef"],
        "LastUpdated": datetime,
        "IssueInfoMap": Dict[Literal["AWSCONFIG", "AWSWAF", "AWSSHIELD_ADVANCED", "AWSVPC"], str],
    },
    total=False,
)

PolicySummaryTypeDef = TypedDict(
    "PolicySummaryTypeDef",
    {
        "PolicyArn": str,
        "PolicyId": str,
        "PolicyName": str,
        "ResourceType": str,
        "SecurityServiceType": Literal[
            "WAF",
            "WAFV2",
            "SHIELD_ADVANCED",
            "SECURITY_GROUPS_COMMON",
            "SECURITY_GROUPS_CONTENT_AUDIT",
            "SECURITY_GROUPS_USAGE_AUDIT",
        ],
        "RemediationEnabled": bool,
    },
    total=False,
)

_RequiredPolicyTypeDef = TypedDict(
    "_RequiredPolicyTypeDef",
    {
        "PolicyName": str,
        "SecurityServicePolicyData": "SecurityServicePolicyDataTypeDef",
        "ResourceType": str,
        "ExcludeResourceTags": bool,
        "RemediationEnabled": bool,
    },
)
_OptionalPolicyTypeDef = TypedDict(
    "_OptionalPolicyTypeDef",
    {
        "PolicyId": str,
        "PolicyUpdateToken": str,
        "ResourceTypeList": List[str],
        "ResourceTags": List["ResourceTagTypeDef"],
        "IncludeMap": Dict[Literal["ACCOUNT", "ORG_UNIT"], List[str]],
        "ExcludeMap": Dict[Literal["ACCOUNT", "ORG_UNIT"], List[str]],
    },
    total=False,
)


class PolicyTypeDef(_RequiredPolicyTypeDef, _OptionalPolicyTypeDef):
    pass


_RequiredResourceTagTypeDef = TypedDict("_RequiredResourceTagTypeDef", {"Key": str})
_OptionalResourceTagTypeDef = TypedDict("_OptionalResourceTagTypeDef", {"Value": str}, total=False)


class ResourceTagTypeDef(_RequiredResourceTagTypeDef, _OptionalResourceTagTypeDef):
    pass


_RequiredSecurityServicePolicyDataTypeDef = TypedDict(
    "_RequiredSecurityServicePolicyDataTypeDef",
    {
        "Type": Literal[
            "WAF",
            "WAFV2",
            "SHIELD_ADVANCED",
            "SECURITY_GROUPS_COMMON",
            "SECURITY_GROUPS_CONTENT_AUDIT",
            "SECURITY_GROUPS_USAGE_AUDIT",
        ]
    },
)
_OptionalSecurityServicePolicyDataTypeDef = TypedDict(
    "_OptionalSecurityServicePolicyDataTypeDef", {"ManagedServiceData": str}, total=False
)


class SecurityServicePolicyDataTypeDef(
    _RequiredSecurityServicePolicyDataTypeDef, _OptionalSecurityServicePolicyDataTypeDef
):
    pass


TagTypeDef = TypedDict("TagTypeDef", {"Key": str, "Value": str})

GetAdminAccountResponseTypeDef = TypedDict(
    "GetAdminAccountResponseTypeDef",
    {
        "AdminAccount": str,
        "RoleStatus": Literal["READY", "CREATING", "PENDING_DELETION", "DELETING", "DELETED"],
    },
    total=False,
)

GetComplianceDetailResponseTypeDef = TypedDict(
    "GetComplianceDetailResponseTypeDef",
    {"PolicyComplianceDetail": "PolicyComplianceDetailTypeDef"},
    total=False,
)

GetNotificationChannelResponseTypeDef = TypedDict(
    "GetNotificationChannelResponseTypeDef", {"SnsTopicArn": str, "SnsRoleName": str}, total=False
)

GetPolicyResponseTypeDef = TypedDict(
    "GetPolicyResponseTypeDef", {"Policy": "PolicyTypeDef", "PolicyArn": str}, total=False
)

GetProtectionStatusResponseTypeDef = TypedDict(
    "GetProtectionStatusResponseTypeDef",
    {
        "AdminAccountId": str,
        "ServiceType": Literal[
            "WAF",
            "WAFV2",
            "SHIELD_ADVANCED",
            "SECURITY_GROUPS_COMMON",
            "SECURITY_GROUPS_CONTENT_AUDIT",
            "SECURITY_GROUPS_USAGE_AUDIT",
        ],
        "Data": str,
        "NextToken": str,
    },
    total=False,
)

ListComplianceStatusResponseTypeDef = TypedDict(
    "ListComplianceStatusResponseTypeDef",
    {"PolicyComplianceStatusList": List["PolicyComplianceStatusTypeDef"], "NextToken": str},
    total=False,
)

ListMemberAccountsResponseTypeDef = TypedDict(
    "ListMemberAccountsResponseTypeDef",
    {"MemberAccounts": List[str], "NextToken": str},
    total=False,
)

ListPoliciesResponseTypeDef = TypedDict(
    "ListPoliciesResponseTypeDef",
    {"PolicyList": List["PolicySummaryTypeDef"], "NextToken": str},
    total=False,
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef", {"TagList": List["TagTypeDef"]}, total=False
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

PutPolicyResponseTypeDef = TypedDict(
    "PutPolicyResponseTypeDef", {"Policy": "PolicyTypeDef", "PolicyArn": str}, total=False
)
