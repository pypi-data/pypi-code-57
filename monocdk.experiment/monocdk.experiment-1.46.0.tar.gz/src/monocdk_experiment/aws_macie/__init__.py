import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *

from .. import (CfnResource as _CfnResource_7760e8e4, Construct as _Construct_f50a3f53, FromCloudFormationOptions as _FromCloudFormationOptions_5f49f6f1, TreeInspector as _TreeInspector_154f5999, IResolvable as _IResolvable_9ceae33e, IInspectable as _IInspectable_051e6ed8)


@jsii.implements(_IInspectable_051e6ed8)
class CfnCustomDataIdentifier(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_macie.CfnCustomDataIdentifier"):
    """A CloudFormation ``AWS::Macie::CustomDataIdentifier``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-customdataidentifier.html
    cloudformationResource:
    :cloudformationResource:: AWS::Macie::CustomDataIdentifier
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, name: str, regex: str, description: typing.Optional[str]=None, ignore_words: typing.Optional[typing.List[str]]=None, keywords: typing.Optional[typing.List[str]]=None, maximum_match_distance: typing.Optional[jsii.Number]=None) -> None:
        """Create a new ``AWS::Macie::CustomDataIdentifier``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: ``AWS::Macie::CustomDataIdentifier.Name``.
        :param regex: ``AWS::Macie::CustomDataIdentifier.Regex``.
        :param description: ``AWS::Macie::CustomDataIdentifier.Description``.
        :param ignore_words: ``AWS::Macie::CustomDataIdentifier.IgnoreWords``.
        :param keywords: ``AWS::Macie::CustomDataIdentifier.Keywords``.
        :param maximum_match_distance: ``AWS::Macie::CustomDataIdentifier.MaximumMatchDistance``.
        """
        props = CfnCustomDataIdentifierProps(name=name, regex=regex, description=description, ignore_words=ignore_words, keywords=keywords, maximum_match_distance=maximum_match_distance)

        jsii.create(CfnCustomDataIdentifier, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnCustomDataIdentifier":
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
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: CreatedAt
        """
        return jsii.get(self, "attrCreatedAt")

    @builtins.property
    @jsii.member(jsii_name="attrDeleted")
    def attr_deleted(self) -> _IResolvable_9ceae33e:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Deleted
        """
        return jsii.get(self, "attrDeleted")

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Id
        """
        return jsii.get(self, "attrId")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """``AWS::Macie::CustomDataIdentifier.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-customdataidentifier.html#cfn-macie-customdataidentifier-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="regex")
    def regex(self) -> str:
        """``AWS::Macie::CustomDataIdentifier.Regex``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-customdataidentifier.html#cfn-macie-customdataidentifier-regex
        """
        return jsii.get(self, "regex")

    @regex.setter
    def regex(self, value: str) -> None:
        jsii.set(self, "regex", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::Macie::CustomDataIdentifier.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-customdataidentifier.html#cfn-macie-customdataidentifier-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="ignoreWords")
    def ignore_words(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Macie::CustomDataIdentifier.IgnoreWords``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-customdataidentifier.html#cfn-macie-customdataidentifier-ignorewords
        """
        return jsii.get(self, "ignoreWords")

    @ignore_words.setter
    def ignore_words(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "ignoreWords", value)

    @builtins.property
    @jsii.member(jsii_name="keywords")
    def keywords(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Macie::CustomDataIdentifier.Keywords``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-customdataidentifier.html#cfn-macie-customdataidentifier-keywords
        """
        return jsii.get(self, "keywords")

    @keywords.setter
    def keywords(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "keywords", value)

    @builtins.property
    @jsii.member(jsii_name="maximumMatchDistance")
    def maximum_match_distance(self) -> typing.Optional[jsii.Number]:
        """``AWS::Macie::CustomDataIdentifier.MaximumMatchDistance``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-customdataidentifier.html#cfn-macie-customdataidentifier-maximummatchdistance
        """
        return jsii.get(self, "maximumMatchDistance")

    @maximum_match_distance.setter
    def maximum_match_distance(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "maximumMatchDistance", value)


@jsii.data_type(jsii_type="monocdk-experiment.aws_macie.CfnCustomDataIdentifierProps", jsii_struct_bases=[], name_mapping={'name': 'name', 'regex': 'regex', 'description': 'description', 'ignore_words': 'ignoreWords', 'keywords': 'keywords', 'maximum_match_distance': 'maximumMatchDistance'})
class CfnCustomDataIdentifierProps():
    def __init__(self, *, name: str, regex: str, description: typing.Optional[str]=None, ignore_words: typing.Optional[typing.List[str]]=None, keywords: typing.Optional[typing.List[str]]=None, maximum_match_distance: typing.Optional[jsii.Number]=None) -> None:
        """Properties for defining a ``AWS::Macie::CustomDataIdentifier``.

        :param name: ``AWS::Macie::CustomDataIdentifier.Name``.
        :param regex: ``AWS::Macie::CustomDataIdentifier.Regex``.
        :param description: ``AWS::Macie::CustomDataIdentifier.Description``.
        :param ignore_words: ``AWS::Macie::CustomDataIdentifier.IgnoreWords``.
        :param keywords: ``AWS::Macie::CustomDataIdentifier.Keywords``.
        :param maximum_match_distance: ``AWS::Macie::CustomDataIdentifier.MaximumMatchDistance``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-customdataidentifier.html
        """
        self._values = {
            'name': name,
            'regex': regex,
        }
        if description is not None: self._values["description"] = description
        if ignore_words is not None: self._values["ignore_words"] = ignore_words
        if keywords is not None: self._values["keywords"] = keywords
        if maximum_match_distance is not None: self._values["maximum_match_distance"] = maximum_match_distance

    @builtins.property
    def name(self) -> str:
        """``AWS::Macie::CustomDataIdentifier.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-customdataidentifier.html#cfn-macie-customdataidentifier-name
        """
        return self._values.get('name')

    @builtins.property
    def regex(self) -> str:
        """``AWS::Macie::CustomDataIdentifier.Regex``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-customdataidentifier.html#cfn-macie-customdataidentifier-regex
        """
        return self._values.get('regex')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::Macie::CustomDataIdentifier.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-customdataidentifier.html#cfn-macie-customdataidentifier-description
        """
        return self._values.get('description')

    @builtins.property
    def ignore_words(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Macie::CustomDataIdentifier.IgnoreWords``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-customdataidentifier.html#cfn-macie-customdataidentifier-ignorewords
        """
        return self._values.get('ignore_words')

    @builtins.property
    def keywords(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Macie::CustomDataIdentifier.Keywords``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-customdataidentifier.html#cfn-macie-customdataidentifier-keywords
        """
        return self._values.get('keywords')

    @builtins.property
    def maximum_match_distance(self) -> typing.Optional[jsii.Number]:
        """``AWS::Macie::CustomDataIdentifier.MaximumMatchDistance``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-customdataidentifier.html#cfn-macie-customdataidentifier-maximummatchdistance
        """
        return self._values.get('maximum_match_distance')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnCustomDataIdentifierProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnFindingsFilter(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_macie.CfnFindingsFilter"):
    """A CloudFormation ``AWS::Macie::FindingsFilter``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-findingsfilter.html
    cloudformationResource:
    :cloudformationResource:: AWS::Macie::FindingsFilter
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, finding_criteria: typing.Union["FindingCriteriaProperty", _IResolvable_9ceae33e], name: str, action: typing.Optional[str]=None, description: typing.Optional[str]=None, position: typing.Optional[jsii.Number]=None) -> None:
        """Create a new ``AWS::Macie::FindingsFilter``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param finding_criteria: ``AWS::Macie::FindingsFilter.FindingCriteria``.
        :param name: ``AWS::Macie::FindingsFilter.Name``.
        :param action: ``AWS::Macie::FindingsFilter.Action``.
        :param description: ``AWS::Macie::FindingsFilter.Description``.
        :param position: ``AWS::Macie::FindingsFilter.Position``.
        """
        props = CfnFindingsFilterProps(finding_criteria=finding_criteria, name=name, action=action, description=description, position=position)

        jsii.create(CfnFindingsFilter, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnFindingsFilter":
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
    @jsii.member(jsii_name="attrFindingsFilterListItems")
    def attr_findings_filter_list_items(self) -> _IResolvable_9ceae33e:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: FindingsFilterListItems
        """
        return jsii.get(self, "attrFindingsFilterListItems")

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Id
        """
        return jsii.get(self, "attrId")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="findingCriteria")
    def finding_criteria(self) -> typing.Union["FindingCriteriaProperty", _IResolvable_9ceae33e]:
        """``AWS::Macie::FindingsFilter.FindingCriteria``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-findingsfilter.html#cfn-macie-findingsfilter-findingcriteria
        """
        return jsii.get(self, "findingCriteria")

    @finding_criteria.setter
    def finding_criteria(self, value: typing.Union["FindingCriteriaProperty", _IResolvable_9ceae33e]) -> None:
        jsii.set(self, "findingCriteria", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """``AWS::Macie::FindingsFilter.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-findingsfilter.html#cfn-macie-findingsfilter-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> typing.Optional[str]:
        """``AWS::Macie::FindingsFilter.Action``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-findingsfilter.html#cfn-macie-findingsfilter-action
        """
        return jsii.get(self, "action")

    @action.setter
    def action(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "action", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::Macie::FindingsFilter.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-findingsfilter.html#cfn-macie-findingsfilter-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="position")
    def position(self) -> typing.Optional[jsii.Number]:
        """``AWS::Macie::FindingsFilter.Position``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-findingsfilter.html#cfn-macie-findingsfilter-position
        """
        return jsii.get(self, "position")

    @position.setter
    def position(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "position", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_macie.CfnFindingsFilter.CriterionProperty", jsii_struct_bases=[], name_mapping={})
    class CriterionProperty():
        def __init__(self) -> None:
            """
            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-macie-findingsfilter-criterion.html
            """
            self._values = {
            }

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'CriterionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_macie.CfnFindingsFilter.FindingCriteriaProperty", jsii_struct_bases=[], name_mapping={'criterion': 'criterion'})
    class FindingCriteriaProperty():
        def __init__(self, *, criterion: typing.Optional[typing.Union["CfnFindingsFilter.CriterionProperty", _IResolvable_9ceae33e]]=None) -> None:
            """
            :param criterion: ``CfnFindingsFilter.FindingCriteriaProperty.Criterion``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-macie-findingsfilter-findingcriteria.html
            """
            self._values = {
            }
            if criterion is not None: self._values["criterion"] = criterion

        @builtins.property
        def criterion(self) -> typing.Optional[typing.Union["CfnFindingsFilter.CriterionProperty", _IResolvable_9ceae33e]]:
            """``CfnFindingsFilter.FindingCriteriaProperty.Criterion``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-macie-findingsfilter-findingcriteria.html#cfn-macie-findingsfilter-findingcriteria-criterion
            """
            return self._values.get('criterion')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'FindingCriteriaProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_macie.CfnFindingsFilterProps", jsii_struct_bases=[], name_mapping={'finding_criteria': 'findingCriteria', 'name': 'name', 'action': 'action', 'description': 'description', 'position': 'position'})
class CfnFindingsFilterProps():
    def __init__(self, *, finding_criteria: typing.Union["CfnFindingsFilter.FindingCriteriaProperty", _IResolvable_9ceae33e], name: str, action: typing.Optional[str]=None, description: typing.Optional[str]=None, position: typing.Optional[jsii.Number]=None) -> None:
        """Properties for defining a ``AWS::Macie::FindingsFilter``.

        :param finding_criteria: ``AWS::Macie::FindingsFilter.FindingCriteria``.
        :param name: ``AWS::Macie::FindingsFilter.Name``.
        :param action: ``AWS::Macie::FindingsFilter.Action``.
        :param description: ``AWS::Macie::FindingsFilter.Description``.
        :param position: ``AWS::Macie::FindingsFilter.Position``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-findingsfilter.html
        """
        self._values = {
            'finding_criteria': finding_criteria,
            'name': name,
        }
        if action is not None: self._values["action"] = action
        if description is not None: self._values["description"] = description
        if position is not None: self._values["position"] = position

    @builtins.property
    def finding_criteria(self) -> typing.Union["CfnFindingsFilter.FindingCriteriaProperty", _IResolvable_9ceae33e]:
        """``AWS::Macie::FindingsFilter.FindingCriteria``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-findingsfilter.html#cfn-macie-findingsfilter-findingcriteria
        """
        return self._values.get('finding_criteria')

    @builtins.property
    def name(self) -> str:
        """``AWS::Macie::FindingsFilter.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-findingsfilter.html#cfn-macie-findingsfilter-name
        """
        return self._values.get('name')

    @builtins.property
    def action(self) -> typing.Optional[str]:
        """``AWS::Macie::FindingsFilter.Action``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-findingsfilter.html#cfn-macie-findingsfilter-action
        """
        return self._values.get('action')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::Macie::FindingsFilter.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-findingsfilter.html#cfn-macie-findingsfilter-description
        """
        return self._values.get('description')

    @builtins.property
    def position(self) -> typing.Optional[jsii.Number]:
        """``AWS::Macie::FindingsFilter.Position``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-findingsfilter.html#cfn-macie-findingsfilter-position
        """
        return self._values.get('position')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnFindingsFilterProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnSession(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_macie.CfnSession"):
    """A CloudFormation ``AWS::Macie::Session``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-session.html
    cloudformationResource:
    :cloudformationResource:: AWS::Macie::Session
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, finding_publishing_frequency: typing.Optional[str]=None, status: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::Macie::Session``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param finding_publishing_frequency: ``AWS::Macie::Session.FindingPublishingFrequency``.
        :param status: ``AWS::Macie::Session.Status``.
        """
        props = CfnSessionProps(finding_publishing_frequency=finding_publishing_frequency, status=status)

        jsii.create(CfnSession, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnSession":
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
    @jsii.member(jsii_name="attrAwsAccountId")
    def attr_aws_account_id(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: AwsAccountId
        """
        return jsii.get(self, "attrAwsAccountId")

    @builtins.property
    @jsii.member(jsii_name="attrServiceRole")
    def attr_service_role(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: ServiceRole
        """
        return jsii.get(self, "attrServiceRole")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="findingPublishingFrequency")
    def finding_publishing_frequency(self) -> typing.Optional[str]:
        """``AWS::Macie::Session.FindingPublishingFrequency``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-session.html#cfn-macie-session-findingpublishingfrequency
        """
        return jsii.get(self, "findingPublishingFrequency")

    @finding_publishing_frequency.setter
    def finding_publishing_frequency(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "findingPublishingFrequency", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> typing.Optional[str]:
        """``AWS::Macie::Session.Status``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-session.html#cfn-macie-session-status
        """
        return jsii.get(self, "status")

    @status.setter
    def status(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "status", value)


@jsii.data_type(jsii_type="monocdk-experiment.aws_macie.CfnSessionProps", jsii_struct_bases=[], name_mapping={'finding_publishing_frequency': 'findingPublishingFrequency', 'status': 'status'})
class CfnSessionProps():
    def __init__(self, *, finding_publishing_frequency: typing.Optional[str]=None, status: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::Macie::Session``.

        :param finding_publishing_frequency: ``AWS::Macie::Session.FindingPublishingFrequency``.
        :param status: ``AWS::Macie::Session.Status``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-session.html
        """
        self._values = {
        }
        if finding_publishing_frequency is not None: self._values["finding_publishing_frequency"] = finding_publishing_frequency
        if status is not None: self._values["status"] = status

    @builtins.property
    def finding_publishing_frequency(self) -> typing.Optional[str]:
        """``AWS::Macie::Session.FindingPublishingFrequency``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-session.html#cfn-macie-session-findingpublishingfrequency
        """
        return self._values.get('finding_publishing_frequency')

    @builtins.property
    def status(self) -> typing.Optional[str]:
        """``AWS::Macie::Session.Status``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-macie-session.html#cfn-macie-session-status
        """
        return self._values.get('status')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnSessionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "CfnCustomDataIdentifier",
    "CfnCustomDataIdentifierProps",
    "CfnFindingsFilter",
    "CfnFindingsFilterProps",
    "CfnSession",
    "CfnSessionProps",
]

publication.publish()
