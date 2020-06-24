import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *

from .. import (Duration as _Duration_5170c158, CfnResource as _CfnResource_7760e8e4, Construct as _Construct_f50a3f53, FromCloudFormationOptions as _FromCloudFormationOptions_5f49f6f1, TreeInspector as _TreeInspector_154f5999, TagManager as _TagManager_2508893f, IResolvable as _IResolvable_9ceae33e, IInspectable as _IInspectable_051e6ed8, CfnTag as _CfnTag_b4661f1a, Resource as _Resource_884d0774, RemovalPolicy as _RemovalPolicy_5986e9f3, IResource as _IResource_72f7ee7e, SecretValue as _SecretValue_99478b8b)
from ..aws_ec2 import (Connections as _Connections_231f38b5, ISecurityGroup as _ISecurityGroup_d72ab8e8, InstanceType as _InstanceType_85a97b30, IConnectable as _IConnectable_a587039f, IVpc as _IVpc_3795853f, SubnetSelection as _SubnetSelection_36a13cd6)
from ..aws_kms import (IKey as _IKey_3336c79d)
from ..aws_secretsmanager import (SecretRotation as _SecretRotation_312fb992, SecretAttachmentTargetProps as _SecretAttachmentTargetProps_b948cd13, ISecret as _ISecret_75279d36, Secret as _Secret_01d21232, ISecretAttachmentTarget as _ISecretAttachmentTarget_0a569782)


@jsii.data_type(jsii_type="monocdk-experiment.aws_docdb.BackupProps", jsii_struct_bases=[], name_mapping={'retention': 'retention', 'preferred_window': 'preferredWindow'})
class BackupProps():
    def __init__(self, *, retention: _Duration_5170c158, preferred_window: typing.Optional[str]=None) -> None:
        """Backup configuration for DocumentDB databases.

        :param retention: How many days to retain the backup.
        :param preferred_window: A daily time range in 24-hours UTC format in which backups preferably execute. Must be at least 30 minutes long. Example: '01:00-02:00' Default: - a 30-minute window selected at random from an 8-hour block of time for each AWS Region. To see the time blocks available, see https://docs.aws.amazon.com/documentdb/latest/developerguide/backup-restore.db-cluster-snapshots.html#backup-restore.backup-window

        default
        :default:

        - The retention period for automated backups is 1 day.
          The preferred backup window will be a 30-minute window selected at random
          from an 8-hour block of time for each AWS Region.

        see
        :see: https://docs.aws.amazon.com/documentdb/latest/developerguide/backup-restore.db-cluster-snapshots.html#backup-restore.backup-window
        stability
        :stability: experimental
        """
        self._values = {
            'retention': retention,
        }
        if preferred_window is not None: self._values["preferred_window"] = preferred_window

    @builtins.property
    def retention(self) -> _Duration_5170c158:
        """How many days to retain the backup.

        stability
        :stability: experimental
        """
        return self._values.get('retention')

    @builtins.property
    def preferred_window(self) -> typing.Optional[str]:
        """A daily time range in 24-hours UTC format in which backups preferably execute.

        Must be at least 30 minutes long.

        Example: '01:00-02:00'

        default
        :default:

        - a 30-minute window selected at random from an 8-hour block of
          time for each AWS Region. To see the time blocks available, see
          https://docs.aws.amazon.com/documentdb/latest/developerguide/backup-restore.db-cluster-snapshots.html#backup-restore.backup-window

        stability
        :stability: experimental
        """
        return self._values.get('preferred_window')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BackupProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnDBCluster(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_docdb.CfnDBCluster"):
    """A CloudFormation ``AWS::DocDB::DBCluster``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html
    cloudformationResource:
    :cloudformationResource:: AWS::DocDB::DBCluster
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, master_username: str, master_user_password: str, availability_zones: typing.Optional[typing.List[str]]=None, backup_retention_period: typing.Optional[jsii.Number]=None, db_cluster_identifier: typing.Optional[str]=None, db_cluster_parameter_group_name: typing.Optional[str]=None, db_subnet_group_name: typing.Optional[str]=None, deletion_protection: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, enable_cloudwatch_logs_exports: typing.Optional[typing.List[str]]=None, engine_version: typing.Optional[str]=None, kms_key_id: typing.Optional[str]=None, port: typing.Optional[jsii.Number]=None, preferred_backup_window: typing.Optional[str]=None, preferred_maintenance_window: typing.Optional[str]=None, snapshot_identifier: typing.Optional[str]=None, storage_encrypted: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None, vpc_security_group_ids: typing.Optional[typing.List[str]]=None) -> None:
        """Create a new ``AWS::DocDB::DBCluster``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param master_username: ``AWS::DocDB::DBCluster.MasterUsername``.
        :param master_user_password: ``AWS::DocDB::DBCluster.MasterUserPassword``.
        :param availability_zones: ``AWS::DocDB::DBCluster.AvailabilityZones``.
        :param backup_retention_period: ``AWS::DocDB::DBCluster.BackupRetentionPeriod``.
        :param db_cluster_identifier: ``AWS::DocDB::DBCluster.DBClusterIdentifier``.
        :param db_cluster_parameter_group_name: ``AWS::DocDB::DBCluster.DBClusterParameterGroupName``.
        :param db_subnet_group_name: ``AWS::DocDB::DBCluster.DBSubnetGroupName``.
        :param deletion_protection: ``AWS::DocDB::DBCluster.DeletionProtection``.
        :param enable_cloudwatch_logs_exports: ``AWS::DocDB::DBCluster.EnableCloudwatchLogsExports``.
        :param engine_version: ``AWS::DocDB::DBCluster.EngineVersion``.
        :param kms_key_id: ``AWS::DocDB::DBCluster.KmsKeyId``.
        :param port: ``AWS::DocDB::DBCluster.Port``.
        :param preferred_backup_window: ``AWS::DocDB::DBCluster.PreferredBackupWindow``.
        :param preferred_maintenance_window: ``AWS::DocDB::DBCluster.PreferredMaintenanceWindow``.
        :param snapshot_identifier: ``AWS::DocDB::DBCluster.SnapshotIdentifier``.
        :param storage_encrypted: ``AWS::DocDB::DBCluster.StorageEncrypted``.
        :param tags: ``AWS::DocDB::DBCluster.Tags``.
        :param vpc_security_group_ids: ``AWS::DocDB::DBCluster.VpcSecurityGroupIds``.
        """
        props = CfnDBClusterProps(master_username=master_username, master_user_password=master_user_password, availability_zones=availability_zones, backup_retention_period=backup_retention_period, db_cluster_identifier=db_cluster_identifier, db_cluster_parameter_group_name=db_cluster_parameter_group_name, db_subnet_group_name=db_subnet_group_name, deletion_protection=deletion_protection, enable_cloudwatch_logs_exports=enable_cloudwatch_logs_exports, engine_version=engine_version, kms_key_id=kms_key_id, port=port, preferred_backup_window=preferred_backup_window, preferred_maintenance_window=preferred_maintenance_window, snapshot_identifier=snapshot_identifier, storage_encrypted=storage_encrypted, tags=tags, vpc_security_group_ids=vpc_security_group_ids)

        jsii.create(CfnDBCluster, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnDBCluster":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = _FromCloudFormationOptions_5f49f6f1(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_154f5999) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="attrClusterResourceId")
    def attr_cluster_resource_id(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: ClusterResourceId
        """
        return jsii.get(self, "attrClusterResourceId")

    @builtins.property
    @jsii.member(jsii_name="attrEndpoint")
    def attr_endpoint(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Endpoint
        """
        return jsii.get(self, "attrEndpoint")

    @builtins.property
    @jsii.member(jsii_name="attrPort")
    def attr_port(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Port
        """
        return jsii.get(self, "attrPort")

    @builtins.property
    @jsii.member(jsii_name="attrReadEndpoint")
    def attr_read_endpoint(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: ReadEndpoint
        """
        return jsii.get(self, "attrReadEndpoint")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::DocDB::DBCluster.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="masterUsername")
    def master_username(self) -> str:
        """``AWS::DocDB::DBCluster.MasterUsername``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-masterusername
        """
        return jsii.get(self, "masterUsername")

    @master_username.setter
    def master_username(self, value: str) -> None:
        jsii.set(self, "masterUsername", value)

    @builtins.property
    @jsii.member(jsii_name="masterUserPassword")
    def master_user_password(self) -> str:
        """``AWS::DocDB::DBCluster.MasterUserPassword``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-masteruserpassword
        """
        return jsii.get(self, "masterUserPassword")

    @master_user_password.setter
    def master_user_password(self, value: str) -> None:
        jsii.set(self, "masterUserPassword", value)

    @builtins.property
    @jsii.member(jsii_name="availabilityZones")
    def availability_zones(self) -> typing.Optional[typing.List[str]]:
        """``AWS::DocDB::DBCluster.AvailabilityZones``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-availabilityzones
        """
        return jsii.get(self, "availabilityZones")

    @availability_zones.setter
    def availability_zones(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "availabilityZones", value)

    @builtins.property
    @jsii.member(jsii_name="backupRetentionPeriod")
    def backup_retention_period(self) -> typing.Optional[jsii.Number]:
        """``AWS::DocDB::DBCluster.BackupRetentionPeriod``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-backupretentionperiod
        """
        return jsii.get(self, "backupRetentionPeriod")

    @backup_retention_period.setter
    def backup_retention_period(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "backupRetentionPeriod", value)

    @builtins.property
    @jsii.member(jsii_name="dbClusterIdentifier")
    def db_cluster_identifier(self) -> typing.Optional[str]:
        """``AWS::DocDB::DBCluster.DBClusterIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-dbclusteridentifier
        """
        return jsii.get(self, "dbClusterIdentifier")

    @db_cluster_identifier.setter
    def db_cluster_identifier(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "dbClusterIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="dbClusterParameterGroupName")
    def db_cluster_parameter_group_name(self) -> typing.Optional[str]:
        """``AWS::DocDB::DBCluster.DBClusterParameterGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-dbclusterparametergroupname
        """
        return jsii.get(self, "dbClusterParameterGroupName")

    @db_cluster_parameter_group_name.setter
    def db_cluster_parameter_group_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "dbClusterParameterGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="dbSubnetGroupName")
    def db_subnet_group_name(self) -> typing.Optional[str]:
        """``AWS::DocDB::DBCluster.DBSubnetGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-dbsubnetgroupname
        """
        return jsii.get(self, "dbSubnetGroupName")

    @db_subnet_group_name.setter
    def db_subnet_group_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "dbSubnetGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="deletionProtection")
    def deletion_protection(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::DocDB::DBCluster.DeletionProtection``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-deletionprotection
        """
        return jsii.get(self, "deletionProtection")

    @deletion_protection.setter
    def deletion_protection(self, value: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "deletionProtection", value)

    @builtins.property
    @jsii.member(jsii_name="enableCloudwatchLogsExports")
    def enable_cloudwatch_logs_exports(self) -> typing.Optional[typing.List[str]]:
        """``AWS::DocDB::DBCluster.EnableCloudwatchLogsExports``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-enablecloudwatchlogsexports
        """
        return jsii.get(self, "enableCloudwatchLogsExports")

    @enable_cloudwatch_logs_exports.setter
    def enable_cloudwatch_logs_exports(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "enableCloudwatchLogsExports", value)

    @builtins.property
    @jsii.member(jsii_name="engineVersion")
    def engine_version(self) -> typing.Optional[str]:
        """``AWS::DocDB::DBCluster.EngineVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-engineversion
        """
        return jsii.get(self, "engineVersion")

    @engine_version.setter
    def engine_version(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "engineVersion", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> typing.Optional[str]:
        """``AWS::DocDB::DBCluster.KmsKeyId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-kmskeyid
        """
        return jsii.get(self, "kmsKeyId")

    @kms_key_id.setter
    def kms_key_id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "kmsKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> typing.Optional[jsii.Number]:
        """``AWS::DocDB::DBCluster.Port``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-port
        """
        return jsii.get(self, "port")

    @port.setter
    def port(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "port", value)

    @builtins.property
    @jsii.member(jsii_name="preferredBackupWindow")
    def preferred_backup_window(self) -> typing.Optional[str]:
        """``AWS::DocDB::DBCluster.PreferredBackupWindow``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-preferredbackupwindow
        """
        return jsii.get(self, "preferredBackupWindow")

    @preferred_backup_window.setter
    def preferred_backup_window(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "preferredBackupWindow", value)

    @builtins.property
    @jsii.member(jsii_name="preferredMaintenanceWindow")
    def preferred_maintenance_window(self) -> typing.Optional[str]:
        """``AWS::DocDB::DBCluster.PreferredMaintenanceWindow``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-preferredmaintenancewindow
        """
        return jsii.get(self, "preferredMaintenanceWindow")

    @preferred_maintenance_window.setter
    def preferred_maintenance_window(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "preferredMaintenanceWindow", value)

    @builtins.property
    @jsii.member(jsii_name="snapshotIdentifier")
    def snapshot_identifier(self) -> typing.Optional[str]:
        """``AWS::DocDB::DBCluster.SnapshotIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-snapshotidentifier
        """
        return jsii.get(self, "snapshotIdentifier")

    @snapshot_identifier.setter
    def snapshot_identifier(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "snapshotIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="storageEncrypted")
    def storage_encrypted(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::DocDB::DBCluster.StorageEncrypted``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-storageencrypted
        """
        return jsii.get(self, "storageEncrypted")

    @storage_encrypted.setter
    def storage_encrypted(self, value: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "storageEncrypted", value)

    @builtins.property
    @jsii.member(jsii_name="vpcSecurityGroupIds")
    def vpc_security_group_ids(self) -> typing.Optional[typing.List[str]]:
        """``AWS::DocDB::DBCluster.VpcSecurityGroupIds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-vpcsecuritygroupids
        """
        return jsii.get(self, "vpcSecurityGroupIds")

    @vpc_security_group_ids.setter
    def vpc_security_group_ids(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "vpcSecurityGroupIds", value)


@jsii.implements(_IInspectable_051e6ed8)
class CfnDBClusterParameterGroup(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_docdb.CfnDBClusterParameterGroup"):
    """A CloudFormation ``AWS::DocDB::DBClusterParameterGroup``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbclusterparametergroup.html
    cloudformationResource:
    :cloudformationResource:: AWS::DocDB::DBClusterParameterGroup
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, description: str, family: str, parameters: typing.Any, name: typing.Optional[str]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None) -> None:
        """Create a new ``AWS::DocDB::DBClusterParameterGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: ``AWS::DocDB::DBClusterParameterGroup.Description``.
        :param family: ``AWS::DocDB::DBClusterParameterGroup.Family``.
        :param parameters: ``AWS::DocDB::DBClusterParameterGroup.Parameters``.
        :param name: ``AWS::DocDB::DBClusterParameterGroup.Name``.
        :param tags: ``AWS::DocDB::DBClusterParameterGroup.Tags``.
        """
        props = CfnDBClusterParameterGroupProps(description=description, family=family, parameters=parameters, name=name, tags=tags)

        jsii.create(CfnDBClusterParameterGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnDBClusterParameterGroup":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = _FromCloudFormationOptions_5f49f6f1(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_154f5999) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::DocDB::DBClusterParameterGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbclusterparametergroup.html#cfn-docdb-dbclusterparametergroup-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> str:
        """``AWS::DocDB::DBClusterParameterGroup.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbclusterparametergroup.html#cfn-docdb-dbclusterparametergroup-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: str) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="family")
    def family(self) -> str:
        """``AWS::DocDB::DBClusterParameterGroup.Family``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbclusterparametergroup.html#cfn-docdb-dbclusterparametergroup-family
        """
        return jsii.get(self, "family")

    @family.setter
    def family(self, value: str) -> None:
        jsii.set(self, "family", value)

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Any:
        """``AWS::DocDB::DBClusterParameterGroup.Parameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbclusterparametergroup.html#cfn-docdb-dbclusterparametergroup-parameters
        """
        return jsii.get(self, "parameters")

    @parameters.setter
    def parameters(self, value: typing.Any) -> None:
        jsii.set(self, "parameters", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[str]:
        """``AWS::DocDB::DBClusterParameterGroup.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbclusterparametergroup.html#cfn-docdb-dbclusterparametergroup-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "name", value)


@jsii.data_type(jsii_type="monocdk-experiment.aws_docdb.CfnDBClusterParameterGroupProps", jsii_struct_bases=[], name_mapping={'description': 'description', 'family': 'family', 'parameters': 'parameters', 'name': 'name', 'tags': 'tags'})
class CfnDBClusterParameterGroupProps():
    def __init__(self, *, description: str, family: str, parameters: typing.Any, name: typing.Optional[str]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None) -> None:
        """Properties for defining a ``AWS::DocDB::DBClusterParameterGroup``.

        :param description: ``AWS::DocDB::DBClusterParameterGroup.Description``.
        :param family: ``AWS::DocDB::DBClusterParameterGroup.Family``.
        :param parameters: ``AWS::DocDB::DBClusterParameterGroup.Parameters``.
        :param name: ``AWS::DocDB::DBClusterParameterGroup.Name``.
        :param tags: ``AWS::DocDB::DBClusterParameterGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbclusterparametergroup.html
        """
        self._values = {
            'description': description,
            'family': family,
            'parameters': parameters,
        }
        if name is not None: self._values["name"] = name
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def description(self) -> str:
        """``AWS::DocDB::DBClusterParameterGroup.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbclusterparametergroup.html#cfn-docdb-dbclusterparametergroup-description
        """
        return self._values.get('description')

    @builtins.property
    def family(self) -> str:
        """``AWS::DocDB::DBClusterParameterGroup.Family``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbclusterparametergroup.html#cfn-docdb-dbclusterparametergroup-family
        """
        return self._values.get('family')

    @builtins.property
    def parameters(self) -> typing.Any:
        """``AWS::DocDB::DBClusterParameterGroup.Parameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbclusterparametergroup.html#cfn-docdb-dbclusterparametergroup-parameters
        """
        return self._values.get('parameters')

    @builtins.property
    def name(self) -> typing.Optional[str]:
        """``AWS::DocDB::DBClusterParameterGroup.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbclusterparametergroup.html#cfn-docdb-dbclusterparametergroup-name
        """
        return self._values.get('name')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_b4661f1a]]:
        """``AWS::DocDB::DBClusterParameterGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbclusterparametergroup.html#cfn-docdb-dbclusterparametergroup-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnDBClusterParameterGroupProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_docdb.CfnDBClusterProps", jsii_struct_bases=[], name_mapping={'master_username': 'masterUsername', 'master_user_password': 'masterUserPassword', 'availability_zones': 'availabilityZones', 'backup_retention_period': 'backupRetentionPeriod', 'db_cluster_identifier': 'dbClusterIdentifier', 'db_cluster_parameter_group_name': 'dbClusterParameterGroupName', 'db_subnet_group_name': 'dbSubnetGroupName', 'deletion_protection': 'deletionProtection', 'enable_cloudwatch_logs_exports': 'enableCloudwatchLogsExports', 'engine_version': 'engineVersion', 'kms_key_id': 'kmsKeyId', 'port': 'port', 'preferred_backup_window': 'preferredBackupWindow', 'preferred_maintenance_window': 'preferredMaintenanceWindow', 'snapshot_identifier': 'snapshotIdentifier', 'storage_encrypted': 'storageEncrypted', 'tags': 'tags', 'vpc_security_group_ids': 'vpcSecurityGroupIds'})
class CfnDBClusterProps():
    def __init__(self, *, master_username: str, master_user_password: str, availability_zones: typing.Optional[typing.List[str]]=None, backup_retention_period: typing.Optional[jsii.Number]=None, db_cluster_identifier: typing.Optional[str]=None, db_cluster_parameter_group_name: typing.Optional[str]=None, db_subnet_group_name: typing.Optional[str]=None, deletion_protection: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, enable_cloudwatch_logs_exports: typing.Optional[typing.List[str]]=None, engine_version: typing.Optional[str]=None, kms_key_id: typing.Optional[str]=None, port: typing.Optional[jsii.Number]=None, preferred_backup_window: typing.Optional[str]=None, preferred_maintenance_window: typing.Optional[str]=None, snapshot_identifier: typing.Optional[str]=None, storage_encrypted: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None, vpc_security_group_ids: typing.Optional[typing.List[str]]=None) -> None:
        """Properties for defining a ``AWS::DocDB::DBCluster``.

        :param master_username: ``AWS::DocDB::DBCluster.MasterUsername``.
        :param master_user_password: ``AWS::DocDB::DBCluster.MasterUserPassword``.
        :param availability_zones: ``AWS::DocDB::DBCluster.AvailabilityZones``.
        :param backup_retention_period: ``AWS::DocDB::DBCluster.BackupRetentionPeriod``.
        :param db_cluster_identifier: ``AWS::DocDB::DBCluster.DBClusterIdentifier``.
        :param db_cluster_parameter_group_name: ``AWS::DocDB::DBCluster.DBClusterParameterGroupName``.
        :param db_subnet_group_name: ``AWS::DocDB::DBCluster.DBSubnetGroupName``.
        :param deletion_protection: ``AWS::DocDB::DBCluster.DeletionProtection``.
        :param enable_cloudwatch_logs_exports: ``AWS::DocDB::DBCluster.EnableCloudwatchLogsExports``.
        :param engine_version: ``AWS::DocDB::DBCluster.EngineVersion``.
        :param kms_key_id: ``AWS::DocDB::DBCluster.KmsKeyId``.
        :param port: ``AWS::DocDB::DBCluster.Port``.
        :param preferred_backup_window: ``AWS::DocDB::DBCluster.PreferredBackupWindow``.
        :param preferred_maintenance_window: ``AWS::DocDB::DBCluster.PreferredMaintenanceWindow``.
        :param snapshot_identifier: ``AWS::DocDB::DBCluster.SnapshotIdentifier``.
        :param storage_encrypted: ``AWS::DocDB::DBCluster.StorageEncrypted``.
        :param tags: ``AWS::DocDB::DBCluster.Tags``.
        :param vpc_security_group_ids: ``AWS::DocDB::DBCluster.VpcSecurityGroupIds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html
        """
        self._values = {
            'master_username': master_username,
            'master_user_password': master_user_password,
        }
        if availability_zones is not None: self._values["availability_zones"] = availability_zones
        if backup_retention_period is not None: self._values["backup_retention_period"] = backup_retention_period
        if db_cluster_identifier is not None: self._values["db_cluster_identifier"] = db_cluster_identifier
        if db_cluster_parameter_group_name is not None: self._values["db_cluster_parameter_group_name"] = db_cluster_parameter_group_name
        if db_subnet_group_name is not None: self._values["db_subnet_group_name"] = db_subnet_group_name
        if deletion_protection is not None: self._values["deletion_protection"] = deletion_protection
        if enable_cloudwatch_logs_exports is not None: self._values["enable_cloudwatch_logs_exports"] = enable_cloudwatch_logs_exports
        if engine_version is not None: self._values["engine_version"] = engine_version
        if kms_key_id is not None: self._values["kms_key_id"] = kms_key_id
        if port is not None: self._values["port"] = port
        if preferred_backup_window is not None: self._values["preferred_backup_window"] = preferred_backup_window
        if preferred_maintenance_window is not None: self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if snapshot_identifier is not None: self._values["snapshot_identifier"] = snapshot_identifier
        if storage_encrypted is not None: self._values["storage_encrypted"] = storage_encrypted
        if tags is not None: self._values["tags"] = tags
        if vpc_security_group_ids is not None: self._values["vpc_security_group_ids"] = vpc_security_group_ids

    @builtins.property
    def master_username(self) -> str:
        """``AWS::DocDB::DBCluster.MasterUsername``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-masterusername
        """
        return self._values.get('master_username')

    @builtins.property
    def master_user_password(self) -> str:
        """``AWS::DocDB::DBCluster.MasterUserPassword``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-masteruserpassword
        """
        return self._values.get('master_user_password')

    @builtins.property
    def availability_zones(self) -> typing.Optional[typing.List[str]]:
        """``AWS::DocDB::DBCluster.AvailabilityZones``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-availabilityzones
        """
        return self._values.get('availability_zones')

    @builtins.property
    def backup_retention_period(self) -> typing.Optional[jsii.Number]:
        """``AWS::DocDB::DBCluster.BackupRetentionPeriod``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-backupretentionperiod
        """
        return self._values.get('backup_retention_period')

    @builtins.property
    def db_cluster_identifier(self) -> typing.Optional[str]:
        """``AWS::DocDB::DBCluster.DBClusterIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-dbclusteridentifier
        """
        return self._values.get('db_cluster_identifier')

    @builtins.property
    def db_cluster_parameter_group_name(self) -> typing.Optional[str]:
        """``AWS::DocDB::DBCluster.DBClusterParameterGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-dbclusterparametergroupname
        """
        return self._values.get('db_cluster_parameter_group_name')

    @builtins.property
    def db_subnet_group_name(self) -> typing.Optional[str]:
        """``AWS::DocDB::DBCluster.DBSubnetGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-dbsubnetgroupname
        """
        return self._values.get('db_subnet_group_name')

    @builtins.property
    def deletion_protection(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::DocDB::DBCluster.DeletionProtection``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-deletionprotection
        """
        return self._values.get('deletion_protection')

    @builtins.property
    def enable_cloudwatch_logs_exports(self) -> typing.Optional[typing.List[str]]:
        """``AWS::DocDB::DBCluster.EnableCloudwatchLogsExports``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-enablecloudwatchlogsexports
        """
        return self._values.get('enable_cloudwatch_logs_exports')

    @builtins.property
    def engine_version(self) -> typing.Optional[str]:
        """``AWS::DocDB::DBCluster.EngineVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-engineversion
        """
        return self._values.get('engine_version')

    @builtins.property
    def kms_key_id(self) -> typing.Optional[str]:
        """``AWS::DocDB::DBCluster.KmsKeyId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-kmskeyid
        """
        return self._values.get('kms_key_id')

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        """``AWS::DocDB::DBCluster.Port``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-port
        """
        return self._values.get('port')

    @builtins.property
    def preferred_backup_window(self) -> typing.Optional[str]:
        """``AWS::DocDB::DBCluster.PreferredBackupWindow``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-preferredbackupwindow
        """
        return self._values.get('preferred_backup_window')

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[str]:
        """``AWS::DocDB::DBCluster.PreferredMaintenanceWindow``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-preferredmaintenancewindow
        """
        return self._values.get('preferred_maintenance_window')

    @builtins.property
    def snapshot_identifier(self) -> typing.Optional[str]:
        """``AWS::DocDB::DBCluster.SnapshotIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-snapshotidentifier
        """
        return self._values.get('snapshot_identifier')

    @builtins.property
    def storage_encrypted(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::DocDB::DBCluster.StorageEncrypted``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-storageencrypted
        """
        return self._values.get('storage_encrypted')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_b4661f1a]]:
        """``AWS::DocDB::DBCluster.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-tags
        """
        return self._values.get('tags')

    @builtins.property
    def vpc_security_group_ids(self) -> typing.Optional[typing.List[str]]:
        """``AWS::DocDB::DBCluster.VpcSecurityGroupIds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbcluster.html#cfn-docdb-dbcluster-vpcsecuritygroupids
        """
        return self._values.get('vpc_security_group_ids')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnDBClusterProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnDBInstance(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_docdb.CfnDBInstance"):
    """A CloudFormation ``AWS::DocDB::DBInstance``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbinstance.html
    cloudformationResource:
    :cloudformationResource:: AWS::DocDB::DBInstance
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, db_cluster_identifier: str, db_instance_class: str, auto_minor_version_upgrade: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, availability_zone: typing.Optional[str]=None, db_instance_identifier: typing.Optional[str]=None, preferred_maintenance_window: typing.Optional[str]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None) -> None:
        """Create a new ``AWS::DocDB::DBInstance``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param db_cluster_identifier: ``AWS::DocDB::DBInstance.DBClusterIdentifier``.
        :param db_instance_class: ``AWS::DocDB::DBInstance.DBInstanceClass``.
        :param auto_minor_version_upgrade: ``AWS::DocDB::DBInstance.AutoMinorVersionUpgrade``.
        :param availability_zone: ``AWS::DocDB::DBInstance.AvailabilityZone``.
        :param db_instance_identifier: ``AWS::DocDB::DBInstance.DBInstanceIdentifier``.
        :param preferred_maintenance_window: ``AWS::DocDB::DBInstance.PreferredMaintenanceWindow``.
        :param tags: ``AWS::DocDB::DBInstance.Tags``.
        """
        props = CfnDBInstanceProps(db_cluster_identifier=db_cluster_identifier, db_instance_class=db_instance_class, auto_minor_version_upgrade=auto_minor_version_upgrade, availability_zone=availability_zone, db_instance_identifier=db_instance_identifier, preferred_maintenance_window=preferred_maintenance_window, tags=tags)

        jsii.create(CfnDBInstance, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnDBInstance":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = _FromCloudFormationOptions_5f49f6f1(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_154f5999) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="attrEndpoint")
    def attr_endpoint(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Endpoint
        """
        return jsii.get(self, "attrEndpoint")

    @builtins.property
    @jsii.member(jsii_name="attrPort")
    def attr_port(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Port
        """
        return jsii.get(self, "attrPort")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::DocDB::DBInstance.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbinstance.html#cfn-docdb-dbinstance-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="dbClusterIdentifier")
    def db_cluster_identifier(self) -> str:
        """``AWS::DocDB::DBInstance.DBClusterIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbinstance.html#cfn-docdb-dbinstance-dbclusteridentifier
        """
        return jsii.get(self, "dbClusterIdentifier")

    @db_cluster_identifier.setter
    def db_cluster_identifier(self, value: str) -> None:
        jsii.set(self, "dbClusterIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="dbInstanceClass")
    def db_instance_class(self) -> str:
        """``AWS::DocDB::DBInstance.DBInstanceClass``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbinstance.html#cfn-docdb-dbinstance-dbinstanceclass
        """
        return jsii.get(self, "dbInstanceClass")

    @db_instance_class.setter
    def db_instance_class(self, value: str) -> None:
        jsii.set(self, "dbInstanceClass", value)

    @builtins.property
    @jsii.member(jsii_name="autoMinorVersionUpgrade")
    def auto_minor_version_upgrade(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::DocDB::DBInstance.AutoMinorVersionUpgrade``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbinstance.html#cfn-docdb-dbinstance-autominorversionupgrade
        """
        return jsii.get(self, "autoMinorVersionUpgrade")

    @auto_minor_version_upgrade.setter
    def auto_minor_version_upgrade(self, value: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "autoMinorVersionUpgrade", value)

    @builtins.property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> typing.Optional[str]:
        """``AWS::DocDB::DBInstance.AvailabilityZone``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbinstance.html#cfn-docdb-dbinstance-availabilityzone
        """
        return jsii.get(self, "availabilityZone")

    @availability_zone.setter
    def availability_zone(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "availabilityZone", value)

    @builtins.property
    @jsii.member(jsii_name="dbInstanceIdentifier")
    def db_instance_identifier(self) -> typing.Optional[str]:
        """``AWS::DocDB::DBInstance.DBInstanceIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbinstance.html#cfn-docdb-dbinstance-dbinstanceidentifier
        """
        return jsii.get(self, "dbInstanceIdentifier")

    @db_instance_identifier.setter
    def db_instance_identifier(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "dbInstanceIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="preferredMaintenanceWindow")
    def preferred_maintenance_window(self) -> typing.Optional[str]:
        """``AWS::DocDB::DBInstance.PreferredMaintenanceWindow``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbinstance.html#cfn-docdb-dbinstance-preferredmaintenancewindow
        """
        return jsii.get(self, "preferredMaintenanceWindow")

    @preferred_maintenance_window.setter
    def preferred_maintenance_window(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "preferredMaintenanceWindow", value)


@jsii.data_type(jsii_type="monocdk-experiment.aws_docdb.CfnDBInstanceProps", jsii_struct_bases=[], name_mapping={'db_cluster_identifier': 'dbClusterIdentifier', 'db_instance_class': 'dbInstanceClass', 'auto_minor_version_upgrade': 'autoMinorVersionUpgrade', 'availability_zone': 'availabilityZone', 'db_instance_identifier': 'dbInstanceIdentifier', 'preferred_maintenance_window': 'preferredMaintenanceWindow', 'tags': 'tags'})
class CfnDBInstanceProps():
    def __init__(self, *, db_cluster_identifier: str, db_instance_class: str, auto_minor_version_upgrade: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, availability_zone: typing.Optional[str]=None, db_instance_identifier: typing.Optional[str]=None, preferred_maintenance_window: typing.Optional[str]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None) -> None:
        """Properties for defining a ``AWS::DocDB::DBInstance``.

        :param db_cluster_identifier: ``AWS::DocDB::DBInstance.DBClusterIdentifier``.
        :param db_instance_class: ``AWS::DocDB::DBInstance.DBInstanceClass``.
        :param auto_minor_version_upgrade: ``AWS::DocDB::DBInstance.AutoMinorVersionUpgrade``.
        :param availability_zone: ``AWS::DocDB::DBInstance.AvailabilityZone``.
        :param db_instance_identifier: ``AWS::DocDB::DBInstance.DBInstanceIdentifier``.
        :param preferred_maintenance_window: ``AWS::DocDB::DBInstance.PreferredMaintenanceWindow``.
        :param tags: ``AWS::DocDB::DBInstance.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbinstance.html
        """
        self._values = {
            'db_cluster_identifier': db_cluster_identifier,
            'db_instance_class': db_instance_class,
        }
        if auto_minor_version_upgrade is not None: self._values["auto_minor_version_upgrade"] = auto_minor_version_upgrade
        if availability_zone is not None: self._values["availability_zone"] = availability_zone
        if db_instance_identifier is not None: self._values["db_instance_identifier"] = db_instance_identifier
        if preferred_maintenance_window is not None: self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def db_cluster_identifier(self) -> str:
        """``AWS::DocDB::DBInstance.DBClusterIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbinstance.html#cfn-docdb-dbinstance-dbclusteridentifier
        """
        return self._values.get('db_cluster_identifier')

    @builtins.property
    def db_instance_class(self) -> str:
        """``AWS::DocDB::DBInstance.DBInstanceClass``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbinstance.html#cfn-docdb-dbinstance-dbinstanceclass
        """
        return self._values.get('db_instance_class')

    @builtins.property
    def auto_minor_version_upgrade(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::DocDB::DBInstance.AutoMinorVersionUpgrade``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbinstance.html#cfn-docdb-dbinstance-autominorversionupgrade
        """
        return self._values.get('auto_minor_version_upgrade')

    @builtins.property
    def availability_zone(self) -> typing.Optional[str]:
        """``AWS::DocDB::DBInstance.AvailabilityZone``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbinstance.html#cfn-docdb-dbinstance-availabilityzone
        """
        return self._values.get('availability_zone')

    @builtins.property
    def db_instance_identifier(self) -> typing.Optional[str]:
        """``AWS::DocDB::DBInstance.DBInstanceIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbinstance.html#cfn-docdb-dbinstance-dbinstanceidentifier
        """
        return self._values.get('db_instance_identifier')

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[str]:
        """``AWS::DocDB::DBInstance.PreferredMaintenanceWindow``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbinstance.html#cfn-docdb-dbinstance-preferredmaintenancewindow
        """
        return self._values.get('preferred_maintenance_window')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_b4661f1a]]:
        """``AWS::DocDB::DBInstance.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbinstance.html#cfn-docdb-dbinstance-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnDBInstanceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnDBSubnetGroup(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_docdb.CfnDBSubnetGroup"):
    """A CloudFormation ``AWS::DocDB::DBSubnetGroup``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbsubnetgroup.html
    cloudformationResource:
    :cloudformationResource:: AWS::DocDB::DBSubnetGroup
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, db_subnet_group_description: str, subnet_ids: typing.List[str], db_subnet_group_name: typing.Optional[str]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None) -> None:
        """Create a new ``AWS::DocDB::DBSubnetGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param db_subnet_group_description: ``AWS::DocDB::DBSubnetGroup.DBSubnetGroupDescription``.
        :param subnet_ids: ``AWS::DocDB::DBSubnetGroup.SubnetIds``.
        :param db_subnet_group_name: ``AWS::DocDB::DBSubnetGroup.DBSubnetGroupName``.
        :param tags: ``AWS::DocDB::DBSubnetGroup.Tags``.
        """
        props = CfnDBSubnetGroupProps(db_subnet_group_description=db_subnet_group_description, subnet_ids=subnet_ids, db_subnet_group_name=db_subnet_group_name, tags=tags)

        jsii.create(CfnDBSubnetGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnDBSubnetGroup":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = _FromCloudFormationOptions_5f49f6f1(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_154f5999) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::DocDB::DBSubnetGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbsubnetgroup.html#cfn-docdb-dbsubnetgroup-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="dbSubnetGroupDescription")
    def db_subnet_group_description(self) -> str:
        """``AWS::DocDB::DBSubnetGroup.DBSubnetGroupDescription``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbsubnetgroup.html#cfn-docdb-dbsubnetgroup-dbsubnetgroupdescription
        """
        return jsii.get(self, "dbSubnetGroupDescription")

    @db_subnet_group_description.setter
    def db_subnet_group_description(self, value: str) -> None:
        jsii.set(self, "dbSubnetGroupDescription", value)

    @builtins.property
    @jsii.member(jsii_name="subnetIds")
    def subnet_ids(self) -> typing.List[str]:
        """``AWS::DocDB::DBSubnetGroup.SubnetIds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbsubnetgroup.html#cfn-docdb-dbsubnetgroup-subnetids
        """
        return jsii.get(self, "subnetIds")

    @subnet_ids.setter
    def subnet_ids(self, value: typing.List[str]) -> None:
        jsii.set(self, "subnetIds", value)

    @builtins.property
    @jsii.member(jsii_name="dbSubnetGroupName")
    def db_subnet_group_name(self) -> typing.Optional[str]:
        """``AWS::DocDB::DBSubnetGroup.DBSubnetGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbsubnetgroup.html#cfn-docdb-dbsubnetgroup-dbsubnetgroupname
        """
        return jsii.get(self, "dbSubnetGroupName")

    @db_subnet_group_name.setter
    def db_subnet_group_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "dbSubnetGroupName", value)


@jsii.data_type(jsii_type="monocdk-experiment.aws_docdb.CfnDBSubnetGroupProps", jsii_struct_bases=[], name_mapping={'db_subnet_group_description': 'dbSubnetGroupDescription', 'subnet_ids': 'subnetIds', 'db_subnet_group_name': 'dbSubnetGroupName', 'tags': 'tags'})
class CfnDBSubnetGroupProps():
    def __init__(self, *, db_subnet_group_description: str, subnet_ids: typing.List[str], db_subnet_group_name: typing.Optional[str]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None) -> None:
        """Properties for defining a ``AWS::DocDB::DBSubnetGroup``.

        :param db_subnet_group_description: ``AWS::DocDB::DBSubnetGroup.DBSubnetGroupDescription``.
        :param subnet_ids: ``AWS::DocDB::DBSubnetGroup.SubnetIds``.
        :param db_subnet_group_name: ``AWS::DocDB::DBSubnetGroup.DBSubnetGroupName``.
        :param tags: ``AWS::DocDB::DBSubnetGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbsubnetgroup.html
        """
        self._values = {
            'db_subnet_group_description': db_subnet_group_description,
            'subnet_ids': subnet_ids,
        }
        if db_subnet_group_name is not None: self._values["db_subnet_group_name"] = db_subnet_group_name
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def db_subnet_group_description(self) -> str:
        """``AWS::DocDB::DBSubnetGroup.DBSubnetGroupDescription``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbsubnetgroup.html#cfn-docdb-dbsubnetgroup-dbsubnetgroupdescription
        """
        return self._values.get('db_subnet_group_description')

    @builtins.property
    def subnet_ids(self) -> typing.List[str]:
        """``AWS::DocDB::DBSubnetGroup.SubnetIds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbsubnetgroup.html#cfn-docdb-dbsubnetgroup-subnetids
        """
        return self._values.get('subnet_ids')

    @builtins.property
    def db_subnet_group_name(self) -> typing.Optional[str]:
        """``AWS::DocDB::DBSubnetGroup.DBSubnetGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbsubnetgroup.html#cfn-docdb-dbsubnetgroup-dbsubnetgroupname
        """
        return self._values.get('db_subnet_group_name')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_b4661f1a]]:
        """``AWS::DocDB::DBSubnetGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdb-dbsubnetgroup.html#cfn-docdb-dbsubnetgroup-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnDBSubnetGroupProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_docdb.ClusterParameterGroupProps", jsii_struct_bases=[], name_mapping={'family': 'family', 'parameters': 'parameters', 'db_cluster_parameter_group_name': 'dbClusterParameterGroupName', 'description': 'description'})
class ClusterParameterGroupProps():
    def __init__(self, *, family: str, parameters: typing.Mapping[str, str], db_cluster_parameter_group_name: typing.Optional[str]=None, description: typing.Optional[str]=None) -> None:
        """Properties for a cluster parameter group.

        :param family: Database family of this parameter group.
        :param parameters: The parameters in this parameter group.
        :param db_cluster_parameter_group_name: The name of the cluster parameter group. Default: A CDK generated name for the cluster parameter group
        :param description: Description for this parameter group. Default: a CDK generated description

        stability
        :stability: experimental
        """
        self._values = {
            'family': family,
            'parameters': parameters,
        }
        if db_cluster_parameter_group_name is not None: self._values["db_cluster_parameter_group_name"] = db_cluster_parameter_group_name
        if description is not None: self._values["description"] = description

    @builtins.property
    def family(self) -> str:
        """Database family of this parameter group.

        stability
        :stability: experimental
        """
        return self._values.get('family')

    @builtins.property
    def parameters(self) -> typing.Mapping[str, str]:
        """The parameters in this parameter group.

        stability
        :stability: experimental
        """
        return self._values.get('parameters')

    @builtins.property
    def db_cluster_parameter_group_name(self) -> typing.Optional[str]:
        """The name of the cluster parameter group.

        default
        :default: A CDK generated name for the cluster parameter group

        stability
        :stability: experimental
        """
        return self._values.get('db_cluster_parameter_group_name')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """Description for this parameter group.

        default
        :default: a CDK generated description

        stability
        :stability: experimental
        """
        return self._values.get('description')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ClusterParameterGroupProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_docdb.DatabaseClusterAttributes", jsii_struct_bases=[], name_mapping={'cluster_endpoint_address': 'clusterEndpointAddress', 'cluster_identifier': 'clusterIdentifier', 'instance_endpoint_addresses': 'instanceEndpointAddresses', 'instance_identifiers': 'instanceIdentifiers', 'port': 'port', 'reader_endpoint_address': 'readerEndpointAddress', 'security_group': 'securityGroup'})
class DatabaseClusterAttributes():
    def __init__(self, *, cluster_endpoint_address: str, cluster_identifier: str, instance_endpoint_addresses: typing.List[str], instance_identifiers: typing.List[str], port: jsii.Number, reader_endpoint_address: str, security_group: _ISecurityGroup_d72ab8e8) -> None:
        """Properties that describe an existing cluster instance.

        :param cluster_endpoint_address: Cluster endpoint address.
        :param cluster_identifier: Identifier for the cluster.
        :param instance_endpoint_addresses: Endpoint addresses of individual instances.
        :param instance_identifiers: Identifier for the instances.
        :param port: The database port.
        :param reader_endpoint_address: Reader endpoint address.
        :param security_group: The security group of the database cluster.

        stability
        :stability: experimental
        """
        self._values = {
            'cluster_endpoint_address': cluster_endpoint_address,
            'cluster_identifier': cluster_identifier,
            'instance_endpoint_addresses': instance_endpoint_addresses,
            'instance_identifiers': instance_identifiers,
            'port': port,
            'reader_endpoint_address': reader_endpoint_address,
            'security_group': security_group,
        }

    @builtins.property
    def cluster_endpoint_address(self) -> str:
        """Cluster endpoint address.

        stability
        :stability: experimental
        """
        return self._values.get('cluster_endpoint_address')

    @builtins.property
    def cluster_identifier(self) -> str:
        """Identifier for the cluster.

        stability
        :stability: experimental
        """
        return self._values.get('cluster_identifier')

    @builtins.property
    def instance_endpoint_addresses(self) -> typing.List[str]:
        """Endpoint addresses of individual instances.

        stability
        :stability: experimental
        """
        return self._values.get('instance_endpoint_addresses')

    @builtins.property
    def instance_identifiers(self) -> typing.List[str]:
        """Identifier for the instances.

        stability
        :stability: experimental
        """
        return self._values.get('instance_identifiers')

    @builtins.property
    def port(self) -> jsii.Number:
        """The database port.

        stability
        :stability: experimental
        """
        return self._values.get('port')

    @builtins.property
    def reader_endpoint_address(self) -> str:
        """Reader endpoint address.

        stability
        :stability: experimental
        """
        return self._values.get('reader_endpoint_address')

    @builtins.property
    def security_group(self) -> _ISecurityGroup_d72ab8e8:
        """The security group of the database cluster.

        stability
        :stability: experimental
        """
        return self._values.get('security_group')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DatabaseClusterAttributes(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_docdb.DatabaseClusterProps", jsii_struct_bases=[], name_mapping={'instance_props': 'instanceProps', 'master_user': 'masterUser', 'backup': 'backup', 'db_cluster_name': 'dbClusterName', 'engine_version': 'engineVersion', 'instance_identifier_base': 'instanceIdentifierBase', 'instances': 'instances', 'kms_key': 'kmsKey', 'parameter_group': 'parameterGroup', 'port': 'port', 'preferred_maintenance_window': 'preferredMaintenanceWindow', 'removal_policy': 'removalPolicy', 'storage_encrypted': 'storageEncrypted'})
class DatabaseClusterProps():
    def __init__(self, *, instance_props: "InstanceProps", master_user: "Login", backup: typing.Optional["BackupProps"]=None, db_cluster_name: typing.Optional[str]=None, engine_version: typing.Optional[str]=None, instance_identifier_base: typing.Optional[str]=None, instances: typing.Optional[jsii.Number]=None, kms_key: typing.Optional[_IKey_3336c79d]=None, parameter_group: typing.Optional["IClusterParameterGroup"]=None, port: typing.Optional[jsii.Number]=None, preferred_maintenance_window: typing.Optional[str]=None, removal_policy: typing.Optional[_RemovalPolicy_5986e9f3]=None, storage_encrypted: typing.Optional[bool]=None) -> None:
        """Properties for a new database cluster.

        :param instance_props: Settings for the individual instances that are launched.
        :param master_user: Username and password for the administrative user.
        :param backup: Backup settings. Default: - Backup retention period for automated backups is 1 day. Backup preferred window is set to a 30-minute window selected at random from an 8-hour block of time for each AWS Region, occurring on a random day of the week.
        :param db_cluster_name: An optional identifier for the cluster. Default: - A name is automatically generated.
        :param engine_version: What version of the database to start. Default: - The default engine version.
        :param instance_identifier_base: Base identifier for instances. Every replica is named by appending the replica number to this string, 1-based. Default: - ``dbClusterName`` is used with the word "Instance" appended. If ``dbClusterName`` is not provided, the identifier is automatically generated.
        :param instances: Number of DocDB compute instances. Default: 1
        :param kms_key: The KMS key for storage encryption. Default: - default master key.
        :param parameter_group: Additional parameters to pass to the database engine. Default: - No parameter group.
        :param port: The port the DocumentDB cluster will listen on. Default: DatabaseCluster.DEFAULT_PORT
        :param preferred_maintenance_window: A weekly time range in which maintenance should preferably execute. Must be at least 30 minutes long. Example: 'tue:04:17-tue:04:47' Default: - 30-minute window selected at random from an 8-hour block of time for each AWS Region, occurring on a random day of the week.
        :param removal_policy: The removal policy to apply when the cluster and its instances are removed or replaced during a stack update, or when the stack is deleted. This removal policy also applies to the implicit security group created for the cluster if one is not supplied as a parameter. Default: - Retain cluster.
        :param storage_encrypted: Whether to enable storage encryption. Default: true

        stability
        :stability: experimental
        """
        if isinstance(instance_props, dict): instance_props = InstanceProps(**instance_props)
        if isinstance(master_user, dict): master_user = Login(**master_user)
        if isinstance(backup, dict): backup = BackupProps(**backup)
        self._values = {
            'instance_props': instance_props,
            'master_user': master_user,
        }
        if backup is not None: self._values["backup"] = backup
        if db_cluster_name is not None: self._values["db_cluster_name"] = db_cluster_name
        if engine_version is not None: self._values["engine_version"] = engine_version
        if instance_identifier_base is not None: self._values["instance_identifier_base"] = instance_identifier_base
        if instances is not None: self._values["instances"] = instances
        if kms_key is not None: self._values["kms_key"] = kms_key
        if parameter_group is not None: self._values["parameter_group"] = parameter_group
        if port is not None: self._values["port"] = port
        if preferred_maintenance_window is not None: self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if removal_policy is not None: self._values["removal_policy"] = removal_policy
        if storage_encrypted is not None: self._values["storage_encrypted"] = storage_encrypted

    @builtins.property
    def instance_props(self) -> "InstanceProps":
        """Settings for the individual instances that are launched.

        stability
        :stability: experimental
        """
        return self._values.get('instance_props')

    @builtins.property
    def master_user(self) -> "Login":
        """Username and password for the administrative user.

        stability
        :stability: experimental
        """
        return self._values.get('master_user')

    @builtins.property
    def backup(self) -> typing.Optional["BackupProps"]:
        """Backup settings.

        default
        :default:

        - Backup retention period for automated backups is 1 day.
          Backup preferred window is set to a 30-minute window selected at random from an
          8-hour block of time for each AWS Region, occurring on a random day of the week.

        see
        :see: https://docs.aws.amazon.com/documentdb/latest/developerguide/backup-restore.db-cluster-snapshots.html#backup-restore.backup-window
        stability
        :stability: experimental
        """
        return self._values.get('backup')

    @builtins.property
    def db_cluster_name(self) -> typing.Optional[str]:
        """An optional identifier for the cluster.

        default
        :default: - A name is automatically generated.

        stability
        :stability: experimental
        """
        return self._values.get('db_cluster_name')

    @builtins.property
    def engine_version(self) -> typing.Optional[str]:
        """What version of the database to start.

        default
        :default: - The default engine version.

        stability
        :stability: experimental
        """
        return self._values.get('engine_version')

    @builtins.property
    def instance_identifier_base(self) -> typing.Optional[str]:
        """Base identifier for instances.

        Every replica is named by appending the replica number to this string, 1-based.

        default
        :default:

        - ``dbClusterName`` is used with the word "Instance" appended. If ``dbClusterName`` is not provided, the
          identifier is automatically generated.

        stability
        :stability: experimental
        """
        return self._values.get('instance_identifier_base')

    @builtins.property
    def instances(self) -> typing.Optional[jsii.Number]:
        """Number of DocDB compute instances.

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('instances')

    @builtins.property
    def kms_key(self) -> typing.Optional[_IKey_3336c79d]:
        """The KMS key for storage encryption.

        default
        :default: - default master key.

        stability
        :stability: experimental
        """
        return self._values.get('kms_key')

    @builtins.property
    def parameter_group(self) -> typing.Optional["IClusterParameterGroup"]:
        """Additional parameters to pass to the database engine.

        default
        :default: - No parameter group.

        stability
        :stability: experimental
        """
        return self._values.get('parameter_group')

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        """The port the DocumentDB cluster will listen on.

        default
        :default: DatabaseCluster.DEFAULT_PORT

        stability
        :stability: experimental
        """
        return self._values.get('port')

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[str]:
        """A weekly time range in which maintenance should preferably execute.

        Must be at least 30 minutes long.

        Example: 'tue:04:17-tue:04:47'

        default
        :default:

        - 30-minute window selected at random from an 8-hour block of time for
          each AWS Region, occurring on a random day of the week.

        see
        :see: https://docs.aws.amazon.com/documentdb/latest/developerguide/db-instance-maintain.html#maintenance-window
        stability
        :stability: experimental
        """
        return self._values.get('preferred_maintenance_window')

    @builtins.property
    def removal_policy(self) -> typing.Optional[_RemovalPolicy_5986e9f3]:
        """The removal policy to apply when the cluster and its instances are removed or replaced during a stack update, or when the stack is deleted.

        This
        removal policy also applies to the implicit security group created for the
        cluster if one is not supplied as a parameter.

        default
        :default: - Retain cluster.

        stability
        :stability: experimental
        """
        return self._values.get('removal_policy')

    @builtins.property
    def storage_encrypted(self) -> typing.Optional[bool]:
        """Whether to enable storage encryption.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('storage_encrypted')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DatabaseClusterProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_docdb.DatabaseInstanceAttributes", jsii_struct_bases=[], name_mapping={'instance_endpoint_address': 'instanceEndpointAddress', 'instance_identifier': 'instanceIdentifier', 'port': 'port'})
class DatabaseInstanceAttributes():
    def __init__(self, *, instance_endpoint_address: str, instance_identifier: str, port: jsii.Number) -> None:
        """Properties that describe an existing instance.

        :param instance_endpoint_address: The endpoint address.
        :param instance_identifier: The instance identifier.
        :param port: The database port.

        stability
        :stability: experimental
        """
        self._values = {
            'instance_endpoint_address': instance_endpoint_address,
            'instance_identifier': instance_identifier,
            'port': port,
        }

    @builtins.property
    def instance_endpoint_address(self) -> str:
        """The endpoint address.

        stability
        :stability: experimental
        """
        return self._values.get('instance_endpoint_address')

    @builtins.property
    def instance_identifier(self) -> str:
        """The instance identifier.

        stability
        :stability: experimental
        """
        return self._values.get('instance_identifier')

    @builtins.property
    def port(self) -> jsii.Number:
        """The database port.

        stability
        :stability: experimental
        """
        return self._values.get('port')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DatabaseInstanceAttributes(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_docdb.DatabaseInstanceProps", jsii_struct_bases=[], name_mapping={'cluster': 'cluster', 'instance_class': 'instanceClass', 'auto_minor_version_upgrade': 'autoMinorVersionUpgrade', 'availability_zone': 'availabilityZone', 'db_instance_name': 'dbInstanceName', 'preferred_maintenance_window': 'preferredMaintenanceWindow', 'removal_policy': 'removalPolicy'})
class DatabaseInstanceProps():
    def __init__(self, *, cluster: "IDatabaseCluster", instance_class: _InstanceType_85a97b30, auto_minor_version_upgrade: typing.Optional[bool]=None, availability_zone: typing.Optional[str]=None, db_instance_name: typing.Optional[str]=None, preferred_maintenance_window: typing.Optional[str]=None, removal_policy: typing.Optional[_RemovalPolicy_5986e9f3]=None) -> None:
        """Construction properties for a DatabaseInstanceNew.

        :param cluster: The DocumentDB database cluster the instance should launch into.
        :param instance_class: The name of the compute and memory capacity classes.
        :param auto_minor_version_upgrade: Indicates that minor engine upgrades are applied automatically to the DB instance during the maintenance window. Default: true
        :param availability_zone: The name of the Availability Zone where the DB instance will be located. Default: - no preference
        :param db_instance_name: A name for the DB instance. If you specify a name, AWS CloudFormation converts it to lowercase. Default: - a CloudFormation generated name
        :param preferred_maintenance_window: The weekly time range (in UTC) during which system maintenance can occur. Format: ``ddd:hh24:mi-ddd:hh24:mi`` Constraint: Minimum 30-minute window Default: - a 30-minute window selected at random from an 8-hour block of time for each AWS Region, occurring on a random day of the week. To see the time blocks available, see https://docs.aws.amazon.com/documentdb/latest/developerguide/db-instance-maintain.html#maintenance-window
        :param removal_policy: The CloudFormation policy to apply when the instance is removed from the stack or replaced during an update. Default: RemovalPolicy.Retain

        stability
        :stability: experimental
        """
        self._values = {
            'cluster': cluster,
            'instance_class': instance_class,
        }
        if auto_minor_version_upgrade is not None: self._values["auto_minor_version_upgrade"] = auto_minor_version_upgrade
        if availability_zone is not None: self._values["availability_zone"] = availability_zone
        if db_instance_name is not None: self._values["db_instance_name"] = db_instance_name
        if preferred_maintenance_window is not None: self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if removal_policy is not None: self._values["removal_policy"] = removal_policy

    @builtins.property
    def cluster(self) -> "IDatabaseCluster":
        """The DocumentDB database cluster the instance should launch into.

        stability
        :stability: experimental
        """
        return self._values.get('cluster')

    @builtins.property
    def instance_class(self) -> _InstanceType_85a97b30:
        """The name of the compute and memory capacity classes.

        stability
        :stability: experimental
        """
        return self._values.get('instance_class')

    @builtins.property
    def auto_minor_version_upgrade(self) -> typing.Optional[bool]:
        """Indicates that minor engine upgrades are applied automatically to the DB instance during the maintenance window.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('auto_minor_version_upgrade')

    @builtins.property
    def availability_zone(self) -> typing.Optional[str]:
        """The name of the Availability Zone where the DB instance will be located.

        default
        :default: - no preference

        stability
        :stability: experimental
        """
        return self._values.get('availability_zone')

    @builtins.property
    def db_instance_name(self) -> typing.Optional[str]:
        """A name for the DB instance.

        If you specify a name, AWS CloudFormation
        converts it to lowercase.

        default
        :default: - a CloudFormation generated name

        stability
        :stability: experimental
        """
        return self._values.get('db_instance_name')

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[str]:
        """The weekly time range (in UTC) during which system maintenance can occur.

        Format: ``ddd:hh24:mi-ddd:hh24:mi``
        Constraint: Minimum 30-minute window

        default
        :default:

        - a 30-minute window selected at random from an 8-hour block of
          time for each AWS Region, occurring on a random day of the week. To see
          the time blocks available, see https://docs.aws.amazon.com/documentdb/latest/developerguide/db-instance-maintain.html#maintenance-window

        stability
        :stability: experimental
        """
        return self._values.get('preferred_maintenance_window')

    @builtins.property
    def removal_policy(self) -> typing.Optional[_RemovalPolicy_5986e9f3]:
        """The CloudFormation policy to apply when the instance is removed from the stack or replaced during an update.

        default
        :default: RemovalPolicy.Retain

        stability
        :stability: experimental
        """
        return self._values.get('removal_policy')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DatabaseInstanceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class DatabaseSecret(_Secret_01d21232, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_docdb.DatabaseSecret"):
    """A database secret.

    stability
    :stability: experimental
    resource:
    :resource:: AWS::SecretsManager::Secret
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, username: str, encryption_key: typing.Optional[_IKey_3336c79d]=None, master_secret: typing.Optional[_ISecret_75279d36]=None, secret_name: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param username: The username.
        :param encryption_key: The KMS key to use to encrypt the secret. Default: default master key
        :param master_secret: The master secret which will be used to rotate this secret. Default: - no master secret information will be included
        :param secret_name: The physical name of the secret. Default: Secretsmanager will generate a physical name for the secret

        stability
        :stability: experimental
        """
        props = DatabaseSecretProps(username=username, encryption_key=encryption_key, master_secret=master_secret, secret_name=secret_name)

        jsii.create(DatabaseSecret, self, [scope, id, props])


@jsii.data_type(jsii_type="monocdk-experiment.aws_docdb.DatabaseSecretProps", jsii_struct_bases=[], name_mapping={'username': 'username', 'encryption_key': 'encryptionKey', 'master_secret': 'masterSecret', 'secret_name': 'secretName'})
class DatabaseSecretProps():
    def __init__(self, *, username: str, encryption_key: typing.Optional[_IKey_3336c79d]=None, master_secret: typing.Optional[_ISecret_75279d36]=None, secret_name: typing.Optional[str]=None) -> None:
        """Construction properties for a DatabaseSecret.

        :param username: The username.
        :param encryption_key: The KMS key to use to encrypt the secret. Default: default master key
        :param master_secret: The master secret which will be used to rotate this secret. Default: - no master secret information will be included
        :param secret_name: The physical name of the secret. Default: Secretsmanager will generate a physical name for the secret

        stability
        :stability: experimental
        """
        self._values = {
            'username': username,
        }
        if encryption_key is not None: self._values["encryption_key"] = encryption_key
        if master_secret is not None: self._values["master_secret"] = master_secret
        if secret_name is not None: self._values["secret_name"] = secret_name

    @builtins.property
    def username(self) -> str:
        """The username.

        stability
        :stability: experimental
        """
        return self._values.get('username')

    @builtins.property
    def encryption_key(self) -> typing.Optional[_IKey_3336c79d]:
        """The KMS key to use to encrypt the secret.

        default
        :default: default master key

        stability
        :stability: experimental
        """
        return self._values.get('encryption_key')

    @builtins.property
    def master_secret(self) -> typing.Optional[_ISecret_75279d36]:
        """The master secret which will be used to rotate this secret.

        default
        :default: - no master secret information will be included

        stability
        :stability: experimental
        """
        return self._values.get('master_secret')

    @builtins.property
    def secret_name(self) -> typing.Optional[str]:
        """The physical name of the secret.

        default
        :default: Secretsmanager will generate a physical name for the secret

        stability
        :stability: experimental
        """
        return self._values.get('secret_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DatabaseSecretProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class Endpoint(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_docdb.Endpoint"):
    """Connection endpoint of a database cluster or instance.

    Consists of a combination of hostname and port.

    stability
    :stability: experimental
    """
    def __init__(self, address: str, port: jsii.Number) -> None:
        """Constructs an Endpoint instance.

        :param address: - The hostname or address of the endpoint.
        :param port: - The port number of the endpoint.

        stability
        :stability: experimental
        """
        jsii.create(Endpoint, self, [address, port])

    @jsii.member(jsii_name="portAsString")
    def port_as_string(self) -> str:
        """Returns the port number as a string representation that can be used for embedding within other strings.

        This is intended to deal with CDK's token system. Numeric CDK tokens are not expanded when their string
        representation is embedded in a string. This function returns the port either as an unresolved string token or
        as a resolved string representation of the port value.

        return
        :return: An (un)resolved string representation of the endpoint's port number

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "portAsString", [])

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> str:
        """The hostname of the endpoint.

        stability
        :stability: experimental
        """
        return jsii.get(self, "hostname")

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        """The port number of the endpoint.

        This can potentially be a CDK token. If you need to embed the port in a string (e.g. instance user data script),
        use {@link Endpoint.portAsString}.

        stability
        :stability: experimental
        """
        return jsii.get(self, "port")

    @builtins.property
    @jsii.member(jsii_name="socketAddress")
    def socket_address(self) -> str:
        """The combination of "HOSTNAME:PORT" for this endpoint.

        stability
        :stability: experimental
        """
        return jsii.get(self, "socketAddress")


@jsii.interface(jsii_type="monocdk-experiment.aws_docdb.IClusterParameterGroup")
class IClusterParameterGroup(_IResource_72f7ee7e, jsii.compat.Protocol):
    """A parameter group.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IClusterParameterGroupProxy

    @builtins.property
    @jsii.member(jsii_name="parameterGroupName")
    def parameter_group_name(self) -> str:
        """The name of this parameter group.

        stability
        :stability: experimental
        """
        ...


class _IClusterParameterGroupProxy(jsii.proxy_for(_IResource_72f7ee7e)):
    """A parameter group.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_docdb.IClusterParameterGroup"
    @builtins.property
    @jsii.member(jsii_name="parameterGroupName")
    def parameter_group_name(self) -> str:
        """The name of this parameter group.

        stability
        :stability: experimental
        """
        return jsii.get(self, "parameterGroupName")


@jsii.interface(jsii_type="monocdk-experiment.aws_docdb.IDatabaseCluster")
class IDatabaseCluster(_IResource_72f7ee7e, _IConnectable_a587039f, _ISecretAttachmentTarget_0a569782, jsii.compat.Protocol):
    """Create a clustered database with a given number of instances.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IDatabaseClusterProxy

    @builtins.property
    @jsii.member(jsii_name="clusterEndpoint")
    def cluster_endpoint(self) -> "Endpoint":
        """The endpoint to use for read/write operations.

        stability
        :stability: experimental
        attribute:
        :attribute:: Endpoint,Port
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="clusterIdentifier")
    def cluster_identifier(self) -> str:
        """Identifier of the cluster.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="clusterReadEndpoint")
    def cluster_read_endpoint(self) -> "Endpoint":
        """Endpoint to use for load-balanced read-only operations.

        stability
        :stability: experimental
        attribute:
        :attribute:: ReadEndpoint
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="instanceEndpoints")
    def instance_endpoints(self) -> typing.List["Endpoint"]:
        """Endpoints which address each individual replica.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="instanceIdentifiers")
    def instance_identifiers(self) -> typing.List[str]:
        """Identifiers of the replicas.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="securityGroupId")
    def security_group_id(self) -> str:
        """The security group for this database cluster.

        stability
        :stability: experimental
        """
        ...


class _IDatabaseClusterProxy(jsii.proxy_for(_IResource_72f7ee7e), jsii.proxy_for(_IConnectable_a587039f), jsii.proxy_for(_ISecretAttachmentTarget_0a569782)):
    """Create a clustered database with a given number of instances.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_docdb.IDatabaseCluster"
    @builtins.property
    @jsii.member(jsii_name="clusterEndpoint")
    def cluster_endpoint(self) -> "Endpoint":
        """The endpoint to use for read/write operations.

        stability
        :stability: experimental
        attribute:
        :attribute:: Endpoint,Port
        """
        return jsii.get(self, "clusterEndpoint")

    @builtins.property
    @jsii.member(jsii_name="clusterIdentifier")
    def cluster_identifier(self) -> str:
        """Identifier of the cluster.

        stability
        :stability: experimental
        """
        return jsii.get(self, "clusterIdentifier")

    @builtins.property
    @jsii.member(jsii_name="clusterReadEndpoint")
    def cluster_read_endpoint(self) -> "Endpoint":
        """Endpoint to use for load-balanced read-only operations.

        stability
        :stability: experimental
        attribute:
        :attribute:: ReadEndpoint
        """
        return jsii.get(self, "clusterReadEndpoint")

    @builtins.property
    @jsii.member(jsii_name="instanceEndpoints")
    def instance_endpoints(self) -> typing.List["Endpoint"]:
        """Endpoints which address each individual replica.

        stability
        :stability: experimental
        """
        return jsii.get(self, "instanceEndpoints")

    @builtins.property
    @jsii.member(jsii_name="instanceIdentifiers")
    def instance_identifiers(self) -> typing.List[str]:
        """Identifiers of the replicas.

        stability
        :stability: experimental
        """
        return jsii.get(self, "instanceIdentifiers")

    @builtins.property
    @jsii.member(jsii_name="securityGroupId")
    def security_group_id(self) -> str:
        """The security group for this database cluster.

        stability
        :stability: experimental
        """
        return jsii.get(self, "securityGroupId")


@jsii.interface(jsii_type="monocdk-experiment.aws_docdb.IDatabaseInstance")
class IDatabaseInstance(_IResource_72f7ee7e, jsii.compat.Protocol):
    """A database instance.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IDatabaseInstanceProxy

    @builtins.property
    @jsii.member(jsii_name="dbInstanceEndpointAddress")
    def db_instance_endpoint_address(self) -> str:
        """The instance endpoint address.

        stability
        :stability: experimental
        attribute:
        :attribute:: Endpoint
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="dbInstanceEndpointPort")
    def db_instance_endpoint_port(self) -> str:
        """The instance endpoint port.

        stability
        :stability: experimental
        attribute:
        :attribute:: Port
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="instanceArn")
    def instance_arn(self) -> str:
        """The instance arn.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="instanceEndpoint")
    def instance_endpoint(self) -> "Endpoint":
        """The instance endpoint.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="instanceIdentifier")
    def instance_identifier(self) -> str:
        """The instance identifier.

        stability
        :stability: experimental
        """
        ...


class _IDatabaseInstanceProxy(jsii.proxy_for(_IResource_72f7ee7e)):
    """A database instance.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_docdb.IDatabaseInstance"
    @builtins.property
    @jsii.member(jsii_name="dbInstanceEndpointAddress")
    def db_instance_endpoint_address(self) -> str:
        """The instance endpoint address.

        stability
        :stability: experimental
        attribute:
        :attribute:: Endpoint
        """
        return jsii.get(self, "dbInstanceEndpointAddress")

    @builtins.property
    @jsii.member(jsii_name="dbInstanceEndpointPort")
    def db_instance_endpoint_port(self) -> str:
        """The instance endpoint port.

        stability
        :stability: experimental
        attribute:
        :attribute:: Port
        """
        return jsii.get(self, "dbInstanceEndpointPort")

    @builtins.property
    @jsii.member(jsii_name="instanceArn")
    def instance_arn(self) -> str:
        """The instance arn.

        stability
        :stability: experimental
        """
        return jsii.get(self, "instanceArn")

    @builtins.property
    @jsii.member(jsii_name="instanceEndpoint")
    def instance_endpoint(self) -> "Endpoint":
        """The instance endpoint.

        stability
        :stability: experimental
        """
        return jsii.get(self, "instanceEndpoint")

    @builtins.property
    @jsii.member(jsii_name="instanceIdentifier")
    def instance_identifier(self) -> str:
        """The instance identifier.

        stability
        :stability: experimental
        """
        return jsii.get(self, "instanceIdentifier")


@jsii.data_type(jsii_type="monocdk-experiment.aws_docdb.InstanceProps", jsii_struct_bases=[], name_mapping={'instance_type': 'instanceType', 'vpc': 'vpc', 'parameter_group': 'parameterGroup', 'security_group': 'securityGroup', 'vpc_subnets': 'vpcSubnets'})
class InstanceProps():
    def __init__(self, *, instance_type: _InstanceType_85a97b30, vpc: _IVpc_3795853f, parameter_group: typing.Optional["IClusterParameterGroup"]=None, security_group: typing.Optional[_ISecurityGroup_d72ab8e8]=None, vpc_subnets: typing.Optional[_SubnetSelection_36a13cd6]=None) -> None:
        """Instance properties for database instances.

        :param instance_type: What type of instance to start for the replicas.
        :param vpc: What subnets to run the DocumentDB instances in. Must be at least 2 subnets in two different AZs.
        :param parameter_group: The DB parameter group to associate with the instance. Default: no parameter group
        :param security_group: Security group. Default: a new security group is created.
        :param vpc_subnets: Where to place the instances within the VPC. Default: private subnets

        stability
        :stability: experimental
        """
        if isinstance(vpc_subnets, dict): vpc_subnets = _SubnetSelection_36a13cd6(**vpc_subnets)
        self._values = {
            'instance_type': instance_type,
            'vpc': vpc,
        }
        if parameter_group is not None: self._values["parameter_group"] = parameter_group
        if security_group is not None: self._values["security_group"] = security_group
        if vpc_subnets is not None: self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def instance_type(self) -> _InstanceType_85a97b30:
        """What type of instance to start for the replicas.

        stability
        :stability: experimental
        """
        return self._values.get('instance_type')

    @builtins.property
    def vpc(self) -> _IVpc_3795853f:
        """What subnets to run the DocumentDB instances in.

        Must be at least 2 subnets in two different AZs.

        stability
        :stability: experimental
        """
        return self._values.get('vpc')

    @builtins.property
    def parameter_group(self) -> typing.Optional["IClusterParameterGroup"]:
        """The DB parameter group to associate with the instance.

        default
        :default: no parameter group

        stability
        :stability: experimental
        """
        return self._values.get('parameter_group')

    @builtins.property
    def security_group(self) -> typing.Optional[_ISecurityGroup_d72ab8e8]:
        """Security group.

        default
        :default: a new security group is created.

        stability
        :stability: experimental
        """
        return self._values.get('security_group')

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_SubnetSelection_36a13cd6]:
        """Where to place the instances within the VPC.

        default
        :default: private subnets

        stability
        :stability: experimental
        """
        return self._values.get('vpc_subnets')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'InstanceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_docdb.Login", jsii_struct_bases=[], name_mapping={'username': 'username', 'kms_key': 'kmsKey', 'password': 'password'})
class Login():
    def __init__(self, *, username: str, kms_key: typing.Optional[_IKey_3336c79d]=None, password: typing.Optional[_SecretValue_99478b8b]=None) -> None:
        """Login credentials for a database cluster.

        :param username: Username.
        :param kms_key: KMS encryption key to encrypt the generated secret. Default: default master key
        :param password: Password. Do not put passwords in your CDK code directly. Default: a Secrets Manager generated password

        stability
        :stability: experimental
        """
        self._values = {
            'username': username,
        }
        if kms_key is not None: self._values["kms_key"] = kms_key
        if password is not None: self._values["password"] = password

    @builtins.property
    def username(self) -> str:
        """Username.

        stability
        :stability: experimental
        """
        return self._values.get('username')

    @builtins.property
    def kms_key(self) -> typing.Optional[_IKey_3336c79d]:
        """KMS encryption key to encrypt the generated secret.

        default
        :default: default master key

        stability
        :stability: experimental
        """
        return self._values.get('kms_key')

    @builtins.property
    def password(self) -> typing.Optional[_SecretValue_99478b8b]:
        """Password.

        Do not put passwords in your CDK code directly.

        default
        :default: a Secrets Manager generated password

        stability
        :stability: experimental
        """
        return self._values.get('password')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'Login(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_docdb.RotationMultiUserOptions", jsii_struct_bases=[], name_mapping={'secret': 'secret', 'automatically_after': 'automaticallyAfter'})
class RotationMultiUserOptions():
    def __init__(self, *, secret: _ISecret_75279d36, automatically_after: typing.Optional[_Duration_5170c158]=None) -> None:
        """Options to add the multi user rotation.

        :param secret: The secret to rotate. It must be a JSON string with the following format:: { "engine": <required: must be set to 'mongo'>, "host": <required: instance host name>, "username": <required: username>, "password": <required: password>, "dbname": <optional: database name>, "port": <optional: if not specified, default port 27017 will be used>, "masterarn": <required: the arn of the master secret which will be used to create users/change passwords> "ssl": <optional: if not specified, defaults to false. This must be true if being used for DocumentDB rotations where the cluster has TLS enabled> }
        :param automatically_after: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. Default: Duration.days(30)

        stability
        :stability: experimental
        """
        self._values = {
            'secret': secret,
        }
        if automatically_after is not None: self._values["automatically_after"] = automatically_after

    @builtins.property
    def secret(self) -> _ISecret_75279d36:
        """The secret to rotate.

        It must be a JSON string with the following format::

           {
              "engine": <required: must be set to 'mongo'>,
              "host": <required: instance host name>,
              "username": <required: username>,
              "password": <required: password>,
              "dbname": <optional: database name>,
              "port": <optional: if not specified, default port 27017 will be used>,
              "masterarn": <required: the arn of the master secret which will be used to create users/change passwords>
              "ssl": <optional: if not specified, defaults to false. This must be true if being used for DocumentDB rotations
                     where the cluster has TLS enabled>
           }

        stability
        :stability: experimental
        """
        return self._values.get('secret')

    @builtins.property
    def automatically_after(self) -> typing.Optional[_Duration_5170c158]:
        """Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation.

        default
        :default: Duration.days(30)

        stability
        :stability: experimental
        """
        return self._values.get('automatically_after')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'RotationMultiUserOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(IClusterParameterGroup)
class ClusterParameterGroup(_Resource_884d0774, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_docdb.ClusterParameterGroup"):
    """A cluster parameter group.

    stability
    :stability: experimental
    resource:
    :resource:: AWS::DocDB::DBClusterParameterGroup
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, family: str, parameters: typing.Mapping[str, str], db_cluster_parameter_group_name: typing.Optional[str]=None, description: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param family: Database family of this parameter group.
        :param parameters: The parameters in this parameter group.
        :param db_cluster_parameter_group_name: The name of the cluster parameter group. Default: A CDK generated name for the cluster parameter group
        :param description: Description for this parameter group. Default: a CDK generated description

        stability
        :stability: experimental
        """
        props = ClusterParameterGroupProps(family=family, parameters=parameters, db_cluster_parameter_group_name=db_cluster_parameter_group_name, description=description)

        jsii.create(ClusterParameterGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromParameterGroupName")
    @builtins.classmethod
    def from_parameter_group_name(cls, scope: _Construct_f50a3f53, id: str, parameter_group_name: str) -> "IClusterParameterGroup":
        """Imports a parameter group.

        :param scope: -
        :param id: -
        :param parameter_group_name: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromParameterGroupName", [scope, id, parameter_group_name])

    @builtins.property
    @jsii.member(jsii_name="parameterGroupName")
    def parameter_group_name(self) -> str:
        """The name of the parameter group.

        stability
        :stability: experimental
        """
        return jsii.get(self, "parameterGroupName")


@jsii.implements(IDatabaseCluster)
class DatabaseCluster(_Resource_884d0774, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_docdb.DatabaseCluster"):
    """Create a clustered database with a given number of instances.

    stability
    :stability: experimental
    resource:
    :resource:: AWS::DocDB::DBCluster
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, instance_props: "InstanceProps", master_user: "Login", backup: typing.Optional["BackupProps"]=None, db_cluster_name: typing.Optional[str]=None, engine_version: typing.Optional[str]=None, instance_identifier_base: typing.Optional[str]=None, instances: typing.Optional[jsii.Number]=None, kms_key: typing.Optional[_IKey_3336c79d]=None, parameter_group: typing.Optional["IClusterParameterGroup"]=None, port: typing.Optional[jsii.Number]=None, preferred_maintenance_window: typing.Optional[str]=None, removal_policy: typing.Optional[_RemovalPolicy_5986e9f3]=None, storage_encrypted: typing.Optional[bool]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param instance_props: Settings for the individual instances that are launched.
        :param master_user: Username and password for the administrative user.
        :param backup: Backup settings. Default: - Backup retention period for automated backups is 1 day. Backup preferred window is set to a 30-minute window selected at random from an 8-hour block of time for each AWS Region, occurring on a random day of the week.
        :param db_cluster_name: An optional identifier for the cluster. Default: - A name is automatically generated.
        :param engine_version: What version of the database to start. Default: - The default engine version.
        :param instance_identifier_base: Base identifier for instances. Every replica is named by appending the replica number to this string, 1-based. Default: - ``dbClusterName`` is used with the word "Instance" appended. If ``dbClusterName`` is not provided, the identifier is automatically generated.
        :param instances: Number of DocDB compute instances. Default: 1
        :param kms_key: The KMS key for storage encryption. Default: - default master key.
        :param parameter_group: Additional parameters to pass to the database engine. Default: - No parameter group.
        :param port: The port the DocumentDB cluster will listen on. Default: DatabaseCluster.DEFAULT_PORT
        :param preferred_maintenance_window: A weekly time range in which maintenance should preferably execute. Must be at least 30 minutes long. Example: 'tue:04:17-tue:04:47' Default: - 30-minute window selected at random from an 8-hour block of time for each AWS Region, occurring on a random day of the week.
        :param removal_policy: The removal policy to apply when the cluster and its instances are removed or replaced during a stack update, or when the stack is deleted. This removal policy also applies to the implicit security group created for the cluster if one is not supplied as a parameter. Default: - Retain cluster.
        :param storage_encrypted: Whether to enable storage encryption. Default: true

        stability
        :stability: experimental
        """
        props = DatabaseClusterProps(instance_props=instance_props, master_user=master_user, backup=backup, db_cluster_name=db_cluster_name, engine_version=engine_version, instance_identifier_base=instance_identifier_base, instances=instances, kms_key=kms_key, parameter_group=parameter_group, port=port, preferred_maintenance_window=preferred_maintenance_window, removal_policy=removal_policy, storage_encrypted=storage_encrypted)

        jsii.create(DatabaseCluster, self, [scope, id, props])

    @jsii.member(jsii_name="fromDatabaseClusterAttributes")
    @builtins.classmethod
    def from_database_cluster_attributes(cls, scope: _Construct_f50a3f53, id: str, *, cluster_endpoint_address: str, cluster_identifier: str, instance_endpoint_addresses: typing.List[str], instance_identifiers: typing.List[str], port: jsii.Number, reader_endpoint_address: str, security_group: _ISecurityGroup_d72ab8e8) -> "IDatabaseCluster":
        """Import an existing DatabaseCluster from properties.

        :param scope: -
        :param id: -
        :param cluster_endpoint_address: Cluster endpoint address.
        :param cluster_identifier: Identifier for the cluster.
        :param instance_endpoint_addresses: Endpoint addresses of individual instances.
        :param instance_identifiers: Identifier for the instances.
        :param port: The database port.
        :param reader_endpoint_address: Reader endpoint address.
        :param security_group: The security group of the database cluster.

        stability
        :stability: experimental
        """
        attrs = DatabaseClusterAttributes(cluster_endpoint_address=cluster_endpoint_address, cluster_identifier=cluster_identifier, instance_endpoint_addresses=instance_endpoint_addresses, instance_identifiers=instance_identifiers, port=port, reader_endpoint_address=reader_endpoint_address, security_group=security_group)

        return jsii.sinvoke(cls, "fromDatabaseClusterAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="addRotationMultiUser")
    def add_rotation_multi_user(self, id: str, *, secret: _ISecret_75279d36, automatically_after: typing.Optional[_Duration_5170c158]=None) -> _SecretRotation_312fb992:
        """Adds the multi user rotation to this cluster.

        :param id: -
        :param secret: The secret to rotate. It must be a JSON string with the following format:: { "engine": <required: must be set to 'mongo'>, "host": <required: instance host name>, "username": <required: username>, "password": <required: password>, "dbname": <optional: database name>, "port": <optional: if not specified, default port 27017 will be used>, "masterarn": <required: the arn of the master secret which will be used to create users/change passwords> "ssl": <optional: if not specified, defaults to false. This must be true if being used for DocumentDB rotations where the cluster has TLS enabled> }
        :param automatically_after: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. Default: Duration.days(30)

        stability
        :stability: experimental
        """
        options = RotationMultiUserOptions(secret=secret, automatically_after=automatically_after)

        return jsii.invoke(self, "addRotationMultiUser", [id, options])

    @jsii.member(jsii_name="addRotationSingleUser")
    def add_rotation_single_user(self, automatically_after: typing.Optional[_Duration_5170c158]=None) -> _SecretRotation_312fb992:
        """Adds the single user rotation of the master password to this cluster.

        :param automatically_after: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addRotationSingleUser", [automatically_after])

    @jsii.member(jsii_name="asSecretAttachmentTarget")
    def as_secret_attachment_target(self) -> _SecretAttachmentTargetProps_b948cd13:
        """Renders the secret attachment target specifications.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "asSecretAttachmentTarget", [])

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT_NUM_INSTANCES")
    def DEFAULT_NUM_INSTANCES(cls) -> jsii.Number:
        """The default number of instances in the DocDB cluster if none are specified.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "DEFAULT_NUM_INSTANCES")

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT_PORT")
    def DEFAULT_PORT(cls) -> jsii.Number:
        """The default port Document DB listens on.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "DEFAULT_PORT")

    @builtins.property
    @jsii.member(jsii_name="clusterEndpoint")
    def cluster_endpoint(self) -> "Endpoint":
        """The endpoint to use for read/write operations.

        stability
        :stability: experimental
        """
        return jsii.get(self, "clusterEndpoint")

    @builtins.property
    @jsii.member(jsii_name="clusterIdentifier")
    def cluster_identifier(self) -> str:
        """Identifier of the cluster.

        stability
        :stability: experimental
        """
        return jsii.get(self, "clusterIdentifier")

    @builtins.property
    @jsii.member(jsii_name="clusterReadEndpoint")
    def cluster_read_endpoint(self) -> "Endpoint":
        """Endpoint to use for load-balanced read-only operations.

        stability
        :stability: experimental
        """
        return jsii.get(self, "clusterReadEndpoint")

    @builtins.property
    @jsii.member(jsii_name="clusterResourceIdentifier")
    def cluster_resource_identifier(self) -> str:
        """The resource id for the cluster;

        for example: cluster-ABCD1234EFGH5678IJKL90MNOP. The cluster ID uniquely
        identifies the cluster and is used in things like IAM authentication policies.

        stability
        :stability: experimental
        attribute:
        :attribute:: ClusterResourceId
        """
        return jsii.get(self, "clusterResourceIdentifier")

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _Connections_231f38b5:
        """The connections object to implement IConectable.

        stability
        :stability: experimental
        """
        return jsii.get(self, "connections")

    @builtins.property
    @jsii.member(jsii_name="instanceEndpoints")
    def instance_endpoints(self) -> typing.List["Endpoint"]:
        """Endpoints which address each individual replica.

        stability
        :stability: experimental
        """
        return jsii.get(self, "instanceEndpoints")

    @builtins.property
    @jsii.member(jsii_name="instanceIdentifiers")
    def instance_identifiers(self) -> typing.List[str]:
        """Identifiers of the replicas.

        stability
        :stability: experimental
        """
        return jsii.get(self, "instanceIdentifiers")

    @builtins.property
    @jsii.member(jsii_name="securityGroupId")
    def security_group_id(self) -> str:
        """Security group identifier of this database.

        stability
        :stability: experimental
        """
        return jsii.get(self, "securityGroupId")

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> typing.Optional[_ISecret_75279d36]:
        """The secret attached to this cluster.

        stability
        :stability: experimental
        """
        return jsii.get(self, "secret")


@jsii.implements(IDatabaseInstance)
class DatabaseInstance(_Resource_884d0774, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_docdb.DatabaseInstance"):
    """A database instance.

    stability
    :stability: experimental
    resource:
    :resource:: AWS::DocDB::DBInstance
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, cluster: "IDatabaseCluster", instance_class: _InstanceType_85a97b30, auto_minor_version_upgrade: typing.Optional[bool]=None, availability_zone: typing.Optional[str]=None, db_instance_name: typing.Optional[str]=None, preferred_maintenance_window: typing.Optional[str]=None, removal_policy: typing.Optional[_RemovalPolicy_5986e9f3]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param cluster: The DocumentDB database cluster the instance should launch into.
        :param instance_class: The name of the compute and memory capacity classes.
        :param auto_minor_version_upgrade: Indicates that minor engine upgrades are applied automatically to the DB instance during the maintenance window. Default: true
        :param availability_zone: The name of the Availability Zone where the DB instance will be located. Default: - no preference
        :param db_instance_name: A name for the DB instance. If you specify a name, AWS CloudFormation converts it to lowercase. Default: - a CloudFormation generated name
        :param preferred_maintenance_window: The weekly time range (in UTC) during which system maintenance can occur. Format: ``ddd:hh24:mi-ddd:hh24:mi`` Constraint: Minimum 30-minute window Default: - a 30-minute window selected at random from an 8-hour block of time for each AWS Region, occurring on a random day of the week. To see the time blocks available, see https://docs.aws.amazon.com/documentdb/latest/developerguide/db-instance-maintain.html#maintenance-window
        :param removal_policy: The CloudFormation policy to apply when the instance is removed from the stack or replaced during an update. Default: RemovalPolicy.Retain

        stability
        :stability: experimental
        """
        props = DatabaseInstanceProps(cluster=cluster, instance_class=instance_class, auto_minor_version_upgrade=auto_minor_version_upgrade, availability_zone=availability_zone, db_instance_name=db_instance_name, preferred_maintenance_window=preferred_maintenance_window, removal_policy=removal_policy)

        jsii.create(DatabaseInstance, self, [scope, id, props])

    @jsii.member(jsii_name="fromDatabaseInstanceAttributes")
    @builtins.classmethod
    def from_database_instance_attributes(cls, scope: _Construct_f50a3f53, id: str, *, instance_endpoint_address: str, instance_identifier: str, port: jsii.Number) -> "IDatabaseInstance":
        """Import an existing database instance.

        :param scope: -
        :param id: -
        :param instance_endpoint_address: The endpoint address.
        :param instance_identifier: The instance identifier.
        :param port: The database port.

        stability
        :stability: experimental
        """
        attrs = DatabaseInstanceAttributes(instance_endpoint_address=instance_endpoint_address, instance_identifier=instance_identifier, port=port)

        return jsii.sinvoke(cls, "fromDatabaseInstanceAttributes", [scope, id, attrs])

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> "IDatabaseCluster":
        """The instance's database cluster.

        stability
        :stability: experimental
        """
        return jsii.get(self, "cluster")

    @builtins.property
    @jsii.member(jsii_name="dbInstanceEndpointAddress")
    def db_instance_endpoint_address(self) -> str:
        """The instance endpoint address.

        stability
        :stability: experimental
        inheritdoc:
        :inheritdoc:: true
        """
        return jsii.get(self, "dbInstanceEndpointAddress")

    @builtins.property
    @jsii.member(jsii_name="dbInstanceEndpointPort")
    def db_instance_endpoint_port(self) -> str:
        """The instance endpoint port.

        stability
        :stability: experimental
        inheritdoc:
        :inheritdoc:: true
        """
        return jsii.get(self, "dbInstanceEndpointPort")

    @builtins.property
    @jsii.member(jsii_name="instanceArn")
    def instance_arn(self) -> str:
        """The instance arn.

        stability
        :stability: experimental
        """
        return jsii.get(self, "instanceArn")

    @builtins.property
    @jsii.member(jsii_name="instanceEndpoint")
    def instance_endpoint(self) -> "Endpoint":
        """The instance endpoint.

        stability
        :stability: experimental
        inheritdoc:
        :inheritdoc:: true
        """
        return jsii.get(self, "instanceEndpoint")

    @builtins.property
    @jsii.member(jsii_name="instanceIdentifier")
    def instance_identifier(self) -> str:
        """The instance identifier.

        stability
        :stability: experimental
        inheritdoc:
        :inheritdoc:: true
        """
        return jsii.get(self, "instanceIdentifier")


__all__ = [
    "BackupProps",
    "CfnDBCluster",
    "CfnDBClusterParameterGroup",
    "CfnDBClusterParameterGroupProps",
    "CfnDBClusterProps",
    "CfnDBInstance",
    "CfnDBInstanceProps",
    "CfnDBSubnetGroup",
    "CfnDBSubnetGroupProps",
    "ClusterParameterGroup",
    "ClusterParameterGroupProps",
    "DatabaseCluster",
    "DatabaseClusterAttributes",
    "DatabaseClusterProps",
    "DatabaseInstance",
    "DatabaseInstanceAttributes",
    "DatabaseInstanceProps",
    "DatabaseSecret",
    "DatabaseSecretProps",
    "Endpoint",
    "IClusterParameterGroup",
    "IDatabaseCluster",
    "IDatabaseInstance",
    "InstanceProps",
    "Login",
    "RotationMultiUserOptions",
]

publication.publish()
