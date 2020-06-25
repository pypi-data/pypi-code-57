# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin,too-many-locals,unused-import
"""
Main interface for quicksight service client

Usage::

    ```python
    import boto3
    from mypy_boto3_quicksight import QuickSightClient

    client: QuickSightClient = boto3.client("quicksight")
    ```
"""
import sys
from typing import Any, Dict, List, Type

from botocore.exceptions import ClientError as Boto3ClientError

from mypy_boto3_quicksight.type_defs import (
    CancelIngestionResponseTypeDef,
    ColumnGroupTypeDef,
    CreateDashboardResponseTypeDef,
    CreateDataSetResponseTypeDef,
    CreateDataSourceResponseTypeDef,
    CreateGroupMembershipResponseTypeDef,
    CreateGroupResponseTypeDef,
    CreateIAMPolicyAssignmentResponseTypeDef,
    CreateIngestionResponseTypeDef,
    CreateTemplateAliasResponseTypeDef,
    CreateTemplateResponseTypeDef,
    DashboardPublishOptionsTypeDef,
    DashboardSearchFilterTypeDef,
    DashboardSourceEntityTypeDef,
    DataSourceCredentialsTypeDef,
    DataSourceParametersTypeDef,
    DeleteDashboardResponseTypeDef,
    DeleteDataSetResponseTypeDef,
    DeleteDataSourceResponseTypeDef,
    DeleteGroupMembershipResponseTypeDef,
    DeleteGroupResponseTypeDef,
    DeleteIAMPolicyAssignmentResponseTypeDef,
    DeleteTemplateAliasResponseTypeDef,
    DeleteTemplateResponseTypeDef,
    DeleteUserByPrincipalIdResponseTypeDef,
    DeleteUserResponseTypeDef,
    DescribeDashboardPermissionsResponseTypeDef,
    DescribeDashboardResponseTypeDef,
    DescribeDataSetPermissionsResponseTypeDef,
    DescribeDataSetResponseTypeDef,
    DescribeDataSourcePermissionsResponseTypeDef,
    DescribeDataSourceResponseTypeDef,
    DescribeGroupResponseTypeDef,
    DescribeIAMPolicyAssignmentResponseTypeDef,
    DescribeIngestionResponseTypeDef,
    DescribeTemplateAliasResponseTypeDef,
    DescribeTemplatePermissionsResponseTypeDef,
    DescribeTemplateResponseTypeDef,
    DescribeUserResponseTypeDef,
    GetDashboardEmbedUrlResponseTypeDef,
    ListDashboardsResponseTypeDef,
    ListDashboardVersionsResponseTypeDef,
    ListDataSetsResponseTypeDef,
    ListDataSourcesResponseTypeDef,
    ListGroupMembershipsResponseTypeDef,
    ListGroupsResponseTypeDef,
    ListIAMPolicyAssignmentsForUserResponseTypeDef,
    ListIAMPolicyAssignmentsResponseTypeDef,
    ListIngestionsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTemplateAliasesResponseTypeDef,
    ListTemplatesResponseTypeDef,
    ListTemplateVersionsResponseTypeDef,
    ListUserGroupsResponseTypeDef,
    ListUsersResponseTypeDef,
    LogicalTableTypeDef,
    ParametersTypeDef,
    PhysicalTableTypeDef,
    RegisterUserResponseTypeDef,
    ResourcePermissionTypeDef,
    RowLevelPermissionDataSetTypeDef,
    SearchDashboardsResponseTypeDef,
    SslPropertiesTypeDef,
    TagResourceResponseTypeDef,
    TagTypeDef,
    TemplateSourceEntityTypeDef,
    UntagResourceResponseTypeDef,
    UpdateDashboardPermissionsResponseTypeDef,
    UpdateDashboardPublishedVersionResponseTypeDef,
    UpdateDashboardResponseTypeDef,
    UpdateDataSetPermissionsResponseTypeDef,
    UpdateDataSetResponseTypeDef,
    UpdateDataSourcePermissionsResponseTypeDef,
    UpdateDataSourceResponseTypeDef,
    UpdateGroupResponseTypeDef,
    UpdateIAMPolicyAssignmentResponseTypeDef,
    UpdateTemplateAliasResponseTypeDef,
    UpdateTemplatePermissionsResponseTypeDef,
    UpdateTemplateResponseTypeDef,
    UpdateUserResponseTypeDef,
    VpcConnectionPropertiesTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("QuickSightClient",)


class Exceptions:
    AccessDeniedException: Type[Boto3ClientError]
    ClientError: Type[Boto3ClientError]
    ConcurrentUpdatingException: Type[Boto3ClientError]
    ConflictException: Type[Boto3ClientError]
    DomainNotWhitelistedException: Type[Boto3ClientError]
    IdentityTypeNotSupportedException: Type[Boto3ClientError]
    InternalFailureException: Type[Boto3ClientError]
    InvalidNextTokenException: Type[Boto3ClientError]
    InvalidParameterValueException: Type[Boto3ClientError]
    LimitExceededException: Type[Boto3ClientError]
    PreconditionNotMetException: Type[Boto3ClientError]
    QuickSightUserNotFoundException: Type[Boto3ClientError]
    ResourceExistsException: Type[Boto3ClientError]
    ResourceNotFoundException: Type[Boto3ClientError]
    ResourceUnavailableException: Type[Boto3ClientError]
    SessionLifetimeInMinutesInvalidException: Type[Boto3ClientError]
    ThrottlingException: Type[Boto3ClientError]
    UnsupportedUserEditionException: Type[Boto3ClientError]


class QuickSightClient:
    """
    [QuickSight.Client documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client)
    """

    exceptions: Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Client.can_paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.can_paginate)
        """

    def cancel_ingestion(
        self, AwsAccountId: str, DataSetId: str, IngestionId: str
    ) -> CancelIngestionResponseTypeDef:
        """
        [Client.cancel_ingestion documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.cancel_ingestion)
        """

    def create_dashboard(
        self,
        AwsAccountId: str,
        DashboardId: str,
        Name: str,
        SourceEntity: DashboardSourceEntityTypeDef,
        Parameters: ParametersTypeDef = None,
        Permissions: List["ResourcePermissionTypeDef"] = None,
        Tags: List["TagTypeDef"] = None,
        VersionDescription: str = None,
        DashboardPublishOptions: DashboardPublishOptionsTypeDef = None,
    ) -> CreateDashboardResponseTypeDef:
        """
        [Client.create_dashboard documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.create_dashboard)
        """

    def create_data_set(
        self,
        AwsAccountId: str,
        DataSetId: str,
        Name: str,
        PhysicalTableMap: Dict[str, "PhysicalTableTypeDef"],
        ImportMode: Literal["SPICE", "DIRECT_QUERY"],
        LogicalTableMap: Dict[str, "LogicalTableTypeDef"] = None,
        ColumnGroups: List["ColumnGroupTypeDef"] = None,
        Permissions: List["ResourcePermissionTypeDef"] = None,
        RowLevelPermissionDataSet: "RowLevelPermissionDataSetTypeDef" = None,
        Tags: List["TagTypeDef"] = None,
    ) -> CreateDataSetResponseTypeDef:
        """
        [Client.create_data_set documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.create_data_set)
        """

    def create_data_source(
        self,
        AwsAccountId: str,
        DataSourceId: str,
        Name: str,
        Type: Literal[
            "ADOBE_ANALYTICS",
            "AMAZON_ELASTICSEARCH",
            "ATHENA",
            "AURORA",
            "AURORA_POSTGRESQL",
            "AWS_IOT_ANALYTICS",
            "GITHUB",
            "JIRA",
            "MARIADB",
            "MYSQL",
            "POSTGRESQL",
            "PRESTO",
            "REDSHIFT",
            "S3",
            "SALESFORCE",
            "SERVICENOW",
            "SNOWFLAKE",
            "SPARK",
            "SQLSERVER",
            "TERADATA",
            "TWITTER",
        ],
        DataSourceParameters: "DataSourceParametersTypeDef" = None,
        Credentials: DataSourceCredentialsTypeDef = None,
        Permissions: List["ResourcePermissionTypeDef"] = None,
        VpcConnectionProperties: "VpcConnectionPropertiesTypeDef" = None,
        SslProperties: "SslPropertiesTypeDef" = None,
        Tags: List["TagTypeDef"] = None,
    ) -> CreateDataSourceResponseTypeDef:
        """
        [Client.create_data_source documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.create_data_source)
        """

    def create_group(
        self, GroupName: str, AwsAccountId: str, Namespace: str, Description: str = None
    ) -> CreateGroupResponseTypeDef:
        """
        [Client.create_group documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.create_group)
        """

    def create_group_membership(
        self, MemberName: str, GroupName: str, AwsAccountId: str, Namespace: str
    ) -> CreateGroupMembershipResponseTypeDef:
        """
        [Client.create_group_membership documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.create_group_membership)
        """

    def create_iam_policy_assignment(
        self,
        AwsAccountId: str,
        AssignmentName: str,
        AssignmentStatus: Literal["ENABLED", "DRAFT", "DISABLED"],
        Namespace: str,
        PolicyArn: str = None,
        Identities: Dict[str, List[str]] = None,
    ) -> CreateIAMPolicyAssignmentResponseTypeDef:
        """
        [Client.create_iam_policy_assignment documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.create_iam_policy_assignment)
        """

    def create_ingestion(
        self, DataSetId: str, IngestionId: str, AwsAccountId: str
    ) -> CreateIngestionResponseTypeDef:
        """
        [Client.create_ingestion documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.create_ingestion)
        """

    def create_template(
        self,
        AwsAccountId: str,
        TemplateId: str,
        SourceEntity: TemplateSourceEntityTypeDef,
        Name: str = None,
        Permissions: List["ResourcePermissionTypeDef"] = None,
        Tags: List["TagTypeDef"] = None,
        VersionDescription: str = None,
    ) -> CreateTemplateResponseTypeDef:
        """
        [Client.create_template documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.create_template)
        """

    def create_template_alias(
        self, AwsAccountId: str, TemplateId: str, AliasName: str, TemplateVersionNumber: int
    ) -> CreateTemplateAliasResponseTypeDef:
        """
        [Client.create_template_alias documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.create_template_alias)
        """

    def delete_dashboard(
        self, AwsAccountId: str, DashboardId: str, VersionNumber: int = None
    ) -> DeleteDashboardResponseTypeDef:
        """
        [Client.delete_dashboard documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.delete_dashboard)
        """

    def delete_data_set(self, AwsAccountId: str, DataSetId: str) -> DeleteDataSetResponseTypeDef:
        """
        [Client.delete_data_set documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.delete_data_set)
        """

    def delete_data_source(
        self, AwsAccountId: str, DataSourceId: str
    ) -> DeleteDataSourceResponseTypeDef:
        """
        [Client.delete_data_source documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.delete_data_source)
        """

    def delete_group(
        self, GroupName: str, AwsAccountId: str, Namespace: str
    ) -> DeleteGroupResponseTypeDef:
        """
        [Client.delete_group documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.delete_group)
        """

    def delete_group_membership(
        self, MemberName: str, GroupName: str, AwsAccountId: str, Namespace: str
    ) -> DeleteGroupMembershipResponseTypeDef:
        """
        [Client.delete_group_membership documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.delete_group_membership)
        """

    def delete_iam_policy_assignment(
        self, AwsAccountId: str, AssignmentName: str, Namespace: str
    ) -> DeleteIAMPolicyAssignmentResponseTypeDef:
        """
        [Client.delete_iam_policy_assignment documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.delete_iam_policy_assignment)
        """

    def delete_template(
        self, AwsAccountId: str, TemplateId: str, VersionNumber: int = None
    ) -> DeleteTemplateResponseTypeDef:
        """
        [Client.delete_template documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.delete_template)
        """

    def delete_template_alias(
        self, AwsAccountId: str, TemplateId: str, AliasName: str
    ) -> DeleteTemplateAliasResponseTypeDef:
        """
        [Client.delete_template_alias documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.delete_template_alias)
        """

    def delete_user(
        self, UserName: str, AwsAccountId: str, Namespace: str
    ) -> DeleteUserResponseTypeDef:
        """
        [Client.delete_user documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.delete_user)
        """

    def delete_user_by_principal_id(
        self, PrincipalId: str, AwsAccountId: str, Namespace: str
    ) -> DeleteUserByPrincipalIdResponseTypeDef:
        """
        [Client.delete_user_by_principal_id documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.delete_user_by_principal_id)
        """

    def describe_dashboard(
        self, AwsAccountId: str, DashboardId: str, VersionNumber: int = None, AliasName: str = None
    ) -> DescribeDashboardResponseTypeDef:
        """
        [Client.describe_dashboard documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.describe_dashboard)
        """

    def describe_dashboard_permissions(
        self, AwsAccountId: str, DashboardId: str
    ) -> DescribeDashboardPermissionsResponseTypeDef:
        """
        [Client.describe_dashboard_permissions documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.describe_dashboard_permissions)
        """

    def describe_data_set(
        self, AwsAccountId: str, DataSetId: str
    ) -> DescribeDataSetResponseTypeDef:
        """
        [Client.describe_data_set documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.describe_data_set)
        """

    def describe_data_set_permissions(
        self, AwsAccountId: str, DataSetId: str
    ) -> DescribeDataSetPermissionsResponseTypeDef:
        """
        [Client.describe_data_set_permissions documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.describe_data_set_permissions)
        """

    def describe_data_source(
        self, AwsAccountId: str, DataSourceId: str
    ) -> DescribeDataSourceResponseTypeDef:
        """
        [Client.describe_data_source documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.describe_data_source)
        """

    def describe_data_source_permissions(
        self, AwsAccountId: str, DataSourceId: str
    ) -> DescribeDataSourcePermissionsResponseTypeDef:
        """
        [Client.describe_data_source_permissions documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.describe_data_source_permissions)
        """

    def describe_group(
        self, GroupName: str, AwsAccountId: str, Namespace: str
    ) -> DescribeGroupResponseTypeDef:
        """
        [Client.describe_group documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.describe_group)
        """

    def describe_iam_policy_assignment(
        self, AwsAccountId: str, AssignmentName: str, Namespace: str
    ) -> DescribeIAMPolicyAssignmentResponseTypeDef:
        """
        [Client.describe_iam_policy_assignment documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.describe_iam_policy_assignment)
        """

    def describe_ingestion(
        self, AwsAccountId: str, DataSetId: str, IngestionId: str
    ) -> DescribeIngestionResponseTypeDef:
        """
        [Client.describe_ingestion documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.describe_ingestion)
        """

    def describe_template(
        self, AwsAccountId: str, TemplateId: str, VersionNumber: int = None, AliasName: str = None
    ) -> DescribeTemplateResponseTypeDef:
        """
        [Client.describe_template documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.describe_template)
        """

    def describe_template_alias(
        self, AwsAccountId: str, TemplateId: str, AliasName: str
    ) -> DescribeTemplateAliasResponseTypeDef:
        """
        [Client.describe_template_alias documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.describe_template_alias)
        """

    def describe_template_permissions(
        self, AwsAccountId: str, TemplateId: str
    ) -> DescribeTemplatePermissionsResponseTypeDef:
        """
        [Client.describe_template_permissions documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.describe_template_permissions)
        """

    def describe_user(
        self, UserName: str, AwsAccountId: str, Namespace: str
    ) -> DescribeUserResponseTypeDef:
        """
        [Client.describe_user documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.describe_user)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Client.generate_presigned_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.generate_presigned_url)
        """

    def get_dashboard_embed_url(
        self,
        AwsAccountId: str,
        DashboardId: str,
        IdentityType: Literal["IAM", "QUICKSIGHT"],
        SessionLifetimeInMinutes: int = None,
        UndoRedoDisabled: bool = None,
        ResetDisabled: bool = None,
        UserArn: str = None,
    ) -> GetDashboardEmbedUrlResponseTypeDef:
        """
        [Client.get_dashboard_embed_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.get_dashboard_embed_url)
        """

    def list_dashboard_versions(
        self, AwsAccountId: str, DashboardId: str, NextToken: str = None, MaxResults: int = None
    ) -> ListDashboardVersionsResponseTypeDef:
        """
        [Client.list_dashboard_versions documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.list_dashboard_versions)
        """

    def list_dashboards(
        self, AwsAccountId: str, NextToken: str = None, MaxResults: int = None
    ) -> ListDashboardsResponseTypeDef:
        """
        [Client.list_dashboards documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.list_dashboards)
        """

    def list_data_sets(
        self, AwsAccountId: str, NextToken: str = None, MaxResults: int = None
    ) -> ListDataSetsResponseTypeDef:
        """
        [Client.list_data_sets documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.list_data_sets)
        """

    def list_data_sources(
        self, AwsAccountId: str, NextToken: str = None, MaxResults: int = None
    ) -> ListDataSourcesResponseTypeDef:
        """
        [Client.list_data_sources documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.list_data_sources)
        """

    def list_group_memberships(
        self,
        GroupName: str,
        AwsAccountId: str,
        Namespace: str,
        NextToken: str = None,
        MaxResults: int = None,
    ) -> ListGroupMembershipsResponseTypeDef:
        """
        [Client.list_group_memberships documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.list_group_memberships)
        """

    def list_groups(
        self, AwsAccountId: str, Namespace: str, NextToken: str = None, MaxResults: int = None
    ) -> ListGroupsResponseTypeDef:
        """
        [Client.list_groups documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.list_groups)
        """

    def list_iam_policy_assignments(
        self,
        AwsAccountId: str,
        Namespace: str,
        AssignmentStatus: Literal["ENABLED", "DRAFT", "DISABLED"] = None,
        NextToken: str = None,
        MaxResults: int = None,
    ) -> ListIAMPolicyAssignmentsResponseTypeDef:
        """
        [Client.list_iam_policy_assignments documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.list_iam_policy_assignments)
        """

    def list_iam_policy_assignments_for_user(
        self,
        AwsAccountId: str,
        UserName: str,
        Namespace: str,
        NextToken: str = None,
        MaxResults: int = None,
    ) -> ListIAMPolicyAssignmentsForUserResponseTypeDef:
        """
        [Client.list_iam_policy_assignments_for_user documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.list_iam_policy_assignments_for_user)
        """

    def list_ingestions(
        self, DataSetId: str, AwsAccountId: str, NextToken: str = None, MaxResults: int = None
    ) -> ListIngestionsResponseTypeDef:
        """
        [Client.list_ingestions documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.list_ingestions)
        """

    def list_tags_for_resource(self, ResourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        [Client.list_tags_for_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.list_tags_for_resource)
        """

    def list_template_aliases(
        self, AwsAccountId: str, TemplateId: str, NextToken: str = None, MaxResults: int = None
    ) -> ListTemplateAliasesResponseTypeDef:
        """
        [Client.list_template_aliases documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.list_template_aliases)
        """

    def list_template_versions(
        self, AwsAccountId: str, TemplateId: str, NextToken: str = None, MaxResults: int = None
    ) -> ListTemplateVersionsResponseTypeDef:
        """
        [Client.list_template_versions documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.list_template_versions)
        """

    def list_templates(
        self, AwsAccountId: str, NextToken: str = None, MaxResults: int = None
    ) -> ListTemplatesResponseTypeDef:
        """
        [Client.list_templates documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.list_templates)
        """

    def list_user_groups(
        self,
        UserName: str,
        AwsAccountId: str,
        Namespace: str,
        NextToken: str = None,
        MaxResults: int = None,
    ) -> ListUserGroupsResponseTypeDef:
        """
        [Client.list_user_groups documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.list_user_groups)
        """

    def list_users(
        self, AwsAccountId: str, Namespace: str, NextToken: str = None, MaxResults: int = None
    ) -> ListUsersResponseTypeDef:
        """
        [Client.list_users documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.list_users)
        """

    def register_user(
        self,
        IdentityType: Literal["IAM", "QUICKSIGHT"],
        Email: str,
        UserRole: Literal["ADMIN", "AUTHOR", "READER", "RESTRICTED_AUTHOR", "RESTRICTED_READER"],
        AwsAccountId: str,
        Namespace: str,
        IamArn: str = None,
        SessionName: str = None,
        UserName: str = None,
    ) -> RegisterUserResponseTypeDef:
        """
        [Client.register_user documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.register_user)
        """

    def search_dashboards(
        self,
        AwsAccountId: str,
        Filters: List[DashboardSearchFilterTypeDef],
        NextToken: str = None,
        MaxResults: int = None,
    ) -> SearchDashboardsResponseTypeDef:
        """
        [Client.search_dashboards documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.search_dashboards)
        """

    def tag_resource(
        self, ResourceArn: str, Tags: List["TagTypeDef"]
    ) -> TagResourceResponseTypeDef:
        """
        [Client.tag_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.tag_resource)
        """

    def untag_resource(self, ResourceArn: str, TagKeys: List[str]) -> UntagResourceResponseTypeDef:
        """
        [Client.untag_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.untag_resource)
        """

    def update_dashboard(
        self,
        AwsAccountId: str,
        DashboardId: str,
        Name: str,
        SourceEntity: DashboardSourceEntityTypeDef,
        Parameters: ParametersTypeDef = None,
        VersionDescription: str = None,
        DashboardPublishOptions: DashboardPublishOptionsTypeDef = None,
    ) -> UpdateDashboardResponseTypeDef:
        """
        [Client.update_dashboard documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.update_dashboard)
        """

    def update_dashboard_permissions(
        self,
        AwsAccountId: str,
        DashboardId: str,
        GrantPermissions: List["ResourcePermissionTypeDef"] = None,
        RevokePermissions: List["ResourcePermissionTypeDef"] = None,
    ) -> UpdateDashboardPermissionsResponseTypeDef:
        """
        [Client.update_dashboard_permissions documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.update_dashboard_permissions)
        """

    def update_dashboard_published_version(
        self, AwsAccountId: str, DashboardId: str, VersionNumber: int
    ) -> UpdateDashboardPublishedVersionResponseTypeDef:
        """
        [Client.update_dashboard_published_version documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.update_dashboard_published_version)
        """

    def update_data_set(
        self,
        AwsAccountId: str,
        DataSetId: str,
        Name: str,
        PhysicalTableMap: Dict[str, "PhysicalTableTypeDef"],
        ImportMode: Literal["SPICE", "DIRECT_QUERY"],
        LogicalTableMap: Dict[str, "LogicalTableTypeDef"] = None,
        ColumnGroups: List["ColumnGroupTypeDef"] = None,
        RowLevelPermissionDataSet: "RowLevelPermissionDataSetTypeDef" = None,
    ) -> UpdateDataSetResponseTypeDef:
        """
        [Client.update_data_set documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.update_data_set)
        """

    def update_data_set_permissions(
        self,
        AwsAccountId: str,
        DataSetId: str,
        GrantPermissions: List["ResourcePermissionTypeDef"] = None,
        RevokePermissions: List["ResourcePermissionTypeDef"] = None,
    ) -> UpdateDataSetPermissionsResponseTypeDef:
        """
        [Client.update_data_set_permissions documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.update_data_set_permissions)
        """

    def update_data_source(
        self,
        AwsAccountId: str,
        DataSourceId: str,
        Name: str,
        DataSourceParameters: "DataSourceParametersTypeDef" = None,
        Credentials: DataSourceCredentialsTypeDef = None,
        VpcConnectionProperties: "VpcConnectionPropertiesTypeDef" = None,
        SslProperties: "SslPropertiesTypeDef" = None,
    ) -> UpdateDataSourceResponseTypeDef:
        """
        [Client.update_data_source documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.update_data_source)
        """

    def update_data_source_permissions(
        self,
        AwsAccountId: str,
        DataSourceId: str,
        GrantPermissions: List["ResourcePermissionTypeDef"] = None,
        RevokePermissions: List["ResourcePermissionTypeDef"] = None,
    ) -> UpdateDataSourcePermissionsResponseTypeDef:
        """
        [Client.update_data_source_permissions documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.update_data_source_permissions)
        """

    def update_group(
        self, GroupName: str, AwsAccountId: str, Namespace: str, Description: str = None
    ) -> UpdateGroupResponseTypeDef:
        """
        [Client.update_group documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.update_group)
        """

    def update_iam_policy_assignment(
        self,
        AwsAccountId: str,
        AssignmentName: str,
        Namespace: str,
        AssignmentStatus: Literal["ENABLED", "DRAFT", "DISABLED"] = None,
        PolicyArn: str = None,
        Identities: Dict[str, List[str]] = None,
    ) -> UpdateIAMPolicyAssignmentResponseTypeDef:
        """
        [Client.update_iam_policy_assignment documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.update_iam_policy_assignment)
        """

    def update_template(
        self,
        AwsAccountId: str,
        TemplateId: str,
        SourceEntity: TemplateSourceEntityTypeDef,
        VersionDescription: str = None,
        Name: str = None,
    ) -> UpdateTemplateResponseTypeDef:
        """
        [Client.update_template documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.update_template)
        """

    def update_template_alias(
        self, AwsAccountId: str, TemplateId: str, AliasName: str, TemplateVersionNumber: int
    ) -> UpdateTemplateAliasResponseTypeDef:
        """
        [Client.update_template_alias documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.update_template_alias)
        """

    def update_template_permissions(
        self,
        AwsAccountId: str,
        TemplateId: str,
        GrantPermissions: List["ResourcePermissionTypeDef"] = None,
        RevokePermissions: List["ResourcePermissionTypeDef"] = None,
    ) -> UpdateTemplatePermissionsResponseTypeDef:
        """
        [Client.update_template_permissions documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.update_template_permissions)
        """

    def update_user(
        self,
        UserName: str,
        AwsAccountId: str,
        Namespace: str,
        Email: str,
        Role: Literal["ADMIN", "AUTHOR", "READER", "RESTRICTED_AUTHOR", "RESTRICTED_READER"],
    ) -> UpdateUserResponseTypeDef:
        """
        [Client.update_user documentation](https://boto3.amazonaws.com/v1/documentation/api/1.14.11/reference/services/quicksight.html#QuickSight.Client.update_user)
        """
