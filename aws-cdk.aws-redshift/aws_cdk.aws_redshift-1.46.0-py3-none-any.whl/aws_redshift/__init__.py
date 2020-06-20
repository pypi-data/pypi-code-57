"""
## Amazon Redshift Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

### Starting a Redshift Cluster Database

To set up a Redshift cluster, define a `Cluster`. It will be launched in a VPC.
You can specify a VPC, otherwise one will be created. The nodes are always launched in private subnets and are encrypted by default.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_redshift as redshift
cluster = redshift.Cluster(self, "Redshift",
    master_user=Login(
        master_username="admin"
    ),
    vpc=vpc
)
```

By default, the master password will be generated and stored in AWS Secrets Manager.

A default database named `default_db` will be created in the cluster. To change the name of this database set the `defaultDatabaseName` attribute in the constructor properties.

### Connecting

To control who can access the cluster, use the `.connections` attribute. Redshift Clusters have
a default port, so you don't need to specify the port:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cluster.connections.allow_from_any_ipv4("Open to the world")
```

The endpoint to access your database cluster will be available as the `.clusterEndpoint` attribute:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cluster.cluster_endpoint.socket_address
```

### Rotating credentials

When the master password is generated and stored in AWS Secrets Manager, it can be rotated automatically:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cluster.add_rotation_single_user()
```

The multi user rotation scheme is also available:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cluster.add_rotation_multi_user("MyUser",
    secret=my_imported_secret
)
```

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from ._jsii import *

import aws_cdk.aws_ec2
import aws_cdk.aws_iam
import aws_cdk.aws_kms
import aws_cdk.aws_s3
import aws_cdk.aws_secretsmanager
import aws_cdk.core


@jsii.implements(aws_cdk.core.IInspectable)
class CfnCluster(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-redshift.CfnCluster"):
    """A CloudFormation ``AWS::Redshift::Cluster``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html
    cloudformationResource:
    :cloudformationResource:: AWS::Redshift::Cluster
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, cluster_type: str, db_name: str, master_username: str, master_user_password: str, node_type: str, allow_version_upgrade: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]=None, automated_snapshot_retention_period: typing.Optional[jsii.Number]=None, availability_zone: typing.Optional[str]=None, cluster_identifier: typing.Optional[str]=None, cluster_parameter_group_name: typing.Optional[str]=None, cluster_security_groups: typing.Optional[typing.List[str]]=None, cluster_subnet_group_name: typing.Optional[str]=None, cluster_version: typing.Optional[str]=None, elastic_ip: typing.Optional[str]=None, encrypted: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]=None, hsm_client_certificate_identifier: typing.Optional[str]=None, hsm_configuration_identifier: typing.Optional[str]=None, iam_roles: typing.Optional[typing.List[str]]=None, kms_key_id: typing.Optional[str]=None, logging_properties: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "LoggingPropertiesProperty"]]=None, number_of_nodes: typing.Optional[jsii.Number]=None, owner_account: typing.Optional[str]=None, port: typing.Optional[jsii.Number]=None, preferred_maintenance_window: typing.Optional[str]=None, publicly_accessible: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]=None, snapshot_cluster_identifier: typing.Optional[str]=None, snapshot_identifier: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, vpc_security_group_ids: typing.Optional[typing.List[str]]=None) -> None:
        """Create a new ``AWS::Redshift::Cluster``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param cluster_type: ``AWS::Redshift::Cluster.ClusterType``.
        :param db_name: ``AWS::Redshift::Cluster.DBName``.
        :param master_username: ``AWS::Redshift::Cluster.MasterUsername``.
        :param master_user_password: ``AWS::Redshift::Cluster.MasterUserPassword``.
        :param node_type: ``AWS::Redshift::Cluster.NodeType``.
        :param allow_version_upgrade: ``AWS::Redshift::Cluster.AllowVersionUpgrade``.
        :param automated_snapshot_retention_period: ``AWS::Redshift::Cluster.AutomatedSnapshotRetentionPeriod``.
        :param availability_zone: ``AWS::Redshift::Cluster.AvailabilityZone``.
        :param cluster_identifier: ``AWS::Redshift::Cluster.ClusterIdentifier``.
        :param cluster_parameter_group_name: ``AWS::Redshift::Cluster.ClusterParameterGroupName``.
        :param cluster_security_groups: ``AWS::Redshift::Cluster.ClusterSecurityGroups``.
        :param cluster_subnet_group_name: ``AWS::Redshift::Cluster.ClusterSubnetGroupName``.
        :param cluster_version: ``AWS::Redshift::Cluster.ClusterVersion``.
        :param elastic_ip: ``AWS::Redshift::Cluster.ElasticIp``.
        :param encrypted: ``AWS::Redshift::Cluster.Encrypted``.
        :param hsm_client_certificate_identifier: ``AWS::Redshift::Cluster.HsmClientCertificateIdentifier``.
        :param hsm_configuration_identifier: ``AWS::Redshift::Cluster.HsmConfigurationIdentifier``.
        :param iam_roles: ``AWS::Redshift::Cluster.IamRoles``.
        :param kms_key_id: ``AWS::Redshift::Cluster.KmsKeyId``.
        :param logging_properties: ``AWS::Redshift::Cluster.LoggingProperties``.
        :param number_of_nodes: ``AWS::Redshift::Cluster.NumberOfNodes``.
        :param owner_account: ``AWS::Redshift::Cluster.OwnerAccount``.
        :param port: ``AWS::Redshift::Cluster.Port``.
        :param preferred_maintenance_window: ``AWS::Redshift::Cluster.PreferredMaintenanceWindow``.
        :param publicly_accessible: ``AWS::Redshift::Cluster.PubliclyAccessible``.
        :param snapshot_cluster_identifier: ``AWS::Redshift::Cluster.SnapshotClusterIdentifier``.
        :param snapshot_identifier: ``AWS::Redshift::Cluster.SnapshotIdentifier``.
        :param tags: ``AWS::Redshift::Cluster.Tags``.
        :param vpc_security_group_ids: ``AWS::Redshift::Cluster.VpcSecurityGroupIds``.
        """
        props = CfnClusterProps(cluster_type=cluster_type, db_name=db_name, master_username=master_username, master_user_password=master_user_password, node_type=node_type, allow_version_upgrade=allow_version_upgrade, automated_snapshot_retention_period=automated_snapshot_retention_period, availability_zone=availability_zone, cluster_identifier=cluster_identifier, cluster_parameter_group_name=cluster_parameter_group_name, cluster_security_groups=cluster_security_groups, cluster_subnet_group_name=cluster_subnet_group_name, cluster_version=cluster_version, elastic_ip=elastic_ip, encrypted=encrypted, hsm_client_certificate_identifier=hsm_client_certificate_identifier, hsm_configuration_identifier=hsm_configuration_identifier, iam_roles=iam_roles, kms_key_id=kms_key_id, logging_properties=logging_properties, number_of_nodes=number_of_nodes, owner_account=owner_account, port=port, preferred_maintenance_window=preferred_maintenance_window, publicly_accessible=publicly_accessible, snapshot_cluster_identifier=snapshot_cluster_identifier, snapshot_identifier=snapshot_identifier, tags=tags, vpc_security_group_ids=vpc_security_group_ids)

        jsii.create(CfnCluster, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnCluster":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
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
    @jsii.member(jsii_name="attrEndpointAddress")
    def attr_endpoint_address(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Endpoint.Address
        """
        return jsii.get(self, "attrEndpointAddress")

    @builtins.property
    @jsii.member(jsii_name="attrEndpointPort")
    def attr_endpoint_port(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Endpoint.Port
        """
        return jsii.get(self, "attrEndpointPort")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::Redshift::Cluster.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="clusterType")
    def cluster_type(self) -> str:
        """``AWS::Redshift::Cluster.ClusterType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-clustertype
        """
        return jsii.get(self, "clusterType")

    @cluster_type.setter
    def cluster_type(self, value: str) -> None:
        jsii.set(self, "clusterType", value)

    @builtins.property
    @jsii.member(jsii_name="dbName")
    def db_name(self) -> str:
        """``AWS::Redshift::Cluster.DBName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-dbname
        """
        return jsii.get(self, "dbName")

    @db_name.setter
    def db_name(self, value: str) -> None:
        jsii.set(self, "dbName", value)

    @builtins.property
    @jsii.member(jsii_name="masterUsername")
    def master_username(self) -> str:
        """``AWS::Redshift::Cluster.MasterUsername``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-masterusername
        """
        return jsii.get(self, "masterUsername")

    @master_username.setter
    def master_username(self, value: str) -> None:
        jsii.set(self, "masterUsername", value)

    @builtins.property
    @jsii.member(jsii_name="masterUserPassword")
    def master_user_password(self) -> str:
        """``AWS::Redshift::Cluster.MasterUserPassword``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-masteruserpassword
        """
        return jsii.get(self, "masterUserPassword")

    @master_user_password.setter
    def master_user_password(self, value: str) -> None:
        jsii.set(self, "masterUserPassword", value)

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> str:
        """``AWS::Redshift::Cluster.NodeType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-nodetype
        """
        return jsii.get(self, "nodeType")

    @node_type.setter
    def node_type(self, value: str) -> None:
        jsii.set(self, "nodeType", value)

    @builtins.property
    @jsii.member(jsii_name="allowVersionUpgrade")
    def allow_version_upgrade(self) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
        """``AWS::Redshift::Cluster.AllowVersionUpgrade``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-allowversionupgrade
        """
        return jsii.get(self, "allowVersionUpgrade")

    @allow_version_upgrade.setter
    def allow_version_upgrade(self, value: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]) -> None:
        jsii.set(self, "allowVersionUpgrade", value)

    @builtins.property
    @jsii.member(jsii_name="automatedSnapshotRetentionPeriod")
    def automated_snapshot_retention_period(self) -> typing.Optional[jsii.Number]:
        """``AWS::Redshift::Cluster.AutomatedSnapshotRetentionPeriod``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-automatedsnapshotretentionperiod
        """
        return jsii.get(self, "automatedSnapshotRetentionPeriod")

    @automated_snapshot_retention_period.setter
    def automated_snapshot_retention_period(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "automatedSnapshotRetentionPeriod", value)

    @builtins.property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> typing.Optional[str]:
        """``AWS::Redshift::Cluster.AvailabilityZone``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-availabilityzone
        """
        return jsii.get(self, "availabilityZone")

    @availability_zone.setter
    def availability_zone(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "availabilityZone", value)

    @builtins.property
    @jsii.member(jsii_name="clusterIdentifier")
    def cluster_identifier(self) -> typing.Optional[str]:
        """``AWS::Redshift::Cluster.ClusterIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-clusteridentifier
        """
        return jsii.get(self, "clusterIdentifier")

    @cluster_identifier.setter
    def cluster_identifier(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "clusterIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="clusterParameterGroupName")
    def cluster_parameter_group_name(self) -> typing.Optional[str]:
        """``AWS::Redshift::Cluster.ClusterParameterGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-clusterparametergroupname
        """
        return jsii.get(self, "clusterParameterGroupName")

    @cluster_parameter_group_name.setter
    def cluster_parameter_group_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "clusterParameterGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="clusterSecurityGroups")
    def cluster_security_groups(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Redshift::Cluster.ClusterSecurityGroups``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-clustersecuritygroups
        """
        return jsii.get(self, "clusterSecurityGroups")

    @cluster_security_groups.setter
    def cluster_security_groups(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "clusterSecurityGroups", value)

    @builtins.property
    @jsii.member(jsii_name="clusterSubnetGroupName")
    def cluster_subnet_group_name(self) -> typing.Optional[str]:
        """``AWS::Redshift::Cluster.ClusterSubnetGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-clustersubnetgroupname
        """
        return jsii.get(self, "clusterSubnetGroupName")

    @cluster_subnet_group_name.setter
    def cluster_subnet_group_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "clusterSubnetGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="clusterVersion")
    def cluster_version(self) -> typing.Optional[str]:
        """``AWS::Redshift::Cluster.ClusterVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-clusterversion
        """
        return jsii.get(self, "clusterVersion")

    @cluster_version.setter
    def cluster_version(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "clusterVersion", value)

    @builtins.property
    @jsii.member(jsii_name="elasticIp")
    def elastic_ip(self) -> typing.Optional[str]:
        """``AWS::Redshift::Cluster.ElasticIp``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-elasticip
        """
        return jsii.get(self, "elasticIp")

    @elastic_ip.setter
    def elastic_ip(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "elasticIp", value)

    @builtins.property
    @jsii.member(jsii_name="encrypted")
    def encrypted(self) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
        """``AWS::Redshift::Cluster.Encrypted``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-encrypted
        """
        return jsii.get(self, "encrypted")

    @encrypted.setter
    def encrypted(self, value: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]) -> None:
        jsii.set(self, "encrypted", value)

    @builtins.property
    @jsii.member(jsii_name="hsmClientCertificateIdentifier")
    def hsm_client_certificate_identifier(self) -> typing.Optional[str]:
        """``AWS::Redshift::Cluster.HsmClientCertificateIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-hsmclientcertidentifier
        """
        return jsii.get(self, "hsmClientCertificateIdentifier")

    @hsm_client_certificate_identifier.setter
    def hsm_client_certificate_identifier(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "hsmClientCertificateIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="hsmConfigurationIdentifier")
    def hsm_configuration_identifier(self) -> typing.Optional[str]:
        """``AWS::Redshift::Cluster.HsmConfigurationIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-HsmConfigurationIdentifier
        """
        return jsii.get(self, "hsmConfigurationIdentifier")

    @hsm_configuration_identifier.setter
    def hsm_configuration_identifier(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "hsmConfigurationIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="iamRoles")
    def iam_roles(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Redshift::Cluster.IamRoles``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-iamroles
        """
        return jsii.get(self, "iamRoles")

    @iam_roles.setter
    def iam_roles(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "iamRoles", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> typing.Optional[str]:
        """``AWS::Redshift::Cluster.KmsKeyId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-kmskeyid
        """
        return jsii.get(self, "kmsKeyId")

    @kms_key_id.setter
    def kms_key_id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "kmsKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="loggingProperties")
    def logging_properties(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "LoggingPropertiesProperty"]]:
        """``AWS::Redshift::Cluster.LoggingProperties``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-loggingproperties
        """
        return jsii.get(self, "loggingProperties")

    @logging_properties.setter
    def logging_properties(self, value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "LoggingPropertiesProperty"]]) -> None:
        jsii.set(self, "loggingProperties", value)

    @builtins.property
    @jsii.member(jsii_name="numberOfNodes")
    def number_of_nodes(self) -> typing.Optional[jsii.Number]:
        """``AWS::Redshift::Cluster.NumberOfNodes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-nodetype
        """
        return jsii.get(self, "numberOfNodes")

    @number_of_nodes.setter
    def number_of_nodes(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "numberOfNodes", value)

    @builtins.property
    @jsii.member(jsii_name="ownerAccount")
    def owner_account(self) -> typing.Optional[str]:
        """``AWS::Redshift::Cluster.OwnerAccount``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-owneraccount
        """
        return jsii.get(self, "ownerAccount")

    @owner_account.setter
    def owner_account(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "ownerAccount", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> typing.Optional[jsii.Number]:
        """``AWS::Redshift::Cluster.Port``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-port
        """
        return jsii.get(self, "port")

    @port.setter
    def port(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "port", value)

    @builtins.property
    @jsii.member(jsii_name="preferredMaintenanceWindow")
    def preferred_maintenance_window(self) -> typing.Optional[str]:
        """``AWS::Redshift::Cluster.PreferredMaintenanceWindow``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-preferredmaintenancewindow
        """
        return jsii.get(self, "preferredMaintenanceWindow")

    @preferred_maintenance_window.setter
    def preferred_maintenance_window(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "preferredMaintenanceWindow", value)

    @builtins.property
    @jsii.member(jsii_name="publiclyAccessible")
    def publicly_accessible(self) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
        """``AWS::Redshift::Cluster.PubliclyAccessible``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-publiclyaccessible
        """
        return jsii.get(self, "publiclyAccessible")

    @publicly_accessible.setter
    def publicly_accessible(self, value: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]) -> None:
        jsii.set(self, "publiclyAccessible", value)

    @builtins.property
    @jsii.member(jsii_name="snapshotClusterIdentifier")
    def snapshot_cluster_identifier(self) -> typing.Optional[str]:
        """``AWS::Redshift::Cluster.SnapshotClusterIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-snapshotclusteridentifier
        """
        return jsii.get(self, "snapshotClusterIdentifier")

    @snapshot_cluster_identifier.setter
    def snapshot_cluster_identifier(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "snapshotClusterIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="snapshotIdentifier")
    def snapshot_identifier(self) -> typing.Optional[str]:
        """``AWS::Redshift::Cluster.SnapshotIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-snapshotidentifier
        """
        return jsii.get(self, "snapshotIdentifier")

    @snapshot_identifier.setter
    def snapshot_identifier(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "snapshotIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="vpcSecurityGroupIds")
    def vpc_security_group_ids(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Redshift::Cluster.VpcSecurityGroupIds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-vpcsecuritygroupids
        """
        return jsii.get(self, "vpcSecurityGroupIds")

    @vpc_security_group_ids.setter
    def vpc_security_group_ids(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "vpcSecurityGroupIds", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-redshift.CfnCluster.LoggingPropertiesProperty", jsii_struct_bases=[], name_mapping={'bucket_name': 'bucketName', 's3_key_prefix': 's3KeyPrefix'})
    class LoggingPropertiesProperty():
        def __init__(self, *, bucket_name: str, s3_key_prefix: typing.Optional[str]=None) -> None:
            """
            :param bucket_name: ``CfnCluster.LoggingPropertiesProperty.BucketName``.
            :param s3_key_prefix: ``CfnCluster.LoggingPropertiesProperty.S3KeyPrefix``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshift-cluster-loggingproperties.html
            """
            self._values = {
                'bucket_name': bucket_name,
            }
            if s3_key_prefix is not None: self._values["s3_key_prefix"] = s3_key_prefix

        @builtins.property
        def bucket_name(self) -> str:
            """``CfnCluster.LoggingPropertiesProperty.BucketName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshift-cluster-loggingproperties.html#cfn-redshift-cluster-loggingproperties-bucketname
            """
            return self._values.get('bucket_name')

        @builtins.property
        def s3_key_prefix(self) -> typing.Optional[str]:
            """``CfnCluster.LoggingPropertiesProperty.S3KeyPrefix``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-redshift-cluster-loggingproperties.html#cfn-redshift-cluster-loggingproperties-s3keyprefix
            """
            return self._values.get('s3_key_prefix')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'LoggingPropertiesProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.implements(aws_cdk.core.IInspectable)
class CfnClusterParameterGroup(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-redshift.CfnClusterParameterGroup"):
    """A CloudFormation ``AWS::Redshift::ClusterParameterGroup``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clusterparametergroup.html
    cloudformationResource:
    :cloudformationResource:: AWS::Redshift::ClusterParameterGroup
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, description: str, parameter_group_family: str, parameters: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["ParameterProperty", aws_cdk.core.IResolvable]]]]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None) -> None:
        """Create a new ``AWS::Redshift::ClusterParameterGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: ``AWS::Redshift::ClusterParameterGroup.Description``.
        :param parameter_group_family: ``AWS::Redshift::ClusterParameterGroup.ParameterGroupFamily``.
        :param parameters: ``AWS::Redshift::ClusterParameterGroup.Parameters``.
        :param tags: ``AWS::Redshift::ClusterParameterGroup.Tags``.
        """
        props = CfnClusterParameterGroupProps(description=description, parameter_group_family=parameter_group_family, parameters=parameters, tags=tags)

        jsii.create(CfnClusterParameterGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnClusterParameterGroup":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
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
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::Redshift::ClusterParameterGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clusterparametergroup.html#cfn-redshift-clusterparametergroup-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> str:
        """``AWS::Redshift::ClusterParameterGroup.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clusterparametergroup.html#cfn-redshift-clusterparametergroup-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: str) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="parameterGroupFamily")
    def parameter_group_family(self) -> str:
        """``AWS::Redshift::ClusterParameterGroup.ParameterGroupFamily``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clusterparametergroup.html#cfn-redshift-clusterparametergroup-parametergroupfamily
        """
        return jsii.get(self, "parameterGroupFamily")

    @parameter_group_family.setter
    def parameter_group_family(self, value: str) -> None:
        jsii.set(self, "parameterGroupFamily", value)

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["ParameterProperty", aws_cdk.core.IResolvable]]]]:
        """``AWS::Redshift::ClusterParameterGroup.Parameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clusterparametergroup.html#cfn-redshift-clusterparametergroup-parameters
        """
        return jsii.get(self, "parameters")

    @parameters.setter
    def parameters(self, value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["ParameterProperty", aws_cdk.core.IResolvable]]]]) -> None:
        jsii.set(self, "parameters", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-redshift.CfnClusterParameterGroup.ParameterProperty", jsii_struct_bases=[], name_mapping={'parameter_name': 'parameterName', 'parameter_value': 'parameterValue'})
    class ParameterProperty():
        def __init__(self, *, parameter_name: str, parameter_value: str) -> None:
            """
            :param parameter_name: ``CfnClusterParameterGroup.ParameterProperty.ParameterName``.
            :param parameter_value: ``CfnClusterParameterGroup.ParameterProperty.ParameterValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-property-redshift-clusterparametergroup-parameter.html
            """
            self._values = {
                'parameter_name': parameter_name,
                'parameter_value': parameter_value,
            }

        @builtins.property
        def parameter_name(self) -> str:
            """``CfnClusterParameterGroup.ParameterProperty.ParameterName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-property-redshift-clusterparametergroup-parameter.html#cfn-redshift-clusterparametergroup-parameter-parametername
            """
            return self._values.get('parameter_name')

        @builtins.property
        def parameter_value(self) -> str:
            """``CfnClusterParameterGroup.ParameterProperty.ParameterValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-property-redshift-clusterparametergroup-parameter.html#cfn-redshift-clusterparametergroup-parameter-parametervalue
            """
            return self._values.get('parameter_value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ParameterProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-redshift.CfnClusterParameterGroupProps", jsii_struct_bases=[], name_mapping={'description': 'description', 'parameter_group_family': 'parameterGroupFamily', 'parameters': 'parameters', 'tags': 'tags'})
class CfnClusterParameterGroupProps():
    def __init__(self, *, description: str, parameter_group_family: str, parameters: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnClusterParameterGroup.ParameterProperty", aws_cdk.core.IResolvable]]]]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None) -> None:
        """Properties for defining a ``AWS::Redshift::ClusterParameterGroup``.

        :param description: ``AWS::Redshift::ClusterParameterGroup.Description``.
        :param parameter_group_family: ``AWS::Redshift::ClusterParameterGroup.ParameterGroupFamily``.
        :param parameters: ``AWS::Redshift::ClusterParameterGroup.Parameters``.
        :param tags: ``AWS::Redshift::ClusterParameterGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clusterparametergroup.html
        """
        self._values = {
            'description': description,
            'parameter_group_family': parameter_group_family,
        }
        if parameters is not None: self._values["parameters"] = parameters
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def description(self) -> str:
        """``AWS::Redshift::ClusterParameterGroup.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clusterparametergroup.html#cfn-redshift-clusterparametergroup-description
        """
        return self._values.get('description')

    @builtins.property
    def parameter_group_family(self) -> str:
        """``AWS::Redshift::ClusterParameterGroup.ParameterGroupFamily``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clusterparametergroup.html#cfn-redshift-clusterparametergroup-parametergroupfamily
        """
        return self._values.get('parameter_group_family')

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnClusterParameterGroup.ParameterProperty", aws_cdk.core.IResolvable]]]]:
        """``AWS::Redshift::ClusterParameterGroup.Parameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clusterparametergroup.html#cfn-redshift-clusterparametergroup-parameters
        """
        return self._values.get('parameters')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::Redshift::ClusterParameterGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clusterparametergroup.html#cfn-redshift-clusterparametergroup-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnClusterParameterGroupProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-redshift.CfnClusterProps", jsii_struct_bases=[], name_mapping={'cluster_type': 'clusterType', 'db_name': 'dbName', 'master_username': 'masterUsername', 'master_user_password': 'masterUserPassword', 'node_type': 'nodeType', 'allow_version_upgrade': 'allowVersionUpgrade', 'automated_snapshot_retention_period': 'automatedSnapshotRetentionPeriod', 'availability_zone': 'availabilityZone', 'cluster_identifier': 'clusterIdentifier', 'cluster_parameter_group_name': 'clusterParameterGroupName', 'cluster_security_groups': 'clusterSecurityGroups', 'cluster_subnet_group_name': 'clusterSubnetGroupName', 'cluster_version': 'clusterVersion', 'elastic_ip': 'elasticIp', 'encrypted': 'encrypted', 'hsm_client_certificate_identifier': 'hsmClientCertificateIdentifier', 'hsm_configuration_identifier': 'hsmConfigurationIdentifier', 'iam_roles': 'iamRoles', 'kms_key_id': 'kmsKeyId', 'logging_properties': 'loggingProperties', 'number_of_nodes': 'numberOfNodes', 'owner_account': 'ownerAccount', 'port': 'port', 'preferred_maintenance_window': 'preferredMaintenanceWindow', 'publicly_accessible': 'publiclyAccessible', 'snapshot_cluster_identifier': 'snapshotClusterIdentifier', 'snapshot_identifier': 'snapshotIdentifier', 'tags': 'tags', 'vpc_security_group_ids': 'vpcSecurityGroupIds'})
class CfnClusterProps():
    def __init__(self, *, cluster_type: str, db_name: str, master_username: str, master_user_password: str, node_type: str, allow_version_upgrade: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]=None, automated_snapshot_retention_period: typing.Optional[jsii.Number]=None, availability_zone: typing.Optional[str]=None, cluster_identifier: typing.Optional[str]=None, cluster_parameter_group_name: typing.Optional[str]=None, cluster_security_groups: typing.Optional[typing.List[str]]=None, cluster_subnet_group_name: typing.Optional[str]=None, cluster_version: typing.Optional[str]=None, elastic_ip: typing.Optional[str]=None, encrypted: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]=None, hsm_client_certificate_identifier: typing.Optional[str]=None, hsm_configuration_identifier: typing.Optional[str]=None, iam_roles: typing.Optional[typing.List[str]]=None, kms_key_id: typing.Optional[str]=None, logging_properties: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCluster.LoggingPropertiesProperty"]]=None, number_of_nodes: typing.Optional[jsii.Number]=None, owner_account: typing.Optional[str]=None, port: typing.Optional[jsii.Number]=None, preferred_maintenance_window: typing.Optional[str]=None, publicly_accessible: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]=None, snapshot_cluster_identifier: typing.Optional[str]=None, snapshot_identifier: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, vpc_security_group_ids: typing.Optional[typing.List[str]]=None) -> None:
        """Properties for defining a ``AWS::Redshift::Cluster``.

        :param cluster_type: ``AWS::Redshift::Cluster.ClusterType``.
        :param db_name: ``AWS::Redshift::Cluster.DBName``.
        :param master_username: ``AWS::Redshift::Cluster.MasterUsername``.
        :param master_user_password: ``AWS::Redshift::Cluster.MasterUserPassword``.
        :param node_type: ``AWS::Redshift::Cluster.NodeType``.
        :param allow_version_upgrade: ``AWS::Redshift::Cluster.AllowVersionUpgrade``.
        :param automated_snapshot_retention_period: ``AWS::Redshift::Cluster.AutomatedSnapshotRetentionPeriod``.
        :param availability_zone: ``AWS::Redshift::Cluster.AvailabilityZone``.
        :param cluster_identifier: ``AWS::Redshift::Cluster.ClusterIdentifier``.
        :param cluster_parameter_group_name: ``AWS::Redshift::Cluster.ClusterParameterGroupName``.
        :param cluster_security_groups: ``AWS::Redshift::Cluster.ClusterSecurityGroups``.
        :param cluster_subnet_group_name: ``AWS::Redshift::Cluster.ClusterSubnetGroupName``.
        :param cluster_version: ``AWS::Redshift::Cluster.ClusterVersion``.
        :param elastic_ip: ``AWS::Redshift::Cluster.ElasticIp``.
        :param encrypted: ``AWS::Redshift::Cluster.Encrypted``.
        :param hsm_client_certificate_identifier: ``AWS::Redshift::Cluster.HsmClientCertificateIdentifier``.
        :param hsm_configuration_identifier: ``AWS::Redshift::Cluster.HsmConfigurationIdentifier``.
        :param iam_roles: ``AWS::Redshift::Cluster.IamRoles``.
        :param kms_key_id: ``AWS::Redshift::Cluster.KmsKeyId``.
        :param logging_properties: ``AWS::Redshift::Cluster.LoggingProperties``.
        :param number_of_nodes: ``AWS::Redshift::Cluster.NumberOfNodes``.
        :param owner_account: ``AWS::Redshift::Cluster.OwnerAccount``.
        :param port: ``AWS::Redshift::Cluster.Port``.
        :param preferred_maintenance_window: ``AWS::Redshift::Cluster.PreferredMaintenanceWindow``.
        :param publicly_accessible: ``AWS::Redshift::Cluster.PubliclyAccessible``.
        :param snapshot_cluster_identifier: ``AWS::Redshift::Cluster.SnapshotClusterIdentifier``.
        :param snapshot_identifier: ``AWS::Redshift::Cluster.SnapshotIdentifier``.
        :param tags: ``AWS::Redshift::Cluster.Tags``.
        :param vpc_security_group_ids: ``AWS::Redshift::Cluster.VpcSecurityGroupIds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html
        """
        self._values = {
            'cluster_type': cluster_type,
            'db_name': db_name,
            'master_username': master_username,
            'master_user_password': master_user_password,
            'node_type': node_type,
        }
        if allow_version_upgrade is not None: self._values["allow_version_upgrade"] = allow_version_upgrade
        if automated_snapshot_retention_period is not None: self._values["automated_snapshot_retention_period"] = automated_snapshot_retention_period
        if availability_zone is not None: self._values["availability_zone"] = availability_zone
        if cluster_identifier is not None: self._values["cluster_identifier"] = cluster_identifier
        if cluster_parameter_group_name is not None: self._values["cluster_parameter_group_name"] = cluster_parameter_group_name
        if cluster_security_groups is not None: self._values["cluster_security_groups"] = cluster_security_groups
        if cluster_subnet_group_name is not None: self._values["cluster_subnet_group_name"] = cluster_subnet_group_name
        if cluster_version is not None: self._values["cluster_version"] = cluster_version
        if elastic_ip is not None: self._values["elastic_ip"] = elastic_ip
        if encrypted is not None: self._values["encrypted"] = encrypted
        if hsm_client_certificate_identifier is not None: self._values["hsm_client_certificate_identifier"] = hsm_client_certificate_identifier
        if hsm_configuration_identifier is not None: self._values["hsm_configuration_identifier"] = hsm_configuration_identifier
        if iam_roles is not None: self._values["iam_roles"] = iam_roles
        if kms_key_id is not None: self._values["kms_key_id"] = kms_key_id
        if logging_properties is not None: self._values["logging_properties"] = logging_properties
        if number_of_nodes is not None: self._values["number_of_nodes"] = number_of_nodes
        if owner_account is not None: self._values["owner_account"] = owner_account
        if port is not None: self._values["port"] = port
        if preferred_maintenance_window is not None: self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if publicly_accessible is not None: self._values["publicly_accessible"] = publicly_accessible
        if snapshot_cluster_identifier is not None: self._values["snapshot_cluster_identifier"] = snapshot_cluster_identifier
        if snapshot_identifier is not None: self._values["snapshot_identifier"] = snapshot_identifier
        if tags is not None: self._values["tags"] = tags
        if vpc_security_group_ids is not None: self._values["vpc_security_group_ids"] = vpc_security_group_ids

    @builtins.property
    def cluster_type(self) -> str:
        """``AWS::Redshift::Cluster.ClusterType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-clustertype
        """
        return self._values.get('cluster_type')

    @builtins.property
    def db_name(self) -> str:
        """``AWS::Redshift::Cluster.DBName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-dbname
        """
        return self._values.get('db_name')

    @builtins.property
    def master_username(self) -> str:
        """``AWS::Redshift::Cluster.MasterUsername``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-masterusername
        """
        return self._values.get('master_username')

    @builtins.property
    def master_user_password(self) -> str:
        """``AWS::Redshift::Cluster.MasterUserPassword``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-masteruserpassword
        """
        return self._values.get('master_user_password')

    @builtins.property
    def node_type(self) -> str:
        """``AWS::Redshift::Cluster.NodeType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-nodetype
        """
        return self._values.get('node_type')

    @builtins.property
    def allow_version_upgrade(self) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
        """``AWS::Redshift::Cluster.AllowVersionUpgrade``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-allowversionupgrade
        """
        return self._values.get('allow_version_upgrade')

    @builtins.property
    def automated_snapshot_retention_period(self) -> typing.Optional[jsii.Number]:
        """``AWS::Redshift::Cluster.AutomatedSnapshotRetentionPeriod``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-automatedsnapshotretentionperiod
        """
        return self._values.get('automated_snapshot_retention_period')

    @builtins.property
    def availability_zone(self) -> typing.Optional[str]:
        """``AWS::Redshift::Cluster.AvailabilityZone``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-availabilityzone
        """
        return self._values.get('availability_zone')

    @builtins.property
    def cluster_identifier(self) -> typing.Optional[str]:
        """``AWS::Redshift::Cluster.ClusterIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-clusteridentifier
        """
        return self._values.get('cluster_identifier')

    @builtins.property
    def cluster_parameter_group_name(self) -> typing.Optional[str]:
        """``AWS::Redshift::Cluster.ClusterParameterGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-clusterparametergroupname
        """
        return self._values.get('cluster_parameter_group_name')

    @builtins.property
    def cluster_security_groups(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Redshift::Cluster.ClusterSecurityGroups``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-clustersecuritygroups
        """
        return self._values.get('cluster_security_groups')

    @builtins.property
    def cluster_subnet_group_name(self) -> typing.Optional[str]:
        """``AWS::Redshift::Cluster.ClusterSubnetGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-clustersubnetgroupname
        """
        return self._values.get('cluster_subnet_group_name')

    @builtins.property
    def cluster_version(self) -> typing.Optional[str]:
        """``AWS::Redshift::Cluster.ClusterVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-clusterversion
        """
        return self._values.get('cluster_version')

    @builtins.property
    def elastic_ip(self) -> typing.Optional[str]:
        """``AWS::Redshift::Cluster.ElasticIp``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-elasticip
        """
        return self._values.get('elastic_ip')

    @builtins.property
    def encrypted(self) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
        """``AWS::Redshift::Cluster.Encrypted``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-encrypted
        """
        return self._values.get('encrypted')

    @builtins.property
    def hsm_client_certificate_identifier(self) -> typing.Optional[str]:
        """``AWS::Redshift::Cluster.HsmClientCertificateIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-hsmclientcertidentifier
        """
        return self._values.get('hsm_client_certificate_identifier')

    @builtins.property
    def hsm_configuration_identifier(self) -> typing.Optional[str]:
        """``AWS::Redshift::Cluster.HsmConfigurationIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-HsmConfigurationIdentifier
        """
        return self._values.get('hsm_configuration_identifier')

    @builtins.property
    def iam_roles(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Redshift::Cluster.IamRoles``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-iamroles
        """
        return self._values.get('iam_roles')

    @builtins.property
    def kms_key_id(self) -> typing.Optional[str]:
        """``AWS::Redshift::Cluster.KmsKeyId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-kmskeyid
        """
        return self._values.get('kms_key_id')

    @builtins.property
    def logging_properties(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCluster.LoggingPropertiesProperty"]]:
        """``AWS::Redshift::Cluster.LoggingProperties``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-loggingproperties
        """
        return self._values.get('logging_properties')

    @builtins.property
    def number_of_nodes(self) -> typing.Optional[jsii.Number]:
        """``AWS::Redshift::Cluster.NumberOfNodes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-nodetype
        """
        return self._values.get('number_of_nodes')

    @builtins.property
    def owner_account(self) -> typing.Optional[str]:
        """``AWS::Redshift::Cluster.OwnerAccount``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-owneraccount
        """
        return self._values.get('owner_account')

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        """``AWS::Redshift::Cluster.Port``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-port
        """
        return self._values.get('port')

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[str]:
        """``AWS::Redshift::Cluster.PreferredMaintenanceWindow``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-preferredmaintenancewindow
        """
        return self._values.get('preferred_maintenance_window')

    @builtins.property
    def publicly_accessible(self) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
        """``AWS::Redshift::Cluster.PubliclyAccessible``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-publiclyaccessible
        """
        return self._values.get('publicly_accessible')

    @builtins.property
    def snapshot_cluster_identifier(self) -> typing.Optional[str]:
        """``AWS::Redshift::Cluster.SnapshotClusterIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-snapshotclusteridentifier
        """
        return self._values.get('snapshot_cluster_identifier')

    @builtins.property
    def snapshot_identifier(self) -> typing.Optional[str]:
        """``AWS::Redshift::Cluster.SnapshotIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-snapshotidentifier
        """
        return self._values.get('snapshot_identifier')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::Redshift::Cluster.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-tags
        """
        return self._values.get('tags')

    @builtins.property
    def vpc_security_group_ids(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Redshift::Cluster.VpcSecurityGroupIds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-cluster.html#cfn-redshift-cluster-vpcsecuritygroupids
        """
        return self._values.get('vpc_security_group_ids')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnClusterProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnClusterSecurityGroup(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-redshift.CfnClusterSecurityGroup"):
    """A CloudFormation ``AWS::Redshift::ClusterSecurityGroup``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersecuritygroup.html
    cloudformationResource:
    :cloudformationResource:: AWS::Redshift::ClusterSecurityGroup
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, description: str, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None) -> None:
        """Create a new ``AWS::Redshift::ClusterSecurityGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: ``AWS::Redshift::ClusterSecurityGroup.Description``.
        :param tags: ``AWS::Redshift::ClusterSecurityGroup.Tags``.
        """
        props = CfnClusterSecurityGroupProps(description=description, tags=tags)

        jsii.create(CfnClusterSecurityGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnClusterSecurityGroup":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
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
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::Redshift::ClusterSecurityGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersecuritygroup.html#cfn-redshift-clustersecuritygroup-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> str:
        """``AWS::Redshift::ClusterSecurityGroup.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersecuritygroup.html#cfn-redshift-clustersecuritygroup-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: str) -> None:
        jsii.set(self, "description", value)


@jsii.implements(aws_cdk.core.IInspectable)
class CfnClusterSecurityGroupIngress(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-redshift.CfnClusterSecurityGroupIngress"):
    """A CloudFormation ``AWS::Redshift::ClusterSecurityGroupIngress``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersecuritygroupingress.html
    cloudformationResource:
    :cloudformationResource:: AWS::Redshift::ClusterSecurityGroupIngress
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, cluster_security_group_name: str, cidrip: typing.Optional[str]=None, ec2_security_group_name: typing.Optional[str]=None, ec2_security_group_owner_id: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::Redshift::ClusterSecurityGroupIngress``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param cluster_security_group_name: ``AWS::Redshift::ClusterSecurityGroupIngress.ClusterSecurityGroupName``.
        :param cidrip: ``AWS::Redshift::ClusterSecurityGroupIngress.CIDRIP``.
        :param ec2_security_group_name: ``AWS::Redshift::ClusterSecurityGroupIngress.EC2SecurityGroupName``.
        :param ec2_security_group_owner_id: ``AWS::Redshift::ClusterSecurityGroupIngress.EC2SecurityGroupOwnerId``.
        """
        props = CfnClusterSecurityGroupIngressProps(cluster_security_group_name=cluster_security_group_name, cidrip=cidrip, ec2_security_group_name=ec2_security_group_name, ec2_security_group_owner_id=ec2_security_group_owner_id)

        jsii.create(CfnClusterSecurityGroupIngress, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnClusterSecurityGroupIngress":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
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
    @jsii.member(jsii_name="clusterSecurityGroupName")
    def cluster_security_group_name(self) -> str:
        """``AWS::Redshift::ClusterSecurityGroupIngress.ClusterSecurityGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersecuritygroupingress.html#cfn-redshift-clustersecuritygroupingress-clustersecuritygroupname
        """
        return jsii.get(self, "clusterSecurityGroupName")

    @cluster_security_group_name.setter
    def cluster_security_group_name(self, value: str) -> None:
        jsii.set(self, "clusterSecurityGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="cidrip")
    def cidrip(self) -> typing.Optional[str]:
        """``AWS::Redshift::ClusterSecurityGroupIngress.CIDRIP``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersecuritygroupingress.html#cfn-redshift-clustersecuritygroupingress-cidrip
        """
        return jsii.get(self, "cidrip")

    @cidrip.setter
    def cidrip(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "cidrip", value)

    @builtins.property
    @jsii.member(jsii_name="ec2SecurityGroupName")
    def ec2_security_group_name(self) -> typing.Optional[str]:
        """``AWS::Redshift::ClusterSecurityGroupIngress.EC2SecurityGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersecuritygroupingress.html#cfn-redshift-clustersecuritygroupingress-ec2securitygroupname
        """
        return jsii.get(self, "ec2SecurityGroupName")

    @ec2_security_group_name.setter
    def ec2_security_group_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "ec2SecurityGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="ec2SecurityGroupOwnerId")
    def ec2_security_group_owner_id(self) -> typing.Optional[str]:
        """``AWS::Redshift::ClusterSecurityGroupIngress.EC2SecurityGroupOwnerId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersecuritygroupingress.html#cfn-redshift-clustersecuritygroupingress-ec2securitygroupownerid
        """
        return jsii.get(self, "ec2SecurityGroupOwnerId")

    @ec2_security_group_owner_id.setter
    def ec2_security_group_owner_id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "ec2SecurityGroupOwnerId", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-redshift.CfnClusterSecurityGroupIngressProps", jsii_struct_bases=[], name_mapping={'cluster_security_group_name': 'clusterSecurityGroupName', 'cidrip': 'cidrip', 'ec2_security_group_name': 'ec2SecurityGroupName', 'ec2_security_group_owner_id': 'ec2SecurityGroupOwnerId'})
class CfnClusterSecurityGroupIngressProps():
    def __init__(self, *, cluster_security_group_name: str, cidrip: typing.Optional[str]=None, ec2_security_group_name: typing.Optional[str]=None, ec2_security_group_owner_id: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::Redshift::ClusterSecurityGroupIngress``.

        :param cluster_security_group_name: ``AWS::Redshift::ClusterSecurityGroupIngress.ClusterSecurityGroupName``.
        :param cidrip: ``AWS::Redshift::ClusterSecurityGroupIngress.CIDRIP``.
        :param ec2_security_group_name: ``AWS::Redshift::ClusterSecurityGroupIngress.EC2SecurityGroupName``.
        :param ec2_security_group_owner_id: ``AWS::Redshift::ClusterSecurityGroupIngress.EC2SecurityGroupOwnerId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersecuritygroupingress.html
        """
        self._values = {
            'cluster_security_group_name': cluster_security_group_name,
        }
        if cidrip is not None: self._values["cidrip"] = cidrip
        if ec2_security_group_name is not None: self._values["ec2_security_group_name"] = ec2_security_group_name
        if ec2_security_group_owner_id is not None: self._values["ec2_security_group_owner_id"] = ec2_security_group_owner_id

    @builtins.property
    def cluster_security_group_name(self) -> str:
        """``AWS::Redshift::ClusterSecurityGroupIngress.ClusterSecurityGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersecuritygroupingress.html#cfn-redshift-clustersecuritygroupingress-clustersecuritygroupname
        """
        return self._values.get('cluster_security_group_name')

    @builtins.property
    def cidrip(self) -> typing.Optional[str]:
        """``AWS::Redshift::ClusterSecurityGroupIngress.CIDRIP``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersecuritygroupingress.html#cfn-redshift-clustersecuritygroupingress-cidrip
        """
        return self._values.get('cidrip')

    @builtins.property
    def ec2_security_group_name(self) -> typing.Optional[str]:
        """``AWS::Redshift::ClusterSecurityGroupIngress.EC2SecurityGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersecuritygroupingress.html#cfn-redshift-clustersecuritygroupingress-ec2securitygroupname
        """
        return self._values.get('ec2_security_group_name')

    @builtins.property
    def ec2_security_group_owner_id(self) -> typing.Optional[str]:
        """``AWS::Redshift::ClusterSecurityGroupIngress.EC2SecurityGroupOwnerId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersecuritygroupingress.html#cfn-redshift-clustersecuritygroupingress-ec2securitygroupownerid
        """
        return self._values.get('ec2_security_group_owner_id')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnClusterSecurityGroupIngressProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-redshift.CfnClusterSecurityGroupProps", jsii_struct_bases=[], name_mapping={'description': 'description', 'tags': 'tags'})
class CfnClusterSecurityGroupProps():
    def __init__(self, *, description: str, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None) -> None:
        """Properties for defining a ``AWS::Redshift::ClusterSecurityGroup``.

        :param description: ``AWS::Redshift::ClusterSecurityGroup.Description``.
        :param tags: ``AWS::Redshift::ClusterSecurityGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersecuritygroup.html
        """
        self._values = {
            'description': description,
        }
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def description(self) -> str:
        """``AWS::Redshift::ClusterSecurityGroup.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersecuritygroup.html#cfn-redshift-clustersecuritygroup-description
        """
        return self._values.get('description')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::Redshift::ClusterSecurityGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersecuritygroup.html#cfn-redshift-clustersecuritygroup-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnClusterSecurityGroupProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnClusterSubnetGroup(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-redshift.CfnClusterSubnetGroup"):
    """A CloudFormation ``AWS::Redshift::ClusterSubnetGroup``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersubnetgroup.html
    cloudformationResource:
    :cloudformationResource:: AWS::Redshift::ClusterSubnetGroup
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, description: str, subnet_ids: typing.List[str], tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None) -> None:
        """Create a new ``AWS::Redshift::ClusterSubnetGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: ``AWS::Redshift::ClusterSubnetGroup.Description``.
        :param subnet_ids: ``AWS::Redshift::ClusterSubnetGroup.SubnetIds``.
        :param tags: ``AWS::Redshift::ClusterSubnetGroup.Tags``.
        """
        props = CfnClusterSubnetGroupProps(description=description, subnet_ids=subnet_ids, tags=tags)

        jsii.create(CfnClusterSubnetGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnClusterSubnetGroup":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
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
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::Redshift::ClusterSubnetGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersubnetgroup.html#cfn-redshift-clustersubnetgroup-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> str:
        """``AWS::Redshift::ClusterSubnetGroup.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersubnetgroup.html#cfn-redshift-clustersubnetgroup-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: str) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="subnetIds")
    def subnet_ids(self) -> typing.List[str]:
        """``AWS::Redshift::ClusterSubnetGroup.SubnetIds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersubnetgroup.html#cfn-redshift-clustersubnetgroup-subnetids
        """
        return jsii.get(self, "subnetIds")

    @subnet_ids.setter
    def subnet_ids(self, value: typing.List[str]) -> None:
        jsii.set(self, "subnetIds", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-redshift.CfnClusterSubnetGroupProps", jsii_struct_bases=[], name_mapping={'description': 'description', 'subnet_ids': 'subnetIds', 'tags': 'tags'})
class CfnClusterSubnetGroupProps():
    def __init__(self, *, description: str, subnet_ids: typing.List[str], tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None) -> None:
        """Properties for defining a ``AWS::Redshift::ClusterSubnetGroup``.

        :param description: ``AWS::Redshift::ClusterSubnetGroup.Description``.
        :param subnet_ids: ``AWS::Redshift::ClusterSubnetGroup.SubnetIds``.
        :param tags: ``AWS::Redshift::ClusterSubnetGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersubnetgroup.html
        """
        self._values = {
            'description': description,
            'subnet_ids': subnet_ids,
        }
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def description(self) -> str:
        """``AWS::Redshift::ClusterSubnetGroup.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersubnetgroup.html#cfn-redshift-clustersubnetgroup-description
        """
        return self._values.get('description')

    @builtins.property
    def subnet_ids(self) -> typing.List[str]:
        """``AWS::Redshift::ClusterSubnetGroup.SubnetIds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersubnetgroup.html#cfn-redshift-clustersubnetgroup-subnetids
        """
        return self._values.get('subnet_ids')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::Redshift::ClusterSubnetGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-redshift-clustersubnetgroup.html#cfn-redshift-clustersubnetgroup-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnClusterSubnetGroupProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-redshift.ClusterAttributes", jsii_struct_bases=[], name_mapping={'cluster_endpoint_address': 'clusterEndpointAddress', 'cluster_endpoint_port': 'clusterEndpointPort', 'cluster_name': 'clusterName', 'security_groups': 'securityGroups'})
class ClusterAttributes():
    def __init__(self, *, cluster_endpoint_address: str, cluster_endpoint_port: jsii.Number, cluster_name: str, security_groups: typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]]=None) -> None:
        """Properties that describe an existing cluster instance.

        :param cluster_endpoint_address: Cluster endpoint address.
        :param cluster_endpoint_port: Cluster endpoint port.
        :param cluster_name: Identifier for the cluster.
        :param security_groups: The security groups of the redshift cluster. Default: no security groups will be attached to the import

        stability
        :stability: experimental
        """
        self._values = {
            'cluster_endpoint_address': cluster_endpoint_address,
            'cluster_endpoint_port': cluster_endpoint_port,
            'cluster_name': cluster_name,
        }
        if security_groups is not None: self._values["security_groups"] = security_groups

    @builtins.property
    def cluster_endpoint_address(self) -> str:
        """Cluster endpoint address.

        stability
        :stability: experimental
        """
        return self._values.get('cluster_endpoint_address')

    @builtins.property
    def cluster_endpoint_port(self) -> jsii.Number:
        """Cluster endpoint port.

        stability
        :stability: experimental
        """
        return self._values.get('cluster_endpoint_port')

    @builtins.property
    def cluster_name(self) -> str:
        """Identifier for the cluster.

        stability
        :stability: experimental
        """
        return self._values.get('cluster_name')

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]]:
        """The security groups of the redshift cluster.

        default
        :default: no security groups will be attached to the import

        stability
        :stability: experimental
        """
        return self._values.get('security_groups')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ClusterAttributes(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-redshift.ClusterParameterGroupProps", jsii_struct_bases=[], name_mapping={'parameters': 'parameters', 'description': 'description'})
class ClusterParameterGroupProps():
    def __init__(self, *, parameters: typing.Mapping[str, str], description: typing.Optional[str]=None) -> None:
        """Properties for a parameter group.

        :param parameters: The parameters in this parameter group.
        :param description: Description for this parameter group. Default: a CDK generated description

        stability
        :stability: experimental
        """
        self._values = {
            'parameters': parameters,
        }
        if description is not None: self._values["description"] = description

    @builtins.property
    def parameters(self) -> typing.Mapping[str, str]:
        """The parameters in this parameter group.

        stability
        :stability: experimental
        """
        return self._values.get('parameters')

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


@jsii.data_type(jsii_type="@aws-cdk/aws-redshift.ClusterProps", jsii_struct_bases=[], name_mapping={'master_user': 'masterUser', 'vpc': 'vpc', 'cluster_name': 'clusterName', 'cluster_type': 'clusterType', 'default_database_name': 'defaultDatabaseName', 'encrypted': 'encrypted', 'encryption_key': 'encryptionKey', 'logging_bucket': 'loggingBucket', 'logging_key_prefix': 'loggingKeyPrefix', 'node_type': 'nodeType', 'number_of_nodes': 'numberOfNodes', 'parameter_group': 'parameterGroup', 'port': 'port', 'preferred_maintenance_window': 'preferredMaintenanceWindow', 'removal_policy': 'removalPolicy', 'roles': 'roles', 'security_groups': 'securityGroups', 'vpc_subnets': 'vpcSubnets'})
class ClusterProps():
    def __init__(self, *, master_user: "Login", vpc: aws_cdk.aws_ec2.IVpc, cluster_name: typing.Optional[str]=None, cluster_type: typing.Optional["ClusterType"]=None, default_database_name: typing.Optional[str]=None, encrypted: typing.Optional[bool]=None, encryption_key: typing.Optional[aws_cdk.aws_kms.IKey]=None, logging_bucket: typing.Optional[aws_cdk.aws_s3.IBucket]=None, logging_key_prefix: typing.Optional[str]=None, node_type: typing.Optional["NodeType"]=None, number_of_nodes: typing.Optional[jsii.Number]=None, parameter_group: typing.Optional["IClusterParameterGroup"]=None, port: typing.Optional[jsii.Number]=None, preferred_maintenance_window: typing.Optional[str]=None, removal_policy: typing.Optional[aws_cdk.core.RemovalPolicy]=None, roles: typing.Optional[typing.List[aws_cdk.aws_iam.IRole]]=None, security_groups: typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]]=None, vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None) -> None:
        """Properties for a new database cluster.

        :param master_user: Username and password for the administrative user.
        :param vpc: The VPC to place the cluster in.
        :param cluster_name: An optional identifier for the cluster. Default: - A name is automatically generated.
        :param cluster_type: Settings for the individual instances that are launched. Default: {@link ClusterType.MULTI_NODE}
        :param default_database_name: Name of a database which is automatically created inside the cluster. Default: - default_db
        :param encrypted: Whether to enable encryption of data at rest in the cluster. Default: true
        :param encryption_key: The KMS key to use for encryption of data at rest. Default: - AWS-managed key, if encryption at rest is enabled
        :param logging_bucket: Bucket to send logs to. Logging information includes queries and connection attempts, for the specified Amazon Redshift cluster. Default: - No Logs
        :param logging_key_prefix: Prefix used for logging. Default: - no prefix
        :param node_type: The node type to be provisioned for the cluster. Default: {@link NodeType.DC2_LARGE}
        :param number_of_nodes: Number of compute nodes in the cluster. Value must be at least 1 and no more than 100. Default: 1
        :param parameter_group: Additional parameters to pass to the database engine https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-parameter-groups.html. Default: - No parameter group.
        :param port: What port to listen on. Default: - The default for the engine is used.
        :param preferred_maintenance_window: A preferred maintenance window day/time range. Should be specified as a range ddd:hh24:mi-ddd:hh24:mi (24H Clock UTC). Example: 'Sun:23:45-Mon:00:15' Default: - 30-minute window selected at random from an 8-hour block of time for each AWS Region, occurring on a random day of the week.
        :param removal_policy: The removal policy to apply when the cluster and its instances are removed from the stack or replaced during an update. Default: RemovalPolicy.RETAIN
        :param roles: A list of AWS Identity and Access Management (IAM) role that can be used by the cluster to access other AWS services. Specify a maximum of 10 roles. Default: - No role is attached to the cluster.
        :param security_groups: Security group. Default: a new security group is created.
        :param vpc_subnets: Where to place the instances within the VPC. Default: private subnets

        stability
        :stability: experimental
        """
        if isinstance(master_user, dict): master_user = Login(**master_user)
        if isinstance(vpc_subnets, dict): vpc_subnets = aws_cdk.aws_ec2.SubnetSelection(**vpc_subnets)
        self._values = {
            'master_user': master_user,
            'vpc': vpc,
        }
        if cluster_name is not None: self._values["cluster_name"] = cluster_name
        if cluster_type is not None: self._values["cluster_type"] = cluster_type
        if default_database_name is not None: self._values["default_database_name"] = default_database_name
        if encrypted is not None: self._values["encrypted"] = encrypted
        if encryption_key is not None: self._values["encryption_key"] = encryption_key
        if logging_bucket is not None: self._values["logging_bucket"] = logging_bucket
        if logging_key_prefix is not None: self._values["logging_key_prefix"] = logging_key_prefix
        if node_type is not None: self._values["node_type"] = node_type
        if number_of_nodes is not None: self._values["number_of_nodes"] = number_of_nodes
        if parameter_group is not None: self._values["parameter_group"] = parameter_group
        if port is not None: self._values["port"] = port
        if preferred_maintenance_window is not None: self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if removal_policy is not None: self._values["removal_policy"] = removal_policy
        if roles is not None: self._values["roles"] = roles
        if security_groups is not None: self._values["security_groups"] = security_groups
        if vpc_subnets is not None: self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def master_user(self) -> "Login":
        """Username and password for the administrative user.

        stability
        :stability: experimental
        """
        return self._values.get('master_user')

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """The VPC to place the cluster in.

        stability
        :stability: experimental
        """
        return self._values.get('vpc')

    @builtins.property
    def cluster_name(self) -> typing.Optional[str]:
        """An optional identifier for the cluster.

        default
        :default: - A name is automatically generated.

        stability
        :stability: experimental
        """
        return self._values.get('cluster_name')

    @builtins.property
    def cluster_type(self) -> typing.Optional["ClusterType"]:
        """Settings for the individual instances that are launched.

        default
        :default: {@link ClusterType.MULTI_NODE}

        stability
        :stability: experimental
        """
        return self._values.get('cluster_type')

    @builtins.property
    def default_database_name(self) -> typing.Optional[str]:
        """Name of a database which is automatically created inside the cluster.

        default
        :default: - default_db

        stability
        :stability: experimental
        """
        return self._values.get('default_database_name')

    @builtins.property
    def encrypted(self) -> typing.Optional[bool]:
        """Whether to enable encryption of data at rest in the cluster.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('encrypted')

    @builtins.property
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """The KMS key to use for encryption of data at rest.

        default
        :default: - AWS-managed key, if encryption at rest is enabled

        stability
        :stability: experimental
        """
        return self._values.get('encryption_key')

    @builtins.property
    def logging_bucket(self) -> typing.Optional[aws_cdk.aws_s3.IBucket]:
        """Bucket to send logs to.

        Logging information includes queries and connection attempts, for the specified Amazon Redshift cluster.

        default
        :default: - No Logs

        stability
        :stability: experimental
        """
        return self._values.get('logging_bucket')

    @builtins.property
    def logging_key_prefix(self) -> typing.Optional[str]:
        """Prefix used for logging.

        default
        :default: - no prefix

        stability
        :stability: experimental
        """
        return self._values.get('logging_key_prefix')

    @builtins.property
    def node_type(self) -> typing.Optional["NodeType"]:
        """The node type to be provisioned for the cluster.

        default
        :default: {@link NodeType.DC2_LARGE}

        stability
        :stability: experimental
        """
        return self._values.get('node_type')

    @builtins.property
    def number_of_nodes(self) -> typing.Optional[jsii.Number]:
        """Number of compute nodes in the cluster.

        Value must be at least 1 and no more than 100.

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('number_of_nodes')

    @builtins.property
    def parameter_group(self) -> typing.Optional["IClusterParameterGroup"]:
        """Additional parameters to pass to the database engine https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-parameter-groups.html.

        default
        :default: - No parameter group.

        stability
        :stability: experimental
        """
        return self._values.get('parameter_group')

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        """What port to listen on.

        default
        :default: - The default for the engine is used.

        stability
        :stability: experimental
        """
        return self._values.get('port')

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[str]:
        """A preferred maintenance window day/time range. Should be specified as a range ddd:hh24:mi-ddd:hh24:mi (24H Clock UTC).

        Example: 'Sun:23:45-Mon:00:15'

        default
        :default:

        - 30-minute window selected at random from an 8-hour block of time for
          each AWS Region, occurring on a random day of the week.

        see
        :see: https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_UpgradeDBInstance.Maintenance.html#Concepts.DBMaintenance
        stability
        :stability: experimental
        """
        return self._values.get('preferred_maintenance_window')

    @builtins.property
    def removal_policy(self) -> typing.Optional[aws_cdk.core.RemovalPolicy]:
        """The removal policy to apply when the cluster and its instances are removed from the stack or replaced during an update.

        default
        :default: RemovalPolicy.RETAIN

        stability
        :stability: experimental
        """
        return self._values.get('removal_policy')

    @builtins.property
    def roles(self) -> typing.Optional[typing.List[aws_cdk.aws_iam.IRole]]:
        """A list of AWS Identity and Access Management (IAM) role that can be used by the cluster to access other AWS services.

        Specify a maximum of 10 roles.

        default
        :default: - No role is attached to the cluster.

        stability
        :stability: experimental
        """
        return self._values.get('roles')

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]]:
        """Security group.

        default
        :default: a new security group is created.

        stability
        :stability: experimental
        """
        return self._values.get('security_groups')

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
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
        return 'ClusterProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-redshift.ClusterType")
class ClusterType(enum.Enum):
    """What cluster type to use.

    Used by {@link ClusterProps.clusterType}

    stability
    :stability: experimental
    """
    SINGLE_NODE = "SINGLE_NODE"
    """single-node cluster, the {@link ClusterProps.numberOfNodes} parameter is not required.

    stability
    :stability: experimental
    """
    MULTI_NODE = "MULTI_NODE"
    """multi-node cluster, set the amount of nodes using {@link ClusterProps.numberOfNodes} parameter.

    stability
    :stability: experimental
    """

class DatabaseSecret(aws_cdk.aws_secretsmanager.Secret, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-redshift.DatabaseSecret"):
    """A database secret.

    stability
    :stability: experimental
    resource:
    :resource:: AWS::SecretsManager::Secret
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, username: str, encryption_key: typing.Optional[aws_cdk.aws_kms.IKey]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param username: The username.
        :param encryption_key: The KMS key to use to encrypt the secret. Default: default master key

        stability
        :stability: experimental
        """
        props = DatabaseSecretProps(username=username, encryption_key=encryption_key)

        jsii.create(DatabaseSecret, self, [scope, id, props])


@jsii.data_type(jsii_type="@aws-cdk/aws-redshift.DatabaseSecretProps", jsii_struct_bases=[], name_mapping={'username': 'username', 'encryption_key': 'encryptionKey'})
class DatabaseSecretProps():
    def __init__(self, *, username: str, encryption_key: typing.Optional[aws_cdk.aws_kms.IKey]=None) -> None:
        """Construction properties for a DatabaseSecret.

        :param username: The username.
        :param encryption_key: The KMS key to use to encrypt the secret. Default: default master key

        stability
        :stability: experimental
        """
        self._values = {
            'username': username,
        }
        if encryption_key is not None: self._values["encryption_key"] = encryption_key

    @builtins.property
    def username(self) -> str:
        """The username.

        stability
        :stability: experimental
        """
        return self._values.get('username')

    @builtins.property
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """The KMS key to use to encrypt the secret.

        default
        :default: default master key

        stability
        :stability: experimental
        """
        return self._values.get('encryption_key')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DatabaseSecretProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class Endpoint(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-redshift.Endpoint"):
    """Connection endpoint of a redshift cluster.

    Consists of a combination of hostname and port.

    stability
    :stability: experimental
    """
    def __init__(self, address: str, port: jsii.Number) -> None:
        """
        :param address: -
        :param port: -

        stability
        :stability: experimental
        """
        jsii.create(Endpoint, self, [address, port])

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
        """The port of the endpoint.

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


@jsii.interface(jsii_type="@aws-cdk/aws-redshift.ICluster")
class ICluster(aws_cdk.core.IResource, aws_cdk.aws_ec2.IConnectable, aws_cdk.aws_secretsmanager.ISecretAttachmentTarget, jsii.compat.Protocol):
    """Create a Redshift Cluster with a given number of nodes.

    Implemented by {@link Cluster} via {@link ClusterBase}.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IClusterProxy

    @builtins.property
    @jsii.member(jsii_name="clusterEndpoint")
    def cluster_endpoint(self) -> "Endpoint":
        """The endpoint to use for read/write operations.

        stability
        :stability: experimental
        attribute:
        :attribute:: EndpointAddress,EndpointPort
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> str:
        """Name of the cluster.

        stability
        :stability: experimental
        attribute:
        :attribute:: ClusterName
        """
        ...


class _IClusterProxy(jsii.proxy_for(aws_cdk.core.IResource), jsii.proxy_for(aws_cdk.aws_ec2.IConnectable), jsii.proxy_for(aws_cdk.aws_secretsmanager.ISecretAttachmentTarget)):
    """Create a Redshift Cluster with a given number of nodes.

    Implemented by {@link Cluster} via {@link ClusterBase}.

    stability
    :stability: experimental
    """
    __jsii_type__ = "@aws-cdk/aws-redshift.ICluster"
    @builtins.property
    @jsii.member(jsii_name="clusterEndpoint")
    def cluster_endpoint(self) -> "Endpoint":
        """The endpoint to use for read/write operations.

        stability
        :stability: experimental
        attribute:
        :attribute:: EndpointAddress,EndpointPort
        """
        return jsii.get(self, "clusterEndpoint")

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> str:
        """Name of the cluster.

        stability
        :stability: experimental
        attribute:
        :attribute:: ClusterName
        """
        return jsii.get(self, "clusterName")


@jsii.interface(jsii_type="@aws-cdk/aws-redshift.IClusterParameterGroup")
class IClusterParameterGroup(aws_cdk.core.IResource, jsii.compat.Protocol):
    """A parameter group.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IClusterParameterGroupProxy

    @builtins.property
    @jsii.member(jsii_name="clusterParameterGroupName")
    def cluster_parameter_group_name(self) -> str:
        """The name of this parameter group.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...


class _IClusterParameterGroupProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    """A parameter group.

    stability
    :stability: experimental
    """
    __jsii_type__ = "@aws-cdk/aws-redshift.IClusterParameterGroup"
    @builtins.property
    @jsii.member(jsii_name="clusterParameterGroupName")
    def cluster_parameter_group_name(self) -> str:
        """The name of this parameter group.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "clusterParameterGroupName")


@jsii.data_type(jsii_type="@aws-cdk/aws-redshift.Login", jsii_struct_bases=[], name_mapping={'master_username': 'masterUsername', 'encryption_key': 'encryptionKey', 'master_password': 'masterPassword'})
class Login():
    def __init__(self, *, master_username: str, encryption_key: typing.Optional[aws_cdk.aws_kms.IKey]=None, master_password: typing.Optional[aws_cdk.core.SecretValue]=None) -> None:
        """Username and password combination.

        :param master_username: Username.
        :param encryption_key: KMS encryption key to encrypt the generated secret. Default: default master key
        :param master_password: Password. Do not put passwords in your CDK code directly. Default: a Secrets Manager generated password

        stability
        :stability: experimental
        """
        self._values = {
            'master_username': master_username,
        }
        if encryption_key is not None: self._values["encryption_key"] = encryption_key
        if master_password is not None: self._values["master_password"] = master_password

    @builtins.property
    def master_username(self) -> str:
        """Username.

        stability
        :stability: experimental
        """
        return self._values.get('master_username')

    @builtins.property
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """KMS encryption key to encrypt the generated secret.

        default
        :default: default master key

        stability
        :stability: experimental
        """
        return self._values.get('encryption_key')

    @builtins.property
    def master_password(self) -> typing.Optional[aws_cdk.core.SecretValue]:
        """Password.

        Do not put passwords in your CDK code directly.

        default
        :default: a Secrets Manager generated password

        stability
        :stability: experimental
        """
        return self._values.get('master_password')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'Login(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-redshift.NodeType")
class NodeType(enum.Enum):
    """Possible Node Types to use in the cluster used for defining {@link ClusterProps.nodeType}.

    stability
    :stability: experimental
    """
    DS2_XLARGE = "DS2_XLARGE"
    """ds2.xlarge.

    stability
    :stability: experimental
    """
    DS2_8XLARGE = "DS2_8XLARGE"
    """ds2.8xlarge.

    stability
    :stability: experimental
    """
    DC1_LARGE = "DC1_LARGE"
    """dc1.large.

    stability
    :stability: experimental
    """
    DC1_8XLARGE = "DC1_8XLARGE"
    """dc1.8xlarge.

    stability
    :stability: experimental
    """
    DC2_LARGE = "DC2_LARGE"
    """dc2.large.

    stability
    :stability: experimental
    """
    DC2_8XLARGE = "DC2_8XLARGE"
    """dc2.8xlarge.

    stability
    :stability: experimental
    """
    RA3_16XLARGE = "RA3_16XLARGE"
    """ra3.16xlarge.

    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-redshift.RotationMultiUserOptions", jsii_struct_bases=[], name_mapping={'secret': 'secret', 'automatically_after': 'automaticallyAfter'})
class RotationMultiUserOptions():
    def __init__(self, *, secret: aws_cdk.aws_secretsmanager.ISecret, automatically_after: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """Options to add the multi user rotation.

        :param secret: The secret to rotate. It must be a JSON string with the following format:: { "engine": <required: database engine>, "host": <required: instance host name>, "username": <required: username>, "password": <required: password>, "dbname": <optional: database name>, "port": <optional: if not specified, default port will be used>, "masterarn": <required: the arn of the master secret which will be used to create users/change passwords> }
        :param automatically_after: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. Default: Duration.days(30)

        stability
        :stability: experimental
        """
        self._values = {
            'secret': secret,
        }
        if automatically_after is not None: self._values["automatically_after"] = automatically_after

    @builtins.property
    def secret(self) -> aws_cdk.aws_secretsmanager.ISecret:
        """The secret to rotate.

        It must be a JSON string with the following format::

           {
              "engine": <required: database engine>,
              "host": <required: instance host name>,
              "username": <required: username>,
              "password": <required: password>,
              "dbname": <optional: database name>,
              "port": <optional: if not specified, default port will be used>,
              "masterarn": <required: the arn of the master secret which will be used to create users/change passwords>
           }

        stability
        :stability: experimental
        """
        return self._values.get('secret')

    @builtins.property
    def automatically_after(self) -> typing.Optional[aws_cdk.core.Duration]:
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


@jsii.implements(ICluster)
class Cluster(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-redshift.Cluster"):
    """Create a Redshift cluster a given number of nodes.

    stability
    :stability: experimental
    resource:
    :resource:: AWS::Redshift::Cluster
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, master_user: "Login", vpc: aws_cdk.aws_ec2.IVpc, cluster_name: typing.Optional[str]=None, cluster_type: typing.Optional["ClusterType"]=None, default_database_name: typing.Optional[str]=None, encrypted: typing.Optional[bool]=None, encryption_key: typing.Optional[aws_cdk.aws_kms.IKey]=None, logging_bucket: typing.Optional[aws_cdk.aws_s3.IBucket]=None, logging_key_prefix: typing.Optional[str]=None, node_type: typing.Optional["NodeType"]=None, number_of_nodes: typing.Optional[jsii.Number]=None, parameter_group: typing.Optional["IClusterParameterGroup"]=None, port: typing.Optional[jsii.Number]=None, preferred_maintenance_window: typing.Optional[str]=None, removal_policy: typing.Optional[aws_cdk.core.RemovalPolicy]=None, roles: typing.Optional[typing.List[aws_cdk.aws_iam.IRole]]=None, security_groups: typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]]=None, vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param master_user: Username and password for the administrative user.
        :param vpc: The VPC to place the cluster in.
        :param cluster_name: An optional identifier for the cluster. Default: - A name is automatically generated.
        :param cluster_type: Settings for the individual instances that are launched. Default: {@link ClusterType.MULTI_NODE}
        :param default_database_name: Name of a database which is automatically created inside the cluster. Default: - default_db
        :param encrypted: Whether to enable encryption of data at rest in the cluster. Default: true
        :param encryption_key: The KMS key to use for encryption of data at rest. Default: - AWS-managed key, if encryption at rest is enabled
        :param logging_bucket: Bucket to send logs to. Logging information includes queries and connection attempts, for the specified Amazon Redshift cluster. Default: - No Logs
        :param logging_key_prefix: Prefix used for logging. Default: - no prefix
        :param node_type: The node type to be provisioned for the cluster. Default: {@link NodeType.DC2_LARGE}
        :param number_of_nodes: Number of compute nodes in the cluster. Value must be at least 1 and no more than 100. Default: 1
        :param parameter_group: Additional parameters to pass to the database engine https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-parameter-groups.html. Default: - No parameter group.
        :param port: What port to listen on. Default: - The default for the engine is used.
        :param preferred_maintenance_window: A preferred maintenance window day/time range. Should be specified as a range ddd:hh24:mi-ddd:hh24:mi (24H Clock UTC). Example: 'Sun:23:45-Mon:00:15' Default: - 30-minute window selected at random from an 8-hour block of time for each AWS Region, occurring on a random day of the week.
        :param removal_policy: The removal policy to apply when the cluster and its instances are removed from the stack or replaced during an update. Default: RemovalPolicy.RETAIN
        :param roles: A list of AWS Identity and Access Management (IAM) role that can be used by the cluster to access other AWS services. Specify a maximum of 10 roles. Default: - No role is attached to the cluster.
        :param security_groups: Security group. Default: a new security group is created.
        :param vpc_subnets: Where to place the instances within the VPC. Default: private subnets

        stability
        :stability: experimental
        """
        props = ClusterProps(master_user=master_user, vpc=vpc, cluster_name=cluster_name, cluster_type=cluster_type, default_database_name=default_database_name, encrypted=encrypted, encryption_key=encryption_key, logging_bucket=logging_bucket, logging_key_prefix=logging_key_prefix, node_type=node_type, number_of_nodes=number_of_nodes, parameter_group=parameter_group, port=port, preferred_maintenance_window=preferred_maintenance_window, removal_policy=removal_policy, roles=roles, security_groups=security_groups, vpc_subnets=vpc_subnets)

        jsii.create(Cluster, self, [scope, id, props])

    @jsii.member(jsii_name="fromClusterAttributes")
    @builtins.classmethod
    def from_cluster_attributes(cls, scope: aws_cdk.core.Construct, id: str, *, cluster_endpoint_address: str, cluster_endpoint_port: jsii.Number, cluster_name: str, security_groups: typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]]=None) -> "ICluster":
        """Import an existing DatabaseCluster from properties.

        :param scope: -
        :param id: -
        :param cluster_endpoint_address: Cluster endpoint address.
        :param cluster_endpoint_port: Cluster endpoint port.
        :param cluster_name: Identifier for the cluster.
        :param security_groups: The security groups of the redshift cluster. Default: no security groups will be attached to the import

        stability
        :stability: experimental
        """
        attrs = ClusterAttributes(cluster_endpoint_address=cluster_endpoint_address, cluster_endpoint_port=cluster_endpoint_port, cluster_name=cluster_name, security_groups=security_groups)

        return jsii.sinvoke(cls, "fromClusterAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="addRotationMultiUser")
    def add_rotation_multi_user(self, id: str, *, secret: aws_cdk.aws_secretsmanager.ISecret, automatically_after: typing.Optional[aws_cdk.core.Duration]=None) -> aws_cdk.aws_secretsmanager.SecretRotation:
        """Adds the multi user rotation to this cluster.

        :param id: -
        :param secret: The secret to rotate. It must be a JSON string with the following format:: { "engine": <required: database engine>, "host": <required: instance host name>, "username": <required: username>, "password": <required: password>, "dbname": <optional: database name>, "port": <optional: if not specified, default port will be used>, "masterarn": <required: the arn of the master secret which will be used to create users/change passwords> }
        :param automatically_after: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. Default: Duration.days(30)

        stability
        :stability: experimental
        """
        options = RotationMultiUserOptions(secret=secret, automatically_after=automatically_after)

        return jsii.invoke(self, "addRotationMultiUser", [id, options])

    @jsii.member(jsii_name="addRotationSingleUser")
    def add_rotation_single_user(self, automatically_after: typing.Optional[aws_cdk.core.Duration]=None) -> aws_cdk.aws_secretsmanager.SecretRotation:
        """Adds the single user rotation of the master password to this cluster.

        :param automatically_after: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addRotationSingleUser", [automatically_after])

    @jsii.member(jsii_name="asSecretAttachmentTarget")
    def as_secret_attachment_target(self) -> aws_cdk.aws_secretsmanager.SecretAttachmentTargetProps:
        """Renders the secret attachment target specifications.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "asSecretAttachmentTarget", [])

    @builtins.property
    @jsii.member(jsii_name="clusterEndpoint")
    def cluster_endpoint(self) -> "Endpoint":
        """The endpoint to use for read/write operations.

        stability
        :stability: experimental
        """
        return jsii.get(self, "clusterEndpoint")

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> str:
        """Identifier of the cluster.

        stability
        :stability: experimental
        """
        return jsii.get(self, "clusterName")

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        """Access to the network connections.

        stability
        :stability: experimental
        """
        return jsii.get(self, "connections")

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> typing.Optional[aws_cdk.aws_secretsmanager.ISecret]:
        """The secret attached to this cluster.

        stability
        :stability: experimental
        """
        return jsii.get(self, "secret")


@jsii.implements(IClusterParameterGroup)
class ClusterParameterGroup(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-redshift.ClusterParameterGroup"):
    """A cluster parameter group.

    stability
    :stability: experimental
    resource:
    :resource:: AWS::Redshift::ClusterParameterGroup
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, parameters: typing.Mapping[str, str], description: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param parameters: The parameters in this parameter group.
        :param description: Description for this parameter group. Default: a CDK generated description

        stability
        :stability: experimental
        """
        props = ClusterParameterGroupProps(parameters=parameters, description=description)

        jsii.create(ClusterParameterGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromClusterParameterGroupName")
    @builtins.classmethod
    def from_cluster_parameter_group_name(cls, scope: aws_cdk.core.Construct, id: str, cluster_parameter_group_name: str) -> "IClusterParameterGroup":
        """Imports a parameter group.

        :param scope: -
        :param id: -
        :param cluster_parameter_group_name: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromClusterParameterGroupName", [scope, id, cluster_parameter_group_name])

    @builtins.property
    @jsii.member(jsii_name="clusterParameterGroupName")
    def cluster_parameter_group_name(self) -> str:
        """The name of the parameter group.

        stability
        :stability: experimental
        """
        return jsii.get(self, "clusterParameterGroupName")


__all__ = [
    "CfnCluster",
    "CfnClusterParameterGroup",
    "CfnClusterParameterGroupProps",
    "CfnClusterProps",
    "CfnClusterSecurityGroup",
    "CfnClusterSecurityGroupIngress",
    "CfnClusterSecurityGroupIngressProps",
    "CfnClusterSecurityGroupProps",
    "CfnClusterSubnetGroup",
    "CfnClusterSubnetGroupProps",
    "Cluster",
    "ClusterAttributes",
    "ClusterParameterGroup",
    "ClusterParameterGroupProps",
    "ClusterProps",
    "ClusterType",
    "DatabaseSecret",
    "DatabaseSecretProps",
    "Endpoint",
    "ICluster",
    "IClusterParameterGroup",
    "Login",
    "NodeType",
    "RotationMultiUserOptions",
]

publication.publish()
