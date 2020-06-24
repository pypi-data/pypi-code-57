import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *

from .. import (CfnResource as _CfnResource_7760e8e4, Construct as _Construct_f50a3f53, FromCloudFormationOptions as _FromCloudFormationOptions_5f49f6f1, TreeInspector as _TreeInspector_154f5999, TagManager as _TagManager_2508893f, IResolvable as _IResolvable_9ceae33e, IInspectable as _IInspectable_051e6ed8)


@jsii.implements(_IInspectable_051e6ed8)
class CfnCluster(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_dax.CfnCluster"):
    """A CloudFormation ``AWS::DAX::Cluster``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html
    cloudformationResource:
    :cloudformationResource:: AWS::DAX::Cluster
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, iam_role_arn: str, node_type: str, replication_factor: jsii.Number, availability_zones: typing.Optional[typing.List[str]]=None, cluster_name: typing.Optional[str]=None, description: typing.Optional[str]=None, notification_topic_arn: typing.Optional[str]=None, parameter_group_name: typing.Optional[str]=None, preferred_maintenance_window: typing.Optional[str]=None, security_group_ids: typing.Optional[typing.List[str]]=None, sse_specification: typing.Optional[typing.Union["SSESpecificationProperty", _IResolvable_9ceae33e]]=None, subnet_group_name: typing.Optional[str]=None, tags: typing.Any=None) -> None:
        """Create a new ``AWS::DAX::Cluster``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param iam_role_arn: ``AWS::DAX::Cluster.IAMRoleARN``.
        :param node_type: ``AWS::DAX::Cluster.NodeType``.
        :param replication_factor: ``AWS::DAX::Cluster.ReplicationFactor``.
        :param availability_zones: ``AWS::DAX::Cluster.AvailabilityZones``.
        :param cluster_name: ``AWS::DAX::Cluster.ClusterName``.
        :param description: ``AWS::DAX::Cluster.Description``.
        :param notification_topic_arn: ``AWS::DAX::Cluster.NotificationTopicARN``.
        :param parameter_group_name: ``AWS::DAX::Cluster.ParameterGroupName``.
        :param preferred_maintenance_window: ``AWS::DAX::Cluster.PreferredMaintenanceWindow``.
        :param security_group_ids: ``AWS::DAX::Cluster.SecurityGroupIds``.
        :param sse_specification: ``AWS::DAX::Cluster.SSESpecification``.
        :param subnet_group_name: ``AWS::DAX::Cluster.SubnetGroupName``.
        :param tags: ``AWS::DAX::Cluster.Tags``.
        """
        props = CfnClusterProps(iam_role_arn=iam_role_arn, node_type=node_type, replication_factor=replication_factor, availability_zones=availability_zones, cluster_name=cluster_name, description=description, notification_topic_arn=notification_topic_arn, parameter_group_name=parameter_group_name, preferred_maintenance_window=preferred_maintenance_window, security_group_ids=security_group_ids, sse_specification=sse_specification, subnet_group_name=subnet_group_name, tags=tags)

        jsii.create(CfnCluster, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnCluster":
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
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Arn
        """
        return jsii.get(self, "attrArn")

    @builtins.property
    @jsii.member(jsii_name="attrClusterDiscoveryEndpoint")
    def attr_cluster_discovery_endpoint(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: ClusterDiscoveryEndpoint
        """
        return jsii.get(self, "attrClusterDiscoveryEndpoint")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::DAX::Cluster.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="iamRoleArn")
    def iam_role_arn(self) -> str:
        """``AWS::DAX::Cluster.IAMRoleARN``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-iamrolearn
        """
        return jsii.get(self, "iamRoleArn")

    @iam_role_arn.setter
    def iam_role_arn(self, value: str) -> None:
        jsii.set(self, "iamRoleArn", value)

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> str:
        """``AWS::DAX::Cluster.NodeType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-nodetype
        """
        return jsii.get(self, "nodeType")

    @node_type.setter
    def node_type(self, value: str) -> None:
        jsii.set(self, "nodeType", value)

    @builtins.property
    @jsii.member(jsii_name="replicationFactor")
    def replication_factor(self) -> jsii.Number:
        """``AWS::DAX::Cluster.ReplicationFactor``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-replicationfactor
        """
        return jsii.get(self, "replicationFactor")

    @replication_factor.setter
    def replication_factor(self, value: jsii.Number) -> None:
        jsii.set(self, "replicationFactor", value)

    @builtins.property
    @jsii.member(jsii_name="availabilityZones")
    def availability_zones(self) -> typing.Optional[typing.List[str]]:
        """``AWS::DAX::Cluster.AvailabilityZones``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-availabilityzones
        """
        return jsii.get(self, "availabilityZones")

    @availability_zones.setter
    def availability_zones(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "availabilityZones", value)

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> typing.Optional[str]:
        """``AWS::DAX::Cluster.ClusterName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-clustername
        """
        return jsii.get(self, "clusterName")

    @cluster_name.setter
    def cluster_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "clusterName", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::DAX::Cluster.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="notificationTopicArn")
    def notification_topic_arn(self) -> typing.Optional[str]:
        """``AWS::DAX::Cluster.NotificationTopicARN``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-notificationtopicarn
        """
        return jsii.get(self, "notificationTopicArn")

    @notification_topic_arn.setter
    def notification_topic_arn(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "notificationTopicArn", value)

    @builtins.property
    @jsii.member(jsii_name="parameterGroupName")
    def parameter_group_name(self) -> typing.Optional[str]:
        """``AWS::DAX::Cluster.ParameterGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-parametergroupname
        """
        return jsii.get(self, "parameterGroupName")

    @parameter_group_name.setter
    def parameter_group_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "parameterGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="preferredMaintenanceWindow")
    def preferred_maintenance_window(self) -> typing.Optional[str]:
        """``AWS::DAX::Cluster.PreferredMaintenanceWindow``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-preferredmaintenancewindow
        """
        return jsii.get(self, "preferredMaintenanceWindow")

    @preferred_maintenance_window.setter
    def preferred_maintenance_window(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "preferredMaintenanceWindow", value)

    @builtins.property
    @jsii.member(jsii_name="securityGroupIds")
    def security_group_ids(self) -> typing.Optional[typing.List[str]]:
        """``AWS::DAX::Cluster.SecurityGroupIds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-securitygroupids
        """
        return jsii.get(self, "securityGroupIds")

    @security_group_ids.setter
    def security_group_ids(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "securityGroupIds", value)

    @builtins.property
    @jsii.member(jsii_name="sseSpecification")
    def sse_specification(self) -> typing.Optional[typing.Union["SSESpecificationProperty", _IResolvable_9ceae33e]]:
        """``AWS::DAX::Cluster.SSESpecification``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-ssespecification
        """
        return jsii.get(self, "sseSpecification")

    @sse_specification.setter
    def sse_specification(self, value: typing.Optional[typing.Union["SSESpecificationProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "sseSpecification", value)

    @builtins.property
    @jsii.member(jsii_name="subnetGroupName")
    def subnet_group_name(self) -> typing.Optional[str]:
        """``AWS::DAX::Cluster.SubnetGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-subnetgroupname
        """
        return jsii.get(self, "subnetGroupName")

    @subnet_group_name.setter
    def subnet_group_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "subnetGroupName", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_dax.CfnCluster.SSESpecificationProperty", jsii_struct_bases=[], name_mapping={'sse_enabled': 'sseEnabled'})
    class SSESpecificationProperty():
        def __init__(self, *, sse_enabled: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None) -> None:
            """
            :param sse_enabled: ``CfnCluster.SSESpecificationProperty.SSEEnabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dax-cluster-ssespecification.html
            """
            self._values = {
            }
            if sse_enabled is not None: self._values["sse_enabled"] = sse_enabled

        @builtins.property
        def sse_enabled(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnCluster.SSESpecificationProperty.SSEEnabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dax-cluster-ssespecification.html#cfn-dax-cluster-ssespecification-sseenabled
            """
            return self._values.get('sse_enabled')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'SSESpecificationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_dax.CfnClusterProps", jsii_struct_bases=[], name_mapping={'iam_role_arn': 'iamRoleArn', 'node_type': 'nodeType', 'replication_factor': 'replicationFactor', 'availability_zones': 'availabilityZones', 'cluster_name': 'clusterName', 'description': 'description', 'notification_topic_arn': 'notificationTopicArn', 'parameter_group_name': 'parameterGroupName', 'preferred_maintenance_window': 'preferredMaintenanceWindow', 'security_group_ids': 'securityGroupIds', 'sse_specification': 'sseSpecification', 'subnet_group_name': 'subnetGroupName', 'tags': 'tags'})
class CfnClusterProps():
    def __init__(self, *, iam_role_arn: str, node_type: str, replication_factor: jsii.Number, availability_zones: typing.Optional[typing.List[str]]=None, cluster_name: typing.Optional[str]=None, description: typing.Optional[str]=None, notification_topic_arn: typing.Optional[str]=None, parameter_group_name: typing.Optional[str]=None, preferred_maintenance_window: typing.Optional[str]=None, security_group_ids: typing.Optional[typing.List[str]]=None, sse_specification: typing.Optional[typing.Union["CfnCluster.SSESpecificationProperty", _IResolvable_9ceae33e]]=None, subnet_group_name: typing.Optional[str]=None, tags: typing.Any=None) -> None:
        """Properties for defining a ``AWS::DAX::Cluster``.

        :param iam_role_arn: ``AWS::DAX::Cluster.IAMRoleARN``.
        :param node_type: ``AWS::DAX::Cluster.NodeType``.
        :param replication_factor: ``AWS::DAX::Cluster.ReplicationFactor``.
        :param availability_zones: ``AWS::DAX::Cluster.AvailabilityZones``.
        :param cluster_name: ``AWS::DAX::Cluster.ClusterName``.
        :param description: ``AWS::DAX::Cluster.Description``.
        :param notification_topic_arn: ``AWS::DAX::Cluster.NotificationTopicARN``.
        :param parameter_group_name: ``AWS::DAX::Cluster.ParameterGroupName``.
        :param preferred_maintenance_window: ``AWS::DAX::Cluster.PreferredMaintenanceWindow``.
        :param security_group_ids: ``AWS::DAX::Cluster.SecurityGroupIds``.
        :param sse_specification: ``AWS::DAX::Cluster.SSESpecification``.
        :param subnet_group_name: ``AWS::DAX::Cluster.SubnetGroupName``.
        :param tags: ``AWS::DAX::Cluster.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html
        """
        self._values = {
            'iam_role_arn': iam_role_arn,
            'node_type': node_type,
            'replication_factor': replication_factor,
        }
        if availability_zones is not None: self._values["availability_zones"] = availability_zones
        if cluster_name is not None: self._values["cluster_name"] = cluster_name
        if description is not None: self._values["description"] = description
        if notification_topic_arn is not None: self._values["notification_topic_arn"] = notification_topic_arn
        if parameter_group_name is not None: self._values["parameter_group_name"] = parameter_group_name
        if preferred_maintenance_window is not None: self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if security_group_ids is not None: self._values["security_group_ids"] = security_group_ids
        if sse_specification is not None: self._values["sse_specification"] = sse_specification
        if subnet_group_name is not None: self._values["subnet_group_name"] = subnet_group_name
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def iam_role_arn(self) -> str:
        """``AWS::DAX::Cluster.IAMRoleARN``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-iamrolearn
        """
        return self._values.get('iam_role_arn')

    @builtins.property
    def node_type(self) -> str:
        """``AWS::DAX::Cluster.NodeType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-nodetype
        """
        return self._values.get('node_type')

    @builtins.property
    def replication_factor(self) -> jsii.Number:
        """``AWS::DAX::Cluster.ReplicationFactor``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-replicationfactor
        """
        return self._values.get('replication_factor')

    @builtins.property
    def availability_zones(self) -> typing.Optional[typing.List[str]]:
        """``AWS::DAX::Cluster.AvailabilityZones``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-availabilityzones
        """
        return self._values.get('availability_zones')

    @builtins.property
    def cluster_name(self) -> typing.Optional[str]:
        """``AWS::DAX::Cluster.ClusterName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-clustername
        """
        return self._values.get('cluster_name')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::DAX::Cluster.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-description
        """
        return self._values.get('description')

    @builtins.property
    def notification_topic_arn(self) -> typing.Optional[str]:
        """``AWS::DAX::Cluster.NotificationTopicARN``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-notificationtopicarn
        """
        return self._values.get('notification_topic_arn')

    @builtins.property
    def parameter_group_name(self) -> typing.Optional[str]:
        """``AWS::DAX::Cluster.ParameterGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-parametergroupname
        """
        return self._values.get('parameter_group_name')

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[str]:
        """``AWS::DAX::Cluster.PreferredMaintenanceWindow``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-preferredmaintenancewindow
        """
        return self._values.get('preferred_maintenance_window')

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[str]]:
        """``AWS::DAX::Cluster.SecurityGroupIds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-securitygroupids
        """
        return self._values.get('security_group_ids')

    @builtins.property
    def sse_specification(self) -> typing.Optional[typing.Union["CfnCluster.SSESpecificationProperty", _IResolvable_9ceae33e]]:
        """``AWS::DAX::Cluster.SSESpecification``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-ssespecification
        """
        return self._values.get('sse_specification')

    @builtins.property
    def subnet_group_name(self) -> typing.Optional[str]:
        """``AWS::DAX::Cluster.SubnetGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-subnetgroupname
        """
        return self._values.get('subnet_group_name')

    @builtins.property
    def tags(self) -> typing.Any:
        """``AWS::DAX::Cluster.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnClusterProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnParameterGroup(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_dax.CfnParameterGroup"):
    """A CloudFormation ``AWS::DAX::ParameterGroup``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-parametergroup.html
    cloudformationResource:
    :cloudformationResource:: AWS::DAX::ParameterGroup
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, description: typing.Optional[str]=None, parameter_group_name: typing.Optional[str]=None, parameter_name_values: typing.Any=None) -> None:
        """Create a new ``AWS::DAX::ParameterGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: ``AWS::DAX::ParameterGroup.Description``.
        :param parameter_group_name: ``AWS::DAX::ParameterGroup.ParameterGroupName``.
        :param parameter_name_values: ``AWS::DAX::ParameterGroup.ParameterNameValues``.
        """
        props = CfnParameterGroupProps(description=description, parameter_group_name=parameter_group_name, parameter_name_values=parameter_name_values)

        jsii.create(CfnParameterGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnParameterGroup":
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
    @jsii.member(jsii_name="parameterNameValues")
    def parameter_name_values(self) -> typing.Any:
        """``AWS::DAX::ParameterGroup.ParameterNameValues``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-parametergroup.html#cfn-dax-parametergroup-parameternamevalues
        """
        return jsii.get(self, "parameterNameValues")

    @parameter_name_values.setter
    def parameter_name_values(self, value: typing.Any) -> None:
        jsii.set(self, "parameterNameValues", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::DAX::ParameterGroup.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-parametergroup.html#cfn-dax-parametergroup-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="parameterGroupName")
    def parameter_group_name(self) -> typing.Optional[str]:
        """``AWS::DAX::ParameterGroup.ParameterGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-parametergroup.html#cfn-dax-parametergroup-parametergroupname
        """
        return jsii.get(self, "parameterGroupName")

    @parameter_group_name.setter
    def parameter_group_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "parameterGroupName", value)


@jsii.data_type(jsii_type="monocdk-experiment.aws_dax.CfnParameterGroupProps", jsii_struct_bases=[], name_mapping={'description': 'description', 'parameter_group_name': 'parameterGroupName', 'parameter_name_values': 'parameterNameValues'})
class CfnParameterGroupProps():
    def __init__(self, *, description: typing.Optional[str]=None, parameter_group_name: typing.Optional[str]=None, parameter_name_values: typing.Any=None) -> None:
        """Properties for defining a ``AWS::DAX::ParameterGroup``.

        :param description: ``AWS::DAX::ParameterGroup.Description``.
        :param parameter_group_name: ``AWS::DAX::ParameterGroup.ParameterGroupName``.
        :param parameter_name_values: ``AWS::DAX::ParameterGroup.ParameterNameValues``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-parametergroup.html
        """
        self._values = {
        }
        if description is not None: self._values["description"] = description
        if parameter_group_name is not None: self._values["parameter_group_name"] = parameter_group_name
        if parameter_name_values is not None: self._values["parameter_name_values"] = parameter_name_values

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::DAX::ParameterGroup.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-parametergroup.html#cfn-dax-parametergroup-description
        """
        return self._values.get('description')

    @builtins.property
    def parameter_group_name(self) -> typing.Optional[str]:
        """``AWS::DAX::ParameterGroup.ParameterGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-parametergroup.html#cfn-dax-parametergroup-parametergroupname
        """
        return self._values.get('parameter_group_name')

    @builtins.property
    def parameter_name_values(self) -> typing.Any:
        """``AWS::DAX::ParameterGroup.ParameterNameValues``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-parametergroup.html#cfn-dax-parametergroup-parameternamevalues
        """
        return self._values.get('parameter_name_values')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnParameterGroupProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnSubnetGroup(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_dax.CfnSubnetGroup"):
    """A CloudFormation ``AWS::DAX::SubnetGroup``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-subnetgroup.html
    cloudformationResource:
    :cloudformationResource:: AWS::DAX::SubnetGroup
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, subnet_ids: typing.List[str], description: typing.Optional[str]=None, subnet_group_name: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::DAX::SubnetGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param subnet_ids: ``AWS::DAX::SubnetGroup.SubnetIds``.
        :param description: ``AWS::DAX::SubnetGroup.Description``.
        :param subnet_group_name: ``AWS::DAX::SubnetGroup.SubnetGroupName``.
        """
        props = CfnSubnetGroupProps(subnet_ids=subnet_ids, description=description, subnet_group_name=subnet_group_name)

        jsii.create(CfnSubnetGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnSubnetGroup":
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
    @jsii.member(jsii_name="subnetIds")
    def subnet_ids(self) -> typing.List[str]:
        """``AWS::DAX::SubnetGroup.SubnetIds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-subnetgroup.html#cfn-dax-subnetgroup-subnetids
        """
        return jsii.get(self, "subnetIds")

    @subnet_ids.setter
    def subnet_ids(self, value: typing.List[str]) -> None:
        jsii.set(self, "subnetIds", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::DAX::SubnetGroup.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-subnetgroup.html#cfn-dax-subnetgroup-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="subnetGroupName")
    def subnet_group_name(self) -> typing.Optional[str]:
        """``AWS::DAX::SubnetGroup.SubnetGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-subnetgroup.html#cfn-dax-subnetgroup-subnetgroupname
        """
        return jsii.get(self, "subnetGroupName")

    @subnet_group_name.setter
    def subnet_group_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "subnetGroupName", value)


@jsii.data_type(jsii_type="monocdk-experiment.aws_dax.CfnSubnetGroupProps", jsii_struct_bases=[], name_mapping={'subnet_ids': 'subnetIds', 'description': 'description', 'subnet_group_name': 'subnetGroupName'})
class CfnSubnetGroupProps():
    def __init__(self, *, subnet_ids: typing.List[str], description: typing.Optional[str]=None, subnet_group_name: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::DAX::SubnetGroup``.

        :param subnet_ids: ``AWS::DAX::SubnetGroup.SubnetIds``.
        :param description: ``AWS::DAX::SubnetGroup.Description``.
        :param subnet_group_name: ``AWS::DAX::SubnetGroup.SubnetGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-subnetgroup.html
        """
        self._values = {
            'subnet_ids': subnet_ids,
        }
        if description is not None: self._values["description"] = description
        if subnet_group_name is not None: self._values["subnet_group_name"] = subnet_group_name

    @builtins.property
    def subnet_ids(self) -> typing.List[str]:
        """``AWS::DAX::SubnetGroup.SubnetIds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-subnetgroup.html#cfn-dax-subnetgroup-subnetids
        """
        return self._values.get('subnet_ids')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::DAX::SubnetGroup.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-subnetgroup.html#cfn-dax-subnetgroup-description
        """
        return self._values.get('description')

    @builtins.property
    def subnet_group_name(self) -> typing.Optional[str]:
        """``AWS::DAX::SubnetGroup.SubnetGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-subnetgroup.html#cfn-dax-subnetgroup-subnetgroupname
        """
        return self._values.get('subnet_group_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnSubnetGroupProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "CfnCluster",
    "CfnClusterProps",
    "CfnParameterGroup",
    "CfnParameterGroupProps",
    "CfnSubnetGroup",
    "CfnSubnetGroupProps",
]

publication.publish()
