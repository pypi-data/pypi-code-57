import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *

from .. import (CfnResource as _CfnResource_7760e8e4, Construct as _Construct_f50a3f53, FromCloudFormationOptions as _FromCloudFormationOptions_5f49f6f1, TreeInspector as _TreeInspector_154f5999, TagManager as _TagManager_2508893f, IResolvable as _IResolvable_9ceae33e, IInspectable as _IInspectable_051e6ed8, CfnTag as _CfnTag_b4661f1a)


@jsii.implements(_IInspectable_051e6ed8)
class CfnDomain(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_elasticsearch.CfnDomain"):
    """A CloudFormation ``AWS::Elasticsearch::Domain``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html
    cloudformationResource:
    :cloudformationResource:: AWS::Elasticsearch::Domain
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, access_policies: typing.Any=None, advanced_options: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.Mapping[str, str]]]=None, cognito_options: typing.Optional[typing.Union["CognitoOptionsProperty", _IResolvable_9ceae33e]]=None, domain_name: typing.Optional[str]=None, ebs_options: typing.Optional[typing.Union["EBSOptionsProperty", _IResolvable_9ceae33e]]=None, elasticsearch_cluster_config: typing.Optional[typing.Union["ElasticsearchClusterConfigProperty", _IResolvable_9ceae33e]]=None, elasticsearch_version: typing.Optional[str]=None, encryption_at_rest_options: typing.Optional[typing.Union["EncryptionAtRestOptionsProperty", _IResolvable_9ceae33e]]=None, log_publishing_options: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.Mapping[str, typing.Union["LogPublishingOptionProperty", _IResolvable_9ceae33e]]]]=None, node_to_node_encryption_options: typing.Optional[typing.Union["NodeToNodeEncryptionOptionsProperty", _IResolvable_9ceae33e]]=None, snapshot_options: typing.Optional[typing.Union["SnapshotOptionsProperty", _IResolvable_9ceae33e]]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None, vpc_options: typing.Optional[typing.Union["VPCOptionsProperty", _IResolvable_9ceae33e]]=None) -> None:
        """Create a new ``AWS::Elasticsearch::Domain``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param access_policies: ``AWS::Elasticsearch::Domain.AccessPolicies``.
        :param advanced_options: ``AWS::Elasticsearch::Domain.AdvancedOptions``.
        :param cognito_options: ``AWS::Elasticsearch::Domain.CognitoOptions``.
        :param domain_name: ``AWS::Elasticsearch::Domain.DomainName``.
        :param ebs_options: ``AWS::Elasticsearch::Domain.EBSOptions``.
        :param elasticsearch_cluster_config: ``AWS::Elasticsearch::Domain.ElasticsearchClusterConfig``.
        :param elasticsearch_version: ``AWS::Elasticsearch::Domain.ElasticsearchVersion``.
        :param encryption_at_rest_options: ``AWS::Elasticsearch::Domain.EncryptionAtRestOptions``.
        :param log_publishing_options: ``AWS::Elasticsearch::Domain.LogPublishingOptions``.
        :param node_to_node_encryption_options: ``AWS::Elasticsearch::Domain.NodeToNodeEncryptionOptions``.
        :param snapshot_options: ``AWS::Elasticsearch::Domain.SnapshotOptions``.
        :param tags: ``AWS::Elasticsearch::Domain.Tags``.
        :param vpc_options: ``AWS::Elasticsearch::Domain.VPCOptions``.
        """
        props = CfnDomainProps(access_policies=access_policies, advanced_options=advanced_options, cognito_options=cognito_options, domain_name=domain_name, ebs_options=ebs_options, elasticsearch_cluster_config=elasticsearch_cluster_config, elasticsearch_version=elasticsearch_version, encryption_at_rest_options=encryption_at_rest_options, log_publishing_options=log_publishing_options, node_to_node_encryption_options=node_to_node_encryption_options, snapshot_options=snapshot_options, tags=tags, vpc_options=vpc_options)

        jsii.create(CfnDomain, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnDomain":
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
    @jsii.member(jsii_name="attrDomainEndpoint")
    def attr_domain_endpoint(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: DomainEndpoint
        """
        return jsii.get(self, "attrDomainEndpoint")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::Elasticsearch::Domain.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="accessPolicies")
    def access_policies(self) -> typing.Any:
        """``AWS::Elasticsearch::Domain.AccessPolicies``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-accesspolicies
        """
        return jsii.get(self, "accessPolicies")

    @access_policies.setter
    def access_policies(self, value: typing.Any) -> None:
        jsii.set(self, "accessPolicies", value)

    @builtins.property
    @jsii.member(jsii_name="advancedOptions")
    def advanced_options(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.Mapping[str, str]]]:
        """``AWS::Elasticsearch::Domain.AdvancedOptions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-advancedoptions
        """
        return jsii.get(self, "advancedOptions")

    @advanced_options.setter
    def advanced_options(self, value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.Mapping[str, str]]]) -> None:
        jsii.set(self, "advancedOptions", value)

    @builtins.property
    @jsii.member(jsii_name="cognitoOptions")
    def cognito_options(self) -> typing.Optional[typing.Union["CognitoOptionsProperty", _IResolvable_9ceae33e]]:
        """``AWS::Elasticsearch::Domain.CognitoOptions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-cognitooptions
        """
        return jsii.get(self, "cognitoOptions")

    @cognito_options.setter
    def cognito_options(self, value: typing.Optional[typing.Union["CognitoOptionsProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "cognitoOptions", value)

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> typing.Optional[str]:
        """``AWS::Elasticsearch::Domain.DomainName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-domainname
        """
        return jsii.get(self, "domainName")

    @domain_name.setter
    def domain_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "domainName", value)

    @builtins.property
    @jsii.member(jsii_name="ebsOptions")
    def ebs_options(self) -> typing.Optional[typing.Union["EBSOptionsProperty", _IResolvable_9ceae33e]]:
        """``AWS::Elasticsearch::Domain.EBSOptions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-ebsoptions
        """
        return jsii.get(self, "ebsOptions")

    @ebs_options.setter
    def ebs_options(self, value: typing.Optional[typing.Union["EBSOptionsProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "ebsOptions", value)

    @builtins.property
    @jsii.member(jsii_name="elasticsearchClusterConfig")
    def elasticsearch_cluster_config(self) -> typing.Optional[typing.Union["ElasticsearchClusterConfigProperty", _IResolvable_9ceae33e]]:
        """``AWS::Elasticsearch::Domain.ElasticsearchClusterConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-elasticsearchclusterconfig
        """
        return jsii.get(self, "elasticsearchClusterConfig")

    @elasticsearch_cluster_config.setter
    def elasticsearch_cluster_config(self, value: typing.Optional[typing.Union["ElasticsearchClusterConfigProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "elasticsearchClusterConfig", value)

    @builtins.property
    @jsii.member(jsii_name="elasticsearchVersion")
    def elasticsearch_version(self) -> typing.Optional[str]:
        """``AWS::Elasticsearch::Domain.ElasticsearchVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-elasticsearchversion
        """
        return jsii.get(self, "elasticsearchVersion")

    @elasticsearch_version.setter
    def elasticsearch_version(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "elasticsearchVersion", value)

    @builtins.property
    @jsii.member(jsii_name="encryptionAtRestOptions")
    def encryption_at_rest_options(self) -> typing.Optional[typing.Union["EncryptionAtRestOptionsProperty", _IResolvable_9ceae33e]]:
        """``AWS::Elasticsearch::Domain.EncryptionAtRestOptions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-encryptionatrestoptions
        """
        return jsii.get(self, "encryptionAtRestOptions")

    @encryption_at_rest_options.setter
    def encryption_at_rest_options(self, value: typing.Optional[typing.Union["EncryptionAtRestOptionsProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "encryptionAtRestOptions", value)

    @builtins.property
    @jsii.member(jsii_name="logPublishingOptions")
    def log_publishing_options(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.Mapping[str, typing.Union["LogPublishingOptionProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::Elasticsearch::Domain.LogPublishingOptions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-logpublishingoptions
        """
        return jsii.get(self, "logPublishingOptions")

    @log_publishing_options.setter
    def log_publishing_options(self, value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.Mapping[str, typing.Union["LogPublishingOptionProperty", _IResolvable_9ceae33e]]]]) -> None:
        jsii.set(self, "logPublishingOptions", value)

    @builtins.property
    @jsii.member(jsii_name="nodeToNodeEncryptionOptions")
    def node_to_node_encryption_options(self) -> typing.Optional[typing.Union["NodeToNodeEncryptionOptionsProperty", _IResolvable_9ceae33e]]:
        """``AWS::Elasticsearch::Domain.NodeToNodeEncryptionOptions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-nodetonodeencryptionoptions
        """
        return jsii.get(self, "nodeToNodeEncryptionOptions")

    @node_to_node_encryption_options.setter
    def node_to_node_encryption_options(self, value: typing.Optional[typing.Union["NodeToNodeEncryptionOptionsProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "nodeToNodeEncryptionOptions", value)

    @builtins.property
    @jsii.member(jsii_name="snapshotOptions")
    def snapshot_options(self) -> typing.Optional[typing.Union["SnapshotOptionsProperty", _IResolvable_9ceae33e]]:
        """``AWS::Elasticsearch::Domain.SnapshotOptions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-snapshotoptions
        """
        return jsii.get(self, "snapshotOptions")

    @snapshot_options.setter
    def snapshot_options(self, value: typing.Optional[typing.Union["SnapshotOptionsProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "snapshotOptions", value)

    @builtins.property
    @jsii.member(jsii_name="vpcOptions")
    def vpc_options(self) -> typing.Optional[typing.Union["VPCOptionsProperty", _IResolvable_9ceae33e]]:
        """``AWS::Elasticsearch::Domain.VPCOptions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-vpcoptions
        """
        return jsii.get(self, "vpcOptions")

    @vpc_options.setter
    def vpc_options(self, value: typing.Optional[typing.Union["VPCOptionsProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "vpcOptions", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_elasticsearch.CfnDomain.CognitoOptionsProperty", jsii_struct_bases=[], name_mapping={'enabled': 'enabled', 'identity_pool_id': 'identityPoolId', 'role_arn': 'roleArn', 'user_pool_id': 'userPoolId'})
    class CognitoOptionsProperty():
        def __init__(self, *, enabled: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, identity_pool_id: typing.Optional[str]=None, role_arn: typing.Optional[str]=None, user_pool_id: typing.Optional[str]=None) -> None:
            """
            :param enabled: ``CfnDomain.CognitoOptionsProperty.Enabled``.
            :param identity_pool_id: ``CfnDomain.CognitoOptionsProperty.IdentityPoolId``.
            :param role_arn: ``CfnDomain.CognitoOptionsProperty.RoleArn``.
            :param user_pool_id: ``CfnDomain.CognitoOptionsProperty.UserPoolId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-cognitooptions.html
            """
            self._values = {
            }
            if enabled is not None: self._values["enabled"] = enabled
            if identity_pool_id is not None: self._values["identity_pool_id"] = identity_pool_id
            if role_arn is not None: self._values["role_arn"] = role_arn
            if user_pool_id is not None: self._values["user_pool_id"] = user_pool_id

        @builtins.property
        def enabled(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnDomain.CognitoOptionsProperty.Enabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-cognitooptions.html#cfn-elasticsearch-domain-cognitooptions-enabled
            """
            return self._values.get('enabled')

        @builtins.property
        def identity_pool_id(self) -> typing.Optional[str]:
            """``CfnDomain.CognitoOptionsProperty.IdentityPoolId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-cognitooptions.html#cfn-elasticsearch-domain-cognitooptions-identitypoolid
            """
            return self._values.get('identity_pool_id')

        @builtins.property
        def role_arn(self) -> typing.Optional[str]:
            """``CfnDomain.CognitoOptionsProperty.RoleArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-cognitooptions.html#cfn-elasticsearch-domain-cognitooptions-rolearn
            """
            return self._values.get('role_arn')

        @builtins.property
        def user_pool_id(self) -> typing.Optional[str]:
            """``CfnDomain.CognitoOptionsProperty.UserPoolId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-cognitooptions.html#cfn-elasticsearch-domain-cognitooptions-userpoolid
            """
            return self._values.get('user_pool_id')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'CognitoOptionsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_elasticsearch.CfnDomain.EBSOptionsProperty", jsii_struct_bases=[], name_mapping={'ebs_enabled': 'ebsEnabled', 'iops': 'iops', 'volume_size': 'volumeSize', 'volume_type': 'volumeType'})
    class EBSOptionsProperty():
        def __init__(self, *, ebs_enabled: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, iops: typing.Optional[jsii.Number]=None, volume_size: typing.Optional[jsii.Number]=None, volume_type: typing.Optional[str]=None) -> None:
            """
            :param ebs_enabled: ``CfnDomain.EBSOptionsProperty.EBSEnabled``.
            :param iops: ``CfnDomain.EBSOptionsProperty.Iops``.
            :param volume_size: ``CfnDomain.EBSOptionsProperty.VolumeSize``.
            :param volume_type: ``CfnDomain.EBSOptionsProperty.VolumeType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-ebsoptions.html
            """
            self._values = {
            }
            if ebs_enabled is not None: self._values["ebs_enabled"] = ebs_enabled
            if iops is not None: self._values["iops"] = iops
            if volume_size is not None: self._values["volume_size"] = volume_size
            if volume_type is not None: self._values["volume_type"] = volume_type

        @builtins.property
        def ebs_enabled(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnDomain.EBSOptionsProperty.EBSEnabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-ebsoptions.html#cfn-elasticsearch-domain-ebsoptions-ebsenabled
            """
            return self._values.get('ebs_enabled')

        @builtins.property
        def iops(self) -> typing.Optional[jsii.Number]:
            """``CfnDomain.EBSOptionsProperty.Iops``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-ebsoptions.html#cfn-elasticsearch-domain-ebsoptions-iops
            """
            return self._values.get('iops')

        @builtins.property
        def volume_size(self) -> typing.Optional[jsii.Number]:
            """``CfnDomain.EBSOptionsProperty.VolumeSize``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-ebsoptions.html#cfn-elasticsearch-domain-ebsoptions-volumesize
            """
            return self._values.get('volume_size')

        @builtins.property
        def volume_type(self) -> typing.Optional[str]:
            """``CfnDomain.EBSOptionsProperty.VolumeType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-ebsoptions.html#cfn-elasticsearch-domain-ebsoptions-volumetype
            """
            return self._values.get('volume_type')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'EBSOptionsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_elasticsearch.CfnDomain.ElasticsearchClusterConfigProperty", jsii_struct_bases=[], name_mapping={'dedicated_master_count': 'dedicatedMasterCount', 'dedicated_master_enabled': 'dedicatedMasterEnabled', 'dedicated_master_type': 'dedicatedMasterType', 'instance_count': 'instanceCount', 'instance_type': 'instanceType', 'zone_awareness_config': 'zoneAwarenessConfig', 'zone_awareness_enabled': 'zoneAwarenessEnabled'})
    class ElasticsearchClusterConfigProperty():
        def __init__(self, *, dedicated_master_count: typing.Optional[jsii.Number]=None, dedicated_master_enabled: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, dedicated_master_type: typing.Optional[str]=None, instance_count: typing.Optional[jsii.Number]=None, instance_type: typing.Optional[str]=None, zone_awareness_config: typing.Optional[typing.Union["CfnDomain.ZoneAwarenessConfigProperty", _IResolvable_9ceae33e]]=None, zone_awareness_enabled: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None) -> None:
            """
            :param dedicated_master_count: ``CfnDomain.ElasticsearchClusterConfigProperty.DedicatedMasterCount``.
            :param dedicated_master_enabled: ``CfnDomain.ElasticsearchClusterConfigProperty.DedicatedMasterEnabled``.
            :param dedicated_master_type: ``CfnDomain.ElasticsearchClusterConfigProperty.DedicatedMasterType``.
            :param instance_count: ``CfnDomain.ElasticsearchClusterConfigProperty.InstanceCount``.
            :param instance_type: ``CfnDomain.ElasticsearchClusterConfigProperty.InstanceType``.
            :param zone_awareness_config: ``CfnDomain.ElasticsearchClusterConfigProperty.ZoneAwarenessConfig``.
            :param zone_awareness_enabled: ``CfnDomain.ElasticsearchClusterConfigProperty.ZoneAwarenessEnabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-elasticsearchclusterconfig.html
            """
            self._values = {
            }
            if dedicated_master_count is not None: self._values["dedicated_master_count"] = dedicated_master_count
            if dedicated_master_enabled is not None: self._values["dedicated_master_enabled"] = dedicated_master_enabled
            if dedicated_master_type is not None: self._values["dedicated_master_type"] = dedicated_master_type
            if instance_count is not None: self._values["instance_count"] = instance_count
            if instance_type is not None: self._values["instance_type"] = instance_type
            if zone_awareness_config is not None: self._values["zone_awareness_config"] = zone_awareness_config
            if zone_awareness_enabled is not None: self._values["zone_awareness_enabled"] = zone_awareness_enabled

        @builtins.property
        def dedicated_master_count(self) -> typing.Optional[jsii.Number]:
            """``CfnDomain.ElasticsearchClusterConfigProperty.DedicatedMasterCount``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-elasticsearchclusterconfig.html#cfn-elasticsearch-domain-elasticseachclusterconfig-dedicatedmastercount
            """
            return self._values.get('dedicated_master_count')

        @builtins.property
        def dedicated_master_enabled(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnDomain.ElasticsearchClusterConfigProperty.DedicatedMasterEnabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-elasticsearchclusterconfig.html#cfn-elasticsearch-domain-elasticseachclusterconfig-dedicatedmasterenabled
            """
            return self._values.get('dedicated_master_enabled')

        @builtins.property
        def dedicated_master_type(self) -> typing.Optional[str]:
            """``CfnDomain.ElasticsearchClusterConfigProperty.DedicatedMasterType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-elasticsearchclusterconfig.html#cfn-elasticsearch-domain-elasticseachclusterconfig-dedicatedmastertype
            """
            return self._values.get('dedicated_master_type')

        @builtins.property
        def instance_count(self) -> typing.Optional[jsii.Number]:
            """``CfnDomain.ElasticsearchClusterConfigProperty.InstanceCount``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-elasticsearchclusterconfig.html#cfn-elasticsearch-domain-elasticseachclusterconfig-instancecount
            """
            return self._values.get('instance_count')

        @builtins.property
        def instance_type(self) -> typing.Optional[str]:
            """``CfnDomain.ElasticsearchClusterConfigProperty.InstanceType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-elasticsearchclusterconfig.html#cfn-elasticsearch-domain-elasticseachclusterconfig-instnacetype
            """
            return self._values.get('instance_type')

        @builtins.property
        def zone_awareness_config(self) -> typing.Optional[typing.Union["CfnDomain.ZoneAwarenessConfigProperty", _IResolvable_9ceae33e]]:
            """``CfnDomain.ElasticsearchClusterConfigProperty.ZoneAwarenessConfig``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-elasticsearchclusterconfig.html#cfn-elasticsearch-domain-elasticsearchclusterconfig-zoneawarenessconfig
            """
            return self._values.get('zone_awareness_config')

        @builtins.property
        def zone_awareness_enabled(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnDomain.ElasticsearchClusterConfigProperty.ZoneAwarenessEnabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-elasticsearchclusterconfig.html#cfn-elasticsearch-domain-elasticseachclusterconfig-zoneawarenessenabled
            """
            return self._values.get('zone_awareness_enabled')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ElasticsearchClusterConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_elasticsearch.CfnDomain.EncryptionAtRestOptionsProperty", jsii_struct_bases=[], name_mapping={'enabled': 'enabled', 'kms_key_id': 'kmsKeyId'})
    class EncryptionAtRestOptionsProperty():
        def __init__(self, *, enabled: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, kms_key_id: typing.Optional[str]=None) -> None:
            """
            :param enabled: ``CfnDomain.EncryptionAtRestOptionsProperty.Enabled``.
            :param kms_key_id: ``CfnDomain.EncryptionAtRestOptionsProperty.KmsKeyId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-encryptionatrestoptions.html
            """
            self._values = {
            }
            if enabled is not None: self._values["enabled"] = enabled
            if kms_key_id is not None: self._values["kms_key_id"] = kms_key_id

        @builtins.property
        def enabled(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnDomain.EncryptionAtRestOptionsProperty.Enabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-encryptionatrestoptions.html#cfn-elasticsearch-domain-encryptionatrestoptions-enabled
            """
            return self._values.get('enabled')

        @builtins.property
        def kms_key_id(self) -> typing.Optional[str]:
            """``CfnDomain.EncryptionAtRestOptionsProperty.KmsKeyId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-encryptionatrestoptions.html#cfn-elasticsearch-domain-encryptionatrestoptions-kmskeyid
            """
            return self._values.get('kms_key_id')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'EncryptionAtRestOptionsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_elasticsearch.CfnDomain.LogPublishingOptionProperty", jsii_struct_bases=[], name_mapping={'cloud_watch_logs_log_group_arn': 'cloudWatchLogsLogGroupArn', 'enabled': 'enabled'})
    class LogPublishingOptionProperty():
        def __init__(self, *, cloud_watch_logs_log_group_arn: typing.Optional[str]=None, enabled: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None) -> None:
            """
            :param cloud_watch_logs_log_group_arn: ``CfnDomain.LogPublishingOptionProperty.CloudWatchLogsLogGroupArn``.
            :param enabled: ``CfnDomain.LogPublishingOptionProperty.Enabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-logpublishingoption.html
            """
            self._values = {
            }
            if cloud_watch_logs_log_group_arn is not None: self._values["cloud_watch_logs_log_group_arn"] = cloud_watch_logs_log_group_arn
            if enabled is not None: self._values["enabled"] = enabled

        @builtins.property
        def cloud_watch_logs_log_group_arn(self) -> typing.Optional[str]:
            """``CfnDomain.LogPublishingOptionProperty.CloudWatchLogsLogGroupArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-logpublishingoption.html#cfn-elasticsearch-domain-logpublishingoption-cloudwatchlogsloggrouparn
            """
            return self._values.get('cloud_watch_logs_log_group_arn')

        @builtins.property
        def enabled(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnDomain.LogPublishingOptionProperty.Enabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-logpublishingoption.html#cfn-elasticsearch-domain-logpublishingoption-enabled
            """
            return self._values.get('enabled')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'LogPublishingOptionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_elasticsearch.CfnDomain.NodeToNodeEncryptionOptionsProperty", jsii_struct_bases=[], name_mapping={'enabled': 'enabled'})
    class NodeToNodeEncryptionOptionsProperty():
        def __init__(self, *, enabled: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None) -> None:
            """
            :param enabled: ``CfnDomain.NodeToNodeEncryptionOptionsProperty.Enabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-nodetonodeencryptionoptions.html
            """
            self._values = {
            }
            if enabled is not None: self._values["enabled"] = enabled

        @builtins.property
        def enabled(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnDomain.NodeToNodeEncryptionOptionsProperty.Enabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-nodetonodeencryptionoptions.html#cfn-elasticsearch-domain-nodetonodeencryptionoptions-enabled
            """
            return self._values.get('enabled')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'NodeToNodeEncryptionOptionsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_elasticsearch.CfnDomain.SnapshotOptionsProperty", jsii_struct_bases=[], name_mapping={'automated_snapshot_start_hour': 'automatedSnapshotStartHour'})
    class SnapshotOptionsProperty():
        def __init__(self, *, automated_snapshot_start_hour: typing.Optional[jsii.Number]=None) -> None:
            """
            :param automated_snapshot_start_hour: ``CfnDomain.SnapshotOptionsProperty.AutomatedSnapshotStartHour``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-snapshotoptions.html
            """
            self._values = {
            }
            if automated_snapshot_start_hour is not None: self._values["automated_snapshot_start_hour"] = automated_snapshot_start_hour

        @builtins.property
        def automated_snapshot_start_hour(self) -> typing.Optional[jsii.Number]:
            """``CfnDomain.SnapshotOptionsProperty.AutomatedSnapshotStartHour``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-snapshotoptions.html#cfn-elasticsearch-domain-snapshotoptions-automatedsnapshotstarthour
            """
            return self._values.get('automated_snapshot_start_hour')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'SnapshotOptionsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_elasticsearch.CfnDomain.VPCOptionsProperty", jsii_struct_bases=[], name_mapping={'security_group_ids': 'securityGroupIds', 'subnet_ids': 'subnetIds'})
    class VPCOptionsProperty():
        def __init__(self, *, security_group_ids: typing.Optional[typing.List[str]]=None, subnet_ids: typing.Optional[typing.List[str]]=None) -> None:
            """
            :param security_group_ids: ``CfnDomain.VPCOptionsProperty.SecurityGroupIds``.
            :param subnet_ids: ``CfnDomain.VPCOptionsProperty.SubnetIds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-vpcoptions.html
            """
            self._values = {
            }
            if security_group_ids is not None: self._values["security_group_ids"] = security_group_ids
            if subnet_ids is not None: self._values["subnet_ids"] = subnet_ids

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[str]]:
            """``CfnDomain.VPCOptionsProperty.SecurityGroupIds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-vpcoptions.html#cfn-elasticsearch-domain-vpcoptions-securitygroupids
            """
            return self._values.get('security_group_ids')

        @builtins.property
        def subnet_ids(self) -> typing.Optional[typing.List[str]]:
            """``CfnDomain.VPCOptionsProperty.SubnetIds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-vpcoptions.html#cfn-elasticsearch-domain-vpcoptions-subnetids
            """
            return self._values.get('subnet_ids')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'VPCOptionsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_elasticsearch.CfnDomain.ZoneAwarenessConfigProperty", jsii_struct_bases=[], name_mapping={'availability_zone_count': 'availabilityZoneCount'})
    class ZoneAwarenessConfigProperty():
        def __init__(self, *, availability_zone_count: typing.Optional[jsii.Number]=None) -> None:
            """
            :param availability_zone_count: ``CfnDomain.ZoneAwarenessConfigProperty.AvailabilityZoneCount``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-zoneawarenessconfig.html
            """
            self._values = {
            }
            if availability_zone_count is not None: self._values["availability_zone_count"] = availability_zone_count

        @builtins.property
        def availability_zone_count(self) -> typing.Optional[jsii.Number]:
            """``CfnDomain.ZoneAwarenessConfigProperty.AvailabilityZoneCount``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-zoneawarenessconfig.html#cfn-elasticsearch-domain-zoneawarenessconfig-availabilityzonecount
            """
            return self._values.get('availability_zone_count')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ZoneAwarenessConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_elasticsearch.CfnDomainProps", jsii_struct_bases=[], name_mapping={'access_policies': 'accessPolicies', 'advanced_options': 'advancedOptions', 'cognito_options': 'cognitoOptions', 'domain_name': 'domainName', 'ebs_options': 'ebsOptions', 'elasticsearch_cluster_config': 'elasticsearchClusterConfig', 'elasticsearch_version': 'elasticsearchVersion', 'encryption_at_rest_options': 'encryptionAtRestOptions', 'log_publishing_options': 'logPublishingOptions', 'node_to_node_encryption_options': 'nodeToNodeEncryptionOptions', 'snapshot_options': 'snapshotOptions', 'tags': 'tags', 'vpc_options': 'vpcOptions'})
class CfnDomainProps():
    def __init__(self, *, access_policies: typing.Any=None, advanced_options: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.Mapping[str, str]]]=None, cognito_options: typing.Optional[typing.Union["CfnDomain.CognitoOptionsProperty", _IResolvable_9ceae33e]]=None, domain_name: typing.Optional[str]=None, ebs_options: typing.Optional[typing.Union["CfnDomain.EBSOptionsProperty", _IResolvable_9ceae33e]]=None, elasticsearch_cluster_config: typing.Optional[typing.Union["CfnDomain.ElasticsearchClusterConfigProperty", _IResolvable_9ceae33e]]=None, elasticsearch_version: typing.Optional[str]=None, encryption_at_rest_options: typing.Optional[typing.Union["CfnDomain.EncryptionAtRestOptionsProperty", _IResolvable_9ceae33e]]=None, log_publishing_options: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.Mapping[str, typing.Union["CfnDomain.LogPublishingOptionProperty", _IResolvable_9ceae33e]]]]=None, node_to_node_encryption_options: typing.Optional[typing.Union["CfnDomain.NodeToNodeEncryptionOptionsProperty", _IResolvable_9ceae33e]]=None, snapshot_options: typing.Optional[typing.Union["CfnDomain.SnapshotOptionsProperty", _IResolvable_9ceae33e]]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None, vpc_options: typing.Optional[typing.Union["CfnDomain.VPCOptionsProperty", _IResolvable_9ceae33e]]=None) -> None:
        """Properties for defining a ``AWS::Elasticsearch::Domain``.

        :param access_policies: ``AWS::Elasticsearch::Domain.AccessPolicies``.
        :param advanced_options: ``AWS::Elasticsearch::Domain.AdvancedOptions``.
        :param cognito_options: ``AWS::Elasticsearch::Domain.CognitoOptions``.
        :param domain_name: ``AWS::Elasticsearch::Domain.DomainName``.
        :param ebs_options: ``AWS::Elasticsearch::Domain.EBSOptions``.
        :param elasticsearch_cluster_config: ``AWS::Elasticsearch::Domain.ElasticsearchClusterConfig``.
        :param elasticsearch_version: ``AWS::Elasticsearch::Domain.ElasticsearchVersion``.
        :param encryption_at_rest_options: ``AWS::Elasticsearch::Domain.EncryptionAtRestOptions``.
        :param log_publishing_options: ``AWS::Elasticsearch::Domain.LogPublishingOptions``.
        :param node_to_node_encryption_options: ``AWS::Elasticsearch::Domain.NodeToNodeEncryptionOptions``.
        :param snapshot_options: ``AWS::Elasticsearch::Domain.SnapshotOptions``.
        :param tags: ``AWS::Elasticsearch::Domain.Tags``.
        :param vpc_options: ``AWS::Elasticsearch::Domain.VPCOptions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html
        """
        self._values = {
        }
        if access_policies is not None: self._values["access_policies"] = access_policies
        if advanced_options is not None: self._values["advanced_options"] = advanced_options
        if cognito_options is not None: self._values["cognito_options"] = cognito_options
        if domain_name is not None: self._values["domain_name"] = domain_name
        if ebs_options is not None: self._values["ebs_options"] = ebs_options
        if elasticsearch_cluster_config is not None: self._values["elasticsearch_cluster_config"] = elasticsearch_cluster_config
        if elasticsearch_version is not None: self._values["elasticsearch_version"] = elasticsearch_version
        if encryption_at_rest_options is not None: self._values["encryption_at_rest_options"] = encryption_at_rest_options
        if log_publishing_options is not None: self._values["log_publishing_options"] = log_publishing_options
        if node_to_node_encryption_options is not None: self._values["node_to_node_encryption_options"] = node_to_node_encryption_options
        if snapshot_options is not None: self._values["snapshot_options"] = snapshot_options
        if tags is not None: self._values["tags"] = tags
        if vpc_options is not None: self._values["vpc_options"] = vpc_options

    @builtins.property
    def access_policies(self) -> typing.Any:
        """``AWS::Elasticsearch::Domain.AccessPolicies``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-accesspolicies
        """
        return self._values.get('access_policies')

    @builtins.property
    def advanced_options(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.Mapping[str, str]]]:
        """``AWS::Elasticsearch::Domain.AdvancedOptions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-advancedoptions
        """
        return self._values.get('advanced_options')

    @builtins.property
    def cognito_options(self) -> typing.Optional[typing.Union["CfnDomain.CognitoOptionsProperty", _IResolvable_9ceae33e]]:
        """``AWS::Elasticsearch::Domain.CognitoOptions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-cognitooptions
        """
        return self._values.get('cognito_options')

    @builtins.property
    def domain_name(self) -> typing.Optional[str]:
        """``AWS::Elasticsearch::Domain.DomainName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-domainname
        """
        return self._values.get('domain_name')

    @builtins.property
    def ebs_options(self) -> typing.Optional[typing.Union["CfnDomain.EBSOptionsProperty", _IResolvable_9ceae33e]]:
        """``AWS::Elasticsearch::Domain.EBSOptions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-ebsoptions
        """
        return self._values.get('ebs_options')

    @builtins.property
    def elasticsearch_cluster_config(self) -> typing.Optional[typing.Union["CfnDomain.ElasticsearchClusterConfigProperty", _IResolvable_9ceae33e]]:
        """``AWS::Elasticsearch::Domain.ElasticsearchClusterConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-elasticsearchclusterconfig
        """
        return self._values.get('elasticsearch_cluster_config')

    @builtins.property
    def elasticsearch_version(self) -> typing.Optional[str]:
        """``AWS::Elasticsearch::Domain.ElasticsearchVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-elasticsearchversion
        """
        return self._values.get('elasticsearch_version')

    @builtins.property
    def encryption_at_rest_options(self) -> typing.Optional[typing.Union["CfnDomain.EncryptionAtRestOptionsProperty", _IResolvable_9ceae33e]]:
        """``AWS::Elasticsearch::Domain.EncryptionAtRestOptions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-encryptionatrestoptions
        """
        return self._values.get('encryption_at_rest_options')

    @builtins.property
    def log_publishing_options(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.Mapping[str, typing.Union["CfnDomain.LogPublishingOptionProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::Elasticsearch::Domain.LogPublishingOptions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-logpublishingoptions
        """
        return self._values.get('log_publishing_options')

    @builtins.property
    def node_to_node_encryption_options(self) -> typing.Optional[typing.Union["CfnDomain.NodeToNodeEncryptionOptionsProperty", _IResolvable_9ceae33e]]:
        """``AWS::Elasticsearch::Domain.NodeToNodeEncryptionOptions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-nodetonodeencryptionoptions
        """
        return self._values.get('node_to_node_encryption_options')

    @builtins.property
    def snapshot_options(self) -> typing.Optional[typing.Union["CfnDomain.SnapshotOptionsProperty", _IResolvable_9ceae33e]]:
        """``AWS::Elasticsearch::Domain.SnapshotOptions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-snapshotoptions
        """
        return self._values.get('snapshot_options')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_b4661f1a]]:
        """``AWS::Elasticsearch::Domain.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-tags
        """
        return self._values.get('tags')

    @builtins.property
    def vpc_options(self) -> typing.Optional[typing.Union["CfnDomain.VPCOptionsProperty", _IResolvable_9ceae33e]]:
        """``AWS::Elasticsearch::Domain.VPCOptions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-vpcoptions
        """
        return self._values.get('vpc_options')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnDomainProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "CfnDomain",
    "CfnDomainProps",
]

publication.publish()
