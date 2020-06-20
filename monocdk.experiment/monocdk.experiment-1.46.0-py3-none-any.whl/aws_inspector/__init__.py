import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *

from .. import (CfnResource as _CfnResource_7760e8e4, Construct as _Construct_f50a3f53, FromCloudFormationOptions as _FromCloudFormationOptions_5f49f6f1, TreeInspector as _TreeInspector_154f5999, IInspectable as _IInspectable_051e6ed8, IResolvable as _IResolvable_9ceae33e, CfnTag as _CfnTag_b4661f1a)


@jsii.implements(_IInspectable_051e6ed8)
class CfnAssessmentTarget(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_inspector.CfnAssessmentTarget"):
    """A CloudFormation ``AWS::Inspector::AssessmentTarget``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttarget.html
    cloudformationResource:
    :cloudformationResource:: AWS::Inspector::AssessmentTarget
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, assessment_target_name: typing.Optional[str]=None, resource_group_arn: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::Inspector::AssessmentTarget``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param assessment_target_name: ``AWS::Inspector::AssessmentTarget.AssessmentTargetName``.
        :param resource_group_arn: ``AWS::Inspector::AssessmentTarget.ResourceGroupArn``.
        """
        props = CfnAssessmentTargetProps(assessment_target_name=assessment_target_name, resource_group_arn=resource_group_arn)

        jsii.create(CfnAssessmentTarget, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnAssessmentTarget":
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
    @jsii.member(jsii_name="assessmentTargetName")
    def assessment_target_name(self) -> typing.Optional[str]:
        """``AWS::Inspector::AssessmentTarget.AssessmentTargetName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttarget.html#cfn-inspector-assessmenttarget-assessmenttargetname
        """
        return jsii.get(self, "assessmentTargetName")

    @assessment_target_name.setter
    def assessment_target_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "assessmentTargetName", value)

    @builtins.property
    @jsii.member(jsii_name="resourceGroupArn")
    def resource_group_arn(self) -> typing.Optional[str]:
        """``AWS::Inspector::AssessmentTarget.ResourceGroupArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttarget.html#cfn-inspector-assessmenttarget-resourcegrouparn
        """
        return jsii.get(self, "resourceGroupArn")

    @resource_group_arn.setter
    def resource_group_arn(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "resourceGroupArn", value)


@jsii.data_type(jsii_type="monocdk-experiment.aws_inspector.CfnAssessmentTargetProps", jsii_struct_bases=[], name_mapping={'assessment_target_name': 'assessmentTargetName', 'resource_group_arn': 'resourceGroupArn'})
class CfnAssessmentTargetProps():
    def __init__(self, *, assessment_target_name: typing.Optional[str]=None, resource_group_arn: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::Inspector::AssessmentTarget``.

        :param assessment_target_name: ``AWS::Inspector::AssessmentTarget.AssessmentTargetName``.
        :param resource_group_arn: ``AWS::Inspector::AssessmentTarget.ResourceGroupArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttarget.html
        """
        self._values = {
        }
        if assessment_target_name is not None: self._values["assessment_target_name"] = assessment_target_name
        if resource_group_arn is not None: self._values["resource_group_arn"] = resource_group_arn

    @builtins.property
    def assessment_target_name(self) -> typing.Optional[str]:
        """``AWS::Inspector::AssessmentTarget.AssessmentTargetName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttarget.html#cfn-inspector-assessmenttarget-assessmenttargetname
        """
        return self._values.get('assessment_target_name')

    @builtins.property
    def resource_group_arn(self) -> typing.Optional[str]:
        """``AWS::Inspector::AssessmentTarget.ResourceGroupArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttarget.html#cfn-inspector-assessmenttarget-resourcegrouparn
        """
        return self._values.get('resource_group_arn')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnAssessmentTargetProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnAssessmentTemplate(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_inspector.CfnAssessmentTemplate"):
    """A CloudFormation ``AWS::Inspector::AssessmentTemplate``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttemplate.html
    cloudformationResource:
    :cloudformationResource:: AWS::Inspector::AssessmentTemplate
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, assessment_target_arn: str, duration_in_seconds: jsii.Number, rules_package_arns: typing.List[str], assessment_template_name: typing.Optional[str]=None, user_attributes_for_findings: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union[_IResolvable_9ceae33e, _CfnTag_b4661f1a]]]]=None) -> None:
        """Create a new ``AWS::Inspector::AssessmentTemplate``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param assessment_target_arn: ``AWS::Inspector::AssessmentTemplate.AssessmentTargetArn``.
        :param duration_in_seconds: ``AWS::Inspector::AssessmentTemplate.DurationInSeconds``.
        :param rules_package_arns: ``AWS::Inspector::AssessmentTemplate.RulesPackageArns``.
        :param assessment_template_name: ``AWS::Inspector::AssessmentTemplate.AssessmentTemplateName``.
        :param user_attributes_for_findings: ``AWS::Inspector::AssessmentTemplate.UserAttributesForFindings``.
        """
        props = CfnAssessmentTemplateProps(assessment_target_arn=assessment_target_arn, duration_in_seconds=duration_in_seconds, rules_package_arns=rules_package_arns, assessment_template_name=assessment_template_name, user_attributes_for_findings=user_attributes_for_findings)

        jsii.create(CfnAssessmentTemplate, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnAssessmentTemplate":
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
    @jsii.member(jsii_name="assessmentTargetArn")
    def assessment_target_arn(self) -> str:
        """``AWS::Inspector::AssessmentTemplate.AssessmentTargetArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttemplate.html#cfn-inspector-assessmenttemplate-assessmenttargetarn
        """
        return jsii.get(self, "assessmentTargetArn")

    @assessment_target_arn.setter
    def assessment_target_arn(self, value: str) -> None:
        jsii.set(self, "assessmentTargetArn", value)

    @builtins.property
    @jsii.member(jsii_name="durationInSeconds")
    def duration_in_seconds(self) -> jsii.Number:
        """``AWS::Inspector::AssessmentTemplate.DurationInSeconds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttemplate.html#cfn-inspector-assessmenttemplate-durationinseconds
        """
        return jsii.get(self, "durationInSeconds")

    @duration_in_seconds.setter
    def duration_in_seconds(self, value: jsii.Number) -> None:
        jsii.set(self, "durationInSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="rulesPackageArns")
    def rules_package_arns(self) -> typing.List[str]:
        """``AWS::Inspector::AssessmentTemplate.RulesPackageArns``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttemplate.html#cfn-inspector-assessmenttemplate-rulespackagearns
        """
        return jsii.get(self, "rulesPackageArns")

    @rules_package_arns.setter
    def rules_package_arns(self, value: typing.List[str]) -> None:
        jsii.set(self, "rulesPackageArns", value)

    @builtins.property
    @jsii.member(jsii_name="assessmentTemplateName")
    def assessment_template_name(self) -> typing.Optional[str]:
        """``AWS::Inspector::AssessmentTemplate.AssessmentTemplateName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttemplate.html#cfn-inspector-assessmenttemplate-assessmenttemplatename
        """
        return jsii.get(self, "assessmentTemplateName")

    @assessment_template_name.setter
    def assessment_template_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "assessmentTemplateName", value)

    @builtins.property
    @jsii.member(jsii_name="userAttributesForFindings")
    def user_attributes_for_findings(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union[_IResolvable_9ceae33e, _CfnTag_b4661f1a]]]]:
        """``AWS::Inspector::AssessmentTemplate.UserAttributesForFindings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttemplate.html#cfn-inspector-assessmenttemplate-userattributesforfindings
        """
        return jsii.get(self, "userAttributesForFindings")

    @user_attributes_for_findings.setter
    def user_attributes_for_findings(self, value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union[_IResolvable_9ceae33e, _CfnTag_b4661f1a]]]]) -> None:
        jsii.set(self, "userAttributesForFindings", value)


@jsii.data_type(jsii_type="monocdk-experiment.aws_inspector.CfnAssessmentTemplateProps", jsii_struct_bases=[], name_mapping={'assessment_target_arn': 'assessmentTargetArn', 'duration_in_seconds': 'durationInSeconds', 'rules_package_arns': 'rulesPackageArns', 'assessment_template_name': 'assessmentTemplateName', 'user_attributes_for_findings': 'userAttributesForFindings'})
class CfnAssessmentTemplateProps():
    def __init__(self, *, assessment_target_arn: str, duration_in_seconds: jsii.Number, rules_package_arns: typing.List[str], assessment_template_name: typing.Optional[str]=None, user_attributes_for_findings: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union[_IResolvable_9ceae33e, _CfnTag_b4661f1a]]]]=None) -> None:
        """Properties for defining a ``AWS::Inspector::AssessmentTemplate``.

        :param assessment_target_arn: ``AWS::Inspector::AssessmentTemplate.AssessmentTargetArn``.
        :param duration_in_seconds: ``AWS::Inspector::AssessmentTemplate.DurationInSeconds``.
        :param rules_package_arns: ``AWS::Inspector::AssessmentTemplate.RulesPackageArns``.
        :param assessment_template_name: ``AWS::Inspector::AssessmentTemplate.AssessmentTemplateName``.
        :param user_attributes_for_findings: ``AWS::Inspector::AssessmentTemplate.UserAttributesForFindings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttemplate.html
        """
        self._values = {
            'assessment_target_arn': assessment_target_arn,
            'duration_in_seconds': duration_in_seconds,
            'rules_package_arns': rules_package_arns,
        }
        if assessment_template_name is not None: self._values["assessment_template_name"] = assessment_template_name
        if user_attributes_for_findings is not None: self._values["user_attributes_for_findings"] = user_attributes_for_findings

    @builtins.property
    def assessment_target_arn(self) -> str:
        """``AWS::Inspector::AssessmentTemplate.AssessmentTargetArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttemplate.html#cfn-inspector-assessmenttemplate-assessmenttargetarn
        """
        return self._values.get('assessment_target_arn')

    @builtins.property
    def duration_in_seconds(self) -> jsii.Number:
        """``AWS::Inspector::AssessmentTemplate.DurationInSeconds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttemplate.html#cfn-inspector-assessmenttemplate-durationinseconds
        """
        return self._values.get('duration_in_seconds')

    @builtins.property
    def rules_package_arns(self) -> typing.List[str]:
        """``AWS::Inspector::AssessmentTemplate.RulesPackageArns``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttemplate.html#cfn-inspector-assessmenttemplate-rulespackagearns
        """
        return self._values.get('rules_package_arns')

    @builtins.property
    def assessment_template_name(self) -> typing.Optional[str]:
        """``AWS::Inspector::AssessmentTemplate.AssessmentTemplateName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttemplate.html#cfn-inspector-assessmenttemplate-assessmenttemplatename
        """
        return self._values.get('assessment_template_name')

    @builtins.property
    def user_attributes_for_findings(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union[_IResolvable_9ceae33e, _CfnTag_b4661f1a]]]]:
        """``AWS::Inspector::AssessmentTemplate.UserAttributesForFindings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttemplate.html#cfn-inspector-assessmenttemplate-userattributesforfindings
        """
        return self._values.get('user_attributes_for_findings')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnAssessmentTemplateProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnResourceGroup(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_inspector.CfnResourceGroup"):
    """A CloudFormation ``AWS::Inspector::ResourceGroup``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-resourcegroup.html
    cloudformationResource:
    :cloudformationResource:: AWS::Inspector::ResourceGroup
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, resource_group_tags: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union[_IResolvable_9ceae33e, _CfnTag_b4661f1a]]]) -> None:
        """Create a new ``AWS::Inspector::ResourceGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param resource_group_tags: ``AWS::Inspector::ResourceGroup.ResourceGroupTags``.
        """
        props = CfnResourceGroupProps(resource_group_tags=resource_group_tags)

        jsii.create(CfnResourceGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnResourceGroup":
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
    @jsii.member(jsii_name="resourceGroupTags")
    def resource_group_tags(self) -> typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union[_IResolvable_9ceae33e, _CfnTag_b4661f1a]]]:
        """``AWS::Inspector::ResourceGroup.ResourceGroupTags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-resourcegroup.html#cfn-inspector-resourcegroup-resourcegrouptags
        """
        return jsii.get(self, "resourceGroupTags")

    @resource_group_tags.setter
    def resource_group_tags(self, value: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union[_IResolvable_9ceae33e, _CfnTag_b4661f1a]]]) -> None:
        jsii.set(self, "resourceGroupTags", value)


@jsii.data_type(jsii_type="monocdk-experiment.aws_inspector.CfnResourceGroupProps", jsii_struct_bases=[], name_mapping={'resource_group_tags': 'resourceGroupTags'})
class CfnResourceGroupProps():
    def __init__(self, *, resource_group_tags: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union[_IResolvable_9ceae33e, _CfnTag_b4661f1a]]]) -> None:
        """Properties for defining a ``AWS::Inspector::ResourceGroup``.

        :param resource_group_tags: ``AWS::Inspector::ResourceGroup.ResourceGroupTags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-resourcegroup.html
        """
        self._values = {
            'resource_group_tags': resource_group_tags,
        }

    @builtins.property
    def resource_group_tags(self) -> typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union[_IResolvable_9ceae33e, _CfnTag_b4661f1a]]]:
        """``AWS::Inspector::ResourceGroup.ResourceGroupTags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-resourcegroup.html#cfn-inspector-resourcegroup-resourcegrouptags
        """
        return self._values.get('resource_group_tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnResourceGroupProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "CfnAssessmentTarget",
    "CfnAssessmentTargetProps",
    "CfnAssessmentTemplate",
    "CfnAssessmentTemplateProps",
    "CfnResourceGroup",
    "CfnResourceGroupProps",
]

publication.publish()
