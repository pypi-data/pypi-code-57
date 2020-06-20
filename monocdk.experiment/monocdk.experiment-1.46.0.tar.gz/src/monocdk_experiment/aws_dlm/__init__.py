import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *

from .. import (CfnResource as _CfnResource_7760e8e4, Construct as _Construct_f50a3f53, FromCloudFormationOptions as _FromCloudFormationOptions_5f49f6f1, TreeInspector as _TreeInspector_154f5999, IResolvable as _IResolvable_9ceae33e, CfnTag as _CfnTag_b4661f1a, IInspectable as _IInspectable_051e6ed8)


@jsii.implements(_IInspectable_051e6ed8)
class CfnLifecyclePolicy(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_dlm.CfnLifecyclePolicy"):
    """A CloudFormation ``AWS::DLM::LifecyclePolicy``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dlm-lifecyclepolicy.html
    cloudformationResource:
    :cloudformationResource:: AWS::DLM::LifecyclePolicy
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, description: typing.Optional[str]=None, execution_role_arn: typing.Optional[str]=None, policy_details: typing.Optional[typing.Union["PolicyDetailsProperty", _IResolvable_9ceae33e]]=None, state: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::DLM::LifecyclePolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: ``AWS::DLM::LifecyclePolicy.Description``.
        :param execution_role_arn: ``AWS::DLM::LifecyclePolicy.ExecutionRoleArn``.
        :param policy_details: ``AWS::DLM::LifecyclePolicy.PolicyDetails``.
        :param state: ``AWS::DLM::LifecyclePolicy.State``.
        """
        props = CfnLifecyclePolicyProps(description=description, execution_role_arn=execution_role_arn, policy_details=policy_details, state=state)

        jsii.create(CfnLifecyclePolicy, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnLifecyclePolicy":
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
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::DLM::LifecyclePolicy.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dlm-lifecyclepolicy.html#cfn-dlm-lifecyclepolicy-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="executionRoleArn")
    def execution_role_arn(self) -> typing.Optional[str]:
        """``AWS::DLM::LifecyclePolicy.ExecutionRoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dlm-lifecyclepolicy.html#cfn-dlm-lifecyclepolicy-executionrolearn
        """
        return jsii.get(self, "executionRoleArn")

    @execution_role_arn.setter
    def execution_role_arn(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "executionRoleArn", value)

    @builtins.property
    @jsii.member(jsii_name="policyDetails")
    def policy_details(self) -> typing.Optional[typing.Union["PolicyDetailsProperty", _IResolvable_9ceae33e]]:
        """``AWS::DLM::LifecyclePolicy.PolicyDetails``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dlm-lifecyclepolicy.html#cfn-dlm-lifecyclepolicy-policydetails
        """
        return jsii.get(self, "policyDetails")

    @policy_details.setter
    def policy_details(self, value: typing.Optional[typing.Union["PolicyDetailsProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "policyDetails", value)

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> typing.Optional[str]:
        """``AWS::DLM::LifecyclePolicy.State``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dlm-lifecyclepolicy.html#cfn-dlm-lifecyclepolicy-state
        """
        return jsii.get(self, "state")

    @state.setter
    def state(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "state", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_dlm.CfnLifecyclePolicy.CreateRuleProperty", jsii_struct_bases=[], name_mapping={'cron_expression': 'cronExpression', 'interval': 'interval', 'interval_unit': 'intervalUnit', 'times': 'times'})
    class CreateRuleProperty():
        def __init__(self, *, cron_expression: typing.Optional[str]=None, interval: typing.Optional[jsii.Number]=None, interval_unit: typing.Optional[str]=None, times: typing.Optional[typing.List[str]]=None) -> None:
            """
            :param cron_expression: ``CfnLifecyclePolicy.CreateRuleProperty.CronExpression``.
            :param interval: ``CfnLifecyclePolicy.CreateRuleProperty.Interval``.
            :param interval_unit: ``CfnLifecyclePolicy.CreateRuleProperty.IntervalUnit``.
            :param times: ``CfnLifecyclePolicy.CreateRuleProperty.Times``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-createrule.html
            """
            self._values = {
            }
            if cron_expression is not None: self._values["cron_expression"] = cron_expression
            if interval is not None: self._values["interval"] = interval
            if interval_unit is not None: self._values["interval_unit"] = interval_unit
            if times is not None: self._values["times"] = times

        @builtins.property
        def cron_expression(self) -> typing.Optional[str]:
            """``CfnLifecyclePolicy.CreateRuleProperty.CronExpression``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-createrule.html#cfn-dlm-lifecyclepolicy-createrule-cronexpression
            """
            return self._values.get('cron_expression')

        @builtins.property
        def interval(self) -> typing.Optional[jsii.Number]:
            """``CfnLifecyclePolicy.CreateRuleProperty.Interval``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-createrule.html#cfn-dlm-lifecyclepolicy-createrule-interval
            """
            return self._values.get('interval')

        @builtins.property
        def interval_unit(self) -> typing.Optional[str]:
            """``CfnLifecyclePolicy.CreateRuleProperty.IntervalUnit``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-createrule.html#cfn-dlm-lifecyclepolicy-createrule-intervalunit
            """
            return self._values.get('interval_unit')

        @builtins.property
        def times(self) -> typing.Optional[typing.List[str]]:
            """``CfnLifecyclePolicy.CreateRuleProperty.Times``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-createrule.html#cfn-dlm-lifecyclepolicy-createrule-times
            """
            return self._values.get('times')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'CreateRuleProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_dlm.CfnLifecyclePolicy.CrossRegionCopyRetainRuleProperty", jsii_struct_bases=[], name_mapping={'interval': 'interval', 'interval_unit': 'intervalUnit'})
    class CrossRegionCopyRetainRuleProperty():
        def __init__(self, *, interval: jsii.Number, interval_unit: str) -> None:
            """
            :param interval: ``CfnLifecyclePolicy.CrossRegionCopyRetainRuleProperty.Interval``.
            :param interval_unit: ``CfnLifecyclePolicy.CrossRegionCopyRetainRuleProperty.IntervalUnit``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopyretainrule.html
            """
            self._values = {
                'interval': interval,
                'interval_unit': interval_unit,
            }

        @builtins.property
        def interval(self) -> jsii.Number:
            """``CfnLifecyclePolicy.CrossRegionCopyRetainRuleProperty.Interval``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopyretainrule.html#cfn-dlm-lifecyclepolicy-crossregioncopyretainrule-interval
            """
            return self._values.get('interval')

        @builtins.property
        def interval_unit(self) -> str:
            """``CfnLifecyclePolicy.CrossRegionCopyRetainRuleProperty.IntervalUnit``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopyretainrule.html#cfn-dlm-lifecyclepolicy-crossregioncopyretainrule-intervalunit
            """
            return self._values.get('interval_unit')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'CrossRegionCopyRetainRuleProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_dlm.CfnLifecyclePolicy.CrossRegionCopyRuleProperty", jsii_struct_bases=[], name_mapping={'encrypted': 'encrypted', 'target_region': 'targetRegion', 'cmk_arn': 'cmkArn', 'copy_tags': 'copyTags', 'retain_rule': 'retainRule'})
    class CrossRegionCopyRuleProperty():
        def __init__(self, *, encrypted: typing.Union[bool, _IResolvable_9ceae33e], target_region: str, cmk_arn: typing.Optional[str]=None, copy_tags: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, retain_rule: typing.Optional[typing.Union["CfnLifecyclePolicy.CrossRegionCopyRetainRuleProperty", _IResolvable_9ceae33e]]=None) -> None:
            """
            :param encrypted: ``CfnLifecyclePolicy.CrossRegionCopyRuleProperty.Encrypted``.
            :param target_region: ``CfnLifecyclePolicy.CrossRegionCopyRuleProperty.TargetRegion``.
            :param cmk_arn: ``CfnLifecyclePolicy.CrossRegionCopyRuleProperty.CmkArn``.
            :param copy_tags: ``CfnLifecyclePolicy.CrossRegionCopyRuleProperty.CopyTags``.
            :param retain_rule: ``CfnLifecyclePolicy.CrossRegionCopyRuleProperty.RetainRule``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopyrule.html
            """
            self._values = {
                'encrypted': encrypted,
                'target_region': target_region,
            }
            if cmk_arn is not None: self._values["cmk_arn"] = cmk_arn
            if copy_tags is not None: self._values["copy_tags"] = copy_tags
            if retain_rule is not None: self._values["retain_rule"] = retain_rule

        @builtins.property
        def encrypted(self) -> typing.Union[bool, _IResolvable_9ceae33e]:
            """``CfnLifecyclePolicy.CrossRegionCopyRuleProperty.Encrypted``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopyrule.html#cfn-dlm-lifecyclepolicy-crossregioncopyrule-encrypted
            """
            return self._values.get('encrypted')

        @builtins.property
        def target_region(self) -> str:
            """``CfnLifecyclePolicy.CrossRegionCopyRuleProperty.TargetRegion``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopyrule.html#cfn-dlm-lifecyclepolicy-crossregioncopyrule-targetregion
            """
            return self._values.get('target_region')

        @builtins.property
        def cmk_arn(self) -> typing.Optional[str]:
            """``CfnLifecyclePolicy.CrossRegionCopyRuleProperty.CmkArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopyrule.html#cfn-dlm-lifecyclepolicy-crossregioncopyrule-cmkarn
            """
            return self._values.get('cmk_arn')

        @builtins.property
        def copy_tags(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnLifecyclePolicy.CrossRegionCopyRuleProperty.CopyTags``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopyrule.html#cfn-dlm-lifecyclepolicy-crossregioncopyrule-copytags
            """
            return self._values.get('copy_tags')

        @builtins.property
        def retain_rule(self) -> typing.Optional[typing.Union["CfnLifecyclePolicy.CrossRegionCopyRetainRuleProperty", _IResolvable_9ceae33e]]:
            """``CfnLifecyclePolicy.CrossRegionCopyRuleProperty.RetainRule``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-crossregioncopyrule.html#cfn-dlm-lifecyclepolicy-crossregioncopyrule-retainrule
            """
            return self._values.get('retain_rule')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'CrossRegionCopyRuleProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_dlm.CfnLifecyclePolicy.FastRestoreRuleProperty", jsii_struct_bases=[], name_mapping={'availability_zones': 'availabilityZones', 'count': 'count', 'interval': 'interval', 'interval_unit': 'intervalUnit'})
    class FastRestoreRuleProperty():
        def __init__(self, *, availability_zones: typing.Optional[typing.List[str]]=None, count: typing.Optional[jsii.Number]=None, interval: typing.Optional[jsii.Number]=None, interval_unit: typing.Optional[str]=None) -> None:
            """
            :param availability_zones: ``CfnLifecyclePolicy.FastRestoreRuleProperty.AvailabilityZones``.
            :param count: ``CfnLifecyclePolicy.FastRestoreRuleProperty.Count``.
            :param interval: ``CfnLifecyclePolicy.FastRestoreRuleProperty.Interval``.
            :param interval_unit: ``CfnLifecyclePolicy.FastRestoreRuleProperty.IntervalUnit``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-fastrestorerule.html
            """
            self._values = {
            }
            if availability_zones is not None: self._values["availability_zones"] = availability_zones
            if count is not None: self._values["count"] = count
            if interval is not None: self._values["interval"] = interval
            if interval_unit is not None: self._values["interval_unit"] = interval_unit

        @builtins.property
        def availability_zones(self) -> typing.Optional[typing.List[str]]:
            """``CfnLifecyclePolicy.FastRestoreRuleProperty.AvailabilityZones``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-fastrestorerule.html#cfn-dlm-lifecyclepolicy-fastrestorerule-availabilityzones
            """
            return self._values.get('availability_zones')

        @builtins.property
        def count(self) -> typing.Optional[jsii.Number]:
            """``CfnLifecyclePolicy.FastRestoreRuleProperty.Count``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-fastrestorerule.html#cfn-dlm-lifecyclepolicy-fastrestorerule-count
            """
            return self._values.get('count')

        @builtins.property
        def interval(self) -> typing.Optional[jsii.Number]:
            """``CfnLifecyclePolicy.FastRestoreRuleProperty.Interval``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-fastrestorerule.html#cfn-dlm-lifecyclepolicy-fastrestorerule-interval
            """
            return self._values.get('interval')

        @builtins.property
        def interval_unit(self) -> typing.Optional[str]:
            """``CfnLifecyclePolicy.FastRestoreRuleProperty.IntervalUnit``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-fastrestorerule.html#cfn-dlm-lifecyclepolicy-fastrestorerule-intervalunit
            """
            return self._values.get('interval_unit')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'FastRestoreRuleProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_dlm.CfnLifecyclePolicy.ParametersProperty", jsii_struct_bases=[], name_mapping={'exclude_boot_volume': 'excludeBootVolume'})
    class ParametersProperty():
        def __init__(self, *, exclude_boot_volume: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None) -> None:
            """
            :param exclude_boot_volume: ``CfnLifecyclePolicy.ParametersProperty.ExcludeBootVolume``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-parameters.html
            """
            self._values = {
            }
            if exclude_boot_volume is not None: self._values["exclude_boot_volume"] = exclude_boot_volume

        @builtins.property
        def exclude_boot_volume(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnLifecyclePolicy.ParametersProperty.ExcludeBootVolume``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-parameters.html#cfn-dlm-lifecyclepolicy-parameters-excludebootvolume
            """
            return self._values.get('exclude_boot_volume')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ParametersProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_dlm.CfnLifecyclePolicy.PolicyDetailsProperty", jsii_struct_bases=[], name_mapping={'resource_types': 'resourceTypes', 'schedules': 'schedules', 'target_tags': 'targetTags', 'parameters': 'parameters', 'policy_type': 'policyType'})
    class PolicyDetailsProperty():
        def __init__(self, *, resource_types: typing.List[str], schedules: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnLifecyclePolicy.ScheduleProperty", _IResolvable_9ceae33e]]], target_tags: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union[_IResolvable_9ceae33e, _CfnTag_b4661f1a]]], parameters: typing.Optional[typing.Union["CfnLifecyclePolicy.ParametersProperty", _IResolvable_9ceae33e]]=None, policy_type: typing.Optional[str]=None) -> None:
            """
            :param resource_types: ``CfnLifecyclePolicy.PolicyDetailsProperty.ResourceTypes``.
            :param schedules: ``CfnLifecyclePolicy.PolicyDetailsProperty.Schedules``.
            :param target_tags: ``CfnLifecyclePolicy.PolicyDetailsProperty.TargetTags``.
            :param parameters: ``CfnLifecyclePolicy.PolicyDetailsProperty.Parameters``.
            :param policy_type: ``CfnLifecyclePolicy.PolicyDetailsProperty.PolicyType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-policydetails.html
            """
            self._values = {
                'resource_types': resource_types,
                'schedules': schedules,
                'target_tags': target_tags,
            }
            if parameters is not None: self._values["parameters"] = parameters
            if policy_type is not None: self._values["policy_type"] = policy_type

        @builtins.property
        def resource_types(self) -> typing.List[str]:
            """``CfnLifecyclePolicy.PolicyDetailsProperty.ResourceTypes``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-policydetails.html#cfn-dlm-lifecyclepolicy-policydetails-resourcetypes
            """
            return self._values.get('resource_types')

        @builtins.property
        def schedules(self) -> typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnLifecyclePolicy.ScheduleProperty", _IResolvable_9ceae33e]]]:
            """``CfnLifecyclePolicy.PolicyDetailsProperty.Schedules``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-policydetails.html#cfn-dlm-lifecyclepolicy-policydetails-schedules
            """
            return self._values.get('schedules')

        @builtins.property
        def target_tags(self) -> typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union[_IResolvable_9ceae33e, _CfnTag_b4661f1a]]]:
            """``CfnLifecyclePolicy.PolicyDetailsProperty.TargetTags``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-policydetails.html#cfn-dlm-lifecyclepolicy-policydetails-targettags
            """
            return self._values.get('target_tags')

        @builtins.property
        def parameters(self) -> typing.Optional[typing.Union["CfnLifecyclePolicy.ParametersProperty", _IResolvable_9ceae33e]]:
            """``CfnLifecyclePolicy.PolicyDetailsProperty.Parameters``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-policydetails.html#cfn-dlm-lifecyclepolicy-policydetails-parameters
            """
            return self._values.get('parameters')

        @builtins.property
        def policy_type(self) -> typing.Optional[str]:
            """``CfnLifecyclePolicy.PolicyDetailsProperty.PolicyType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-policydetails.html#cfn-dlm-lifecyclepolicy-policydetails-policytype
            """
            return self._values.get('policy_type')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'PolicyDetailsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_dlm.CfnLifecyclePolicy.RetainRuleProperty", jsii_struct_bases=[], name_mapping={'count': 'count', 'interval': 'interval', 'interval_unit': 'intervalUnit'})
    class RetainRuleProperty():
        def __init__(self, *, count: typing.Optional[jsii.Number]=None, interval: typing.Optional[jsii.Number]=None, interval_unit: typing.Optional[str]=None) -> None:
            """
            :param count: ``CfnLifecyclePolicy.RetainRuleProperty.Count``.
            :param interval: ``CfnLifecyclePolicy.RetainRuleProperty.Interval``.
            :param interval_unit: ``CfnLifecyclePolicy.RetainRuleProperty.IntervalUnit``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-retainrule.html
            """
            self._values = {
            }
            if count is not None: self._values["count"] = count
            if interval is not None: self._values["interval"] = interval
            if interval_unit is not None: self._values["interval_unit"] = interval_unit

        @builtins.property
        def count(self) -> typing.Optional[jsii.Number]:
            """``CfnLifecyclePolicy.RetainRuleProperty.Count``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-retainrule.html#cfn-dlm-lifecyclepolicy-retainrule-count
            """
            return self._values.get('count')

        @builtins.property
        def interval(self) -> typing.Optional[jsii.Number]:
            """``CfnLifecyclePolicy.RetainRuleProperty.Interval``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-retainrule.html#cfn-dlm-lifecyclepolicy-retainrule-interval
            """
            return self._values.get('interval')

        @builtins.property
        def interval_unit(self) -> typing.Optional[str]:
            """``CfnLifecyclePolicy.RetainRuleProperty.IntervalUnit``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-retainrule.html#cfn-dlm-lifecyclepolicy-retainrule-intervalunit
            """
            return self._values.get('interval_unit')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'RetainRuleProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_dlm.CfnLifecyclePolicy.ScheduleProperty", jsii_struct_bases=[], name_mapping={'copy_tags': 'copyTags', 'create_rule': 'createRule', 'cross_region_copy_rules': 'crossRegionCopyRules', 'fast_restore_rule': 'fastRestoreRule', 'name': 'name', 'retain_rule': 'retainRule', 'tags_to_add': 'tagsToAdd', 'variable_tags': 'variableTags'})
    class ScheduleProperty():
        def __init__(self, *, copy_tags: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, create_rule: typing.Optional[typing.Union["CfnLifecyclePolicy.CreateRuleProperty", _IResolvable_9ceae33e]]=None, cross_region_copy_rules: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnLifecyclePolicy.CrossRegionCopyRuleProperty", _IResolvable_9ceae33e]]]]=None, fast_restore_rule: typing.Optional[typing.Union["CfnLifecyclePolicy.FastRestoreRuleProperty", _IResolvable_9ceae33e]]=None, name: typing.Optional[str]=None, retain_rule: typing.Optional[typing.Union["CfnLifecyclePolicy.RetainRuleProperty", _IResolvable_9ceae33e]]=None, tags_to_add: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union[_IResolvable_9ceae33e, _CfnTag_b4661f1a]]]]=None, variable_tags: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union[_IResolvable_9ceae33e, _CfnTag_b4661f1a]]]]=None) -> None:
            """
            :param copy_tags: ``CfnLifecyclePolicy.ScheduleProperty.CopyTags``.
            :param create_rule: ``CfnLifecyclePolicy.ScheduleProperty.CreateRule``.
            :param cross_region_copy_rules: ``CfnLifecyclePolicy.ScheduleProperty.CrossRegionCopyRules``.
            :param fast_restore_rule: ``CfnLifecyclePolicy.ScheduleProperty.FastRestoreRule``.
            :param name: ``CfnLifecyclePolicy.ScheduleProperty.Name``.
            :param retain_rule: ``CfnLifecyclePolicy.ScheduleProperty.RetainRule``.
            :param tags_to_add: ``CfnLifecyclePolicy.ScheduleProperty.TagsToAdd``.
            :param variable_tags: ``CfnLifecyclePolicy.ScheduleProperty.VariableTags``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-schedule.html
            """
            self._values = {
            }
            if copy_tags is not None: self._values["copy_tags"] = copy_tags
            if create_rule is not None: self._values["create_rule"] = create_rule
            if cross_region_copy_rules is not None: self._values["cross_region_copy_rules"] = cross_region_copy_rules
            if fast_restore_rule is not None: self._values["fast_restore_rule"] = fast_restore_rule
            if name is not None: self._values["name"] = name
            if retain_rule is not None: self._values["retain_rule"] = retain_rule
            if tags_to_add is not None: self._values["tags_to_add"] = tags_to_add
            if variable_tags is not None: self._values["variable_tags"] = variable_tags

        @builtins.property
        def copy_tags(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnLifecyclePolicy.ScheduleProperty.CopyTags``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-schedule.html#cfn-dlm-lifecyclepolicy-schedule-copytags
            """
            return self._values.get('copy_tags')

        @builtins.property
        def create_rule(self) -> typing.Optional[typing.Union["CfnLifecyclePolicy.CreateRuleProperty", _IResolvable_9ceae33e]]:
            """``CfnLifecyclePolicy.ScheduleProperty.CreateRule``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-schedule.html#cfn-dlm-lifecyclepolicy-schedule-createrule
            """
            return self._values.get('create_rule')

        @builtins.property
        def cross_region_copy_rules(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnLifecyclePolicy.CrossRegionCopyRuleProperty", _IResolvable_9ceae33e]]]]:
            """``CfnLifecyclePolicy.ScheduleProperty.CrossRegionCopyRules``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-schedule.html#cfn-dlm-lifecyclepolicy-schedule-crossregioncopyrules
            """
            return self._values.get('cross_region_copy_rules')

        @builtins.property
        def fast_restore_rule(self) -> typing.Optional[typing.Union["CfnLifecyclePolicy.FastRestoreRuleProperty", _IResolvable_9ceae33e]]:
            """``CfnLifecyclePolicy.ScheduleProperty.FastRestoreRule``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-schedule.html#cfn-dlm-lifecyclepolicy-schedule-fastrestorerule
            """
            return self._values.get('fast_restore_rule')

        @builtins.property
        def name(self) -> typing.Optional[str]:
            """``CfnLifecyclePolicy.ScheduleProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-schedule.html#cfn-dlm-lifecyclepolicy-schedule-name
            """
            return self._values.get('name')

        @builtins.property
        def retain_rule(self) -> typing.Optional[typing.Union["CfnLifecyclePolicy.RetainRuleProperty", _IResolvable_9ceae33e]]:
            """``CfnLifecyclePolicy.ScheduleProperty.RetainRule``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-schedule.html#cfn-dlm-lifecyclepolicy-schedule-retainrule
            """
            return self._values.get('retain_rule')

        @builtins.property
        def tags_to_add(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union[_IResolvable_9ceae33e, _CfnTag_b4661f1a]]]]:
            """``CfnLifecyclePolicy.ScheduleProperty.TagsToAdd``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-schedule.html#cfn-dlm-lifecyclepolicy-schedule-tagstoadd
            """
            return self._values.get('tags_to_add')

        @builtins.property
        def variable_tags(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union[_IResolvable_9ceae33e, _CfnTag_b4661f1a]]]]:
            """``CfnLifecyclePolicy.ScheduleProperty.VariableTags``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dlm-lifecyclepolicy-schedule.html#cfn-dlm-lifecyclepolicy-schedule-variabletags
            """
            return self._values.get('variable_tags')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ScheduleProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_dlm.CfnLifecyclePolicyProps", jsii_struct_bases=[], name_mapping={'description': 'description', 'execution_role_arn': 'executionRoleArn', 'policy_details': 'policyDetails', 'state': 'state'})
class CfnLifecyclePolicyProps():
    def __init__(self, *, description: typing.Optional[str]=None, execution_role_arn: typing.Optional[str]=None, policy_details: typing.Optional[typing.Union["CfnLifecyclePolicy.PolicyDetailsProperty", _IResolvable_9ceae33e]]=None, state: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::DLM::LifecyclePolicy``.

        :param description: ``AWS::DLM::LifecyclePolicy.Description``.
        :param execution_role_arn: ``AWS::DLM::LifecyclePolicy.ExecutionRoleArn``.
        :param policy_details: ``AWS::DLM::LifecyclePolicy.PolicyDetails``.
        :param state: ``AWS::DLM::LifecyclePolicy.State``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dlm-lifecyclepolicy.html
        """
        self._values = {
        }
        if description is not None: self._values["description"] = description
        if execution_role_arn is not None: self._values["execution_role_arn"] = execution_role_arn
        if policy_details is not None: self._values["policy_details"] = policy_details
        if state is not None: self._values["state"] = state

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::DLM::LifecyclePolicy.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dlm-lifecyclepolicy.html#cfn-dlm-lifecyclepolicy-description
        """
        return self._values.get('description')

    @builtins.property
    def execution_role_arn(self) -> typing.Optional[str]:
        """``AWS::DLM::LifecyclePolicy.ExecutionRoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dlm-lifecyclepolicy.html#cfn-dlm-lifecyclepolicy-executionrolearn
        """
        return self._values.get('execution_role_arn')

    @builtins.property
    def policy_details(self) -> typing.Optional[typing.Union["CfnLifecyclePolicy.PolicyDetailsProperty", _IResolvable_9ceae33e]]:
        """``AWS::DLM::LifecyclePolicy.PolicyDetails``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dlm-lifecyclepolicy.html#cfn-dlm-lifecyclepolicy-policydetails
        """
        return self._values.get('policy_details')

    @builtins.property
    def state(self) -> typing.Optional[str]:
        """``AWS::DLM::LifecyclePolicy.State``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dlm-lifecyclepolicy.html#cfn-dlm-lifecyclepolicy-state
        """
        return self._values.get('state')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnLifecyclePolicyProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "CfnLifecyclePolicy",
    "CfnLifecyclePolicyProps",
]

publication.publish()
