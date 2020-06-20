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
class CfnContainer(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_mediastore.CfnContainer"):
    """A CloudFormation ``AWS::MediaStore::Container``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediastore-container.html
    cloudformationResource:
    :cloudformationResource:: AWS::MediaStore::Container
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, container_name: str, access_logging_enabled: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, cors_policy: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CorsRuleProperty", _IResolvable_9ceae33e]]]]=None, lifecycle_policy: typing.Optional[str]=None, metric_policy: typing.Optional[typing.Union["MetricPolicyProperty", _IResolvable_9ceae33e]]=None, policy: typing.Optional[str]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None) -> None:
        """Create a new ``AWS::MediaStore::Container``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param container_name: ``AWS::MediaStore::Container.ContainerName``.
        :param access_logging_enabled: ``AWS::MediaStore::Container.AccessLoggingEnabled``.
        :param cors_policy: ``AWS::MediaStore::Container.CorsPolicy``.
        :param lifecycle_policy: ``AWS::MediaStore::Container.LifecyclePolicy``.
        :param metric_policy: ``AWS::MediaStore::Container.MetricPolicy``.
        :param policy: ``AWS::MediaStore::Container.Policy``.
        :param tags: ``AWS::MediaStore::Container.Tags``.
        """
        props = CfnContainerProps(container_name=container_name, access_logging_enabled=access_logging_enabled, cors_policy=cors_policy, lifecycle_policy=lifecycle_policy, metric_policy=metric_policy, policy=policy, tags=tags)

        jsii.create(CfnContainer, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnContainer":
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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::MediaStore::Container.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediastore-container.html#cfn-mediastore-container-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="containerName")
    def container_name(self) -> str:
        """``AWS::MediaStore::Container.ContainerName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediastore-container.html#cfn-mediastore-container-containername
        """
        return jsii.get(self, "containerName")

    @container_name.setter
    def container_name(self, value: str) -> None:
        jsii.set(self, "containerName", value)

    @builtins.property
    @jsii.member(jsii_name="accessLoggingEnabled")
    def access_logging_enabled(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::MediaStore::Container.AccessLoggingEnabled``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediastore-container.html#cfn-mediastore-container-accessloggingenabled
        """
        return jsii.get(self, "accessLoggingEnabled")

    @access_logging_enabled.setter
    def access_logging_enabled(self, value: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "accessLoggingEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="corsPolicy")
    def cors_policy(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CorsRuleProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::MediaStore::Container.CorsPolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediastore-container.html#cfn-mediastore-container-corspolicy
        """
        return jsii.get(self, "corsPolicy")

    @cors_policy.setter
    def cors_policy(self, value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CorsRuleProperty", _IResolvable_9ceae33e]]]]) -> None:
        jsii.set(self, "corsPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="lifecyclePolicy")
    def lifecycle_policy(self) -> typing.Optional[str]:
        """``AWS::MediaStore::Container.LifecyclePolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediastore-container.html#cfn-mediastore-container-lifecyclepolicy
        """
        return jsii.get(self, "lifecyclePolicy")

    @lifecycle_policy.setter
    def lifecycle_policy(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "lifecyclePolicy", value)

    @builtins.property
    @jsii.member(jsii_name="metricPolicy")
    def metric_policy(self) -> typing.Optional[typing.Union["MetricPolicyProperty", _IResolvable_9ceae33e]]:
        """``AWS::MediaStore::Container.MetricPolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediastore-container.html#cfn-mediastore-container-metricpolicy
        """
        return jsii.get(self, "metricPolicy")

    @metric_policy.setter
    def metric_policy(self, value: typing.Optional[typing.Union["MetricPolicyProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "metricPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(self) -> typing.Optional[str]:
        """``AWS::MediaStore::Container.Policy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediastore-container.html#cfn-mediastore-container-policy
        """
        return jsii.get(self, "policy")

    @policy.setter
    def policy(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "policy", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_mediastore.CfnContainer.CorsRuleProperty", jsii_struct_bases=[], name_mapping={'allowed_headers': 'allowedHeaders', 'allowed_methods': 'allowedMethods', 'allowed_origins': 'allowedOrigins', 'expose_headers': 'exposeHeaders', 'max_age_seconds': 'maxAgeSeconds'})
    class CorsRuleProperty():
        def __init__(self, *, allowed_headers: typing.Optional[typing.List[str]]=None, allowed_methods: typing.Optional[typing.List[str]]=None, allowed_origins: typing.Optional[typing.List[str]]=None, expose_headers: typing.Optional[typing.List[str]]=None, max_age_seconds: typing.Optional[jsii.Number]=None) -> None:
            """
            :param allowed_headers: ``CfnContainer.CorsRuleProperty.AllowedHeaders``.
            :param allowed_methods: ``CfnContainer.CorsRuleProperty.AllowedMethods``.
            :param allowed_origins: ``CfnContainer.CorsRuleProperty.AllowedOrigins``.
            :param expose_headers: ``CfnContainer.CorsRuleProperty.ExposeHeaders``.
            :param max_age_seconds: ``CfnContainer.CorsRuleProperty.MaxAgeSeconds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediastore-container-corsrule.html
            """
            self._values = {
            }
            if allowed_headers is not None: self._values["allowed_headers"] = allowed_headers
            if allowed_methods is not None: self._values["allowed_methods"] = allowed_methods
            if allowed_origins is not None: self._values["allowed_origins"] = allowed_origins
            if expose_headers is not None: self._values["expose_headers"] = expose_headers
            if max_age_seconds is not None: self._values["max_age_seconds"] = max_age_seconds

        @builtins.property
        def allowed_headers(self) -> typing.Optional[typing.List[str]]:
            """``CfnContainer.CorsRuleProperty.AllowedHeaders``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediastore-container-corsrule.html#cfn-mediastore-container-corsrule-allowedheaders
            """
            return self._values.get('allowed_headers')

        @builtins.property
        def allowed_methods(self) -> typing.Optional[typing.List[str]]:
            """``CfnContainer.CorsRuleProperty.AllowedMethods``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediastore-container-corsrule.html#cfn-mediastore-container-corsrule-allowedmethods
            """
            return self._values.get('allowed_methods')

        @builtins.property
        def allowed_origins(self) -> typing.Optional[typing.List[str]]:
            """``CfnContainer.CorsRuleProperty.AllowedOrigins``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediastore-container-corsrule.html#cfn-mediastore-container-corsrule-allowedorigins
            """
            return self._values.get('allowed_origins')

        @builtins.property
        def expose_headers(self) -> typing.Optional[typing.List[str]]:
            """``CfnContainer.CorsRuleProperty.ExposeHeaders``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediastore-container-corsrule.html#cfn-mediastore-container-corsrule-exposeheaders
            """
            return self._values.get('expose_headers')

        @builtins.property
        def max_age_seconds(self) -> typing.Optional[jsii.Number]:
            """``CfnContainer.CorsRuleProperty.MaxAgeSeconds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediastore-container-corsrule.html#cfn-mediastore-container-corsrule-maxageseconds
            """
            return self._values.get('max_age_seconds')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'CorsRuleProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_mediastore.CfnContainer.MetricPolicyProperty", jsii_struct_bases=[], name_mapping={'container_level_metrics': 'containerLevelMetrics', 'metric_policy_rules': 'metricPolicyRules'})
    class MetricPolicyProperty():
        def __init__(self, *, container_level_metrics: str, metric_policy_rules: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnContainer.MetricPolicyRuleProperty", _IResolvable_9ceae33e]]]]=None) -> None:
            """
            :param container_level_metrics: ``CfnContainer.MetricPolicyProperty.ContainerLevelMetrics``.
            :param metric_policy_rules: ``CfnContainer.MetricPolicyProperty.MetricPolicyRules``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediastore-container-metricpolicy.html
            """
            self._values = {
                'container_level_metrics': container_level_metrics,
            }
            if metric_policy_rules is not None: self._values["metric_policy_rules"] = metric_policy_rules

        @builtins.property
        def container_level_metrics(self) -> str:
            """``CfnContainer.MetricPolicyProperty.ContainerLevelMetrics``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediastore-container-metricpolicy.html#cfn-mediastore-container-metricpolicy-containerlevelmetrics
            """
            return self._values.get('container_level_metrics')

        @builtins.property
        def metric_policy_rules(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnContainer.MetricPolicyRuleProperty", _IResolvable_9ceae33e]]]]:
            """``CfnContainer.MetricPolicyProperty.MetricPolicyRules``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediastore-container-metricpolicy.html#cfn-mediastore-container-metricpolicy-metricpolicyrules
            """
            return self._values.get('metric_policy_rules')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'MetricPolicyProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_mediastore.CfnContainer.MetricPolicyRuleProperty", jsii_struct_bases=[], name_mapping={'object_group': 'objectGroup', 'object_group_name': 'objectGroupName'})
    class MetricPolicyRuleProperty():
        def __init__(self, *, object_group: str, object_group_name: str) -> None:
            """
            :param object_group: ``CfnContainer.MetricPolicyRuleProperty.ObjectGroup``.
            :param object_group_name: ``CfnContainer.MetricPolicyRuleProperty.ObjectGroupName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediastore-container-metricpolicyrule.html
            """
            self._values = {
                'object_group': object_group,
                'object_group_name': object_group_name,
            }

        @builtins.property
        def object_group(self) -> str:
            """``CfnContainer.MetricPolicyRuleProperty.ObjectGroup``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediastore-container-metricpolicyrule.html#cfn-mediastore-container-metricpolicyrule-objectgroup
            """
            return self._values.get('object_group')

        @builtins.property
        def object_group_name(self) -> str:
            """``CfnContainer.MetricPolicyRuleProperty.ObjectGroupName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediastore-container-metricpolicyrule.html#cfn-mediastore-container-metricpolicyrule-objectgroupname
            """
            return self._values.get('object_group_name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'MetricPolicyRuleProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_mediastore.CfnContainerProps", jsii_struct_bases=[], name_mapping={'container_name': 'containerName', 'access_logging_enabled': 'accessLoggingEnabled', 'cors_policy': 'corsPolicy', 'lifecycle_policy': 'lifecyclePolicy', 'metric_policy': 'metricPolicy', 'policy': 'policy', 'tags': 'tags'})
class CfnContainerProps():
    def __init__(self, *, container_name: str, access_logging_enabled: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, cors_policy: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnContainer.CorsRuleProperty", _IResolvable_9ceae33e]]]]=None, lifecycle_policy: typing.Optional[str]=None, metric_policy: typing.Optional[typing.Union["CfnContainer.MetricPolicyProperty", _IResolvable_9ceae33e]]=None, policy: typing.Optional[str]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None) -> None:
        """Properties for defining a ``AWS::MediaStore::Container``.

        :param container_name: ``AWS::MediaStore::Container.ContainerName``.
        :param access_logging_enabled: ``AWS::MediaStore::Container.AccessLoggingEnabled``.
        :param cors_policy: ``AWS::MediaStore::Container.CorsPolicy``.
        :param lifecycle_policy: ``AWS::MediaStore::Container.LifecyclePolicy``.
        :param metric_policy: ``AWS::MediaStore::Container.MetricPolicy``.
        :param policy: ``AWS::MediaStore::Container.Policy``.
        :param tags: ``AWS::MediaStore::Container.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediastore-container.html
        """
        self._values = {
            'container_name': container_name,
        }
        if access_logging_enabled is not None: self._values["access_logging_enabled"] = access_logging_enabled
        if cors_policy is not None: self._values["cors_policy"] = cors_policy
        if lifecycle_policy is not None: self._values["lifecycle_policy"] = lifecycle_policy
        if metric_policy is not None: self._values["metric_policy"] = metric_policy
        if policy is not None: self._values["policy"] = policy
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def container_name(self) -> str:
        """``AWS::MediaStore::Container.ContainerName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediastore-container.html#cfn-mediastore-container-containername
        """
        return self._values.get('container_name')

    @builtins.property
    def access_logging_enabled(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::MediaStore::Container.AccessLoggingEnabled``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediastore-container.html#cfn-mediastore-container-accessloggingenabled
        """
        return self._values.get('access_logging_enabled')

    @builtins.property
    def cors_policy(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnContainer.CorsRuleProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::MediaStore::Container.CorsPolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediastore-container.html#cfn-mediastore-container-corspolicy
        """
        return self._values.get('cors_policy')

    @builtins.property
    def lifecycle_policy(self) -> typing.Optional[str]:
        """``AWS::MediaStore::Container.LifecyclePolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediastore-container.html#cfn-mediastore-container-lifecyclepolicy
        """
        return self._values.get('lifecycle_policy')

    @builtins.property
    def metric_policy(self) -> typing.Optional[typing.Union["CfnContainer.MetricPolicyProperty", _IResolvable_9ceae33e]]:
        """``AWS::MediaStore::Container.MetricPolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediastore-container.html#cfn-mediastore-container-metricpolicy
        """
        return self._values.get('metric_policy')

    @builtins.property
    def policy(self) -> typing.Optional[str]:
        """``AWS::MediaStore::Container.Policy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediastore-container.html#cfn-mediastore-container-policy
        """
        return self._values.get('policy')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_b4661f1a]]:
        """``AWS::MediaStore::Container.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediastore-container.html#cfn-mediastore-container-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnContainerProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "CfnContainer",
    "CfnContainerProps",
]

publication.publish()
