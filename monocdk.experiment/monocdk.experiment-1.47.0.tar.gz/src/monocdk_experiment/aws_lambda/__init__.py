import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *

from .. import (Construct as _Construct_f50a3f53, Duration as _Duration_5170c158, CfnResource as _CfnResource_7760e8e4, FromCloudFormationOptions as _FromCloudFormationOptions_5f49f6f1, TreeInspector as _TreeInspector_154f5999, IResolvable as _IResolvable_9ceae33e, IInspectable as _IInspectable_051e6ed8, TagManager as _TagManager_2508893f, CfnTag as _CfnTag_b4661f1a, CfnParameter as _CfnParameter_90f1d0df, Resource as _Resource_884d0774, ConstructNode as _ConstructNode_6884f5de, ResourceProps as _ResourceProps_92be6f66, IResource as _IResource_72f7ee7e, BundlingDockerImage as _BundlingDockerImage_5a43b005, IDependable as _IDependable_4fc803f7, IConstruct as _IConstruct_db0cc7e3, RemovalPolicy as _RemovalPolicy_5986e9f3)
from ..aws_cloudwatch import (Metric as _Metric_53e89548, MetricOptions as _MetricOptions_ad2c4d5d)
from ..aws_ec2 import (ISecurityGroup as _ISecurityGroup_d72ab8e8, Connections as _Connections_231f38b5, IVpc as _IVpc_3795853f, SubnetSelection as _SubnetSelection_36a13cd6, IConnectable as _IConnectable_a587039f)
from ..aws_iam import (IPrincipal as _IPrincipal_97126874, IRole as _IRole_e69bbae4, PolicyStatement as _PolicyStatement_f75dc775, Grant as _Grant_96af6d2d, IGrantable as _IGrantable_0fcfc53a)
from ..aws_logs import (ILogGroup as _ILogGroup_6b54c8e1, RetentionDays as _RetentionDays_bdc7ad1f)
from ..aws_s3 import (Location as _Location_2d2ff215, IBucket as _IBucket_25bad983)
from ..aws_s3_assets import (AssetOptions as _AssetOptions_ed6c2956)
from ..aws_sqs import (IQueue as _IQueue_b743f559)


@jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.AliasAttributes", jsii_struct_bases=[], name_mapping={'alias_name': 'aliasName', 'alias_version': 'aliasVersion'})
class AliasAttributes():
    def __init__(self, *, alias_name: str, alias_version: "IVersion") -> None:
        """
        :param alias_name: 
        :param alias_version: 

        stability
        :stability: experimental
        """
        self._values = {
            'alias_name': alias_name,
            'alias_version': alias_version,
        }

    @builtins.property
    def alias_name(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get('alias_name')

    @builtins.property
    def alias_version(self) -> "IVersion":
        """
        stability
        :stability: experimental
        """
        return self._values.get('alias_version')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AliasAttributes(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnAlias(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_lambda.CfnAlias"):
    """A CloudFormation ``AWS::Lambda::Alias``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-alias.html
    cloudformationResource:
    :cloudformationResource:: AWS::Lambda::Alias
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, function_name: str, function_version: str, name: str, description: typing.Optional[str]=None, provisioned_concurrency_config: typing.Optional[typing.Union["ProvisionedConcurrencyConfigurationProperty", _IResolvable_9ceae33e]]=None, routing_config: typing.Optional[typing.Union["AliasRoutingConfigurationProperty", _IResolvable_9ceae33e]]=None) -> None:
        """Create a new ``AWS::Lambda::Alias``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param function_name: ``AWS::Lambda::Alias.FunctionName``.
        :param function_version: ``AWS::Lambda::Alias.FunctionVersion``.
        :param name: ``AWS::Lambda::Alias.Name``.
        :param description: ``AWS::Lambda::Alias.Description``.
        :param provisioned_concurrency_config: ``AWS::Lambda::Alias.ProvisionedConcurrencyConfig``.
        :param routing_config: ``AWS::Lambda::Alias.RoutingConfig``.
        """
        props = CfnAliasProps(function_name=function_name, function_version=function_version, name=name, description=description, provisioned_concurrency_config=provisioned_concurrency_config, routing_config=routing_config)

        jsii.create(CfnAlias, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnAlias":
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
    @jsii.member(jsii_name="functionName")
    def function_name(self) -> str:
        """``AWS::Lambda::Alias.FunctionName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-alias.html#cfn-lambda-alias-functionname
        """
        return jsii.get(self, "functionName")

    @function_name.setter
    def function_name(self, value: str) -> None:
        jsii.set(self, "functionName", value)

    @builtins.property
    @jsii.member(jsii_name="functionVersion")
    def function_version(self) -> str:
        """``AWS::Lambda::Alias.FunctionVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-alias.html#cfn-lambda-alias-functionversion
        """
        return jsii.get(self, "functionVersion")

    @function_version.setter
    def function_version(self, value: str) -> None:
        jsii.set(self, "functionVersion", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """``AWS::Lambda::Alias.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-alias.html#cfn-lambda-alias-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::Lambda::Alias.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-alias.html#cfn-lambda-alias-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="provisionedConcurrencyConfig")
    def provisioned_concurrency_config(self) -> typing.Optional[typing.Union["ProvisionedConcurrencyConfigurationProperty", _IResolvable_9ceae33e]]:
        """``AWS::Lambda::Alias.ProvisionedConcurrencyConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-alias.html#cfn-lambda-alias-provisionedconcurrencyconfig
        """
        return jsii.get(self, "provisionedConcurrencyConfig")

    @provisioned_concurrency_config.setter
    def provisioned_concurrency_config(self, value: typing.Optional[typing.Union["ProvisionedConcurrencyConfigurationProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "provisionedConcurrencyConfig", value)

    @builtins.property
    @jsii.member(jsii_name="routingConfig")
    def routing_config(self) -> typing.Optional[typing.Union["AliasRoutingConfigurationProperty", _IResolvable_9ceae33e]]:
        """``AWS::Lambda::Alias.RoutingConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-alias.html#cfn-lambda-alias-routingconfig
        """
        return jsii.get(self, "routingConfig")

    @routing_config.setter
    def routing_config(self, value: typing.Optional[typing.Union["AliasRoutingConfigurationProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "routingConfig", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.CfnAlias.AliasRoutingConfigurationProperty", jsii_struct_bases=[], name_mapping={'additional_version_weights': 'additionalVersionWeights'})
    class AliasRoutingConfigurationProperty():
        def __init__(self, *, additional_version_weights: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnAlias.VersionWeightProperty", _IResolvable_9ceae33e]]]) -> None:
            """
            :param additional_version_weights: ``CfnAlias.AliasRoutingConfigurationProperty.AdditionalVersionWeights``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-alias-aliasroutingconfiguration.html
            """
            self._values = {
                'additional_version_weights': additional_version_weights,
            }

        @builtins.property
        def additional_version_weights(self) -> typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnAlias.VersionWeightProperty", _IResolvable_9ceae33e]]]:
            """``CfnAlias.AliasRoutingConfigurationProperty.AdditionalVersionWeights``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-alias-aliasroutingconfiguration.html#cfn-lambda-alias-aliasroutingconfiguration-additionalversionweights
            """
            return self._values.get('additional_version_weights')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AliasRoutingConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.CfnAlias.ProvisionedConcurrencyConfigurationProperty", jsii_struct_bases=[], name_mapping={'provisioned_concurrent_executions': 'provisionedConcurrentExecutions'})
    class ProvisionedConcurrencyConfigurationProperty():
        def __init__(self, *, provisioned_concurrent_executions: jsii.Number) -> None:
            """
            :param provisioned_concurrent_executions: ``CfnAlias.ProvisionedConcurrencyConfigurationProperty.ProvisionedConcurrentExecutions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-alias-provisionedconcurrencyconfiguration.html
            """
            self._values = {
                'provisioned_concurrent_executions': provisioned_concurrent_executions,
            }

        @builtins.property
        def provisioned_concurrent_executions(self) -> jsii.Number:
            """``CfnAlias.ProvisionedConcurrencyConfigurationProperty.ProvisionedConcurrentExecutions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-alias-provisionedconcurrencyconfiguration.html#cfn-lambda-alias-provisionedconcurrencyconfiguration-provisionedconcurrentexecutions
            """
            return self._values.get('provisioned_concurrent_executions')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ProvisionedConcurrencyConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.CfnAlias.VersionWeightProperty", jsii_struct_bases=[], name_mapping={'function_version': 'functionVersion', 'function_weight': 'functionWeight'})
    class VersionWeightProperty():
        def __init__(self, *, function_version: str, function_weight: jsii.Number) -> None:
            """
            :param function_version: ``CfnAlias.VersionWeightProperty.FunctionVersion``.
            :param function_weight: ``CfnAlias.VersionWeightProperty.FunctionWeight``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-alias-versionweight.html
            """
            self._values = {
                'function_version': function_version,
                'function_weight': function_weight,
            }

        @builtins.property
        def function_version(self) -> str:
            """``CfnAlias.VersionWeightProperty.FunctionVersion``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-alias-versionweight.html#cfn-lambda-alias-versionweight-functionversion
            """
            return self._values.get('function_version')

        @builtins.property
        def function_weight(self) -> jsii.Number:
            """``CfnAlias.VersionWeightProperty.FunctionWeight``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-alias-versionweight.html#cfn-lambda-alias-versionweight-functionweight
            """
            return self._values.get('function_weight')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'VersionWeightProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.CfnAliasProps", jsii_struct_bases=[], name_mapping={'function_name': 'functionName', 'function_version': 'functionVersion', 'name': 'name', 'description': 'description', 'provisioned_concurrency_config': 'provisionedConcurrencyConfig', 'routing_config': 'routingConfig'})
class CfnAliasProps():
    def __init__(self, *, function_name: str, function_version: str, name: str, description: typing.Optional[str]=None, provisioned_concurrency_config: typing.Optional[typing.Union["CfnAlias.ProvisionedConcurrencyConfigurationProperty", _IResolvable_9ceae33e]]=None, routing_config: typing.Optional[typing.Union["CfnAlias.AliasRoutingConfigurationProperty", _IResolvable_9ceae33e]]=None) -> None:
        """Properties for defining a ``AWS::Lambda::Alias``.

        :param function_name: ``AWS::Lambda::Alias.FunctionName``.
        :param function_version: ``AWS::Lambda::Alias.FunctionVersion``.
        :param name: ``AWS::Lambda::Alias.Name``.
        :param description: ``AWS::Lambda::Alias.Description``.
        :param provisioned_concurrency_config: ``AWS::Lambda::Alias.ProvisionedConcurrencyConfig``.
        :param routing_config: ``AWS::Lambda::Alias.RoutingConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-alias.html
        """
        self._values = {
            'function_name': function_name,
            'function_version': function_version,
            'name': name,
        }
        if description is not None: self._values["description"] = description
        if provisioned_concurrency_config is not None: self._values["provisioned_concurrency_config"] = provisioned_concurrency_config
        if routing_config is not None: self._values["routing_config"] = routing_config

    @builtins.property
    def function_name(self) -> str:
        """``AWS::Lambda::Alias.FunctionName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-alias.html#cfn-lambda-alias-functionname
        """
        return self._values.get('function_name')

    @builtins.property
    def function_version(self) -> str:
        """``AWS::Lambda::Alias.FunctionVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-alias.html#cfn-lambda-alias-functionversion
        """
        return self._values.get('function_version')

    @builtins.property
    def name(self) -> str:
        """``AWS::Lambda::Alias.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-alias.html#cfn-lambda-alias-name
        """
        return self._values.get('name')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::Lambda::Alias.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-alias.html#cfn-lambda-alias-description
        """
        return self._values.get('description')

    @builtins.property
    def provisioned_concurrency_config(self) -> typing.Optional[typing.Union["CfnAlias.ProvisionedConcurrencyConfigurationProperty", _IResolvable_9ceae33e]]:
        """``AWS::Lambda::Alias.ProvisionedConcurrencyConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-alias.html#cfn-lambda-alias-provisionedconcurrencyconfig
        """
        return self._values.get('provisioned_concurrency_config')

    @builtins.property
    def routing_config(self) -> typing.Optional[typing.Union["CfnAlias.AliasRoutingConfigurationProperty", _IResolvable_9ceae33e]]:
        """``AWS::Lambda::Alias.RoutingConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-alias.html#cfn-lambda-alias-routingconfig
        """
        return self._values.get('routing_config')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnAliasProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnEventInvokeConfig(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_lambda.CfnEventInvokeConfig"):
    """A CloudFormation ``AWS::Lambda::EventInvokeConfig``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventinvokeconfig.html
    cloudformationResource:
    :cloudformationResource:: AWS::Lambda::EventInvokeConfig
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, function_name: str, qualifier: str, destination_config: typing.Optional[typing.Union["DestinationConfigProperty", _IResolvable_9ceae33e]]=None, maximum_event_age_in_seconds: typing.Optional[jsii.Number]=None, maximum_retry_attempts: typing.Optional[jsii.Number]=None) -> None:
        """Create a new ``AWS::Lambda::EventInvokeConfig``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param function_name: ``AWS::Lambda::EventInvokeConfig.FunctionName``.
        :param qualifier: ``AWS::Lambda::EventInvokeConfig.Qualifier``.
        :param destination_config: ``AWS::Lambda::EventInvokeConfig.DestinationConfig``.
        :param maximum_event_age_in_seconds: ``AWS::Lambda::EventInvokeConfig.MaximumEventAgeInSeconds``.
        :param maximum_retry_attempts: ``AWS::Lambda::EventInvokeConfig.MaximumRetryAttempts``.
        """
        props = CfnEventInvokeConfigProps(function_name=function_name, qualifier=qualifier, destination_config=destination_config, maximum_event_age_in_seconds=maximum_event_age_in_seconds, maximum_retry_attempts=maximum_retry_attempts)

        jsii.create(CfnEventInvokeConfig, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnEventInvokeConfig":
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
    @jsii.member(jsii_name="functionName")
    def function_name(self) -> str:
        """``AWS::Lambda::EventInvokeConfig.FunctionName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventinvokeconfig.html#cfn-lambda-eventinvokeconfig-functionname
        """
        return jsii.get(self, "functionName")

    @function_name.setter
    def function_name(self, value: str) -> None:
        jsii.set(self, "functionName", value)

    @builtins.property
    @jsii.member(jsii_name="qualifier")
    def qualifier(self) -> str:
        """``AWS::Lambda::EventInvokeConfig.Qualifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventinvokeconfig.html#cfn-lambda-eventinvokeconfig-qualifier
        """
        return jsii.get(self, "qualifier")

    @qualifier.setter
    def qualifier(self, value: str) -> None:
        jsii.set(self, "qualifier", value)

    @builtins.property
    @jsii.member(jsii_name="destinationConfig")
    def destination_config(self) -> typing.Optional[typing.Union["DestinationConfigProperty", _IResolvable_9ceae33e]]:
        """``AWS::Lambda::EventInvokeConfig.DestinationConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventinvokeconfig.html#cfn-lambda-eventinvokeconfig-destinationconfig
        """
        return jsii.get(self, "destinationConfig")

    @destination_config.setter
    def destination_config(self, value: typing.Optional[typing.Union["DestinationConfigProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "destinationConfig", value)

    @builtins.property
    @jsii.member(jsii_name="maximumEventAgeInSeconds")
    def maximum_event_age_in_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::Lambda::EventInvokeConfig.MaximumEventAgeInSeconds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventinvokeconfig.html#cfn-lambda-eventinvokeconfig-maximumeventageinseconds
        """
        return jsii.get(self, "maximumEventAgeInSeconds")

    @maximum_event_age_in_seconds.setter
    def maximum_event_age_in_seconds(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "maximumEventAgeInSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="maximumRetryAttempts")
    def maximum_retry_attempts(self) -> typing.Optional[jsii.Number]:
        """``AWS::Lambda::EventInvokeConfig.MaximumRetryAttempts``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventinvokeconfig.html#cfn-lambda-eventinvokeconfig-maximumretryattempts
        """
        return jsii.get(self, "maximumRetryAttempts")

    @maximum_retry_attempts.setter
    def maximum_retry_attempts(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "maximumRetryAttempts", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.CfnEventInvokeConfig.DestinationConfigProperty", jsii_struct_bases=[], name_mapping={'on_failure': 'onFailure', 'on_success': 'onSuccess'})
    class DestinationConfigProperty():
        def __init__(self, *, on_failure: typing.Optional[typing.Union["CfnEventInvokeConfig.OnFailureProperty", _IResolvable_9ceae33e]]=None, on_success: typing.Optional[typing.Union["CfnEventInvokeConfig.OnSuccessProperty", _IResolvable_9ceae33e]]=None) -> None:
            """
            :param on_failure: ``CfnEventInvokeConfig.DestinationConfigProperty.OnFailure``.
            :param on_success: ``CfnEventInvokeConfig.DestinationConfigProperty.OnSuccess``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventinvokeconfig-destinationconfig.html
            """
            self._values = {
            }
            if on_failure is not None: self._values["on_failure"] = on_failure
            if on_success is not None: self._values["on_success"] = on_success

        @builtins.property
        def on_failure(self) -> typing.Optional[typing.Union["CfnEventInvokeConfig.OnFailureProperty", _IResolvable_9ceae33e]]:
            """``CfnEventInvokeConfig.DestinationConfigProperty.OnFailure``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventinvokeconfig-destinationconfig.html#cfn-lambda-eventinvokeconfig-destinationconfig-onfailure
            """
            return self._values.get('on_failure')

        @builtins.property
        def on_success(self) -> typing.Optional[typing.Union["CfnEventInvokeConfig.OnSuccessProperty", _IResolvable_9ceae33e]]:
            """``CfnEventInvokeConfig.DestinationConfigProperty.OnSuccess``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventinvokeconfig-destinationconfig.html#cfn-lambda-eventinvokeconfig-destinationconfig-onsuccess
            """
            return self._values.get('on_success')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'DestinationConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.CfnEventInvokeConfig.OnFailureProperty", jsii_struct_bases=[], name_mapping={'destination': 'destination'})
    class OnFailureProperty():
        def __init__(self, *, destination: str) -> None:
            """
            :param destination: ``CfnEventInvokeConfig.OnFailureProperty.Destination``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventinvokeconfig-destinationconfig-onfailure.html
            """
            self._values = {
                'destination': destination,
            }

        @builtins.property
        def destination(self) -> str:
            """``CfnEventInvokeConfig.OnFailureProperty.Destination``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventinvokeconfig-destinationconfig-onfailure.html#cfn-lambda-eventinvokeconfig-destinationconfig-onfailure-destination
            """
            return self._values.get('destination')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'OnFailureProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.CfnEventInvokeConfig.OnSuccessProperty", jsii_struct_bases=[], name_mapping={'destination': 'destination'})
    class OnSuccessProperty():
        def __init__(self, *, destination: str) -> None:
            """
            :param destination: ``CfnEventInvokeConfig.OnSuccessProperty.Destination``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventinvokeconfig-destinationconfig-onsuccess.html
            """
            self._values = {
                'destination': destination,
            }

        @builtins.property
        def destination(self) -> str:
            """``CfnEventInvokeConfig.OnSuccessProperty.Destination``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventinvokeconfig-destinationconfig-onsuccess.html#cfn-lambda-eventinvokeconfig-destinationconfig-onsuccess-destination
            """
            return self._values.get('destination')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'OnSuccessProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.CfnEventInvokeConfigProps", jsii_struct_bases=[], name_mapping={'function_name': 'functionName', 'qualifier': 'qualifier', 'destination_config': 'destinationConfig', 'maximum_event_age_in_seconds': 'maximumEventAgeInSeconds', 'maximum_retry_attempts': 'maximumRetryAttempts'})
class CfnEventInvokeConfigProps():
    def __init__(self, *, function_name: str, qualifier: str, destination_config: typing.Optional[typing.Union["CfnEventInvokeConfig.DestinationConfigProperty", _IResolvable_9ceae33e]]=None, maximum_event_age_in_seconds: typing.Optional[jsii.Number]=None, maximum_retry_attempts: typing.Optional[jsii.Number]=None) -> None:
        """Properties for defining a ``AWS::Lambda::EventInvokeConfig``.

        :param function_name: ``AWS::Lambda::EventInvokeConfig.FunctionName``.
        :param qualifier: ``AWS::Lambda::EventInvokeConfig.Qualifier``.
        :param destination_config: ``AWS::Lambda::EventInvokeConfig.DestinationConfig``.
        :param maximum_event_age_in_seconds: ``AWS::Lambda::EventInvokeConfig.MaximumEventAgeInSeconds``.
        :param maximum_retry_attempts: ``AWS::Lambda::EventInvokeConfig.MaximumRetryAttempts``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventinvokeconfig.html
        """
        self._values = {
            'function_name': function_name,
            'qualifier': qualifier,
        }
        if destination_config is not None: self._values["destination_config"] = destination_config
        if maximum_event_age_in_seconds is not None: self._values["maximum_event_age_in_seconds"] = maximum_event_age_in_seconds
        if maximum_retry_attempts is not None: self._values["maximum_retry_attempts"] = maximum_retry_attempts

    @builtins.property
    def function_name(self) -> str:
        """``AWS::Lambda::EventInvokeConfig.FunctionName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventinvokeconfig.html#cfn-lambda-eventinvokeconfig-functionname
        """
        return self._values.get('function_name')

    @builtins.property
    def qualifier(self) -> str:
        """``AWS::Lambda::EventInvokeConfig.Qualifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventinvokeconfig.html#cfn-lambda-eventinvokeconfig-qualifier
        """
        return self._values.get('qualifier')

    @builtins.property
    def destination_config(self) -> typing.Optional[typing.Union["CfnEventInvokeConfig.DestinationConfigProperty", _IResolvable_9ceae33e]]:
        """``AWS::Lambda::EventInvokeConfig.DestinationConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventinvokeconfig.html#cfn-lambda-eventinvokeconfig-destinationconfig
        """
        return self._values.get('destination_config')

    @builtins.property
    def maximum_event_age_in_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::Lambda::EventInvokeConfig.MaximumEventAgeInSeconds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventinvokeconfig.html#cfn-lambda-eventinvokeconfig-maximumeventageinseconds
        """
        return self._values.get('maximum_event_age_in_seconds')

    @builtins.property
    def maximum_retry_attempts(self) -> typing.Optional[jsii.Number]:
        """``AWS::Lambda::EventInvokeConfig.MaximumRetryAttempts``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventinvokeconfig.html#cfn-lambda-eventinvokeconfig-maximumretryattempts
        """
        return self._values.get('maximum_retry_attempts')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnEventInvokeConfigProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnEventSourceMapping(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_lambda.CfnEventSourceMapping"):
    """A CloudFormation ``AWS::Lambda::EventSourceMapping``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html
    cloudformationResource:
    :cloudformationResource:: AWS::Lambda::EventSourceMapping
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, event_source_arn: str, function_name: str, batch_size: typing.Optional[jsii.Number]=None, bisect_batch_on_function_error: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, destination_config: typing.Optional[typing.Union["DestinationConfigProperty", _IResolvable_9ceae33e]]=None, enabled: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, maximum_batching_window_in_seconds: typing.Optional[jsii.Number]=None, maximum_record_age_in_seconds: typing.Optional[jsii.Number]=None, maximum_retry_attempts: typing.Optional[jsii.Number]=None, parallelization_factor: typing.Optional[jsii.Number]=None, starting_position: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::Lambda::EventSourceMapping``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param event_source_arn: ``AWS::Lambda::EventSourceMapping.EventSourceArn``.
        :param function_name: ``AWS::Lambda::EventSourceMapping.FunctionName``.
        :param batch_size: ``AWS::Lambda::EventSourceMapping.BatchSize``.
        :param bisect_batch_on_function_error: ``AWS::Lambda::EventSourceMapping.BisectBatchOnFunctionError``.
        :param destination_config: ``AWS::Lambda::EventSourceMapping.DestinationConfig``.
        :param enabled: ``AWS::Lambda::EventSourceMapping.Enabled``.
        :param maximum_batching_window_in_seconds: ``AWS::Lambda::EventSourceMapping.MaximumBatchingWindowInSeconds``.
        :param maximum_record_age_in_seconds: ``AWS::Lambda::EventSourceMapping.MaximumRecordAgeInSeconds``.
        :param maximum_retry_attempts: ``AWS::Lambda::EventSourceMapping.MaximumRetryAttempts``.
        :param parallelization_factor: ``AWS::Lambda::EventSourceMapping.ParallelizationFactor``.
        :param starting_position: ``AWS::Lambda::EventSourceMapping.StartingPosition``.
        """
        props = CfnEventSourceMappingProps(event_source_arn=event_source_arn, function_name=function_name, batch_size=batch_size, bisect_batch_on_function_error=bisect_batch_on_function_error, destination_config=destination_config, enabled=enabled, maximum_batching_window_in_seconds=maximum_batching_window_in_seconds, maximum_record_age_in_seconds=maximum_record_age_in_seconds, maximum_retry_attempts=maximum_retry_attempts, parallelization_factor=parallelization_factor, starting_position=starting_position)

        jsii.create(CfnEventSourceMapping, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnEventSourceMapping":
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
    @jsii.member(jsii_name="eventSourceArn")
    def event_source_arn(self) -> str:
        """``AWS::Lambda::EventSourceMapping.EventSourceArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-eventsourcearn
        """
        return jsii.get(self, "eventSourceArn")

    @event_source_arn.setter
    def event_source_arn(self, value: str) -> None:
        jsii.set(self, "eventSourceArn", value)

    @builtins.property
    @jsii.member(jsii_name="functionName")
    def function_name(self) -> str:
        """``AWS::Lambda::EventSourceMapping.FunctionName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-functionname
        """
        return jsii.get(self, "functionName")

    @function_name.setter
    def function_name(self, value: str) -> None:
        jsii.set(self, "functionName", value)

    @builtins.property
    @jsii.member(jsii_name="batchSize")
    def batch_size(self) -> typing.Optional[jsii.Number]:
        """``AWS::Lambda::EventSourceMapping.BatchSize``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-batchsize
        """
        return jsii.get(self, "batchSize")

    @batch_size.setter
    def batch_size(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "batchSize", value)

    @builtins.property
    @jsii.member(jsii_name="bisectBatchOnFunctionError")
    def bisect_batch_on_function_error(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::Lambda::EventSourceMapping.BisectBatchOnFunctionError``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-bisectbatchonfunctionerror
        """
        return jsii.get(self, "bisectBatchOnFunctionError")

    @bisect_batch_on_function_error.setter
    def bisect_batch_on_function_error(self, value: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "bisectBatchOnFunctionError", value)

    @builtins.property
    @jsii.member(jsii_name="destinationConfig")
    def destination_config(self) -> typing.Optional[typing.Union["DestinationConfigProperty", _IResolvable_9ceae33e]]:
        """``AWS::Lambda::EventSourceMapping.DestinationConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-destinationconfig
        """
        return jsii.get(self, "destinationConfig")

    @destination_config.setter
    def destination_config(self, value: typing.Optional[typing.Union["DestinationConfigProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "destinationConfig", value)

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::Lambda::EventSourceMapping.Enabled``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-enabled
        """
        return jsii.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="maximumBatchingWindowInSeconds")
    def maximum_batching_window_in_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::Lambda::EventSourceMapping.MaximumBatchingWindowInSeconds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-maximumbatchingwindowinseconds
        """
        return jsii.get(self, "maximumBatchingWindowInSeconds")

    @maximum_batching_window_in_seconds.setter
    def maximum_batching_window_in_seconds(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "maximumBatchingWindowInSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="maximumRecordAgeInSeconds")
    def maximum_record_age_in_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::Lambda::EventSourceMapping.MaximumRecordAgeInSeconds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-maximumrecordageinseconds
        """
        return jsii.get(self, "maximumRecordAgeInSeconds")

    @maximum_record_age_in_seconds.setter
    def maximum_record_age_in_seconds(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "maximumRecordAgeInSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="maximumRetryAttempts")
    def maximum_retry_attempts(self) -> typing.Optional[jsii.Number]:
        """``AWS::Lambda::EventSourceMapping.MaximumRetryAttempts``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-maximumretryattempts
        """
        return jsii.get(self, "maximumRetryAttempts")

    @maximum_retry_attempts.setter
    def maximum_retry_attempts(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "maximumRetryAttempts", value)

    @builtins.property
    @jsii.member(jsii_name="parallelizationFactor")
    def parallelization_factor(self) -> typing.Optional[jsii.Number]:
        """``AWS::Lambda::EventSourceMapping.ParallelizationFactor``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-parallelizationfactor
        """
        return jsii.get(self, "parallelizationFactor")

    @parallelization_factor.setter
    def parallelization_factor(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "parallelizationFactor", value)

    @builtins.property
    @jsii.member(jsii_name="startingPosition")
    def starting_position(self) -> typing.Optional[str]:
        """``AWS::Lambda::EventSourceMapping.StartingPosition``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-startingposition
        """
        return jsii.get(self, "startingPosition")

    @starting_position.setter
    def starting_position(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "startingPosition", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.CfnEventSourceMapping.DestinationConfigProperty", jsii_struct_bases=[], name_mapping={'on_failure': 'onFailure'})
    class DestinationConfigProperty():
        def __init__(self, *, on_failure: typing.Union["CfnEventSourceMapping.OnFailureProperty", _IResolvable_9ceae33e]) -> None:
            """
            :param on_failure: ``CfnEventSourceMapping.DestinationConfigProperty.OnFailure``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-destinationconfig.html
            """
            self._values = {
                'on_failure': on_failure,
            }

        @builtins.property
        def on_failure(self) -> typing.Union["CfnEventSourceMapping.OnFailureProperty", _IResolvable_9ceae33e]:
            """``CfnEventSourceMapping.DestinationConfigProperty.OnFailure``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-destinationconfig.html#cfn-lambda-eventsourcemapping-destinationconfig-onfailure
            """
            return self._values.get('on_failure')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'DestinationConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.CfnEventSourceMapping.OnFailureProperty", jsii_struct_bases=[], name_mapping={'destination': 'destination'})
    class OnFailureProperty():
        def __init__(self, *, destination: str) -> None:
            """
            :param destination: ``CfnEventSourceMapping.OnFailureProperty.Destination``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-onfailure.html
            """
            self._values = {
                'destination': destination,
            }

        @builtins.property
        def destination(self) -> str:
            """``CfnEventSourceMapping.OnFailureProperty.Destination``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-eventsourcemapping-onfailure.html#cfn-lambda-eventsourcemapping-onfailure-destination
            """
            return self._values.get('destination')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'OnFailureProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.CfnEventSourceMappingProps", jsii_struct_bases=[], name_mapping={'event_source_arn': 'eventSourceArn', 'function_name': 'functionName', 'batch_size': 'batchSize', 'bisect_batch_on_function_error': 'bisectBatchOnFunctionError', 'destination_config': 'destinationConfig', 'enabled': 'enabled', 'maximum_batching_window_in_seconds': 'maximumBatchingWindowInSeconds', 'maximum_record_age_in_seconds': 'maximumRecordAgeInSeconds', 'maximum_retry_attempts': 'maximumRetryAttempts', 'parallelization_factor': 'parallelizationFactor', 'starting_position': 'startingPosition'})
class CfnEventSourceMappingProps():
    def __init__(self, *, event_source_arn: str, function_name: str, batch_size: typing.Optional[jsii.Number]=None, bisect_batch_on_function_error: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, destination_config: typing.Optional[typing.Union["CfnEventSourceMapping.DestinationConfigProperty", _IResolvable_9ceae33e]]=None, enabled: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, maximum_batching_window_in_seconds: typing.Optional[jsii.Number]=None, maximum_record_age_in_seconds: typing.Optional[jsii.Number]=None, maximum_retry_attempts: typing.Optional[jsii.Number]=None, parallelization_factor: typing.Optional[jsii.Number]=None, starting_position: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::Lambda::EventSourceMapping``.

        :param event_source_arn: ``AWS::Lambda::EventSourceMapping.EventSourceArn``.
        :param function_name: ``AWS::Lambda::EventSourceMapping.FunctionName``.
        :param batch_size: ``AWS::Lambda::EventSourceMapping.BatchSize``.
        :param bisect_batch_on_function_error: ``AWS::Lambda::EventSourceMapping.BisectBatchOnFunctionError``.
        :param destination_config: ``AWS::Lambda::EventSourceMapping.DestinationConfig``.
        :param enabled: ``AWS::Lambda::EventSourceMapping.Enabled``.
        :param maximum_batching_window_in_seconds: ``AWS::Lambda::EventSourceMapping.MaximumBatchingWindowInSeconds``.
        :param maximum_record_age_in_seconds: ``AWS::Lambda::EventSourceMapping.MaximumRecordAgeInSeconds``.
        :param maximum_retry_attempts: ``AWS::Lambda::EventSourceMapping.MaximumRetryAttempts``.
        :param parallelization_factor: ``AWS::Lambda::EventSourceMapping.ParallelizationFactor``.
        :param starting_position: ``AWS::Lambda::EventSourceMapping.StartingPosition``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html
        """
        self._values = {
            'event_source_arn': event_source_arn,
            'function_name': function_name,
        }
        if batch_size is not None: self._values["batch_size"] = batch_size
        if bisect_batch_on_function_error is not None: self._values["bisect_batch_on_function_error"] = bisect_batch_on_function_error
        if destination_config is not None: self._values["destination_config"] = destination_config
        if enabled is not None: self._values["enabled"] = enabled
        if maximum_batching_window_in_seconds is not None: self._values["maximum_batching_window_in_seconds"] = maximum_batching_window_in_seconds
        if maximum_record_age_in_seconds is not None: self._values["maximum_record_age_in_seconds"] = maximum_record_age_in_seconds
        if maximum_retry_attempts is not None: self._values["maximum_retry_attempts"] = maximum_retry_attempts
        if parallelization_factor is not None: self._values["parallelization_factor"] = parallelization_factor
        if starting_position is not None: self._values["starting_position"] = starting_position

    @builtins.property
    def event_source_arn(self) -> str:
        """``AWS::Lambda::EventSourceMapping.EventSourceArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-eventsourcearn
        """
        return self._values.get('event_source_arn')

    @builtins.property
    def function_name(self) -> str:
        """``AWS::Lambda::EventSourceMapping.FunctionName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-functionname
        """
        return self._values.get('function_name')

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        """``AWS::Lambda::EventSourceMapping.BatchSize``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-batchsize
        """
        return self._values.get('batch_size')

    @builtins.property
    def bisect_batch_on_function_error(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::Lambda::EventSourceMapping.BisectBatchOnFunctionError``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-bisectbatchonfunctionerror
        """
        return self._values.get('bisect_batch_on_function_error')

    @builtins.property
    def destination_config(self) -> typing.Optional[typing.Union["CfnEventSourceMapping.DestinationConfigProperty", _IResolvable_9ceae33e]]:
        """``AWS::Lambda::EventSourceMapping.DestinationConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-destinationconfig
        """
        return self._values.get('destination_config')

    @builtins.property
    def enabled(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::Lambda::EventSourceMapping.Enabled``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-enabled
        """
        return self._values.get('enabled')

    @builtins.property
    def maximum_batching_window_in_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::Lambda::EventSourceMapping.MaximumBatchingWindowInSeconds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-maximumbatchingwindowinseconds
        """
        return self._values.get('maximum_batching_window_in_seconds')

    @builtins.property
    def maximum_record_age_in_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::Lambda::EventSourceMapping.MaximumRecordAgeInSeconds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-maximumrecordageinseconds
        """
        return self._values.get('maximum_record_age_in_seconds')

    @builtins.property
    def maximum_retry_attempts(self) -> typing.Optional[jsii.Number]:
        """``AWS::Lambda::EventSourceMapping.MaximumRetryAttempts``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-maximumretryattempts
        """
        return self._values.get('maximum_retry_attempts')

    @builtins.property
    def parallelization_factor(self) -> typing.Optional[jsii.Number]:
        """``AWS::Lambda::EventSourceMapping.ParallelizationFactor``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-parallelizationfactor
        """
        return self._values.get('parallelization_factor')

    @builtins.property
    def starting_position(self) -> typing.Optional[str]:
        """``AWS::Lambda::EventSourceMapping.StartingPosition``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html#cfn-lambda-eventsourcemapping-startingposition
        """
        return self._values.get('starting_position')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnEventSourceMappingProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnFunction(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_lambda.CfnFunction"):
    """A CloudFormation ``AWS::Lambda::Function``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html
    cloudformationResource:
    :cloudformationResource:: AWS::Lambda::Function
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, code: typing.Union["CodeProperty", _IResolvable_9ceae33e], handler: str, role: str, runtime: str, dead_letter_config: typing.Optional[typing.Union["DeadLetterConfigProperty", _IResolvable_9ceae33e]]=None, description: typing.Optional[str]=None, environment: typing.Optional[typing.Union["EnvironmentProperty", _IResolvable_9ceae33e]]=None, function_name: typing.Optional[str]=None, kms_key_arn: typing.Optional[str]=None, layers: typing.Optional[typing.List[str]]=None, memory_size: typing.Optional[jsii.Number]=None, reserved_concurrent_executions: typing.Optional[jsii.Number]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None, timeout: typing.Optional[jsii.Number]=None, tracing_config: typing.Optional[typing.Union["TracingConfigProperty", _IResolvable_9ceae33e]]=None, vpc_config: typing.Optional[typing.Union["VpcConfigProperty", _IResolvable_9ceae33e]]=None) -> None:
        """Create a new ``AWS::Lambda::Function``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param code: ``AWS::Lambda::Function.Code``.
        :param handler: ``AWS::Lambda::Function.Handler``.
        :param role: ``AWS::Lambda::Function.Role``.
        :param runtime: ``AWS::Lambda::Function.Runtime``.
        :param dead_letter_config: ``AWS::Lambda::Function.DeadLetterConfig``.
        :param description: ``AWS::Lambda::Function.Description``.
        :param environment: ``AWS::Lambda::Function.Environment``.
        :param function_name: ``AWS::Lambda::Function.FunctionName``.
        :param kms_key_arn: ``AWS::Lambda::Function.KmsKeyArn``.
        :param layers: ``AWS::Lambda::Function.Layers``.
        :param memory_size: ``AWS::Lambda::Function.MemorySize``.
        :param reserved_concurrent_executions: ``AWS::Lambda::Function.ReservedConcurrentExecutions``.
        :param tags: ``AWS::Lambda::Function.Tags``.
        :param timeout: ``AWS::Lambda::Function.Timeout``.
        :param tracing_config: ``AWS::Lambda::Function.TracingConfig``.
        :param vpc_config: ``AWS::Lambda::Function.VpcConfig``.
        """
        props = CfnFunctionProps(code=code, handler=handler, role=role, runtime=runtime, dead_letter_config=dead_letter_config, description=description, environment=environment, function_name=function_name, kms_key_arn=kms_key_arn, layers=layers, memory_size=memory_size, reserved_concurrent_executions=reserved_concurrent_executions, tags=tags, timeout=timeout, tracing_config=tracing_config, vpc_config=vpc_config)

        jsii.create(CfnFunction, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnFunction":
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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::Lambda::Function.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="code")
    def code(self) -> typing.Union["CodeProperty", _IResolvable_9ceae33e]:
        """``AWS::Lambda::Function.Code``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-code
        """
        return jsii.get(self, "code")

    @code.setter
    def code(self, value: typing.Union["CodeProperty", _IResolvable_9ceae33e]) -> None:
        jsii.set(self, "code", value)

    @builtins.property
    @jsii.member(jsii_name="handler")
    def handler(self) -> str:
        """``AWS::Lambda::Function.Handler``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-handler
        """
        return jsii.get(self, "handler")

    @handler.setter
    def handler(self, value: str) -> None:
        jsii.set(self, "handler", value)

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> str:
        """``AWS::Lambda::Function.Role``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-role
        """
        return jsii.get(self, "role")

    @role.setter
    def role(self, value: str) -> None:
        jsii.set(self, "role", value)

    @builtins.property
    @jsii.member(jsii_name="runtime")
    def runtime(self) -> str:
        """``AWS::Lambda::Function.Runtime``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-runtime
        """
        return jsii.get(self, "runtime")

    @runtime.setter
    def runtime(self, value: str) -> None:
        jsii.set(self, "runtime", value)

    @builtins.property
    @jsii.member(jsii_name="deadLetterConfig")
    def dead_letter_config(self) -> typing.Optional[typing.Union["DeadLetterConfigProperty", _IResolvable_9ceae33e]]:
        """``AWS::Lambda::Function.DeadLetterConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-deadletterconfig
        """
        return jsii.get(self, "deadLetterConfig")

    @dead_letter_config.setter
    def dead_letter_config(self, value: typing.Optional[typing.Union["DeadLetterConfigProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "deadLetterConfig", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::Lambda::Function.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(self) -> typing.Optional[typing.Union["EnvironmentProperty", _IResolvable_9ceae33e]]:
        """``AWS::Lambda::Function.Environment``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-environment
        """
        return jsii.get(self, "environment")

    @environment.setter
    def environment(self, value: typing.Optional[typing.Union["EnvironmentProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "environment", value)

    @builtins.property
    @jsii.member(jsii_name="functionName")
    def function_name(self) -> typing.Optional[str]:
        """``AWS::Lambda::Function.FunctionName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-functionname
        """
        return jsii.get(self, "functionName")

    @function_name.setter
    def function_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "functionName", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArn")
    def kms_key_arn(self) -> typing.Optional[str]:
        """``AWS::Lambda::Function.KmsKeyArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-kmskeyarn
        """
        return jsii.get(self, "kmsKeyArn")

    @kms_key_arn.setter
    def kms_key_arn(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "kmsKeyArn", value)

    @builtins.property
    @jsii.member(jsii_name="layers")
    def layers(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Lambda::Function.Layers``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-layers
        """
        return jsii.get(self, "layers")

    @layers.setter
    def layers(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "layers", value)

    @builtins.property
    @jsii.member(jsii_name="memorySize")
    def memory_size(self) -> typing.Optional[jsii.Number]:
        """``AWS::Lambda::Function.MemorySize``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-memorysize
        """
        return jsii.get(self, "memorySize")

    @memory_size.setter
    def memory_size(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "memorySize", value)

    @builtins.property
    @jsii.member(jsii_name="reservedConcurrentExecutions")
    def reserved_concurrent_executions(self) -> typing.Optional[jsii.Number]:
        """``AWS::Lambda::Function.ReservedConcurrentExecutions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-reservedconcurrentexecutions
        """
        return jsii.get(self, "reservedConcurrentExecutions")

    @reserved_concurrent_executions.setter
    def reserved_concurrent_executions(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "reservedConcurrentExecutions", value)

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> typing.Optional[jsii.Number]:
        """``AWS::Lambda::Function.Timeout``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-timeout
        """
        return jsii.get(self, "timeout")

    @timeout.setter
    def timeout(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "timeout", value)

    @builtins.property
    @jsii.member(jsii_name="tracingConfig")
    def tracing_config(self) -> typing.Optional[typing.Union["TracingConfigProperty", _IResolvable_9ceae33e]]:
        """``AWS::Lambda::Function.TracingConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-tracingconfig
        """
        return jsii.get(self, "tracingConfig")

    @tracing_config.setter
    def tracing_config(self, value: typing.Optional[typing.Union["TracingConfigProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "tracingConfig", value)

    @builtins.property
    @jsii.member(jsii_name="vpcConfig")
    def vpc_config(self) -> typing.Optional[typing.Union["VpcConfigProperty", _IResolvable_9ceae33e]]:
        """``AWS::Lambda::Function.VpcConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-vpcconfig
        """
        return jsii.get(self, "vpcConfig")

    @vpc_config.setter
    def vpc_config(self, value: typing.Optional[typing.Union["VpcConfigProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "vpcConfig", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.CfnFunction.CodeProperty", jsii_struct_bases=[], name_mapping={'s3_bucket': 's3Bucket', 's3_key': 's3Key', 's3_object_version': 's3ObjectVersion', 'zip_file': 'zipFile'})
    class CodeProperty():
        def __init__(self, *, s3_bucket: typing.Optional[str]=None, s3_key: typing.Optional[str]=None, s3_object_version: typing.Optional[str]=None, zip_file: typing.Optional[str]=None) -> None:
            """
            :param s3_bucket: ``CfnFunction.CodeProperty.S3Bucket``.
            :param s3_key: ``CfnFunction.CodeProperty.S3Key``.
            :param s3_object_version: ``CfnFunction.CodeProperty.S3ObjectVersion``.
            :param zip_file: ``CfnFunction.CodeProperty.ZipFile``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-code.html
            """
            self._values = {
            }
            if s3_bucket is not None: self._values["s3_bucket"] = s3_bucket
            if s3_key is not None: self._values["s3_key"] = s3_key
            if s3_object_version is not None: self._values["s3_object_version"] = s3_object_version
            if zip_file is not None: self._values["zip_file"] = zip_file

        @builtins.property
        def s3_bucket(self) -> typing.Optional[str]:
            """``CfnFunction.CodeProperty.S3Bucket``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-code.html#cfn-lambda-function-code-s3bucket
            """
            return self._values.get('s3_bucket')

        @builtins.property
        def s3_key(self) -> typing.Optional[str]:
            """``CfnFunction.CodeProperty.S3Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-code.html#cfn-lambda-function-code-s3key
            """
            return self._values.get('s3_key')

        @builtins.property
        def s3_object_version(self) -> typing.Optional[str]:
            """``CfnFunction.CodeProperty.S3ObjectVersion``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-code.html#cfn-lambda-function-code-s3objectversion
            """
            return self._values.get('s3_object_version')

        @builtins.property
        def zip_file(self) -> typing.Optional[str]:
            """``CfnFunction.CodeProperty.ZipFile``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-code.html#cfn-lambda-function-code-zipfile
            """
            return self._values.get('zip_file')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'CodeProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.CfnFunction.DeadLetterConfigProperty", jsii_struct_bases=[], name_mapping={'target_arn': 'targetArn'})
    class DeadLetterConfigProperty():
        def __init__(self, *, target_arn: typing.Optional[str]=None) -> None:
            """
            :param target_arn: ``CfnFunction.DeadLetterConfigProperty.TargetArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-deadletterconfig.html
            """
            self._values = {
            }
            if target_arn is not None: self._values["target_arn"] = target_arn

        @builtins.property
        def target_arn(self) -> typing.Optional[str]:
            """``CfnFunction.DeadLetterConfigProperty.TargetArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-deadletterconfig.html#cfn-lambda-function-deadletterconfig-targetarn
            """
            return self._values.get('target_arn')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'DeadLetterConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.CfnFunction.EnvironmentProperty", jsii_struct_bases=[], name_mapping={'variables': 'variables'})
    class EnvironmentProperty():
        def __init__(self, *, variables: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.Mapping[str, str]]]=None) -> None:
            """
            :param variables: ``CfnFunction.EnvironmentProperty.Variables``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-environment.html
            """
            self._values = {
            }
            if variables is not None: self._values["variables"] = variables

        @builtins.property
        def variables(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.Mapping[str, str]]]:
            """``CfnFunction.EnvironmentProperty.Variables``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-environment.html#cfn-lambda-function-environment-variables
            """
            return self._values.get('variables')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'EnvironmentProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.CfnFunction.TracingConfigProperty", jsii_struct_bases=[], name_mapping={'mode': 'mode'})
    class TracingConfigProperty():
        def __init__(self, *, mode: typing.Optional[str]=None) -> None:
            """
            :param mode: ``CfnFunction.TracingConfigProperty.Mode``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-tracingconfig.html
            """
            self._values = {
            }
            if mode is not None: self._values["mode"] = mode

        @builtins.property
        def mode(self) -> typing.Optional[str]:
            """``CfnFunction.TracingConfigProperty.Mode``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-tracingconfig.html#cfn-lambda-function-tracingconfig-mode
            """
            return self._values.get('mode')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'TracingConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.CfnFunction.VpcConfigProperty", jsii_struct_bases=[], name_mapping={'security_group_ids': 'securityGroupIds', 'subnet_ids': 'subnetIds'})
    class VpcConfigProperty():
        def __init__(self, *, security_group_ids: typing.List[str], subnet_ids: typing.List[str]) -> None:
            """
            :param security_group_ids: ``CfnFunction.VpcConfigProperty.SecurityGroupIds``.
            :param subnet_ids: ``CfnFunction.VpcConfigProperty.SubnetIds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-vpcconfig.html
            """
            self._values = {
                'security_group_ids': security_group_ids,
                'subnet_ids': subnet_ids,
            }

        @builtins.property
        def security_group_ids(self) -> typing.List[str]:
            """``CfnFunction.VpcConfigProperty.SecurityGroupIds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-vpcconfig.html#cfn-lambda-function-vpcconfig-securitygroupids
            """
            return self._values.get('security_group_ids')

        @builtins.property
        def subnet_ids(self) -> typing.List[str]:
            """``CfnFunction.VpcConfigProperty.SubnetIds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-function-vpcconfig.html#cfn-lambda-function-vpcconfig-subnetids
            """
            return self._values.get('subnet_ids')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'VpcConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.CfnFunctionProps", jsii_struct_bases=[], name_mapping={'code': 'code', 'handler': 'handler', 'role': 'role', 'runtime': 'runtime', 'dead_letter_config': 'deadLetterConfig', 'description': 'description', 'environment': 'environment', 'function_name': 'functionName', 'kms_key_arn': 'kmsKeyArn', 'layers': 'layers', 'memory_size': 'memorySize', 'reserved_concurrent_executions': 'reservedConcurrentExecutions', 'tags': 'tags', 'timeout': 'timeout', 'tracing_config': 'tracingConfig', 'vpc_config': 'vpcConfig'})
class CfnFunctionProps():
    def __init__(self, *, code: typing.Union["CfnFunction.CodeProperty", _IResolvable_9ceae33e], handler: str, role: str, runtime: str, dead_letter_config: typing.Optional[typing.Union["CfnFunction.DeadLetterConfigProperty", _IResolvable_9ceae33e]]=None, description: typing.Optional[str]=None, environment: typing.Optional[typing.Union["CfnFunction.EnvironmentProperty", _IResolvable_9ceae33e]]=None, function_name: typing.Optional[str]=None, kms_key_arn: typing.Optional[str]=None, layers: typing.Optional[typing.List[str]]=None, memory_size: typing.Optional[jsii.Number]=None, reserved_concurrent_executions: typing.Optional[jsii.Number]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None, timeout: typing.Optional[jsii.Number]=None, tracing_config: typing.Optional[typing.Union["CfnFunction.TracingConfigProperty", _IResolvable_9ceae33e]]=None, vpc_config: typing.Optional[typing.Union["CfnFunction.VpcConfigProperty", _IResolvable_9ceae33e]]=None) -> None:
        """Properties for defining a ``AWS::Lambda::Function``.

        :param code: ``AWS::Lambda::Function.Code``.
        :param handler: ``AWS::Lambda::Function.Handler``.
        :param role: ``AWS::Lambda::Function.Role``.
        :param runtime: ``AWS::Lambda::Function.Runtime``.
        :param dead_letter_config: ``AWS::Lambda::Function.DeadLetterConfig``.
        :param description: ``AWS::Lambda::Function.Description``.
        :param environment: ``AWS::Lambda::Function.Environment``.
        :param function_name: ``AWS::Lambda::Function.FunctionName``.
        :param kms_key_arn: ``AWS::Lambda::Function.KmsKeyArn``.
        :param layers: ``AWS::Lambda::Function.Layers``.
        :param memory_size: ``AWS::Lambda::Function.MemorySize``.
        :param reserved_concurrent_executions: ``AWS::Lambda::Function.ReservedConcurrentExecutions``.
        :param tags: ``AWS::Lambda::Function.Tags``.
        :param timeout: ``AWS::Lambda::Function.Timeout``.
        :param tracing_config: ``AWS::Lambda::Function.TracingConfig``.
        :param vpc_config: ``AWS::Lambda::Function.VpcConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html
        """
        self._values = {
            'code': code,
            'handler': handler,
            'role': role,
            'runtime': runtime,
        }
        if dead_letter_config is not None: self._values["dead_letter_config"] = dead_letter_config
        if description is not None: self._values["description"] = description
        if environment is not None: self._values["environment"] = environment
        if function_name is not None: self._values["function_name"] = function_name
        if kms_key_arn is not None: self._values["kms_key_arn"] = kms_key_arn
        if layers is not None: self._values["layers"] = layers
        if memory_size is not None: self._values["memory_size"] = memory_size
        if reserved_concurrent_executions is not None: self._values["reserved_concurrent_executions"] = reserved_concurrent_executions
        if tags is not None: self._values["tags"] = tags
        if timeout is not None: self._values["timeout"] = timeout
        if tracing_config is not None: self._values["tracing_config"] = tracing_config
        if vpc_config is not None: self._values["vpc_config"] = vpc_config

    @builtins.property
    def code(self) -> typing.Union["CfnFunction.CodeProperty", _IResolvable_9ceae33e]:
        """``AWS::Lambda::Function.Code``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-code
        """
        return self._values.get('code')

    @builtins.property
    def handler(self) -> str:
        """``AWS::Lambda::Function.Handler``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-handler
        """
        return self._values.get('handler')

    @builtins.property
    def role(self) -> str:
        """``AWS::Lambda::Function.Role``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-role
        """
        return self._values.get('role')

    @builtins.property
    def runtime(self) -> str:
        """``AWS::Lambda::Function.Runtime``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-runtime
        """
        return self._values.get('runtime')

    @builtins.property
    def dead_letter_config(self) -> typing.Optional[typing.Union["CfnFunction.DeadLetterConfigProperty", _IResolvable_9ceae33e]]:
        """``AWS::Lambda::Function.DeadLetterConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-deadletterconfig
        """
        return self._values.get('dead_letter_config')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::Lambda::Function.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-description
        """
        return self._values.get('description')

    @builtins.property
    def environment(self) -> typing.Optional[typing.Union["CfnFunction.EnvironmentProperty", _IResolvable_9ceae33e]]:
        """``AWS::Lambda::Function.Environment``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-environment
        """
        return self._values.get('environment')

    @builtins.property
    def function_name(self) -> typing.Optional[str]:
        """``AWS::Lambda::Function.FunctionName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-functionname
        """
        return self._values.get('function_name')

    @builtins.property
    def kms_key_arn(self) -> typing.Optional[str]:
        """``AWS::Lambda::Function.KmsKeyArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-kmskeyarn
        """
        return self._values.get('kms_key_arn')

    @builtins.property
    def layers(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Lambda::Function.Layers``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-layers
        """
        return self._values.get('layers')

    @builtins.property
    def memory_size(self) -> typing.Optional[jsii.Number]:
        """``AWS::Lambda::Function.MemorySize``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-memorysize
        """
        return self._values.get('memory_size')

    @builtins.property
    def reserved_concurrent_executions(self) -> typing.Optional[jsii.Number]:
        """``AWS::Lambda::Function.ReservedConcurrentExecutions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-reservedconcurrentexecutions
        """
        return self._values.get('reserved_concurrent_executions')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_b4661f1a]]:
        """``AWS::Lambda::Function.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-tags
        """
        return self._values.get('tags')

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        """``AWS::Lambda::Function.Timeout``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-timeout
        """
        return self._values.get('timeout')

    @builtins.property
    def tracing_config(self) -> typing.Optional[typing.Union["CfnFunction.TracingConfigProperty", _IResolvable_9ceae33e]]:
        """``AWS::Lambda::Function.TracingConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-tracingconfig
        """
        return self._values.get('tracing_config')

    @builtins.property
    def vpc_config(self) -> typing.Optional[typing.Union["CfnFunction.VpcConfigProperty", _IResolvable_9ceae33e]]:
        """``AWS::Lambda::Function.VpcConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-function.html#cfn-lambda-function-vpcconfig
        """
        return self._values.get('vpc_config')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnFunctionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnLayerVersion(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_lambda.CfnLayerVersion"):
    """A CloudFormation ``AWS::Lambda::LayerVersion``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-layerversion.html
    cloudformationResource:
    :cloudformationResource:: AWS::Lambda::LayerVersion
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, content: typing.Union["ContentProperty", _IResolvable_9ceae33e], compatible_runtimes: typing.Optional[typing.List[str]]=None, description: typing.Optional[str]=None, layer_name: typing.Optional[str]=None, license_info: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::Lambda::LayerVersion``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param content: ``AWS::Lambda::LayerVersion.Content``.
        :param compatible_runtimes: ``AWS::Lambda::LayerVersion.CompatibleRuntimes``.
        :param description: ``AWS::Lambda::LayerVersion.Description``.
        :param layer_name: ``AWS::Lambda::LayerVersion.LayerName``.
        :param license_info: ``AWS::Lambda::LayerVersion.LicenseInfo``.
        """
        props = CfnLayerVersionProps(content=content, compatible_runtimes=compatible_runtimes, description=description, layer_name=layer_name, license_info=license_info)

        jsii.create(CfnLayerVersion, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnLayerVersion":
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
    @jsii.member(jsii_name="content")
    def content(self) -> typing.Union["ContentProperty", _IResolvable_9ceae33e]:
        """``AWS::Lambda::LayerVersion.Content``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-layerversion.html#cfn-lambda-layerversion-content
        """
        return jsii.get(self, "content")

    @content.setter
    def content(self, value: typing.Union["ContentProperty", _IResolvable_9ceae33e]) -> None:
        jsii.set(self, "content", value)

    @builtins.property
    @jsii.member(jsii_name="compatibleRuntimes")
    def compatible_runtimes(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Lambda::LayerVersion.CompatibleRuntimes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-layerversion.html#cfn-lambda-layerversion-compatibleruntimes
        """
        return jsii.get(self, "compatibleRuntimes")

    @compatible_runtimes.setter
    def compatible_runtimes(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "compatibleRuntimes", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::Lambda::LayerVersion.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-layerversion.html#cfn-lambda-layerversion-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="layerName")
    def layer_name(self) -> typing.Optional[str]:
        """``AWS::Lambda::LayerVersion.LayerName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-layerversion.html#cfn-lambda-layerversion-layername
        """
        return jsii.get(self, "layerName")

    @layer_name.setter
    def layer_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "layerName", value)

    @builtins.property
    @jsii.member(jsii_name="licenseInfo")
    def license_info(self) -> typing.Optional[str]:
        """``AWS::Lambda::LayerVersion.LicenseInfo``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-layerversion.html#cfn-lambda-layerversion-licenseinfo
        """
        return jsii.get(self, "licenseInfo")

    @license_info.setter
    def license_info(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "licenseInfo", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.CfnLayerVersion.ContentProperty", jsii_struct_bases=[], name_mapping={'s3_bucket': 's3Bucket', 's3_key': 's3Key', 's3_object_version': 's3ObjectVersion'})
    class ContentProperty():
        def __init__(self, *, s3_bucket: str, s3_key: str, s3_object_version: typing.Optional[str]=None) -> None:
            """
            :param s3_bucket: ``CfnLayerVersion.ContentProperty.S3Bucket``.
            :param s3_key: ``CfnLayerVersion.ContentProperty.S3Key``.
            :param s3_object_version: ``CfnLayerVersion.ContentProperty.S3ObjectVersion``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-layerversion-content.html
            """
            self._values = {
                's3_bucket': s3_bucket,
                's3_key': s3_key,
            }
            if s3_object_version is not None: self._values["s3_object_version"] = s3_object_version

        @builtins.property
        def s3_bucket(self) -> str:
            """``CfnLayerVersion.ContentProperty.S3Bucket``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-layerversion-content.html#cfn-lambda-layerversion-content-s3bucket
            """
            return self._values.get('s3_bucket')

        @builtins.property
        def s3_key(self) -> str:
            """``CfnLayerVersion.ContentProperty.S3Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-layerversion-content.html#cfn-lambda-layerversion-content-s3key
            """
            return self._values.get('s3_key')

        @builtins.property
        def s3_object_version(self) -> typing.Optional[str]:
            """``CfnLayerVersion.ContentProperty.S3ObjectVersion``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-layerversion-content.html#cfn-lambda-layerversion-content-s3objectversion
            """
            return self._values.get('s3_object_version')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ContentProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.implements(_IInspectable_051e6ed8)
class CfnLayerVersionPermission(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_lambda.CfnLayerVersionPermission"):
    """A CloudFormation ``AWS::Lambda::LayerVersionPermission``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-layerversionpermission.html
    cloudformationResource:
    :cloudformationResource:: AWS::Lambda::LayerVersionPermission
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, action: str, layer_version_arn: str, principal: str, organization_id: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::Lambda::LayerVersionPermission``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param action: ``AWS::Lambda::LayerVersionPermission.Action``.
        :param layer_version_arn: ``AWS::Lambda::LayerVersionPermission.LayerVersionArn``.
        :param principal: ``AWS::Lambda::LayerVersionPermission.Principal``.
        :param organization_id: ``AWS::Lambda::LayerVersionPermission.OrganizationId``.
        """
        props = CfnLayerVersionPermissionProps(action=action, layer_version_arn=layer_version_arn, principal=principal, organization_id=organization_id)

        jsii.create(CfnLayerVersionPermission, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnLayerVersionPermission":
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
    @jsii.member(jsii_name="action")
    def action(self) -> str:
        """``AWS::Lambda::LayerVersionPermission.Action``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-layerversionpermission.html#cfn-lambda-layerversionpermission-action
        """
        return jsii.get(self, "action")

    @action.setter
    def action(self, value: str) -> None:
        jsii.set(self, "action", value)

    @builtins.property
    @jsii.member(jsii_name="layerVersionArn")
    def layer_version_arn(self) -> str:
        """``AWS::Lambda::LayerVersionPermission.LayerVersionArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-layerversionpermission.html#cfn-lambda-layerversionpermission-layerversionarn
        """
        return jsii.get(self, "layerVersionArn")

    @layer_version_arn.setter
    def layer_version_arn(self, value: str) -> None:
        jsii.set(self, "layerVersionArn", value)

    @builtins.property
    @jsii.member(jsii_name="principal")
    def principal(self) -> str:
        """``AWS::Lambda::LayerVersionPermission.Principal``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-layerversionpermission.html#cfn-lambda-layerversionpermission-principal
        """
        return jsii.get(self, "principal")

    @principal.setter
    def principal(self, value: str) -> None:
        jsii.set(self, "principal", value)

    @builtins.property
    @jsii.member(jsii_name="organizationId")
    def organization_id(self) -> typing.Optional[str]:
        """``AWS::Lambda::LayerVersionPermission.OrganizationId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-layerversionpermission.html#cfn-lambda-layerversionpermission-organizationid
        """
        return jsii.get(self, "organizationId")

    @organization_id.setter
    def organization_id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "organizationId", value)


@jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.CfnLayerVersionPermissionProps", jsii_struct_bases=[], name_mapping={'action': 'action', 'layer_version_arn': 'layerVersionArn', 'principal': 'principal', 'organization_id': 'organizationId'})
class CfnLayerVersionPermissionProps():
    def __init__(self, *, action: str, layer_version_arn: str, principal: str, organization_id: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::Lambda::LayerVersionPermission``.

        :param action: ``AWS::Lambda::LayerVersionPermission.Action``.
        :param layer_version_arn: ``AWS::Lambda::LayerVersionPermission.LayerVersionArn``.
        :param principal: ``AWS::Lambda::LayerVersionPermission.Principal``.
        :param organization_id: ``AWS::Lambda::LayerVersionPermission.OrganizationId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-layerversionpermission.html
        """
        self._values = {
            'action': action,
            'layer_version_arn': layer_version_arn,
            'principal': principal,
        }
        if organization_id is not None: self._values["organization_id"] = organization_id

    @builtins.property
    def action(self) -> str:
        """``AWS::Lambda::LayerVersionPermission.Action``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-layerversionpermission.html#cfn-lambda-layerversionpermission-action
        """
        return self._values.get('action')

    @builtins.property
    def layer_version_arn(self) -> str:
        """``AWS::Lambda::LayerVersionPermission.LayerVersionArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-layerversionpermission.html#cfn-lambda-layerversionpermission-layerversionarn
        """
        return self._values.get('layer_version_arn')

    @builtins.property
    def principal(self) -> str:
        """``AWS::Lambda::LayerVersionPermission.Principal``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-layerversionpermission.html#cfn-lambda-layerversionpermission-principal
        """
        return self._values.get('principal')

    @builtins.property
    def organization_id(self) -> typing.Optional[str]:
        """``AWS::Lambda::LayerVersionPermission.OrganizationId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-layerversionpermission.html#cfn-lambda-layerversionpermission-organizationid
        """
        return self._values.get('organization_id')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnLayerVersionPermissionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.CfnLayerVersionProps", jsii_struct_bases=[], name_mapping={'content': 'content', 'compatible_runtimes': 'compatibleRuntimes', 'description': 'description', 'layer_name': 'layerName', 'license_info': 'licenseInfo'})
class CfnLayerVersionProps():
    def __init__(self, *, content: typing.Union["CfnLayerVersion.ContentProperty", _IResolvable_9ceae33e], compatible_runtimes: typing.Optional[typing.List[str]]=None, description: typing.Optional[str]=None, layer_name: typing.Optional[str]=None, license_info: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::Lambda::LayerVersion``.

        :param content: ``AWS::Lambda::LayerVersion.Content``.
        :param compatible_runtimes: ``AWS::Lambda::LayerVersion.CompatibleRuntimes``.
        :param description: ``AWS::Lambda::LayerVersion.Description``.
        :param layer_name: ``AWS::Lambda::LayerVersion.LayerName``.
        :param license_info: ``AWS::Lambda::LayerVersion.LicenseInfo``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-layerversion.html
        """
        self._values = {
            'content': content,
        }
        if compatible_runtimes is not None: self._values["compatible_runtimes"] = compatible_runtimes
        if description is not None: self._values["description"] = description
        if layer_name is not None: self._values["layer_name"] = layer_name
        if license_info is not None: self._values["license_info"] = license_info

    @builtins.property
    def content(self) -> typing.Union["CfnLayerVersion.ContentProperty", _IResolvable_9ceae33e]:
        """``AWS::Lambda::LayerVersion.Content``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-layerversion.html#cfn-lambda-layerversion-content
        """
        return self._values.get('content')

    @builtins.property
    def compatible_runtimes(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Lambda::LayerVersion.CompatibleRuntimes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-layerversion.html#cfn-lambda-layerversion-compatibleruntimes
        """
        return self._values.get('compatible_runtimes')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::Lambda::LayerVersion.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-layerversion.html#cfn-lambda-layerversion-description
        """
        return self._values.get('description')

    @builtins.property
    def layer_name(self) -> typing.Optional[str]:
        """``AWS::Lambda::LayerVersion.LayerName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-layerversion.html#cfn-lambda-layerversion-layername
        """
        return self._values.get('layer_name')

    @builtins.property
    def license_info(self) -> typing.Optional[str]:
        """``AWS::Lambda::LayerVersion.LicenseInfo``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-layerversion.html#cfn-lambda-layerversion-licenseinfo
        """
        return self._values.get('license_info')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnLayerVersionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.CfnParametersCodeProps", jsii_struct_bases=[], name_mapping={'bucket_name_param': 'bucketNameParam', 'object_key_param': 'objectKeyParam'})
class CfnParametersCodeProps():
    def __init__(self, *, bucket_name_param: typing.Optional[_CfnParameter_90f1d0df]=None, object_key_param: typing.Optional[_CfnParameter_90f1d0df]=None) -> None:
        """Construction properties for {@link CfnParametersCode}.

        :param bucket_name_param: The CloudFormation parameter that represents the name of the S3 Bucket where the Lambda code will be located in. Must be of type 'String'. Default: a new parameter will be created
        :param object_key_param: The CloudFormation parameter that represents the path inside the S3 Bucket where the Lambda code will be located at. Must be of type 'String'. Default: a new parameter will be created

        stability
        :stability: experimental
        """
        self._values = {
        }
        if bucket_name_param is not None: self._values["bucket_name_param"] = bucket_name_param
        if object_key_param is not None: self._values["object_key_param"] = object_key_param

    @builtins.property
    def bucket_name_param(self) -> typing.Optional[_CfnParameter_90f1d0df]:
        """The CloudFormation parameter that represents the name of the S3 Bucket where the Lambda code will be located in.

        Must be of type 'String'.

        default
        :default: a new parameter will be created

        stability
        :stability: experimental
        """
        return self._values.get('bucket_name_param')

    @builtins.property
    def object_key_param(self) -> typing.Optional[_CfnParameter_90f1d0df]:
        """The CloudFormation parameter that represents the path inside the S3 Bucket where the Lambda code will be located at.

        Must be of type 'String'.

        default
        :default: a new parameter will be created

        stability
        :stability: experimental
        """
        return self._values.get('object_key_param')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnParametersCodeProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnPermission(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_lambda.CfnPermission"):
    """A CloudFormation ``AWS::Lambda::Permission``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-permission.html
    cloudformationResource:
    :cloudformationResource:: AWS::Lambda::Permission
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, action: str, function_name: str, principal: str, event_source_token: typing.Optional[str]=None, source_account: typing.Optional[str]=None, source_arn: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::Lambda::Permission``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param action: ``AWS::Lambda::Permission.Action``.
        :param function_name: ``AWS::Lambda::Permission.FunctionName``.
        :param principal: ``AWS::Lambda::Permission.Principal``.
        :param event_source_token: ``AWS::Lambda::Permission.EventSourceToken``.
        :param source_account: ``AWS::Lambda::Permission.SourceAccount``.
        :param source_arn: ``AWS::Lambda::Permission.SourceArn``.
        """
        props = CfnPermissionProps(action=action, function_name=function_name, principal=principal, event_source_token=event_source_token, source_account=source_account, source_arn=source_arn)

        jsii.create(CfnPermission, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnPermission":
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
    @jsii.member(jsii_name="action")
    def action(self) -> str:
        """``AWS::Lambda::Permission.Action``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-permission.html#cfn-lambda-permission-action
        """
        return jsii.get(self, "action")

    @action.setter
    def action(self, value: str) -> None:
        jsii.set(self, "action", value)

    @builtins.property
    @jsii.member(jsii_name="functionName")
    def function_name(self) -> str:
        """``AWS::Lambda::Permission.FunctionName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-permission.html#cfn-lambda-permission-functionname
        """
        return jsii.get(self, "functionName")

    @function_name.setter
    def function_name(self, value: str) -> None:
        jsii.set(self, "functionName", value)

    @builtins.property
    @jsii.member(jsii_name="principal")
    def principal(self) -> str:
        """``AWS::Lambda::Permission.Principal``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-permission.html#cfn-lambda-permission-principal
        """
        return jsii.get(self, "principal")

    @principal.setter
    def principal(self, value: str) -> None:
        jsii.set(self, "principal", value)

    @builtins.property
    @jsii.member(jsii_name="eventSourceToken")
    def event_source_token(self) -> typing.Optional[str]:
        """``AWS::Lambda::Permission.EventSourceToken``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-permission.html#cfn-lambda-permission-eventsourcetoken
        """
        return jsii.get(self, "eventSourceToken")

    @event_source_token.setter
    def event_source_token(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "eventSourceToken", value)

    @builtins.property
    @jsii.member(jsii_name="sourceAccount")
    def source_account(self) -> typing.Optional[str]:
        """``AWS::Lambda::Permission.SourceAccount``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-permission.html#cfn-lambda-permission-sourceaccount
        """
        return jsii.get(self, "sourceAccount")

    @source_account.setter
    def source_account(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "sourceAccount", value)

    @builtins.property
    @jsii.member(jsii_name="sourceArn")
    def source_arn(self) -> typing.Optional[str]:
        """``AWS::Lambda::Permission.SourceArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-permission.html#cfn-lambda-permission-sourcearn
        """
        return jsii.get(self, "sourceArn")

    @source_arn.setter
    def source_arn(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "sourceArn", value)


@jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.CfnPermissionProps", jsii_struct_bases=[], name_mapping={'action': 'action', 'function_name': 'functionName', 'principal': 'principal', 'event_source_token': 'eventSourceToken', 'source_account': 'sourceAccount', 'source_arn': 'sourceArn'})
class CfnPermissionProps():
    def __init__(self, *, action: str, function_name: str, principal: str, event_source_token: typing.Optional[str]=None, source_account: typing.Optional[str]=None, source_arn: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::Lambda::Permission``.

        :param action: ``AWS::Lambda::Permission.Action``.
        :param function_name: ``AWS::Lambda::Permission.FunctionName``.
        :param principal: ``AWS::Lambda::Permission.Principal``.
        :param event_source_token: ``AWS::Lambda::Permission.EventSourceToken``.
        :param source_account: ``AWS::Lambda::Permission.SourceAccount``.
        :param source_arn: ``AWS::Lambda::Permission.SourceArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-permission.html
        """
        self._values = {
            'action': action,
            'function_name': function_name,
            'principal': principal,
        }
        if event_source_token is not None: self._values["event_source_token"] = event_source_token
        if source_account is not None: self._values["source_account"] = source_account
        if source_arn is not None: self._values["source_arn"] = source_arn

    @builtins.property
    def action(self) -> str:
        """``AWS::Lambda::Permission.Action``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-permission.html#cfn-lambda-permission-action
        """
        return self._values.get('action')

    @builtins.property
    def function_name(self) -> str:
        """``AWS::Lambda::Permission.FunctionName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-permission.html#cfn-lambda-permission-functionname
        """
        return self._values.get('function_name')

    @builtins.property
    def principal(self) -> str:
        """``AWS::Lambda::Permission.Principal``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-permission.html#cfn-lambda-permission-principal
        """
        return self._values.get('principal')

    @builtins.property
    def event_source_token(self) -> typing.Optional[str]:
        """``AWS::Lambda::Permission.EventSourceToken``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-permission.html#cfn-lambda-permission-eventsourcetoken
        """
        return self._values.get('event_source_token')

    @builtins.property
    def source_account(self) -> typing.Optional[str]:
        """``AWS::Lambda::Permission.SourceAccount``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-permission.html#cfn-lambda-permission-sourceaccount
        """
        return self._values.get('source_account')

    @builtins.property
    def source_arn(self) -> typing.Optional[str]:
        """``AWS::Lambda::Permission.SourceArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-permission.html#cfn-lambda-permission-sourcearn
        """
        return self._values.get('source_arn')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnPermissionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnVersion(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_lambda.CfnVersion"):
    """A CloudFormation ``AWS::Lambda::Version``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-version.html
    cloudformationResource:
    :cloudformationResource:: AWS::Lambda::Version
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, function_name: str, code_sha256: typing.Optional[str]=None, description: typing.Optional[str]=None, provisioned_concurrency_config: typing.Optional[typing.Union["ProvisionedConcurrencyConfigurationProperty", _IResolvable_9ceae33e]]=None) -> None:
        """Create a new ``AWS::Lambda::Version``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param function_name: ``AWS::Lambda::Version.FunctionName``.
        :param code_sha256: ``AWS::Lambda::Version.CodeSha256``.
        :param description: ``AWS::Lambda::Version.Description``.
        :param provisioned_concurrency_config: ``AWS::Lambda::Version.ProvisionedConcurrencyConfig``.
        """
        props = CfnVersionProps(function_name=function_name, code_sha256=code_sha256, description=description, provisioned_concurrency_config=provisioned_concurrency_config)

        jsii.create(CfnVersion, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnVersion":
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
    @jsii.member(jsii_name="attrVersion")
    def attr_version(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Version
        """
        return jsii.get(self, "attrVersion")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="functionName")
    def function_name(self) -> str:
        """``AWS::Lambda::Version.FunctionName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-version.html#cfn-lambda-version-functionname
        """
        return jsii.get(self, "functionName")

    @function_name.setter
    def function_name(self, value: str) -> None:
        jsii.set(self, "functionName", value)

    @builtins.property
    @jsii.member(jsii_name="codeSha256")
    def code_sha256(self) -> typing.Optional[str]:
        """``AWS::Lambda::Version.CodeSha256``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-version.html#cfn-lambda-version-codesha256
        """
        return jsii.get(self, "codeSha256")

    @code_sha256.setter
    def code_sha256(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "codeSha256", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::Lambda::Version.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-version.html#cfn-lambda-version-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="provisionedConcurrencyConfig")
    def provisioned_concurrency_config(self) -> typing.Optional[typing.Union["ProvisionedConcurrencyConfigurationProperty", _IResolvable_9ceae33e]]:
        """``AWS::Lambda::Version.ProvisionedConcurrencyConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-version.html#cfn-lambda-version-provisionedconcurrencyconfig
        """
        return jsii.get(self, "provisionedConcurrencyConfig")

    @provisioned_concurrency_config.setter
    def provisioned_concurrency_config(self, value: typing.Optional[typing.Union["ProvisionedConcurrencyConfigurationProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "provisionedConcurrencyConfig", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.CfnVersion.ProvisionedConcurrencyConfigurationProperty", jsii_struct_bases=[], name_mapping={'provisioned_concurrent_executions': 'provisionedConcurrentExecutions'})
    class ProvisionedConcurrencyConfigurationProperty():
        def __init__(self, *, provisioned_concurrent_executions: jsii.Number) -> None:
            """
            :param provisioned_concurrent_executions: ``CfnVersion.ProvisionedConcurrencyConfigurationProperty.ProvisionedConcurrentExecutions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-version-provisionedconcurrencyconfiguration.html
            """
            self._values = {
                'provisioned_concurrent_executions': provisioned_concurrent_executions,
            }

        @builtins.property
        def provisioned_concurrent_executions(self) -> jsii.Number:
            """``CfnVersion.ProvisionedConcurrencyConfigurationProperty.ProvisionedConcurrentExecutions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lambda-version-provisionedconcurrencyconfiguration.html#cfn-lambda-version-provisionedconcurrencyconfiguration-provisionedconcurrentexecutions
            """
            return self._values.get('provisioned_concurrent_executions')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ProvisionedConcurrencyConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.CfnVersionProps", jsii_struct_bases=[], name_mapping={'function_name': 'functionName', 'code_sha256': 'codeSha256', 'description': 'description', 'provisioned_concurrency_config': 'provisionedConcurrencyConfig'})
class CfnVersionProps():
    def __init__(self, *, function_name: str, code_sha256: typing.Optional[str]=None, description: typing.Optional[str]=None, provisioned_concurrency_config: typing.Optional[typing.Union["CfnVersion.ProvisionedConcurrencyConfigurationProperty", _IResolvable_9ceae33e]]=None) -> None:
        """Properties for defining a ``AWS::Lambda::Version``.

        :param function_name: ``AWS::Lambda::Version.FunctionName``.
        :param code_sha256: ``AWS::Lambda::Version.CodeSha256``.
        :param description: ``AWS::Lambda::Version.Description``.
        :param provisioned_concurrency_config: ``AWS::Lambda::Version.ProvisionedConcurrencyConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-version.html
        """
        self._values = {
            'function_name': function_name,
        }
        if code_sha256 is not None: self._values["code_sha256"] = code_sha256
        if description is not None: self._values["description"] = description
        if provisioned_concurrency_config is not None: self._values["provisioned_concurrency_config"] = provisioned_concurrency_config

    @builtins.property
    def function_name(self) -> str:
        """``AWS::Lambda::Version.FunctionName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-version.html#cfn-lambda-version-functionname
        """
        return self._values.get('function_name')

    @builtins.property
    def code_sha256(self) -> typing.Optional[str]:
        """``AWS::Lambda::Version.CodeSha256``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-version.html#cfn-lambda-version-codesha256
        """
        return self._values.get('code_sha256')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::Lambda::Version.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-version.html#cfn-lambda-version-description
        """
        return self._values.get('description')

    @builtins.property
    def provisioned_concurrency_config(self) -> typing.Optional[typing.Union["CfnVersion.ProvisionedConcurrencyConfigurationProperty", _IResolvable_9ceae33e]]:
        """``AWS::Lambda::Version.ProvisionedConcurrencyConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-version.html#cfn-lambda-version-provisionedconcurrencyconfig
        """
        return self._values.get('provisioned_concurrency_config')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnVersionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class Code(metaclass=jsii.JSIIAbstractClass, jsii_type="monocdk-experiment.aws_lambda.Code"):
    """
    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _CodeProxy

    def __init__(self) -> None:
        jsii.create(Code, self, [])

    @jsii.member(jsii_name="asset")
    @builtins.classmethod
    def asset(cls, path: str) -> "AssetCode":
        """
        :param path: -

        deprecated
        :deprecated: use ``fromAsset``

        stability
        :stability: deprecated
        """
        return jsii.sinvoke(cls, "asset", [path])

    @jsii.member(jsii_name="bucket")
    @builtins.classmethod
    def bucket(cls, bucket: _IBucket_25bad983, key: str, object_version: typing.Optional[str]=None) -> "S3Code":
        """
        :param bucket: -
        :param key: -
        :param object_version: -

        deprecated
        :deprecated: use ``fromBucket``

        stability
        :stability: deprecated
        """
        return jsii.sinvoke(cls, "bucket", [bucket, key, object_version])

    @jsii.member(jsii_name="cfnParameters")
    @builtins.classmethod
    def cfn_parameters(cls, *, bucket_name_param: typing.Optional[_CfnParameter_90f1d0df]=None, object_key_param: typing.Optional[_CfnParameter_90f1d0df]=None) -> "CfnParametersCode":
        """
        :param bucket_name_param: The CloudFormation parameter that represents the name of the S3 Bucket where the Lambda code will be located in. Must be of type 'String'. Default: a new parameter will be created
        :param object_key_param: The CloudFormation parameter that represents the path inside the S3 Bucket where the Lambda code will be located at. Must be of type 'String'. Default: a new parameter will be created

        deprecated
        :deprecated: use ``fromCfnParameters``

        stability
        :stability: deprecated
        """
        props = CfnParametersCodeProps(bucket_name_param=bucket_name_param, object_key_param=object_key_param)

        return jsii.sinvoke(cls, "cfnParameters", [props])

    @jsii.member(jsii_name="fromAsset")
    @builtins.classmethod
    def from_asset(cls, path: str, *, readers: typing.Optional[typing.List[_IGrantable_0fcfc53a]]=None, source_hash: typing.Optional[str]=None, exclude: typing.Optional[typing.List[str]]=None, follow: typing.Optional[_FollowMode_f74e7125]=None, asset_hash: typing.Optional[str]=None, asset_hash_type: typing.Optional[_AssetHashType_16f7047a]=None, bundling: typing.Optional[_BundlingOptions_0cab5223]=None) -> "AssetCode":
        """Loads the function code from a local disk path.

        :param path: Either a directory with the Lambda code bundle or a .zip file.
        :param readers: A list of principals that should be able to read this asset from S3. You can use ``asset.grantRead(principal)`` to grant read permissions later. Default: - No principals that can read file asset.
        :param source_hash: Custom hash to use when identifying the specific version of the asset. For consistency, this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be the asset hash. NOTE: the source hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the source hash, you will need to make sure it is updated every time the source changes, or otherwise it is possible that some deployments will not be invalidated. Default: - automatically calculate source hash based on the contents of the source file or directory.
        :param exclude: Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: A strategy for how to handle symlinks. Default: Never
        :param asset_hash: Specify a custom hash for this asset. If ``assetHashType`` is set it must be set to ``AssetHashType.CUSTOM``. For consistency, this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be the asset hash. NOTE: the hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the hash, you will need to make sure it is updated every time the asset changes, or otherwise it is possible that some deployments will not be invalidated. Default: - based on ``assetHashType``
        :param asset_hash_type: Specifies the type of hash to calculate for this asset. If ``assetHash`` is configured, this option must be ``undefined`` or ``AssetHashType.CUSTOM``. Default: - the default is ``AssetHashType.SOURCE``, but if ``assetHash`` is explicitly specified this value defaults to ``AssetHashType.CUSTOM``.
        :param bundling: Bundle the asset by executing a command in a Docker container. The asset path will be mounted at ``/asset-input``. The Docker container is responsible for putting content at ``/asset-output``. The content at ``/asset-output`` will be zipped and used as the final asset. Default: - uploaded as-is to S3 if the asset is a regular file or a .zip file, archived into a .zip file and uploaded to S3 otherwise

        stability
        :stability: experimental
        """
        options = _AssetOptions_ed6c2956(readers=readers, source_hash=source_hash, exclude=exclude, follow=follow, asset_hash=asset_hash, asset_hash_type=asset_hash_type, bundling=bundling)

        return jsii.sinvoke(cls, "fromAsset", [path, options])

    @jsii.member(jsii_name="fromBucket")
    @builtins.classmethod
    def from_bucket(cls, bucket: _IBucket_25bad983, key: str, object_version: typing.Optional[str]=None) -> "S3Code":
        """
        :param bucket: The S3 bucket.
        :param key: The object key.
        :param object_version: Optional S3 object version.

        return
        :return: ``LambdaS3Code`` associated with the specified S3 object.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromBucket", [bucket, key, object_version])

    @jsii.member(jsii_name="fromCfnParameters")
    @builtins.classmethod
    def from_cfn_parameters(cls, *, bucket_name_param: typing.Optional[_CfnParameter_90f1d0df]=None, object_key_param: typing.Optional[_CfnParameter_90f1d0df]=None) -> "CfnParametersCode":
        """Creates a new Lambda source defined using CloudFormation parameters.

        :param bucket_name_param: The CloudFormation parameter that represents the name of the S3 Bucket where the Lambda code will be located in. Must be of type 'String'. Default: a new parameter will be created
        :param object_key_param: The CloudFormation parameter that represents the path inside the S3 Bucket where the Lambda code will be located at. Must be of type 'String'. Default: a new parameter will be created

        return
        :return: a new instance of ``CfnParametersCode``

        stability
        :stability: experimental
        """
        props = CfnParametersCodeProps(bucket_name_param=bucket_name_param, object_key_param=object_key_param)

        return jsii.sinvoke(cls, "fromCfnParameters", [props])

    @jsii.member(jsii_name="fromInline")
    @builtins.classmethod
    def from_inline(cls, code: str) -> "InlineCode":
        """
        :param code: The actual handler code (limited to 4KiB).

        return
        :return: ``LambdaInlineCode`` with inline code.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromInline", [code])

    @jsii.member(jsii_name="inline")
    @builtins.classmethod
    def inline(cls, code: str) -> "InlineCode":
        """
        :param code: -

        deprecated
        :deprecated: use ``fromInline``

        stability
        :stability: deprecated
        """
        return jsii.sinvoke(cls, "inline", [code])

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(self, scope: _Construct_f50a3f53) -> "CodeConfig":
        """Called when the lambda or layer is initialized to allow this object to bind to the stack, add resources and have fun.

        :param scope: The binding scope. Don't be smart about trying to down-cast or assume it's initialized. You may just use it as a construct scope.

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="bindToResource")
    def bind_to_resource(self, _resource: _CfnResource_7760e8e4, *, resource_property: typing.Optional[str]=None) -> None:
        """Called after the CFN function resource has been created to allow the code class to bind to it.

        Specifically it's required to allow assets to add
        metadata for tooling like SAM CLI to be able to find their origins.

        :param _resource: -
        :param resource_property: The name of the CloudFormation property to annotate with asset metadata. Default: Code

        stability
        :stability: experimental
        """
        _options = ResourceBindOptions(resource_property=resource_property)

        return jsii.invoke(self, "bindToResource", [_resource, _options])

    @builtins.property
    @jsii.member(jsii_name="isInline")
    @abc.abstractmethod
    def is_inline(self) -> bool:
        """Determines whether this Code is inline code or not.

        deprecated
        :deprecated:

        this value is ignored since inline is now determined based on the
        the ``inlineCode`` field of ``CodeConfig`` returned from ``bind()``.

        stability
        :stability: deprecated
        """
        ...


class _CodeProxy(Code):
    @jsii.member(jsii_name="bind")
    def bind(self, scope: _Construct_f50a3f53) -> "CodeConfig":
        """Called when the lambda or layer is initialized to allow this object to bind to the stack, add resources and have fun.

        :param scope: The binding scope. Don't be smart about trying to down-cast or assume it's initialized. You may just use it as a construct scope.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [scope])

    @builtins.property
    @jsii.member(jsii_name="isInline")
    def is_inline(self) -> bool:
        """Determines whether this Code is inline code or not.

        deprecated
        :deprecated:

        this value is ignored since inline is now determined based on the
        the ``inlineCode`` field of ``CodeConfig`` returned from ``bind()``.

        stability
        :stability: deprecated
        """
        return jsii.get(self, "isInline")


@jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.CodeConfig", jsii_struct_bases=[], name_mapping={'inline_code': 'inlineCode', 's3_location': 's3Location'})
class CodeConfig():
    def __init__(self, *, inline_code: typing.Optional[str]=None, s3_location: typing.Optional[_Location_2d2ff215]=None) -> None:
        """
        :param inline_code: Inline code (mutually exclusive with ``s3Location``).
        :param s3_location: The location of the code in S3 (mutually exclusive with ``inlineCode``).

        stability
        :stability: experimental
        """
        if isinstance(s3_location, dict): s3_location = _Location_2d2ff215(**s3_location)
        self._values = {
        }
        if inline_code is not None: self._values["inline_code"] = inline_code
        if s3_location is not None: self._values["s3_location"] = s3_location

    @builtins.property
    def inline_code(self) -> typing.Optional[str]:
        """Inline code (mutually exclusive with ``s3Location``).

        stability
        :stability: experimental
        """
        return self._values.get('inline_code')

    @builtins.property
    def s3_location(self) -> typing.Optional[_Location_2d2ff215]:
        """The location of the code in S3 (mutually exclusive with ``inlineCode``).

        stability
        :stability: experimental
        """
        return self._values.get('s3_location')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CodeConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.DestinationConfig", jsii_struct_bases=[], name_mapping={'destination': 'destination'})
class DestinationConfig():
    def __init__(self, *, destination: str) -> None:
        """A destination configuration.

        :param destination: The Amazon Resource Name (ARN) of the destination resource.

        stability
        :stability: experimental
        """
        self._values = {
            'destination': destination,
        }

    @builtins.property
    def destination(self) -> str:
        """The Amazon Resource Name (ARN) of the destination resource.

        stability
        :stability: experimental
        """
        return self._values.get('destination')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DestinationConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.DestinationOptions", jsii_struct_bases=[], name_mapping={'type': 'type'})
class DestinationOptions():
    def __init__(self, *, type: "DestinationType") -> None:
        """Options when binding a destination to a function.

        :param type: The destination type.

        stability
        :stability: experimental
        """
        self._values = {
            'type': type,
        }

    @builtins.property
    def type(self) -> "DestinationType":
        """The destination type.

        stability
        :stability: experimental
        """
        return self._values.get('type')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DestinationOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="monocdk-experiment.aws_lambda.DestinationType")
class DestinationType(enum.Enum):
    """The type of destination.

    stability
    :stability: experimental
    """
    FAILURE = "FAILURE"
    """Failure.

    stability
    :stability: experimental
    """
    SUCCESS = "SUCCESS"
    """Success.

    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.DlqDestinationConfig", jsii_struct_bases=[], name_mapping={'destination': 'destination'})
class DlqDestinationConfig():
    def __init__(self, *, destination: str) -> None:
        """A destination configuration.

        :param destination: The Amazon Resource Name (ARN) of the destination resource.

        stability
        :stability: experimental
        """
        self._values = {
            'destination': destination,
        }

    @builtins.property
    def destination(self) -> str:
        """The Amazon Resource Name (ARN) of the destination resource.

        stability
        :stability: experimental
        """
        return self._values.get('destination')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DlqDestinationConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class EventInvokeConfig(_Resource_884d0774, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_lambda.EventInvokeConfig"):
    """Configure options for asynchronous invocation on a version or an alias.

    By default, Lambda retries an asynchronous invocation twice if the function
    returns an error. It retains events in a queue for up to six hours. When an
    event fails all processing attempts or stays in the asynchronous invocation
    queue for too long, Lambda discards it.

    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, function: "IFunction", qualifier: typing.Optional[str]=None, max_event_age: typing.Optional[_Duration_5170c158]=None, on_failure: typing.Optional["IDestination"]=None, on_success: typing.Optional["IDestination"]=None, retry_attempts: typing.Optional[jsii.Number]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param function: The Lambda function.
        :param qualifier: The qualifier. Default: - latest version
        :param max_event_age: The maximum age of a request that Lambda sends to a function for processing. Minimum: 60 seconds Maximum: 6 hours Default: Duration.hours(6)
        :param on_failure: The destination for failed invocations. Default: - no destination
        :param on_success: The destination for successful invocations. Default: - no destination
        :param retry_attempts: The maximum number of times to retry when the function returns an error. Minimum: 0 Maximum: 2 Default: 2

        stability
        :stability: experimental
        """
        props = EventInvokeConfigProps(function=function, qualifier=qualifier, max_event_age=max_event_age, on_failure=on_failure, on_success=on_success, retry_attempts=retry_attempts)

        jsii.create(EventInvokeConfig, self, [scope, id, props])


@jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.EventInvokeConfigOptions", jsii_struct_bases=[], name_mapping={'max_event_age': 'maxEventAge', 'on_failure': 'onFailure', 'on_success': 'onSuccess', 'retry_attempts': 'retryAttempts'})
class EventInvokeConfigOptions():
    def __init__(self, *, max_event_age: typing.Optional[_Duration_5170c158]=None, on_failure: typing.Optional["IDestination"]=None, on_success: typing.Optional["IDestination"]=None, retry_attempts: typing.Optional[jsii.Number]=None) -> None:
        """Options to add an EventInvokeConfig to a function.

        :param max_event_age: The maximum age of a request that Lambda sends to a function for processing. Minimum: 60 seconds Maximum: 6 hours Default: Duration.hours(6)
        :param on_failure: The destination for failed invocations. Default: - no destination
        :param on_success: The destination for successful invocations. Default: - no destination
        :param retry_attempts: The maximum number of times to retry when the function returns an error. Minimum: 0 Maximum: 2 Default: 2

        stability
        :stability: experimental
        """
        self._values = {
        }
        if max_event_age is not None: self._values["max_event_age"] = max_event_age
        if on_failure is not None: self._values["on_failure"] = on_failure
        if on_success is not None: self._values["on_success"] = on_success
        if retry_attempts is not None: self._values["retry_attempts"] = retry_attempts

    @builtins.property
    def max_event_age(self) -> typing.Optional[_Duration_5170c158]:
        """The maximum age of a request that Lambda sends to a function for processing.

        Minimum: 60 seconds
        Maximum: 6 hours

        default
        :default: Duration.hours(6)

        stability
        :stability: experimental
        """
        return self._values.get('max_event_age')

    @builtins.property
    def on_failure(self) -> typing.Optional["IDestination"]:
        """The destination for failed invocations.

        default
        :default: - no destination

        stability
        :stability: experimental
        """
        return self._values.get('on_failure')

    @builtins.property
    def on_success(self) -> typing.Optional["IDestination"]:
        """The destination for successful invocations.

        default
        :default: - no destination

        stability
        :stability: experimental
        """
        return self._values.get('on_success')

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        """The maximum number of times to retry when the function returns an error.

        Minimum: 0
        Maximum: 2

        default
        :default: 2

        stability
        :stability: experimental
        """
        return self._values.get('retry_attempts')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EventInvokeConfigOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.EventInvokeConfigProps", jsii_struct_bases=[EventInvokeConfigOptions], name_mapping={'max_event_age': 'maxEventAge', 'on_failure': 'onFailure', 'on_success': 'onSuccess', 'retry_attempts': 'retryAttempts', 'function': 'function', 'qualifier': 'qualifier'})
class EventInvokeConfigProps(EventInvokeConfigOptions):
    def __init__(self, *, max_event_age: typing.Optional[_Duration_5170c158]=None, on_failure: typing.Optional["IDestination"]=None, on_success: typing.Optional["IDestination"]=None, retry_attempts: typing.Optional[jsii.Number]=None, function: "IFunction", qualifier: typing.Optional[str]=None) -> None:
        """Properties for an EventInvokeConfig.

        :param max_event_age: The maximum age of a request that Lambda sends to a function for processing. Minimum: 60 seconds Maximum: 6 hours Default: Duration.hours(6)
        :param on_failure: The destination for failed invocations. Default: - no destination
        :param on_success: The destination for successful invocations. Default: - no destination
        :param retry_attempts: The maximum number of times to retry when the function returns an error. Minimum: 0 Maximum: 2 Default: 2
        :param function: The Lambda function.
        :param qualifier: The qualifier. Default: - latest version

        stability
        :stability: experimental
        """
        self._values = {
            'function': function,
        }
        if max_event_age is not None: self._values["max_event_age"] = max_event_age
        if on_failure is not None: self._values["on_failure"] = on_failure
        if on_success is not None: self._values["on_success"] = on_success
        if retry_attempts is not None: self._values["retry_attempts"] = retry_attempts
        if qualifier is not None: self._values["qualifier"] = qualifier

    @builtins.property
    def max_event_age(self) -> typing.Optional[_Duration_5170c158]:
        """The maximum age of a request that Lambda sends to a function for processing.

        Minimum: 60 seconds
        Maximum: 6 hours

        default
        :default: Duration.hours(6)

        stability
        :stability: experimental
        """
        return self._values.get('max_event_age')

    @builtins.property
    def on_failure(self) -> typing.Optional["IDestination"]:
        """The destination for failed invocations.

        default
        :default: - no destination

        stability
        :stability: experimental
        """
        return self._values.get('on_failure')

    @builtins.property
    def on_success(self) -> typing.Optional["IDestination"]:
        """The destination for successful invocations.

        default
        :default: - no destination

        stability
        :stability: experimental
        """
        return self._values.get('on_success')

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        """The maximum number of times to retry when the function returns an error.

        Minimum: 0
        Maximum: 2

        default
        :default: 2

        stability
        :stability: experimental
        """
        return self._values.get('retry_attempts')

    @builtins.property
    def function(self) -> "IFunction":
        """The Lambda function.

        stability
        :stability: experimental
        """
        return self._values.get('function')

    @builtins.property
    def qualifier(self) -> typing.Optional[str]:
        """The qualifier.

        default
        :default: - latest version

        stability
        :stability: experimental
        """
        return self._values.get('qualifier')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EventInvokeConfigProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.EventSourceMappingOptions", jsii_struct_bases=[], name_mapping={'event_source_arn': 'eventSourceArn', 'batch_size': 'batchSize', 'bisect_batch_on_error': 'bisectBatchOnError', 'enabled': 'enabled', 'max_batching_window': 'maxBatchingWindow', 'max_record_age': 'maxRecordAge', 'on_failure': 'onFailure', 'parallelization_factor': 'parallelizationFactor', 'retry_attempts': 'retryAttempts', 'starting_position': 'startingPosition'})
class EventSourceMappingOptions():
    def __init__(self, *, event_source_arn: str, batch_size: typing.Optional[jsii.Number]=None, bisect_batch_on_error: typing.Optional[bool]=None, enabled: typing.Optional[bool]=None, max_batching_window: typing.Optional[_Duration_5170c158]=None, max_record_age: typing.Optional[_Duration_5170c158]=None, on_failure: typing.Optional["IEventSourceDlq"]=None, parallelization_factor: typing.Optional[jsii.Number]=None, retry_attempts: typing.Optional[jsii.Number]=None, starting_position: typing.Optional["StartingPosition"]=None) -> None:
        """
        :param event_source_arn: The Amazon Resource Name (ARN) of the event source. Any record added to this stream can invoke the Lambda function.
        :param batch_size: The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: Minimum value of 1. Maximum value of 10000. Default: - Amazon Kinesis and Amazon DynamoDB is 100 records. Both the default and maximum for Amazon SQS are 10 messages.
        :param bisect_batch_on_error: If the function returns an error, split the batch in two and retry. Default: false
        :param enabled: Set to false to disable the event source upon creation. Default: true
        :param max_batching_window: The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5) Default: Duration.seconds(0)
        :param max_record_age: The maximum age of a record that Lambda sends to a function for processing. Valid Range: - Minimum value of 60 seconds - Maximum value of 7 days Default: Duration.days(7)
        :param on_failure: An Amazon SQS queue or Amazon SNS topic destination for discarded records. Default: discarded records are ignored
        :param parallelization_factor: The number of batches to process from each shard concurrently. Valid Range: - Minimum value of 1 - Maximum value of 10 Default: 1
        :param retry_attempts: The maximum number of times to retry when the function returns an error. Valid Range: - Minimum value of 0 - Maximum value of 10000 Default: 10000
        :param starting_position: The position in the DynamoDB or Kinesis stream where AWS Lambda should start reading. Default: - Required for Amazon Kinesis and Amazon DynamoDB Streams sources.

        stability
        :stability: experimental
        """
        self._values = {
            'event_source_arn': event_source_arn,
        }
        if batch_size is not None: self._values["batch_size"] = batch_size
        if bisect_batch_on_error is not None: self._values["bisect_batch_on_error"] = bisect_batch_on_error
        if enabled is not None: self._values["enabled"] = enabled
        if max_batching_window is not None: self._values["max_batching_window"] = max_batching_window
        if max_record_age is not None: self._values["max_record_age"] = max_record_age
        if on_failure is not None: self._values["on_failure"] = on_failure
        if parallelization_factor is not None: self._values["parallelization_factor"] = parallelization_factor
        if retry_attempts is not None: self._values["retry_attempts"] = retry_attempts
        if starting_position is not None: self._values["starting_position"] = starting_position

    @builtins.property
    def event_source_arn(self) -> str:
        """The Amazon Resource Name (ARN) of the event source.

        Any record added to
        this stream can invoke the Lambda function.

        stability
        :stability: experimental
        """
        return self._values.get('event_source_arn')

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        """The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function.

        Your function receives an
        event with all the retrieved records.

        Valid Range: Minimum value of 1. Maximum value of 10000.

        default
        :default:

        - Amazon Kinesis and Amazon DynamoDB is 100 records.
          Both the default and maximum for Amazon SQS are 10 messages.

        stability
        :stability: experimental
        """
        return self._values.get('batch_size')

    @builtins.property
    def bisect_batch_on_error(self) -> typing.Optional[bool]:
        """If the function returns an error, split the batch in two and retry.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('bisect_batch_on_error')

    @builtins.property
    def enabled(self) -> typing.Optional[bool]:
        """Set to false to disable the event source upon creation.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('enabled')

    @builtins.property
    def max_batching_window(self) -> typing.Optional[_Duration_5170c158]:
        """The maximum amount of time to gather records before invoking the function.

        Maximum of Duration.minutes(5)

        default
        :default: Duration.seconds(0)

        stability
        :stability: experimental
        """
        return self._values.get('max_batching_window')

    @builtins.property
    def max_record_age(self) -> typing.Optional[_Duration_5170c158]:
        """The maximum age of a record that Lambda sends to a function for processing.

        Valid Range:

        - Minimum value of 60 seconds
        - Maximum value of 7 days

        default
        :default: Duration.days(7)

        stability
        :stability: experimental
        """
        return self._values.get('max_record_age')

    @builtins.property
    def on_failure(self) -> typing.Optional["IEventSourceDlq"]:
        """An Amazon SQS queue or Amazon SNS topic destination for discarded records.

        default
        :default: discarded records are ignored

        stability
        :stability: experimental
        """
        return self._values.get('on_failure')

    @builtins.property
    def parallelization_factor(self) -> typing.Optional[jsii.Number]:
        """The number of batches to process from each shard concurrently.

        Valid Range:

        - Minimum value of 1
        - Maximum value of 10

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('parallelization_factor')

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        """The maximum number of times to retry when the function returns an error.

        Valid Range:

        - Minimum value of 0
        - Maximum value of 10000

        default
        :default: 10000

        stability
        :stability: experimental
        """
        return self._values.get('retry_attempts')

    @builtins.property
    def starting_position(self) -> typing.Optional["StartingPosition"]:
        """The position in the DynamoDB or Kinesis stream where AWS Lambda should start reading.

        default
        :default: - Required for Amazon Kinesis and Amazon DynamoDB Streams sources.

        see
        :see: https://docs.aws.amazon.com/kinesis/latest/APIReference/API_GetShardIterator.html#Kinesis-GetShardIterator-request-ShardIteratorType
        stability
        :stability: experimental
        """
        return self._values.get('starting_position')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EventSourceMappingOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.EventSourceMappingProps", jsii_struct_bases=[EventSourceMappingOptions], name_mapping={'event_source_arn': 'eventSourceArn', 'batch_size': 'batchSize', 'bisect_batch_on_error': 'bisectBatchOnError', 'enabled': 'enabled', 'max_batching_window': 'maxBatchingWindow', 'max_record_age': 'maxRecordAge', 'on_failure': 'onFailure', 'parallelization_factor': 'parallelizationFactor', 'retry_attempts': 'retryAttempts', 'starting_position': 'startingPosition', 'target': 'target'})
class EventSourceMappingProps(EventSourceMappingOptions):
    def __init__(self, *, event_source_arn: str, batch_size: typing.Optional[jsii.Number]=None, bisect_batch_on_error: typing.Optional[bool]=None, enabled: typing.Optional[bool]=None, max_batching_window: typing.Optional[_Duration_5170c158]=None, max_record_age: typing.Optional[_Duration_5170c158]=None, on_failure: typing.Optional["IEventSourceDlq"]=None, parallelization_factor: typing.Optional[jsii.Number]=None, retry_attempts: typing.Optional[jsii.Number]=None, starting_position: typing.Optional["StartingPosition"]=None, target: "IFunction") -> None:
        """Properties for declaring a new event source mapping.

        :param event_source_arn: The Amazon Resource Name (ARN) of the event source. Any record added to this stream can invoke the Lambda function.
        :param batch_size: The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: Minimum value of 1. Maximum value of 10000. Default: - Amazon Kinesis and Amazon DynamoDB is 100 records. Both the default and maximum for Amazon SQS are 10 messages.
        :param bisect_batch_on_error: If the function returns an error, split the batch in two and retry. Default: false
        :param enabled: Set to false to disable the event source upon creation. Default: true
        :param max_batching_window: The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5) Default: Duration.seconds(0)
        :param max_record_age: The maximum age of a record that Lambda sends to a function for processing. Valid Range: - Minimum value of 60 seconds - Maximum value of 7 days Default: Duration.days(7)
        :param on_failure: An Amazon SQS queue or Amazon SNS topic destination for discarded records. Default: discarded records are ignored
        :param parallelization_factor: The number of batches to process from each shard concurrently. Valid Range: - Minimum value of 1 - Maximum value of 10 Default: 1
        :param retry_attempts: The maximum number of times to retry when the function returns an error. Valid Range: - Minimum value of 0 - Maximum value of 10000 Default: 10000
        :param starting_position: The position in the DynamoDB or Kinesis stream where AWS Lambda should start reading. Default: - Required for Amazon Kinesis and Amazon DynamoDB Streams sources.
        :param target: The target AWS Lambda function.

        stability
        :stability: experimental
        """
        self._values = {
            'event_source_arn': event_source_arn,
            'target': target,
        }
        if batch_size is not None: self._values["batch_size"] = batch_size
        if bisect_batch_on_error is not None: self._values["bisect_batch_on_error"] = bisect_batch_on_error
        if enabled is not None: self._values["enabled"] = enabled
        if max_batching_window is not None: self._values["max_batching_window"] = max_batching_window
        if max_record_age is not None: self._values["max_record_age"] = max_record_age
        if on_failure is not None: self._values["on_failure"] = on_failure
        if parallelization_factor is not None: self._values["parallelization_factor"] = parallelization_factor
        if retry_attempts is not None: self._values["retry_attempts"] = retry_attempts
        if starting_position is not None: self._values["starting_position"] = starting_position

    @builtins.property
    def event_source_arn(self) -> str:
        """The Amazon Resource Name (ARN) of the event source.

        Any record added to
        this stream can invoke the Lambda function.

        stability
        :stability: experimental
        """
        return self._values.get('event_source_arn')

    @builtins.property
    def batch_size(self) -> typing.Optional[jsii.Number]:
        """The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function.

        Your function receives an
        event with all the retrieved records.

        Valid Range: Minimum value of 1. Maximum value of 10000.

        default
        :default:

        - Amazon Kinesis and Amazon DynamoDB is 100 records.
          Both the default and maximum for Amazon SQS are 10 messages.

        stability
        :stability: experimental
        """
        return self._values.get('batch_size')

    @builtins.property
    def bisect_batch_on_error(self) -> typing.Optional[bool]:
        """If the function returns an error, split the batch in two and retry.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('bisect_batch_on_error')

    @builtins.property
    def enabled(self) -> typing.Optional[bool]:
        """Set to false to disable the event source upon creation.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('enabled')

    @builtins.property
    def max_batching_window(self) -> typing.Optional[_Duration_5170c158]:
        """The maximum amount of time to gather records before invoking the function.

        Maximum of Duration.minutes(5)

        default
        :default: Duration.seconds(0)

        stability
        :stability: experimental
        """
        return self._values.get('max_batching_window')

    @builtins.property
    def max_record_age(self) -> typing.Optional[_Duration_5170c158]:
        """The maximum age of a record that Lambda sends to a function for processing.

        Valid Range:

        - Minimum value of 60 seconds
        - Maximum value of 7 days

        default
        :default: Duration.days(7)

        stability
        :stability: experimental
        """
        return self._values.get('max_record_age')

    @builtins.property
    def on_failure(self) -> typing.Optional["IEventSourceDlq"]:
        """An Amazon SQS queue or Amazon SNS topic destination for discarded records.

        default
        :default: discarded records are ignored

        stability
        :stability: experimental
        """
        return self._values.get('on_failure')

    @builtins.property
    def parallelization_factor(self) -> typing.Optional[jsii.Number]:
        """The number of batches to process from each shard concurrently.

        Valid Range:

        - Minimum value of 1
        - Maximum value of 10

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get('parallelization_factor')

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        """The maximum number of times to retry when the function returns an error.

        Valid Range:

        - Minimum value of 0
        - Maximum value of 10000

        default
        :default: 10000

        stability
        :stability: experimental
        """
        return self._values.get('retry_attempts')

    @builtins.property
    def starting_position(self) -> typing.Optional["StartingPosition"]:
        """The position in the DynamoDB or Kinesis stream where AWS Lambda should start reading.

        default
        :default: - Required for Amazon Kinesis and Amazon DynamoDB Streams sources.

        see
        :see: https://docs.aws.amazon.com/kinesis/latest/APIReference/API_GetShardIterator.html#Kinesis-GetShardIterator-request-ShardIteratorType
        stability
        :stability: experimental
        """
        return self._values.get('starting_position')

    @builtins.property
    def target(self) -> "IFunction":
        """The target AWS Lambda function.

        stability
        :stability: experimental
        """
        return self._values.get('target')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EventSourceMappingProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.FunctionAttributes", jsii_struct_bases=[], name_mapping={'function_arn': 'functionArn', 'role': 'role', 'security_group': 'securityGroup', 'security_group_id': 'securityGroupId'})
class FunctionAttributes():
    def __init__(self, *, function_arn: str, role: typing.Optional[_IRole_e69bbae4]=None, security_group: typing.Optional[_ISecurityGroup_d72ab8e8]=None, security_group_id: typing.Optional[str]=None) -> None:
        """Represents a Lambda function defined outside of this stack.

        :param function_arn: The ARN of the Lambda function. Format: arn::lambda:::function:
        :param role: The IAM execution role associated with this function. If the role is not specified, any role-related operations will no-op.
        :param security_group: The security group of this Lambda, if in a VPC. This needs to be given in order to support allowing connections to this Lambda.
        :param security_group_id: Id of the security group of this Lambda, if in a VPC. This needs to be given in order to support allowing connections to this Lambda.

        stability
        :stability: experimental
        """
        self._values = {
            'function_arn': function_arn,
        }
        if role is not None: self._values["role"] = role
        if security_group is not None: self._values["security_group"] = security_group
        if security_group_id is not None: self._values["security_group_id"] = security_group_id

    @builtins.property
    def function_arn(self) -> str:
        """The ARN of the Lambda function.

        Format: arn::lambda:::function:

        stability
        :stability: experimental
        """
        return self._values.get('function_arn')

    @builtins.property
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The IAM execution role associated with this function.

        If the role is not specified, any role-related operations will no-op.

        stability
        :stability: experimental
        """
        return self._values.get('role')

    @builtins.property
    def security_group(self) -> typing.Optional[_ISecurityGroup_d72ab8e8]:
        """The security group of this Lambda, if in a VPC.

        This needs to be given in order to support allowing connections
        to this Lambda.

        stability
        :stability: experimental
        """
        return self._values.get('security_group')

    @builtins.property
    def security_group_id(self) -> typing.Optional[str]:
        """Id of the security group of this Lambda, if in a VPC.

        This needs to be given in order to support allowing connections
        to this Lambda.

        deprecated
        :deprecated: use ``securityGroup`` instead

        stability
        :stability: deprecated
        """
        return self._values.get('security_group_id')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'FunctionAttributes(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.FunctionOptions", jsii_struct_bases=[EventInvokeConfigOptions], name_mapping={'max_event_age': 'maxEventAge', 'on_failure': 'onFailure', 'on_success': 'onSuccess', 'retry_attempts': 'retryAttempts', 'allow_all_outbound': 'allowAllOutbound', 'current_version_options': 'currentVersionOptions', 'dead_letter_queue': 'deadLetterQueue', 'dead_letter_queue_enabled': 'deadLetterQueueEnabled', 'description': 'description', 'environment': 'environment', 'events': 'events', 'function_name': 'functionName', 'initial_policy': 'initialPolicy', 'layers': 'layers', 'log_retention': 'logRetention', 'log_retention_retry_options': 'logRetentionRetryOptions', 'log_retention_role': 'logRetentionRole', 'memory_size': 'memorySize', 'reserved_concurrent_executions': 'reservedConcurrentExecutions', 'role': 'role', 'security_group': 'securityGroup', 'security_groups': 'securityGroups', 'timeout': 'timeout', 'tracing': 'tracing', 'vpc': 'vpc', 'vpc_subnets': 'vpcSubnets'})
class FunctionOptions(EventInvokeConfigOptions):
    def __init__(self, *, max_event_age: typing.Optional[_Duration_5170c158]=None, on_failure: typing.Optional["IDestination"]=None, on_success: typing.Optional["IDestination"]=None, retry_attempts: typing.Optional[jsii.Number]=None, allow_all_outbound: typing.Optional[bool]=None, current_version_options: typing.Optional["VersionOptions"]=None, dead_letter_queue: typing.Optional[_IQueue_b743f559]=None, dead_letter_queue_enabled: typing.Optional[bool]=None, description: typing.Optional[str]=None, environment: typing.Optional[typing.Mapping[str, str]]=None, events: typing.Optional[typing.List["IEventSource"]]=None, function_name: typing.Optional[str]=None, initial_policy: typing.Optional[typing.List[_PolicyStatement_f75dc775]]=None, layers: typing.Optional[typing.List["ILayerVersion"]]=None, log_retention: typing.Optional[_RetentionDays_bdc7ad1f]=None, log_retention_retry_options: typing.Optional["LogRetentionRetryOptions"]=None, log_retention_role: typing.Optional[_IRole_e69bbae4]=None, memory_size: typing.Optional[jsii.Number]=None, reserved_concurrent_executions: typing.Optional[jsii.Number]=None, role: typing.Optional[_IRole_e69bbae4]=None, security_group: typing.Optional[_ISecurityGroup_d72ab8e8]=None, security_groups: typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]]=None, timeout: typing.Optional[_Duration_5170c158]=None, tracing: typing.Optional["Tracing"]=None, vpc: typing.Optional[_IVpc_3795853f]=None, vpc_subnets: typing.Optional[_SubnetSelection_36a13cd6]=None) -> None:
        """Non runtime options.

        :param max_event_age: The maximum age of a request that Lambda sends to a function for processing. Minimum: 60 seconds Maximum: 6 hours Default: Duration.hours(6)
        :param on_failure: The destination for failed invocations. Default: - no destination
        :param on_success: The destination for successful invocations. Default: - no destination
        :param retry_attempts: The maximum number of times to retry when the function returns an error. Minimum: 0 Maximum: 2 Default: 2
        :param allow_all_outbound: Whether to allow the Lambda to send all network traffic. If set to false, you must individually add traffic rules to allow the Lambda to connect to network targets. Default: true
        :param current_version_options: Options for the ``lambda.Version`` resource automatically created by the ``fn.currentVersion`` method. Default: - default options as described in ``VersionOptions``
        :param dead_letter_queue: The SQS queue to use if DLQ is enabled. Default: - SQS queue with 14 day retention period if ``deadLetterQueueEnabled`` is ``true``
        :param dead_letter_queue_enabled: Enabled DLQ. If ``deadLetterQueue`` is undefined, an SQS queue with default options will be defined for your Function. Default: - false unless ``deadLetterQueue`` is set, which implies DLQ is enabled.
        :param description: A description of the function. Default: - No description.
        :param environment: Key-value pairs that Lambda caches and makes available for your Lambda functions. Use environment variables to apply configuration changes, such as test and production environment configurations, without changing your Lambda function source code. Default: - No environment variables.
        :param events: Event sources for this function. You can also add event sources using ``addEventSource``. Default: - No event sources.
        :param function_name: A name for the function. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the function's name. For more information, see Name Type.
        :param initial_policy: Initial policy statements to add to the created Lambda Role. You can call ``addToRolePolicy`` to the created lambda to add statements post creation. Default: - No policy statements are added to the created Lambda role.
        :param layers: A list of layers to add to the function's execution environment. You can configure your Lambda function to pull in additional code during initialization in the form of layers. Layers are packages of libraries or other dependencies that can be used by mulitple functions. Default: - No layers.
        :param log_retention: The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.INFINITE
        :param log_retention_retry_options: When log retention is specified, a custom resource attempts to create the CloudWatch log group. These options control the retry policy when interacting with CloudWatch APIs. Default: - Default AWS SDK retry options.
        :param log_retention_role: The IAM role for the Lambda function associated with the custom resource that sets the retention policy. Default: - A new role is created.
        :param memory_size: The amount of memory, in MB, that is allocated to your Lambda function. Lambda uses this value to proportionally allocate the amount of CPU power. For more information, see Resource Model in the AWS Lambda Developer Guide. Default: 128
        :param reserved_concurrent_executions: The maximum of concurrent executions you want to reserve for the function. Default: - No specific limit - account limit.
        :param role: Lambda execution role. This is the role that will be assumed by the function upon execution. It controls the permissions that the function will have. The Role must be assumable by the 'lambda.amazonaws.com' service principal. The default Role automatically has permissions granted for Lambda execution. If you provide a Role, you must add the relevant AWS managed policies yourself. The relevant managed policies are "service-role/AWSLambdaBasicExecutionRole" and "service-role/AWSLambdaVPCAccessExecutionRole". Default: - A unique role will be generated for this lambda function. Both supplied and generated roles can always be changed by calling ``addToRolePolicy``.
        :param security_group: What security group to associate with the Lambda's network interfaces. This property is being deprecated, consider using securityGroups instead. Only used if 'vpc' is supplied. Use securityGroups property instead. Function constructor will throw an error if both are specified. Default: - If the function is placed within a VPC and a security group is not specified, either by this or securityGroups prop, a dedicated security group will be created for this function.
        :param security_groups: The list of security groups to associate with the Lambda's network interfaces. Only used if 'vpc' is supplied. Default: - If the function is placed within a VPC and a security group is not specified, either by this or securityGroup prop, a dedicated security group will be created for this function.
        :param timeout: The function execution time (in seconds) after which Lambda terminates the function. Because the execution time affects cost, set this value based on the function's expected execution time. Default: Duration.seconds(3)
        :param tracing: Enable AWS X-Ray Tracing for Lambda Function. Default: Tracing.Disabled
        :param vpc: VPC network to place Lambda network interfaces. Specify this if the Lambda function needs to access resources in a VPC. Default: - Function is not placed within a VPC.
        :param vpc_subnets: Where to place the network interfaces within the VPC. Only used if 'vpc' is supplied. Note: internet access for Lambdas requires a NAT gateway, so picking Public subnets is not allowed. Default: - the Vpc default strategy if not specified

        stability
        :stability: experimental
        """
        if isinstance(current_version_options, dict): current_version_options = VersionOptions(**current_version_options)
        if isinstance(log_retention_retry_options, dict): log_retention_retry_options = LogRetentionRetryOptions(**log_retention_retry_options)
        if isinstance(vpc_subnets, dict): vpc_subnets = _SubnetSelection_36a13cd6(**vpc_subnets)
        self._values = {
        }
        if max_event_age is not None: self._values["max_event_age"] = max_event_age
        if on_failure is not None: self._values["on_failure"] = on_failure
        if on_success is not None: self._values["on_success"] = on_success
        if retry_attempts is not None: self._values["retry_attempts"] = retry_attempts
        if allow_all_outbound is not None: self._values["allow_all_outbound"] = allow_all_outbound
        if current_version_options is not None: self._values["current_version_options"] = current_version_options
        if dead_letter_queue is not None: self._values["dead_letter_queue"] = dead_letter_queue
        if dead_letter_queue_enabled is not None: self._values["dead_letter_queue_enabled"] = dead_letter_queue_enabled
        if description is not None: self._values["description"] = description
        if environment is not None: self._values["environment"] = environment
        if events is not None: self._values["events"] = events
        if function_name is not None: self._values["function_name"] = function_name
        if initial_policy is not None: self._values["initial_policy"] = initial_policy
        if layers is not None: self._values["layers"] = layers
        if log_retention is not None: self._values["log_retention"] = log_retention
        if log_retention_retry_options is not None: self._values["log_retention_retry_options"] = log_retention_retry_options
        if log_retention_role is not None: self._values["log_retention_role"] = log_retention_role
        if memory_size is not None: self._values["memory_size"] = memory_size
        if reserved_concurrent_executions is not None: self._values["reserved_concurrent_executions"] = reserved_concurrent_executions
        if role is not None: self._values["role"] = role
        if security_group is not None: self._values["security_group"] = security_group
        if security_groups is not None: self._values["security_groups"] = security_groups
        if timeout is not None: self._values["timeout"] = timeout
        if tracing is not None: self._values["tracing"] = tracing
        if vpc is not None: self._values["vpc"] = vpc
        if vpc_subnets is not None: self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def max_event_age(self) -> typing.Optional[_Duration_5170c158]:
        """The maximum age of a request that Lambda sends to a function for processing.

        Minimum: 60 seconds
        Maximum: 6 hours

        default
        :default: Duration.hours(6)

        stability
        :stability: experimental
        """
        return self._values.get('max_event_age')

    @builtins.property
    def on_failure(self) -> typing.Optional["IDestination"]:
        """The destination for failed invocations.

        default
        :default: - no destination

        stability
        :stability: experimental
        """
        return self._values.get('on_failure')

    @builtins.property
    def on_success(self) -> typing.Optional["IDestination"]:
        """The destination for successful invocations.

        default
        :default: - no destination

        stability
        :stability: experimental
        """
        return self._values.get('on_success')

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        """The maximum number of times to retry when the function returns an error.

        Minimum: 0
        Maximum: 2

        default
        :default: 2

        stability
        :stability: experimental
        """
        return self._values.get('retry_attempts')

    @builtins.property
    def allow_all_outbound(self) -> typing.Optional[bool]:
        """Whether to allow the Lambda to send all network traffic.

        If set to false, you must individually add traffic rules to allow the
        Lambda to connect to network targets.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('allow_all_outbound')

    @builtins.property
    def current_version_options(self) -> typing.Optional["VersionOptions"]:
        """Options for the ``lambda.Version`` resource automatically created by the ``fn.currentVersion`` method.

        default
        :default: - default options as described in ``VersionOptions``

        stability
        :stability: experimental
        """
        return self._values.get('current_version_options')

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_IQueue_b743f559]:
        """The SQS queue to use if DLQ is enabled.

        default
        :default: - SQS queue with 14 day retention period if ``deadLetterQueueEnabled`` is ``true``

        stability
        :stability: experimental
        """
        return self._values.get('dead_letter_queue')

    @builtins.property
    def dead_letter_queue_enabled(self) -> typing.Optional[bool]:
        """Enabled DLQ.

        If ``deadLetterQueue`` is undefined,
        an SQS queue with default options will be defined for your Function.

        default
        :default: - false unless ``deadLetterQueue`` is set, which implies DLQ is enabled.

        stability
        :stability: experimental
        """
        return self._values.get('dead_letter_queue_enabled')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """A description of the function.

        default
        :default: - No description.

        stability
        :stability: experimental
        """
        return self._values.get('description')

    @builtins.property
    def environment(self) -> typing.Optional[typing.Mapping[str, str]]:
        """Key-value pairs that Lambda caches and makes available for your Lambda functions.

        Use environment variables to apply configuration changes, such
        as test and production environment configurations, without changing your
        Lambda function source code.

        default
        :default: - No environment variables.

        stability
        :stability: experimental
        """
        return self._values.get('environment')

    @builtins.property
    def events(self) -> typing.Optional[typing.List["IEventSource"]]:
        """Event sources for this function.

        You can also add event sources using ``addEventSource``.

        default
        :default: - No event sources.

        stability
        :stability: experimental
        """
        return self._values.get('events')

    @builtins.property
    def function_name(self) -> typing.Optional[str]:
        """A name for the function.

        default
        :default:

        - AWS CloudFormation generates a unique physical ID and uses that
          ID for the function's name. For more information, see Name Type.

        stability
        :stability: experimental
        """
        return self._values.get('function_name')

    @builtins.property
    def initial_policy(self) -> typing.Optional[typing.List[_PolicyStatement_f75dc775]]:
        """Initial policy statements to add to the created Lambda Role.

        You can call ``addToRolePolicy`` to the created lambda to add statements post creation.

        default
        :default: - No policy statements are added to the created Lambda role.

        stability
        :stability: experimental
        """
        return self._values.get('initial_policy')

    @builtins.property
    def layers(self) -> typing.Optional[typing.List["ILayerVersion"]]:
        """A list of layers to add to the function's execution environment.

        You can configure your Lambda function to pull in
        additional code during initialization in the form of layers. Layers are packages of libraries or other dependencies
        that can be used by mulitple functions.

        default
        :default: - No layers.

        stability
        :stability: experimental
        """
        return self._values.get('layers')

    @builtins.property
    def log_retention(self) -> typing.Optional[_RetentionDays_bdc7ad1f]:
        """The number of days log events are kept in CloudWatch Logs.

        When updating
        this property, unsetting it doesn't remove the log retention policy. To
        remove the retention policy, set the value to ``INFINITE``.

        default
        :default: logs.RetentionDays.INFINITE

        stability
        :stability: experimental
        """
        return self._values.get('log_retention')

    @builtins.property
    def log_retention_retry_options(self) -> typing.Optional["LogRetentionRetryOptions"]:
        """When log retention is specified, a custom resource attempts to create the CloudWatch log group.

        These options control the retry policy when interacting with CloudWatch APIs.

        default
        :default: - Default AWS SDK retry options.

        stability
        :stability: experimental
        """
        return self._values.get('log_retention_retry_options')

    @builtins.property
    def log_retention_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The IAM role for the Lambda function associated with the custom resource that sets the retention policy.

        default
        :default: - A new role is created.

        stability
        :stability: experimental
        """
        return self._values.get('log_retention_role')

    @builtins.property
    def memory_size(self) -> typing.Optional[jsii.Number]:
        """The amount of memory, in MB, that is allocated to your Lambda function.

        Lambda uses this value to proportionally allocate the amount of CPU
        power. For more information, see Resource Model in the AWS Lambda
        Developer Guide.

        default
        :default: 128

        stability
        :stability: experimental
        """
        return self._values.get('memory_size')

    @builtins.property
    def reserved_concurrent_executions(self) -> typing.Optional[jsii.Number]:
        """The maximum of concurrent executions you want to reserve for the function.

        default
        :default: - No specific limit - account limit.

        see
        :see: https://docs.aws.amazon.com/lambda/latest/dg/concurrent-executions.html
        stability
        :stability: experimental
        """
        return self._values.get('reserved_concurrent_executions')

    @builtins.property
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """Lambda execution role.

        This is the role that will be assumed by the function upon execution.
        It controls the permissions that the function will have. The Role must
        be assumable by the 'lambda.amazonaws.com' service principal.

        The default Role automatically has permissions granted for Lambda execution. If you
        provide a Role, you must add the relevant AWS managed policies yourself.

        The relevant managed policies are "service-role/AWSLambdaBasicExecutionRole" and
        "service-role/AWSLambdaVPCAccessExecutionRole".

        default
        :default:

        - A unique role will be generated for this lambda function.
          Both supplied and generated roles can always be changed by calling ``addToRolePolicy``.

        stability
        :stability: experimental
        """
        return self._values.get('role')

    @builtins.property
    def security_group(self) -> typing.Optional[_ISecurityGroup_d72ab8e8]:
        """What security group to associate with the Lambda's network interfaces. This property is being deprecated, consider using securityGroups instead.

        Only used if 'vpc' is supplied.

        Use securityGroups property instead.
        Function constructor will throw an error if both are specified.

        default
        :default:

        - If the function is placed within a VPC and a security group is
          not specified, either by this or securityGroups prop, a dedicated security
          group will be created for this function.

        deprecated
        :deprecated: - This property is deprecated, use securityGroups instead

        stability
        :stability: deprecated
        """
        return self._values.get('security_group')

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]]:
        """The list of security groups to associate with the Lambda's network interfaces.

        Only used if 'vpc' is supplied.

        default
        :default:

        - If the function is placed within a VPC and a security group is
          not specified, either by this or securityGroup prop, a dedicated security
          group will be created for this function.

        stability
        :stability: experimental
        """
        return self._values.get('security_groups')

    @builtins.property
    def timeout(self) -> typing.Optional[_Duration_5170c158]:
        """The function execution time (in seconds) after which Lambda terminates the function.

        Because the execution time affects cost, set this value
        based on the function's expected execution time.

        default
        :default: Duration.seconds(3)

        stability
        :stability: experimental
        """
        return self._values.get('timeout')

    @builtins.property
    def tracing(self) -> typing.Optional["Tracing"]:
        """Enable AWS X-Ray Tracing for Lambda Function.

        default
        :default: Tracing.Disabled

        stability
        :stability: experimental
        """
        return self._values.get('tracing')

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_3795853f]:
        """VPC network to place Lambda network interfaces.

        Specify this if the Lambda function needs to access resources in a VPC.

        default
        :default: - Function is not placed within a VPC.

        stability
        :stability: experimental
        """
        return self._values.get('vpc')

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_SubnetSelection_36a13cd6]:
        """Where to place the network interfaces within the VPC.

        Only used if 'vpc' is supplied. Note: internet access for Lambdas
        requires a NAT gateway, so picking Public subnets is not allowed.

        default
        :default: - the Vpc default strategy if not specified

        stability
        :stability: experimental
        """
        return self._values.get('vpc_subnets')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'FunctionOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.FunctionProps", jsii_struct_bases=[FunctionOptions], name_mapping={'max_event_age': 'maxEventAge', 'on_failure': 'onFailure', 'on_success': 'onSuccess', 'retry_attempts': 'retryAttempts', 'allow_all_outbound': 'allowAllOutbound', 'current_version_options': 'currentVersionOptions', 'dead_letter_queue': 'deadLetterQueue', 'dead_letter_queue_enabled': 'deadLetterQueueEnabled', 'description': 'description', 'environment': 'environment', 'events': 'events', 'function_name': 'functionName', 'initial_policy': 'initialPolicy', 'layers': 'layers', 'log_retention': 'logRetention', 'log_retention_retry_options': 'logRetentionRetryOptions', 'log_retention_role': 'logRetentionRole', 'memory_size': 'memorySize', 'reserved_concurrent_executions': 'reservedConcurrentExecutions', 'role': 'role', 'security_group': 'securityGroup', 'security_groups': 'securityGroups', 'timeout': 'timeout', 'tracing': 'tracing', 'vpc': 'vpc', 'vpc_subnets': 'vpcSubnets', 'code': 'code', 'handler': 'handler', 'runtime': 'runtime'})
class FunctionProps(FunctionOptions):
    def __init__(self, *, max_event_age: typing.Optional[_Duration_5170c158]=None, on_failure: typing.Optional["IDestination"]=None, on_success: typing.Optional["IDestination"]=None, retry_attempts: typing.Optional[jsii.Number]=None, allow_all_outbound: typing.Optional[bool]=None, current_version_options: typing.Optional["VersionOptions"]=None, dead_letter_queue: typing.Optional[_IQueue_b743f559]=None, dead_letter_queue_enabled: typing.Optional[bool]=None, description: typing.Optional[str]=None, environment: typing.Optional[typing.Mapping[str, str]]=None, events: typing.Optional[typing.List["IEventSource"]]=None, function_name: typing.Optional[str]=None, initial_policy: typing.Optional[typing.List[_PolicyStatement_f75dc775]]=None, layers: typing.Optional[typing.List["ILayerVersion"]]=None, log_retention: typing.Optional[_RetentionDays_bdc7ad1f]=None, log_retention_retry_options: typing.Optional["LogRetentionRetryOptions"]=None, log_retention_role: typing.Optional[_IRole_e69bbae4]=None, memory_size: typing.Optional[jsii.Number]=None, reserved_concurrent_executions: typing.Optional[jsii.Number]=None, role: typing.Optional[_IRole_e69bbae4]=None, security_group: typing.Optional[_ISecurityGroup_d72ab8e8]=None, security_groups: typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]]=None, timeout: typing.Optional[_Duration_5170c158]=None, tracing: typing.Optional["Tracing"]=None, vpc: typing.Optional[_IVpc_3795853f]=None, vpc_subnets: typing.Optional[_SubnetSelection_36a13cd6]=None, code: "Code", handler: str, runtime: "Runtime") -> None:
        """
        :param max_event_age: The maximum age of a request that Lambda sends to a function for processing. Minimum: 60 seconds Maximum: 6 hours Default: Duration.hours(6)
        :param on_failure: The destination for failed invocations. Default: - no destination
        :param on_success: The destination for successful invocations. Default: - no destination
        :param retry_attempts: The maximum number of times to retry when the function returns an error. Minimum: 0 Maximum: 2 Default: 2
        :param allow_all_outbound: Whether to allow the Lambda to send all network traffic. If set to false, you must individually add traffic rules to allow the Lambda to connect to network targets. Default: true
        :param current_version_options: Options for the ``lambda.Version`` resource automatically created by the ``fn.currentVersion`` method. Default: - default options as described in ``VersionOptions``
        :param dead_letter_queue: The SQS queue to use if DLQ is enabled. Default: - SQS queue with 14 day retention period if ``deadLetterQueueEnabled`` is ``true``
        :param dead_letter_queue_enabled: Enabled DLQ. If ``deadLetterQueue`` is undefined, an SQS queue with default options will be defined for your Function. Default: - false unless ``deadLetterQueue`` is set, which implies DLQ is enabled.
        :param description: A description of the function. Default: - No description.
        :param environment: Key-value pairs that Lambda caches and makes available for your Lambda functions. Use environment variables to apply configuration changes, such as test and production environment configurations, without changing your Lambda function source code. Default: - No environment variables.
        :param events: Event sources for this function. You can also add event sources using ``addEventSource``. Default: - No event sources.
        :param function_name: A name for the function. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the function's name. For more information, see Name Type.
        :param initial_policy: Initial policy statements to add to the created Lambda Role. You can call ``addToRolePolicy`` to the created lambda to add statements post creation. Default: - No policy statements are added to the created Lambda role.
        :param layers: A list of layers to add to the function's execution environment. You can configure your Lambda function to pull in additional code during initialization in the form of layers. Layers are packages of libraries or other dependencies that can be used by mulitple functions. Default: - No layers.
        :param log_retention: The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.INFINITE
        :param log_retention_retry_options: When log retention is specified, a custom resource attempts to create the CloudWatch log group. These options control the retry policy when interacting with CloudWatch APIs. Default: - Default AWS SDK retry options.
        :param log_retention_role: The IAM role for the Lambda function associated with the custom resource that sets the retention policy. Default: - A new role is created.
        :param memory_size: The amount of memory, in MB, that is allocated to your Lambda function. Lambda uses this value to proportionally allocate the amount of CPU power. For more information, see Resource Model in the AWS Lambda Developer Guide. Default: 128
        :param reserved_concurrent_executions: The maximum of concurrent executions you want to reserve for the function. Default: - No specific limit - account limit.
        :param role: Lambda execution role. This is the role that will be assumed by the function upon execution. It controls the permissions that the function will have. The Role must be assumable by the 'lambda.amazonaws.com' service principal. The default Role automatically has permissions granted for Lambda execution. If you provide a Role, you must add the relevant AWS managed policies yourself. The relevant managed policies are "service-role/AWSLambdaBasicExecutionRole" and "service-role/AWSLambdaVPCAccessExecutionRole". Default: - A unique role will be generated for this lambda function. Both supplied and generated roles can always be changed by calling ``addToRolePolicy``.
        :param security_group: What security group to associate with the Lambda's network interfaces. This property is being deprecated, consider using securityGroups instead. Only used if 'vpc' is supplied. Use securityGroups property instead. Function constructor will throw an error if both are specified. Default: - If the function is placed within a VPC and a security group is not specified, either by this or securityGroups prop, a dedicated security group will be created for this function.
        :param security_groups: The list of security groups to associate with the Lambda's network interfaces. Only used if 'vpc' is supplied. Default: - If the function is placed within a VPC and a security group is not specified, either by this or securityGroup prop, a dedicated security group will be created for this function.
        :param timeout: The function execution time (in seconds) after which Lambda terminates the function. Because the execution time affects cost, set this value based on the function's expected execution time. Default: Duration.seconds(3)
        :param tracing: Enable AWS X-Ray Tracing for Lambda Function. Default: Tracing.Disabled
        :param vpc: VPC network to place Lambda network interfaces. Specify this if the Lambda function needs to access resources in a VPC. Default: - Function is not placed within a VPC.
        :param vpc_subnets: Where to place the network interfaces within the VPC. Only used if 'vpc' is supplied. Note: internet access for Lambdas requires a NAT gateway, so picking Public subnets is not allowed. Default: - the Vpc default strategy if not specified
        :param code: The source code of your Lambda function. You can point to a file in an Amazon Simple Storage Service (Amazon S3) bucket or specify your source code as inline text.
        :param handler: The name of the method within your code that Lambda calls to execute your function. The format includes the file name. It can also include namespaces and other qualifiers, depending on the runtime. For more information, see https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-features.html#gettingstarted-features-programmingmodel. NOTE: If you specify your source code as inline text by specifying the ZipFile property within the Code property, specify index.function_name as the handler.
        :param runtime: The runtime environment for the Lambda function that you are uploading. For valid values, see the Runtime property in the AWS Lambda Developer Guide.

        stability
        :stability: experimental
        """
        if isinstance(current_version_options, dict): current_version_options = VersionOptions(**current_version_options)
        if isinstance(log_retention_retry_options, dict): log_retention_retry_options = LogRetentionRetryOptions(**log_retention_retry_options)
        if isinstance(vpc_subnets, dict): vpc_subnets = _SubnetSelection_36a13cd6(**vpc_subnets)
        self._values = {
            'code': code,
            'handler': handler,
            'runtime': runtime,
        }
        if max_event_age is not None: self._values["max_event_age"] = max_event_age
        if on_failure is not None: self._values["on_failure"] = on_failure
        if on_success is not None: self._values["on_success"] = on_success
        if retry_attempts is not None: self._values["retry_attempts"] = retry_attempts
        if allow_all_outbound is not None: self._values["allow_all_outbound"] = allow_all_outbound
        if current_version_options is not None: self._values["current_version_options"] = current_version_options
        if dead_letter_queue is not None: self._values["dead_letter_queue"] = dead_letter_queue
        if dead_letter_queue_enabled is not None: self._values["dead_letter_queue_enabled"] = dead_letter_queue_enabled
        if description is not None: self._values["description"] = description
        if environment is not None: self._values["environment"] = environment
        if events is not None: self._values["events"] = events
        if function_name is not None: self._values["function_name"] = function_name
        if initial_policy is not None: self._values["initial_policy"] = initial_policy
        if layers is not None: self._values["layers"] = layers
        if log_retention is not None: self._values["log_retention"] = log_retention
        if log_retention_retry_options is not None: self._values["log_retention_retry_options"] = log_retention_retry_options
        if log_retention_role is not None: self._values["log_retention_role"] = log_retention_role
        if memory_size is not None: self._values["memory_size"] = memory_size
        if reserved_concurrent_executions is not None: self._values["reserved_concurrent_executions"] = reserved_concurrent_executions
        if role is not None: self._values["role"] = role
        if security_group is not None: self._values["security_group"] = security_group
        if security_groups is not None: self._values["security_groups"] = security_groups
        if timeout is not None: self._values["timeout"] = timeout
        if tracing is not None: self._values["tracing"] = tracing
        if vpc is not None: self._values["vpc"] = vpc
        if vpc_subnets is not None: self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def max_event_age(self) -> typing.Optional[_Duration_5170c158]:
        """The maximum age of a request that Lambda sends to a function for processing.

        Minimum: 60 seconds
        Maximum: 6 hours

        default
        :default: Duration.hours(6)

        stability
        :stability: experimental
        """
        return self._values.get('max_event_age')

    @builtins.property
    def on_failure(self) -> typing.Optional["IDestination"]:
        """The destination for failed invocations.

        default
        :default: - no destination

        stability
        :stability: experimental
        """
        return self._values.get('on_failure')

    @builtins.property
    def on_success(self) -> typing.Optional["IDestination"]:
        """The destination for successful invocations.

        default
        :default: - no destination

        stability
        :stability: experimental
        """
        return self._values.get('on_success')

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        """The maximum number of times to retry when the function returns an error.

        Minimum: 0
        Maximum: 2

        default
        :default: 2

        stability
        :stability: experimental
        """
        return self._values.get('retry_attempts')

    @builtins.property
    def allow_all_outbound(self) -> typing.Optional[bool]:
        """Whether to allow the Lambda to send all network traffic.

        If set to false, you must individually add traffic rules to allow the
        Lambda to connect to network targets.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('allow_all_outbound')

    @builtins.property
    def current_version_options(self) -> typing.Optional["VersionOptions"]:
        """Options for the ``lambda.Version`` resource automatically created by the ``fn.currentVersion`` method.

        default
        :default: - default options as described in ``VersionOptions``

        stability
        :stability: experimental
        """
        return self._values.get('current_version_options')

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_IQueue_b743f559]:
        """The SQS queue to use if DLQ is enabled.

        default
        :default: - SQS queue with 14 day retention period if ``deadLetterQueueEnabled`` is ``true``

        stability
        :stability: experimental
        """
        return self._values.get('dead_letter_queue')

    @builtins.property
    def dead_letter_queue_enabled(self) -> typing.Optional[bool]:
        """Enabled DLQ.

        If ``deadLetterQueue`` is undefined,
        an SQS queue with default options will be defined for your Function.

        default
        :default: - false unless ``deadLetterQueue`` is set, which implies DLQ is enabled.

        stability
        :stability: experimental
        """
        return self._values.get('dead_letter_queue_enabled')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """A description of the function.

        default
        :default: - No description.

        stability
        :stability: experimental
        """
        return self._values.get('description')

    @builtins.property
    def environment(self) -> typing.Optional[typing.Mapping[str, str]]:
        """Key-value pairs that Lambda caches and makes available for your Lambda functions.

        Use environment variables to apply configuration changes, such
        as test and production environment configurations, without changing your
        Lambda function source code.

        default
        :default: - No environment variables.

        stability
        :stability: experimental
        """
        return self._values.get('environment')

    @builtins.property
    def events(self) -> typing.Optional[typing.List["IEventSource"]]:
        """Event sources for this function.

        You can also add event sources using ``addEventSource``.

        default
        :default: - No event sources.

        stability
        :stability: experimental
        """
        return self._values.get('events')

    @builtins.property
    def function_name(self) -> typing.Optional[str]:
        """A name for the function.

        default
        :default:

        - AWS CloudFormation generates a unique physical ID and uses that
          ID for the function's name. For more information, see Name Type.

        stability
        :stability: experimental
        """
        return self._values.get('function_name')

    @builtins.property
    def initial_policy(self) -> typing.Optional[typing.List[_PolicyStatement_f75dc775]]:
        """Initial policy statements to add to the created Lambda Role.

        You can call ``addToRolePolicy`` to the created lambda to add statements post creation.

        default
        :default: - No policy statements are added to the created Lambda role.

        stability
        :stability: experimental
        """
        return self._values.get('initial_policy')

    @builtins.property
    def layers(self) -> typing.Optional[typing.List["ILayerVersion"]]:
        """A list of layers to add to the function's execution environment.

        You can configure your Lambda function to pull in
        additional code during initialization in the form of layers. Layers are packages of libraries or other dependencies
        that can be used by mulitple functions.

        default
        :default: - No layers.

        stability
        :stability: experimental
        """
        return self._values.get('layers')

    @builtins.property
    def log_retention(self) -> typing.Optional[_RetentionDays_bdc7ad1f]:
        """The number of days log events are kept in CloudWatch Logs.

        When updating
        this property, unsetting it doesn't remove the log retention policy. To
        remove the retention policy, set the value to ``INFINITE``.

        default
        :default: logs.RetentionDays.INFINITE

        stability
        :stability: experimental
        """
        return self._values.get('log_retention')

    @builtins.property
    def log_retention_retry_options(self) -> typing.Optional["LogRetentionRetryOptions"]:
        """When log retention is specified, a custom resource attempts to create the CloudWatch log group.

        These options control the retry policy when interacting with CloudWatch APIs.

        default
        :default: - Default AWS SDK retry options.

        stability
        :stability: experimental
        """
        return self._values.get('log_retention_retry_options')

    @builtins.property
    def log_retention_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The IAM role for the Lambda function associated with the custom resource that sets the retention policy.

        default
        :default: - A new role is created.

        stability
        :stability: experimental
        """
        return self._values.get('log_retention_role')

    @builtins.property
    def memory_size(self) -> typing.Optional[jsii.Number]:
        """The amount of memory, in MB, that is allocated to your Lambda function.

        Lambda uses this value to proportionally allocate the amount of CPU
        power. For more information, see Resource Model in the AWS Lambda
        Developer Guide.

        default
        :default: 128

        stability
        :stability: experimental
        """
        return self._values.get('memory_size')

    @builtins.property
    def reserved_concurrent_executions(self) -> typing.Optional[jsii.Number]:
        """The maximum of concurrent executions you want to reserve for the function.

        default
        :default: - No specific limit - account limit.

        see
        :see: https://docs.aws.amazon.com/lambda/latest/dg/concurrent-executions.html
        stability
        :stability: experimental
        """
        return self._values.get('reserved_concurrent_executions')

    @builtins.property
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """Lambda execution role.

        This is the role that will be assumed by the function upon execution.
        It controls the permissions that the function will have. The Role must
        be assumable by the 'lambda.amazonaws.com' service principal.

        The default Role automatically has permissions granted for Lambda execution. If you
        provide a Role, you must add the relevant AWS managed policies yourself.

        The relevant managed policies are "service-role/AWSLambdaBasicExecutionRole" and
        "service-role/AWSLambdaVPCAccessExecutionRole".

        default
        :default:

        - A unique role will be generated for this lambda function.
          Both supplied and generated roles can always be changed by calling ``addToRolePolicy``.

        stability
        :stability: experimental
        """
        return self._values.get('role')

    @builtins.property
    def security_group(self) -> typing.Optional[_ISecurityGroup_d72ab8e8]:
        """What security group to associate with the Lambda's network interfaces. This property is being deprecated, consider using securityGroups instead.

        Only used if 'vpc' is supplied.

        Use securityGroups property instead.
        Function constructor will throw an error if both are specified.

        default
        :default:

        - If the function is placed within a VPC and a security group is
          not specified, either by this or securityGroups prop, a dedicated security
          group will be created for this function.

        deprecated
        :deprecated: - This property is deprecated, use securityGroups instead

        stability
        :stability: deprecated
        """
        return self._values.get('security_group')

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]]:
        """The list of security groups to associate with the Lambda's network interfaces.

        Only used if 'vpc' is supplied.

        default
        :default:

        - If the function is placed within a VPC and a security group is
          not specified, either by this or securityGroup prop, a dedicated security
          group will be created for this function.

        stability
        :stability: experimental
        """
        return self._values.get('security_groups')

    @builtins.property
    def timeout(self) -> typing.Optional[_Duration_5170c158]:
        """The function execution time (in seconds) after which Lambda terminates the function.

        Because the execution time affects cost, set this value
        based on the function's expected execution time.

        default
        :default: Duration.seconds(3)

        stability
        :stability: experimental
        """
        return self._values.get('timeout')

    @builtins.property
    def tracing(self) -> typing.Optional["Tracing"]:
        """Enable AWS X-Ray Tracing for Lambda Function.

        default
        :default: Tracing.Disabled

        stability
        :stability: experimental
        """
        return self._values.get('tracing')

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_3795853f]:
        """VPC network to place Lambda network interfaces.

        Specify this if the Lambda function needs to access resources in a VPC.

        default
        :default: - Function is not placed within a VPC.

        stability
        :stability: experimental
        """
        return self._values.get('vpc')

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_SubnetSelection_36a13cd6]:
        """Where to place the network interfaces within the VPC.

        Only used if 'vpc' is supplied. Note: internet access for Lambdas
        requires a NAT gateway, so picking Public subnets is not allowed.

        default
        :default: - the Vpc default strategy if not specified

        stability
        :stability: experimental
        """
        return self._values.get('vpc_subnets')

    @builtins.property
    def code(self) -> "Code":
        """The source code of your Lambda function.

        You can point to a file in an
        Amazon Simple Storage Service (Amazon S3) bucket or specify your source
        code as inline text.

        stability
        :stability: experimental
        """
        return self._values.get('code')

    @builtins.property
    def handler(self) -> str:
        """The name of the method within your code that Lambda calls to execute your function.

        The format includes the file name. It can also include
        namespaces and other qualifiers, depending on the runtime.
        For more information, see https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-features.html#gettingstarted-features-programmingmodel.

        NOTE: If you specify your source code as inline text by specifying the
        ZipFile property within the Code property, specify index.function_name as
        the handler.

        stability
        :stability: experimental
        """
        return self._values.get('handler')

    @builtins.property
    def runtime(self) -> "Runtime":
        """The runtime environment for the Lambda function that you are uploading.

        For valid values, see the Runtime property in the AWS Lambda Developer
        Guide.

        stability
        :stability: experimental
        """
        return self._values.get('runtime')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'FunctionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.interface(jsii_type="monocdk-experiment.aws_lambda.IDestination")
class IDestination(jsii.compat.Protocol):
    """A Lambda destination.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IDestinationProxy

    @jsii.member(jsii_name="bind")
    def bind(self, scope: _Construct_f50a3f53, fn: "IFunction", *, type: "DestinationType") -> "DestinationConfig":
        """Binds this destination to the Lambda function.

        :param scope: -
        :param fn: -
        :param type: The destination type.

        stability
        :stability: experimental
        """
        ...


class _IDestinationProxy():
    """A Lambda destination.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_lambda.IDestination"
    @jsii.member(jsii_name="bind")
    def bind(self, scope: _Construct_f50a3f53, fn: "IFunction", *, type: "DestinationType") -> "DestinationConfig":
        """Binds this destination to the Lambda function.

        :param scope: -
        :param fn: -
        :param type: The destination type.

        stability
        :stability: experimental
        """
        options = DestinationOptions(type=type)

        return jsii.invoke(self, "bind", [scope, fn, options])


@jsii.interface(jsii_type="monocdk-experiment.aws_lambda.IEventSource")
class IEventSource(jsii.compat.Protocol):
    """An abstract class which represents an AWS Lambda event source.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IEventSourceProxy

    @jsii.member(jsii_name="bind")
    def bind(self, target: "IFunction") -> None:
        """Called by ``lambda.addEventSource`` to allow the event source to bind to this function.

        :param target: That lambda function to bind to.

        stability
        :stability: experimental
        """
        ...


class _IEventSourceProxy():
    """An abstract class which represents an AWS Lambda event source.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_lambda.IEventSource"
    @jsii.member(jsii_name="bind")
    def bind(self, target: "IFunction") -> None:
        """Called by ``lambda.addEventSource`` to allow the event source to bind to this function.

        :param target: That lambda function to bind to.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [target])


@jsii.interface(jsii_type="monocdk-experiment.aws_lambda.IEventSourceDlq")
class IEventSourceDlq(jsii.compat.Protocol):
    """A DLQ for an event source.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IEventSourceDlqProxy

    @jsii.member(jsii_name="bind")
    def bind(self, target: "IEventSourceMapping", target_handler: "IFunction") -> "DlqDestinationConfig":
        """Returns the DLQ destination config of the DLQ.

        :param target: -
        :param target_handler: -

        stability
        :stability: experimental
        """
        ...


class _IEventSourceDlqProxy():
    """A DLQ for an event source.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_lambda.IEventSourceDlq"
    @jsii.member(jsii_name="bind")
    def bind(self, target: "IEventSourceMapping", target_handler: "IFunction") -> "DlqDestinationConfig":
        """Returns the DLQ destination config of the DLQ.

        :param target: -
        :param target_handler: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [target, target_handler])


@jsii.interface(jsii_type="monocdk-experiment.aws_lambda.IEventSourceMapping")
class IEventSourceMapping(_IResource_72f7ee7e, jsii.compat.Protocol):
    """Represents an event source mapping for a lambda function.

    see
    :see: https://docs.aws.amazon.com/lambda/latest/dg/invocation-eventsourcemapping.html
    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IEventSourceMappingProxy

    @builtins.property
    @jsii.member(jsii_name="eventSourceMappingId")
    def event_source_mapping_id(self) -> str:
        """The identifier for this EventSourceMapping.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...


class _IEventSourceMappingProxy(jsii.proxy_for(_IResource_72f7ee7e)):
    """Represents an event source mapping for a lambda function.

    see
    :see: https://docs.aws.amazon.com/lambda/latest/dg/invocation-eventsourcemapping.html
    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_lambda.IEventSourceMapping"
    @builtins.property
    @jsii.member(jsii_name="eventSourceMappingId")
    def event_source_mapping_id(self) -> str:
        """The identifier for this EventSourceMapping.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "eventSourceMappingId")


@jsii.interface(jsii_type="monocdk-experiment.aws_lambda.IFunction")
class IFunction(_IResource_72f7ee7e, _IConnectable_a587039f, _IGrantable_0fcfc53a, jsii.compat.Protocol):
    """
    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IFunctionProxy

    @builtins.property
    @jsii.member(jsii_name="functionArn")
    def function_arn(self) -> str:
        """The ARN fo the function.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="functionName")
    def function_name(self) -> str:
        """The name of the function.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="isBoundToVpc")
    def is_bound_to_vpc(self) -> bool:
        """Whether or not this Lambda function was bound to a VPC.

        If this is is ``false``, trying to access the ``connections`` object will fail.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="latestVersion")
    def latest_version(self) -> "IVersion":
        """The ``$LATEST`` version of this function.

        Note that this is reference to a non-specific AWS Lambda version, which
        means the function this version refers to can return different results in
        different invocations.

        To obtain a reference to an explicit version which references the current
        function configuration, use ``lambdaFunction.currentVersion`` instead.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="permissionsNode")
    def permissions_node(self) -> _ConstructNode_6884f5de:
        """The construct node where permissions are attached.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The IAM role associated with this function.

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="addEventSource")
    def add_event_source(self, source: "IEventSource") -> None:
        """
        :param source: -

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="addEventSourceMapping")
    def add_event_source_mapping(self, id: str, *, event_source_arn: str, batch_size: typing.Optional[jsii.Number]=None, bisect_batch_on_error: typing.Optional[bool]=None, enabled: typing.Optional[bool]=None, max_batching_window: typing.Optional[_Duration_5170c158]=None, max_record_age: typing.Optional[_Duration_5170c158]=None, on_failure: typing.Optional["IEventSourceDlq"]=None, parallelization_factor: typing.Optional[jsii.Number]=None, retry_attempts: typing.Optional[jsii.Number]=None, starting_position: typing.Optional["StartingPosition"]=None) -> "EventSourceMapping":
        """Adds an event source that maps to this AWS Lambda function.

        :param id: construct ID.
        :param event_source_arn: The Amazon Resource Name (ARN) of the event source. Any record added to this stream can invoke the Lambda function.
        :param batch_size: The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: Minimum value of 1. Maximum value of 10000. Default: - Amazon Kinesis and Amazon DynamoDB is 100 records. Both the default and maximum for Amazon SQS are 10 messages.
        :param bisect_batch_on_error: If the function returns an error, split the batch in two and retry. Default: false
        :param enabled: Set to false to disable the event source upon creation. Default: true
        :param max_batching_window: The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5) Default: Duration.seconds(0)
        :param max_record_age: The maximum age of a record that Lambda sends to a function for processing. Valid Range: - Minimum value of 60 seconds - Maximum value of 7 days Default: Duration.days(7)
        :param on_failure: An Amazon SQS queue or Amazon SNS topic destination for discarded records. Default: discarded records are ignored
        :param parallelization_factor: The number of batches to process from each shard concurrently. Valid Range: - Minimum value of 1 - Maximum value of 10 Default: 1
        :param retry_attempts: The maximum number of times to retry when the function returns an error. Valid Range: - Minimum value of 0 - Maximum value of 10000 Default: 10000
        :param starting_position: The position in the DynamoDB or Kinesis stream where AWS Lambda should start reading. Default: - Required for Amazon Kinesis and Amazon DynamoDB Streams sources.

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="addPermission")
    def add_permission(self, id: str, *, principal: _IPrincipal_97126874, action: typing.Optional[str]=None, event_source_token: typing.Optional[str]=None, scope: typing.Optional[_Construct_f50a3f53]=None, source_account: typing.Optional[str]=None, source_arn: typing.Optional[str]=None) -> None:
        """Adds a permission to the Lambda resource policy.

        :param id: The id ƒor the permission construct.
        :param principal: The entity for which you are granting permission to invoke the Lambda function. This entity can be any valid AWS service principal, such as s3.amazonaws.com or sns.amazonaws.com, or, if you are granting cross-account permission, an AWS account ID. For example, you might want to allow a custom application in another AWS account to push events to Lambda by invoking your function. The principal can be either an AccountPrincipal or a ServicePrincipal.
        :param action: The Lambda actions that you want to allow in this statement. For example, you can specify lambda:CreateFunction to specify a certain action, or use a wildcard (``lambda:*``) to grant permission to all Lambda actions. For a list of actions, see Actions and Condition Context Keys for AWS Lambda in the IAM User Guide. Default: 'lambda:InvokeFunction'
        :param event_source_token: A unique token that must be supplied by the principal invoking the function. Default: The caller would not need to present a token.
        :param scope: The scope to which the permission constructs be attached. The default is the Lambda function construct itself, but this would need to be different in cases such as cross-stack references where the Permissions would need to sit closer to the consumer of this permission (i.e., the caller). Default: - The instance of lambda.IFunction
        :param source_account: The AWS account ID (without hyphens) of the source owner. For example, if you specify an S3 bucket in the SourceArn property, this value is the bucket owner's account ID. You can use this property to ensure that all source principals are owned by a specific account.
        :param source_arn: The ARN of a resource that is invoking your function. When granting Amazon Simple Storage Service (Amazon S3) permission to invoke your function, specify this property with the bucket ARN as its value. This ensures that events generated only from the specified bucket, not just any bucket from any AWS account that creates a mapping to your function, can invoke the function.

        see
        :see: Permission for details.
        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="addToRolePolicy")
    def add_to_role_policy(self, statement: _PolicyStatement_f75dc775) -> None:
        """Adds a statement to the IAM role assumed by the instance.

        :param statement: -

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="configureAsyncInvoke")
    def configure_async_invoke(self, *, max_event_age: typing.Optional[_Duration_5170c158]=None, on_failure: typing.Optional["IDestination"]=None, on_success: typing.Optional["IDestination"]=None, retry_attempts: typing.Optional[jsii.Number]=None) -> None:
        """Configures options for asynchronous invocation.

        :param max_event_age: The maximum age of a request that Lambda sends to a function for processing. Minimum: 60 seconds Maximum: 6 hours Default: Duration.hours(6)
        :param on_failure: The destination for failed invocations. Default: - no destination
        :param on_success: The destination for successful invocations. Default: - no destination
        :param retry_attempts: The maximum number of times to retry when the function returns an error. Minimum: 0 Maximum: 2 Default: 2

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="grantInvoke")
    def grant_invoke(self, identity: _IGrantable_0fcfc53a) -> _Grant_96af6d2d:
        """Grant the given identity permissions to invoke this Lambda.

        :param identity: -

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="metric")
    def metric(self, metric_name: str, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[_Duration_5170c158]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[_Unit_e1b74f3c]=None) -> _Metric_53e89548:
        """Return the given named metric for this Lambda Return the given named metric for this Function.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="metricDuration")
    def metric_duration(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[_Duration_5170c158]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[_Unit_e1b74f3c]=None) -> _Metric_53e89548:
        """Metric for the Duration of this Lambda How long execution of this Lambda takes.

        Average over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: average over 5 minutes

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="metricErrors")
    def metric_errors(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[_Duration_5170c158]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[_Unit_e1b74f3c]=None) -> _Metric_53e89548:
        """How many invocations of this Lambda fail.

        Sum over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="metricInvocations")
    def metric_invocations(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[_Duration_5170c158]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[_Unit_e1b74f3c]=None) -> _Metric_53e89548:
        """Metric for the number of invocations of this Lambda How often this Lambda is invoked.

        Sum over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over 5 minutes

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="metricThrottles")
    def metric_throttles(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[_Duration_5170c158]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[_Unit_e1b74f3c]=None) -> _Metric_53e89548:
        """Metric for the number of throttled invocations of this Lambda How often this Lambda is throttled.

        Sum over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over 5 minutes

        stability
        :stability: experimental
        """
        ...


class _IFunctionProxy(jsii.proxy_for(_IResource_72f7ee7e), jsii.proxy_for(_IConnectable_a587039f), jsii.proxy_for(_IGrantable_0fcfc53a)):
    """
    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_lambda.IFunction"
    @builtins.property
    @jsii.member(jsii_name="functionArn")
    def function_arn(self) -> str:
        """The ARN fo the function.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "functionArn")

    @builtins.property
    @jsii.member(jsii_name="functionName")
    def function_name(self) -> str:
        """The name of the function.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "functionName")

    @builtins.property
    @jsii.member(jsii_name="isBoundToVpc")
    def is_bound_to_vpc(self) -> bool:
        """Whether or not this Lambda function was bound to a VPC.

        If this is is ``false``, trying to access the ``connections`` object will fail.

        stability
        :stability: experimental
        """
        return jsii.get(self, "isBoundToVpc")

    @builtins.property
    @jsii.member(jsii_name="latestVersion")
    def latest_version(self) -> "IVersion":
        """The ``$LATEST`` version of this function.

        Note that this is reference to a non-specific AWS Lambda version, which
        means the function this version refers to can return different results in
        different invocations.

        To obtain a reference to an explicit version which references the current
        function configuration, use ``lambdaFunction.currentVersion`` instead.

        stability
        :stability: experimental
        """
        return jsii.get(self, "latestVersion")

    @builtins.property
    @jsii.member(jsii_name="permissionsNode")
    def permissions_node(self) -> _ConstructNode_6884f5de:
        """The construct node where permissions are attached.

        stability
        :stability: experimental
        """
        return jsii.get(self, "permissionsNode")

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The IAM role associated with this function.

        stability
        :stability: experimental
        """
        return jsii.get(self, "role")

    @jsii.member(jsii_name="addEventSource")
    def add_event_source(self, source: "IEventSource") -> None:
        """
        :param source: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addEventSource", [source])

    @jsii.member(jsii_name="addEventSourceMapping")
    def add_event_source_mapping(self, id: str, *, event_source_arn: str, batch_size: typing.Optional[jsii.Number]=None, bisect_batch_on_error: typing.Optional[bool]=None, enabled: typing.Optional[bool]=None, max_batching_window: typing.Optional[_Duration_5170c158]=None, max_record_age: typing.Optional[_Duration_5170c158]=None, on_failure: typing.Optional["IEventSourceDlq"]=None, parallelization_factor: typing.Optional[jsii.Number]=None, retry_attempts: typing.Optional[jsii.Number]=None, starting_position: typing.Optional["StartingPosition"]=None) -> "EventSourceMapping":
        """Adds an event source that maps to this AWS Lambda function.

        :param id: construct ID.
        :param event_source_arn: The Amazon Resource Name (ARN) of the event source. Any record added to this stream can invoke the Lambda function.
        :param batch_size: The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: Minimum value of 1. Maximum value of 10000. Default: - Amazon Kinesis and Amazon DynamoDB is 100 records. Both the default and maximum for Amazon SQS are 10 messages.
        :param bisect_batch_on_error: If the function returns an error, split the batch in two and retry. Default: false
        :param enabled: Set to false to disable the event source upon creation. Default: true
        :param max_batching_window: The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5) Default: Duration.seconds(0)
        :param max_record_age: The maximum age of a record that Lambda sends to a function for processing. Valid Range: - Minimum value of 60 seconds - Maximum value of 7 days Default: Duration.days(7)
        :param on_failure: An Amazon SQS queue or Amazon SNS topic destination for discarded records. Default: discarded records are ignored
        :param parallelization_factor: The number of batches to process from each shard concurrently. Valid Range: - Minimum value of 1 - Maximum value of 10 Default: 1
        :param retry_attempts: The maximum number of times to retry when the function returns an error. Valid Range: - Minimum value of 0 - Maximum value of 10000 Default: 10000
        :param starting_position: The position in the DynamoDB or Kinesis stream where AWS Lambda should start reading. Default: - Required for Amazon Kinesis and Amazon DynamoDB Streams sources.

        stability
        :stability: experimental
        """
        options = EventSourceMappingOptions(event_source_arn=event_source_arn, batch_size=batch_size, bisect_batch_on_error=bisect_batch_on_error, enabled=enabled, max_batching_window=max_batching_window, max_record_age=max_record_age, on_failure=on_failure, parallelization_factor=parallelization_factor, retry_attempts=retry_attempts, starting_position=starting_position)

        return jsii.invoke(self, "addEventSourceMapping", [id, options])

    @jsii.member(jsii_name="addPermission")
    def add_permission(self, id: str, *, principal: _IPrincipal_97126874, action: typing.Optional[str]=None, event_source_token: typing.Optional[str]=None, scope: typing.Optional[_Construct_f50a3f53]=None, source_account: typing.Optional[str]=None, source_arn: typing.Optional[str]=None) -> None:
        """Adds a permission to the Lambda resource policy.

        :param id: The id ƒor the permission construct.
        :param principal: The entity for which you are granting permission to invoke the Lambda function. This entity can be any valid AWS service principal, such as s3.amazonaws.com or sns.amazonaws.com, or, if you are granting cross-account permission, an AWS account ID. For example, you might want to allow a custom application in another AWS account to push events to Lambda by invoking your function. The principal can be either an AccountPrincipal or a ServicePrincipal.
        :param action: The Lambda actions that you want to allow in this statement. For example, you can specify lambda:CreateFunction to specify a certain action, or use a wildcard (``lambda:*``) to grant permission to all Lambda actions. For a list of actions, see Actions and Condition Context Keys for AWS Lambda in the IAM User Guide. Default: 'lambda:InvokeFunction'
        :param event_source_token: A unique token that must be supplied by the principal invoking the function. Default: The caller would not need to present a token.
        :param scope: The scope to which the permission constructs be attached. The default is the Lambda function construct itself, but this would need to be different in cases such as cross-stack references where the Permissions would need to sit closer to the consumer of this permission (i.e., the caller). Default: - The instance of lambda.IFunction
        :param source_account: The AWS account ID (without hyphens) of the source owner. For example, if you specify an S3 bucket in the SourceArn property, this value is the bucket owner's account ID. You can use this property to ensure that all source principals are owned by a specific account.
        :param source_arn: The ARN of a resource that is invoking your function. When granting Amazon Simple Storage Service (Amazon S3) permission to invoke your function, specify this property with the bucket ARN as its value. This ensures that events generated only from the specified bucket, not just any bucket from any AWS account that creates a mapping to your function, can invoke the function.

        see
        :see: Permission for details.
        stability
        :stability: experimental
        """
        permission = Permission(principal=principal, action=action, event_source_token=event_source_token, scope=scope, source_account=source_account, source_arn=source_arn)

        return jsii.invoke(self, "addPermission", [id, permission])

    @jsii.member(jsii_name="addToRolePolicy")
    def add_to_role_policy(self, statement: _PolicyStatement_f75dc775) -> None:
        """Adds a statement to the IAM role assumed by the instance.

        :param statement: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addToRolePolicy", [statement])

    @jsii.member(jsii_name="configureAsyncInvoke")
    def configure_async_invoke(self, *, max_event_age: typing.Optional[_Duration_5170c158]=None, on_failure: typing.Optional["IDestination"]=None, on_success: typing.Optional["IDestination"]=None, retry_attempts: typing.Optional[jsii.Number]=None) -> None:
        """Configures options for asynchronous invocation.

        :param max_event_age: The maximum age of a request that Lambda sends to a function for processing. Minimum: 60 seconds Maximum: 6 hours Default: Duration.hours(6)
        :param on_failure: The destination for failed invocations. Default: - no destination
        :param on_success: The destination for successful invocations. Default: - no destination
        :param retry_attempts: The maximum number of times to retry when the function returns an error. Minimum: 0 Maximum: 2 Default: 2

        stability
        :stability: experimental
        """
        options = EventInvokeConfigOptions(max_event_age=max_event_age, on_failure=on_failure, on_success=on_success, retry_attempts=retry_attempts)

        return jsii.invoke(self, "configureAsyncInvoke", [options])

    @jsii.member(jsii_name="grantInvoke")
    def grant_invoke(self, identity: _IGrantable_0fcfc53a) -> _Grant_96af6d2d:
        """Grant the given identity permissions to invoke this Lambda.

        :param identity: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "grantInvoke", [identity])

    @jsii.member(jsii_name="metric")
    def metric(self, metric_name: str, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[_Duration_5170c158]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[_Unit_e1b74f3c]=None) -> _Metric_53e89548:
        """Return the given named metric for this Lambda Return the given named metric for this Function.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metric", [metric_name, props])

    @jsii.member(jsii_name="metricDuration")
    def metric_duration(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[_Duration_5170c158]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[_Unit_e1b74f3c]=None) -> _Metric_53e89548:
        """Metric for the Duration of this Lambda How long execution of this Lambda takes.

        Average over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: average over 5 minutes

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricDuration", [props])

    @jsii.member(jsii_name="metricErrors")
    def metric_errors(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[_Duration_5170c158]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[_Unit_e1b74f3c]=None) -> _Metric_53e89548:
        """How many invocations of this Lambda fail.

        Sum over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricErrors", [props])

    @jsii.member(jsii_name="metricInvocations")
    def metric_invocations(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[_Duration_5170c158]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[_Unit_e1b74f3c]=None) -> _Metric_53e89548:
        """Metric for the number of invocations of this Lambda How often this Lambda is invoked.

        Sum over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over 5 minutes

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricInvocations", [props])

    @jsii.member(jsii_name="metricThrottles")
    def metric_throttles(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[_Duration_5170c158]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[_Unit_e1b74f3c]=None) -> _Metric_53e89548:
        """Metric for the number of throttled invocations of this Lambda How often this Lambda is throttled.

        Sum over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over 5 minutes

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricThrottles", [props])


@jsii.interface(jsii_type="monocdk-experiment.aws_lambda.ILayerVersion")
class ILayerVersion(_IResource_72f7ee7e, jsii.compat.Protocol):
    """
    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ILayerVersionProxy

    @builtins.property
    @jsii.member(jsii_name="layerVersionArn")
    def layer_version_arn(self) -> str:
        """The ARN of the Lambda Layer version that this Layer defines.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="compatibleRuntimes")
    def compatible_runtimes(self) -> typing.Optional[typing.List["Runtime"]]:
        """The runtimes compatible with this Layer.

        default
        :default: Runtime.All

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="addPermission")
    def add_permission(self, id: str, *, account_id: str, organization_id: typing.Optional[str]=None) -> None:
        """Add permission for this layer version to specific entities.

        Usage within
        the same account where the layer is defined is always allowed and does not
        require calling this method. Note that the principal that creates the
        Lambda function using the layer (for example, a CloudFormation changeset
        execution role) also needs to have the ``lambda:GetLayerVersion``
        permission on the layer version.

        :param id: the ID of the grant in the construct tree.
        :param account_id: The AWS Account id of the account that is authorized to use a Lambda Layer Version. The wild-card ``'*'`` can be used to grant access to "any" account (or any account in an organization when ``organizationId`` is specified).
        :param organization_id: The ID of the AWS Organization to hwich the grant is restricted. Can only be specified if ``accountId`` is ``'*'``

        stability
        :stability: experimental
        """
        ...


class _ILayerVersionProxy(jsii.proxy_for(_IResource_72f7ee7e)):
    """
    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_lambda.ILayerVersion"
    @builtins.property
    @jsii.member(jsii_name="layerVersionArn")
    def layer_version_arn(self) -> str:
        """The ARN of the Lambda Layer version that this Layer defines.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "layerVersionArn")

    @builtins.property
    @jsii.member(jsii_name="compatibleRuntimes")
    def compatible_runtimes(self) -> typing.Optional[typing.List["Runtime"]]:
        """The runtimes compatible with this Layer.

        default
        :default: Runtime.All

        stability
        :stability: experimental
        """
        return jsii.get(self, "compatibleRuntimes")

    @jsii.member(jsii_name="addPermission")
    def add_permission(self, id: str, *, account_id: str, organization_id: typing.Optional[str]=None) -> None:
        """Add permission for this layer version to specific entities.

        Usage within
        the same account where the layer is defined is always allowed and does not
        require calling this method. Note that the principal that creates the
        Lambda function using the layer (for example, a CloudFormation changeset
        execution role) also needs to have the ``lambda:GetLayerVersion``
        permission on the layer version.

        :param id: the ID of the grant in the construct tree.
        :param account_id: The AWS Account id of the account that is authorized to use a Lambda Layer Version. The wild-card ``'*'`` can be used to grant access to "any" account (or any account in an organization when ``organizationId`` is specified).
        :param organization_id: The ID of the AWS Organization to hwich the grant is restricted. Can only be specified if ``accountId`` is ``'*'``

        stability
        :stability: experimental
        """
        permission = LayerVersionPermission(account_id=account_id, organization_id=organization_id)

        return jsii.invoke(self, "addPermission", [id, permission])


@jsii.interface(jsii_type="monocdk-experiment.aws_lambda.IVersion")
class IVersion(IFunction, jsii.compat.Protocol):
    """
    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IVersionProxy

    @builtins.property
    @jsii.member(jsii_name="lambda")
    def lambda_(self) -> "IFunction":
        """The underlying AWS Lambda function.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> str:
        """The most recently deployed version of this function.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @jsii.member(jsii_name="addAlias")
    def add_alias(self, alias_name: str, *, additional_versions: typing.Optional[typing.List["VersionWeight"]]=None, description: typing.Optional[str]=None, provisioned_concurrent_executions: typing.Optional[jsii.Number]=None, max_event_age: typing.Optional[_Duration_5170c158]=None, on_failure: typing.Optional["IDestination"]=None, on_success: typing.Optional["IDestination"]=None, retry_attempts: typing.Optional[jsii.Number]=None) -> "Alias":
        """Defines an alias for this version.

        :param alias_name: The name of the alias.
        :param additional_versions: Additional versions with individual weights this alias points to. Individual additional version weights specified here should add up to (less than) one. All remaining weight is routed to the default version. For example, the config is Example:: version: "1" additionalVersions: [{ version: "2", weight: 0.05 }] Then 5% of traffic will be routed to function version 2, while the remaining 95% of traffic will be routed to function version 1. Default: No additional versions
        :param description: Description for the alias. Default: No description
        :param provisioned_concurrent_executions: Specifies a provisioned concurrency configuration for a function's alias. Default: No provisioned concurrency
        :param max_event_age: The maximum age of a request that Lambda sends to a function for processing. Minimum: 60 seconds Maximum: 6 hours Default: Duration.hours(6)
        :param on_failure: The destination for failed invocations. Default: - no destination
        :param on_success: The destination for successful invocations. Default: - no destination
        :param retry_attempts: The maximum number of times to retry when the function returns an error. Minimum: 0 Maximum: 2 Default: 2

        stability
        :stability: experimental
        """
        ...


class _IVersionProxy(jsii.proxy_for(IFunction)):
    """
    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_lambda.IVersion"
    @builtins.property
    @jsii.member(jsii_name="lambda")
    def lambda_(self) -> "IFunction":
        """The underlying AWS Lambda function.

        stability
        :stability: experimental
        """
        return jsii.get(self, "lambda")

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> str:
        """The most recently deployed version of this function.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "version")

    @jsii.member(jsii_name="addAlias")
    def add_alias(self, alias_name: str, *, additional_versions: typing.Optional[typing.List["VersionWeight"]]=None, description: typing.Optional[str]=None, provisioned_concurrent_executions: typing.Optional[jsii.Number]=None, max_event_age: typing.Optional[_Duration_5170c158]=None, on_failure: typing.Optional["IDestination"]=None, on_success: typing.Optional["IDestination"]=None, retry_attempts: typing.Optional[jsii.Number]=None) -> "Alias":
        """Defines an alias for this version.

        :param alias_name: The name of the alias.
        :param additional_versions: Additional versions with individual weights this alias points to. Individual additional version weights specified here should add up to (less than) one. All remaining weight is routed to the default version. For example, the config is Example:: version: "1" additionalVersions: [{ version: "2", weight: 0.05 }] Then 5% of traffic will be routed to function version 2, while the remaining 95% of traffic will be routed to function version 1. Default: No additional versions
        :param description: Description for the alias. Default: No description
        :param provisioned_concurrent_executions: Specifies a provisioned concurrency configuration for a function's alias. Default: No provisioned concurrency
        :param max_event_age: The maximum age of a request that Lambda sends to a function for processing. Minimum: 60 seconds Maximum: 6 hours Default: Duration.hours(6)
        :param on_failure: The destination for failed invocations. Default: - no destination
        :param on_success: The destination for successful invocations. Default: - no destination
        :param retry_attempts: The maximum number of times to retry when the function returns an error. Minimum: 0 Maximum: 2 Default: 2

        stability
        :stability: experimental
        """
        options = AliasOptions(additional_versions=additional_versions, description=description, provisioned_concurrent_executions=provisioned_concurrent_executions, max_event_age=max_event_age, on_failure=on_failure, on_success=on_success, retry_attempts=retry_attempts)

        return jsii.invoke(self, "addAlias", [alias_name, options])


class InlineCode(Code, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_lambda.InlineCode"):
    """Lambda code from an inline string (limited to 4KiB).

    stability
    :stability: experimental
    """
    def __init__(self, code: str) -> None:
        """
        :param code: -

        stability
        :stability: experimental
        """
        jsii.create(InlineCode, self, [code])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: _Construct_f50a3f53) -> "CodeConfig":
        """Called when the lambda or layer is initialized to allow this object to bind to the stack, add resources and have fun.

        :param _scope: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_scope])

    @builtins.property
    @jsii.member(jsii_name="isInline")
    def is_inline(self) -> bool:
        """Determines whether this Code is inline code or not.

        stability
        :stability: experimental
        """
        return jsii.get(self, "isInline")


@jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.LambdaRuntimeProps", jsii_struct_bases=[], name_mapping={'supports_inline_code': 'supportsInlineCode'})
class LambdaRuntimeProps():
    def __init__(self, *, supports_inline_code: typing.Optional[bool]=None) -> None:
        """
        :param supports_inline_code: Whether the ``ZipFile`` (aka inline code) property can be used with this runtime. Default: false

        stability
        :stability: experimental
        """
        self._values = {
        }
        if supports_inline_code is not None: self._values["supports_inline_code"] = supports_inline_code

    @builtins.property
    def supports_inline_code(self) -> typing.Optional[bool]:
        """Whether the ``ZipFile`` (aka inline code) property can be used with this runtime.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('supports_inline_code')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LambdaRuntimeProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(ILayerVersion)
class LayerVersion(_Resource_884d0774, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_lambda.LayerVersion"):
    """Defines a new Lambda Layer version.

    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, code: "Code", compatible_runtimes: typing.Optional[typing.List["Runtime"]]=None, description: typing.Optional[str]=None, layer_version_name: typing.Optional[str]=None, license: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param code: The content of this Layer. Using ``Code.fromInline`` is not supported.
        :param compatible_runtimes: The runtimes compatible with this Layer. Default: - All runtimes are supported.
        :param description: The description the this Lambda Layer. Default: - No description.
        :param layer_version_name: The name of the layer. Default: - A name will be generated.
        :param license: The SPDX licence identifier or URL to the license file for this layer. Default: - No license information will be recorded.

        stability
        :stability: experimental
        """
        props = LayerVersionProps(code=code, compatible_runtimes=compatible_runtimes, description=description, layer_version_name=layer_version_name, license=license)

        jsii.create(LayerVersion, self, [scope, id, props])

    @jsii.member(jsii_name="fromLayerVersionArn")
    @builtins.classmethod
    def from_layer_version_arn(cls, scope: _Construct_f50a3f53, id: str, layer_version_arn: str) -> "ILayerVersion":
        """Imports a layer version by ARN.

        Assumes it is compatible with all Lambda runtimes.

        :param scope: -
        :param id: -
        :param layer_version_arn: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromLayerVersionArn", [scope, id, layer_version_arn])

    @jsii.member(jsii_name="fromLayerVersionAttributes")
    @builtins.classmethod
    def from_layer_version_attributes(cls, scope: _Construct_f50a3f53, id: str, *, layer_version_arn: str, compatible_runtimes: typing.Optional[typing.List["Runtime"]]=None) -> "ILayerVersion":
        """Imports a Layer that has been defined externally.

        :param scope: the parent Construct that will use the imported layer.
        :param id: the id of the imported layer in the construct tree.
        :param layer_version_arn: The ARN of the LayerVersion.
        :param compatible_runtimes: The list of compatible runtimes with this Layer.

        stability
        :stability: experimental
        """
        attrs = LayerVersionAttributes(layer_version_arn=layer_version_arn, compatible_runtimes=compatible_runtimes)

        return jsii.sinvoke(cls, "fromLayerVersionAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="addPermission")
    def add_permission(self, id: str, *, account_id: str, organization_id: typing.Optional[str]=None) -> None:
        """Add permission for this layer version to specific entities.

        Usage within
        the same account where the layer is defined is always allowed and does not
        require calling this method. Note that the principal that creates the
        Lambda function using the layer (for example, a CloudFormation changeset
        execution role) also needs to have the ``lambda:GetLayerVersion``
        permission on the layer version.

        :param id: -
        :param account_id: The AWS Account id of the account that is authorized to use a Lambda Layer Version. The wild-card ``'*'`` can be used to grant access to "any" account (or any account in an organization when ``organizationId`` is specified).
        :param organization_id: The ID of the AWS Organization to hwich the grant is restricted. Can only be specified if ``accountId`` is ``'*'``

        stability
        :stability: experimental
        """
        permission = LayerVersionPermission(account_id=account_id, organization_id=organization_id)

        return jsii.invoke(self, "addPermission", [id, permission])

    @builtins.property
    @jsii.member(jsii_name="layerVersionArn")
    def layer_version_arn(self) -> str:
        """The ARN of the Lambda Layer version that this Layer defines.

        stability
        :stability: experimental
        """
        return jsii.get(self, "layerVersionArn")

    @builtins.property
    @jsii.member(jsii_name="compatibleRuntimes")
    def compatible_runtimes(self) -> typing.Optional[typing.List["Runtime"]]:
        """The runtimes compatible with this Layer.

        stability
        :stability: experimental
        """
        return jsii.get(self, "compatibleRuntimes")


@jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.LayerVersionAttributes", jsii_struct_bases=[], name_mapping={'layer_version_arn': 'layerVersionArn', 'compatible_runtimes': 'compatibleRuntimes'})
class LayerVersionAttributes():
    def __init__(self, *, layer_version_arn: str, compatible_runtimes: typing.Optional[typing.List["Runtime"]]=None) -> None:
        """Properties necessary to import a LayerVersion.

        :param layer_version_arn: The ARN of the LayerVersion.
        :param compatible_runtimes: The list of compatible runtimes with this Layer.

        stability
        :stability: experimental
        """
        self._values = {
            'layer_version_arn': layer_version_arn,
        }
        if compatible_runtimes is not None: self._values["compatible_runtimes"] = compatible_runtimes

    @builtins.property
    def layer_version_arn(self) -> str:
        """The ARN of the LayerVersion.

        stability
        :stability: experimental
        """
        return self._values.get('layer_version_arn')

    @builtins.property
    def compatible_runtimes(self) -> typing.Optional[typing.List["Runtime"]]:
        """The list of compatible runtimes with this Layer.

        stability
        :stability: experimental
        """
        return self._values.get('compatible_runtimes')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LayerVersionAttributes(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.LayerVersionPermission", jsii_struct_bases=[], name_mapping={'account_id': 'accountId', 'organization_id': 'organizationId'})
class LayerVersionPermission():
    def __init__(self, *, account_id: str, organization_id: typing.Optional[str]=None) -> None:
        """Identification of an account (or organization) that is allowed to access a Lambda Layer Version.

        :param account_id: The AWS Account id of the account that is authorized to use a Lambda Layer Version. The wild-card ``'*'`` can be used to grant access to "any" account (or any account in an organization when ``organizationId`` is specified).
        :param organization_id: The ID of the AWS Organization to hwich the grant is restricted. Can only be specified if ``accountId`` is ``'*'``

        stability
        :stability: experimental
        """
        self._values = {
            'account_id': account_id,
        }
        if organization_id is not None: self._values["organization_id"] = organization_id

    @builtins.property
    def account_id(self) -> str:
        """The AWS Account id of the account that is authorized to use a Lambda Layer Version.

        The wild-card ``'*'`` can be
        used to grant access to "any" account (or any account in an organization when ``organizationId`` is specified).

        stability
        :stability: experimental
        """
        return self._values.get('account_id')

    @builtins.property
    def organization_id(self) -> typing.Optional[str]:
        """The ID of the AWS Organization to hwich the grant is restricted.

        Can only be specified if ``accountId`` is ``'*'``

        stability
        :stability: experimental
        """
        return self._values.get('organization_id')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LayerVersionPermission(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.LayerVersionProps", jsii_struct_bases=[], name_mapping={'code': 'code', 'compatible_runtimes': 'compatibleRuntimes', 'description': 'description', 'layer_version_name': 'layerVersionName', 'license': 'license'})
class LayerVersionProps():
    def __init__(self, *, code: "Code", compatible_runtimes: typing.Optional[typing.List["Runtime"]]=None, description: typing.Optional[str]=None, layer_version_name: typing.Optional[str]=None, license: typing.Optional[str]=None) -> None:
        """
        :param code: The content of this Layer. Using ``Code.fromInline`` is not supported.
        :param compatible_runtimes: The runtimes compatible with this Layer. Default: - All runtimes are supported.
        :param description: The description the this Lambda Layer. Default: - No description.
        :param layer_version_name: The name of the layer. Default: - A name will be generated.
        :param license: The SPDX licence identifier or URL to the license file for this layer. Default: - No license information will be recorded.

        stability
        :stability: experimental
        """
        self._values = {
            'code': code,
        }
        if compatible_runtimes is not None: self._values["compatible_runtimes"] = compatible_runtimes
        if description is not None: self._values["description"] = description
        if layer_version_name is not None: self._values["layer_version_name"] = layer_version_name
        if license is not None: self._values["license"] = license

    @builtins.property
    def code(self) -> "Code":
        """The content of this Layer.

        Using ``Code.fromInline`` is not supported.

        stability
        :stability: experimental
        """
        return self._values.get('code')

    @builtins.property
    def compatible_runtimes(self) -> typing.Optional[typing.List["Runtime"]]:
        """The runtimes compatible with this Layer.

        default
        :default: - All runtimes are supported.

        stability
        :stability: experimental
        """
        return self._values.get('compatible_runtimes')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """The description the this Lambda Layer.

        default
        :default: - No description.

        stability
        :stability: experimental
        """
        return self._values.get('description')

    @builtins.property
    def layer_version_name(self) -> typing.Optional[str]:
        """The name of the layer.

        default
        :default: - A name will be generated.

        stability
        :stability: experimental
        """
        return self._values.get('layer_version_name')

    @builtins.property
    def license(self) -> typing.Optional[str]:
        """The SPDX licence identifier or URL to the license file for this layer.

        default
        :default: - No license information will be recorded.

        stability
        :stability: experimental
        """
        return self._values.get('license')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LayerVersionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class LogRetention(_Construct_f50a3f53, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_lambda.LogRetention"):
    """Creates a custom resource to control the retention policy of a CloudWatch Logs log group.

    The log group is created if it doesn't already exist. The policy
    is removed when ``retentionDays`` is ``undefined`` or equal to ``Infinity``.

    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, log_group_name: str, retention: _RetentionDays_bdc7ad1f, log_retention_retry_options: typing.Optional["LogRetentionRetryOptions"]=None, role: typing.Optional[_IRole_e69bbae4]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param log_group_name: The log group name.
        :param retention: The number of days log events are kept in CloudWatch Logs.
        :param log_retention_retry_options: Retry options for all AWS API calls. Default: - AWS SDK default retry options
        :param role: The IAM role for the Lambda function associated with the custom resource. Default: - A new role is created

        stability
        :stability: experimental
        """
        props = LogRetentionProps(log_group_name=log_group_name, retention=retention, log_retention_retry_options=log_retention_retry_options, role=role)

        jsii.create(LogRetention, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="logGroupArn")
    def log_group_arn(self) -> str:
        """The ARN of the LogGroup.

        stability
        :stability: experimental
        """
        return jsii.get(self, "logGroupArn")


@jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.LogRetentionProps", jsii_struct_bases=[], name_mapping={'log_group_name': 'logGroupName', 'retention': 'retention', 'log_retention_retry_options': 'logRetentionRetryOptions', 'role': 'role'})
class LogRetentionProps():
    def __init__(self, *, log_group_name: str, retention: _RetentionDays_bdc7ad1f, log_retention_retry_options: typing.Optional["LogRetentionRetryOptions"]=None, role: typing.Optional[_IRole_e69bbae4]=None) -> None:
        """Construction properties for a LogRetention.

        :param log_group_name: The log group name.
        :param retention: The number of days log events are kept in CloudWatch Logs.
        :param log_retention_retry_options: Retry options for all AWS API calls. Default: - AWS SDK default retry options
        :param role: The IAM role for the Lambda function associated with the custom resource. Default: - A new role is created

        stability
        :stability: experimental
        """
        if isinstance(log_retention_retry_options, dict): log_retention_retry_options = LogRetentionRetryOptions(**log_retention_retry_options)
        self._values = {
            'log_group_name': log_group_name,
            'retention': retention,
        }
        if log_retention_retry_options is not None: self._values["log_retention_retry_options"] = log_retention_retry_options
        if role is not None: self._values["role"] = role

    @builtins.property
    def log_group_name(self) -> str:
        """The log group name.

        stability
        :stability: experimental
        """
        return self._values.get('log_group_name')

    @builtins.property
    def retention(self) -> _RetentionDays_bdc7ad1f:
        """The number of days log events are kept in CloudWatch Logs.

        stability
        :stability: experimental
        """
        return self._values.get('retention')

    @builtins.property
    def log_retention_retry_options(self) -> typing.Optional["LogRetentionRetryOptions"]:
        """Retry options for all AWS API calls.

        default
        :default: - AWS SDK default retry options

        stability
        :stability: experimental
        """
        return self._values.get('log_retention_retry_options')

    @builtins.property
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The IAM role for the Lambda function associated with the custom resource.

        default
        :default: - A new role is created

        stability
        :stability: experimental
        """
        return self._values.get('role')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LogRetentionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.LogRetentionRetryOptions", jsii_struct_bases=[], name_mapping={'base': 'base', 'max_retries': 'maxRetries'})
class LogRetentionRetryOptions():
    def __init__(self, *, base: typing.Optional[_Duration_5170c158]=None, max_retries: typing.Optional[jsii.Number]=None) -> None:
        """Retry options for all AWS API calls.

        :param base: The base duration to use in the exponential backoff for operation retries. Default: Duration.millis(100) (AWS SDK default)
        :param max_retries: The maximum amount of retries. Default: 3 (AWS SDK default)

        stability
        :stability: experimental
        """
        self._values = {
        }
        if base is not None: self._values["base"] = base
        if max_retries is not None: self._values["max_retries"] = max_retries

    @builtins.property
    def base(self) -> typing.Optional[_Duration_5170c158]:
        """The base duration to use in the exponential backoff for operation retries.

        default
        :default: Duration.millis(100) (AWS SDK default)

        stability
        :stability: experimental
        """
        return self._values.get('base')

    @builtins.property
    def max_retries(self) -> typing.Optional[jsii.Number]:
        """The maximum amount of retries.

        default
        :default: 3 (AWS SDK default)

        stability
        :stability: experimental
        """
        return self._values.get('max_retries')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LogRetentionRetryOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.Permission", jsii_struct_bases=[], name_mapping={'principal': 'principal', 'action': 'action', 'event_source_token': 'eventSourceToken', 'scope': 'scope', 'source_account': 'sourceAccount', 'source_arn': 'sourceArn'})
class Permission():
    def __init__(self, *, principal: _IPrincipal_97126874, action: typing.Optional[str]=None, event_source_token: typing.Optional[str]=None, scope: typing.Optional[_Construct_f50a3f53]=None, source_account: typing.Optional[str]=None, source_arn: typing.Optional[str]=None) -> None:
        """Represents a permission statement that can be added to a Lambda's resource policy via the ``addToResourcePolicy`` method.

        :param principal: The entity for which you are granting permission to invoke the Lambda function. This entity can be any valid AWS service principal, such as s3.amazonaws.com or sns.amazonaws.com, or, if you are granting cross-account permission, an AWS account ID. For example, you might want to allow a custom application in another AWS account to push events to Lambda by invoking your function. The principal can be either an AccountPrincipal or a ServicePrincipal.
        :param action: The Lambda actions that you want to allow in this statement. For example, you can specify lambda:CreateFunction to specify a certain action, or use a wildcard (``lambda:*``) to grant permission to all Lambda actions. For a list of actions, see Actions and Condition Context Keys for AWS Lambda in the IAM User Guide. Default: 'lambda:InvokeFunction'
        :param event_source_token: A unique token that must be supplied by the principal invoking the function. Default: The caller would not need to present a token.
        :param scope: The scope to which the permission constructs be attached. The default is the Lambda function construct itself, but this would need to be different in cases such as cross-stack references where the Permissions would need to sit closer to the consumer of this permission (i.e., the caller). Default: - The instance of lambda.IFunction
        :param source_account: The AWS account ID (without hyphens) of the source owner. For example, if you specify an S3 bucket in the SourceArn property, this value is the bucket owner's account ID. You can use this property to ensure that all source principals are owned by a specific account.
        :param source_arn: The ARN of a resource that is invoking your function. When granting Amazon Simple Storage Service (Amazon S3) permission to invoke your function, specify this property with the bucket ARN as its value. This ensures that events generated only from the specified bucket, not just any bucket from any AWS account that creates a mapping to your function, can invoke the function.

        stability
        :stability: experimental
        """
        self._values = {
            'principal': principal,
        }
        if action is not None: self._values["action"] = action
        if event_source_token is not None: self._values["event_source_token"] = event_source_token
        if scope is not None: self._values["scope"] = scope
        if source_account is not None: self._values["source_account"] = source_account
        if source_arn is not None: self._values["source_arn"] = source_arn

    @builtins.property
    def principal(self) -> _IPrincipal_97126874:
        """The entity for which you are granting permission to invoke the Lambda function.

        This entity can be any valid AWS service principal, such as
        s3.amazonaws.com or sns.amazonaws.com, or, if you are granting
        cross-account permission, an AWS account ID. For example, you might want
        to allow a custom application in another AWS account to push events to
        Lambda by invoking your function.

        The principal can be either an AccountPrincipal or a ServicePrincipal.

        stability
        :stability: experimental
        """
        return self._values.get('principal')

    @builtins.property
    def action(self) -> typing.Optional[str]:
        """The Lambda actions that you want to allow in this statement.

        For example,
        you can specify lambda:CreateFunction to specify a certain action, or use
        a wildcard (``lambda:*``) to grant permission to all Lambda actions. For a
        list of actions, see Actions and Condition Context Keys for AWS Lambda in
        the IAM User Guide.

        default
        :default: 'lambda:InvokeFunction'

        stability
        :stability: experimental
        """
        return self._values.get('action')

    @builtins.property
    def event_source_token(self) -> typing.Optional[str]:
        """A unique token that must be supplied by the principal invoking the function.

        default
        :default: The caller would not need to present a token.

        stability
        :stability: experimental
        """
        return self._values.get('event_source_token')

    @builtins.property
    def scope(self) -> typing.Optional[_Construct_f50a3f53]:
        """The scope to which the permission constructs be attached.

        The default is
        the Lambda function construct itself, but this would need to be different
        in cases such as cross-stack references where the Permissions would need
        to sit closer to the consumer of this permission (i.e., the caller).

        default
        :default: - The instance of lambda.IFunction

        stability
        :stability: experimental
        """
        return self._values.get('scope')

    @builtins.property
    def source_account(self) -> typing.Optional[str]:
        """The AWS account ID (without hyphens) of the source owner.

        For example, if
        you specify an S3 bucket in the SourceArn property, this value is the
        bucket owner's account ID. You can use this property to ensure that all
        source principals are owned by a specific account.

        stability
        :stability: experimental
        """
        return self._values.get('source_account')

    @builtins.property
    def source_arn(self) -> typing.Optional[str]:
        """The ARN of a resource that is invoking your function.

        When granting
        Amazon Simple Storage Service (Amazon S3) permission to invoke your
        function, specify this property with the bucket ARN as its value. This
        ensures that events generated only from the specified bucket, not just
        any bucket from any AWS account that creates a mapping to your function,
        can invoke the function.

        stability
        :stability: experimental
        """
        return self._values.get('source_arn')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'Permission(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.ResourceBindOptions", jsii_struct_bases=[], name_mapping={'resource_property': 'resourceProperty'})
class ResourceBindOptions():
    def __init__(self, *, resource_property: typing.Optional[str]=None) -> None:
        """
        :param resource_property: The name of the CloudFormation property to annotate with asset metadata. Default: Code

        stability
        :stability: experimental
        """
        self._values = {
        }
        if resource_property is not None: self._values["resource_property"] = resource_property

    @builtins.property
    def resource_property(self) -> typing.Optional[str]:
        """The name of the CloudFormation property to annotate with asset metadata.

        default
        :default: Code

        see
        :see: https://github.com/aws/aws-cdk/issues/1432
        stability
        :stability: experimental
        """
        return self._values.get('resource_property')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ResourceBindOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class Runtime(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_lambda.Runtime"):
    """Lambda function runtime environment.

    If you need to use a runtime name that doesn't exist as a static member, you
    can instantiate a ``Runtime`` object, e.g: ``new Runtime('nodejs99.99')``.

    stability
    :stability: experimental
    """
    def __init__(self, name: str, family: typing.Optional["RuntimeFamily"]=None, *, supports_inline_code: typing.Optional[bool]=None) -> None:
        """
        :param name: -
        :param family: -
        :param supports_inline_code: Whether the ``ZipFile`` (aka inline code) property can be used with this runtime. Default: false

        stability
        :stability: experimental
        """
        props = LambdaRuntimeProps(supports_inline_code=supports_inline_code)

        jsii.create(Runtime, self, [name, family, props])

    @jsii.member(jsii_name="runtimeEquals")
    def runtime_equals(self, other: "Runtime") -> bool:
        """
        :param other: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "runtimeEquals", [other])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toString", [])

    @jsii.python.classproperty
    @jsii.member(jsii_name="ALL")
    def ALL(cls) -> typing.List["Runtime"]:
        """A list of all known ``Runtime``'s.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "ALL")

    @jsii.python.classproperty
    @jsii.member(jsii_name="DOTNET_CORE_1")
    def DOTNET_CORE_1(cls) -> "Runtime":
        """The .NET Core 1.0 runtime (dotnetcore1.0).

        deprecated
        :deprecated: Use {@link DOTNET_CORE_2_1}

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "DOTNET_CORE_1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="DOTNET_CORE_2")
    def DOTNET_CORE_2(cls) -> "Runtime":
        """The .NET Core 2.0 runtime (dotnetcore2.0).

        deprecated
        :deprecated: Use {@link DOTNET_CORE_2_1}

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "DOTNET_CORE_2")

    @jsii.python.classproperty
    @jsii.member(jsii_name="DOTNET_CORE_2_1")
    def DOTNET_CORE_2_1(cls) -> "Runtime":
        """The .NET Core 2.1 runtime (dotnetcore2.1).

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "DOTNET_CORE_2_1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="DOTNET_CORE_3_1")
    def DOTNET_CORE_3_1(cls) -> "Runtime":
        """The .NET Core 3.1 runtime (dotnetcore3.1).

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "DOTNET_CORE_3_1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="GO_1_X")
    def GO_1_X(cls) -> "Runtime":
        """The Go 1.x runtime (go1.x).

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "GO_1_X")

    @jsii.python.classproperty
    @jsii.member(jsii_name="JAVA_11")
    def JAVA_11(cls) -> "Runtime":
        """The Java 11 runtime (java11).

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "JAVA_11")

    @jsii.python.classproperty
    @jsii.member(jsii_name="JAVA_8")
    def JAVA_8(cls) -> "Runtime":
        """The Java 8 runtime (java8).

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "JAVA_8")

    @jsii.python.classproperty
    @jsii.member(jsii_name="NODEJS")
    def NODEJS(cls) -> "Runtime":
        """The NodeJS runtime (nodejs).

        deprecated
        :deprecated: Use {@link NODEJS_10_X}

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "NODEJS")

    @jsii.python.classproperty
    @jsii.member(jsii_name="NODEJS_10_X")
    def NODEJS_10_X(cls) -> "Runtime":
        """The NodeJS 10.x runtime (nodejs10.x).

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "NODEJS_10_X")

    @jsii.python.classproperty
    @jsii.member(jsii_name="NODEJS_12_X")
    def NODEJS_12_X(cls) -> "Runtime":
        """The NodeJS 12.x runtime (nodejs12.x).

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "NODEJS_12_X")

    @jsii.python.classproperty
    @jsii.member(jsii_name="NODEJS_4_3")
    def NODEJS_4_3(cls) -> "Runtime":
        """The NodeJS 4.3 runtime (nodejs4.3).

        deprecated
        :deprecated: Use {@link NODEJS_10_X}

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "NODEJS_4_3")

    @jsii.python.classproperty
    @jsii.member(jsii_name="NODEJS_6_10")
    def NODEJS_6_10(cls) -> "Runtime":
        """The NodeJS 6.10 runtime (nodejs6.10).

        deprecated
        :deprecated: Use {@link NODEJS_10_X}

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "NODEJS_6_10")

    @jsii.python.classproperty
    @jsii.member(jsii_name="NODEJS_8_10")
    def NODEJS_8_10(cls) -> "Runtime":
        """The NodeJS 8.10 runtime (nodejs8.10).

        deprecated
        :deprecated: Use {@link NODEJS_10_X}

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "NODEJS_8_10")

    @jsii.python.classproperty
    @jsii.member(jsii_name="PROVIDED")
    def PROVIDED(cls) -> "Runtime":
        """The custom provided runtime (provided).

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "PROVIDED")

    @jsii.python.classproperty
    @jsii.member(jsii_name="PYTHON_2_7")
    def PYTHON_2_7(cls) -> "Runtime":
        """The Python 2.7 runtime (python2.7).

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "PYTHON_2_7")

    @jsii.python.classproperty
    @jsii.member(jsii_name="PYTHON_3_6")
    def PYTHON_3_6(cls) -> "Runtime":
        """The Python 3.6 runtime (python3.6).

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "PYTHON_3_6")

    @jsii.python.classproperty
    @jsii.member(jsii_name="PYTHON_3_7")
    def PYTHON_3_7(cls) -> "Runtime":
        """The Python 3.7 runtime (python3.7).

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "PYTHON_3_7")

    @jsii.python.classproperty
    @jsii.member(jsii_name="PYTHON_3_8")
    def PYTHON_3_8(cls) -> "Runtime":
        """The Python 3.8 runtime (python3.8).

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "PYTHON_3_8")

    @jsii.python.classproperty
    @jsii.member(jsii_name="RUBY_2_5")
    def RUBY_2_5(cls) -> "Runtime":
        """The Ruby 2.5 runtime (ruby2.5).

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "RUBY_2_5")

    @jsii.python.classproperty
    @jsii.member(jsii_name="RUBY_2_7")
    def RUBY_2_7(cls) -> "Runtime":
        """The Ruby 2.7 runtime (ruby2.7).

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "RUBY_2_7")

    @builtins.property
    @jsii.member(jsii_name="bundlingDockerImage")
    def bundling_docker_image(self) -> _BundlingDockerImage_5a43b005:
        """The bundling Docker image for this runtime.

        Points to the lambci/lambda build image for this runtime.

        see
        :see: https://hub.docker.com/r/lambci/lambda/
        stability
        :stability: experimental
        """
        return jsii.get(self, "bundlingDockerImage")

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """The name of this runtime, as expected by the Lambda resource.

        stability
        :stability: experimental
        """
        return jsii.get(self, "name")

    @builtins.property
    @jsii.member(jsii_name="supportsInlineCode")
    def supports_inline_code(self) -> bool:
        """Whether the ``ZipFile`` (aka inline code) property can be used with this runtime.

        stability
        :stability: experimental
        """
        return jsii.get(self, "supportsInlineCode")

    @builtins.property
    @jsii.member(jsii_name="family")
    def family(self) -> typing.Optional["RuntimeFamily"]:
        """The runtime family.

        stability
        :stability: experimental
        """
        return jsii.get(self, "family")


@jsii.enum(jsii_type="monocdk-experiment.aws_lambda.RuntimeFamily")
class RuntimeFamily(enum.Enum):
    """
    stability
    :stability: experimental
    """
    NODEJS = "NODEJS"
    """
    stability
    :stability: experimental
    """
    JAVA = "JAVA"
    """
    stability
    :stability: experimental
    """
    PYTHON = "PYTHON"
    """
    stability
    :stability: experimental
    """
    DOTNET_CORE = "DOTNET_CORE"
    """
    stability
    :stability: experimental
    """
    GO = "GO"
    """
    stability
    :stability: experimental
    """
    RUBY = "RUBY"
    """
    stability
    :stability: experimental
    """
    OTHER = "OTHER"
    """
    stability
    :stability: experimental
    """

class S3Code(Code, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_lambda.S3Code"):
    """Lambda code from an S3 archive.

    stability
    :stability: experimental
    """
    def __init__(self, bucket: _IBucket_25bad983, key: str, object_version: typing.Optional[str]=None) -> None:
        """
        :param bucket: -
        :param key: -
        :param object_version: -

        stability
        :stability: experimental
        """
        jsii.create(S3Code, self, [bucket, key, object_version])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: _Construct_f50a3f53) -> "CodeConfig":
        """Called when the lambda or layer is initialized to allow this object to bind to the stack, add resources and have fun.

        :param _scope: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_scope])

    @builtins.property
    @jsii.member(jsii_name="isInline")
    def is_inline(self) -> bool:
        """Determines whether this Code is inline code or not.

        stability
        :stability: experimental
        """
        return jsii.get(self, "isInline")


@jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.SingletonFunctionProps", jsii_struct_bases=[FunctionProps], name_mapping={'max_event_age': 'maxEventAge', 'on_failure': 'onFailure', 'on_success': 'onSuccess', 'retry_attempts': 'retryAttempts', 'allow_all_outbound': 'allowAllOutbound', 'current_version_options': 'currentVersionOptions', 'dead_letter_queue': 'deadLetterQueue', 'dead_letter_queue_enabled': 'deadLetterQueueEnabled', 'description': 'description', 'environment': 'environment', 'events': 'events', 'function_name': 'functionName', 'initial_policy': 'initialPolicy', 'layers': 'layers', 'log_retention': 'logRetention', 'log_retention_retry_options': 'logRetentionRetryOptions', 'log_retention_role': 'logRetentionRole', 'memory_size': 'memorySize', 'reserved_concurrent_executions': 'reservedConcurrentExecutions', 'role': 'role', 'security_group': 'securityGroup', 'security_groups': 'securityGroups', 'timeout': 'timeout', 'tracing': 'tracing', 'vpc': 'vpc', 'vpc_subnets': 'vpcSubnets', 'code': 'code', 'handler': 'handler', 'runtime': 'runtime', 'uuid': 'uuid', 'lambda_purpose': 'lambdaPurpose'})
class SingletonFunctionProps(FunctionProps):
    def __init__(self, *, max_event_age: typing.Optional[_Duration_5170c158]=None, on_failure: typing.Optional["IDestination"]=None, on_success: typing.Optional["IDestination"]=None, retry_attempts: typing.Optional[jsii.Number]=None, allow_all_outbound: typing.Optional[bool]=None, current_version_options: typing.Optional["VersionOptions"]=None, dead_letter_queue: typing.Optional[_IQueue_b743f559]=None, dead_letter_queue_enabled: typing.Optional[bool]=None, description: typing.Optional[str]=None, environment: typing.Optional[typing.Mapping[str, str]]=None, events: typing.Optional[typing.List["IEventSource"]]=None, function_name: typing.Optional[str]=None, initial_policy: typing.Optional[typing.List[_PolicyStatement_f75dc775]]=None, layers: typing.Optional[typing.List["ILayerVersion"]]=None, log_retention: typing.Optional[_RetentionDays_bdc7ad1f]=None, log_retention_retry_options: typing.Optional["LogRetentionRetryOptions"]=None, log_retention_role: typing.Optional[_IRole_e69bbae4]=None, memory_size: typing.Optional[jsii.Number]=None, reserved_concurrent_executions: typing.Optional[jsii.Number]=None, role: typing.Optional[_IRole_e69bbae4]=None, security_group: typing.Optional[_ISecurityGroup_d72ab8e8]=None, security_groups: typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]]=None, timeout: typing.Optional[_Duration_5170c158]=None, tracing: typing.Optional["Tracing"]=None, vpc: typing.Optional[_IVpc_3795853f]=None, vpc_subnets: typing.Optional[_SubnetSelection_36a13cd6]=None, code: "Code", handler: str, runtime: "Runtime", uuid: str, lambda_purpose: typing.Optional[str]=None) -> None:
        """Properties for a newly created singleton Lambda.

        :param max_event_age: The maximum age of a request that Lambda sends to a function for processing. Minimum: 60 seconds Maximum: 6 hours Default: Duration.hours(6)
        :param on_failure: The destination for failed invocations. Default: - no destination
        :param on_success: The destination for successful invocations. Default: - no destination
        :param retry_attempts: The maximum number of times to retry when the function returns an error. Minimum: 0 Maximum: 2 Default: 2
        :param allow_all_outbound: Whether to allow the Lambda to send all network traffic. If set to false, you must individually add traffic rules to allow the Lambda to connect to network targets. Default: true
        :param current_version_options: Options for the ``lambda.Version`` resource automatically created by the ``fn.currentVersion`` method. Default: - default options as described in ``VersionOptions``
        :param dead_letter_queue: The SQS queue to use if DLQ is enabled. Default: - SQS queue with 14 day retention period if ``deadLetterQueueEnabled`` is ``true``
        :param dead_letter_queue_enabled: Enabled DLQ. If ``deadLetterQueue`` is undefined, an SQS queue with default options will be defined for your Function. Default: - false unless ``deadLetterQueue`` is set, which implies DLQ is enabled.
        :param description: A description of the function. Default: - No description.
        :param environment: Key-value pairs that Lambda caches and makes available for your Lambda functions. Use environment variables to apply configuration changes, such as test and production environment configurations, without changing your Lambda function source code. Default: - No environment variables.
        :param events: Event sources for this function. You can also add event sources using ``addEventSource``. Default: - No event sources.
        :param function_name: A name for the function. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the function's name. For more information, see Name Type.
        :param initial_policy: Initial policy statements to add to the created Lambda Role. You can call ``addToRolePolicy`` to the created lambda to add statements post creation. Default: - No policy statements are added to the created Lambda role.
        :param layers: A list of layers to add to the function's execution environment. You can configure your Lambda function to pull in additional code during initialization in the form of layers. Layers are packages of libraries or other dependencies that can be used by mulitple functions. Default: - No layers.
        :param log_retention: The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.INFINITE
        :param log_retention_retry_options: When log retention is specified, a custom resource attempts to create the CloudWatch log group. These options control the retry policy when interacting with CloudWatch APIs. Default: - Default AWS SDK retry options.
        :param log_retention_role: The IAM role for the Lambda function associated with the custom resource that sets the retention policy. Default: - A new role is created.
        :param memory_size: The amount of memory, in MB, that is allocated to your Lambda function. Lambda uses this value to proportionally allocate the amount of CPU power. For more information, see Resource Model in the AWS Lambda Developer Guide. Default: 128
        :param reserved_concurrent_executions: The maximum of concurrent executions you want to reserve for the function. Default: - No specific limit - account limit.
        :param role: Lambda execution role. This is the role that will be assumed by the function upon execution. It controls the permissions that the function will have. The Role must be assumable by the 'lambda.amazonaws.com' service principal. The default Role automatically has permissions granted for Lambda execution. If you provide a Role, you must add the relevant AWS managed policies yourself. The relevant managed policies are "service-role/AWSLambdaBasicExecutionRole" and "service-role/AWSLambdaVPCAccessExecutionRole". Default: - A unique role will be generated for this lambda function. Both supplied and generated roles can always be changed by calling ``addToRolePolicy``.
        :param security_group: What security group to associate with the Lambda's network interfaces. This property is being deprecated, consider using securityGroups instead. Only used if 'vpc' is supplied. Use securityGroups property instead. Function constructor will throw an error if both are specified. Default: - If the function is placed within a VPC and a security group is not specified, either by this or securityGroups prop, a dedicated security group will be created for this function.
        :param security_groups: The list of security groups to associate with the Lambda's network interfaces. Only used if 'vpc' is supplied. Default: - If the function is placed within a VPC and a security group is not specified, either by this or securityGroup prop, a dedicated security group will be created for this function.
        :param timeout: The function execution time (in seconds) after which Lambda terminates the function. Because the execution time affects cost, set this value based on the function's expected execution time. Default: Duration.seconds(3)
        :param tracing: Enable AWS X-Ray Tracing for Lambda Function. Default: Tracing.Disabled
        :param vpc: VPC network to place Lambda network interfaces. Specify this if the Lambda function needs to access resources in a VPC. Default: - Function is not placed within a VPC.
        :param vpc_subnets: Where to place the network interfaces within the VPC. Only used if 'vpc' is supplied. Note: internet access for Lambdas requires a NAT gateway, so picking Public subnets is not allowed. Default: - the Vpc default strategy if not specified
        :param code: The source code of your Lambda function. You can point to a file in an Amazon Simple Storage Service (Amazon S3) bucket or specify your source code as inline text.
        :param handler: The name of the method within your code that Lambda calls to execute your function. The format includes the file name. It can also include namespaces and other qualifiers, depending on the runtime. For more information, see https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-features.html#gettingstarted-features-programmingmodel. NOTE: If you specify your source code as inline text by specifying the ZipFile property within the Code property, specify index.function_name as the handler.
        :param runtime: The runtime environment for the Lambda function that you are uploading. For valid values, see the Runtime property in the AWS Lambda Developer Guide.
        :param uuid: A unique identifier to identify this lambda. The identifier should be unique across all custom resource providers. We recommend generating a UUID per provider.
        :param lambda_purpose: A descriptive name for the purpose of this Lambda. If the Lambda does not have a physical name, this string will be reflected its generated name. The combination of lambdaPurpose and uuid must be unique. Default: SingletonLambda

        stability
        :stability: experimental
        """
        if isinstance(current_version_options, dict): current_version_options = VersionOptions(**current_version_options)
        if isinstance(log_retention_retry_options, dict): log_retention_retry_options = LogRetentionRetryOptions(**log_retention_retry_options)
        if isinstance(vpc_subnets, dict): vpc_subnets = _SubnetSelection_36a13cd6(**vpc_subnets)
        self._values = {
            'code': code,
            'handler': handler,
            'runtime': runtime,
            'uuid': uuid,
        }
        if max_event_age is not None: self._values["max_event_age"] = max_event_age
        if on_failure is not None: self._values["on_failure"] = on_failure
        if on_success is not None: self._values["on_success"] = on_success
        if retry_attempts is not None: self._values["retry_attempts"] = retry_attempts
        if allow_all_outbound is not None: self._values["allow_all_outbound"] = allow_all_outbound
        if current_version_options is not None: self._values["current_version_options"] = current_version_options
        if dead_letter_queue is not None: self._values["dead_letter_queue"] = dead_letter_queue
        if dead_letter_queue_enabled is not None: self._values["dead_letter_queue_enabled"] = dead_letter_queue_enabled
        if description is not None: self._values["description"] = description
        if environment is not None: self._values["environment"] = environment
        if events is not None: self._values["events"] = events
        if function_name is not None: self._values["function_name"] = function_name
        if initial_policy is not None: self._values["initial_policy"] = initial_policy
        if layers is not None: self._values["layers"] = layers
        if log_retention is not None: self._values["log_retention"] = log_retention
        if log_retention_retry_options is not None: self._values["log_retention_retry_options"] = log_retention_retry_options
        if log_retention_role is not None: self._values["log_retention_role"] = log_retention_role
        if memory_size is not None: self._values["memory_size"] = memory_size
        if reserved_concurrent_executions is not None: self._values["reserved_concurrent_executions"] = reserved_concurrent_executions
        if role is not None: self._values["role"] = role
        if security_group is not None: self._values["security_group"] = security_group
        if security_groups is not None: self._values["security_groups"] = security_groups
        if timeout is not None: self._values["timeout"] = timeout
        if tracing is not None: self._values["tracing"] = tracing
        if vpc is not None: self._values["vpc"] = vpc
        if vpc_subnets is not None: self._values["vpc_subnets"] = vpc_subnets
        if lambda_purpose is not None: self._values["lambda_purpose"] = lambda_purpose

    @builtins.property
    def max_event_age(self) -> typing.Optional[_Duration_5170c158]:
        """The maximum age of a request that Lambda sends to a function for processing.

        Minimum: 60 seconds
        Maximum: 6 hours

        default
        :default: Duration.hours(6)

        stability
        :stability: experimental
        """
        return self._values.get('max_event_age')

    @builtins.property
    def on_failure(self) -> typing.Optional["IDestination"]:
        """The destination for failed invocations.

        default
        :default: - no destination

        stability
        :stability: experimental
        """
        return self._values.get('on_failure')

    @builtins.property
    def on_success(self) -> typing.Optional["IDestination"]:
        """The destination for successful invocations.

        default
        :default: - no destination

        stability
        :stability: experimental
        """
        return self._values.get('on_success')

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        """The maximum number of times to retry when the function returns an error.

        Minimum: 0
        Maximum: 2

        default
        :default: 2

        stability
        :stability: experimental
        """
        return self._values.get('retry_attempts')

    @builtins.property
    def allow_all_outbound(self) -> typing.Optional[bool]:
        """Whether to allow the Lambda to send all network traffic.

        If set to false, you must individually add traffic rules to allow the
        Lambda to connect to network targets.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('allow_all_outbound')

    @builtins.property
    def current_version_options(self) -> typing.Optional["VersionOptions"]:
        """Options for the ``lambda.Version`` resource automatically created by the ``fn.currentVersion`` method.

        default
        :default: - default options as described in ``VersionOptions``

        stability
        :stability: experimental
        """
        return self._values.get('current_version_options')

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_IQueue_b743f559]:
        """The SQS queue to use if DLQ is enabled.

        default
        :default: - SQS queue with 14 day retention period if ``deadLetterQueueEnabled`` is ``true``

        stability
        :stability: experimental
        """
        return self._values.get('dead_letter_queue')

    @builtins.property
    def dead_letter_queue_enabled(self) -> typing.Optional[bool]:
        """Enabled DLQ.

        If ``deadLetterQueue`` is undefined,
        an SQS queue with default options will be defined for your Function.

        default
        :default: - false unless ``deadLetterQueue`` is set, which implies DLQ is enabled.

        stability
        :stability: experimental
        """
        return self._values.get('dead_letter_queue_enabled')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """A description of the function.

        default
        :default: - No description.

        stability
        :stability: experimental
        """
        return self._values.get('description')

    @builtins.property
    def environment(self) -> typing.Optional[typing.Mapping[str, str]]:
        """Key-value pairs that Lambda caches and makes available for your Lambda functions.

        Use environment variables to apply configuration changes, such
        as test and production environment configurations, without changing your
        Lambda function source code.

        default
        :default: - No environment variables.

        stability
        :stability: experimental
        """
        return self._values.get('environment')

    @builtins.property
    def events(self) -> typing.Optional[typing.List["IEventSource"]]:
        """Event sources for this function.

        You can also add event sources using ``addEventSource``.

        default
        :default: - No event sources.

        stability
        :stability: experimental
        """
        return self._values.get('events')

    @builtins.property
    def function_name(self) -> typing.Optional[str]:
        """A name for the function.

        default
        :default:

        - AWS CloudFormation generates a unique physical ID and uses that
          ID for the function's name. For more information, see Name Type.

        stability
        :stability: experimental
        """
        return self._values.get('function_name')

    @builtins.property
    def initial_policy(self) -> typing.Optional[typing.List[_PolicyStatement_f75dc775]]:
        """Initial policy statements to add to the created Lambda Role.

        You can call ``addToRolePolicy`` to the created lambda to add statements post creation.

        default
        :default: - No policy statements are added to the created Lambda role.

        stability
        :stability: experimental
        """
        return self._values.get('initial_policy')

    @builtins.property
    def layers(self) -> typing.Optional[typing.List["ILayerVersion"]]:
        """A list of layers to add to the function's execution environment.

        You can configure your Lambda function to pull in
        additional code during initialization in the form of layers. Layers are packages of libraries or other dependencies
        that can be used by mulitple functions.

        default
        :default: - No layers.

        stability
        :stability: experimental
        """
        return self._values.get('layers')

    @builtins.property
    def log_retention(self) -> typing.Optional[_RetentionDays_bdc7ad1f]:
        """The number of days log events are kept in CloudWatch Logs.

        When updating
        this property, unsetting it doesn't remove the log retention policy. To
        remove the retention policy, set the value to ``INFINITE``.

        default
        :default: logs.RetentionDays.INFINITE

        stability
        :stability: experimental
        """
        return self._values.get('log_retention')

    @builtins.property
    def log_retention_retry_options(self) -> typing.Optional["LogRetentionRetryOptions"]:
        """When log retention is specified, a custom resource attempts to create the CloudWatch log group.

        These options control the retry policy when interacting with CloudWatch APIs.

        default
        :default: - Default AWS SDK retry options.

        stability
        :stability: experimental
        """
        return self._values.get('log_retention_retry_options')

    @builtins.property
    def log_retention_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The IAM role for the Lambda function associated with the custom resource that sets the retention policy.

        default
        :default: - A new role is created.

        stability
        :stability: experimental
        """
        return self._values.get('log_retention_role')

    @builtins.property
    def memory_size(self) -> typing.Optional[jsii.Number]:
        """The amount of memory, in MB, that is allocated to your Lambda function.

        Lambda uses this value to proportionally allocate the amount of CPU
        power. For more information, see Resource Model in the AWS Lambda
        Developer Guide.

        default
        :default: 128

        stability
        :stability: experimental
        """
        return self._values.get('memory_size')

    @builtins.property
    def reserved_concurrent_executions(self) -> typing.Optional[jsii.Number]:
        """The maximum of concurrent executions you want to reserve for the function.

        default
        :default: - No specific limit - account limit.

        see
        :see: https://docs.aws.amazon.com/lambda/latest/dg/concurrent-executions.html
        stability
        :stability: experimental
        """
        return self._values.get('reserved_concurrent_executions')

    @builtins.property
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """Lambda execution role.

        This is the role that will be assumed by the function upon execution.
        It controls the permissions that the function will have. The Role must
        be assumable by the 'lambda.amazonaws.com' service principal.

        The default Role automatically has permissions granted for Lambda execution. If you
        provide a Role, you must add the relevant AWS managed policies yourself.

        The relevant managed policies are "service-role/AWSLambdaBasicExecutionRole" and
        "service-role/AWSLambdaVPCAccessExecutionRole".

        default
        :default:

        - A unique role will be generated for this lambda function.
          Both supplied and generated roles can always be changed by calling ``addToRolePolicy``.

        stability
        :stability: experimental
        """
        return self._values.get('role')

    @builtins.property
    def security_group(self) -> typing.Optional[_ISecurityGroup_d72ab8e8]:
        """What security group to associate with the Lambda's network interfaces. This property is being deprecated, consider using securityGroups instead.

        Only used if 'vpc' is supplied.

        Use securityGroups property instead.
        Function constructor will throw an error if both are specified.

        default
        :default:

        - If the function is placed within a VPC and a security group is
          not specified, either by this or securityGroups prop, a dedicated security
          group will be created for this function.

        deprecated
        :deprecated: - This property is deprecated, use securityGroups instead

        stability
        :stability: deprecated
        """
        return self._values.get('security_group')

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]]:
        """The list of security groups to associate with the Lambda's network interfaces.

        Only used if 'vpc' is supplied.

        default
        :default:

        - If the function is placed within a VPC and a security group is
          not specified, either by this or securityGroup prop, a dedicated security
          group will be created for this function.

        stability
        :stability: experimental
        """
        return self._values.get('security_groups')

    @builtins.property
    def timeout(self) -> typing.Optional[_Duration_5170c158]:
        """The function execution time (in seconds) after which Lambda terminates the function.

        Because the execution time affects cost, set this value
        based on the function's expected execution time.

        default
        :default: Duration.seconds(3)

        stability
        :stability: experimental
        """
        return self._values.get('timeout')

    @builtins.property
    def tracing(self) -> typing.Optional["Tracing"]:
        """Enable AWS X-Ray Tracing for Lambda Function.

        default
        :default: Tracing.Disabled

        stability
        :stability: experimental
        """
        return self._values.get('tracing')

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_3795853f]:
        """VPC network to place Lambda network interfaces.

        Specify this if the Lambda function needs to access resources in a VPC.

        default
        :default: - Function is not placed within a VPC.

        stability
        :stability: experimental
        """
        return self._values.get('vpc')

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_SubnetSelection_36a13cd6]:
        """Where to place the network interfaces within the VPC.

        Only used if 'vpc' is supplied. Note: internet access for Lambdas
        requires a NAT gateway, so picking Public subnets is not allowed.

        default
        :default: - the Vpc default strategy if not specified

        stability
        :stability: experimental
        """
        return self._values.get('vpc_subnets')

    @builtins.property
    def code(self) -> "Code":
        """The source code of your Lambda function.

        You can point to a file in an
        Amazon Simple Storage Service (Amazon S3) bucket or specify your source
        code as inline text.

        stability
        :stability: experimental
        """
        return self._values.get('code')

    @builtins.property
    def handler(self) -> str:
        """The name of the method within your code that Lambda calls to execute your function.

        The format includes the file name. It can also include
        namespaces and other qualifiers, depending on the runtime.
        For more information, see https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-features.html#gettingstarted-features-programmingmodel.

        NOTE: If you specify your source code as inline text by specifying the
        ZipFile property within the Code property, specify index.function_name as
        the handler.

        stability
        :stability: experimental
        """
        return self._values.get('handler')

    @builtins.property
    def runtime(self) -> "Runtime":
        """The runtime environment for the Lambda function that you are uploading.

        For valid values, see the Runtime property in the AWS Lambda Developer
        Guide.

        stability
        :stability: experimental
        """
        return self._values.get('runtime')

    @builtins.property
    def uuid(self) -> str:
        """A unique identifier to identify this lambda.

        The identifier should be unique across all custom resource providers.
        We recommend generating a UUID per provider.

        stability
        :stability: experimental
        """
        return self._values.get('uuid')

    @builtins.property
    def lambda_purpose(self) -> typing.Optional[str]:
        """A descriptive name for the purpose of this Lambda.

        If the Lambda does not have a physical name, this string will be
        reflected its generated name. The combination of lambdaPurpose
        and uuid must be unique.

        default
        :default: SingletonLambda

        stability
        :stability: experimental
        """
        return self._values.get('lambda_purpose')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SingletonFunctionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="monocdk-experiment.aws_lambda.StartingPosition")
class StartingPosition(enum.Enum):
    """The position in the DynamoDB or Kinesis stream where AWS Lambda should start reading.

    stability
    :stability: experimental
    """
    TRIM_HORIZON = "TRIM_HORIZON"
    """Start reading at the last untrimmed record in the shard in the system, which is the oldest data record in the shard.

    stability
    :stability: experimental
    """
    LATEST = "LATEST"
    """Start reading just after the most recent record in the shard, so that you always read the most recent data in the shard.

    stability
    :stability: experimental
    """

@jsii.enum(jsii_type="monocdk-experiment.aws_lambda.Tracing")
class Tracing(enum.Enum):
    """X-Ray Tracing Modes (https://docs.aws.amazon.com/lambda/latest/dg/API_TracingConfig.html).

    stability
    :stability: experimental
    """
    ACTIVE = "ACTIVE"
    """Lambda will respect any tracing header it receives from an upstream service.

    If no tracing header is received, Lambda will call X-Ray for a tracing decision.

    stability
    :stability: experimental
    """
    PASS_THROUGH = "PASS_THROUGH"
    """Lambda will only trace the request from an upstream service if it contains a tracing header with "sampled=1".

    stability
    :stability: experimental
    """
    DISABLED = "DISABLED"
    """Lambda will not trace any request.

    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.VersionAttributes", jsii_struct_bases=[], name_mapping={'lambda_': 'lambda', 'version': 'version'})
class VersionAttributes():
    def __init__(self, *, lambda_: "IFunction", version: str) -> None:
        """
        :param lambda_: The lambda function.
        :param version: The version.

        stability
        :stability: experimental
        """
        self._values = {
            'lambda_': lambda_,
            'version': version,
        }

    @builtins.property
    def lambda_(self) -> "IFunction":
        """The lambda function.

        stability
        :stability: experimental
        """
        return self._values.get('lambda_')

    @builtins.property
    def version(self) -> str:
        """The version.

        stability
        :stability: experimental
        """
        return self._values.get('version')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'VersionAttributes(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.VersionOptions", jsii_struct_bases=[EventInvokeConfigOptions], name_mapping={'max_event_age': 'maxEventAge', 'on_failure': 'onFailure', 'on_success': 'onSuccess', 'retry_attempts': 'retryAttempts', 'code_sha256': 'codeSha256', 'description': 'description', 'provisioned_concurrent_executions': 'provisionedConcurrentExecutions', 'removal_policy': 'removalPolicy'})
class VersionOptions(EventInvokeConfigOptions):
    def __init__(self, *, max_event_age: typing.Optional[_Duration_5170c158]=None, on_failure: typing.Optional["IDestination"]=None, on_success: typing.Optional["IDestination"]=None, retry_attempts: typing.Optional[jsii.Number]=None, code_sha256: typing.Optional[str]=None, description: typing.Optional[str]=None, provisioned_concurrent_executions: typing.Optional[jsii.Number]=None, removal_policy: typing.Optional[_RemovalPolicy_5986e9f3]=None) -> None:
        """Options for ``lambda.Version``.

        :param max_event_age: The maximum age of a request that Lambda sends to a function for processing. Minimum: 60 seconds Maximum: 6 hours Default: Duration.hours(6)
        :param on_failure: The destination for failed invocations. Default: - no destination
        :param on_success: The destination for successful invocations. Default: - no destination
        :param retry_attempts: The maximum number of times to retry when the function returns an error. Minimum: 0 Maximum: 2 Default: 2
        :param code_sha256: SHA256 of the version of the Lambda source code. Specify to validate that you're deploying the right version. Default: No validation is performed
        :param description: Description of the version. Default: Description of the Lambda
        :param provisioned_concurrent_executions: Specifies a provisioned concurrency configuration for a function's version. Default: No provisioned concurrency
        :param removal_policy: Whether to retain old versions of this function when a new version is created. Default: RemovalPolicy.DESTROY

        stability
        :stability: experimental
        """
        self._values = {
        }
        if max_event_age is not None: self._values["max_event_age"] = max_event_age
        if on_failure is not None: self._values["on_failure"] = on_failure
        if on_success is not None: self._values["on_success"] = on_success
        if retry_attempts is not None: self._values["retry_attempts"] = retry_attempts
        if code_sha256 is not None: self._values["code_sha256"] = code_sha256
        if description is not None: self._values["description"] = description
        if provisioned_concurrent_executions is not None: self._values["provisioned_concurrent_executions"] = provisioned_concurrent_executions
        if removal_policy is not None: self._values["removal_policy"] = removal_policy

    @builtins.property
    def max_event_age(self) -> typing.Optional[_Duration_5170c158]:
        """The maximum age of a request that Lambda sends to a function for processing.

        Minimum: 60 seconds
        Maximum: 6 hours

        default
        :default: Duration.hours(6)

        stability
        :stability: experimental
        """
        return self._values.get('max_event_age')

    @builtins.property
    def on_failure(self) -> typing.Optional["IDestination"]:
        """The destination for failed invocations.

        default
        :default: - no destination

        stability
        :stability: experimental
        """
        return self._values.get('on_failure')

    @builtins.property
    def on_success(self) -> typing.Optional["IDestination"]:
        """The destination for successful invocations.

        default
        :default: - no destination

        stability
        :stability: experimental
        """
        return self._values.get('on_success')

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        """The maximum number of times to retry when the function returns an error.

        Minimum: 0
        Maximum: 2

        default
        :default: 2

        stability
        :stability: experimental
        """
        return self._values.get('retry_attempts')

    @builtins.property
    def code_sha256(self) -> typing.Optional[str]:
        """SHA256 of the version of the Lambda source code.

        Specify to validate that you're deploying the right version.

        default
        :default: No validation is performed

        stability
        :stability: experimental
        """
        return self._values.get('code_sha256')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """Description of the version.

        default
        :default: Description of the Lambda

        stability
        :stability: experimental
        """
        return self._values.get('description')

    @builtins.property
    def provisioned_concurrent_executions(self) -> typing.Optional[jsii.Number]:
        """Specifies a provisioned concurrency configuration for a function's version.

        default
        :default: No provisioned concurrency

        stability
        :stability: experimental
        """
        return self._values.get('provisioned_concurrent_executions')

    @builtins.property
    def removal_policy(self) -> typing.Optional[_RemovalPolicy_5986e9f3]:
        """Whether to retain old versions of this function when a new version is created.

        default
        :default: RemovalPolicy.DESTROY

        stability
        :stability: experimental
        """
        return self._values.get('removal_policy')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'VersionOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.VersionProps", jsii_struct_bases=[VersionOptions], name_mapping={'max_event_age': 'maxEventAge', 'on_failure': 'onFailure', 'on_success': 'onSuccess', 'retry_attempts': 'retryAttempts', 'code_sha256': 'codeSha256', 'description': 'description', 'provisioned_concurrent_executions': 'provisionedConcurrentExecutions', 'removal_policy': 'removalPolicy', 'lambda_': 'lambda'})
class VersionProps(VersionOptions):
    def __init__(self, *, max_event_age: typing.Optional[_Duration_5170c158]=None, on_failure: typing.Optional["IDestination"]=None, on_success: typing.Optional["IDestination"]=None, retry_attempts: typing.Optional[jsii.Number]=None, code_sha256: typing.Optional[str]=None, description: typing.Optional[str]=None, provisioned_concurrent_executions: typing.Optional[jsii.Number]=None, removal_policy: typing.Optional[_RemovalPolicy_5986e9f3]=None, lambda_: "IFunction") -> None:
        """Properties for a new Lambda version.

        :param max_event_age: The maximum age of a request that Lambda sends to a function for processing. Minimum: 60 seconds Maximum: 6 hours Default: Duration.hours(6)
        :param on_failure: The destination for failed invocations. Default: - no destination
        :param on_success: The destination for successful invocations. Default: - no destination
        :param retry_attempts: The maximum number of times to retry when the function returns an error. Minimum: 0 Maximum: 2 Default: 2
        :param code_sha256: SHA256 of the version of the Lambda source code. Specify to validate that you're deploying the right version. Default: No validation is performed
        :param description: Description of the version. Default: Description of the Lambda
        :param provisioned_concurrent_executions: Specifies a provisioned concurrency configuration for a function's version. Default: No provisioned concurrency
        :param removal_policy: Whether to retain old versions of this function when a new version is created. Default: RemovalPolicy.DESTROY
        :param lambda_: Function to get the value of.

        stability
        :stability: experimental
        """
        self._values = {
            'lambda_': lambda_,
        }
        if max_event_age is not None: self._values["max_event_age"] = max_event_age
        if on_failure is not None: self._values["on_failure"] = on_failure
        if on_success is not None: self._values["on_success"] = on_success
        if retry_attempts is not None: self._values["retry_attempts"] = retry_attempts
        if code_sha256 is not None: self._values["code_sha256"] = code_sha256
        if description is not None: self._values["description"] = description
        if provisioned_concurrent_executions is not None: self._values["provisioned_concurrent_executions"] = provisioned_concurrent_executions
        if removal_policy is not None: self._values["removal_policy"] = removal_policy

    @builtins.property
    def max_event_age(self) -> typing.Optional[_Duration_5170c158]:
        """The maximum age of a request that Lambda sends to a function for processing.

        Minimum: 60 seconds
        Maximum: 6 hours

        default
        :default: Duration.hours(6)

        stability
        :stability: experimental
        """
        return self._values.get('max_event_age')

    @builtins.property
    def on_failure(self) -> typing.Optional["IDestination"]:
        """The destination for failed invocations.

        default
        :default: - no destination

        stability
        :stability: experimental
        """
        return self._values.get('on_failure')

    @builtins.property
    def on_success(self) -> typing.Optional["IDestination"]:
        """The destination for successful invocations.

        default
        :default: - no destination

        stability
        :stability: experimental
        """
        return self._values.get('on_success')

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        """The maximum number of times to retry when the function returns an error.

        Minimum: 0
        Maximum: 2

        default
        :default: 2

        stability
        :stability: experimental
        """
        return self._values.get('retry_attempts')

    @builtins.property
    def code_sha256(self) -> typing.Optional[str]:
        """SHA256 of the version of the Lambda source code.

        Specify to validate that you're deploying the right version.

        default
        :default: No validation is performed

        stability
        :stability: experimental
        """
        return self._values.get('code_sha256')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """Description of the version.

        default
        :default: Description of the Lambda

        stability
        :stability: experimental
        """
        return self._values.get('description')

    @builtins.property
    def provisioned_concurrent_executions(self) -> typing.Optional[jsii.Number]:
        """Specifies a provisioned concurrency configuration for a function's version.

        default
        :default: No provisioned concurrency

        stability
        :stability: experimental
        """
        return self._values.get('provisioned_concurrent_executions')

    @builtins.property
    def removal_policy(self) -> typing.Optional[_RemovalPolicy_5986e9f3]:
        """Whether to retain old versions of this function when a new version is created.

        default
        :default: RemovalPolicy.DESTROY

        stability
        :stability: experimental
        """
        return self._values.get('removal_policy')

    @builtins.property
    def lambda_(self) -> "IFunction":
        """Function to get the value of.

        stability
        :stability: experimental
        """
        return self._values.get('lambda_')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'VersionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.VersionWeight", jsii_struct_bases=[], name_mapping={'version': 'version', 'weight': 'weight'})
class VersionWeight():
    def __init__(self, *, version: "IVersion", weight: jsii.Number) -> None:
        """A version/weight pair for routing traffic to Lambda functions.

        :param version: The version to route traffic to.
        :param weight: How much weight to assign to this version (0..1).

        stability
        :stability: experimental
        """
        self._values = {
            'version': version,
            'weight': weight,
        }

    @builtins.property
    def version(self) -> "IVersion":
        """The version to route traffic to.

        stability
        :stability: experimental
        """
        return self._values.get('version')

    @builtins.property
    def weight(self) -> jsii.Number:
        """How much weight to assign to this version (0..1).

        stability
        :stability: experimental
        """
        return self._values.get('weight')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'VersionWeight(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.AliasOptions", jsii_struct_bases=[EventInvokeConfigOptions], name_mapping={'max_event_age': 'maxEventAge', 'on_failure': 'onFailure', 'on_success': 'onSuccess', 'retry_attempts': 'retryAttempts', 'additional_versions': 'additionalVersions', 'description': 'description', 'provisioned_concurrent_executions': 'provisionedConcurrentExecutions'})
class AliasOptions(EventInvokeConfigOptions):
    def __init__(self, *, max_event_age: typing.Optional[_Duration_5170c158]=None, on_failure: typing.Optional["IDestination"]=None, on_success: typing.Optional["IDestination"]=None, retry_attempts: typing.Optional[jsii.Number]=None, additional_versions: typing.Optional[typing.List["VersionWeight"]]=None, description: typing.Optional[str]=None, provisioned_concurrent_executions: typing.Optional[jsii.Number]=None) -> None:
        """Options for ``lambda.Alias``.

        :param max_event_age: The maximum age of a request that Lambda sends to a function for processing. Minimum: 60 seconds Maximum: 6 hours Default: Duration.hours(6)
        :param on_failure: The destination for failed invocations. Default: - no destination
        :param on_success: The destination for successful invocations. Default: - no destination
        :param retry_attempts: The maximum number of times to retry when the function returns an error. Minimum: 0 Maximum: 2 Default: 2
        :param additional_versions: Additional versions with individual weights this alias points to. Individual additional version weights specified here should add up to (less than) one. All remaining weight is routed to the default version. For example, the config is Example:: version: "1" additionalVersions: [{ version: "2", weight: 0.05 }] Then 5% of traffic will be routed to function version 2, while the remaining 95% of traffic will be routed to function version 1. Default: No additional versions
        :param description: Description for the alias. Default: No description
        :param provisioned_concurrent_executions: Specifies a provisioned concurrency configuration for a function's alias. Default: No provisioned concurrency

        stability
        :stability: experimental
        """
        self._values = {
        }
        if max_event_age is not None: self._values["max_event_age"] = max_event_age
        if on_failure is not None: self._values["on_failure"] = on_failure
        if on_success is not None: self._values["on_success"] = on_success
        if retry_attempts is not None: self._values["retry_attempts"] = retry_attempts
        if additional_versions is not None: self._values["additional_versions"] = additional_versions
        if description is not None: self._values["description"] = description
        if provisioned_concurrent_executions is not None: self._values["provisioned_concurrent_executions"] = provisioned_concurrent_executions

    @builtins.property
    def max_event_age(self) -> typing.Optional[_Duration_5170c158]:
        """The maximum age of a request that Lambda sends to a function for processing.

        Minimum: 60 seconds
        Maximum: 6 hours

        default
        :default: Duration.hours(6)

        stability
        :stability: experimental
        """
        return self._values.get('max_event_age')

    @builtins.property
    def on_failure(self) -> typing.Optional["IDestination"]:
        """The destination for failed invocations.

        default
        :default: - no destination

        stability
        :stability: experimental
        """
        return self._values.get('on_failure')

    @builtins.property
    def on_success(self) -> typing.Optional["IDestination"]:
        """The destination for successful invocations.

        default
        :default: - no destination

        stability
        :stability: experimental
        """
        return self._values.get('on_success')

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        """The maximum number of times to retry when the function returns an error.

        Minimum: 0
        Maximum: 2

        default
        :default: 2

        stability
        :stability: experimental
        """
        return self._values.get('retry_attempts')

    @builtins.property
    def additional_versions(self) -> typing.Optional[typing.List["VersionWeight"]]:
        """Additional versions with individual weights this alias points to.

        Individual additional version weights specified here should add up to
        (less than) one. All remaining weight is routed to the default
        version.

        For example, the config is Example::

           version: "1"
           additionalVersions: [{ version: "2", weight: 0.05 }]

        Then 5% of traffic will be routed to function version 2, while
        the remaining 95% of traffic will be routed to function version 1.

        default
        :default: No additional versions

        stability
        :stability: experimental
        """
        return self._values.get('additional_versions')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """Description for the alias.

        default
        :default: No description

        stability
        :stability: experimental
        """
        return self._values.get('description')

    @builtins.property
    def provisioned_concurrent_executions(self) -> typing.Optional[jsii.Number]:
        """Specifies a provisioned concurrency configuration for a function's alias.

        default
        :default: No provisioned concurrency

        stability
        :stability: experimental
        """
        return self._values.get('provisioned_concurrent_executions')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AliasOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_lambda.AliasProps", jsii_struct_bases=[AliasOptions], name_mapping={'max_event_age': 'maxEventAge', 'on_failure': 'onFailure', 'on_success': 'onSuccess', 'retry_attempts': 'retryAttempts', 'additional_versions': 'additionalVersions', 'description': 'description', 'provisioned_concurrent_executions': 'provisionedConcurrentExecutions', 'alias_name': 'aliasName', 'version': 'version'})
class AliasProps(AliasOptions):
    def __init__(self, *, max_event_age: typing.Optional[_Duration_5170c158]=None, on_failure: typing.Optional["IDestination"]=None, on_success: typing.Optional["IDestination"]=None, retry_attempts: typing.Optional[jsii.Number]=None, additional_versions: typing.Optional[typing.List["VersionWeight"]]=None, description: typing.Optional[str]=None, provisioned_concurrent_executions: typing.Optional[jsii.Number]=None, alias_name: str, version: "IVersion") -> None:
        """Properties for a new Lambda alias.

        :param max_event_age: The maximum age of a request that Lambda sends to a function for processing. Minimum: 60 seconds Maximum: 6 hours Default: Duration.hours(6)
        :param on_failure: The destination for failed invocations. Default: - no destination
        :param on_success: The destination for successful invocations. Default: - no destination
        :param retry_attempts: The maximum number of times to retry when the function returns an error. Minimum: 0 Maximum: 2 Default: 2
        :param additional_versions: Additional versions with individual weights this alias points to. Individual additional version weights specified here should add up to (less than) one. All remaining weight is routed to the default version. For example, the config is Example:: version: "1" additionalVersions: [{ version: "2", weight: 0.05 }] Then 5% of traffic will be routed to function version 2, while the remaining 95% of traffic will be routed to function version 1. Default: No additional versions
        :param description: Description for the alias. Default: No description
        :param provisioned_concurrent_executions: Specifies a provisioned concurrency configuration for a function's alias. Default: No provisioned concurrency
        :param alias_name: Name of this alias.
        :param version: Function version this alias refers to. Use lambda.addVersion() to obtain a new lambda version to refer to.

        stability
        :stability: experimental
        """
        self._values = {
            'alias_name': alias_name,
            'version': version,
        }
        if max_event_age is not None: self._values["max_event_age"] = max_event_age
        if on_failure is not None: self._values["on_failure"] = on_failure
        if on_success is not None: self._values["on_success"] = on_success
        if retry_attempts is not None: self._values["retry_attempts"] = retry_attempts
        if additional_versions is not None: self._values["additional_versions"] = additional_versions
        if description is not None: self._values["description"] = description
        if provisioned_concurrent_executions is not None: self._values["provisioned_concurrent_executions"] = provisioned_concurrent_executions

    @builtins.property
    def max_event_age(self) -> typing.Optional[_Duration_5170c158]:
        """The maximum age of a request that Lambda sends to a function for processing.

        Minimum: 60 seconds
        Maximum: 6 hours

        default
        :default: Duration.hours(6)

        stability
        :stability: experimental
        """
        return self._values.get('max_event_age')

    @builtins.property
    def on_failure(self) -> typing.Optional["IDestination"]:
        """The destination for failed invocations.

        default
        :default: - no destination

        stability
        :stability: experimental
        """
        return self._values.get('on_failure')

    @builtins.property
    def on_success(self) -> typing.Optional["IDestination"]:
        """The destination for successful invocations.

        default
        :default: - no destination

        stability
        :stability: experimental
        """
        return self._values.get('on_success')

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        """The maximum number of times to retry when the function returns an error.

        Minimum: 0
        Maximum: 2

        default
        :default: 2

        stability
        :stability: experimental
        """
        return self._values.get('retry_attempts')

    @builtins.property
    def additional_versions(self) -> typing.Optional[typing.List["VersionWeight"]]:
        """Additional versions with individual weights this alias points to.

        Individual additional version weights specified here should add up to
        (less than) one. All remaining weight is routed to the default
        version.

        For example, the config is Example::

           version: "1"
           additionalVersions: [{ version: "2", weight: 0.05 }]

        Then 5% of traffic will be routed to function version 2, while
        the remaining 95% of traffic will be routed to function version 1.

        default
        :default: No additional versions

        stability
        :stability: experimental
        """
        return self._values.get('additional_versions')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """Description for the alias.

        default
        :default: No description

        stability
        :stability: experimental
        """
        return self._values.get('description')

    @builtins.property
    def provisioned_concurrent_executions(self) -> typing.Optional[jsii.Number]:
        """Specifies a provisioned concurrency configuration for a function's alias.

        default
        :default: No provisioned concurrency

        stability
        :stability: experimental
        """
        return self._values.get('provisioned_concurrent_executions')

    @builtins.property
    def alias_name(self) -> str:
        """Name of this alias.

        stability
        :stability: experimental
        """
        return self._values.get('alias_name')

    @builtins.property
    def version(self) -> "IVersion":
        """Function version this alias refers to.

        Use lambda.addVersion() to obtain a new lambda version to refer to.

        stability
        :stability: experimental
        """
        return self._values.get('version')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AliasProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class AssetCode(Code, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_lambda.AssetCode"):
    """Lambda code from a local directory.

    stability
    :stability: experimental
    """
    def __init__(self, path: str, *, readers: typing.Optional[typing.List[_IGrantable_0fcfc53a]]=None, source_hash: typing.Optional[str]=None, exclude: typing.Optional[typing.List[str]]=None, follow: typing.Optional[_FollowMode_f74e7125]=None, asset_hash: typing.Optional[str]=None, asset_hash_type: typing.Optional[_AssetHashType_16f7047a]=None, bundling: typing.Optional[_BundlingOptions_0cab5223]=None) -> None:
        """
        :param path: The path to the asset file or directory.
        :param readers: A list of principals that should be able to read this asset from S3. You can use ``asset.grantRead(principal)`` to grant read permissions later. Default: - No principals that can read file asset.
        :param source_hash: Custom hash to use when identifying the specific version of the asset. For consistency, this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be the asset hash. NOTE: the source hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the source hash, you will need to make sure it is updated every time the source changes, or otherwise it is possible that some deployments will not be invalidated. Default: - automatically calculate source hash based on the contents of the source file or directory.
        :param exclude: Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: A strategy for how to handle symlinks. Default: Never
        :param asset_hash: Specify a custom hash for this asset. If ``assetHashType`` is set it must be set to ``AssetHashType.CUSTOM``. For consistency, this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be the asset hash. NOTE: the hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the hash, you will need to make sure it is updated every time the asset changes, or otherwise it is possible that some deployments will not be invalidated. Default: - based on ``assetHashType``
        :param asset_hash_type: Specifies the type of hash to calculate for this asset. If ``assetHash`` is configured, this option must be ``undefined`` or ``AssetHashType.CUSTOM``. Default: - the default is ``AssetHashType.SOURCE``, but if ``assetHash`` is explicitly specified this value defaults to ``AssetHashType.CUSTOM``.
        :param bundling: Bundle the asset by executing a command in a Docker container. The asset path will be mounted at ``/asset-input``. The Docker container is responsible for putting content at ``/asset-output``. The content at ``/asset-output`` will be zipped and used as the final asset. Default: - uploaded as-is to S3 if the asset is a regular file or a .zip file, archived into a .zip file and uploaded to S3 otherwise

        stability
        :stability: experimental
        """
        options = _AssetOptions_ed6c2956(readers=readers, source_hash=source_hash, exclude=exclude, follow=follow, asset_hash=asset_hash, asset_hash_type=asset_hash_type, bundling=bundling)

        jsii.create(AssetCode, self, [path, options])

    @jsii.member(jsii_name="bind")
    def bind(self, scope: _Construct_f50a3f53) -> "CodeConfig":
        """Called when the lambda or layer is initialized to allow this object to bind to the stack, add resources and have fun.

        :param scope: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [scope])

    @jsii.member(jsii_name="bindToResource")
    def bind_to_resource(self, resource: _CfnResource_7760e8e4, *, resource_property: typing.Optional[str]=None) -> None:
        """Called after the CFN function resource has been created to allow the code class to bind to it.

        Specifically it's required to allow assets to add
        metadata for tooling like SAM CLI to be able to find their origins.

        :param resource: -
        :param resource_property: The name of the CloudFormation property to annotate with asset metadata. Default: Code

        stability
        :stability: experimental
        """
        options = ResourceBindOptions(resource_property=resource_property)

        return jsii.invoke(self, "bindToResource", [resource, options])

    @builtins.property
    @jsii.member(jsii_name="isInline")
    def is_inline(self) -> bool:
        """Determines whether this Code is inline code or not.

        stability
        :stability: experimental
        """
        return jsii.get(self, "isInline")

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> str:
        """The path to the asset file or directory.

        stability
        :stability: experimental
        """
        return jsii.get(self, "path")


class CfnParametersCode(Code, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_lambda.CfnParametersCode"):
    """Lambda code defined using 2 CloudFormation parameters.

    Useful when you don't have access to the code of your Lambda from your CDK code, so you can't use Assets,
    and you want to deploy the Lambda in a CodePipeline, using CloudFormation Actions -
    you can fill the parameters using the {@link #assign} method.

    stability
    :stability: experimental
    """
    def __init__(self, *, bucket_name_param: typing.Optional[_CfnParameter_90f1d0df]=None, object_key_param: typing.Optional[_CfnParameter_90f1d0df]=None) -> None:
        """
        :param bucket_name_param: The CloudFormation parameter that represents the name of the S3 Bucket where the Lambda code will be located in. Must be of type 'String'. Default: a new parameter will be created
        :param object_key_param: The CloudFormation parameter that represents the path inside the S3 Bucket where the Lambda code will be located at. Must be of type 'String'. Default: a new parameter will be created

        stability
        :stability: experimental
        """
        props = CfnParametersCodeProps(bucket_name_param=bucket_name_param, object_key_param=object_key_param)

        jsii.create(CfnParametersCode, self, [props])

    @jsii.member(jsii_name="assign")
    def assign(self, *, bucket_name: str, object_key: str, object_version: typing.Optional[str]=None) -> typing.Mapping[str, typing.Any]:
        """Create a parameters map from this instance's CloudFormation parameters.

        It returns a map with 2 keys that correspond to the names of the parameters defined in this Lambda code,
        and as values it contains the appropriate expressions pointing at the provided S3 location
        (most likely, obtained from a CodePipeline Artifact by calling the ``artifact.s3Location`` method).
        The result should be provided to the CloudFormation Action
        that is deploying the Stack that the Lambda with this code is part of,
        in the ``parameterOverrides`` property.

        :param bucket_name: The name of the S3 Bucket the object is in.
        :param object_key: The path inside the Bucket where the object is located at.
        :param object_version: The S3 object version.

        stability
        :stability: experimental
        """
        location = _Location_2d2ff215(bucket_name=bucket_name, object_key=object_key, object_version=object_version)

        return jsii.invoke(self, "assign", [location])

    @jsii.member(jsii_name="bind")
    def bind(self, scope: _Construct_f50a3f53) -> "CodeConfig":
        """Called when the lambda or layer is initialized to allow this object to bind to the stack, add resources and have fun.

        :param scope: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [scope])

    @builtins.property
    @jsii.member(jsii_name="bucketNameParam")
    def bucket_name_param(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "bucketNameParam")

    @builtins.property
    @jsii.member(jsii_name="isInline")
    def is_inline(self) -> bool:
        """Determines whether this Code is inline code or not.

        stability
        :stability: experimental
        """
        return jsii.get(self, "isInline")

    @builtins.property
    @jsii.member(jsii_name="objectKeyParam")
    def object_key_param(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "objectKeyParam")


@jsii.implements(IEventSourceMapping)
class EventSourceMapping(_Resource_884d0774, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_lambda.EventSourceMapping"):
    """Defines a Lambda EventSourceMapping resource.

    Usually, you won't need to define the mapping yourself. This will usually be done by
    event sources. For example, to add an SQS event source to a function::

       import { SqsEventSource } from '@aws-cdk/aws-lambda-event-sources';
       lambda.addEventSource(new SqsEventSource(sqs));

    The ``SqsEventSource`` class will automatically create the mapping, and will also
    modify the Lambda's execution role so it can consume messages from the queue.

    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, target: "IFunction", event_source_arn: str, batch_size: typing.Optional[jsii.Number]=None, bisect_batch_on_error: typing.Optional[bool]=None, enabled: typing.Optional[bool]=None, max_batching_window: typing.Optional[_Duration_5170c158]=None, max_record_age: typing.Optional[_Duration_5170c158]=None, on_failure: typing.Optional["IEventSourceDlq"]=None, parallelization_factor: typing.Optional[jsii.Number]=None, retry_attempts: typing.Optional[jsii.Number]=None, starting_position: typing.Optional["StartingPosition"]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param target: The target AWS Lambda function.
        :param event_source_arn: The Amazon Resource Name (ARN) of the event source. Any record added to this stream can invoke the Lambda function.
        :param batch_size: The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: Minimum value of 1. Maximum value of 10000. Default: - Amazon Kinesis and Amazon DynamoDB is 100 records. Both the default and maximum for Amazon SQS are 10 messages.
        :param bisect_batch_on_error: If the function returns an error, split the batch in two and retry. Default: false
        :param enabled: Set to false to disable the event source upon creation. Default: true
        :param max_batching_window: The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5) Default: Duration.seconds(0)
        :param max_record_age: The maximum age of a record that Lambda sends to a function for processing. Valid Range: - Minimum value of 60 seconds - Maximum value of 7 days Default: Duration.days(7)
        :param on_failure: An Amazon SQS queue or Amazon SNS topic destination for discarded records. Default: discarded records are ignored
        :param parallelization_factor: The number of batches to process from each shard concurrently. Valid Range: - Minimum value of 1 - Maximum value of 10 Default: 1
        :param retry_attempts: The maximum number of times to retry when the function returns an error. Valid Range: - Minimum value of 0 - Maximum value of 10000 Default: 10000
        :param starting_position: The position in the DynamoDB or Kinesis stream where AWS Lambda should start reading. Default: - Required for Amazon Kinesis and Amazon DynamoDB Streams sources.

        stability
        :stability: experimental
        """
        props = EventSourceMappingProps(target=target, event_source_arn=event_source_arn, batch_size=batch_size, bisect_batch_on_error=bisect_batch_on_error, enabled=enabled, max_batching_window=max_batching_window, max_record_age=max_record_age, on_failure=on_failure, parallelization_factor=parallelization_factor, retry_attempts=retry_attempts, starting_position=starting_position)

        jsii.create(EventSourceMapping, self, [scope, id, props])

    @jsii.member(jsii_name="fromEventSourceMappingId")
    @builtins.classmethod
    def from_event_source_mapping_id(cls, scope: _Construct_f50a3f53, id: str, event_source_mapping_id: str) -> "IEventSourceMapping":
        """Import an event source into this stack from its event source id.

        :param scope: -
        :param id: -
        :param event_source_mapping_id: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromEventSourceMappingId", [scope, id, event_source_mapping_id])

    @builtins.property
    @jsii.member(jsii_name="eventSourceMappingId")
    def event_source_mapping_id(self) -> str:
        """The identifier for this EventSourceMapping.

        stability
        :stability: experimental
        """
        return jsii.get(self, "eventSourceMappingId")


@jsii.implements(IFunction)
class FunctionBase(_Resource_884d0774, metaclass=jsii.JSIIAbstractClass, jsii_type="monocdk-experiment.aws_lambda.FunctionBase"):
    """
    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _FunctionBaseProxy

    def __init__(self, scope: _Construct_f50a3f53, id: str, *, physical_name: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time

        stability
        :stability: experimental
        """
        props = _ResourceProps_92be6f66(physical_name=physical_name)

        jsii.create(FunctionBase, self, [scope, id, props])

    @jsii.member(jsii_name="addEventSource")
    def add_event_source(self, source: "IEventSource") -> None:
        """Adds an event source to this function.

        Event sources are implemented in the @aws-cdk/aws-lambda-event-sources module.

        The following example adds an SQS Queue as an event source::

            import { SqsEventSource } from '@aws-cdk/aws-lambda-event-sources';
            myFunction.addEventSource(new SqsEventSource(myQueue));

        :param source: The event source to bind to this function.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addEventSource", [source])

    @jsii.member(jsii_name="addEventSourceMapping")
    def add_event_source_mapping(self, id: str, *, event_source_arn: str, batch_size: typing.Optional[jsii.Number]=None, bisect_batch_on_error: typing.Optional[bool]=None, enabled: typing.Optional[bool]=None, max_batching_window: typing.Optional[_Duration_5170c158]=None, max_record_age: typing.Optional[_Duration_5170c158]=None, on_failure: typing.Optional["IEventSourceDlq"]=None, parallelization_factor: typing.Optional[jsii.Number]=None, retry_attempts: typing.Optional[jsii.Number]=None, starting_position: typing.Optional["StartingPosition"]=None) -> "EventSourceMapping":
        """Adds an event source that maps to this AWS Lambda function.

        :param id: -
        :param event_source_arn: The Amazon Resource Name (ARN) of the event source. Any record added to this stream can invoke the Lambda function.
        :param batch_size: The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: Minimum value of 1. Maximum value of 10000. Default: - Amazon Kinesis and Amazon DynamoDB is 100 records. Both the default and maximum for Amazon SQS are 10 messages.
        :param bisect_batch_on_error: If the function returns an error, split the batch in two and retry. Default: false
        :param enabled: Set to false to disable the event source upon creation. Default: true
        :param max_batching_window: The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5) Default: Duration.seconds(0)
        :param max_record_age: The maximum age of a record that Lambda sends to a function for processing. Valid Range: - Minimum value of 60 seconds - Maximum value of 7 days Default: Duration.days(7)
        :param on_failure: An Amazon SQS queue or Amazon SNS topic destination for discarded records. Default: discarded records are ignored
        :param parallelization_factor: The number of batches to process from each shard concurrently. Valid Range: - Minimum value of 1 - Maximum value of 10 Default: 1
        :param retry_attempts: The maximum number of times to retry when the function returns an error. Valid Range: - Minimum value of 0 - Maximum value of 10000 Default: 10000
        :param starting_position: The position in the DynamoDB or Kinesis stream where AWS Lambda should start reading. Default: - Required for Amazon Kinesis and Amazon DynamoDB Streams sources.

        stability
        :stability: experimental
        """
        options = EventSourceMappingOptions(event_source_arn=event_source_arn, batch_size=batch_size, bisect_batch_on_error=bisect_batch_on_error, enabled=enabled, max_batching_window=max_batching_window, max_record_age=max_record_age, on_failure=on_failure, parallelization_factor=parallelization_factor, retry_attempts=retry_attempts, starting_position=starting_position)

        return jsii.invoke(self, "addEventSourceMapping", [id, options])

    @jsii.member(jsii_name="addPermission")
    def add_permission(self, id: str, *, principal: _IPrincipal_97126874, action: typing.Optional[str]=None, event_source_token: typing.Optional[str]=None, scope: typing.Optional[_Construct_f50a3f53]=None, source_account: typing.Optional[str]=None, source_arn: typing.Optional[str]=None) -> None:
        """Adds a permission to the Lambda resource policy.

        :param id: The id ƒor the permission construct.
        :param principal: The entity for which you are granting permission to invoke the Lambda function. This entity can be any valid AWS service principal, such as s3.amazonaws.com or sns.amazonaws.com, or, if you are granting cross-account permission, an AWS account ID. For example, you might want to allow a custom application in another AWS account to push events to Lambda by invoking your function. The principal can be either an AccountPrincipal or a ServicePrincipal.
        :param action: The Lambda actions that you want to allow in this statement. For example, you can specify lambda:CreateFunction to specify a certain action, or use a wildcard (``lambda:*``) to grant permission to all Lambda actions. For a list of actions, see Actions and Condition Context Keys for AWS Lambda in the IAM User Guide. Default: 'lambda:InvokeFunction'
        :param event_source_token: A unique token that must be supplied by the principal invoking the function. Default: The caller would not need to present a token.
        :param scope: The scope to which the permission constructs be attached. The default is the Lambda function construct itself, but this would need to be different in cases such as cross-stack references where the Permissions would need to sit closer to the consumer of this permission (i.e., the caller). Default: - The instance of lambda.IFunction
        :param source_account: The AWS account ID (without hyphens) of the source owner. For example, if you specify an S3 bucket in the SourceArn property, this value is the bucket owner's account ID. You can use this property to ensure that all source principals are owned by a specific account.
        :param source_arn: The ARN of a resource that is invoking your function. When granting Amazon Simple Storage Service (Amazon S3) permission to invoke your function, specify this property with the bucket ARN as its value. This ensures that events generated only from the specified bucket, not just any bucket from any AWS account that creates a mapping to your function, can invoke the function.

        see
        :see: Permission for details.
        stability
        :stability: experimental
        """
        permission = Permission(principal=principal, action=action, event_source_token=event_source_token, scope=scope, source_account=source_account, source_arn=source_arn)

        return jsii.invoke(self, "addPermission", [id, permission])

    @jsii.member(jsii_name="addToRolePolicy")
    def add_to_role_policy(self, statement: _PolicyStatement_f75dc775) -> None:
        """Adds a statement to the IAM role assumed by the instance.

        :param statement: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addToRolePolicy", [statement])

    @jsii.member(jsii_name="configureAsyncInvoke")
    def configure_async_invoke(self, *, max_event_age: typing.Optional[_Duration_5170c158]=None, on_failure: typing.Optional["IDestination"]=None, on_success: typing.Optional["IDestination"]=None, retry_attempts: typing.Optional[jsii.Number]=None) -> None:
        """Configures options for asynchronous invocation.

        :param max_event_age: The maximum age of a request that Lambda sends to a function for processing. Minimum: 60 seconds Maximum: 6 hours Default: Duration.hours(6)
        :param on_failure: The destination for failed invocations. Default: - no destination
        :param on_success: The destination for successful invocations. Default: - no destination
        :param retry_attempts: The maximum number of times to retry when the function returns an error. Minimum: 0 Maximum: 2 Default: 2

        stability
        :stability: experimental
        """
        options = EventInvokeConfigOptions(max_event_age=max_event_age, on_failure=on_failure, on_success=on_success, retry_attempts=retry_attempts)

        return jsii.invoke(self, "configureAsyncInvoke", [options])

    @jsii.member(jsii_name="grantInvoke")
    def grant_invoke(self, grantee: _IGrantable_0fcfc53a) -> _Grant_96af6d2d:
        """Grant the given identity permissions to invoke this Lambda.

        :param grantee: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "grantInvoke", [grantee])

    @jsii.member(jsii_name="metric")
    def metric(self, metric_name: str, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[_Duration_5170c158]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[_Unit_e1b74f3c]=None) -> _Metric_53e89548:
        """Return the given named metric for this Function.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metric", [metric_name, props])

    @jsii.member(jsii_name="metricDuration")
    def metric_duration(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[_Duration_5170c158]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[_Unit_e1b74f3c]=None) -> _Metric_53e89548:
        """How long execution of this Lambda takes.

        Average over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricDuration", [props])

    @jsii.member(jsii_name="metricErrors")
    def metric_errors(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[_Duration_5170c158]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[_Unit_e1b74f3c]=None) -> _Metric_53e89548:
        """How many invocations of this Lambda fail.

        Sum over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricErrors", [props])

    @jsii.member(jsii_name="metricInvocations")
    def metric_invocations(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[_Duration_5170c158]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[_Unit_e1b74f3c]=None) -> _Metric_53e89548:
        """How often this Lambda is invoked.

        Sum over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricInvocations", [props])

    @jsii.member(jsii_name="metricThrottles")
    def metric_throttles(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[_Duration_5170c158]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[_Unit_e1b74f3c]=None) -> _Metric_53e89548:
        """How often this Lambda is throttled.

        Sum over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metricThrottles", [props])

    @builtins.property
    @jsii.member(jsii_name="canCreatePermissions")
    @abc.abstractmethod
    def _can_create_permissions(self) -> bool:
        """Whether the addPermission() call adds any permissions.

        True for new Lambdas, false for imported Lambdas (they might live in different accounts).

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _Connections_231f38b5:
        """Access the Connections object.

        Will fail if not a VPC-enabled Lambda Function

        stability
        :stability: experimental
        """
        return jsii.get(self, "connections")

    @builtins.property
    @jsii.member(jsii_name="functionArn")
    @abc.abstractmethod
    def function_arn(self) -> str:
        """The ARN fo the function.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="functionName")
    @abc.abstractmethod
    def function_name(self) -> str:
        """The name of the function.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    @abc.abstractmethod
    def grant_principal(self) -> _IPrincipal_97126874:
        """The principal this Lambda Function is running as.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="isBoundToVpc")
    def is_bound_to_vpc(self) -> bool:
        """Whether or not this Lambda function was bound to a VPC.

        If this is is ``false``, trying to access the ``connections`` object will fail.

        stability
        :stability: experimental
        """
        return jsii.get(self, "isBoundToVpc")

    @builtins.property
    @jsii.member(jsii_name="latestVersion")
    def latest_version(self) -> "IVersion":
        """The ``$LATEST`` version of this function.

        Note that this is reference to a non-specific AWS Lambda version, which
        means the function this version refers to can return different results in
        different invocations.

        To obtain a reference to an explicit version which references the current
        function configuration, use ``lambdaFunction.currentVersion`` instead.

        stability
        :stability: experimental
        """
        return jsii.get(self, "latestVersion")

    @builtins.property
    @jsii.member(jsii_name="permissionsNode")
    @abc.abstractmethod
    def permissions_node(self) -> _ConstructNode_6884f5de:
        """The construct node where permissions are attached.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="role")
    @abc.abstractmethod
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The IAM role associated with this function.

        Undefined if the function was imported without a role.

        stability
        :stability: experimental
        """
        ...


class _FunctionBaseProxy(FunctionBase, jsii.proxy_for(_Resource_884d0774)):
    @builtins.property
    @jsii.member(jsii_name="canCreatePermissions")
    def _can_create_permissions(self) -> bool:
        """Whether the addPermission() call adds any permissions.

        True for new Lambdas, false for imported Lambdas (they might live in different accounts).

        stability
        :stability: experimental
        """
        return jsii.get(self, "canCreatePermissions")

    @builtins.property
    @jsii.member(jsii_name="functionArn")
    def function_arn(self) -> str:
        """The ARN fo the function.

        stability
        :stability: experimental
        """
        return jsii.get(self, "functionArn")

    @builtins.property
    @jsii.member(jsii_name="functionName")
    def function_name(self) -> str:
        """The name of the function.

        stability
        :stability: experimental
        """
        return jsii.get(self, "functionName")

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> _IPrincipal_97126874:
        """The principal this Lambda Function is running as.

        stability
        :stability: experimental
        """
        return jsii.get(self, "grantPrincipal")

    @builtins.property
    @jsii.member(jsii_name="permissionsNode")
    def permissions_node(self) -> _ConstructNode_6884f5de:
        """The construct node where permissions are attached.

        stability
        :stability: experimental
        """
        return jsii.get(self, "permissionsNode")

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The IAM role associated with this function.

        Undefined if the function was imported without a role.

        stability
        :stability: experimental
        """
        return jsii.get(self, "role")


@jsii.interface(jsii_type="monocdk-experiment.aws_lambda.IAlias")
class IAlias(IFunction, jsii.compat.Protocol):
    """
    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IAliasProxy

    @builtins.property
    @jsii.member(jsii_name="aliasName")
    def alias_name(self) -> str:
        """Name of this alias.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> "IVersion":
        """The underlying Lambda function version.

        stability
        :stability: experimental
        """
        ...


class _IAliasProxy(jsii.proxy_for(IFunction)):
    """
    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_lambda.IAlias"
    @builtins.property
    @jsii.member(jsii_name="aliasName")
    def alias_name(self) -> str:
        """Name of this alias.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "aliasName")

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> "IVersion":
        """The underlying Lambda function version.

        stability
        :stability: experimental
        """
        return jsii.get(self, "version")


class QualifiedFunctionBase(FunctionBase, metaclass=jsii.JSIIAbstractClass, jsii_type="monocdk-experiment.aws_lambda.QualifiedFunctionBase"):
    """
    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _QualifiedFunctionBaseProxy

    def __init__(self, scope: _Construct_f50a3f53, id: str, *, physical_name: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time

        stability
        :stability: experimental
        """
        props = _ResourceProps_92be6f66(physical_name=physical_name)

        jsii.create(QualifiedFunctionBase, self, [scope, id, props])

    @jsii.member(jsii_name="configureAsyncInvoke")
    def configure_async_invoke(self, *, max_event_age: typing.Optional[_Duration_5170c158]=None, on_failure: typing.Optional["IDestination"]=None, on_success: typing.Optional["IDestination"]=None, retry_attempts: typing.Optional[jsii.Number]=None) -> None:
        """Configures options for asynchronous invocation.

        :param max_event_age: The maximum age of a request that Lambda sends to a function for processing. Minimum: 60 seconds Maximum: 6 hours Default: Duration.hours(6)
        :param on_failure: The destination for failed invocations. Default: - no destination
        :param on_success: The destination for successful invocations. Default: - no destination
        :param retry_attempts: The maximum number of times to retry when the function returns an error. Minimum: 0 Maximum: 2 Default: 2

        stability
        :stability: experimental
        """
        options = EventInvokeConfigOptions(max_event_age=max_event_age, on_failure=on_failure, on_success=on_success, retry_attempts=retry_attempts)

        return jsii.invoke(self, "configureAsyncInvoke", [options])

    @builtins.property
    @jsii.member(jsii_name="lambda")
    @abc.abstractmethod
    def lambda_(self) -> "IFunction":
        """
        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="latestVersion")
    def latest_version(self) -> "IVersion":
        """The ``$LATEST`` version of this function.

        Note that this is reference to a non-specific AWS Lambda version, which
        means the function this version refers to can return different results in
        different invocations.

        To obtain a reference to an explicit version which references the current
        function configuration, use ``lambdaFunction.currentVersion`` instead.

        stability
        :stability: experimental
        """
        return jsii.get(self, "latestVersion")

    @builtins.property
    @jsii.member(jsii_name="permissionsNode")
    def permissions_node(self) -> _ConstructNode_6884f5de:
        """The construct node where permissions are attached.

        stability
        :stability: experimental
        """
        return jsii.get(self, "permissionsNode")

    @builtins.property
    @jsii.member(jsii_name="qualifier")
    @abc.abstractmethod
    def _qualifier(self) -> str:
        """The qualifier of the version or alias of this function.

        A qualifier is the identifier that's appended to a version or alias ARN.

        see
        :see: https://docs.aws.amazon.com/lambda/latest/dg/API_GetFunctionConfiguration.html#API_GetFunctionConfiguration_RequestParameters
        stability
        :stability: experimental
        """
        ...


class _QualifiedFunctionBaseProxy(QualifiedFunctionBase, jsii.proxy_for(FunctionBase)):
    @builtins.property
    @jsii.member(jsii_name="lambda")
    def lambda_(self) -> "IFunction":
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "lambda")

    @builtins.property
    @jsii.member(jsii_name="qualifier")
    def _qualifier(self) -> str:
        """The qualifier of the version or alias of this function.

        A qualifier is the identifier that's appended to a version or alias ARN.

        see
        :see: https://docs.aws.amazon.com/lambda/latest/dg/API_GetFunctionConfiguration.html#API_GetFunctionConfiguration_RequestParameters
        stability
        :stability: experimental
        """
        return jsii.get(self, "qualifier")


class SingletonFunction(FunctionBase, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_lambda.SingletonFunction"):
    """A Lambda that will only ever be added to a stack once.

    This construct is a way to guarantee that the lambda function will be guaranteed to be part of the stack,
    once and only once, irrespective of how many times the construct is declared to be part of the stack.
    This is guaranteed as long as the ``uuid`` property and the optional ``lambdaPurpose`` property stay the same
    whenever they're declared into the stack.

    stability
    :stability: experimental
    resource:
    :resource:: AWS::Lambda::Function
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, uuid: str, lambda_purpose: typing.Optional[str]=None, code: "Code", handler: str, runtime: "Runtime", allow_all_outbound: typing.Optional[bool]=None, current_version_options: typing.Optional["VersionOptions"]=None, dead_letter_queue: typing.Optional[_IQueue_b743f559]=None, dead_letter_queue_enabled: typing.Optional[bool]=None, description: typing.Optional[str]=None, environment: typing.Optional[typing.Mapping[str, str]]=None, events: typing.Optional[typing.List["IEventSource"]]=None, function_name: typing.Optional[str]=None, initial_policy: typing.Optional[typing.List[_PolicyStatement_f75dc775]]=None, layers: typing.Optional[typing.List["ILayerVersion"]]=None, log_retention: typing.Optional[_RetentionDays_bdc7ad1f]=None, log_retention_retry_options: typing.Optional["LogRetentionRetryOptions"]=None, log_retention_role: typing.Optional[_IRole_e69bbae4]=None, memory_size: typing.Optional[jsii.Number]=None, reserved_concurrent_executions: typing.Optional[jsii.Number]=None, role: typing.Optional[_IRole_e69bbae4]=None, security_group: typing.Optional[_ISecurityGroup_d72ab8e8]=None, security_groups: typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]]=None, timeout: typing.Optional[_Duration_5170c158]=None, tracing: typing.Optional["Tracing"]=None, vpc: typing.Optional[_IVpc_3795853f]=None, vpc_subnets: typing.Optional[_SubnetSelection_36a13cd6]=None, max_event_age: typing.Optional[_Duration_5170c158]=None, on_failure: typing.Optional["IDestination"]=None, on_success: typing.Optional["IDestination"]=None, retry_attempts: typing.Optional[jsii.Number]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param uuid: A unique identifier to identify this lambda. The identifier should be unique across all custom resource providers. We recommend generating a UUID per provider.
        :param lambda_purpose: A descriptive name for the purpose of this Lambda. If the Lambda does not have a physical name, this string will be reflected its generated name. The combination of lambdaPurpose and uuid must be unique. Default: SingletonLambda
        :param code: The source code of your Lambda function. You can point to a file in an Amazon Simple Storage Service (Amazon S3) bucket or specify your source code as inline text.
        :param handler: The name of the method within your code that Lambda calls to execute your function. The format includes the file name. It can also include namespaces and other qualifiers, depending on the runtime. For more information, see https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-features.html#gettingstarted-features-programmingmodel. NOTE: If you specify your source code as inline text by specifying the ZipFile property within the Code property, specify index.function_name as the handler.
        :param runtime: The runtime environment for the Lambda function that you are uploading. For valid values, see the Runtime property in the AWS Lambda Developer Guide.
        :param allow_all_outbound: Whether to allow the Lambda to send all network traffic. If set to false, you must individually add traffic rules to allow the Lambda to connect to network targets. Default: true
        :param current_version_options: Options for the ``lambda.Version`` resource automatically created by the ``fn.currentVersion`` method. Default: - default options as described in ``VersionOptions``
        :param dead_letter_queue: The SQS queue to use if DLQ is enabled. Default: - SQS queue with 14 day retention period if ``deadLetterQueueEnabled`` is ``true``
        :param dead_letter_queue_enabled: Enabled DLQ. If ``deadLetterQueue`` is undefined, an SQS queue with default options will be defined for your Function. Default: - false unless ``deadLetterQueue`` is set, which implies DLQ is enabled.
        :param description: A description of the function. Default: - No description.
        :param environment: Key-value pairs that Lambda caches and makes available for your Lambda functions. Use environment variables to apply configuration changes, such as test and production environment configurations, without changing your Lambda function source code. Default: - No environment variables.
        :param events: Event sources for this function. You can also add event sources using ``addEventSource``. Default: - No event sources.
        :param function_name: A name for the function. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the function's name. For more information, see Name Type.
        :param initial_policy: Initial policy statements to add to the created Lambda Role. You can call ``addToRolePolicy`` to the created lambda to add statements post creation. Default: - No policy statements are added to the created Lambda role.
        :param layers: A list of layers to add to the function's execution environment. You can configure your Lambda function to pull in additional code during initialization in the form of layers. Layers are packages of libraries or other dependencies that can be used by mulitple functions. Default: - No layers.
        :param log_retention: The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.INFINITE
        :param log_retention_retry_options: When log retention is specified, a custom resource attempts to create the CloudWatch log group. These options control the retry policy when interacting with CloudWatch APIs. Default: - Default AWS SDK retry options.
        :param log_retention_role: The IAM role for the Lambda function associated with the custom resource that sets the retention policy. Default: - A new role is created.
        :param memory_size: The amount of memory, in MB, that is allocated to your Lambda function. Lambda uses this value to proportionally allocate the amount of CPU power. For more information, see Resource Model in the AWS Lambda Developer Guide. Default: 128
        :param reserved_concurrent_executions: The maximum of concurrent executions you want to reserve for the function. Default: - No specific limit - account limit.
        :param role: Lambda execution role. This is the role that will be assumed by the function upon execution. It controls the permissions that the function will have. The Role must be assumable by the 'lambda.amazonaws.com' service principal. The default Role automatically has permissions granted for Lambda execution. If you provide a Role, you must add the relevant AWS managed policies yourself. The relevant managed policies are "service-role/AWSLambdaBasicExecutionRole" and "service-role/AWSLambdaVPCAccessExecutionRole". Default: - A unique role will be generated for this lambda function. Both supplied and generated roles can always be changed by calling ``addToRolePolicy``.
        :param security_group: What security group to associate with the Lambda's network interfaces. This property is being deprecated, consider using securityGroups instead. Only used if 'vpc' is supplied. Use securityGroups property instead. Function constructor will throw an error if both are specified. Default: - If the function is placed within a VPC and a security group is not specified, either by this or securityGroups prop, a dedicated security group will be created for this function.
        :param security_groups: The list of security groups to associate with the Lambda's network interfaces. Only used if 'vpc' is supplied. Default: - If the function is placed within a VPC and a security group is not specified, either by this or securityGroup prop, a dedicated security group will be created for this function.
        :param timeout: The function execution time (in seconds) after which Lambda terminates the function. Because the execution time affects cost, set this value based on the function's expected execution time. Default: Duration.seconds(3)
        :param tracing: Enable AWS X-Ray Tracing for Lambda Function. Default: Tracing.Disabled
        :param vpc: VPC network to place Lambda network interfaces. Specify this if the Lambda function needs to access resources in a VPC. Default: - Function is not placed within a VPC.
        :param vpc_subnets: Where to place the network interfaces within the VPC. Only used if 'vpc' is supplied. Note: internet access for Lambdas requires a NAT gateway, so picking Public subnets is not allowed. Default: - the Vpc default strategy if not specified
        :param max_event_age: The maximum age of a request that Lambda sends to a function for processing. Minimum: 60 seconds Maximum: 6 hours Default: Duration.hours(6)
        :param on_failure: The destination for failed invocations. Default: - no destination
        :param on_success: The destination for successful invocations. Default: - no destination
        :param retry_attempts: The maximum number of times to retry when the function returns an error. Minimum: 0 Maximum: 2 Default: 2

        stability
        :stability: experimental
        """
        props = SingletonFunctionProps(uuid=uuid, lambda_purpose=lambda_purpose, code=code, handler=handler, runtime=runtime, allow_all_outbound=allow_all_outbound, current_version_options=current_version_options, dead_letter_queue=dead_letter_queue, dead_letter_queue_enabled=dead_letter_queue_enabled, description=description, environment=environment, events=events, function_name=function_name, initial_policy=initial_policy, layers=layers, log_retention=log_retention, log_retention_retry_options=log_retention_retry_options, log_retention_role=log_retention_role, memory_size=memory_size, reserved_concurrent_executions=reserved_concurrent_executions, role=role, security_group=security_group, security_groups=security_groups, timeout=timeout, tracing=tracing, vpc=vpc, vpc_subnets=vpc_subnets, max_event_age=max_event_age, on_failure=on_failure, on_success=on_success, retry_attempts=retry_attempts)

        jsii.create(SingletonFunction, self, [scope, id, props])

    @jsii.member(jsii_name="addDependency")
    def add_dependency(self, *up: _IDependable_4fc803f7) -> None:
        """Using node.addDependency() does not work on this method as the underlying lambda function is modeled as a singleton across the stack. Use this method instead to declare dependencies.

        :param up: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addDependency", [*up])

    @jsii.member(jsii_name="addPermission")
    def add_permission(self, name: str, *, principal: _IPrincipal_97126874, action: typing.Optional[str]=None, event_source_token: typing.Optional[str]=None, scope: typing.Optional[_Construct_f50a3f53]=None, source_account: typing.Optional[str]=None, source_arn: typing.Optional[str]=None) -> None:
        """Adds a permission to the Lambda resource policy.

        :param name: -
        :param principal: The entity for which you are granting permission to invoke the Lambda function. This entity can be any valid AWS service principal, such as s3.amazonaws.com or sns.amazonaws.com, or, if you are granting cross-account permission, an AWS account ID. For example, you might want to allow a custom application in another AWS account to push events to Lambda by invoking your function. The principal can be either an AccountPrincipal or a ServicePrincipal.
        :param action: The Lambda actions that you want to allow in this statement. For example, you can specify lambda:CreateFunction to specify a certain action, or use a wildcard (``lambda:*``) to grant permission to all Lambda actions. For a list of actions, see Actions and Condition Context Keys for AWS Lambda in the IAM User Guide. Default: 'lambda:InvokeFunction'
        :param event_source_token: A unique token that must be supplied by the principal invoking the function. Default: The caller would not need to present a token.
        :param scope: The scope to which the permission constructs be attached. The default is the Lambda function construct itself, but this would need to be different in cases such as cross-stack references where the Permissions would need to sit closer to the consumer of this permission (i.e., the caller). Default: - The instance of lambda.IFunction
        :param source_account: The AWS account ID (without hyphens) of the source owner. For example, if you specify an S3 bucket in the SourceArn property, this value is the bucket owner's account ID. You can use this property to ensure that all source principals are owned by a specific account.
        :param source_arn: The ARN of a resource that is invoking your function. When granting Amazon Simple Storage Service (Amazon S3) permission to invoke your function, specify this property with the bucket ARN as its value. This ensures that events generated only from the specified bucket, not just any bucket from any AWS account that creates a mapping to your function, can invoke the function.

        stability
        :stability: experimental
        """
        permission = Permission(principal=principal, action=action, event_source_token=event_source_token, scope=scope, source_account=source_account, source_arn=source_arn)

        return jsii.invoke(self, "addPermission", [name, permission])

    @jsii.member(jsii_name="dependOn")
    def depend_on(self, down: _IConstruct_db0cc7e3) -> None:
        """The SingletonFunction construct cannot be added as a dependency of another construct using node.addDependency(). Use this method instead to declare this as a dependency of another construct.

        :param down: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "dependOn", [down])

    @builtins.property
    @jsii.member(jsii_name="canCreatePermissions")
    def _can_create_permissions(self) -> bool:
        """Whether the addPermission() call adds any permissions.

        True for new Lambdas, false for imported Lambdas (they might live in different accounts).

        stability
        :stability: experimental
        """
        return jsii.get(self, "canCreatePermissions")

    @builtins.property
    @jsii.member(jsii_name="functionArn")
    def function_arn(self) -> str:
        """The ARN fo the function.

        stability
        :stability: experimental
        """
        return jsii.get(self, "functionArn")

    @builtins.property
    @jsii.member(jsii_name="functionName")
    def function_name(self) -> str:
        """The name of the function.

        stability
        :stability: experimental
        """
        return jsii.get(self, "functionName")

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> _IPrincipal_97126874:
        """The principal this Lambda Function is running as.

        stability
        :stability: experimental
        """
        return jsii.get(self, "grantPrincipal")

    @builtins.property
    @jsii.member(jsii_name="permissionsNode")
    def permissions_node(self) -> _ConstructNode_6884f5de:
        """The construct node where permissions are attached.

        stability
        :stability: experimental
        """
        return jsii.get(self, "permissionsNode")

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The IAM role associated with this function.

        Undefined if the function was imported without a role.

        stability
        :stability: experimental
        """
        return jsii.get(self, "role")


@jsii.implements(IVersion)
class Version(QualifiedFunctionBase, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_lambda.Version"):
    """A single newly-deployed version of a Lambda function.

    This object exists to--at deploy time--query the "then-current" version of
    the Lambda function that it refers to. This Version object can then be
    used in ``Alias`` to refer to a particular deployment of a Lambda.

    This means that for every new update you deploy to your Lambda (using the
    CDK and Aliases), you must always create a new Version object. In
    particular, it must have a different name, so that a new resource is
    created.

    If you want to ensure that you're associating the right version with
    the right deployment, specify the ``codeSha256`` property while
    creating the `Version.

    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, lambda_: "IFunction", code_sha256: typing.Optional[str]=None, description: typing.Optional[str]=None, provisioned_concurrent_executions: typing.Optional[jsii.Number]=None, removal_policy: typing.Optional[_RemovalPolicy_5986e9f3]=None, max_event_age: typing.Optional[_Duration_5170c158]=None, on_failure: typing.Optional["IDestination"]=None, on_success: typing.Optional["IDestination"]=None, retry_attempts: typing.Optional[jsii.Number]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param lambda_: Function to get the value of.
        :param code_sha256: SHA256 of the version of the Lambda source code. Specify to validate that you're deploying the right version. Default: No validation is performed
        :param description: Description of the version. Default: Description of the Lambda
        :param provisioned_concurrent_executions: Specifies a provisioned concurrency configuration for a function's version. Default: No provisioned concurrency
        :param removal_policy: Whether to retain old versions of this function when a new version is created. Default: RemovalPolicy.DESTROY
        :param max_event_age: The maximum age of a request that Lambda sends to a function for processing. Minimum: 60 seconds Maximum: 6 hours Default: Duration.hours(6)
        :param on_failure: The destination for failed invocations. Default: - no destination
        :param on_success: The destination for successful invocations. Default: - no destination
        :param retry_attempts: The maximum number of times to retry when the function returns an error. Minimum: 0 Maximum: 2 Default: 2

        stability
        :stability: experimental
        """
        props = VersionProps(lambda_=lambda_, code_sha256=code_sha256, description=description, provisioned_concurrent_executions=provisioned_concurrent_executions, removal_policy=removal_policy, max_event_age=max_event_age, on_failure=on_failure, on_success=on_success, retry_attempts=retry_attempts)

        jsii.create(Version, self, [scope, id, props])

    @jsii.member(jsii_name="fromVersionArn")
    @builtins.classmethod
    def from_version_arn(cls, scope: _Construct_f50a3f53, id: str, version_arn: str) -> "IVersion":
        """Construct a Version object from a Version ARN.

        :param scope: The cdk scope creating this resource.
        :param id: The cdk id of this resource.
        :param version_arn: The version ARN to create this version from.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromVersionArn", [scope, id, version_arn])

    @jsii.member(jsii_name="fromVersionAttributes")
    @builtins.classmethod
    def from_version_attributes(cls, scope: _Construct_f50a3f53, id: str, *, lambda_: "IFunction", version: str) -> "IVersion":
        """
        :param scope: -
        :param id: -
        :param lambda_: The lambda function.
        :param version: The version.

        stability
        :stability: experimental
        """
        attrs = VersionAttributes(lambda_=lambda_, version=version)

        return jsii.sinvoke(cls, "fromVersionAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="addAlias")
    def add_alias(self, alias_name: str, *, additional_versions: typing.Optional[typing.List["VersionWeight"]]=None, description: typing.Optional[str]=None, provisioned_concurrent_executions: typing.Optional[jsii.Number]=None, max_event_age: typing.Optional[_Duration_5170c158]=None, on_failure: typing.Optional["IDestination"]=None, on_success: typing.Optional["IDestination"]=None, retry_attempts: typing.Optional[jsii.Number]=None) -> "Alias":
        """Defines an alias for this version.

        :param alias_name: The name of the alias (e.g. "live").
        :param additional_versions: Additional versions with individual weights this alias points to. Individual additional version weights specified here should add up to (less than) one. All remaining weight is routed to the default version. For example, the config is Example:: version: "1" additionalVersions: [{ version: "2", weight: 0.05 }] Then 5% of traffic will be routed to function version 2, while the remaining 95% of traffic will be routed to function version 1. Default: No additional versions
        :param description: Description for the alias. Default: No description
        :param provisioned_concurrent_executions: Specifies a provisioned concurrency configuration for a function's alias. Default: No provisioned concurrency
        :param max_event_age: The maximum age of a request that Lambda sends to a function for processing. Minimum: 60 seconds Maximum: 6 hours Default: Duration.hours(6)
        :param on_failure: The destination for failed invocations. Default: - no destination
        :param on_success: The destination for successful invocations. Default: - no destination
        :param retry_attempts: The maximum number of times to retry when the function returns an error. Minimum: 0 Maximum: 2 Default: 2

        stability
        :stability: experimental
        """
        options = AliasOptions(additional_versions=additional_versions, description=description, provisioned_concurrent_executions=provisioned_concurrent_executions, max_event_age=max_event_age, on_failure=on_failure, on_success=on_success, retry_attempts=retry_attempts)

        return jsii.invoke(self, "addAlias", [alias_name, options])

    @jsii.member(jsii_name="metric")
    def metric(self, metric_name: str, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[_Duration_5170c158]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[_Unit_e1b74f3c]=None) -> _Metric_53e89548:
        """Return the given named metric for this Function.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metric", [metric_name, props])

    @builtins.property
    @jsii.member(jsii_name="canCreatePermissions")
    def _can_create_permissions(self) -> bool:
        """Whether the addPermission() call adds any permissions.

        True for new Lambdas, false for imported Lambdas (they might live in different accounts).

        stability
        :stability: experimental
        """
        return jsii.get(self, "canCreatePermissions")

    @builtins.property
    @jsii.member(jsii_name="functionArn")
    def function_arn(self) -> str:
        """The ARN fo the function.

        stability
        :stability: experimental
        """
        return jsii.get(self, "functionArn")

    @builtins.property
    @jsii.member(jsii_name="functionName")
    def function_name(self) -> str:
        """The name of the function.

        stability
        :stability: experimental
        """
        return jsii.get(self, "functionName")

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> _IPrincipal_97126874:
        """The principal this Lambda Function is running as.

        stability
        :stability: experimental
        """
        return jsii.get(self, "grantPrincipal")

    @builtins.property
    @jsii.member(jsii_name="lambda")
    def lambda_(self) -> "IFunction":
        """The underlying AWS Lambda function.

        stability
        :stability: experimental
        """
        return jsii.get(self, "lambda")

    @builtins.property
    @jsii.member(jsii_name="qualifier")
    def _qualifier(self) -> str:
        """The qualifier of the version or alias of this function.

        A qualifier is the identifier that's appended to a version or alias ARN.

        stability
        :stability: experimental
        """
        return jsii.get(self, "qualifier")

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> str:
        """The most recently deployed version of this function.

        stability
        :stability: experimental
        """
        return jsii.get(self, "version")

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The IAM role associated with this function.

        Undefined if the function was imported without a role.

        stability
        :stability: experimental
        """
        return jsii.get(self, "role")


@jsii.implements(IAlias)
class Alias(QualifiedFunctionBase, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_lambda.Alias"):
    """A new alias to a particular version of a Lambda function.

    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, alias_name: str, version: "IVersion", additional_versions: typing.Optional[typing.List["VersionWeight"]]=None, description: typing.Optional[str]=None, provisioned_concurrent_executions: typing.Optional[jsii.Number]=None, max_event_age: typing.Optional[_Duration_5170c158]=None, on_failure: typing.Optional["IDestination"]=None, on_success: typing.Optional["IDestination"]=None, retry_attempts: typing.Optional[jsii.Number]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param alias_name: Name of this alias.
        :param version: Function version this alias refers to. Use lambda.addVersion() to obtain a new lambda version to refer to.
        :param additional_versions: Additional versions with individual weights this alias points to. Individual additional version weights specified here should add up to (less than) one. All remaining weight is routed to the default version. For example, the config is Example:: version: "1" additionalVersions: [{ version: "2", weight: 0.05 }] Then 5% of traffic will be routed to function version 2, while the remaining 95% of traffic will be routed to function version 1. Default: No additional versions
        :param description: Description for the alias. Default: No description
        :param provisioned_concurrent_executions: Specifies a provisioned concurrency configuration for a function's alias. Default: No provisioned concurrency
        :param max_event_age: The maximum age of a request that Lambda sends to a function for processing. Minimum: 60 seconds Maximum: 6 hours Default: Duration.hours(6)
        :param on_failure: The destination for failed invocations. Default: - no destination
        :param on_success: The destination for successful invocations. Default: - no destination
        :param retry_attempts: The maximum number of times to retry when the function returns an error. Minimum: 0 Maximum: 2 Default: 2

        stability
        :stability: experimental
        """
        props = AliasProps(alias_name=alias_name, version=version, additional_versions=additional_versions, description=description, provisioned_concurrent_executions=provisioned_concurrent_executions, max_event_age=max_event_age, on_failure=on_failure, on_success=on_success, retry_attempts=retry_attempts)

        jsii.create(Alias, self, [scope, id, props])

    @jsii.member(jsii_name="fromAliasAttributes")
    @builtins.classmethod
    def from_alias_attributes(cls, scope: _Construct_f50a3f53, id: str, *, alias_name: str, alias_version: "IVersion") -> "IAlias":
        """
        :param scope: -
        :param id: -
        :param alias_name: 
        :param alias_version: 

        stability
        :stability: experimental
        """
        attrs = AliasAttributes(alias_name=alias_name, alias_version=alias_version)

        return jsii.sinvoke(cls, "fromAliasAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="metric")
    def metric(self, metric_name: str, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[_Duration_5170c158]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[_Unit_e1b74f3c]=None) -> _Metric_53e89548:
        """Return the given named metric for this Function.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metric", [metric_name, props])

    @builtins.property
    @jsii.member(jsii_name="aliasName")
    def alias_name(self) -> str:
        """Name of this alias.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "aliasName")

    @builtins.property
    @jsii.member(jsii_name="canCreatePermissions")
    def _can_create_permissions(self) -> bool:
        """Whether the addPermission() call adds any permissions.

        True for new Lambdas, false for imported Lambdas (they might live in different accounts).

        stability
        :stability: experimental
        """
        return jsii.get(self, "canCreatePermissions")

    @builtins.property
    @jsii.member(jsii_name="functionArn")
    def function_arn(self) -> str:
        """ARN of this alias.

        Used to be able to use Alias in place of a regular Lambda. Lambda accepts
        ARNs everywhere it accepts function names.

        stability
        :stability: experimental
        """
        return jsii.get(self, "functionArn")

    @builtins.property
    @jsii.member(jsii_name="functionName")
    def function_name(self) -> str:
        """ARN of this alias.

        Used to be able to use Alias in place of a regular Lambda. Lambda accepts
        ARNs everywhere it accepts function names.

        stability
        :stability: experimental
        """
        return jsii.get(self, "functionName")

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> _IPrincipal_97126874:
        """The principal this Lambda Function is running as.

        stability
        :stability: experimental
        """
        return jsii.get(self, "grantPrincipal")

    @builtins.property
    @jsii.member(jsii_name="lambda")
    def lambda_(self) -> "IFunction":
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "lambda")

    @builtins.property
    @jsii.member(jsii_name="qualifier")
    def _qualifier(self) -> str:
        """The qualifier of the version or alias of this function.

        A qualifier is the identifier that's appended to a version or alias ARN.

        stability
        :stability: experimental
        """
        return jsii.get(self, "qualifier")

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> "IVersion":
        """The underlying Lambda function version.

        stability
        :stability: experimental
        """
        return jsii.get(self, "version")

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The IAM role associated with this function.

        Undefined if the function was imported without a role.

        stability
        :stability: experimental
        """
        return jsii.get(self, "role")


class Function(FunctionBase, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_lambda.Function"):
    """Deploys a file from from inside the construct library as a function.

    The supplied file is subject to the 4096 bytes limit of being embedded in a
    CloudFormation template.

    The construct includes an associated role with the lambda.

    This construct does not yet reproduce all features from the underlying resource
    library.

    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, code: "Code", handler: str, runtime: "Runtime", allow_all_outbound: typing.Optional[bool]=None, current_version_options: typing.Optional["VersionOptions"]=None, dead_letter_queue: typing.Optional[_IQueue_b743f559]=None, dead_letter_queue_enabled: typing.Optional[bool]=None, description: typing.Optional[str]=None, environment: typing.Optional[typing.Mapping[str, str]]=None, events: typing.Optional[typing.List["IEventSource"]]=None, function_name: typing.Optional[str]=None, initial_policy: typing.Optional[typing.List[_PolicyStatement_f75dc775]]=None, layers: typing.Optional[typing.List["ILayerVersion"]]=None, log_retention: typing.Optional[_RetentionDays_bdc7ad1f]=None, log_retention_retry_options: typing.Optional["LogRetentionRetryOptions"]=None, log_retention_role: typing.Optional[_IRole_e69bbae4]=None, memory_size: typing.Optional[jsii.Number]=None, reserved_concurrent_executions: typing.Optional[jsii.Number]=None, role: typing.Optional[_IRole_e69bbae4]=None, security_group: typing.Optional[_ISecurityGroup_d72ab8e8]=None, security_groups: typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]]=None, timeout: typing.Optional[_Duration_5170c158]=None, tracing: typing.Optional["Tracing"]=None, vpc: typing.Optional[_IVpc_3795853f]=None, vpc_subnets: typing.Optional[_SubnetSelection_36a13cd6]=None, max_event_age: typing.Optional[_Duration_5170c158]=None, on_failure: typing.Optional["IDestination"]=None, on_success: typing.Optional["IDestination"]=None, retry_attempts: typing.Optional[jsii.Number]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param code: The source code of your Lambda function. You can point to a file in an Amazon Simple Storage Service (Amazon S3) bucket or specify your source code as inline text.
        :param handler: The name of the method within your code that Lambda calls to execute your function. The format includes the file name. It can also include namespaces and other qualifiers, depending on the runtime. For more information, see https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-features.html#gettingstarted-features-programmingmodel. NOTE: If you specify your source code as inline text by specifying the ZipFile property within the Code property, specify index.function_name as the handler.
        :param runtime: The runtime environment for the Lambda function that you are uploading. For valid values, see the Runtime property in the AWS Lambda Developer Guide.
        :param allow_all_outbound: Whether to allow the Lambda to send all network traffic. If set to false, you must individually add traffic rules to allow the Lambda to connect to network targets. Default: true
        :param current_version_options: Options for the ``lambda.Version`` resource automatically created by the ``fn.currentVersion`` method. Default: - default options as described in ``VersionOptions``
        :param dead_letter_queue: The SQS queue to use if DLQ is enabled. Default: - SQS queue with 14 day retention period if ``deadLetterQueueEnabled`` is ``true``
        :param dead_letter_queue_enabled: Enabled DLQ. If ``deadLetterQueue`` is undefined, an SQS queue with default options will be defined for your Function. Default: - false unless ``deadLetterQueue`` is set, which implies DLQ is enabled.
        :param description: A description of the function. Default: - No description.
        :param environment: Key-value pairs that Lambda caches and makes available for your Lambda functions. Use environment variables to apply configuration changes, such as test and production environment configurations, without changing your Lambda function source code. Default: - No environment variables.
        :param events: Event sources for this function. You can also add event sources using ``addEventSource``. Default: - No event sources.
        :param function_name: A name for the function. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the function's name. For more information, see Name Type.
        :param initial_policy: Initial policy statements to add to the created Lambda Role. You can call ``addToRolePolicy`` to the created lambda to add statements post creation. Default: - No policy statements are added to the created Lambda role.
        :param layers: A list of layers to add to the function's execution environment. You can configure your Lambda function to pull in additional code during initialization in the form of layers. Layers are packages of libraries or other dependencies that can be used by mulitple functions. Default: - No layers.
        :param log_retention: The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.INFINITE
        :param log_retention_retry_options: When log retention is specified, a custom resource attempts to create the CloudWatch log group. These options control the retry policy when interacting with CloudWatch APIs. Default: - Default AWS SDK retry options.
        :param log_retention_role: The IAM role for the Lambda function associated with the custom resource that sets the retention policy. Default: - A new role is created.
        :param memory_size: The amount of memory, in MB, that is allocated to your Lambda function. Lambda uses this value to proportionally allocate the amount of CPU power. For more information, see Resource Model in the AWS Lambda Developer Guide. Default: 128
        :param reserved_concurrent_executions: The maximum of concurrent executions you want to reserve for the function. Default: - No specific limit - account limit.
        :param role: Lambda execution role. This is the role that will be assumed by the function upon execution. It controls the permissions that the function will have. The Role must be assumable by the 'lambda.amazonaws.com' service principal. The default Role automatically has permissions granted for Lambda execution. If you provide a Role, you must add the relevant AWS managed policies yourself. The relevant managed policies are "service-role/AWSLambdaBasicExecutionRole" and "service-role/AWSLambdaVPCAccessExecutionRole". Default: - A unique role will be generated for this lambda function. Both supplied and generated roles can always be changed by calling ``addToRolePolicy``.
        :param security_group: What security group to associate with the Lambda's network interfaces. This property is being deprecated, consider using securityGroups instead. Only used if 'vpc' is supplied. Use securityGroups property instead. Function constructor will throw an error if both are specified. Default: - If the function is placed within a VPC and a security group is not specified, either by this or securityGroups prop, a dedicated security group will be created for this function.
        :param security_groups: The list of security groups to associate with the Lambda's network interfaces. Only used if 'vpc' is supplied. Default: - If the function is placed within a VPC and a security group is not specified, either by this or securityGroup prop, a dedicated security group will be created for this function.
        :param timeout: The function execution time (in seconds) after which Lambda terminates the function. Because the execution time affects cost, set this value based on the function's expected execution time. Default: Duration.seconds(3)
        :param tracing: Enable AWS X-Ray Tracing for Lambda Function. Default: Tracing.Disabled
        :param vpc: VPC network to place Lambda network interfaces. Specify this if the Lambda function needs to access resources in a VPC. Default: - Function is not placed within a VPC.
        :param vpc_subnets: Where to place the network interfaces within the VPC. Only used if 'vpc' is supplied. Note: internet access for Lambdas requires a NAT gateway, so picking Public subnets is not allowed. Default: - the Vpc default strategy if not specified
        :param max_event_age: The maximum age of a request that Lambda sends to a function for processing. Minimum: 60 seconds Maximum: 6 hours Default: Duration.hours(6)
        :param on_failure: The destination for failed invocations. Default: - no destination
        :param on_success: The destination for successful invocations. Default: - no destination
        :param retry_attempts: The maximum number of times to retry when the function returns an error. Minimum: 0 Maximum: 2 Default: 2

        stability
        :stability: experimental
        """
        props = FunctionProps(code=code, handler=handler, runtime=runtime, allow_all_outbound=allow_all_outbound, current_version_options=current_version_options, dead_letter_queue=dead_letter_queue, dead_letter_queue_enabled=dead_letter_queue_enabled, description=description, environment=environment, events=events, function_name=function_name, initial_policy=initial_policy, layers=layers, log_retention=log_retention, log_retention_retry_options=log_retention_retry_options, log_retention_role=log_retention_role, memory_size=memory_size, reserved_concurrent_executions=reserved_concurrent_executions, role=role, security_group=security_group, security_groups=security_groups, timeout=timeout, tracing=tracing, vpc=vpc, vpc_subnets=vpc_subnets, max_event_age=max_event_age, on_failure=on_failure, on_success=on_success, retry_attempts=retry_attempts)

        jsii.create(Function, self, [scope, id, props])

    @jsii.member(jsii_name="fromFunctionArn")
    @builtins.classmethod
    def from_function_arn(cls, scope: _Construct_f50a3f53, id: str, function_arn: str) -> "IFunction":
        """
        :param scope: -
        :param id: -
        :param function_arn: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromFunctionArn", [scope, id, function_arn])

    @jsii.member(jsii_name="fromFunctionAttributes")
    @builtins.classmethod
    def from_function_attributes(cls, scope: _Construct_f50a3f53, id: str, *, function_arn: str, role: typing.Optional[_IRole_e69bbae4]=None, security_group: typing.Optional[_ISecurityGroup_d72ab8e8]=None, security_group_id: typing.Optional[str]=None) -> "IFunction":
        """Creates a Lambda function object which represents a function not defined within this stack.

        :param scope: The parent construct.
        :param id: The name of the lambda construct.
        :param function_arn: The ARN of the Lambda function. Format: arn::lambda:::function:
        :param role: The IAM execution role associated with this function. If the role is not specified, any role-related operations will no-op.
        :param security_group: The security group of this Lambda, if in a VPC. This needs to be given in order to support allowing connections to this Lambda.
        :param security_group_id: Id of the security group of this Lambda, if in a VPC. This needs to be given in order to support allowing connections to this Lambda.

        stability
        :stability: experimental
        """
        attrs = FunctionAttributes(function_arn=function_arn, role=role, security_group=security_group, security_group_id=security_group_id)

        return jsii.sinvoke(cls, "fromFunctionAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="metricAll")
    @builtins.classmethod
    def metric_all(cls, metric_name: str, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[_Duration_5170c158]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[_Unit_e1b74f3c]=None) -> _Metric_53e89548:
        """Return the given named metric for this Lambda.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.sinvoke(cls, "metricAll", [metric_name, props])

    @jsii.member(jsii_name="metricAllConcurrentExecutions")
    @builtins.classmethod
    def metric_all_concurrent_executions(cls, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[_Duration_5170c158]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[_Unit_e1b74f3c]=None) -> _Metric_53e89548:
        """Metric for the number of concurrent executions across all Lambdas.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: max over 5 minutes

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.sinvoke(cls, "metricAllConcurrentExecutions", [props])

    @jsii.member(jsii_name="metricAllDuration")
    @builtins.classmethod
    def metric_all_duration(cls, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[_Duration_5170c158]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[_Unit_e1b74f3c]=None) -> _Metric_53e89548:
        """Metric for the Duration executing all Lambdas.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: average over 5 minutes

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.sinvoke(cls, "metricAllDuration", [props])

    @jsii.member(jsii_name="metricAllErrors")
    @builtins.classmethod
    def metric_all_errors(cls, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[_Duration_5170c158]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[_Unit_e1b74f3c]=None) -> _Metric_53e89548:
        """Metric for the number of Errors executing all Lambdas.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over 5 minutes

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.sinvoke(cls, "metricAllErrors", [props])

    @jsii.member(jsii_name="metricAllInvocations")
    @builtins.classmethod
    def metric_all_invocations(cls, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[_Duration_5170c158]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[_Unit_e1b74f3c]=None) -> _Metric_53e89548:
        """Metric for the number of invocations of all Lambdas.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over 5 minutes

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.sinvoke(cls, "metricAllInvocations", [props])

    @jsii.member(jsii_name="metricAllThrottles")
    @builtins.classmethod
    def metric_all_throttles(cls, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[_Duration_5170c158]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[_Unit_e1b74f3c]=None) -> _Metric_53e89548:
        """Metric for the number of throttled invocations of all Lambdas.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: sum over 5 minutes

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.sinvoke(cls, "metricAllThrottles", [props])

    @jsii.member(jsii_name="metricAllUnreservedConcurrentExecutions")
    @builtins.classmethod
    def metric_all_unreserved_concurrent_executions(cls, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[_Duration_5170c158]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[_Unit_e1b74f3c]=None) -> _Metric_53e89548:
        """Metric for the number of unreserved concurrent executions across all Lambdas.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: max over 5 minutes

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.sinvoke(cls, "metricAllUnreservedConcurrentExecutions", [props])

    @jsii.member(jsii_name="addEnvironment")
    def add_environment(self, key: str, value: str) -> "Function":
        """Adds an environment variable to this Lambda function.

        If this is a ref to a Lambda function, this operation results in a no-op.

        :param key: The environment variable key.
        :param value: The environment variable's value.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addEnvironment", [key, value])

    @jsii.member(jsii_name="addLayers")
    def add_layers(self, *layers: "ILayerVersion") -> None:
        """Adds one or more Lambda Layers to this Lambda function.

        :param layers: the layers to be added.

        stability
        :stability: experimental
        throws:
        :throws:: if there are already 5 layers on this function, or the layer is incompatible with this function's runtime.
        """
        return jsii.invoke(self, "addLayers", [*layers])

    @jsii.member(jsii_name="addVersion")
    def add_version(self, name: str, code_sha256: typing.Optional[str]=None, description: typing.Optional[str]=None, provisioned_executions: typing.Optional[jsii.Number]=None, *, max_event_age: typing.Optional[_Duration_5170c158]=None, on_failure: typing.Optional["IDestination"]=None, on_success: typing.Optional["IDestination"]=None, retry_attempts: typing.Optional[jsii.Number]=None) -> "Version":
        """Add a new version for this Lambda.

        If you want to deploy through CloudFormation and use aliases, you need to
        add a new version (with a new name) to your Lambda every time you want to
        deploy an update. An alias can then refer to the newly created Version.

        All versions should have distinct names, and you should not delete versions
        as long as your Alias needs to refer to them.

        :param name: A unique name for this version.
        :param code_sha256: The SHA-256 hash of the most recently deployed Lambda source code, or omit to skip validation.
        :param description: A description for this version.
        :param provisioned_executions: A provisioned concurrency configuration for a function's version.
        :param max_event_age: The maximum age of a request that Lambda sends to a function for processing. Minimum: 60 seconds Maximum: 6 hours Default: Duration.hours(6)
        :param on_failure: The destination for failed invocations. Default: - no destination
        :param on_success: The destination for successful invocations. Default: - no destination
        :param retry_attempts: The maximum number of times to retry when the function returns an error. Minimum: 0 Maximum: 2 Default: 2

        return
        :return: A new Version object.

        deprecated
        :deprecated:

        This method will create an AWS::Lambda::Version resource which
        snapshots the AWS Lambda function *at the time of its creation* and it
        won't get updated when the function changes. Instead, use
        ``this.currentVersion`` to obtain a reference to a version resource that gets
        automatically recreated when the function configuration (or code) changes.

        stability
        :stability: deprecated
        """
        async_invoke_config = EventInvokeConfigOptions(max_event_age=max_event_age, on_failure=on_failure, on_success=on_success, retry_attempts=retry_attempts)

        return jsii.invoke(self, "addVersion", [name, code_sha256, description, provisioned_executions, async_invoke_config])

    @jsii.member(jsii_name="prepare")
    def _prepare(self) -> None:
        """Perform final modifications before synthesis.

        This method can be implemented by derived constructs in order to perform
        final changes before synthesis. prepare() will be called after child
        constructs have been prepared.

        This is an advanced framework feature. Only use this if you
        understand the implications.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "prepare", [])

    @builtins.property
    @jsii.member(jsii_name="canCreatePermissions")
    def _can_create_permissions(self) -> bool:
        """Whether the addPermission() call adds any permissions.

        True for new Lambdas, false for imported Lambdas (they might live in different accounts).

        stability
        :stability: experimental
        """
        return jsii.get(self, "canCreatePermissions")

    @builtins.property
    @jsii.member(jsii_name="currentVersion")
    def current_version(self) -> "Version":
        """Returns a ``lambda.Version`` which represents the current version of this Lambda function. A new version will be created every time the function's configuration changes.

        You can specify options for this version using the ``currentVersionOptions``
        prop when initializing the ``lambda.Function``.

        stability
        :stability: experimental
        """
        return jsii.get(self, "currentVersion")

    @builtins.property
    @jsii.member(jsii_name="functionArn")
    def function_arn(self) -> str:
        """ARN of this function.

        stability
        :stability: experimental
        """
        return jsii.get(self, "functionArn")

    @builtins.property
    @jsii.member(jsii_name="functionName")
    def function_name(self) -> str:
        """Name of this function.

        stability
        :stability: experimental
        """
        return jsii.get(self, "functionName")

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> _IPrincipal_97126874:
        """The principal this Lambda Function is running as.

        stability
        :stability: experimental
        """
        return jsii.get(self, "grantPrincipal")

    @builtins.property
    @jsii.member(jsii_name="logGroup")
    def log_group(self) -> _ILogGroup_6b54c8e1:
        """The LogGroup where the Lambda function's logs are made available.

        If either ``logRetention`` is set or this property is called, a CloudFormation custom resource is added to the stack that
        pre-creates the log group as part of the stack deployment, if it already doesn't exist, and sets the correct log retention
        period (never expire, by default).

        Further, if the log group already exists and the ``logRetention`` is not set, the custom resource will reset the log retention
        to never expire even if it was configured with a different value.

        stability
        :stability: experimental
        """
        return jsii.get(self, "logGroup")

    @builtins.property
    @jsii.member(jsii_name="permissionsNode")
    def permissions_node(self) -> _ConstructNode_6884f5de:
        """The construct node where permissions are attached.

        stability
        :stability: experimental
        """
        return jsii.get(self, "permissionsNode")

    @builtins.property
    @jsii.member(jsii_name="runtime")
    def runtime(self) -> "Runtime":
        """The runtime configured for this lambda.

        stability
        :stability: experimental
        """
        return jsii.get(self, "runtime")

    @builtins.property
    @jsii.member(jsii_name="deadLetterQueue")
    def dead_letter_queue(self) -> typing.Optional[_IQueue_b743f559]:
        """The DLQ associated with this Lambda Function (this is an optional attribute).

        stability
        :stability: experimental
        """
        return jsii.get(self, "deadLetterQueue")

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """Execution role associated with this function.

        stability
        :stability: experimental
        """
        return jsii.get(self, "role")


__all__ = [
    "Alias",
    "AliasAttributes",
    "AliasOptions",
    "AliasProps",
    "AssetCode",
    "CfnAlias",
    "CfnAliasProps",
    "CfnEventInvokeConfig",
    "CfnEventInvokeConfigProps",
    "CfnEventSourceMapping",
    "CfnEventSourceMappingProps",
    "CfnFunction",
    "CfnFunctionProps",
    "CfnLayerVersion",
    "CfnLayerVersionPermission",
    "CfnLayerVersionPermissionProps",
    "CfnLayerVersionProps",
    "CfnParametersCode",
    "CfnParametersCodeProps",
    "CfnPermission",
    "CfnPermissionProps",
    "CfnVersion",
    "CfnVersionProps",
    "Code",
    "CodeConfig",
    "DestinationConfig",
    "DestinationOptions",
    "DestinationType",
    "DlqDestinationConfig",
    "EventInvokeConfig",
    "EventInvokeConfigOptions",
    "EventInvokeConfigProps",
    "EventSourceMapping",
    "EventSourceMappingOptions",
    "EventSourceMappingProps",
    "Function",
    "FunctionAttributes",
    "FunctionBase",
    "FunctionOptions",
    "FunctionProps",
    "IAlias",
    "IDestination",
    "IEventSource",
    "IEventSourceDlq",
    "IEventSourceMapping",
    "IFunction",
    "ILayerVersion",
    "IVersion",
    "InlineCode",
    "LambdaRuntimeProps",
    "LayerVersion",
    "LayerVersionAttributes",
    "LayerVersionPermission",
    "LayerVersionProps",
    "LogRetention",
    "LogRetentionProps",
    "LogRetentionRetryOptions",
    "Permission",
    "QualifiedFunctionBase",
    "ResourceBindOptions",
    "Runtime",
    "RuntimeFamily",
    "S3Code",
    "SingletonFunction",
    "SingletonFunctionProps",
    "StartingPosition",
    "Tracing",
    "Version",
    "VersionAttributes",
    "VersionOptions",
    "VersionProps",
    "VersionWeight",
]

publication.publish()
