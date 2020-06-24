"""
## AWS::CE Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_ce as ce
```
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

import aws_cdk.core


@jsii.implements(aws_cdk.core.IInspectable)
class CfnCostCategory(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ce.CfnCostCategory"):
    """A CloudFormation ``AWS::CE::CostCategory``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-costcategory.html
    cloudformationResource:
    :cloudformationResource:: AWS::CE::CostCategory
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, name: str, rules: str, rule_version: str) -> None:
        """Create a new ``AWS::CE::CostCategory``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: ``AWS::CE::CostCategory.Name``.
        :param rules: ``AWS::CE::CostCategory.Rules``.
        :param rule_version: ``AWS::CE::CostCategory.RuleVersion``.
        """
        props = CfnCostCategoryProps(name=name, rules=rules, rule_version=rule_version)

        jsii.create(CfnCostCategory, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnCostCategory":
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
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Arn
        """
        return jsii.get(self, "attrArn")

    @builtins.property
    @jsii.member(jsii_name="attrEffectiveStart")
    def attr_effective_start(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: EffectiveStart
        """
        return jsii.get(self, "attrEffectiveStart")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """``AWS::CE::CostCategory.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-costcategory.html#cfn-ce-costcategory-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="rules")
    def rules(self) -> str:
        """``AWS::CE::CostCategory.Rules``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-costcategory.html#cfn-ce-costcategory-rules
        """
        return jsii.get(self, "rules")

    @rules.setter
    def rules(self, value: str) -> None:
        jsii.set(self, "rules", value)

    @builtins.property
    @jsii.member(jsii_name="ruleVersion")
    def rule_version(self) -> str:
        """``AWS::CE::CostCategory.RuleVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-costcategory.html#cfn-ce-costcategory-ruleversion
        """
        return jsii.get(self, "ruleVersion")

    @rule_version.setter
    def rule_version(self, value: str) -> None:
        jsii.set(self, "ruleVersion", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-ce.CfnCostCategoryProps", jsii_struct_bases=[], name_mapping={'name': 'name', 'rules': 'rules', 'rule_version': 'ruleVersion'})
class CfnCostCategoryProps():
    def __init__(self, *, name: str, rules: str, rule_version: str) -> None:
        """Properties for defining a ``AWS::CE::CostCategory``.

        :param name: ``AWS::CE::CostCategory.Name``.
        :param rules: ``AWS::CE::CostCategory.Rules``.
        :param rule_version: ``AWS::CE::CostCategory.RuleVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-costcategory.html
        """
        self._values = {
            'name': name,
            'rules': rules,
            'rule_version': rule_version,
        }

    @builtins.property
    def name(self) -> str:
        """``AWS::CE::CostCategory.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-costcategory.html#cfn-ce-costcategory-name
        """
        return self._values.get('name')

    @builtins.property
    def rules(self) -> str:
        """``AWS::CE::CostCategory.Rules``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-costcategory.html#cfn-ce-costcategory-rules
        """
        return self._values.get('rules')

    @builtins.property
    def rule_version(self) -> str:
        """``AWS::CE::CostCategory.RuleVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ce-costcategory.html#cfn-ce-costcategory-ruleversion
        """
        return self._values.get('rule_version')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnCostCategoryProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "CfnCostCategory",
    "CfnCostCategoryProps",
]

publication.publish()
