"""
Main interface for quicksight service type definitions.

Usage::

    ```python
    from mypy_boto3_quicksight.type_defs import ActiveIAMPolicyAssignmentTypeDef

    data: ActiveIAMPolicyAssignmentTypeDef = {...}
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
    "ActiveIAMPolicyAssignmentTypeDef",
    "AdHocFilteringOptionTypeDef",
    "AmazonElasticsearchParametersTypeDef",
    "AthenaParametersTypeDef",
    "AuroraParametersTypeDef",
    "AuroraPostgreSqlParametersTypeDef",
    "AwsIotAnalyticsParametersTypeDef",
    "CalculatedColumnTypeDef",
    "CastColumnTypeOperationTypeDef",
    "ColumnGroupColumnSchemaTypeDef",
    "ColumnGroupSchemaTypeDef",
    "ColumnGroupTypeDef",
    "ColumnSchemaTypeDef",
    "ColumnTagTypeDef",
    "CreateColumnsOperationTypeDef",
    "CredentialPairTypeDef",
    "CustomSqlTypeDef",
    "DashboardErrorTypeDef",
    "DashboardSourceTemplateTypeDef",
    "DashboardSummaryTypeDef",
    "DashboardTypeDef",
    "DashboardVersionSummaryTypeDef",
    "DashboardVersionTypeDef",
    "DataSetConfigurationTypeDef",
    "DataSetReferenceTypeDef",
    "DataSetSchemaTypeDef",
    "DataSetSummaryTypeDef",
    "DataSetTypeDef",
    "DataSourceErrorInfoTypeDef",
    "DataSourceParametersTypeDef",
    "DataSourceTypeDef",
    "DateTimeParameterTypeDef",
    "DecimalParameterTypeDef",
    "ErrorInfoTypeDef",
    "ExportToCSVOptionTypeDef",
    "FilterOperationTypeDef",
    "GeoSpatialColumnGroupTypeDef",
    "GroupMemberTypeDef",
    "GroupTypeDef",
    "IAMPolicyAssignmentSummaryTypeDef",
    "IAMPolicyAssignmentTypeDef",
    "IngestionTypeDef",
    "InputColumnTypeDef",
    "IntegerParameterTypeDef",
    "JiraParametersTypeDef",
    "JoinInstructionTypeDef",
    "LogicalTableSourceTypeDef",
    "LogicalTableTypeDef",
    "ManifestFileLocationTypeDef",
    "MariaDbParametersTypeDef",
    "MySqlParametersTypeDef",
    "OutputColumnTypeDef",
    "PhysicalTableTypeDef",
    "PostgreSqlParametersTypeDef",
    "PrestoParametersTypeDef",
    "ProjectOperationTypeDef",
    "QueueInfoTypeDef",
    "RdsParametersTypeDef",
    "RedshiftParametersTypeDef",
    "RelationalTableTypeDef",
    "RenameColumnOperationTypeDef",
    "ResourcePermissionTypeDef",
    "RowInfoTypeDef",
    "RowLevelPermissionDataSetTypeDef",
    "S3ParametersTypeDef",
    "S3SourceTypeDef",
    "ServiceNowParametersTypeDef",
    "SheetControlsOptionTypeDef",
    "SnowflakeParametersTypeDef",
    "SparkParametersTypeDef",
    "SqlServerParametersTypeDef",
    "SslPropertiesTypeDef",
    "StringParameterTypeDef",
    "TagColumnOperationTypeDef",
    "TagTypeDef",
    "TemplateAliasTypeDef",
    "TemplateErrorTypeDef",
    "TemplateSourceAnalysisTypeDef",
    "TemplateSourceTemplateTypeDef",
    "TemplateSummaryTypeDef",
    "TemplateTypeDef",
    "TemplateVersionSummaryTypeDef",
    "TemplateVersionTypeDef",
    "TeradataParametersTypeDef",
    "TransformOperationTypeDef",
    "TwitterParametersTypeDef",
    "UploadSettingsTypeDef",
    "UserTypeDef",
    "VpcConnectionPropertiesTypeDef",
    "CancelIngestionResponseTypeDef",
    "CreateDashboardResponseTypeDef",
    "CreateDataSetResponseTypeDef",
    "CreateDataSourceResponseTypeDef",
    "CreateGroupMembershipResponseTypeDef",
    "CreateGroupResponseTypeDef",
    "CreateIAMPolicyAssignmentResponseTypeDef",
    "CreateIngestionResponseTypeDef",
    "CreateTemplateAliasResponseTypeDef",
    "CreateTemplateResponseTypeDef",
    "DashboardPublishOptionsTypeDef",
    "DashboardSearchFilterTypeDef",
    "DashboardSourceEntityTypeDef",
    "DataSourceCredentialsTypeDef",
    "DeleteDashboardResponseTypeDef",
    "DeleteDataSetResponseTypeDef",
    "DeleteDataSourceResponseTypeDef",
    "DeleteGroupMembershipResponseTypeDef",
    "DeleteGroupResponseTypeDef",
    "DeleteIAMPolicyAssignmentResponseTypeDef",
    "DeleteTemplateAliasResponseTypeDef",
    "DeleteTemplateResponseTypeDef",
    "DeleteUserByPrincipalIdResponseTypeDef",
    "DeleteUserResponseTypeDef",
    "DescribeDashboardPermissionsResponseTypeDef",
    "DescribeDashboardResponseTypeDef",
    "DescribeDataSetPermissionsResponseTypeDef",
    "DescribeDataSetResponseTypeDef",
    "DescribeDataSourcePermissionsResponseTypeDef",
    "DescribeDataSourceResponseTypeDef",
    "DescribeGroupResponseTypeDef",
    "DescribeIAMPolicyAssignmentResponseTypeDef",
    "DescribeIngestionResponseTypeDef",
    "DescribeTemplateAliasResponseTypeDef",
    "DescribeTemplatePermissionsResponseTypeDef",
    "DescribeTemplateResponseTypeDef",
    "DescribeUserResponseTypeDef",
    "GetDashboardEmbedUrlResponseTypeDef",
    "ListDashboardVersionsResponseTypeDef",
    "ListDashboardsResponseTypeDef",
    "ListDataSetsResponseTypeDef",
    "ListDataSourcesResponseTypeDef",
    "ListGroupMembershipsResponseTypeDef",
    "ListGroupsResponseTypeDef",
    "ListIAMPolicyAssignmentsForUserResponseTypeDef",
    "ListIAMPolicyAssignmentsResponseTypeDef",
    "ListIngestionsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTemplateAliasesResponseTypeDef",
    "ListTemplateVersionsResponseTypeDef",
    "ListTemplatesResponseTypeDef",
    "ListUserGroupsResponseTypeDef",
    "ListUsersResponseTypeDef",
    "ParametersTypeDef",
    "RegisterUserResponseTypeDef",
    "SearchDashboardsResponseTypeDef",
    "TagResourceResponseTypeDef",
    "TemplateSourceEntityTypeDef",
    "UntagResourceResponseTypeDef",
    "UpdateDashboardPermissionsResponseTypeDef",
    "UpdateDashboardPublishedVersionResponseTypeDef",
    "UpdateDashboardResponseTypeDef",
    "UpdateDataSetPermissionsResponseTypeDef",
    "UpdateDataSetResponseTypeDef",
    "UpdateDataSourcePermissionsResponseTypeDef",
    "UpdateDataSourceResponseTypeDef",
    "UpdateGroupResponseTypeDef",
    "UpdateIAMPolicyAssignmentResponseTypeDef",
    "UpdateTemplateAliasResponseTypeDef",
    "UpdateTemplatePermissionsResponseTypeDef",
    "UpdateTemplateResponseTypeDef",
    "UpdateUserResponseTypeDef",
)

ActiveIAMPolicyAssignmentTypeDef = TypedDict(
    "ActiveIAMPolicyAssignmentTypeDef", {"AssignmentName": str, "PolicyArn": str}, total=False
)

AdHocFilteringOptionTypeDef = TypedDict(
    "AdHocFilteringOptionTypeDef",
    {"AvailabilityStatus": Literal["ENABLED", "DISABLED"]},
    total=False,
)

AmazonElasticsearchParametersTypeDef = TypedDict(
    "AmazonElasticsearchParametersTypeDef", {"Domain": str}
)

AthenaParametersTypeDef = TypedDict("AthenaParametersTypeDef", {"WorkGroup": str}, total=False)

AuroraParametersTypeDef = TypedDict(
    "AuroraParametersTypeDef", {"Host": str, "Port": int, "Database": str}
)

AuroraPostgreSqlParametersTypeDef = TypedDict(
    "AuroraPostgreSqlParametersTypeDef", {"Host": str, "Port": int, "Database": str}
)

AwsIotAnalyticsParametersTypeDef = TypedDict(
    "AwsIotAnalyticsParametersTypeDef", {"DataSetName": str}
)

CalculatedColumnTypeDef = TypedDict(
    "CalculatedColumnTypeDef", {"ColumnName": str, "ColumnId": str, "Expression": str}
)

_RequiredCastColumnTypeOperationTypeDef = TypedDict(
    "_RequiredCastColumnTypeOperationTypeDef",
    {"ColumnName": str, "NewColumnType": Literal["STRING", "INTEGER", "DECIMAL", "DATETIME"]},
)
_OptionalCastColumnTypeOperationTypeDef = TypedDict(
    "_OptionalCastColumnTypeOperationTypeDef", {"Format": str}, total=False
)


class CastColumnTypeOperationTypeDef(
    _RequiredCastColumnTypeOperationTypeDef, _OptionalCastColumnTypeOperationTypeDef
):
    pass


ColumnGroupColumnSchemaTypeDef = TypedDict(
    "ColumnGroupColumnSchemaTypeDef", {"Name": str}, total=False
)

ColumnGroupSchemaTypeDef = TypedDict(
    "ColumnGroupSchemaTypeDef",
    {"Name": str, "ColumnGroupColumnSchemaList": List["ColumnGroupColumnSchemaTypeDef"]},
    total=False,
)

ColumnGroupTypeDef = TypedDict(
    "ColumnGroupTypeDef", {"GeoSpatialColumnGroup": "GeoSpatialColumnGroupTypeDef"}, total=False
)

ColumnSchemaTypeDef = TypedDict(
    "ColumnSchemaTypeDef", {"Name": str, "DataType": str, "GeographicRole": str}, total=False
)

ColumnTagTypeDef = TypedDict(
    "ColumnTagTypeDef",
    {
        "ColumnGeographicRole": Literal[
            "COUNTRY", "STATE", "COUNTY", "CITY", "POSTCODE", "LONGITUDE", "LATITUDE"
        ]
    },
    total=False,
)

CreateColumnsOperationTypeDef = TypedDict(
    "CreateColumnsOperationTypeDef", {"Columns": List["CalculatedColumnTypeDef"]}
)

CredentialPairTypeDef = TypedDict("CredentialPairTypeDef", {"Username": str, "Password": str})

_RequiredCustomSqlTypeDef = TypedDict(
    "_RequiredCustomSqlTypeDef", {"DataSourceArn": str, "Name": str, "SqlQuery": str}
)
_OptionalCustomSqlTypeDef = TypedDict(
    "_OptionalCustomSqlTypeDef", {"Columns": List["InputColumnTypeDef"]}, total=False
)


class CustomSqlTypeDef(_RequiredCustomSqlTypeDef, _OptionalCustomSqlTypeDef):
    pass


DashboardErrorTypeDef = TypedDict(
    "DashboardErrorTypeDef",
    {
        "Type": Literal[
            "ACCESS_DENIED",
            "SOURCE_NOT_FOUND",
            "DATA_SET_NOT_FOUND",
            "INTERNAL_FAILURE",
            "PARAMETER_VALUE_INCOMPATIBLE",
            "PARAMETER_TYPE_INVALID",
            "PARAMETER_NOT_FOUND",
            "COLUMN_TYPE_MISMATCH",
            "COLUMN_GEOGRAPHIC_ROLE_MISMATCH",
            "COLUMN_REPLACEMENT_MISSING",
        ],
        "Message": str,
    },
    total=False,
)

DashboardSourceTemplateTypeDef = TypedDict(
    "DashboardSourceTemplateTypeDef",
    {"DataSetReferences": List["DataSetReferenceTypeDef"], "Arn": str},
)

DashboardSummaryTypeDef = TypedDict(
    "DashboardSummaryTypeDef",
    {
        "Arn": str,
        "DashboardId": str,
        "Name": str,
        "CreatedTime": datetime,
        "LastUpdatedTime": datetime,
        "PublishedVersionNumber": int,
        "LastPublishedTime": datetime,
    },
    total=False,
)

DashboardTypeDef = TypedDict(
    "DashboardTypeDef",
    {
        "DashboardId": str,
        "Arn": str,
        "Name": str,
        "Version": "DashboardVersionTypeDef",
        "CreatedTime": datetime,
        "LastPublishedTime": datetime,
        "LastUpdatedTime": datetime,
    },
    total=False,
)

DashboardVersionSummaryTypeDef = TypedDict(
    "DashboardVersionSummaryTypeDef",
    {
        "Arn": str,
        "CreatedTime": datetime,
        "VersionNumber": int,
        "Status": Literal[
            "CREATION_IN_PROGRESS",
            "CREATION_SUCCESSFUL",
            "CREATION_FAILED",
            "UPDATE_IN_PROGRESS",
            "UPDATE_SUCCESSFUL",
            "UPDATE_FAILED",
        ],
        "SourceEntityArn": str,
        "Description": str,
    },
    total=False,
)

DashboardVersionTypeDef = TypedDict(
    "DashboardVersionTypeDef",
    {
        "CreatedTime": datetime,
        "Errors": List["DashboardErrorTypeDef"],
        "VersionNumber": int,
        "Status": Literal[
            "CREATION_IN_PROGRESS",
            "CREATION_SUCCESSFUL",
            "CREATION_FAILED",
            "UPDATE_IN_PROGRESS",
            "UPDATE_SUCCESSFUL",
            "UPDATE_FAILED",
        ],
        "Arn": str,
        "SourceEntityArn": str,
        "DataSetArns": List[str],
        "Description": str,
    },
    total=False,
)

DataSetConfigurationTypeDef = TypedDict(
    "DataSetConfigurationTypeDef",
    {
        "Placeholder": str,
        "DataSetSchema": "DataSetSchemaTypeDef",
        "ColumnGroupSchemaList": List["ColumnGroupSchemaTypeDef"],
    },
    total=False,
)

DataSetReferenceTypeDef = TypedDict(
    "DataSetReferenceTypeDef", {"DataSetPlaceholder": str, "DataSetArn": str}
)

DataSetSchemaTypeDef = TypedDict(
    "DataSetSchemaTypeDef", {"ColumnSchemaList": List["ColumnSchemaTypeDef"]}, total=False
)

DataSetSummaryTypeDef = TypedDict(
    "DataSetSummaryTypeDef",
    {
        "Arn": str,
        "DataSetId": str,
        "Name": str,
        "CreatedTime": datetime,
        "LastUpdatedTime": datetime,
        "ImportMode": Literal["SPICE", "DIRECT_QUERY"],
        "RowLevelPermissionDataSet": "RowLevelPermissionDataSetTypeDef",
    },
    total=False,
)

DataSetTypeDef = TypedDict(
    "DataSetTypeDef",
    {
        "Arn": str,
        "DataSetId": str,
        "Name": str,
        "CreatedTime": datetime,
        "LastUpdatedTime": datetime,
        "PhysicalTableMap": Dict[str, "PhysicalTableTypeDef"],
        "LogicalTableMap": Dict[str, "LogicalTableTypeDef"],
        "OutputColumns": List["OutputColumnTypeDef"],
        "ImportMode": Literal["SPICE", "DIRECT_QUERY"],
        "ConsumedSpiceCapacityInBytes": int,
        "ColumnGroups": List["ColumnGroupTypeDef"],
        "RowLevelPermissionDataSet": "RowLevelPermissionDataSetTypeDef",
    },
    total=False,
)

DataSourceErrorInfoTypeDef = TypedDict(
    "DataSourceErrorInfoTypeDef",
    {
        "Type": Literal[
            "TIMEOUT",
            "ENGINE_VERSION_NOT_SUPPORTED",
            "UNKNOWN_HOST",
            "GENERIC_SQL_FAILURE",
            "CONFLICT",
            "UNKNOWN",
        ],
        "Message": str,
    },
    total=False,
)

DataSourceParametersTypeDef = TypedDict(
    "DataSourceParametersTypeDef",
    {
        "AmazonElasticsearchParameters": "AmazonElasticsearchParametersTypeDef",
        "AthenaParameters": "AthenaParametersTypeDef",
        "AuroraParameters": "AuroraParametersTypeDef",
        "AuroraPostgreSqlParameters": "AuroraPostgreSqlParametersTypeDef",
        "AwsIotAnalyticsParameters": "AwsIotAnalyticsParametersTypeDef",
        "JiraParameters": "JiraParametersTypeDef",
        "MariaDbParameters": "MariaDbParametersTypeDef",
        "MySqlParameters": "MySqlParametersTypeDef",
        "PostgreSqlParameters": "PostgreSqlParametersTypeDef",
        "PrestoParameters": "PrestoParametersTypeDef",
        "RdsParameters": "RdsParametersTypeDef",
        "RedshiftParameters": "RedshiftParametersTypeDef",
        "S3Parameters": "S3ParametersTypeDef",
        "ServiceNowParameters": "ServiceNowParametersTypeDef",
        "SnowflakeParameters": "SnowflakeParametersTypeDef",
        "SparkParameters": "SparkParametersTypeDef",
        "SqlServerParameters": "SqlServerParametersTypeDef",
        "TeradataParameters": "TeradataParametersTypeDef",
        "TwitterParameters": "TwitterParametersTypeDef",
    },
    total=False,
)

DataSourceTypeDef = TypedDict(
    "DataSourceTypeDef",
    {
        "Arn": str,
        "DataSourceId": str,
        "Name": str,
        "Type": Literal[
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
        "Status": Literal[
            "CREATION_IN_PROGRESS",
            "CREATION_SUCCESSFUL",
            "CREATION_FAILED",
            "UPDATE_IN_PROGRESS",
            "UPDATE_SUCCESSFUL",
            "UPDATE_FAILED",
        ],
        "CreatedTime": datetime,
        "LastUpdatedTime": datetime,
        "DataSourceParameters": "DataSourceParametersTypeDef",
        "VpcConnectionProperties": "VpcConnectionPropertiesTypeDef",
        "SslProperties": "SslPropertiesTypeDef",
        "ErrorInfo": "DataSourceErrorInfoTypeDef",
    },
    total=False,
)

DateTimeParameterTypeDef = TypedDict(
    "DateTimeParameterTypeDef", {"Name": str, "Values": List[datetime]}
)

DecimalParameterTypeDef = TypedDict("DecimalParameterTypeDef", {"Name": str, "Values": List[float]})

ErrorInfoTypeDef = TypedDict(
    "ErrorInfoTypeDef",
    {
        "Type": Literal[
            "FAILURE_TO_ASSUME_ROLE",
            "INGESTION_SUPERSEDED",
            "INGESTION_CANCELED",
            "DATA_SET_DELETED",
            "DATA_SET_NOT_SPICE",
            "S3_UPLOADED_FILE_DELETED",
            "S3_MANIFEST_ERROR",
            "DATA_TOLERANCE_EXCEPTION",
            "SPICE_TABLE_NOT_FOUND",
            "DATA_SET_SIZE_LIMIT_EXCEEDED",
            "ROW_SIZE_LIMIT_EXCEEDED",
            "ACCOUNT_CAPACITY_LIMIT_EXCEEDED",
            "CUSTOMER_ERROR",
            "DATA_SOURCE_NOT_FOUND",
            "IAM_ROLE_NOT_AVAILABLE",
            "CONNECTION_FAILURE",
            "SQL_TABLE_NOT_FOUND",
            "PERMISSION_DENIED",
            "SSL_CERTIFICATE_VALIDATION_FAILURE",
            "OAUTH_TOKEN_FAILURE",
            "SOURCE_API_LIMIT_EXCEEDED_FAILURE",
            "PASSWORD_AUTHENTICATION_FAILURE",
            "SQL_SCHEMA_MISMATCH_ERROR",
            "INVALID_DATE_FORMAT",
            "INVALID_DATAPREP_SYNTAX",
            "SOURCE_RESOURCE_LIMIT_EXCEEDED",
            "SQL_INVALID_PARAMETER_VALUE",
            "QUERY_TIMEOUT",
            "SQL_NUMERIC_OVERFLOW",
            "UNRESOLVABLE_HOST",
            "UNROUTABLE_HOST",
            "SQL_EXCEPTION",
            "S3_FILE_INACCESSIBLE",
            "IOT_FILE_NOT_FOUND",
            "IOT_DATA_SET_FILE_EMPTY",
            "INVALID_DATA_SOURCE_CONFIG",
            "DATA_SOURCE_AUTH_FAILED",
            "DATA_SOURCE_CONNECTION_FAILED",
            "FAILURE_TO_PROCESS_JSON_FILE",
            "INTERNAL_SERVICE_ERROR",
        ],
        "Message": str,
    },
    total=False,
)

ExportToCSVOptionTypeDef = TypedDict(
    "ExportToCSVOptionTypeDef", {"AvailabilityStatus": Literal["ENABLED", "DISABLED"]}, total=False
)

FilterOperationTypeDef = TypedDict("FilterOperationTypeDef", {"ConditionExpression": str})

GeoSpatialColumnGroupTypeDef = TypedDict(
    "GeoSpatialColumnGroupTypeDef",
    {"Name": str, "CountryCode": Literal["US"], "Columns": List[str]},
)

GroupMemberTypeDef = TypedDict("GroupMemberTypeDef", {"Arn": str, "MemberName": str}, total=False)

GroupTypeDef = TypedDict(
    "GroupTypeDef",
    {"Arn": str, "GroupName": str, "Description": str, "PrincipalId": str},
    total=False,
)

IAMPolicyAssignmentSummaryTypeDef = TypedDict(
    "IAMPolicyAssignmentSummaryTypeDef",
    {"AssignmentName": str, "AssignmentStatus": Literal["ENABLED", "DRAFT", "DISABLED"]},
    total=False,
)

IAMPolicyAssignmentTypeDef = TypedDict(
    "IAMPolicyAssignmentTypeDef",
    {
        "AwsAccountId": str,
        "AssignmentId": str,
        "AssignmentName": str,
        "PolicyArn": str,
        "Identities": Dict[str, List[str]],
        "AssignmentStatus": Literal["ENABLED", "DRAFT", "DISABLED"],
    },
    total=False,
)

_RequiredIngestionTypeDef = TypedDict(
    "_RequiredIngestionTypeDef",
    {
        "Arn": str,
        "IngestionStatus": Literal[
            "INITIALIZED", "QUEUED", "RUNNING", "FAILED", "COMPLETED", "CANCELLED"
        ],
        "CreatedTime": datetime,
    },
)
_OptionalIngestionTypeDef = TypedDict(
    "_OptionalIngestionTypeDef",
    {
        "IngestionId": str,
        "ErrorInfo": "ErrorInfoTypeDef",
        "RowInfo": "RowInfoTypeDef",
        "QueueInfo": "QueueInfoTypeDef",
        "IngestionTimeInSeconds": int,
        "IngestionSizeInBytes": int,
        "RequestSource": Literal["MANUAL", "SCHEDULED"],
        "RequestType": Literal["INITIAL_INGESTION", "EDIT", "INCREMENTAL_REFRESH", "FULL_REFRESH"],
    },
    total=False,
)


class IngestionTypeDef(_RequiredIngestionTypeDef, _OptionalIngestionTypeDef):
    pass


InputColumnTypeDef = TypedDict(
    "InputColumnTypeDef",
    {
        "Name": str,
        "Type": Literal["STRING", "INTEGER", "DECIMAL", "DATETIME", "BIT", "BOOLEAN", "JSON"],
    },
)

IntegerParameterTypeDef = TypedDict("IntegerParameterTypeDef", {"Name": str, "Values": List[int]})

JiraParametersTypeDef = TypedDict("JiraParametersTypeDef", {"SiteBaseUrl": str})

JoinInstructionTypeDef = TypedDict(
    "JoinInstructionTypeDef",
    {
        "LeftOperand": str,
        "RightOperand": str,
        "Type": Literal["INNER", "OUTER", "LEFT", "RIGHT"],
        "OnClause": str,
    },
)

LogicalTableSourceTypeDef = TypedDict(
    "LogicalTableSourceTypeDef",
    {"JoinInstruction": "JoinInstructionTypeDef", "PhysicalTableId": str},
    total=False,
)

_RequiredLogicalTableTypeDef = TypedDict(
    "_RequiredLogicalTableTypeDef", {"Alias": str, "Source": "LogicalTableSourceTypeDef"}
)
_OptionalLogicalTableTypeDef = TypedDict(
    "_OptionalLogicalTableTypeDef",
    {"DataTransforms": List["TransformOperationTypeDef"]},
    total=False,
)


class LogicalTableTypeDef(_RequiredLogicalTableTypeDef, _OptionalLogicalTableTypeDef):
    pass


ManifestFileLocationTypeDef = TypedDict("ManifestFileLocationTypeDef", {"Bucket": str, "Key": str})

MariaDbParametersTypeDef = TypedDict(
    "MariaDbParametersTypeDef", {"Host": str, "Port": int, "Database": str}
)

MySqlParametersTypeDef = TypedDict(
    "MySqlParametersTypeDef", {"Host": str, "Port": int, "Database": str}
)

OutputColumnTypeDef = TypedDict(
    "OutputColumnTypeDef",
    {"Name": str, "Type": Literal["STRING", "INTEGER", "DECIMAL", "DATETIME"]},
    total=False,
)

PhysicalTableTypeDef = TypedDict(
    "PhysicalTableTypeDef",
    {
        "RelationalTable": "RelationalTableTypeDef",
        "CustomSql": "CustomSqlTypeDef",
        "S3Source": "S3SourceTypeDef",
    },
    total=False,
)

PostgreSqlParametersTypeDef = TypedDict(
    "PostgreSqlParametersTypeDef", {"Host": str, "Port": int, "Database": str}
)

PrestoParametersTypeDef = TypedDict(
    "PrestoParametersTypeDef", {"Host": str, "Port": int, "Catalog": str}
)

ProjectOperationTypeDef = TypedDict("ProjectOperationTypeDef", {"ProjectedColumns": List[str]})

QueueInfoTypeDef = TypedDict(
    "QueueInfoTypeDef", {"WaitingOnIngestion": str, "QueuedIngestion": str}
)

RdsParametersTypeDef = TypedDict("RdsParametersTypeDef", {"InstanceId": str, "Database": str})

_RequiredRedshiftParametersTypeDef = TypedDict(
    "_RequiredRedshiftParametersTypeDef", {"Database": str}
)
_OptionalRedshiftParametersTypeDef = TypedDict(
    "_OptionalRedshiftParametersTypeDef", {"Host": str, "Port": int, "ClusterId": str}, total=False
)


class RedshiftParametersTypeDef(
    _RequiredRedshiftParametersTypeDef, _OptionalRedshiftParametersTypeDef
):
    pass


_RequiredRelationalTableTypeDef = TypedDict(
    "_RequiredRelationalTableTypeDef",
    {"DataSourceArn": str, "Name": str, "InputColumns": List["InputColumnTypeDef"]},
)
_OptionalRelationalTableTypeDef = TypedDict(
    "_OptionalRelationalTableTypeDef", {"Schema": str}, total=False
)


class RelationalTableTypeDef(_RequiredRelationalTableTypeDef, _OptionalRelationalTableTypeDef):
    pass


RenameColumnOperationTypeDef = TypedDict(
    "RenameColumnOperationTypeDef", {"ColumnName": str, "NewColumnName": str}
)

ResourcePermissionTypeDef = TypedDict(
    "ResourcePermissionTypeDef", {"Principal": str, "Actions": List[str]}
)

RowInfoTypeDef = TypedDict("RowInfoTypeDef", {"RowsIngested": int, "RowsDropped": int}, total=False)

RowLevelPermissionDataSetTypeDef = TypedDict(
    "RowLevelPermissionDataSetTypeDef",
    {"Arn": str, "PermissionPolicy": Literal["GRANT_ACCESS", "DENY_ACCESS"]},
)

S3ParametersTypeDef = TypedDict(
    "S3ParametersTypeDef", {"ManifestFileLocation": "ManifestFileLocationTypeDef"}
)

_RequiredS3SourceTypeDef = TypedDict(
    "_RequiredS3SourceTypeDef", {"DataSourceArn": str, "InputColumns": List["InputColumnTypeDef"]}
)
_OptionalS3SourceTypeDef = TypedDict(
    "_OptionalS3SourceTypeDef", {"UploadSettings": "UploadSettingsTypeDef"}, total=False
)


class S3SourceTypeDef(_RequiredS3SourceTypeDef, _OptionalS3SourceTypeDef):
    pass


ServiceNowParametersTypeDef = TypedDict("ServiceNowParametersTypeDef", {"SiteBaseUrl": str})

SheetControlsOptionTypeDef = TypedDict(
    "SheetControlsOptionTypeDef", {"VisibilityState": Literal["EXPANDED", "COLLAPSED"]}, total=False
)

SnowflakeParametersTypeDef = TypedDict(
    "SnowflakeParametersTypeDef", {"Host": str, "Database": str, "Warehouse": str}
)

SparkParametersTypeDef = TypedDict("SparkParametersTypeDef", {"Host": str, "Port": int})

SqlServerParametersTypeDef = TypedDict(
    "SqlServerParametersTypeDef", {"Host": str, "Port": int, "Database": str}
)

SslPropertiesTypeDef = TypedDict("SslPropertiesTypeDef", {"DisableSsl": bool}, total=False)

StringParameterTypeDef = TypedDict("StringParameterTypeDef", {"Name": str, "Values": List[str]})

TagColumnOperationTypeDef = TypedDict(
    "TagColumnOperationTypeDef", {"ColumnName": str, "Tags": List["ColumnTagTypeDef"]}
)

TagTypeDef = TypedDict("TagTypeDef", {"Key": str, "Value": str})

TemplateAliasTypeDef = TypedDict(
    "TemplateAliasTypeDef",
    {"AliasName": str, "Arn": str, "TemplateVersionNumber": int},
    total=False,
)

TemplateErrorTypeDef = TypedDict(
    "TemplateErrorTypeDef",
    {"Type": Literal["SOURCE_NOT_FOUND", "DATA_SET_NOT_FOUND", "INTERNAL_FAILURE"], "Message": str},
    total=False,
)

TemplateSourceAnalysisTypeDef = TypedDict(
    "TemplateSourceAnalysisTypeDef",
    {"Arn": str, "DataSetReferences": List["DataSetReferenceTypeDef"]},
)

TemplateSourceTemplateTypeDef = TypedDict("TemplateSourceTemplateTypeDef", {"Arn": str})

TemplateSummaryTypeDef = TypedDict(
    "TemplateSummaryTypeDef",
    {
        "Arn": str,
        "TemplateId": str,
        "Name": str,
        "LatestVersionNumber": int,
        "CreatedTime": datetime,
        "LastUpdatedTime": datetime,
    },
    total=False,
)

TemplateTypeDef = TypedDict(
    "TemplateTypeDef",
    {
        "Arn": str,
        "Name": str,
        "Version": "TemplateVersionTypeDef",
        "TemplateId": str,
        "LastUpdatedTime": datetime,
        "CreatedTime": datetime,
    },
    total=False,
)

TemplateVersionSummaryTypeDef = TypedDict(
    "TemplateVersionSummaryTypeDef",
    {
        "Arn": str,
        "VersionNumber": int,
        "CreatedTime": datetime,
        "Status": Literal[
            "CREATION_IN_PROGRESS",
            "CREATION_SUCCESSFUL",
            "CREATION_FAILED",
            "UPDATE_IN_PROGRESS",
            "UPDATE_SUCCESSFUL",
            "UPDATE_FAILED",
        ],
        "Description": str,
    },
    total=False,
)

TemplateVersionTypeDef = TypedDict(
    "TemplateVersionTypeDef",
    {
        "CreatedTime": datetime,
        "Errors": List["TemplateErrorTypeDef"],
        "VersionNumber": int,
        "Status": Literal[
            "CREATION_IN_PROGRESS",
            "CREATION_SUCCESSFUL",
            "CREATION_FAILED",
            "UPDATE_IN_PROGRESS",
            "UPDATE_SUCCESSFUL",
            "UPDATE_FAILED",
        ],
        "DataSetConfigurations": List["DataSetConfigurationTypeDef"],
        "Description": str,
        "SourceEntityArn": str,
    },
    total=False,
)

TeradataParametersTypeDef = TypedDict(
    "TeradataParametersTypeDef", {"Host": str, "Port": int, "Database": str}
)

TransformOperationTypeDef = TypedDict(
    "TransformOperationTypeDef",
    {
        "ProjectOperation": "ProjectOperationTypeDef",
        "FilterOperation": "FilterOperationTypeDef",
        "CreateColumnsOperation": "CreateColumnsOperationTypeDef",
        "RenameColumnOperation": "RenameColumnOperationTypeDef",
        "CastColumnTypeOperation": "CastColumnTypeOperationTypeDef",
        "TagColumnOperation": "TagColumnOperationTypeDef",
    },
    total=False,
)

TwitterParametersTypeDef = TypedDict("TwitterParametersTypeDef", {"Query": str, "MaxRows": int})

UploadSettingsTypeDef = TypedDict(
    "UploadSettingsTypeDef",
    {
        "Format": Literal["CSV", "TSV", "CLF", "ELF", "XLSX", "JSON"],
        "StartFromRow": int,
        "ContainsHeader": bool,
        "TextQualifier": Literal["DOUBLE_QUOTE", "SINGLE_QUOTE"],
        "Delimiter": str,
    },
    total=False,
)

UserTypeDef = TypedDict(
    "UserTypeDef",
    {
        "Arn": str,
        "UserName": str,
        "Email": str,
        "Role": Literal["ADMIN", "AUTHOR", "READER", "RESTRICTED_AUTHOR", "RESTRICTED_READER"],
        "IdentityType": Literal["IAM", "QUICKSIGHT"],
        "Active": bool,
        "PrincipalId": str,
    },
    total=False,
)

VpcConnectionPropertiesTypeDef = TypedDict(
    "VpcConnectionPropertiesTypeDef", {"VpcConnectionArn": str}
)

CancelIngestionResponseTypeDef = TypedDict(
    "CancelIngestionResponseTypeDef",
    {"Arn": str, "IngestionId": str, "RequestId": str, "Status": int},
    total=False,
)

CreateDashboardResponseTypeDef = TypedDict(
    "CreateDashboardResponseTypeDef",
    {
        "Arn": str,
        "VersionArn": str,
        "DashboardId": str,
        "CreationStatus": Literal[
            "CREATION_IN_PROGRESS",
            "CREATION_SUCCESSFUL",
            "CREATION_FAILED",
            "UPDATE_IN_PROGRESS",
            "UPDATE_SUCCESSFUL",
            "UPDATE_FAILED",
        ],
        "Status": int,
        "RequestId": str,
    },
    total=False,
)

CreateDataSetResponseTypeDef = TypedDict(
    "CreateDataSetResponseTypeDef",
    {
        "Arn": str,
        "DataSetId": str,
        "IngestionArn": str,
        "IngestionId": str,
        "RequestId": str,
        "Status": int,
    },
    total=False,
)

CreateDataSourceResponseTypeDef = TypedDict(
    "CreateDataSourceResponseTypeDef",
    {
        "Arn": str,
        "DataSourceId": str,
        "CreationStatus": Literal[
            "CREATION_IN_PROGRESS",
            "CREATION_SUCCESSFUL",
            "CREATION_FAILED",
            "UPDATE_IN_PROGRESS",
            "UPDATE_SUCCESSFUL",
            "UPDATE_FAILED",
        ],
        "RequestId": str,
        "Status": int,
    },
    total=False,
)

CreateGroupMembershipResponseTypeDef = TypedDict(
    "CreateGroupMembershipResponseTypeDef",
    {"GroupMember": "GroupMemberTypeDef", "RequestId": str, "Status": int},
    total=False,
)

CreateGroupResponseTypeDef = TypedDict(
    "CreateGroupResponseTypeDef",
    {"Group": "GroupTypeDef", "RequestId": str, "Status": int},
    total=False,
)

CreateIAMPolicyAssignmentResponseTypeDef = TypedDict(
    "CreateIAMPolicyAssignmentResponseTypeDef",
    {
        "AssignmentName": str,
        "AssignmentId": str,
        "AssignmentStatus": Literal["ENABLED", "DRAFT", "DISABLED"],
        "PolicyArn": str,
        "Identities": Dict[str, List[str]],
        "RequestId": str,
        "Status": int,
    },
    total=False,
)

CreateIngestionResponseTypeDef = TypedDict(
    "CreateIngestionResponseTypeDef",
    {
        "Arn": str,
        "IngestionId": str,
        "IngestionStatus": Literal[
            "INITIALIZED", "QUEUED", "RUNNING", "FAILED", "COMPLETED", "CANCELLED"
        ],
        "RequestId": str,
        "Status": int,
    },
    total=False,
)

CreateTemplateAliasResponseTypeDef = TypedDict(
    "CreateTemplateAliasResponseTypeDef",
    {"TemplateAlias": "TemplateAliasTypeDef", "Status": int, "RequestId": str},
    total=False,
)

CreateTemplateResponseTypeDef = TypedDict(
    "CreateTemplateResponseTypeDef",
    {
        "Arn": str,
        "VersionArn": str,
        "TemplateId": str,
        "CreationStatus": Literal[
            "CREATION_IN_PROGRESS",
            "CREATION_SUCCESSFUL",
            "CREATION_FAILED",
            "UPDATE_IN_PROGRESS",
            "UPDATE_SUCCESSFUL",
            "UPDATE_FAILED",
        ],
        "Status": int,
        "RequestId": str,
    },
    total=False,
)

DashboardPublishOptionsTypeDef = TypedDict(
    "DashboardPublishOptionsTypeDef",
    {
        "AdHocFilteringOption": "AdHocFilteringOptionTypeDef",
        "ExportToCSVOption": "ExportToCSVOptionTypeDef",
        "SheetControlsOption": "SheetControlsOptionTypeDef",
    },
    total=False,
)

_RequiredDashboardSearchFilterTypeDef = TypedDict(
    "_RequiredDashboardSearchFilterTypeDef", {"Operator": Literal["StringEquals"]}
)
_OptionalDashboardSearchFilterTypeDef = TypedDict(
    "_OptionalDashboardSearchFilterTypeDef",
    {"Name": Literal["QUICKSIGHT_USER"], "Value": str},
    total=False,
)


class DashboardSearchFilterTypeDef(
    _RequiredDashboardSearchFilterTypeDef, _OptionalDashboardSearchFilterTypeDef
):
    pass


DashboardSourceEntityTypeDef = TypedDict(
    "DashboardSourceEntityTypeDef",
    {"SourceTemplate": "DashboardSourceTemplateTypeDef"},
    total=False,
)

DataSourceCredentialsTypeDef = TypedDict(
    "DataSourceCredentialsTypeDef", {"CredentialPair": "CredentialPairTypeDef"}, total=False
)

DeleteDashboardResponseTypeDef = TypedDict(
    "DeleteDashboardResponseTypeDef",
    {"Status": int, "Arn": str, "DashboardId": str, "RequestId": str},
    total=False,
)

DeleteDataSetResponseTypeDef = TypedDict(
    "DeleteDataSetResponseTypeDef",
    {"Arn": str, "DataSetId": str, "RequestId": str, "Status": int},
    total=False,
)

DeleteDataSourceResponseTypeDef = TypedDict(
    "DeleteDataSourceResponseTypeDef",
    {"Arn": str, "DataSourceId": str, "RequestId": str, "Status": int},
    total=False,
)

DeleteGroupMembershipResponseTypeDef = TypedDict(
    "DeleteGroupMembershipResponseTypeDef", {"RequestId": str, "Status": int}, total=False
)

DeleteGroupResponseTypeDef = TypedDict(
    "DeleteGroupResponseTypeDef", {"RequestId": str, "Status": int}, total=False
)

DeleteIAMPolicyAssignmentResponseTypeDef = TypedDict(
    "DeleteIAMPolicyAssignmentResponseTypeDef",
    {"AssignmentName": str, "RequestId": str, "Status": int},
    total=False,
)

DeleteTemplateAliasResponseTypeDef = TypedDict(
    "DeleteTemplateAliasResponseTypeDef",
    {"Status": int, "TemplateId": str, "AliasName": str, "Arn": str, "RequestId": str},
    total=False,
)

DeleteTemplateResponseTypeDef = TypedDict(
    "DeleteTemplateResponseTypeDef",
    {"RequestId": str, "Arn": str, "TemplateId": str, "Status": int},
    total=False,
)

DeleteUserByPrincipalIdResponseTypeDef = TypedDict(
    "DeleteUserByPrincipalIdResponseTypeDef", {"RequestId": str, "Status": int}, total=False
)

DeleteUserResponseTypeDef = TypedDict(
    "DeleteUserResponseTypeDef", {"RequestId": str, "Status": int}, total=False
)

DescribeDashboardPermissionsResponseTypeDef = TypedDict(
    "DescribeDashboardPermissionsResponseTypeDef",
    {
        "DashboardId": str,
        "DashboardArn": str,
        "Permissions": List["ResourcePermissionTypeDef"],
        "Status": int,
        "RequestId": str,
    },
    total=False,
)

DescribeDashboardResponseTypeDef = TypedDict(
    "DescribeDashboardResponseTypeDef",
    {"Dashboard": "DashboardTypeDef", "Status": int, "RequestId": str},
    total=False,
)

DescribeDataSetPermissionsResponseTypeDef = TypedDict(
    "DescribeDataSetPermissionsResponseTypeDef",
    {
        "DataSetArn": str,
        "DataSetId": str,
        "Permissions": List["ResourcePermissionTypeDef"],
        "RequestId": str,
        "Status": int,
    },
    total=False,
)

DescribeDataSetResponseTypeDef = TypedDict(
    "DescribeDataSetResponseTypeDef",
    {"DataSet": "DataSetTypeDef", "RequestId": str, "Status": int},
    total=False,
)

DescribeDataSourcePermissionsResponseTypeDef = TypedDict(
    "DescribeDataSourcePermissionsResponseTypeDef",
    {
        "DataSourceArn": str,
        "DataSourceId": str,
        "Permissions": List["ResourcePermissionTypeDef"],
        "RequestId": str,
        "Status": int,
    },
    total=False,
)

DescribeDataSourceResponseTypeDef = TypedDict(
    "DescribeDataSourceResponseTypeDef",
    {"DataSource": "DataSourceTypeDef", "RequestId": str, "Status": int},
    total=False,
)

DescribeGroupResponseTypeDef = TypedDict(
    "DescribeGroupResponseTypeDef",
    {"Group": "GroupTypeDef", "RequestId": str, "Status": int},
    total=False,
)

DescribeIAMPolicyAssignmentResponseTypeDef = TypedDict(
    "DescribeIAMPolicyAssignmentResponseTypeDef",
    {"IAMPolicyAssignment": "IAMPolicyAssignmentTypeDef", "RequestId": str, "Status": int},
    total=False,
)

DescribeIngestionResponseTypeDef = TypedDict(
    "DescribeIngestionResponseTypeDef",
    {"Ingestion": "IngestionTypeDef", "RequestId": str, "Status": int},
    total=False,
)

DescribeTemplateAliasResponseTypeDef = TypedDict(
    "DescribeTemplateAliasResponseTypeDef",
    {"TemplateAlias": "TemplateAliasTypeDef", "Status": int, "RequestId": str},
    total=False,
)

DescribeTemplatePermissionsResponseTypeDef = TypedDict(
    "DescribeTemplatePermissionsResponseTypeDef",
    {
        "TemplateId": str,
        "TemplateArn": str,
        "Permissions": List["ResourcePermissionTypeDef"],
        "RequestId": str,
        "Status": int,
    },
    total=False,
)

DescribeTemplateResponseTypeDef = TypedDict(
    "DescribeTemplateResponseTypeDef", {"Template": "TemplateTypeDef", "Status": int}, total=False
)

DescribeUserResponseTypeDef = TypedDict(
    "DescribeUserResponseTypeDef",
    {"User": "UserTypeDef", "RequestId": str, "Status": int},
    total=False,
)

GetDashboardEmbedUrlResponseTypeDef = TypedDict(
    "GetDashboardEmbedUrlResponseTypeDef",
    {"EmbedUrl": str, "Status": int, "RequestId": str},
    total=False,
)

ListDashboardVersionsResponseTypeDef = TypedDict(
    "ListDashboardVersionsResponseTypeDef",
    {
        "DashboardVersionSummaryList": List["DashboardVersionSummaryTypeDef"],
        "NextToken": str,
        "Status": int,
        "RequestId": str,
    },
    total=False,
)

ListDashboardsResponseTypeDef = TypedDict(
    "ListDashboardsResponseTypeDef",
    {
        "DashboardSummaryList": List["DashboardSummaryTypeDef"],
        "NextToken": str,
        "Status": int,
        "RequestId": str,
    },
    total=False,
)

ListDataSetsResponseTypeDef = TypedDict(
    "ListDataSetsResponseTypeDef",
    {
        "DataSetSummaries": List["DataSetSummaryTypeDef"],
        "NextToken": str,
        "RequestId": str,
        "Status": int,
    },
    total=False,
)

ListDataSourcesResponseTypeDef = TypedDict(
    "ListDataSourcesResponseTypeDef",
    {"DataSources": List["DataSourceTypeDef"], "NextToken": str, "RequestId": str, "Status": int},
    total=False,
)

ListGroupMembershipsResponseTypeDef = TypedDict(
    "ListGroupMembershipsResponseTypeDef",
    {
        "GroupMemberList": List["GroupMemberTypeDef"],
        "NextToken": str,
        "RequestId": str,
        "Status": int,
    },
    total=False,
)

ListGroupsResponseTypeDef = TypedDict(
    "ListGroupsResponseTypeDef",
    {"GroupList": List["GroupTypeDef"], "NextToken": str, "RequestId": str, "Status": int},
    total=False,
)

ListIAMPolicyAssignmentsForUserResponseTypeDef = TypedDict(
    "ListIAMPolicyAssignmentsForUserResponseTypeDef",
    {
        "ActiveAssignments": List["ActiveIAMPolicyAssignmentTypeDef"],
        "RequestId": str,
        "NextToken": str,
        "Status": int,
    },
    total=False,
)

ListIAMPolicyAssignmentsResponseTypeDef = TypedDict(
    "ListIAMPolicyAssignmentsResponseTypeDef",
    {
        "IAMPolicyAssignments": List["IAMPolicyAssignmentSummaryTypeDef"],
        "NextToken": str,
        "RequestId": str,
        "Status": int,
    },
    total=False,
)

ListIngestionsResponseTypeDef = TypedDict(
    "ListIngestionsResponseTypeDef",
    {"Ingestions": List["IngestionTypeDef"], "NextToken": str, "RequestId": str, "Status": int},
    total=False,
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {"Tags": List["TagTypeDef"], "RequestId": str, "Status": int},
    total=False,
)

ListTemplateAliasesResponseTypeDef = TypedDict(
    "ListTemplateAliasesResponseTypeDef",
    {
        "TemplateAliasList": List["TemplateAliasTypeDef"],
        "Status": int,
        "RequestId": str,
        "NextToken": str,
    },
    total=False,
)

ListTemplateVersionsResponseTypeDef = TypedDict(
    "ListTemplateVersionsResponseTypeDef",
    {
        "TemplateVersionSummaryList": List["TemplateVersionSummaryTypeDef"],
        "NextToken": str,
        "Status": int,
        "RequestId": str,
    },
    total=False,
)

ListTemplatesResponseTypeDef = TypedDict(
    "ListTemplatesResponseTypeDef",
    {
        "TemplateSummaryList": List["TemplateSummaryTypeDef"],
        "NextToken": str,
        "Status": int,
        "RequestId": str,
    },
    total=False,
)

ListUserGroupsResponseTypeDef = TypedDict(
    "ListUserGroupsResponseTypeDef",
    {"GroupList": List["GroupTypeDef"], "NextToken": str, "RequestId": str, "Status": int},
    total=False,
)

ListUsersResponseTypeDef = TypedDict(
    "ListUsersResponseTypeDef",
    {"UserList": List["UserTypeDef"], "NextToken": str, "RequestId": str, "Status": int},
    total=False,
)

ParametersTypeDef = TypedDict(
    "ParametersTypeDef",
    {
        "StringParameters": List["StringParameterTypeDef"],
        "IntegerParameters": List["IntegerParameterTypeDef"],
        "DecimalParameters": List["DecimalParameterTypeDef"],
        "DateTimeParameters": List["DateTimeParameterTypeDef"],
    },
    total=False,
)

RegisterUserResponseTypeDef = TypedDict(
    "RegisterUserResponseTypeDef",
    {"User": "UserTypeDef", "UserInvitationUrl": str, "RequestId": str, "Status": int},
    total=False,
)

SearchDashboardsResponseTypeDef = TypedDict(
    "SearchDashboardsResponseTypeDef",
    {
        "DashboardSummaryList": List["DashboardSummaryTypeDef"],
        "NextToken": str,
        "Status": int,
        "RequestId": str,
    },
    total=False,
)

TagResourceResponseTypeDef = TypedDict(
    "TagResourceResponseTypeDef", {"RequestId": str, "Status": int}, total=False
)

TemplateSourceEntityTypeDef = TypedDict(
    "TemplateSourceEntityTypeDef",
    {
        "SourceAnalysis": "TemplateSourceAnalysisTypeDef",
        "SourceTemplate": "TemplateSourceTemplateTypeDef",
    },
    total=False,
)

UntagResourceResponseTypeDef = TypedDict(
    "UntagResourceResponseTypeDef", {"RequestId": str, "Status": int}, total=False
)

UpdateDashboardPermissionsResponseTypeDef = TypedDict(
    "UpdateDashboardPermissionsResponseTypeDef",
    {
        "DashboardArn": str,
        "DashboardId": str,
        "Permissions": List["ResourcePermissionTypeDef"],
        "RequestId": str,
        "Status": int,
    },
    total=False,
)

UpdateDashboardPublishedVersionResponseTypeDef = TypedDict(
    "UpdateDashboardPublishedVersionResponseTypeDef",
    {"DashboardId": str, "DashboardArn": str, "Status": int, "RequestId": str},
    total=False,
)

UpdateDashboardResponseTypeDef = TypedDict(
    "UpdateDashboardResponseTypeDef",
    {
        "Arn": str,
        "VersionArn": str,
        "DashboardId": str,
        "CreationStatus": Literal[
            "CREATION_IN_PROGRESS",
            "CREATION_SUCCESSFUL",
            "CREATION_FAILED",
            "UPDATE_IN_PROGRESS",
            "UPDATE_SUCCESSFUL",
            "UPDATE_FAILED",
        ],
        "Status": int,
        "RequestId": str,
    },
    total=False,
)

UpdateDataSetPermissionsResponseTypeDef = TypedDict(
    "UpdateDataSetPermissionsResponseTypeDef",
    {"DataSetArn": str, "DataSetId": str, "RequestId": str, "Status": int},
    total=False,
)

UpdateDataSetResponseTypeDef = TypedDict(
    "UpdateDataSetResponseTypeDef",
    {
        "Arn": str,
        "DataSetId": str,
        "IngestionArn": str,
        "IngestionId": str,
        "RequestId": str,
        "Status": int,
    },
    total=False,
)

UpdateDataSourcePermissionsResponseTypeDef = TypedDict(
    "UpdateDataSourcePermissionsResponseTypeDef",
    {"DataSourceArn": str, "DataSourceId": str, "RequestId": str, "Status": int},
    total=False,
)

UpdateDataSourceResponseTypeDef = TypedDict(
    "UpdateDataSourceResponseTypeDef",
    {
        "Arn": str,
        "DataSourceId": str,
        "UpdateStatus": Literal[
            "CREATION_IN_PROGRESS",
            "CREATION_SUCCESSFUL",
            "CREATION_FAILED",
            "UPDATE_IN_PROGRESS",
            "UPDATE_SUCCESSFUL",
            "UPDATE_FAILED",
        ],
        "RequestId": str,
        "Status": int,
    },
    total=False,
)

UpdateGroupResponseTypeDef = TypedDict(
    "UpdateGroupResponseTypeDef",
    {"Group": "GroupTypeDef", "RequestId": str, "Status": int},
    total=False,
)

UpdateIAMPolicyAssignmentResponseTypeDef = TypedDict(
    "UpdateIAMPolicyAssignmentResponseTypeDef",
    {
        "AssignmentName": str,
        "AssignmentId": str,
        "PolicyArn": str,
        "Identities": Dict[str, List[str]],
        "AssignmentStatus": Literal["ENABLED", "DRAFT", "DISABLED"],
        "RequestId": str,
        "Status": int,
    },
    total=False,
)

UpdateTemplateAliasResponseTypeDef = TypedDict(
    "UpdateTemplateAliasResponseTypeDef",
    {"TemplateAlias": "TemplateAliasTypeDef", "Status": int, "RequestId": str},
    total=False,
)

UpdateTemplatePermissionsResponseTypeDef = TypedDict(
    "UpdateTemplatePermissionsResponseTypeDef",
    {
        "TemplateId": str,
        "TemplateArn": str,
        "Permissions": List["ResourcePermissionTypeDef"],
        "RequestId": str,
        "Status": int,
    },
    total=False,
)

UpdateTemplateResponseTypeDef = TypedDict(
    "UpdateTemplateResponseTypeDef",
    {
        "TemplateId": str,
        "Arn": str,
        "VersionArn": str,
        "CreationStatus": Literal[
            "CREATION_IN_PROGRESS",
            "CREATION_SUCCESSFUL",
            "CREATION_FAILED",
            "UPDATE_IN_PROGRESS",
            "UPDATE_SUCCESSFUL",
            "UPDATE_FAILED",
        ],
        "Status": int,
        "RequestId": str,
    },
    total=False,
)

UpdateUserResponseTypeDef = TypedDict(
    "UpdateUserResponseTypeDef",
    {"User": "UserTypeDef", "RequestId": str, "Status": int},
    total=False,
)
