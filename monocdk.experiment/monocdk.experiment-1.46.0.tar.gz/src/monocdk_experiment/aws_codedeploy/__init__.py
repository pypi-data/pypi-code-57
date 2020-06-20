import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *

from .. import (CfnResource as _CfnResource_7760e8e4, Construct as _Construct_f50a3f53, FromCloudFormationOptions as _FromCloudFormationOptions_5f49f6f1, TreeInspector as _TreeInspector_154f5999, IInspectable as _IInspectable_051e6ed8, IResolvable as _IResolvable_9ceae33e, Resource as _Resource_884d0774, IResource as _IResource_72f7ee7e)
from ..aws_autoscaling import (AutoScalingGroup as _AutoScalingGroup_003d0b84)
from ..aws_cloudwatch import (IAlarm as _IAlarm_478ec33c)
from ..aws_elasticloadbalancing import (LoadBalancer as _LoadBalancer_6d00b4b8)
from ..aws_elasticloadbalancingv2 import (ApplicationTargetGroup as _ApplicationTargetGroup_7d0a8d54, NetworkTargetGroup as _NetworkTargetGroup_4f773ed3)
from ..aws_iam import (IRole as _IRole_e69bbae4, Grant as _Grant_96af6d2d, IGrantable as _IGrantable_0fcfc53a)
from ..aws_lambda import (IFunction as _IFunction_1c1de0bc, Alias as _Alias_67f7db75)


@jsii.data_type(jsii_type="monocdk-experiment.aws_codedeploy.AutoRollbackConfig", jsii_struct_bases=[], name_mapping={'deployment_in_alarm': 'deploymentInAlarm', 'failed_deployment': 'failedDeployment', 'stopped_deployment': 'stoppedDeployment'})
class AutoRollbackConfig():
    def __init__(self, *, deployment_in_alarm: typing.Optional[bool]=None, failed_deployment: typing.Optional[bool]=None, stopped_deployment: typing.Optional[bool]=None) -> None:
        """The configuration for automatically rolling back deployments in a given Deployment Group.

        :param deployment_in_alarm: Whether to automatically roll back a deployment during which one of the configured CloudWatch alarms for this Deployment Group went off. Default: true if you've provided any Alarms with the ``alarms`` property, false otherwise
        :param failed_deployment: Whether to automatically roll back a deployment that fails. Default: true
        :param stopped_deployment: Whether to automatically roll back a deployment that was manually stopped. Default: false

        stability
        :stability: experimental
        """
        self._values = {
        }
        if deployment_in_alarm is not None: self._values["deployment_in_alarm"] = deployment_in_alarm
        if failed_deployment is not None: self._values["failed_deployment"] = failed_deployment
        if stopped_deployment is not None: self._values["stopped_deployment"] = stopped_deployment

    @builtins.property
    def deployment_in_alarm(self) -> typing.Optional[bool]:
        """Whether to automatically roll back a deployment during which one of the configured CloudWatch alarms for this Deployment Group went off.

        default
        :default: true if you've provided any Alarms with the ``alarms`` property, false otherwise

        stability
        :stability: experimental
        """
        return self._values.get('deployment_in_alarm')

    @builtins.property
    def failed_deployment(self) -> typing.Optional[bool]:
        """Whether to automatically roll back a deployment that fails.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('failed_deployment')

    @builtins.property
    def stopped_deployment(self) -> typing.Optional[bool]:
        """Whether to automatically roll back a deployment that was manually stopped.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('stopped_deployment')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AutoRollbackConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnApplication(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_codedeploy.CfnApplication"):
    """A CloudFormation ``AWS::CodeDeploy::Application``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-application.html
    cloudformationResource:
    :cloudformationResource:: AWS::CodeDeploy::Application
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, application_name: typing.Optional[str]=None, compute_platform: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::CodeDeploy::Application``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_name: ``AWS::CodeDeploy::Application.ApplicationName``.
        :param compute_platform: ``AWS::CodeDeploy::Application.ComputePlatform``.
        """
        props = CfnApplicationProps(application_name=application_name, compute_platform=compute_platform)

        jsii.create(CfnApplication, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnApplication":
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
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> typing.Optional[str]:
        """``AWS::CodeDeploy::Application.ApplicationName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-application.html#cfn-codedeploy-application-applicationname
        """
        return jsii.get(self, "applicationName")

    @application_name.setter
    def application_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "applicationName", value)

    @builtins.property
    @jsii.member(jsii_name="computePlatform")
    def compute_platform(self) -> typing.Optional[str]:
        """``AWS::CodeDeploy::Application.ComputePlatform``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-application.html#cfn-codedeploy-application-computeplatform
        """
        return jsii.get(self, "computePlatform")

    @compute_platform.setter
    def compute_platform(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "computePlatform", value)


@jsii.data_type(jsii_type="monocdk-experiment.aws_codedeploy.CfnApplicationProps", jsii_struct_bases=[], name_mapping={'application_name': 'applicationName', 'compute_platform': 'computePlatform'})
class CfnApplicationProps():
    def __init__(self, *, application_name: typing.Optional[str]=None, compute_platform: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::CodeDeploy::Application``.

        :param application_name: ``AWS::CodeDeploy::Application.ApplicationName``.
        :param compute_platform: ``AWS::CodeDeploy::Application.ComputePlatform``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-application.html
        """
        self._values = {
        }
        if application_name is not None: self._values["application_name"] = application_name
        if compute_platform is not None: self._values["compute_platform"] = compute_platform

    @builtins.property
    def application_name(self) -> typing.Optional[str]:
        """``AWS::CodeDeploy::Application.ApplicationName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-application.html#cfn-codedeploy-application-applicationname
        """
        return self._values.get('application_name')

    @builtins.property
    def compute_platform(self) -> typing.Optional[str]:
        """``AWS::CodeDeploy::Application.ComputePlatform``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-application.html#cfn-codedeploy-application-computeplatform
        """
        return self._values.get('compute_platform')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnApplicationProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnDeploymentConfig(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_codedeploy.CfnDeploymentConfig"):
    """A CloudFormation ``AWS::CodeDeploy::DeploymentConfig``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentconfig.html
    cloudformationResource:
    :cloudformationResource:: AWS::CodeDeploy::DeploymentConfig
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, deployment_config_name: typing.Optional[str]=None, minimum_healthy_hosts: typing.Optional[typing.Union["MinimumHealthyHostsProperty", _IResolvable_9ceae33e]]=None) -> None:
        """Create a new ``AWS::CodeDeploy::DeploymentConfig``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param deployment_config_name: ``AWS::CodeDeploy::DeploymentConfig.DeploymentConfigName``.
        :param minimum_healthy_hosts: ``AWS::CodeDeploy::DeploymentConfig.MinimumHealthyHosts``.
        """
        props = CfnDeploymentConfigProps(deployment_config_name=deployment_config_name, minimum_healthy_hosts=minimum_healthy_hosts)

        jsii.create(CfnDeploymentConfig, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnDeploymentConfig":
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
    @jsii.member(jsii_name="deploymentConfigName")
    def deployment_config_name(self) -> typing.Optional[str]:
        """``AWS::CodeDeploy::DeploymentConfig.DeploymentConfigName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentconfig.html#cfn-codedeploy-deploymentconfig-deploymentconfigname
        """
        return jsii.get(self, "deploymentConfigName")

    @deployment_config_name.setter
    def deployment_config_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "deploymentConfigName", value)

    @builtins.property
    @jsii.member(jsii_name="minimumHealthyHosts")
    def minimum_healthy_hosts(self) -> typing.Optional[typing.Union["MinimumHealthyHostsProperty", _IResolvable_9ceae33e]]:
        """``AWS::CodeDeploy::DeploymentConfig.MinimumHealthyHosts``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentconfig.html#cfn-codedeploy-deploymentconfig-minimumhealthyhosts
        """
        return jsii.get(self, "minimumHealthyHosts")

    @minimum_healthy_hosts.setter
    def minimum_healthy_hosts(self, value: typing.Optional[typing.Union["MinimumHealthyHostsProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "minimumHealthyHosts", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_codedeploy.CfnDeploymentConfig.MinimumHealthyHostsProperty", jsii_struct_bases=[], name_mapping={'type': 'type', 'value': 'value'})
    class MinimumHealthyHostsProperty():
        def __init__(self, *, type: str, value: jsii.Number) -> None:
            """
            :param type: ``CfnDeploymentConfig.MinimumHealthyHostsProperty.Type``.
            :param value: ``CfnDeploymentConfig.MinimumHealthyHostsProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentconfig-minimumhealthyhosts.html
            """
            self._values = {
                'type': type,
                'value': value,
            }

        @builtins.property
        def type(self) -> str:
            """``CfnDeploymentConfig.MinimumHealthyHostsProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentconfig-minimumhealthyhosts.html#cfn-codedeploy-deploymentconfig-minimumhealthyhosts-type
            """
            return self._values.get('type')

        @builtins.property
        def value(self) -> jsii.Number:
            """``CfnDeploymentConfig.MinimumHealthyHostsProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentconfig-minimumhealthyhosts.html#cfn-codedeploy-deploymentconfig-minimumhealthyhosts-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'MinimumHealthyHostsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_codedeploy.CfnDeploymentConfigProps", jsii_struct_bases=[], name_mapping={'deployment_config_name': 'deploymentConfigName', 'minimum_healthy_hosts': 'minimumHealthyHosts'})
class CfnDeploymentConfigProps():
    def __init__(self, *, deployment_config_name: typing.Optional[str]=None, minimum_healthy_hosts: typing.Optional[typing.Union["CfnDeploymentConfig.MinimumHealthyHostsProperty", _IResolvable_9ceae33e]]=None) -> None:
        """Properties for defining a ``AWS::CodeDeploy::DeploymentConfig``.

        :param deployment_config_name: ``AWS::CodeDeploy::DeploymentConfig.DeploymentConfigName``.
        :param minimum_healthy_hosts: ``AWS::CodeDeploy::DeploymentConfig.MinimumHealthyHosts``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentconfig.html
        """
        self._values = {
        }
        if deployment_config_name is not None: self._values["deployment_config_name"] = deployment_config_name
        if minimum_healthy_hosts is not None: self._values["minimum_healthy_hosts"] = minimum_healthy_hosts

    @builtins.property
    def deployment_config_name(self) -> typing.Optional[str]:
        """``AWS::CodeDeploy::DeploymentConfig.DeploymentConfigName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentconfig.html#cfn-codedeploy-deploymentconfig-deploymentconfigname
        """
        return self._values.get('deployment_config_name')

    @builtins.property
    def minimum_healthy_hosts(self) -> typing.Optional[typing.Union["CfnDeploymentConfig.MinimumHealthyHostsProperty", _IResolvable_9ceae33e]]:
        """``AWS::CodeDeploy::DeploymentConfig.MinimumHealthyHosts``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentconfig.html#cfn-codedeploy-deploymentconfig-minimumhealthyhosts
        """
        return self._values.get('minimum_healthy_hosts')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnDeploymentConfigProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnDeploymentGroup(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_codedeploy.CfnDeploymentGroup"):
    """A CloudFormation ``AWS::CodeDeploy::DeploymentGroup``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html
    cloudformationResource:
    :cloudformationResource:: AWS::CodeDeploy::DeploymentGroup
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, application_name: str, service_role_arn: str, alarm_configuration: typing.Optional[typing.Union["AlarmConfigurationProperty", _IResolvable_9ceae33e]]=None, auto_rollback_configuration: typing.Optional[typing.Union["AutoRollbackConfigurationProperty", _IResolvable_9ceae33e]]=None, auto_scaling_groups: typing.Optional[typing.List[str]]=None, deployment: typing.Optional[typing.Union["DeploymentProperty", _IResolvable_9ceae33e]]=None, deployment_config_name: typing.Optional[str]=None, deployment_group_name: typing.Optional[str]=None, deployment_style: typing.Optional[typing.Union["DeploymentStyleProperty", _IResolvable_9ceae33e]]=None, ec2_tag_filters: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["EC2TagFilterProperty", _IResolvable_9ceae33e]]]]=None, ec2_tag_set: typing.Optional[typing.Union["EC2TagSetProperty", _IResolvable_9ceae33e]]=None, load_balancer_info: typing.Optional[typing.Union["LoadBalancerInfoProperty", _IResolvable_9ceae33e]]=None, on_premises_instance_tag_filters: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["TagFilterProperty", _IResolvable_9ceae33e]]]]=None, on_premises_tag_set: typing.Optional[typing.Union["OnPremisesTagSetProperty", _IResolvable_9ceae33e]]=None, trigger_configurations: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["TriggerConfigProperty", _IResolvable_9ceae33e]]]]=None) -> None:
        """Create a new ``AWS::CodeDeploy::DeploymentGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_name: ``AWS::CodeDeploy::DeploymentGroup.ApplicationName``.
        :param service_role_arn: ``AWS::CodeDeploy::DeploymentGroup.ServiceRoleArn``.
        :param alarm_configuration: ``AWS::CodeDeploy::DeploymentGroup.AlarmConfiguration``.
        :param auto_rollback_configuration: ``AWS::CodeDeploy::DeploymentGroup.AutoRollbackConfiguration``.
        :param auto_scaling_groups: ``AWS::CodeDeploy::DeploymentGroup.AutoScalingGroups``.
        :param deployment: ``AWS::CodeDeploy::DeploymentGroup.Deployment``.
        :param deployment_config_name: ``AWS::CodeDeploy::DeploymentGroup.DeploymentConfigName``.
        :param deployment_group_name: ``AWS::CodeDeploy::DeploymentGroup.DeploymentGroupName``.
        :param deployment_style: ``AWS::CodeDeploy::DeploymentGroup.DeploymentStyle``.
        :param ec2_tag_filters: ``AWS::CodeDeploy::DeploymentGroup.Ec2TagFilters``.
        :param ec2_tag_set: ``AWS::CodeDeploy::DeploymentGroup.Ec2TagSet``.
        :param load_balancer_info: ``AWS::CodeDeploy::DeploymentGroup.LoadBalancerInfo``.
        :param on_premises_instance_tag_filters: ``AWS::CodeDeploy::DeploymentGroup.OnPremisesInstanceTagFilters``.
        :param on_premises_tag_set: ``AWS::CodeDeploy::DeploymentGroup.OnPremisesTagSet``.
        :param trigger_configurations: ``AWS::CodeDeploy::DeploymentGroup.TriggerConfigurations``.
        """
        props = CfnDeploymentGroupProps(application_name=application_name, service_role_arn=service_role_arn, alarm_configuration=alarm_configuration, auto_rollback_configuration=auto_rollback_configuration, auto_scaling_groups=auto_scaling_groups, deployment=deployment, deployment_config_name=deployment_config_name, deployment_group_name=deployment_group_name, deployment_style=deployment_style, ec2_tag_filters=ec2_tag_filters, ec2_tag_set=ec2_tag_set, load_balancer_info=load_balancer_info, on_premises_instance_tag_filters=on_premises_instance_tag_filters, on_premises_tag_set=on_premises_tag_set, trigger_configurations=trigger_configurations)

        jsii.create(CfnDeploymentGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnDeploymentGroup":
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
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> str:
        """``AWS::CodeDeploy::DeploymentGroup.ApplicationName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-applicationname
        """
        return jsii.get(self, "applicationName")

    @application_name.setter
    def application_name(self, value: str) -> None:
        jsii.set(self, "applicationName", value)

    @builtins.property
    @jsii.member(jsii_name="serviceRoleArn")
    def service_role_arn(self) -> str:
        """``AWS::CodeDeploy::DeploymentGroup.ServiceRoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-servicerolearn
        """
        return jsii.get(self, "serviceRoleArn")

    @service_role_arn.setter
    def service_role_arn(self, value: str) -> None:
        jsii.set(self, "serviceRoleArn", value)

    @builtins.property
    @jsii.member(jsii_name="alarmConfiguration")
    def alarm_configuration(self) -> typing.Optional[typing.Union["AlarmConfigurationProperty", _IResolvable_9ceae33e]]:
        """``AWS::CodeDeploy::DeploymentGroup.AlarmConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-alarmconfiguration
        """
        return jsii.get(self, "alarmConfiguration")

    @alarm_configuration.setter
    def alarm_configuration(self, value: typing.Optional[typing.Union["AlarmConfigurationProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "alarmConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="autoRollbackConfiguration")
    def auto_rollback_configuration(self) -> typing.Optional[typing.Union["AutoRollbackConfigurationProperty", _IResolvable_9ceae33e]]:
        """``AWS::CodeDeploy::DeploymentGroup.AutoRollbackConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-autorollbackconfiguration
        """
        return jsii.get(self, "autoRollbackConfiguration")

    @auto_rollback_configuration.setter
    def auto_rollback_configuration(self, value: typing.Optional[typing.Union["AutoRollbackConfigurationProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "autoRollbackConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="autoScalingGroups")
    def auto_scaling_groups(self) -> typing.Optional[typing.List[str]]:
        """``AWS::CodeDeploy::DeploymentGroup.AutoScalingGroups``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-autoscalinggroups
        """
        return jsii.get(self, "autoScalingGroups")

    @auto_scaling_groups.setter
    def auto_scaling_groups(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "autoScalingGroups", value)

    @builtins.property
    @jsii.member(jsii_name="deployment")
    def deployment(self) -> typing.Optional[typing.Union["DeploymentProperty", _IResolvable_9ceae33e]]:
        """``AWS::CodeDeploy::DeploymentGroup.Deployment``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-deployment
        """
        return jsii.get(self, "deployment")

    @deployment.setter
    def deployment(self, value: typing.Optional[typing.Union["DeploymentProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "deployment", value)

    @builtins.property
    @jsii.member(jsii_name="deploymentConfigName")
    def deployment_config_name(self) -> typing.Optional[str]:
        """``AWS::CodeDeploy::DeploymentGroup.DeploymentConfigName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-deploymentconfigname
        """
        return jsii.get(self, "deploymentConfigName")

    @deployment_config_name.setter
    def deployment_config_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "deploymentConfigName", value)

    @builtins.property
    @jsii.member(jsii_name="deploymentGroupName")
    def deployment_group_name(self) -> typing.Optional[str]:
        """``AWS::CodeDeploy::DeploymentGroup.DeploymentGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-deploymentgroupname
        """
        return jsii.get(self, "deploymentGroupName")

    @deployment_group_name.setter
    def deployment_group_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "deploymentGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="deploymentStyle")
    def deployment_style(self) -> typing.Optional[typing.Union["DeploymentStyleProperty", _IResolvable_9ceae33e]]:
        """``AWS::CodeDeploy::DeploymentGroup.DeploymentStyle``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-deploymentstyle
        """
        return jsii.get(self, "deploymentStyle")

    @deployment_style.setter
    def deployment_style(self, value: typing.Optional[typing.Union["DeploymentStyleProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "deploymentStyle", value)

    @builtins.property
    @jsii.member(jsii_name="ec2TagFilters")
    def ec2_tag_filters(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["EC2TagFilterProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::CodeDeploy::DeploymentGroup.Ec2TagFilters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-ec2tagfilters
        """
        return jsii.get(self, "ec2TagFilters")

    @ec2_tag_filters.setter
    def ec2_tag_filters(self, value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["EC2TagFilterProperty", _IResolvable_9ceae33e]]]]) -> None:
        jsii.set(self, "ec2TagFilters", value)

    @builtins.property
    @jsii.member(jsii_name="ec2TagSet")
    def ec2_tag_set(self) -> typing.Optional[typing.Union["EC2TagSetProperty", _IResolvable_9ceae33e]]:
        """``AWS::CodeDeploy::DeploymentGroup.Ec2TagSet``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-ec2tagset
        """
        return jsii.get(self, "ec2TagSet")

    @ec2_tag_set.setter
    def ec2_tag_set(self, value: typing.Optional[typing.Union["EC2TagSetProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "ec2TagSet", value)

    @builtins.property
    @jsii.member(jsii_name="loadBalancerInfo")
    def load_balancer_info(self) -> typing.Optional[typing.Union["LoadBalancerInfoProperty", _IResolvable_9ceae33e]]:
        """``AWS::CodeDeploy::DeploymentGroup.LoadBalancerInfo``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-loadbalancerinfo
        """
        return jsii.get(self, "loadBalancerInfo")

    @load_balancer_info.setter
    def load_balancer_info(self, value: typing.Optional[typing.Union["LoadBalancerInfoProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "loadBalancerInfo", value)

    @builtins.property
    @jsii.member(jsii_name="onPremisesInstanceTagFilters")
    def on_premises_instance_tag_filters(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["TagFilterProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::CodeDeploy::DeploymentGroup.OnPremisesInstanceTagFilters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-onpremisesinstancetagfilters
        """
        return jsii.get(self, "onPremisesInstanceTagFilters")

    @on_premises_instance_tag_filters.setter
    def on_premises_instance_tag_filters(self, value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["TagFilterProperty", _IResolvable_9ceae33e]]]]) -> None:
        jsii.set(self, "onPremisesInstanceTagFilters", value)

    @builtins.property
    @jsii.member(jsii_name="onPremisesTagSet")
    def on_premises_tag_set(self) -> typing.Optional[typing.Union["OnPremisesTagSetProperty", _IResolvable_9ceae33e]]:
        """``AWS::CodeDeploy::DeploymentGroup.OnPremisesTagSet``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-onpremisestagset
        """
        return jsii.get(self, "onPremisesTagSet")

    @on_premises_tag_set.setter
    def on_premises_tag_set(self, value: typing.Optional[typing.Union["OnPremisesTagSetProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "onPremisesTagSet", value)

    @builtins.property
    @jsii.member(jsii_name="triggerConfigurations")
    def trigger_configurations(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["TriggerConfigProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::CodeDeploy::DeploymentGroup.TriggerConfigurations``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-triggerconfigurations
        """
        return jsii.get(self, "triggerConfigurations")

    @trigger_configurations.setter
    def trigger_configurations(self, value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["TriggerConfigProperty", _IResolvable_9ceae33e]]]]) -> None:
        jsii.set(self, "triggerConfigurations", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_codedeploy.CfnDeploymentGroup.AlarmConfigurationProperty", jsii_struct_bases=[], name_mapping={'alarms': 'alarms', 'enabled': 'enabled', 'ignore_poll_alarm_failure': 'ignorePollAlarmFailure'})
    class AlarmConfigurationProperty():
        def __init__(self, *, alarms: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnDeploymentGroup.AlarmProperty", _IResolvable_9ceae33e]]]]=None, enabled: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, ignore_poll_alarm_failure: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None) -> None:
            """
            :param alarms: ``CfnDeploymentGroup.AlarmConfigurationProperty.Alarms``.
            :param enabled: ``CfnDeploymentGroup.AlarmConfigurationProperty.Enabled``.
            :param ignore_poll_alarm_failure: ``CfnDeploymentGroup.AlarmConfigurationProperty.IgnorePollAlarmFailure``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-alarmconfiguration.html
            """
            self._values = {
            }
            if alarms is not None: self._values["alarms"] = alarms
            if enabled is not None: self._values["enabled"] = enabled
            if ignore_poll_alarm_failure is not None: self._values["ignore_poll_alarm_failure"] = ignore_poll_alarm_failure

        @builtins.property
        def alarms(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnDeploymentGroup.AlarmProperty", _IResolvable_9ceae33e]]]]:
            """``CfnDeploymentGroup.AlarmConfigurationProperty.Alarms``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-alarmconfiguration.html#cfn-codedeploy-deploymentgroup-alarmconfiguration-alarms
            """
            return self._values.get('alarms')

        @builtins.property
        def enabled(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnDeploymentGroup.AlarmConfigurationProperty.Enabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-alarmconfiguration.html#cfn-codedeploy-deploymentgroup-alarmconfiguration-enabled
            """
            return self._values.get('enabled')

        @builtins.property
        def ignore_poll_alarm_failure(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnDeploymentGroup.AlarmConfigurationProperty.IgnorePollAlarmFailure``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-alarmconfiguration.html#cfn-codedeploy-deploymentgroup-alarmconfiguration-ignorepollalarmfailure
            """
            return self._values.get('ignore_poll_alarm_failure')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AlarmConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_codedeploy.CfnDeploymentGroup.AlarmProperty", jsii_struct_bases=[], name_mapping={'name': 'name'})
    class AlarmProperty():
        def __init__(self, *, name: typing.Optional[str]=None) -> None:
            """
            :param name: ``CfnDeploymentGroup.AlarmProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-alarm.html
            """
            self._values = {
            }
            if name is not None: self._values["name"] = name

        @builtins.property
        def name(self) -> typing.Optional[str]:
            """``CfnDeploymentGroup.AlarmProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-alarm.html#cfn-codedeploy-deploymentgroup-alarm-name
            """
            return self._values.get('name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AlarmProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_codedeploy.CfnDeploymentGroup.AutoRollbackConfigurationProperty", jsii_struct_bases=[], name_mapping={'enabled': 'enabled', 'events': 'events'})
    class AutoRollbackConfigurationProperty():
        def __init__(self, *, enabled: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, events: typing.Optional[typing.List[str]]=None) -> None:
            """
            :param enabled: ``CfnDeploymentGroup.AutoRollbackConfigurationProperty.Enabled``.
            :param events: ``CfnDeploymentGroup.AutoRollbackConfigurationProperty.Events``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-autorollbackconfiguration.html
            """
            self._values = {
            }
            if enabled is not None: self._values["enabled"] = enabled
            if events is not None: self._values["events"] = events

        @builtins.property
        def enabled(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnDeploymentGroup.AutoRollbackConfigurationProperty.Enabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-autorollbackconfiguration.html#cfn-codedeploy-deploymentgroup-autorollbackconfiguration-enabled
            """
            return self._values.get('enabled')

        @builtins.property
        def events(self) -> typing.Optional[typing.List[str]]:
            """``CfnDeploymentGroup.AutoRollbackConfigurationProperty.Events``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-autorollbackconfiguration.html#cfn-codedeploy-deploymentgroup-autorollbackconfiguration-events
            """
            return self._values.get('events')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AutoRollbackConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_codedeploy.CfnDeploymentGroup.DeploymentProperty", jsii_struct_bases=[], name_mapping={'revision': 'revision', 'description': 'description', 'ignore_application_stop_failures': 'ignoreApplicationStopFailures'})
    class DeploymentProperty():
        def __init__(self, *, revision: typing.Union["CfnDeploymentGroup.RevisionLocationProperty", _IResolvable_9ceae33e], description: typing.Optional[str]=None, ignore_application_stop_failures: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None) -> None:
            """
            :param revision: ``CfnDeploymentGroup.DeploymentProperty.Revision``.
            :param description: ``CfnDeploymentGroup.DeploymentProperty.Description``.
            :param ignore_application_stop_failures: ``CfnDeploymentGroup.DeploymentProperty.IgnoreApplicationStopFailures``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment.html
            """
            self._values = {
                'revision': revision,
            }
            if description is not None: self._values["description"] = description
            if ignore_application_stop_failures is not None: self._values["ignore_application_stop_failures"] = ignore_application_stop_failures

        @builtins.property
        def revision(self) -> typing.Union["CfnDeploymentGroup.RevisionLocationProperty", _IResolvable_9ceae33e]:
            """``CfnDeploymentGroup.DeploymentProperty.Revision``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment.html#cfn-properties-codedeploy-deploymentgroup-deployment-revision
            """
            return self._values.get('revision')

        @builtins.property
        def description(self) -> typing.Optional[str]:
            """``CfnDeploymentGroup.DeploymentProperty.Description``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment.html#cfn-properties-codedeploy-deploymentgroup-deployment-description
            """
            return self._values.get('description')

        @builtins.property
        def ignore_application_stop_failures(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnDeploymentGroup.DeploymentProperty.IgnoreApplicationStopFailures``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment.html#cfn-properties-codedeploy-deploymentgroup-deployment-ignoreapplicationstopfailures
            """
            return self._values.get('ignore_application_stop_failures')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'DeploymentProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_codedeploy.CfnDeploymentGroup.DeploymentStyleProperty", jsii_struct_bases=[], name_mapping={'deployment_option': 'deploymentOption', 'deployment_type': 'deploymentType'})
    class DeploymentStyleProperty():
        def __init__(self, *, deployment_option: typing.Optional[str]=None, deployment_type: typing.Optional[str]=None) -> None:
            """
            :param deployment_option: ``CfnDeploymentGroup.DeploymentStyleProperty.DeploymentOption``.
            :param deployment_type: ``CfnDeploymentGroup.DeploymentStyleProperty.DeploymentType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deploymentstyle.html
            """
            self._values = {
            }
            if deployment_option is not None: self._values["deployment_option"] = deployment_option
            if deployment_type is not None: self._values["deployment_type"] = deployment_type

        @builtins.property
        def deployment_option(self) -> typing.Optional[str]:
            """``CfnDeploymentGroup.DeploymentStyleProperty.DeploymentOption``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deploymentstyle.html#cfn-codedeploy-deploymentgroup-deploymentstyle-deploymentoption
            """
            return self._values.get('deployment_option')

        @builtins.property
        def deployment_type(self) -> typing.Optional[str]:
            """``CfnDeploymentGroup.DeploymentStyleProperty.DeploymentType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deploymentstyle.html#cfn-codedeploy-deploymentgroup-deploymentstyle-deploymenttype
            """
            return self._values.get('deployment_type')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'DeploymentStyleProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_codedeploy.CfnDeploymentGroup.EC2TagFilterProperty", jsii_struct_bases=[], name_mapping={'key': 'key', 'type': 'type', 'value': 'value'})
    class EC2TagFilterProperty():
        def __init__(self, *, key: typing.Optional[str]=None, type: typing.Optional[str]=None, value: typing.Optional[str]=None) -> None:
            """
            :param key: ``CfnDeploymentGroup.EC2TagFilterProperty.Key``.
            :param type: ``CfnDeploymentGroup.EC2TagFilterProperty.Type``.
            :param value: ``CfnDeploymentGroup.EC2TagFilterProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-ec2tagfilter.html
            """
            self._values = {
            }
            if key is not None: self._values["key"] = key
            if type is not None: self._values["type"] = type
            if value is not None: self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[str]:
            """``CfnDeploymentGroup.EC2TagFilterProperty.Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-ec2tagfilter.html#cfn-codedeploy-deploymentgroup-ec2tagfilter-key
            """
            return self._values.get('key')

        @builtins.property
        def type(self) -> typing.Optional[str]:
            """``CfnDeploymentGroup.EC2TagFilterProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-ec2tagfilter.html#cfn-codedeploy-deploymentgroup-ec2tagfilter-type
            """
            return self._values.get('type')

        @builtins.property
        def value(self) -> typing.Optional[str]:
            """``CfnDeploymentGroup.EC2TagFilterProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-ec2tagfilter.html#cfn-codedeploy-deploymentgroup-ec2tagfilter-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'EC2TagFilterProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_codedeploy.CfnDeploymentGroup.EC2TagSetListObjectProperty", jsii_struct_bases=[], name_mapping={'ec2_tag_group': 'ec2TagGroup'})
    class EC2TagSetListObjectProperty():
        def __init__(self, *, ec2_tag_group: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnDeploymentGroup.EC2TagFilterProperty", _IResolvable_9ceae33e]]]]=None) -> None:
            """
            :param ec2_tag_group: ``CfnDeploymentGroup.EC2TagSetListObjectProperty.Ec2TagGroup``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-ec2tagsetlistobject.html
            """
            self._values = {
            }
            if ec2_tag_group is not None: self._values["ec2_tag_group"] = ec2_tag_group

        @builtins.property
        def ec2_tag_group(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnDeploymentGroup.EC2TagFilterProperty", _IResolvable_9ceae33e]]]]:
            """``CfnDeploymentGroup.EC2TagSetListObjectProperty.Ec2TagGroup``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-ec2tagsetlistobject.html#cfn-codedeploy-deploymentgroup-ec2tagsetlistobject-ec2taggroup
            """
            return self._values.get('ec2_tag_group')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'EC2TagSetListObjectProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_codedeploy.CfnDeploymentGroup.EC2TagSetProperty", jsii_struct_bases=[], name_mapping={'ec2_tag_set_list': 'ec2TagSetList'})
    class EC2TagSetProperty():
        def __init__(self, *, ec2_tag_set_list: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnDeploymentGroup.EC2TagSetListObjectProperty", _IResolvable_9ceae33e]]]]=None) -> None:
            """
            :param ec2_tag_set_list: ``CfnDeploymentGroup.EC2TagSetProperty.Ec2TagSetList``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-ec2tagset.html
            """
            self._values = {
            }
            if ec2_tag_set_list is not None: self._values["ec2_tag_set_list"] = ec2_tag_set_list

        @builtins.property
        def ec2_tag_set_list(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnDeploymentGroup.EC2TagSetListObjectProperty", _IResolvable_9ceae33e]]]]:
            """``CfnDeploymentGroup.EC2TagSetProperty.Ec2TagSetList``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-ec2tagset.html#cfn-codedeploy-deploymentgroup-ec2tagset-ec2tagsetlist
            """
            return self._values.get('ec2_tag_set_list')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'EC2TagSetProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_codedeploy.CfnDeploymentGroup.ELBInfoProperty", jsii_struct_bases=[], name_mapping={'name': 'name'})
    class ELBInfoProperty():
        def __init__(self, *, name: typing.Optional[str]=None) -> None:
            """
            :param name: ``CfnDeploymentGroup.ELBInfoProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-elbinfo.html
            """
            self._values = {
            }
            if name is not None: self._values["name"] = name

        @builtins.property
        def name(self) -> typing.Optional[str]:
            """``CfnDeploymentGroup.ELBInfoProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-elbinfo.html#cfn-codedeploy-deploymentgroup-elbinfo-name
            """
            return self._values.get('name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ELBInfoProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_codedeploy.CfnDeploymentGroup.GitHubLocationProperty", jsii_struct_bases=[], name_mapping={'commit_id': 'commitId', 'repository': 'repository'})
    class GitHubLocationProperty():
        def __init__(self, *, commit_id: str, repository: str) -> None:
            """
            :param commit_id: ``CfnDeploymentGroup.GitHubLocationProperty.CommitId``.
            :param repository: ``CfnDeploymentGroup.GitHubLocationProperty.Repository``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision-githublocation.html
            """
            self._values = {
                'commit_id': commit_id,
                'repository': repository,
            }

        @builtins.property
        def commit_id(self) -> str:
            """``CfnDeploymentGroup.GitHubLocationProperty.CommitId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision-githublocation.html#cfn-properties-codedeploy-deploymentgroup-deployment-revision-githublocation-commitid
            """
            return self._values.get('commit_id')

        @builtins.property
        def repository(self) -> str:
            """``CfnDeploymentGroup.GitHubLocationProperty.Repository``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision-githublocation.html#cfn-properties-codedeploy-deploymentgroup-deployment-revision-githublocation-repository
            """
            return self._values.get('repository')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'GitHubLocationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_codedeploy.CfnDeploymentGroup.LoadBalancerInfoProperty", jsii_struct_bases=[], name_mapping={'elb_info_list': 'elbInfoList', 'target_group_info_list': 'targetGroupInfoList'})
    class LoadBalancerInfoProperty():
        def __init__(self, *, elb_info_list: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnDeploymentGroup.ELBInfoProperty", _IResolvable_9ceae33e]]]]=None, target_group_info_list: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnDeploymentGroup.TargetGroupInfoProperty", _IResolvable_9ceae33e]]]]=None) -> None:
            """
            :param elb_info_list: ``CfnDeploymentGroup.LoadBalancerInfoProperty.ElbInfoList``.
            :param target_group_info_list: ``CfnDeploymentGroup.LoadBalancerInfoProperty.TargetGroupInfoList``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-loadbalancerinfo.html
            """
            self._values = {
            }
            if elb_info_list is not None: self._values["elb_info_list"] = elb_info_list
            if target_group_info_list is not None: self._values["target_group_info_list"] = target_group_info_list

        @builtins.property
        def elb_info_list(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnDeploymentGroup.ELBInfoProperty", _IResolvable_9ceae33e]]]]:
            """``CfnDeploymentGroup.LoadBalancerInfoProperty.ElbInfoList``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-loadbalancerinfo.html#cfn-codedeploy-deploymentgroup-loadbalancerinfo-elbinfolist
            """
            return self._values.get('elb_info_list')

        @builtins.property
        def target_group_info_list(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnDeploymentGroup.TargetGroupInfoProperty", _IResolvable_9ceae33e]]]]:
            """``CfnDeploymentGroup.LoadBalancerInfoProperty.TargetGroupInfoList``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-loadbalancerinfo.html#cfn-codedeploy-deploymentgroup-loadbalancerinfo-targetgroupinfolist
            """
            return self._values.get('target_group_info_list')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'LoadBalancerInfoProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_codedeploy.CfnDeploymentGroup.OnPremisesTagSetListObjectProperty", jsii_struct_bases=[], name_mapping={'on_premises_tag_group': 'onPremisesTagGroup'})
    class OnPremisesTagSetListObjectProperty():
        def __init__(self, *, on_premises_tag_group: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnDeploymentGroup.TagFilterProperty", _IResolvable_9ceae33e]]]]=None) -> None:
            """
            :param on_premises_tag_group: ``CfnDeploymentGroup.OnPremisesTagSetListObjectProperty.OnPremisesTagGroup``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-onpremisestagsetlistobject.html
            """
            self._values = {
            }
            if on_premises_tag_group is not None: self._values["on_premises_tag_group"] = on_premises_tag_group

        @builtins.property
        def on_premises_tag_group(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnDeploymentGroup.TagFilterProperty", _IResolvable_9ceae33e]]]]:
            """``CfnDeploymentGroup.OnPremisesTagSetListObjectProperty.OnPremisesTagGroup``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-onpremisestagsetlistobject.html#cfn-codedeploy-deploymentgroup-onpremisestagsetlistobject-onpremisestaggroup
            """
            return self._values.get('on_premises_tag_group')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'OnPremisesTagSetListObjectProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_codedeploy.CfnDeploymentGroup.OnPremisesTagSetProperty", jsii_struct_bases=[], name_mapping={'on_premises_tag_set_list': 'onPremisesTagSetList'})
    class OnPremisesTagSetProperty():
        def __init__(self, *, on_premises_tag_set_list: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnDeploymentGroup.OnPremisesTagSetListObjectProperty", _IResolvable_9ceae33e]]]]=None) -> None:
            """
            :param on_premises_tag_set_list: ``CfnDeploymentGroup.OnPremisesTagSetProperty.OnPremisesTagSetList``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-onpremisestagset.html
            """
            self._values = {
            }
            if on_premises_tag_set_list is not None: self._values["on_premises_tag_set_list"] = on_premises_tag_set_list

        @builtins.property
        def on_premises_tag_set_list(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnDeploymentGroup.OnPremisesTagSetListObjectProperty", _IResolvable_9ceae33e]]]]:
            """``CfnDeploymentGroup.OnPremisesTagSetProperty.OnPremisesTagSetList``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-onpremisestagset.html#cfn-codedeploy-deploymentgroup-onpremisestagset-onpremisestagsetlist
            """
            return self._values.get('on_premises_tag_set_list')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'OnPremisesTagSetProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_codedeploy.CfnDeploymentGroup.RevisionLocationProperty", jsii_struct_bases=[], name_mapping={'git_hub_location': 'gitHubLocation', 'revision_type': 'revisionType', 's3_location': 's3Location'})
    class RevisionLocationProperty():
        def __init__(self, *, git_hub_location: typing.Optional[typing.Union["CfnDeploymentGroup.GitHubLocationProperty", _IResolvable_9ceae33e]]=None, revision_type: typing.Optional[str]=None, s3_location: typing.Optional[typing.Union["CfnDeploymentGroup.S3LocationProperty", _IResolvable_9ceae33e]]=None) -> None:
            """
            :param git_hub_location: ``CfnDeploymentGroup.RevisionLocationProperty.GitHubLocation``.
            :param revision_type: ``CfnDeploymentGroup.RevisionLocationProperty.RevisionType``.
            :param s3_location: ``CfnDeploymentGroup.RevisionLocationProperty.S3Location``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision.html
            """
            self._values = {
            }
            if git_hub_location is not None: self._values["git_hub_location"] = git_hub_location
            if revision_type is not None: self._values["revision_type"] = revision_type
            if s3_location is not None: self._values["s3_location"] = s3_location

        @builtins.property
        def git_hub_location(self) -> typing.Optional[typing.Union["CfnDeploymentGroup.GitHubLocationProperty", _IResolvable_9ceae33e]]:
            """``CfnDeploymentGroup.RevisionLocationProperty.GitHubLocation``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision.html#cfn-properties-codedeploy-deploymentgroup-deployment-revision-githublocation
            """
            return self._values.get('git_hub_location')

        @builtins.property
        def revision_type(self) -> typing.Optional[str]:
            """``CfnDeploymentGroup.RevisionLocationProperty.RevisionType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision.html#cfn-properties-codedeploy-deploymentgroup-deployment-revision-revisiontype
            """
            return self._values.get('revision_type')

        @builtins.property
        def s3_location(self) -> typing.Optional[typing.Union["CfnDeploymentGroup.S3LocationProperty", _IResolvable_9ceae33e]]:
            """``CfnDeploymentGroup.RevisionLocationProperty.S3Location``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision.html#cfn-properties-codedeploy-deploymentgroup-deployment-revision-s3location
            """
            return self._values.get('s3_location')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'RevisionLocationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_codedeploy.CfnDeploymentGroup.S3LocationProperty", jsii_struct_bases=[], name_mapping={'bucket': 'bucket', 'key': 'key', 'bundle_type': 'bundleType', 'e_tag': 'eTag', 'version': 'version'})
    class S3LocationProperty():
        def __init__(self, *, bucket: str, key: str, bundle_type: typing.Optional[str]=None, e_tag: typing.Optional[str]=None, version: typing.Optional[str]=None) -> None:
            """
            :param bucket: ``CfnDeploymentGroup.S3LocationProperty.Bucket``.
            :param key: ``CfnDeploymentGroup.S3LocationProperty.Key``.
            :param bundle_type: ``CfnDeploymentGroup.S3LocationProperty.BundleType``.
            :param e_tag: ``CfnDeploymentGroup.S3LocationProperty.ETag``.
            :param version: ``CfnDeploymentGroup.S3LocationProperty.Version``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision-s3location.html
            """
            self._values = {
                'bucket': bucket,
                'key': key,
            }
            if bundle_type is not None: self._values["bundle_type"] = bundle_type
            if e_tag is not None: self._values["e_tag"] = e_tag
            if version is not None: self._values["version"] = version

        @builtins.property
        def bucket(self) -> str:
            """``CfnDeploymentGroup.S3LocationProperty.Bucket``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision-s3location.html#cfn-properties-codedeploy-deploymentgroup-deployment-revision-s3location-bucket
            """
            return self._values.get('bucket')

        @builtins.property
        def key(self) -> str:
            """``CfnDeploymentGroup.S3LocationProperty.Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision-s3location.html#cfn-properties-codedeploy-deploymentgroup-deployment-revision-s3location-key
            """
            return self._values.get('key')

        @builtins.property
        def bundle_type(self) -> typing.Optional[str]:
            """``CfnDeploymentGroup.S3LocationProperty.BundleType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision-s3location.html#cfn-properties-codedeploy-deploymentgroup-deployment-revision-s3location-bundletype
            """
            return self._values.get('bundle_type')

        @builtins.property
        def e_tag(self) -> typing.Optional[str]:
            """``CfnDeploymentGroup.S3LocationProperty.ETag``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision-s3location.html#cfn-properties-codedeploy-deploymentgroup-deployment-revision-s3location-etag
            """
            return self._values.get('e_tag')

        @builtins.property
        def version(self) -> typing.Optional[str]:
            """``CfnDeploymentGroup.S3LocationProperty.Version``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision-s3location.html#cfn-properties-codedeploy-deploymentgroup-deployment-revision-s3location-value
            """
            return self._values.get('version')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'S3LocationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_codedeploy.CfnDeploymentGroup.TagFilterProperty", jsii_struct_bases=[], name_mapping={'key': 'key', 'type': 'type', 'value': 'value'})
    class TagFilterProperty():
        def __init__(self, *, key: typing.Optional[str]=None, type: typing.Optional[str]=None, value: typing.Optional[str]=None) -> None:
            """
            :param key: ``CfnDeploymentGroup.TagFilterProperty.Key``.
            :param type: ``CfnDeploymentGroup.TagFilterProperty.Type``.
            :param value: ``CfnDeploymentGroup.TagFilterProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-tagfilter.html
            """
            self._values = {
            }
            if key is not None: self._values["key"] = key
            if type is not None: self._values["type"] = type
            if value is not None: self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[str]:
            """``CfnDeploymentGroup.TagFilterProperty.Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-tagfilter.html#cfn-codedeploy-deploymentgroup-tagfilter-key
            """
            return self._values.get('key')

        @builtins.property
        def type(self) -> typing.Optional[str]:
            """``CfnDeploymentGroup.TagFilterProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-tagfilter.html#cfn-codedeploy-deploymentgroup-tagfilter-type
            """
            return self._values.get('type')

        @builtins.property
        def value(self) -> typing.Optional[str]:
            """``CfnDeploymentGroup.TagFilterProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-tagfilter.html#cfn-codedeploy-deploymentgroup-tagfilter-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'TagFilterProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_codedeploy.CfnDeploymentGroup.TargetGroupInfoProperty", jsii_struct_bases=[], name_mapping={'name': 'name'})
    class TargetGroupInfoProperty():
        def __init__(self, *, name: typing.Optional[str]=None) -> None:
            """
            :param name: ``CfnDeploymentGroup.TargetGroupInfoProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-targetgroupinfo.html
            """
            self._values = {
            }
            if name is not None: self._values["name"] = name

        @builtins.property
        def name(self) -> typing.Optional[str]:
            """``CfnDeploymentGroup.TargetGroupInfoProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-targetgroupinfo.html#cfn-codedeploy-deploymentgroup-targetgroupinfo-name
            """
            return self._values.get('name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'TargetGroupInfoProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_codedeploy.CfnDeploymentGroup.TriggerConfigProperty", jsii_struct_bases=[], name_mapping={'trigger_events': 'triggerEvents', 'trigger_name': 'triggerName', 'trigger_target_arn': 'triggerTargetArn'})
    class TriggerConfigProperty():
        def __init__(self, *, trigger_events: typing.Optional[typing.List[str]]=None, trigger_name: typing.Optional[str]=None, trigger_target_arn: typing.Optional[str]=None) -> None:
            """
            :param trigger_events: ``CfnDeploymentGroup.TriggerConfigProperty.TriggerEvents``.
            :param trigger_name: ``CfnDeploymentGroup.TriggerConfigProperty.TriggerName``.
            :param trigger_target_arn: ``CfnDeploymentGroup.TriggerConfigProperty.TriggerTargetArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-triggerconfig.html
            """
            self._values = {
            }
            if trigger_events is not None: self._values["trigger_events"] = trigger_events
            if trigger_name is not None: self._values["trigger_name"] = trigger_name
            if trigger_target_arn is not None: self._values["trigger_target_arn"] = trigger_target_arn

        @builtins.property
        def trigger_events(self) -> typing.Optional[typing.List[str]]:
            """``CfnDeploymentGroup.TriggerConfigProperty.TriggerEvents``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-triggerconfig.html#cfn-codedeploy-deploymentgroup-triggerconfig-triggerevents
            """
            return self._values.get('trigger_events')

        @builtins.property
        def trigger_name(self) -> typing.Optional[str]:
            """``CfnDeploymentGroup.TriggerConfigProperty.TriggerName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-triggerconfig.html#cfn-codedeploy-deploymentgroup-triggerconfig-triggername
            """
            return self._values.get('trigger_name')

        @builtins.property
        def trigger_target_arn(self) -> typing.Optional[str]:
            """``CfnDeploymentGroup.TriggerConfigProperty.TriggerTargetArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-triggerconfig.html#cfn-codedeploy-deploymentgroup-triggerconfig-triggertargetarn
            """
            return self._values.get('trigger_target_arn')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'TriggerConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_codedeploy.CfnDeploymentGroupProps", jsii_struct_bases=[], name_mapping={'application_name': 'applicationName', 'service_role_arn': 'serviceRoleArn', 'alarm_configuration': 'alarmConfiguration', 'auto_rollback_configuration': 'autoRollbackConfiguration', 'auto_scaling_groups': 'autoScalingGroups', 'deployment': 'deployment', 'deployment_config_name': 'deploymentConfigName', 'deployment_group_name': 'deploymentGroupName', 'deployment_style': 'deploymentStyle', 'ec2_tag_filters': 'ec2TagFilters', 'ec2_tag_set': 'ec2TagSet', 'load_balancer_info': 'loadBalancerInfo', 'on_premises_instance_tag_filters': 'onPremisesInstanceTagFilters', 'on_premises_tag_set': 'onPremisesTagSet', 'trigger_configurations': 'triggerConfigurations'})
class CfnDeploymentGroupProps():
    def __init__(self, *, application_name: str, service_role_arn: str, alarm_configuration: typing.Optional[typing.Union["CfnDeploymentGroup.AlarmConfigurationProperty", _IResolvable_9ceae33e]]=None, auto_rollback_configuration: typing.Optional[typing.Union["CfnDeploymentGroup.AutoRollbackConfigurationProperty", _IResolvable_9ceae33e]]=None, auto_scaling_groups: typing.Optional[typing.List[str]]=None, deployment: typing.Optional[typing.Union["CfnDeploymentGroup.DeploymentProperty", _IResolvable_9ceae33e]]=None, deployment_config_name: typing.Optional[str]=None, deployment_group_name: typing.Optional[str]=None, deployment_style: typing.Optional[typing.Union["CfnDeploymentGroup.DeploymentStyleProperty", _IResolvable_9ceae33e]]=None, ec2_tag_filters: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnDeploymentGroup.EC2TagFilterProperty", _IResolvable_9ceae33e]]]]=None, ec2_tag_set: typing.Optional[typing.Union["CfnDeploymentGroup.EC2TagSetProperty", _IResolvable_9ceae33e]]=None, load_balancer_info: typing.Optional[typing.Union["CfnDeploymentGroup.LoadBalancerInfoProperty", _IResolvable_9ceae33e]]=None, on_premises_instance_tag_filters: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnDeploymentGroup.TagFilterProperty", _IResolvable_9ceae33e]]]]=None, on_premises_tag_set: typing.Optional[typing.Union["CfnDeploymentGroup.OnPremisesTagSetProperty", _IResolvable_9ceae33e]]=None, trigger_configurations: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnDeploymentGroup.TriggerConfigProperty", _IResolvable_9ceae33e]]]]=None) -> None:
        """Properties for defining a ``AWS::CodeDeploy::DeploymentGroup``.

        :param application_name: ``AWS::CodeDeploy::DeploymentGroup.ApplicationName``.
        :param service_role_arn: ``AWS::CodeDeploy::DeploymentGroup.ServiceRoleArn``.
        :param alarm_configuration: ``AWS::CodeDeploy::DeploymentGroup.AlarmConfiguration``.
        :param auto_rollback_configuration: ``AWS::CodeDeploy::DeploymentGroup.AutoRollbackConfiguration``.
        :param auto_scaling_groups: ``AWS::CodeDeploy::DeploymentGroup.AutoScalingGroups``.
        :param deployment: ``AWS::CodeDeploy::DeploymentGroup.Deployment``.
        :param deployment_config_name: ``AWS::CodeDeploy::DeploymentGroup.DeploymentConfigName``.
        :param deployment_group_name: ``AWS::CodeDeploy::DeploymentGroup.DeploymentGroupName``.
        :param deployment_style: ``AWS::CodeDeploy::DeploymentGroup.DeploymentStyle``.
        :param ec2_tag_filters: ``AWS::CodeDeploy::DeploymentGroup.Ec2TagFilters``.
        :param ec2_tag_set: ``AWS::CodeDeploy::DeploymentGroup.Ec2TagSet``.
        :param load_balancer_info: ``AWS::CodeDeploy::DeploymentGroup.LoadBalancerInfo``.
        :param on_premises_instance_tag_filters: ``AWS::CodeDeploy::DeploymentGroup.OnPremisesInstanceTagFilters``.
        :param on_premises_tag_set: ``AWS::CodeDeploy::DeploymentGroup.OnPremisesTagSet``.
        :param trigger_configurations: ``AWS::CodeDeploy::DeploymentGroup.TriggerConfigurations``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html
        """
        self._values = {
            'application_name': application_name,
            'service_role_arn': service_role_arn,
        }
        if alarm_configuration is not None: self._values["alarm_configuration"] = alarm_configuration
        if auto_rollback_configuration is not None: self._values["auto_rollback_configuration"] = auto_rollback_configuration
        if auto_scaling_groups is not None: self._values["auto_scaling_groups"] = auto_scaling_groups
        if deployment is not None: self._values["deployment"] = deployment
        if deployment_config_name is not None: self._values["deployment_config_name"] = deployment_config_name
        if deployment_group_name is not None: self._values["deployment_group_name"] = deployment_group_name
        if deployment_style is not None: self._values["deployment_style"] = deployment_style
        if ec2_tag_filters is not None: self._values["ec2_tag_filters"] = ec2_tag_filters
        if ec2_tag_set is not None: self._values["ec2_tag_set"] = ec2_tag_set
        if load_balancer_info is not None: self._values["load_balancer_info"] = load_balancer_info
        if on_premises_instance_tag_filters is not None: self._values["on_premises_instance_tag_filters"] = on_premises_instance_tag_filters
        if on_premises_tag_set is not None: self._values["on_premises_tag_set"] = on_premises_tag_set
        if trigger_configurations is not None: self._values["trigger_configurations"] = trigger_configurations

    @builtins.property
    def application_name(self) -> str:
        """``AWS::CodeDeploy::DeploymentGroup.ApplicationName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-applicationname
        """
        return self._values.get('application_name')

    @builtins.property
    def service_role_arn(self) -> str:
        """``AWS::CodeDeploy::DeploymentGroup.ServiceRoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-servicerolearn
        """
        return self._values.get('service_role_arn')

    @builtins.property
    def alarm_configuration(self) -> typing.Optional[typing.Union["CfnDeploymentGroup.AlarmConfigurationProperty", _IResolvable_9ceae33e]]:
        """``AWS::CodeDeploy::DeploymentGroup.AlarmConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-alarmconfiguration
        """
        return self._values.get('alarm_configuration')

    @builtins.property
    def auto_rollback_configuration(self) -> typing.Optional[typing.Union["CfnDeploymentGroup.AutoRollbackConfigurationProperty", _IResolvable_9ceae33e]]:
        """``AWS::CodeDeploy::DeploymentGroup.AutoRollbackConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-autorollbackconfiguration
        """
        return self._values.get('auto_rollback_configuration')

    @builtins.property
    def auto_scaling_groups(self) -> typing.Optional[typing.List[str]]:
        """``AWS::CodeDeploy::DeploymentGroup.AutoScalingGroups``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-autoscalinggroups
        """
        return self._values.get('auto_scaling_groups')

    @builtins.property
    def deployment(self) -> typing.Optional[typing.Union["CfnDeploymentGroup.DeploymentProperty", _IResolvable_9ceae33e]]:
        """``AWS::CodeDeploy::DeploymentGroup.Deployment``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-deployment
        """
        return self._values.get('deployment')

    @builtins.property
    def deployment_config_name(self) -> typing.Optional[str]:
        """``AWS::CodeDeploy::DeploymentGroup.DeploymentConfigName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-deploymentconfigname
        """
        return self._values.get('deployment_config_name')

    @builtins.property
    def deployment_group_name(self) -> typing.Optional[str]:
        """``AWS::CodeDeploy::DeploymentGroup.DeploymentGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-deploymentgroupname
        """
        return self._values.get('deployment_group_name')

    @builtins.property
    def deployment_style(self) -> typing.Optional[typing.Union["CfnDeploymentGroup.DeploymentStyleProperty", _IResolvable_9ceae33e]]:
        """``AWS::CodeDeploy::DeploymentGroup.DeploymentStyle``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-deploymentstyle
        """
        return self._values.get('deployment_style')

    @builtins.property
    def ec2_tag_filters(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnDeploymentGroup.EC2TagFilterProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::CodeDeploy::DeploymentGroup.Ec2TagFilters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-ec2tagfilters
        """
        return self._values.get('ec2_tag_filters')

    @builtins.property
    def ec2_tag_set(self) -> typing.Optional[typing.Union["CfnDeploymentGroup.EC2TagSetProperty", _IResolvable_9ceae33e]]:
        """``AWS::CodeDeploy::DeploymentGroup.Ec2TagSet``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-ec2tagset
        """
        return self._values.get('ec2_tag_set')

    @builtins.property
    def load_balancer_info(self) -> typing.Optional[typing.Union["CfnDeploymentGroup.LoadBalancerInfoProperty", _IResolvable_9ceae33e]]:
        """``AWS::CodeDeploy::DeploymentGroup.LoadBalancerInfo``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-loadbalancerinfo
        """
        return self._values.get('load_balancer_info')

    @builtins.property
    def on_premises_instance_tag_filters(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnDeploymentGroup.TagFilterProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::CodeDeploy::DeploymentGroup.OnPremisesInstanceTagFilters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-onpremisesinstancetagfilters
        """
        return self._values.get('on_premises_instance_tag_filters')

    @builtins.property
    def on_premises_tag_set(self) -> typing.Optional[typing.Union["CfnDeploymentGroup.OnPremisesTagSetProperty", _IResolvable_9ceae33e]]:
        """``AWS::CodeDeploy::DeploymentGroup.OnPremisesTagSet``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-onpremisestagset
        """
        return self._values.get('on_premises_tag_set')

    @builtins.property
    def trigger_configurations(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnDeploymentGroup.TriggerConfigProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::CodeDeploy::DeploymentGroup.TriggerConfigurations``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-triggerconfigurations
        """
        return self._values.get('trigger_configurations')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnDeploymentGroupProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_codedeploy.EcsApplicationProps", jsii_struct_bases=[], name_mapping={'application_name': 'applicationName'})
class EcsApplicationProps():
    def __init__(self, *, application_name: typing.Optional[str]=None) -> None:
        """Construction properties for {@link EcsApplication}.

        :param application_name: The physical, human-readable name of the CodeDeploy Application. Default: an auto-generated name will be used

        stability
        :stability: experimental
        """
        self._values = {
        }
        if application_name is not None: self._values["application_name"] = application_name

    @builtins.property
    def application_name(self) -> typing.Optional[str]:
        """The physical, human-readable name of the CodeDeploy Application.

        default
        :default: an auto-generated name will be used

        stability
        :stability: experimental
        """
        return self._values.get('application_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EcsApplicationProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class EcsDeploymentConfig(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_codedeploy.EcsDeploymentConfig"):
    """A custom Deployment Configuration for an ECS Deployment Group.

    Note: This class currently stands as namespaced container of the default configurations
    until CloudFormation supports custom ECS Deployment Configs. Until then it is closed
    (private constructor) and does not extend {@link cdk.Construct}

    stability
    :stability: experimental
    resource:
    :resource:: AWS::CodeDeploy::DeploymentConfig
    """
    @jsii.member(jsii_name="fromEcsDeploymentConfigName")
    @builtins.classmethod
    def from_ecs_deployment_config_name(cls, _scope: _Construct_f50a3f53, _id: str, ecs_deployment_config_name: str) -> "IEcsDeploymentConfig":
        """Import a custom Deployment Configuration for an ECS Deployment Group defined outside the CDK.

        :param _scope: the parent Construct for this new Construct.
        :param _id: the logical ID of this new Construct.
        :param ecs_deployment_config_name: the name of the referenced custom Deployment Configuration.

        return
        :return: a Construct representing a reference to an existing custom Deployment Configuration

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromEcsDeploymentConfigName", [_scope, _id, ecs_deployment_config_name])

    @jsii.python.classproperty
    @jsii.member(jsii_name="ALL_AT_ONCE")
    def ALL_AT_ONCE(cls) -> "IEcsDeploymentConfig":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "ALL_AT_ONCE")


class EcsDeploymentGroup(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_codedeploy.EcsDeploymentGroup"):
    """Note: This class currently stands as a namespaced container for importing an ECS Deployment Group defined outside the CDK app until CloudFormation supports provisioning ECS Deployment Groups.

    Until then it is closed (private constructor) and does not
    extend {@link cdk.Construct}.

    stability
    :stability: experimental
    resource:
    :resource:: AWS::CodeDeploy::DeploymentGroup
    """
    @jsii.member(jsii_name="fromEcsDeploymentGroupAttributes")
    @builtins.classmethod
    def from_ecs_deployment_group_attributes(cls, scope: _Construct_f50a3f53, id: str, *, application: "IEcsApplication", deployment_group_name: str, deployment_config: typing.Optional["IEcsDeploymentConfig"]=None) -> "IEcsDeploymentGroup":
        """Import an ECS Deployment Group defined outside the CDK app.

        :param scope: the parent Construct for this new Construct.
        :param id: the logical ID of this new Construct.
        :param application: The reference to the CodeDeploy ECS Application that this Deployment Group belongs to.
        :param deployment_group_name: The physical, human-readable name of the CodeDeploy ECS Deployment Group that we are referencing.
        :param deployment_config: The Deployment Configuration this Deployment Group uses. Default: EcsDeploymentConfig.ALL_AT_ONCE

        return
        :return: a Construct representing a reference to an existing Deployment Group

        stability
        :stability: experimental
        """
        attrs = EcsDeploymentGroupAttributes(application=application, deployment_group_name=deployment_group_name, deployment_config=deployment_config)

        return jsii.sinvoke(cls, "fromEcsDeploymentGroupAttributes", [scope, id, attrs])


@jsii.data_type(jsii_type="monocdk-experiment.aws_codedeploy.EcsDeploymentGroupAttributes", jsii_struct_bases=[], name_mapping={'application': 'application', 'deployment_group_name': 'deploymentGroupName', 'deployment_config': 'deploymentConfig'})
class EcsDeploymentGroupAttributes():
    def __init__(self, *, application: "IEcsApplication", deployment_group_name: str, deployment_config: typing.Optional["IEcsDeploymentConfig"]=None) -> None:
        """Properties of a reference to a CodeDeploy ECS Deployment Group.

        :param application: The reference to the CodeDeploy ECS Application that this Deployment Group belongs to.
        :param deployment_group_name: The physical, human-readable name of the CodeDeploy ECS Deployment Group that we are referencing.
        :param deployment_config: The Deployment Configuration this Deployment Group uses. Default: EcsDeploymentConfig.ALL_AT_ONCE

        see
        :see: EcsDeploymentGroup#fromEcsDeploymentGroupAttributes
        stability
        :stability: experimental
        """
        self._values = {
            'application': application,
            'deployment_group_name': deployment_group_name,
        }
        if deployment_config is not None: self._values["deployment_config"] = deployment_config

    @builtins.property
    def application(self) -> "IEcsApplication":
        """The reference to the CodeDeploy ECS Application that this Deployment Group belongs to.

        stability
        :stability: experimental
        """
        return self._values.get('application')

    @builtins.property
    def deployment_group_name(self) -> str:
        """The physical, human-readable name of the CodeDeploy ECS Deployment Group that we are referencing.

        stability
        :stability: experimental
        """
        return self._values.get('deployment_group_name')

    @builtins.property
    def deployment_config(self) -> typing.Optional["IEcsDeploymentConfig"]:
        """The Deployment Configuration this Deployment Group uses.

        default
        :default: EcsDeploymentConfig.ALL_AT_ONCE

        stability
        :stability: experimental
        """
        return self._values.get('deployment_config')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EcsDeploymentGroupAttributes(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.interface(jsii_type="monocdk-experiment.aws_codedeploy.IEcsApplication")
class IEcsApplication(_IResource_72f7ee7e, jsii.compat.Protocol):
    """Represents a reference to a CodeDeploy Application deploying to Amazon ECS.

    If you're managing the Application alongside the rest of your CDK resources,
    use the {@link EcsApplication} class.

    If you want to reference an already existing Application,
    or one defined in a different CDK Stack,
    use the {@link EcsApplication#fromEcsApplicationName} method.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IEcsApplicationProxy

    @builtins.property
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> str:
        """
        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> str:
        """
        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...


class _IEcsApplicationProxy(jsii.proxy_for(_IResource_72f7ee7e)):
    """Represents a reference to a CodeDeploy Application deploying to Amazon ECS.

    If you're managing the Application alongside the rest of your CDK resources,
    use the {@link EcsApplication} class.

    If you want to reference an already existing Application,
    or one defined in a different CDK Stack,
    use the {@link EcsApplication#fromEcsApplicationName} method.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_codedeploy.IEcsApplication"
    @builtins.property
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> str:
        """
        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "applicationArn")

    @builtins.property
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> str:
        """
        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "applicationName")


@jsii.interface(jsii_type="monocdk-experiment.aws_codedeploy.IEcsDeploymentConfig")
class IEcsDeploymentConfig(jsii.compat.Protocol):
    """The Deployment Configuration of an ECS Deployment Group.

    The default, pre-defined Configurations are available as constants on the {@link EcsDeploymentConfig} class
    (for example, ``EcsDeploymentConfig.AllAtOnce``).

    Note: CloudFormation does not currently support creating custom ECS configs outside
    of using a custom resource. You can import custom deployment config created outside the
    CDK or via a custom resource with {@link EcsDeploymentConfig#fromEcsDeploymentConfigName}.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IEcsDeploymentConfigProxy

    @builtins.property
    @jsii.member(jsii_name="deploymentConfigArn")
    def deployment_config_arn(self) -> str:
        """
        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="deploymentConfigName")
    def deployment_config_name(self) -> str:
        """
        stability
        :stability: experimental
        """
        ...


class _IEcsDeploymentConfigProxy():
    """The Deployment Configuration of an ECS Deployment Group.

    The default, pre-defined Configurations are available as constants on the {@link EcsDeploymentConfig} class
    (for example, ``EcsDeploymentConfig.AllAtOnce``).

    Note: CloudFormation does not currently support creating custom ECS configs outside
    of using a custom resource. You can import custom deployment config created outside the
    CDK or via a custom resource with {@link EcsDeploymentConfig#fromEcsDeploymentConfigName}.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_codedeploy.IEcsDeploymentConfig"
    @builtins.property
    @jsii.member(jsii_name="deploymentConfigArn")
    def deployment_config_arn(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "deploymentConfigArn")

    @builtins.property
    @jsii.member(jsii_name="deploymentConfigName")
    def deployment_config_name(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "deploymentConfigName")


@jsii.interface(jsii_type="monocdk-experiment.aws_codedeploy.IEcsDeploymentGroup")
class IEcsDeploymentGroup(_IResource_72f7ee7e, jsii.compat.Protocol):
    """Interface for an ECS deployment group.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IEcsDeploymentGroupProxy

    @builtins.property
    @jsii.member(jsii_name="application")
    def application(self) -> "IEcsApplication":
        """The reference to the CodeDeploy ECS Application that this Deployment Group belongs to.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="deploymentConfig")
    def deployment_config(self) -> "IEcsDeploymentConfig":
        """The Deployment Configuration this Group uses.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="deploymentGroupArn")
    def deployment_group_arn(self) -> str:
        """The ARN of this Deployment Group.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="deploymentGroupName")
    def deployment_group_name(self) -> str:
        """The physical name of the CodeDeploy Deployment Group.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...


class _IEcsDeploymentGroupProxy(jsii.proxy_for(_IResource_72f7ee7e)):
    """Interface for an ECS deployment group.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_codedeploy.IEcsDeploymentGroup"
    @builtins.property
    @jsii.member(jsii_name="application")
    def application(self) -> "IEcsApplication":
        """The reference to the CodeDeploy ECS Application that this Deployment Group belongs to.

        stability
        :stability: experimental
        """
        return jsii.get(self, "application")

    @builtins.property
    @jsii.member(jsii_name="deploymentConfig")
    def deployment_config(self) -> "IEcsDeploymentConfig":
        """The Deployment Configuration this Group uses.

        stability
        :stability: experimental
        """
        return jsii.get(self, "deploymentConfig")

    @builtins.property
    @jsii.member(jsii_name="deploymentGroupArn")
    def deployment_group_arn(self) -> str:
        """The ARN of this Deployment Group.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "deploymentGroupArn")

    @builtins.property
    @jsii.member(jsii_name="deploymentGroupName")
    def deployment_group_name(self) -> str:
        """The physical name of the CodeDeploy Deployment Group.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "deploymentGroupName")


@jsii.interface(jsii_type="monocdk-experiment.aws_codedeploy.ILambdaApplication")
class ILambdaApplication(_IResource_72f7ee7e, jsii.compat.Protocol):
    """Represents a reference to a CodeDeploy Application deploying to AWS Lambda.

    If you're managing the Application alongside the rest of your CDK resources,
    use the {@link LambdaApplication} class.

    If you want to reference an already existing Application,
    or one defined in a different CDK Stack,
    use the {@link LambdaApplication#fromLambdaApplicationName} method.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ILambdaApplicationProxy

    @builtins.property
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> str:
        """
        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> str:
        """
        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...


class _ILambdaApplicationProxy(jsii.proxy_for(_IResource_72f7ee7e)):
    """Represents a reference to a CodeDeploy Application deploying to AWS Lambda.

    If you're managing the Application alongside the rest of your CDK resources,
    use the {@link LambdaApplication} class.

    If you want to reference an already existing Application,
    or one defined in a different CDK Stack,
    use the {@link LambdaApplication#fromLambdaApplicationName} method.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_codedeploy.ILambdaApplication"
    @builtins.property
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> str:
        """
        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "applicationArn")

    @builtins.property
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> str:
        """
        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "applicationName")


@jsii.interface(jsii_type="monocdk-experiment.aws_codedeploy.ILambdaDeploymentConfig")
class ILambdaDeploymentConfig(jsii.compat.Protocol):
    """The Deployment Configuration of a Lambda Deployment Group.

    The default, pre-defined Configurations are available as constants on the {@link LambdaDeploymentConfig} class
    (``LambdaDeploymentConfig.AllAtOnce``, ``LambdaDeploymentConfig.Canary10Percent30Minutes``, etc.).

    Note: CloudFormation does not currently support creating custom lambda configs outside
    of using a custom resource. You can import custom deployment config created outside the
    CDK or via a custom resource with {@link LambdaDeploymentConfig#import}.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ILambdaDeploymentConfigProxy

    @builtins.property
    @jsii.member(jsii_name="deploymentConfigArn")
    def deployment_config_arn(self) -> str:
        """
        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="deploymentConfigName")
    def deployment_config_name(self) -> str:
        """
        stability
        :stability: experimental
        """
        ...


class _ILambdaDeploymentConfigProxy():
    """The Deployment Configuration of a Lambda Deployment Group.

    The default, pre-defined Configurations are available as constants on the {@link LambdaDeploymentConfig} class
    (``LambdaDeploymentConfig.AllAtOnce``, ``LambdaDeploymentConfig.Canary10Percent30Minutes``, etc.).

    Note: CloudFormation does not currently support creating custom lambda configs outside
    of using a custom resource. You can import custom deployment config created outside the
    CDK or via a custom resource with {@link LambdaDeploymentConfig#import}.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_codedeploy.ILambdaDeploymentConfig"
    @builtins.property
    @jsii.member(jsii_name="deploymentConfigArn")
    def deployment_config_arn(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "deploymentConfigArn")

    @builtins.property
    @jsii.member(jsii_name="deploymentConfigName")
    def deployment_config_name(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "deploymentConfigName")


@jsii.interface(jsii_type="monocdk-experiment.aws_codedeploy.ILambdaDeploymentGroup")
class ILambdaDeploymentGroup(_IResource_72f7ee7e, jsii.compat.Protocol):
    """Interface for a Lambda deployment groups.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ILambdaDeploymentGroupProxy

    @builtins.property
    @jsii.member(jsii_name="application")
    def application(self) -> "ILambdaApplication":
        """The reference to the CodeDeploy Lambda Application that this Deployment Group belongs to.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="deploymentConfig")
    def deployment_config(self) -> "ILambdaDeploymentConfig":
        """The Deployment Configuration this Group uses.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="deploymentGroupArn")
    def deployment_group_arn(self) -> str:
        """The ARN of this Deployment Group.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="deploymentGroupName")
    def deployment_group_name(self) -> str:
        """The physical name of the CodeDeploy Deployment Group.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...


class _ILambdaDeploymentGroupProxy(jsii.proxy_for(_IResource_72f7ee7e)):
    """Interface for a Lambda deployment groups.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_codedeploy.ILambdaDeploymentGroup"
    @builtins.property
    @jsii.member(jsii_name="application")
    def application(self) -> "ILambdaApplication":
        """The reference to the CodeDeploy Lambda Application that this Deployment Group belongs to.

        stability
        :stability: experimental
        """
        return jsii.get(self, "application")

    @builtins.property
    @jsii.member(jsii_name="deploymentConfig")
    def deployment_config(self) -> "ILambdaDeploymentConfig":
        """The Deployment Configuration this Group uses.

        stability
        :stability: experimental
        """
        return jsii.get(self, "deploymentConfig")

    @builtins.property
    @jsii.member(jsii_name="deploymentGroupArn")
    def deployment_group_arn(self) -> str:
        """The ARN of this Deployment Group.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "deploymentGroupArn")

    @builtins.property
    @jsii.member(jsii_name="deploymentGroupName")
    def deployment_group_name(self) -> str:
        """The physical name of the CodeDeploy Deployment Group.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "deploymentGroupName")


@jsii.interface(jsii_type="monocdk-experiment.aws_codedeploy.IServerApplication")
class IServerApplication(_IResource_72f7ee7e, jsii.compat.Protocol):
    """Represents a reference to a CodeDeploy Application deploying to EC2/on-premise instances.

    If you're managing the Application alongside the rest of your CDK resources,
    use the {@link ServerApplication} class.

    If you want to reference an already existing Application,
    or one defined in a different CDK Stack,
    use the {@link #fromServerApplicationName} method.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IServerApplicationProxy

    @builtins.property
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> str:
        """
        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> str:
        """
        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...


class _IServerApplicationProxy(jsii.proxy_for(_IResource_72f7ee7e)):
    """Represents a reference to a CodeDeploy Application deploying to EC2/on-premise instances.

    If you're managing the Application alongside the rest of your CDK resources,
    use the {@link ServerApplication} class.

    If you want to reference an already existing Application,
    or one defined in a different CDK Stack,
    use the {@link #fromServerApplicationName} method.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_codedeploy.IServerApplication"
    @builtins.property
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> str:
        """
        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "applicationArn")

    @builtins.property
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> str:
        """
        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "applicationName")


@jsii.interface(jsii_type="monocdk-experiment.aws_codedeploy.IServerDeploymentConfig")
class IServerDeploymentConfig(jsii.compat.Protocol):
    """The Deployment Configuration of an EC2/on-premise Deployment Group.

    The default, pre-defined Configurations are available as constants on the {@link ServerDeploymentConfig} class
    (``ServerDeploymentConfig.HalfAtATime``, ``ServerDeploymentConfig.AllAtOnce``, etc.).
    To create a custom Deployment Configuration,
    instantiate the {@link ServerDeploymentConfig} Construct.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IServerDeploymentConfigProxy

    @builtins.property
    @jsii.member(jsii_name="deploymentConfigArn")
    def deployment_config_arn(self) -> str:
        """
        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="deploymentConfigName")
    def deployment_config_name(self) -> str:
        """
        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...


class _IServerDeploymentConfigProxy():
    """The Deployment Configuration of an EC2/on-premise Deployment Group.

    The default, pre-defined Configurations are available as constants on the {@link ServerDeploymentConfig} class
    (``ServerDeploymentConfig.HalfAtATime``, ``ServerDeploymentConfig.AllAtOnce``, etc.).
    To create a custom Deployment Configuration,
    instantiate the {@link ServerDeploymentConfig} Construct.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_codedeploy.IServerDeploymentConfig"
    @builtins.property
    @jsii.member(jsii_name="deploymentConfigArn")
    def deployment_config_arn(self) -> str:
        """
        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "deploymentConfigArn")

    @builtins.property
    @jsii.member(jsii_name="deploymentConfigName")
    def deployment_config_name(self) -> str:
        """
        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "deploymentConfigName")


@jsii.interface(jsii_type="monocdk-experiment.aws_codedeploy.IServerDeploymentGroup")
class IServerDeploymentGroup(_IResource_72f7ee7e, jsii.compat.Protocol):
    """
    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IServerDeploymentGroupProxy

    @builtins.property
    @jsii.member(jsii_name="application")
    def application(self) -> "IServerApplication":
        """
        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="deploymentConfig")
    def deployment_config(self) -> "IServerDeploymentConfig":
        """
        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="deploymentGroupArn")
    def deployment_group_arn(self) -> str:
        """
        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="deploymentGroupName")
    def deployment_group_name(self) -> str:
        """
        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="autoScalingGroups")
    def auto_scaling_groups(self) -> typing.Optional[typing.List[_AutoScalingGroup_003d0b84]]:
        """
        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """
        stability
        :stability: experimental
        """
        ...


class _IServerDeploymentGroupProxy(jsii.proxy_for(_IResource_72f7ee7e)):
    """
    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_codedeploy.IServerDeploymentGroup"
    @builtins.property
    @jsii.member(jsii_name="application")
    def application(self) -> "IServerApplication":
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "application")

    @builtins.property
    @jsii.member(jsii_name="deploymentConfig")
    def deployment_config(self) -> "IServerDeploymentConfig":
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "deploymentConfig")

    @builtins.property
    @jsii.member(jsii_name="deploymentGroupArn")
    def deployment_group_arn(self) -> str:
        """
        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "deploymentGroupArn")

    @builtins.property
    @jsii.member(jsii_name="deploymentGroupName")
    def deployment_group_name(self) -> str:
        """
        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "deploymentGroupName")

    @builtins.property
    @jsii.member(jsii_name="autoScalingGroups")
    def auto_scaling_groups(self) -> typing.Optional[typing.List[_AutoScalingGroup_003d0b84]]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "autoScalingGroups")

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "role")


class InstanceTagSet(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_codedeploy.InstanceTagSet"):
    """Represents a set of instance tag groups.

    An instance will match a set if it matches all of the groups in the set -
    in other words, sets follow 'and' semantics.
    You can have a maximum of 3 tag groups inside a set.

    stability
    :stability: experimental
    """
    def __init__(self, *instance_tag_groups: typing.Mapping[str, typing.List[str]]) -> None:
        """
        :param instance_tag_groups: -

        stability
        :stability: experimental
        """
        jsii.create(InstanceTagSet, self, [*instance_tag_groups])

    @builtins.property
    @jsii.member(jsii_name="instanceTagGroups")
    def instance_tag_groups(self) -> typing.List[typing.Mapping[str, typing.List[str]]]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "instanceTagGroups")


@jsii.implements(ILambdaApplication)
class LambdaApplication(_Resource_884d0774, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_codedeploy.LambdaApplication"):
    """A CodeDeploy Application that deploys to an AWS Lambda function.

    stability
    :stability: experimental
    resource:
    :resource:: AWS::CodeDeploy::Application
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, application_name: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param application_name: The physical, human-readable name of the CodeDeploy Application. Default: an auto-generated name will be used

        stability
        :stability: experimental
        """
        props = LambdaApplicationProps(application_name=application_name)

        jsii.create(LambdaApplication, self, [scope, id, props])

    @jsii.member(jsii_name="fromLambdaApplicationName")
    @builtins.classmethod
    def from_lambda_application_name(cls, scope: _Construct_f50a3f53, id: str, lambda_application_name: str) -> "ILambdaApplication":
        """Import an Application defined either outside the CDK, or in a different CDK Stack.

        :param scope: the parent Construct for this new Construct.
        :param id: the logical ID of this new Construct.
        :param lambda_application_name: the name of the application to import.

        return
        :return: a Construct representing a reference to an existing Application

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromLambdaApplicationName", [scope, id, lambda_application_name])

    @builtins.property
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "applicationArn")

    @builtins.property
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "applicationName")


@jsii.data_type(jsii_type="monocdk-experiment.aws_codedeploy.LambdaApplicationProps", jsii_struct_bases=[], name_mapping={'application_name': 'applicationName'})
class LambdaApplicationProps():
    def __init__(self, *, application_name: typing.Optional[str]=None) -> None:
        """Construction properties for {@link LambdaApplication}.

        :param application_name: The physical, human-readable name of the CodeDeploy Application. Default: an auto-generated name will be used

        stability
        :stability: experimental
        """
        self._values = {
        }
        if application_name is not None: self._values["application_name"] = application_name

    @builtins.property
    def application_name(self) -> typing.Optional[str]:
        """The physical, human-readable name of the CodeDeploy Application.

        default
        :default: an auto-generated name will be used

        stability
        :stability: experimental
        """
        return self._values.get('application_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LambdaApplicationProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class LambdaDeploymentConfig(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_codedeploy.LambdaDeploymentConfig"):
    """A custom Deployment Configuration for a Lambda Deployment Group.

    Note: This class currently stands as namespaced container of the default configurations
    until CloudFormation supports custom Lambda Deployment Configs. Until then it is closed
    (private constructor) and does not extend {@link cdk.Construct}

    stability
    :stability: experimental
    resource:
    :resource:: AWS::CodeDeploy::DeploymentConfig
    """
    @jsii.member(jsii_name="import")
    @builtins.classmethod
    def import_(cls, _scope: _Construct_f50a3f53, _id: str, *, deployment_config_name: str) -> "ILambdaDeploymentConfig":
        """Import a custom Deployment Configuration for a Lambda Deployment Group defined outside the CDK.

        :param _scope: the parent Construct for this new Construct.
        :param _id: the logical ID of this new Construct.
        :param deployment_config_name: The physical, human-readable name of the custom CodeDeploy Lambda Deployment Configuration that we are referencing.

        return
        :return: a Construct representing a reference to an existing custom Deployment Configuration

        stability
        :stability: experimental
        """
        props = LambdaDeploymentConfigImportProps(deployment_config_name=deployment_config_name)

        return jsii.sinvoke(cls, "import", [_scope, _id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="ALL_AT_ONCE")
    def ALL_AT_ONCE(cls) -> "ILambdaDeploymentConfig":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "ALL_AT_ONCE")

    @jsii.python.classproperty
    @jsii.member(jsii_name="CANARY_10PERCENT_10MINUTES")
    def CANARY_10_PERCENT_10_MINUTES(cls) -> "ILambdaDeploymentConfig":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "CANARY_10PERCENT_10MINUTES")

    @jsii.python.classproperty
    @jsii.member(jsii_name="CANARY_10PERCENT_15MINUTES")
    def CANARY_10_PERCENT_15_MINUTES(cls) -> "ILambdaDeploymentConfig":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "CANARY_10PERCENT_15MINUTES")

    @jsii.python.classproperty
    @jsii.member(jsii_name="CANARY_10PERCENT_30MINUTES")
    def CANARY_10_PERCENT_30_MINUTES(cls) -> "ILambdaDeploymentConfig":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "CANARY_10PERCENT_30MINUTES")

    @jsii.python.classproperty
    @jsii.member(jsii_name="CANARY_10PERCENT_5MINUTES")
    def CANARY_10_PERCENT_5_MINUTES(cls) -> "ILambdaDeploymentConfig":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "CANARY_10PERCENT_5MINUTES")

    @jsii.python.classproperty
    @jsii.member(jsii_name="LINEAR_10PERCENT_EVERY_10MINUTES")
    def LINEAR_10_PERCENT_EVERY_10_MINUTES(cls) -> "ILambdaDeploymentConfig":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "LINEAR_10PERCENT_EVERY_10MINUTES")

    @jsii.python.classproperty
    @jsii.member(jsii_name="LINEAR_10PERCENT_EVERY_1MINUTE")
    def LINEAR_10_PERCENT_EVERY_1_MINUTE(cls) -> "ILambdaDeploymentConfig":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "LINEAR_10PERCENT_EVERY_1MINUTE")

    @jsii.python.classproperty
    @jsii.member(jsii_name="LINEAR_10PERCENT_EVERY_2MINUTES")
    def LINEAR_10_PERCENT_EVERY_2_MINUTES(cls) -> "ILambdaDeploymentConfig":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "LINEAR_10PERCENT_EVERY_2MINUTES")

    @jsii.python.classproperty
    @jsii.member(jsii_name="LINEAR_10PERCENT_EVERY_3MINUTES")
    def LINEAR_10_PERCENT_EVERY_3_MINUTES(cls) -> "ILambdaDeploymentConfig":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "LINEAR_10PERCENT_EVERY_3MINUTES")


@jsii.data_type(jsii_type="monocdk-experiment.aws_codedeploy.LambdaDeploymentConfigImportProps", jsii_struct_bases=[], name_mapping={'deployment_config_name': 'deploymentConfigName'})
class LambdaDeploymentConfigImportProps():
    def __init__(self, *, deployment_config_name: str) -> None:
        """Properties of a reference to a CodeDeploy Lambda Deployment Configuration.

        :param deployment_config_name: The physical, human-readable name of the custom CodeDeploy Lambda Deployment Configuration that we are referencing.

        see
        :see: LambdaDeploymentConfig#import
        stability
        :stability: experimental
        """
        self._values = {
            'deployment_config_name': deployment_config_name,
        }

    @builtins.property
    def deployment_config_name(self) -> str:
        """The physical, human-readable name of the custom CodeDeploy Lambda Deployment Configuration that we are referencing.

        stability
        :stability: experimental
        """
        return self._values.get('deployment_config_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LambdaDeploymentConfigImportProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(ILambdaDeploymentGroup)
class LambdaDeploymentGroup(_Resource_884d0774, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_codedeploy.LambdaDeploymentGroup"):
    """
    stability
    :stability: experimental
    resource:
    :resource:: AWS::CodeDeploy::DeploymentGroup
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, alias: _Alias_67f7db75, alarms: typing.Optional[typing.List[_IAlarm_478ec33c]]=None, application: typing.Optional["ILambdaApplication"]=None, auto_rollback: typing.Optional["AutoRollbackConfig"]=None, deployment_config: typing.Optional["ILambdaDeploymentConfig"]=None, deployment_group_name: typing.Optional[str]=None, ignore_poll_alarms_failure: typing.Optional[bool]=None, post_hook: typing.Optional[_IFunction_1c1de0bc]=None, pre_hook: typing.Optional[_IFunction_1c1de0bc]=None, role: typing.Optional[_IRole_e69bbae4]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param alias: Lambda Alias to shift traffic. Updating the version of the alias will trigger a CodeDeploy deployment. [disable-awslint:ref-via-interface] since we need to modify the alias CFN resource update policy
        :param alarms: The CloudWatch alarms associated with this Deployment Group. CodeDeploy will stop (and optionally roll back) a deployment if during it any of the alarms trigger. Alarms can also be added after the Deployment Group is created using the {@link #addAlarm} method. Default: []
        :param application: The reference to the CodeDeploy Lambda Application that this Deployment Group belongs to. Default: - One will be created for you.
        :param auto_rollback: The auto-rollback configuration for this Deployment Group. Default: - default AutoRollbackConfig.
        :param deployment_config: The Deployment Configuration this Deployment Group uses. Default: LambdaDeploymentConfig.CANARY_10PERCENT_5MINUTES
        :param deployment_group_name: The physical, human-readable name of the CodeDeploy Deployment Group. Default: - An auto-generated name will be used.
        :param ignore_poll_alarms_failure: Whether to continue a deployment even if fetching the alarm status from CloudWatch failed. Default: false
        :param post_hook: The Lambda function to run after traffic routing starts. Default: - None.
        :param pre_hook: The Lambda function to run before traffic routing starts. Default: - None.
        :param role: The service Role of this Deployment Group. Default: - A new Role will be created.

        stability
        :stability: experimental
        """
        props = LambdaDeploymentGroupProps(alias=alias, alarms=alarms, application=application, auto_rollback=auto_rollback, deployment_config=deployment_config, deployment_group_name=deployment_group_name, ignore_poll_alarms_failure=ignore_poll_alarms_failure, post_hook=post_hook, pre_hook=pre_hook, role=role)

        jsii.create(LambdaDeploymentGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromLambdaDeploymentGroupAttributes")
    @builtins.classmethod
    def from_lambda_deployment_group_attributes(cls, scope: _Construct_f50a3f53, id: str, *, application: "ILambdaApplication", deployment_group_name: str, deployment_config: typing.Optional["ILambdaDeploymentConfig"]=None) -> "ILambdaDeploymentGroup":
        """Import an Lambda Deployment Group defined either outside the CDK app, or in a different AWS region.

        :param scope: the parent Construct for this new Construct.
        :param id: the logical ID of this new Construct.
        :param application: The reference to the CodeDeploy Lambda Application that this Deployment Group belongs to.
        :param deployment_group_name: The physical, human-readable name of the CodeDeploy Lambda Deployment Group that we are referencing.
        :param deployment_config: The Deployment Configuration this Deployment Group uses. Default: LambdaDeploymentConfig.CANARY_10PERCENT_5MINUTES

        return
        :return: a Construct representing a reference to an existing Deployment Group

        stability
        :stability: experimental
        """
        attrs = LambdaDeploymentGroupAttributes(application=application, deployment_group_name=deployment_group_name, deployment_config=deployment_config)

        return jsii.sinvoke(cls, "fromLambdaDeploymentGroupAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="addAlarm")
    def add_alarm(self, alarm: _IAlarm_478ec33c) -> None:
        """Associates an additional alarm with this Deployment Group.

        :param alarm: the alarm to associate with this Deployment Group.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addAlarm", [alarm])

    @jsii.member(jsii_name="addPostHook")
    def add_post_hook(self, post_hook: _IFunction_1c1de0bc) -> None:
        """Associate a function to run after deployment completes.

        :param post_hook: function to run after deployment completes.

        stability
        :stability: experimental
        throws:
        :throws:: an error if a post-hook function is already configured
        """
        return jsii.invoke(self, "addPostHook", [post_hook])

    @jsii.member(jsii_name="addPreHook")
    def add_pre_hook(self, pre_hook: _IFunction_1c1de0bc) -> None:
        """Associate a function to run before deployment begins.

        :param pre_hook: function to run before deployment beings.

        stability
        :stability: experimental
        throws:
        :throws:: an error if a pre-hook function is already configured
        """
        return jsii.invoke(self, "addPreHook", [pre_hook])

    @jsii.member(jsii_name="grantPutLifecycleEventHookExecutionStatus")
    def grant_put_lifecycle_event_hook_execution_status(self, grantee: _IGrantable_0fcfc53a) -> _Grant_96af6d2d:
        """Grant a principal permission to codedeploy:PutLifecycleEventHookExecutionStatus on this deployment group resource.

        :param grantee: to grant permission to.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "grantPutLifecycleEventHookExecutionStatus", [grantee])

    @builtins.property
    @jsii.member(jsii_name="application")
    def application(self) -> "ILambdaApplication":
        """The reference to the CodeDeploy Lambda Application that this Deployment Group belongs to.

        stability
        :stability: experimental
        """
        return jsii.get(self, "application")

    @builtins.property
    @jsii.member(jsii_name="deploymentConfig")
    def deployment_config(self) -> "ILambdaDeploymentConfig":
        """The Deployment Configuration this Group uses.

        stability
        :stability: experimental
        """
        return jsii.get(self, "deploymentConfig")

    @builtins.property
    @jsii.member(jsii_name="deploymentGroupArn")
    def deployment_group_arn(self) -> str:
        """The ARN of this Deployment Group.

        stability
        :stability: experimental
        """
        return jsii.get(self, "deploymentGroupArn")

    @builtins.property
    @jsii.member(jsii_name="deploymentGroupName")
    def deployment_group_name(self) -> str:
        """The physical name of the CodeDeploy Deployment Group.

        stability
        :stability: experimental
        """
        return jsii.get(self, "deploymentGroupName")

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> _IRole_e69bbae4:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "role")


@jsii.data_type(jsii_type="monocdk-experiment.aws_codedeploy.LambdaDeploymentGroupAttributes", jsii_struct_bases=[], name_mapping={'application': 'application', 'deployment_group_name': 'deploymentGroupName', 'deployment_config': 'deploymentConfig'})
class LambdaDeploymentGroupAttributes():
    def __init__(self, *, application: "ILambdaApplication", deployment_group_name: str, deployment_config: typing.Optional["ILambdaDeploymentConfig"]=None) -> None:
        """Properties of a reference to a CodeDeploy Lambda Deployment Group.

        :param application: The reference to the CodeDeploy Lambda Application that this Deployment Group belongs to.
        :param deployment_group_name: The physical, human-readable name of the CodeDeploy Lambda Deployment Group that we are referencing.
        :param deployment_config: The Deployment Configuration this Deployment Group uses. Default: LambdaDeploymentConfig.CANARY_10PERCENT_5MINUTES

        see
        :see: LambdaDeploymentGroup#fromLambdaDeploymentGroupAttributes
        stability
        :stability: experimental
        """
        self._values = {
            'application': application,
            'deployment_group_name': deployment_group_name,
        }
        if deployment_config is not None: self._values["deployment_config"] = deployment_config

    @builtins.property
    def application(self) -> "ILambdaApplication":
        """The reference to the CodeDeploy Lambda Application that this Deployment Group belongs to.

        stability
        :stability: experimental
        """
        return self._values.get('application')

    @builtins.property
    def deployment_group_name(self) -> str:
        """The physical, human-readable name of the CodeDeploy Lambda Deployment Group that we are referencing.

        stability
        :stability: experimental
        """
        return self._values.get('deployment_group_name')

    @builtins.property
    def deployment_config(self) -> typing.Optional["ILambdaDeploymentConfig"]:
        """The Deployment Configuration this Deployment Group uses.

        default
        :default: LambdaDeploymentConfig.CANARY_10PERCENT_5MINUTES

        stability
        :stability: experimental
        """
        return self._values.get('deployment_config')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LambdaDeploymentGroupAttributes(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_codedeploy.LambdaDeploymentGroupProps", jsii_struct_bases=[], name_mapping={'alias': 'alias', 'alarms': 'alarms', 'application': 'application', 'auto_rollback': 'autoRollback', 'deployment_config': 'deploymentConfig', 'deployment_group_name': 'deploymentGroupName', 'ignore_poll_alarms_failure': 'ignorePollAlarmsFailure', 'post_hook': 'postHook', 'pre_hook': 'preHook', 'role': 'role'})
class LambdaDeploymentGroupProps():
    def __init__(self, *, alias: _Alias_67f7db75, alarms: typing.Optional[typing.List[_IAlarm_478ec33c]]=None, application: typing.Optional["ILambdaApplication"]=None, auto_rollback: typing.Optional["AutoRollbackConfig"]=None, deployment_config: typing.Optional["ILambdaDeploymentConfig"]=None, deployment_group_name: typing.Optional[str]=None, ignore_poll_alarms_failure: typing.Optional[bool]=None, post_hook: typing.Optional[_IFunction_1c1de0bc]=None, pre_hook: typing.Optional[_IFunction_1c1de0bc]=None, role: typing.Optional[_IRole_e69bbae4]=None) -> None:
        """Construction properties for {@link LambdaDeploymentGroup}.

        :param alias: Lambda Alias to shift traffic. Updating the version of the alias will trigger a CodeDeploy deployment. [disable-awslint:ref-via-interface] since we need to modify the alias CFN resource update policy
        :param alarms: The CloudWatch alarms associated with this Deployment Group. CodeDeploy will stop (and optionally roll back) a deployment if during it any of the alarms trigger. Alarms can also be added after the Deployment Group is created using the {@link #addAlarm} method. Default: []
        :param application: The reference to the CodeDeploy Lambda Application that this Deployment Group belongs to. Default: - One will be created for you.
        :param auto_rollback: The auto-rollback configuration for this Deployment Group. Default: - default AutoRollbackConfig.
        :param deployment_config: The Deployment Configuration this Deployment Group uses. Default: LambdaDeploymentConfig.CANARY_10PERCENT_5MINUTES
        :param deployment_group_name: The physical, human-readable name of the CodeDeploy Deployment Group. Default: - An auto-generated name will be used.
        :param ignore_poll_alarms_failure: Whether to continue a deployment even if fetching the alarm status from CloudWatch failed. Default: false
        :param post_hook: The Lambda function to run after traffic routing starts. Default: - None.
        :param pre_hook: The Lambda function to run before traffic routing starts. Default: - None.
        :param role: The service Role of this Deployment Group. Default: - A new Role will be created.

        stability
        :stability: experimental
        """
        if isinstance(auto_rollback, dict): auto_rollback = AutoRollbackConfig(**auto_rollback)
        self._values = {
            'alias': alias,
        }
        if alarms is not None: self._values["alarms"] = alarms
        if application is not None: self._values["application"] = application
        if auto_rollback is not None: self._values["auto_rollback"] = auto_rollback
        if deployment_config is not None: self._values["deployment_config"] = deployment_config
        if deployment_group_name is not None: self._values["deployment_group_name"] = deployment_group_name
        if ignore_poll_alarms_failure is not None: self._values["ignore_poll_alarms_failure"] = ignore_poll_alarms_failure
        if post_hook is not None: self._values["post_hook"] = post_hook
        if pre_hook is not None: self._values["pre_hook"] = pre_hook
        if role is not None: self._values["role"] = role

    @builtins.property
    def alias(self) -> _Alias_67f7db75:
        """Lambda Alias to shift traffic. Updating the version of the alias will trigger a CodeDeploy deployment.

        [disable-awslint:ref-via-interface] since we need to modify the alias CFN resource update policy

        stability
        :stability: experimental
        """
        return self._values.get('alias')

    @builtins.property
    def alarms(self) -> typing.Optional[typing.List[_IAlarm_478ec33c]]:
        """The CloudWatch alarms associated with this Deployment Group.

        CodeDeploy will stop (and optionally roll back)
        a deployment if during it any of the alarms trigger.

        Alarms can also be added after the Deployment Group is created using the {@link #addAlarm} method.

        default
        :default: []

        see
        :see: https://docs.aws.amazon.com/codedeploy/latest/userguide/monitoring-create-alarms.html
        stability
        :stability: experimental
        """
        return self._values.get('alarms')

    @builtins.property
    def application(self) -> typing.Optional["ILambdaApplication"]:
        """The reference to the CodeDeploy Lambda Application that this Deployment Group belongs to.

        default
        :default: - One will be created for you.

        stability
        :stability: experimental
        """
        return self._values.get('application')

    @builtins.property
    def auto_rollback(self) -> typing.Optional["AutoRollbackConfig"]:
        """The auto-rollback configuration for this Deployment Group.

        default
        :default: - default AutoRollbackConfig.

        stability
        :stability: experimental
        """
        return self._values.get('auto_rollback')

    @builtins.property
    def deployment_config(self) -> typing.Optional["ILambdaDeploymentConfig"]:
        """The Deployment Configuration this Deployment Group uses.

        default
        :default: LambdaDeploymentConfig.CANARY_10PERCENT_5MINUTES

        stability
        :stability: experimental
        """
        return self._values.get('deployment_config')

    @builtins.property
    def deployment_group_name(self) -> typing.Optional[str]:
        """The physical, human-readable name of the CodeDeploy Deployment Group.

        default
        :default: - An auto-generated name will be used.

        stability
        :stability: experimental
        """
        return self._values.get('deployment_group_name')

    @builtins.property
    def ignore_poll_alarms_failure(self) -> typing.Optional[bool]:
        """Whether to continue a deployment even if fetching the alarm status from CloudWatch failed.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('ignore_poll_alarms_failure')

    @builtins.property
    def post_hook(self) -> typing.Optional[_IFunction_1c1de0bc]:
        """The Lambda function to run after traffic routing starts.

        default
        :default: - None.

        stability
        :stability: experimental
        """
        return self._values.get('post_hook')

    @builtins.property
    def pre_hook(self) -> typing.Optional[_IFunction_1c1de0bc]:
        """The Lambda function to run before traffic routing starts.

        default
        :default: - None.

        stability
        :stability: experimental
        """
        return self._values.get('pre_hook')

    @builtins.property
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The service Role of this Deployment Group.

        default
        :default: - A new Role will be created.

        stability
        :stability: experimental
        """
        return self._values.get('role')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LambdaDeploymentGroupProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class LoadBalancer(metaclass=jsii.JSIIAbstractClass, jsii_type="monocdk-experiment.aws_codedeploy.LoadBalancer"):
    """An interface of an abstract load balancer, as needed by CodeDeploy.

    Create instances using the static factory methods:
    {@link #classic}, {@link #application} and {@link #network}.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _LoadBalancerProxy

    def __init__(self) -> None:
        jsii.create(LoadBalancer, self, [])

    @jsii.member(jsii_name="application")
    @builtins.classmethod
    def application(cls, alb_target_group: _ApplicationTargetGroup_7d0a8d54) -> "LoadBalancer":
        """Creates a new CodeDeploy load balancer from an Application Load Balancer Target Group.

        :param alb_target_group: an ALB Target Group.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "application", [alb_target_group])

    @jsii.member(jsii_name="classic")
    @builtins.classmethod
    def classic(cls, load_balancer: _LoadBalancer_6d00b4b8) -> "LoadBalancer":
        """Creates a new CodeDeploy load balancer from a Classic ELB Load Balancer.

        :param load_balancer: a classic ELB Load Balancer.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "classic", [load_balancer])

    @jsii.member(jsii_name="network")
    @builtins.classmethod
    def network(cls, nlb_target_group: _NetworkTargetGroup_4f773ed3) -> "LoadBalancer":
        """Creates a new CodeDeploy load balancer from a Network Load Balancer Target Group.

        :param nlb_target_group: an NLB Target Group.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "network", [nlb_target_group])

    @builtins.property
    @jsii.member(jsii_name="generation")
    @abc.abstractmethod
    def generation(self) -> "LoadBalancerGeneration":
        """
        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="name")
    @abc.abstractmethod
    def name(self) -> str:
        """
        stability
        :stability: experimental
        """
        ...


class _LoadBalancerProxy(LoadBalancer):
    @builtins.property
    @jsii.member(jsii_name="generation")
    def generation(self) -> "LoadBalancerGeneration":
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "generation")

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "name")


@jsii.enum(jsii_type="monocdk-experiment.aws_codedeploy.LoadBalancerGeneration")
class LoadBalancerGeneration(enum.Enum):
    """The generations of AWS load balancing solutions.

    stability
    :stability: experimental
    """
    FIRST = "FIRST"
    """The first generation (ELB Classic).

    stability
    :stability: experimental
    """
    SECOND = "SECOND"
    """The second generation (ALB and NLB).

    stability
    :stability: experimental
    """

class MinimumHealthyHosts(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_codedeploy.MinimumHealthyHosts"):
    """Minimum number of healthy hosts for a server deployment.

    stability
    :stability: experimental
    """
    @jsii.member(jsii_name="count")
    @builtins.classmethod
    def count(cls, value: jsii.Number) -> "MinimumHealthyHosts":
        """The minimum healhty hosts threshold expressed as an absolute number.

        :param value: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "count", [value])

    @jsii.member(jsii_name="percentage")
    @builtins.classmethod
    def percentage(cls, value: jsii.Number) -> "MinimumHealthyHosts":
        """The minmum healhty hosts threshold expressed as a percentage of the fleet.

        :param value: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "percentage", [value])


@jsii.implements(IServerApplication)
class ServerApplication(_Resource_884d0774, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_codedeploy.ServerApplication"):
    """A CodeDeploy Application that deploys to EC2/on-premise instances.

    stability
    :stability: experimental
    resource:
    :resource:: AWS::CodeDeploy::Application
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, application_name: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param application_name: The physical, human-readable name of the CodeDeploy Application. Default: an auto-generated name will be used

        stability
        :stability: experimental
        """
        props = ServerApplicationProps(application_name=application_name)

        jsii.create(ServerApplication, self, [scope, id, props])

    @jsii.member(jsii_name="fromServerApplicationName")
    @builtins.classmethod
    def from_server_application_name(cls, scope: _Construct_f50a3f53, id: str, server_application_name: str) -> "IServerApplication":
        """Import an Application defined either outside the CDK app, or in a different region.

        :param scope: the parent Construct for this new Construct.
        :param id: the logical ID of this new Construct.
        :param server_application_name: the name of the application to import.

        return
        :return: a Construct representing a reference to an existing Application

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromServerApplicationName", [scope, id, server_application_name])

    @builtins.property
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "applicationArn")

    @builtins.property
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "applicationName")


@jsii.data_type(jsii_type="monocdk-experiment.aws_codedeploy.ServerApplicationProps", jsii_struct_bases=[], name_mapping={'application_name': 'applicationName'})
class ServerApplicationProps():
    def __init__(self, *, application_name: typing.Optional[str]=None) -> None:
        """Construction properties for {@link ServerApplication}.

        :param application_name: The physical, human-readable name of the CodeDeploy Application. Default: an auto-generated name will be used

        stability
        :stability: experimental
        """
        self._values = {
        }
        if application_name is not None: self._values["application_name"] = application_name

    @builtins.property
    def application_name(self) -> typing.Optional[str]:
        """The physical, human-readable name of the CodeDeploy Application.

        default
        :default: an auto-generated name will be used

        stability
        :stability: experimental
        """
        return self._values.get('application_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ServerApplicationProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(IServerDeploymentConfig)
class ServerDeploymentConfig(_Resource_884d0774, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_codedeploy.ServerDeploymentConfig"):
    """A custom Deployment Configuration for an EC2/on-premise Deployment Group.

    stability
    :stability: experimental
    resource:
    :resource:: AWS::CodeDeploy::DeploymentConfig
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, minimum_healthy_hosts: "MinimumHealthyHosts", deployment_config_name: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param minimum_healthy_hosts: Minimum number of healthy hosts.
        :param deployment_config_name: The physical, human-readable name of the Deployment Configuration. Default: a name will be auto-generated

        stability
        :stability: experimental
        """
        props = ServerDeploymentConfigProps(minimum_healthy_hosts=minimum_healthy_hosts, deployment_config_name=deployment_config_name)

        jsii.create(ServerDeploymentConfig, self, [scope, id, props])

    @jsii.member(jsii_name="fromServerDeploymentConfigName")
    @builtins.classmethod
    def from_server_deployment_config_name(cls, scope: _Construct_f50a3f53, id: str, server_deployment_config_name: str) -> "IServerDeploymentConfig":
        """Import a custom Deployment Configuration for an EC2/on-premise Deployment Group defined either outside the CDK app, or in a different region.

        :param scope: the parent Construct for this new Construct.
        :param id: the logical ID of this new Construct.
        :param server_deployment_config_name: the properties of the referenced custom Deployment Configuration.

        return
        :return: a Construct representing a reference to an existing custom Deployment Configuration

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromServerDeploymentConfigName", [scope, id, server_deployment_config_name])

    @jsii.python.classproperty
    @jsii.member(jsii_name="ALL_AT_ONCE")
    def ALL_AT_ONCE(cls) -> "IServerDeploymentConfig":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "ALL_AT_ONCE")

    @jsii.python.classproperty
    @jsii.member(jsii_name="HALF_AT_A_TIME")
    def HALF_AT_A_TIME(cls) -> "IServerDeploymentConfig":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "HALF_AT_A_TIME")

    @jsii.python.classproperty
    @jsii.member(jsii_name="ONE_AT_A_TIME")
    def ONE_AT_A_TIME(cls) -> "IServerDeploymentConfig":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "ONE_AT_A_TIME")

    @builtins.property
    @jsii.member(jsii_name="deploymentConfigArn")
    def deployment_config_arn(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "deploymentConfigArn")

    @builtins.property
    @jsii.member(jsii_name="deploymentConfigName")
    def deployment_config_name(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "deploymentConfigName")


@jsii.data_type(jsii_type="monocdk-experiment.aws_codedeploy.ServerDeploymentConfigProps", jsii_struct_bases=[], name_mapping={'minimum_healthy_hosts': 'minimumHealthyHosts', 'deployment_config_name': 'deploymentConfigName'})
class ServerDeploymentConfigProps():
    def __init__(self, *, minimum_healthy_hosts: "MinimumHealthyHosts", deployment_config_name: typing.Optional[str]=None) -> None:
        """Construction properties of {@link ServerDeploymentConfig}.

        :param minimum_healthy_hosts: Minimum number of healthy hosts.
        :param deployment_config_name: The physical, human-readable name of the Deployment Configuration. Default: a name will be auto-generated

        stability
        :stability: experimental
        """
        self._values = {
            'minimum_healthy_hosts': minimum_healthy_hosts,
        }
        if deployment_config_name is not None: self._values["deployment_config_name"] = deployment_config_name

    @builtins.property
    def minimum_healthy_hosts(self) -> "MinimumHealthyHosts":
        """Minimum number of healthy hosts.

        stability
        :stability: experimental
        """
        return self._values.get('minimum_healthy_hosts')

    @builtins.property
    def deployment_config_name(self) -> typing.Optional[str]:
        """The physical, human-readable name of the Deployment Configuration.

        default
        :default: a name will be auto-generated

        stability
        :stability: experimental
        """
        return self._values.get('deployment_config_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ServerDeploymentConfigProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(IServerDeploymentGroup)
class ServerDeploymentGroup(_Resource_884d0774, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_codedeploy.ServerDeploymentGroup"):
    """A CodeDeploy Deployment Group that deploys to EC2/on-premise instances.

    stability
    :stability: experimental
    resource:
    :resource:: AWS::CodeDeploy::DeploymentGroup
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, alarms: typing.Optional[typing.List[_IAlarm_478ec33c]]=None, application: typing.Optional["IServerApplication"]=None, auto_rollback: typing.Optional["AutoRollbackConfig"]=None, auto_scaling_groups: typing.Optional[typing.List[_AutoScalingGroup_003d0b84]]=None, deployment_config: typing.Optional["IServerDeploymentConfig"]=None, deployment_group_name: typing.Optional[str]=None, ec2_instance_tags: typing.Optional["InstanceTagSet"]=None, ignore_poll_alarms_failure: typing.Optional[bool]=None, install_agent: typing.Optional[bool]=None, load_balancer: typing.Optional["LoadBalancer"]=None, on_premise_instance_tags: typing.Optional["InstanceTagSet"]=None, role: typing.Optional[_IRole_e69bbae4]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param alarms: The CloudWatch alarms associated with this Deployment Group. CodeDeploy will stop (and optionally roll back) a deployment if during it any of the alarms trigger. Alarms can also be added after the Deployment Group is created using the {@link #addAlarm} method. Default: []
        :param application: The CodeDeploy EC2/on-premise Application this Deployment Group belongs to. Default: - A new Application will be created.
        :param auto_rollback: The auto-rollback configuration for this Deployment Group. Default: - default AutoRollbackConfig.
        :param auto_scaling_groups: The auto-scaling groups belonging to this Deployment Group. Auto-scaling groups can also be added after the Deployment Group is created using the {@link #addAutoScalingGroup} method. [disable-awslint:ref-via-interface] is needed because we update userdata for ASGs to install the codedeploy agent. Default: []
        :param deployment_config: The EC2/on-premise Deployment Configuration to use for this Deployment Group. Default: ServerDeploymentConfig#OneAtATime
        :param deployment_group_name: The physical, human-readable name of the CodeDeploy Deployment Group. Default: - An auto-generated name will be used.
        :param ec2_instance_tags: All EC2 instances matching the given set of tags when a deployment occurs will be added to this Deployment Group. Default: - No additional EC2 instances will be added to the Deployment Group.
        :param ignore_poll_alarms_failure: Whether to continue a deployment even if fetching the alarm status from CloudWatch failed. Default: false
        :param install_agent: If you've provided any auto-scaling groups with the {@link #autoScalingGroups} property, you can set this property to add User Data that installs the CodeDeploy agent on the instances. Default: true
        :param load_balancer: The load balancer to place in front of this Deployment Group. Can be created from either a classic Elastic Load Balancer, or an Application Load Balancer / Network Load Balancer Target Group. Default: - Deployment Group will not have a load balancer defined.
        :param on_premise_instance_tags: All on-premise instances matching the given set of tags when a deployment occurs will be added to this Deployment Group. Default: - No additional on-premise instances will be added to the Deployment Group.
        :param role: The service Role of this Deployment Group. Default: - A new Role will be created.

        stability
        :stability: experimental
        """
        props = ServerDeploymentGroupProps(alarms=alarms, application=application, auto_rollback=auto_rollback, auto_scaling_groups=auto_scaling_groups, deployment_config=deployment_config, deployment_group_name=deployment_group_name, ec2_instance_tags=ec2_instance_tags, ignore_poll_alarms_failure=ignore_poll_alarms_failure, install_agent=install_agent, load_balancer=load_balancer, on_premise_instance_tags=on_premise_instance_tags, role=role)

        jsii.create(ServerDeploymentGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromServerDeploymentGroupAttributes")
    @builtins.classmethod
    def from_server_deployment_group_attributes(cls, scope: _Construct_f50a3f53, id: str, *, application: "IServerApplication", deployment_group_name: str, deployment_config: typing.Optional["IServerDeploymentConfig"]=None) -> "IServerDeploymentGroup":
        """Import an EC2/on-premise Deployment Group defined either outside the CDK app, or in a different region.

        :param scope: the parent Construct for this new Construct.
        :param id: the logical ID of this new Construct.
        :param application: The reference to the CodeDeploy EC2/on-premise Application that this Deployment Group belongs to.
        :param deployment_group_name: The physical, human-readable name of the CodeDeploy EC2/on-premise Deployment Group that we are referencing.
        :param deployment_config: The Deployment Configuration this Deployment Group uses. Default: ServerDeploymentConfig#OneAtATime

        return
        :return: a Construct representing a reference to an existing Deployment Group

        stability
        :stability: experimental
        """
        attrs = ServerDeploymentGroupAttributes(application=application, deployment_group_name=deployment_group_name, deployment_config=deployment_config)

        return jsii.sinvoke(cls, "fromServerDeploymentGroupAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="addAlarm")
    def add_alarm(self, alarm: _IAlarm_478ec33c) -> None:
        """Associates an additional alarm with this Deployment Group.

        :param alarm: the alarm to associate with this Deployment Group.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addAlarm", [alarm])

    @jsii.member(jsii_name="addAutoScalingGroup")
    def add_auto_scaling_group(self, asg: _AutoScalingGroup_003d0b84) -> None:
        """Adds an additional auto-scaling group to this Deployment Group.

        :param asg: the auto-scaling group to add to this Deployment Group. [disable-awslint:ref-via-interface] is needed in order to install the code deploy agent by updating the ASGs user data.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addAutoScalingGroup", [asg])

    @builtins.property
    @jsii.member(jsii_name="application")
    def application(self) -> "IServerApplication":
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "application")

    @builtins.property
    @jsii.member(jsii_name="deploymentConfig")
    def deployment_config(self) -> "IServerDeploymentConfig":
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "deploymentConfig")

    @builtins.property
    @jsii.member(jsii_name="deploymentGroupArn")
    def deployment_group_arn(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "deploymentGroupArn")

    @builtins.property
    @jsii.member(jsii_name="deploymentGroupName")
    def deployment_group_name(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "deploymentGroupName")

    @builtins.property
    @jsii.member(jsii_name="autoScalingGroups")
    def auto_scaling_groups(self) -> typing.Optional[typing.List[_AutoScalingGroup_003d0b84]]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "autoScalingGroups")

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "role")


@jsii.data_type(jsii_type="monocdk-experiment.aws_codedeploy.ServerDeploymentGroupAttributes", jsii_struct_bases=[], name_mapping={'application': 'application', 'deployment_group_name': 'deploymentGroupName', 'deployment_config': 'deploymentConfig'})
class ServerDeploymentGroupAttributes():
    def __init__(self, *, application: "IServerApplication", deployment_group_name: str, deployment_config: typing.Optional["IServerDeploymentConfig"]=None) -> None:
        """Properties of a reference to a CodeDeploy EC2/on-premise Deployment Group.

        :param application: The reference to the CodeDeploy EC2/on-premise Application that this Deployment Group belongs to.
        :param deployment_group_name: The physical, human-readable name of the CodeDeploy EC2/on-premise Deployment Group that we are referencing.
        :param deployment_config: The Deployment Configuration this Deployment Group uses. Default: ServerDeploymentConfig#OneAtATime

        see
        :see: ServerDeploymentGroup#import
        stability
        :stability: experimental
        """
        self._values = {
            'application': application,
            'deployment_group_name': deployment_group_name,
        }
        if deployment_config is not None: self._values["deployment_config"] = deployment_config

    @builtins.property
    def application(self) -> "IServerApplication":
        """The reference to the CodeDeploy EC2/on-premise Application that this Deployment Group belongs to.

        stability
        :stability: experimental
        """
        return self._values.get('application')

    @builtins.property
    def deployment_group_name(self) -> str:
        """The physical, human-readable name of the CodeDeploy EC2/on-premise Deployment Group that we are referencing.

        stability
        :stability: experimental
        """
        return self._values.get('deployment_group_name')

    @builtins.property
    def deployment_config(self) -> typing.Optional["IServerDeploymentConfig"]:
        """The Deployment Configuration this Deployment Group uses.

        default
        :default: ServerDeploymentConfig#OneAtATime

        stability
        :stability: experimental
        """
        return self._values.get('deployment_config')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ServerDeploymentGroupAttributes(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_codedeploy.ServerDeploymentGroupProps", jsii_struct_bases=[], name_mapping={'alarms': 'alarms', 'application': 'application', 'auto_rollback': 'autoRollback', 'auto_scaling_groups': 'autoScalingGroups', 'deployment_config': 'deploymentConfig', 'deployment_group_name': 'deploymentGroupName', 'ec2_instance_tags': 'ec2InstanceTags', 'ignore_poll_alarms_failure': 'ignorePollAlarmsFailure', 'install_agent': 'installAgent', 'load_balancer': 'loadBalancer', 'on_premise_instance_tags': 'onPremiseInstanceTags', 'role': 'role'})
class ServerDeploymentGroupProps():
    def __init__(self, *, alarms: typing.Optional[typing.List[_IAlarm_478ec33c]]=None, application: typing.Optional["IServerApplication"]=None, auto_rollback: typing.Optional["AutoRollbackConfig"]=None, auto_scaling_groups: typing.Optional[typing.List[_AutoScalingGroup_003d0b84]]=None, deployment_config: typing.Optional["IServerDeploymentConfig"]=None, deployment_group_name: typing.Optional[str]=None, ec2_instance_tags: typing.Optional["InstanceTagSet"]=None, ignore_poll_alarms_failure: typing.Optional[bool]=None, install_agent: typing.Optional[bool]=None, load_balancer: typing.Optional["LoadBalancer"]=None, on_premise_instance_tags: typing.Optional["InstanceTagSet"]=None, role: typing.Optional[_IRole_e69bbae4]=None) -> None:
        """Construction properties for {@link ServerDeploymentGroup}.

        :param alarms: The CloudWatch alarms associated with this Deployment Group. CodeDeploy will stop (and optionally roll back) a deployment if during it any of the alarms trigger. Alarms can also be added after the Deployment Group is created using the {@link #addAlarm} method. Default: []
        :param application: The CodeDeploy EC2/on-premise Application this Deployment Group belongs to. Default: - A new Application will be created.
        :param auto_rollback: The auto-rollback configuration for this Deployment Group. Default: - default AutoRollbackConfig.
        :param auto_scaling_groups: The auto-scaling groups belonging to this Deployment Group. Auto-scaling groups can also be added after the Deployment Group is created using the {@link #addAutoScalingGroup} method. [disable-awslint:ref-via-interface] is needed because we update userdata for ASGs to install the codedeploy agent. Default: []
        :param deployment_config: The EC2/on-premise Deployment Configuration to use for this Deployment Group. Default: ServerDeploymentConfig#OneAtATime
        :param deployment_group_name: The physical, human-readable name of the CodeDeploy Deployment Group. Default: - An auto-generated name will be used.
        :param ec2_instance_tags: All EC2 instances matching the given set of tags when a deployment occurs will be added to this Deployment Group. Default: - No additional EC2 instances will be added to the Deployment Group.
        :param ignore_poll_alarms_failure: Whether to continue a deployment even if fetching the alarm status from CloudWatch failed. Default: false
        :param install_agent: If you've provided any auto-scaling groups with the {@link #autoScalingGroups} property, you can set this property to add User Data that installs the CodeDeploy agent on the instances. Default: true
        :param load_balancer: The load balancer to place in front of this Deployment Group. Can be created from either a classic Elastic Load Balancer, or an Application Load Balancer / Network Load Balancer Target Group. Default: - Deployment Group will not have a load balancer defined.
        :param on_premise_instance_tags: All on-premise instances matching the given set of tags when a deployment occurs will be added to this Deployment Group. Default: - No additional on-premise instances will be added to the Deployment Group.
        :param role: The service Role of this Deployment Group. Default: - A new Role will be created.

        stability
        :stability: experimental
        """
        if isinstance(auto_rollback, dict): auto_rollback = AutoRollbackConfig(**auto_rollback)
        self._values = {
        }
        if alarms is not None: self._values["alarms"] = alarms
        if application is not None: self._values["application"] = application
        if auto_rollback is not None: self._values["auto_rollback"] = auto_rollback
        if auto_scaling_groups is not None: self._values["auto_scaling_groups"] = auto_scaling_groups
        if deployment_config is not None: self._values["deployment_config"] = deployment_config
        if deployment_group_name is not None: self._values["deployment_group_name"] = deployment_group_name
        if ec2_instance_tags is not None: self._values["ec2_instance_tags"] = ec2_instance_tags
        if ignore_poll_alarms_failure is not None: self._values["ignore_poll_alarms_failure"] = ignore_poll_alarms_failure
        if install_agent is not None: self._values["install_agent"] = install_agent
        if load_balancer is not None: self._values["load_balancer"] = load_balancer
        if on_premise_instance_tags is not None: self._values["on_premise_instance_tags"] = on_premise_instance_tags
        if role is not None: self._values["role"] = role

    @builtins.property
    def alarms(self) -> typing.Optional[typing.List[_IAlarm_478ec33c]]:
        """The CloudWatch alarms associated with this Deployment Group.

        CodeDeploy will stop (and optionally roll back)
        a deployment if during it any of the alarms trigger.

        Alarms can also be added after the Deployment Group is created using the {@link #addAlarm} method.

        default
        :default: []

        see
        :see: https://docs.aws.amazon.com/codedeploy/latest/userguide/monitoring-create-alarms.html
        stability
        :stability: experimental
        """
        return self._values.get('alarms')

    @builtins.property
    def application(self) -> typing.Optional["IServerApplication"]:
        """The CodeDeploy EC2/on-premise Application this Deployment Group belongs to.

        default
        :default: - A new Application will be created.

        stability
        :stability: experimental
        """
        return self._values.get('application')

    @builtins.property
    def auto_rollback(self) -> typing.Optional["AutoRollbackConfig"]:
        """The auto-rollback configuration for this Deployment Group.

        default
        :default: - default AutoRollbackConfig.

        stability
        :stability: experimental
        """
        return self._values.get('auto_rollback')

    @builtins.property
    def auto_scaling_groups(self) -> typing.Optional[typing.List[_AutoScalingGroup_003d0b84]]:
        """The auto-scaling groups belonging to this Deployment Group.

        Auto-scaling groups can also be added after the Deployment Group is created
        using the {@link #addAutoScalingGroup} method.

        [disable-awslint:ref-via-interface] is needed because we update userdata
        for ASGs to install the codedeploy agent.

        default
        :default: []

        stability
        :stability: experimental
        """
        return self._values.get('auto_scaling_groups')

    @builtins.property
    def deployment_config(self) -> typing.Optional["IServerDeploymentConfig"]:
        """The EC2/on-premise Deployment Configuration to use for this Deployment Group.

        default
        :default: ServerDeploymentConfig#OneAtATime

        stability
        :stability: experimental
        """
        return self._values.get('deployment_config')

    @builtins.property
    def deployment_group_name(self) -> typing.Optional[str]:
        """The physical, human-readable name of the CodeDeploy Deployment Group.

        default
        :default: - An auto-generated name will be used.

        stability
        :stability: experimental
        """
        return self._values.get('deployment_group_name')

    @builtins.property
    def ec2_instance_tags(self) -> typing.Optional["InstanceTagSet"]:
        """All EC2 instances matching the given set of tags when a deployment occurs will be added to this Deployment Group.

        default
        :default: - No additional EC2 instances will be added to the Deployment Group.

        stability
        :stability: experimental
        """
        return self._values.get('ec2_instance_tags')

    @builtins.property
    def ignore_poll_alarms_failure(self) -> typing.Optional[bool]:
        """Whether to continue a deployment even if fetching the alarm status from CloudWatch failed.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('ignore_poll_alarms_failure')

    @builtins.property
    def install_agent(self) -> typing.Optional[bool]:
        """If you've provided any auto-scaling groups with the {@link #autoScalingGroups} property, you can set this property to add User Data that installs the CodeDeploy agent on the instances.

        default
        :default: true

        see
        :see: https://docs.aws.amazon.com/codedeploy/latest/userguide/codedeploy-agent-operations-install.html
        stability
        :stability: experimental
        """
        return self._values.get('install_agent')

    @builtins.property
    def load_balancer(self) -> typing.Optional["LoadBalancer"]:
        """The load balancer to place in front of this Deployment Group.

        Can be created from either a classic Elastic Load Balancer,
        or an Application Load Balancer / Network Load Balancer Target Group.

        default
        :default: - Deployment Group will not have a load balancer defined.

        stability
        :stability: experimental
        """
        return self._values.get('load_balancer')

    @builtins.property
    def on_premise_instance_tags(self) -> typing.Optional["InstanceTagSet"]:
        """All on-premise instances matching the given set of tags when a deployment occurs will be added to this Deployment Group.

        default
        :default: - No additional on-premise instances will be added to the Deployment Group.

        stability
        :stability: experimental
        """
        return self._values.get('on_premise_instance_tags')

    @builtins.property
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The service Role of this Deployment Group.

        default
        :default: - A new Role will be created.

        stability
        :stability: experimental
        """
        return self._values.get('role')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ServerDeploymentGroupProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(IEcsApplication)
class EcsApplication(_Resource_884d0774, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_codedeploy.EcsApplication"):
    """A CodeDeploy Application that deploys to an Amazon ECS service.

    stability
    :stability: experimental
    resource:
    :resource:: AWS::CodeDeploy::Application
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, application_name: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param application_name: The physical, human-readable name of the CodeDeploy Application. Default: an auto-generated name will be used

        stability
        :stability: experimental
        """
        props = EcsApplicationProps(application_name=application_name)

        jsii.create(EcsApplication, self, [scope, id, props])

    @jsii.member(jsii_name="fromEcsApplicationName")
    @builtins.classmethod
    def from_ecs_application_name(cls, scope: _Construct_f50a3f53, id: str, ecs_application_name: str) -> "IEcsApplication":
        """Import an Application defined either outside the CDK, or in a different CDK Stack.

        :param scope: the parent Construct for this new Construct.
        :param id: the logical ID of this new Construct.
        :param ecs_application_name: the name of the application to import.

        return
        :return: a Construct representing a reference to an existing Application

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromEcsApplicationName", [scope, id, ecs_application_name])

    @builtins.property
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "applicationArn")

    @builtins.property
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "applicationName")


__all__ = [
    "AutoRollbackConfig",
    "CfnApplication",
    "CfnApplicationProps",
    "CfnDeploymentConfig",
    "CfnDeploymentConfigProps",
    "CfnDeploymentGroup",
    "CfnDeploymentGroupProps",
    "EcsApplication",
    "EcsApplicationProps",
    "EcsDeploymentConfig",
    "EcsDeploymentGroup",
    "EcsDeploymentGroupAttributes",
    "IEcsApplication",
    "IEcsDeploymentConfig",
    "IEcsDeploymentGroup",
    "ILambdaApplication",
    "ILambdaDeploymentConfig",
    "ILambdaDeploymentGroup",
    "IServerApplication",
    "IServerDeploymentConfig",
    "IServerDeploymentGroup",
    "InstanceTagSet",
    "LambdaApplication",
    "LambdaApplicationProps",
    "LambdaDeploymentConfig",
    "LambdaDeploymentConfigImportProps",
    "LambdaDeploymentGroup",
    "LambdaDeploymentGroupAttributes",
    "LambdaDeploymentGroupProps",
    "LoadBalancer",
    "LoadBalancerGeneration",
    "MinimumHealthyHosts",
    "ServerApplication",
    "ServerApplicationProps",
    "ServerDeploymentConfig",
    "ServerDeploymentConfigProps",
    "ServerDeploymentGroup",
    "ServerDeploymentGroupAttributes",
    "ServerDeploymentGroupProps",
]

publication.publish()
