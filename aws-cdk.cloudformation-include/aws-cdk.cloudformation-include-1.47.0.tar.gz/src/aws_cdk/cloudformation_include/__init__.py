"""
# Include CloudFormation templates in the CDK

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development. They are subject to non-backward compatible changes or removal in any future version. These are not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be announced in the release notes. This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

This module contains a set of classes whose goal is to facilitate working
with existing CloudFormation templates in the CDK.
It can be thought of as an extension of the capabilities of the
[`CfnInclude` class](../@aws-cdk/core/lib/cfn-include.ts).

## Basic usage

Assume we have a file `my-template.json`, that contains the following CloudFormation template:

```json
{
  "Resources": {
    "Bucket": {
      "Type": "AWS::S3::Bucket",
      "Properties": {
        "BucketName": "some-bucket-name"
      }
    }
  }
}
```

It can be included in a CDK application with the following code:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.cloudformation_include as cfn_inc

cfn_template = cfn_inc.CfnInclude(self, "Template",
    template_file="my-template.json"
)
```

This will add all resources from `my-template.json` into the CDK application,
preserving their original logical IDs from the template file.

Any resource from the included template can be retrieved by referring to it by its logical ID from the template.
If you know the class of the CDK object that corresponds to that resource,
you can cast the returned object to the correct type:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_s3 as s3

cfn_bucket = cfn_template.get_resource("Bucket")
```

Any modifications made to that resource will be reflected in the resulting CDK template;
for example, the name of the bucket can be changed:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cfn_bucket.bucket_name = "my-bucket-name"
```

You can also refer to the resource when defining other constructs,
including the higher-level ones
(those whose name does not start with `Cfn`),
for example:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_iam as iam

role = iam.Role(self, "Role",
    assumed_by=iam.AnyPrincipal()
)
role.add_to_policy(iam.PolicyStatement(
    actions=["s3:*"],
    resources=[cfn_bucket.attr_arn]
))
```

If you need, you can also convert the CloudFormation resource to a higher-level
resource by importing it by its name:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
bucket = s3.Bucket.from_bucket_name(self, "L2Bucket", cfn_bucket.ref)
```

## Conditions

If your template uses [CloudFormation Conditions](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/conditions-section-structure.html),
you can retrieve them from your template:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.core as core

condition = cfn_template.get_condition("MyCondition")
```

The `CfnCondition` object is mutable,
and any changes you make to it will be reflected in the resulting template:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
condition.expression = core.Fn.condition_equals(1, 2)
```

## Known limitations

This module is still in its early, experimental stage,
and so does not implement all features of CloudFormation templates.
All items unchecked below are currently not supported.

### Ability to retrieve CloudFormation objects from the template:

* [x] Resources
* [x] Parameters
* [x] Conditions
* [ ] Outputs

### [Resource attributes](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-product-attribute-reference.html):

* [x] Properties
* [x] Condition
* [x] DependsOn
* [x] CreationPolicy
* [x] UpdatePolicy
* [x] UpdateReplacePolicy
* [x] DeletionPolicy
* [x] Metadata

### [CloudFormation functions](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference.html):

* [x] Ref
* [x] Fn::GetAtt
* [x] Fn::Join
* [x] Fn::If
* [x] Fn::And
* [x] Fn::Equals
* [x] Fn::Not
* [x] Fn::Or
* [x] Fn::Base64
* [x] Fn::Cidr
* [x] Fn::FindInMap
* [x] Fn::GetAZs
* [x] Fn::ImportValue
* [x] Fn::Select
* [x] Fn::Split
* [ ] Fn::Sub
* [x] Fn::Transform
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


class CfnInclude(aws_cdk.core.CfnElement, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/cloudformation-include.CfnInclude"):
    """Construct to import an existing CloudFormation template file into a CDK application.

    All resources defined in the template file can be retrieved by calling the {@link getResource} method.
    Any modifications made on the returned resource objects will be reflected in the resulting CDK template.

    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, template_file: str) -> None:
        """
        :param scope: -
        :param id: -
        :param template_file: Path to the template file. Currently, only JSON templates are supported.

        stability
        :stability: experimental
        """
        props = CfnIncludeProps(template_file=template_file)

        jsii.create(CfnInclude, self, [scope, id, props])

    @jsii.member(jsii_name="getCondition")
    def get_condition(self, condition_name: str) -> aws_cdk.core.CfnCondition:
        """Returns the CfnCondition object from the 'Conditions' section of the CloudFormation template with the given name.

        Any modifications performed on that object will be reflected in the resulting CDK template.

        If a Condition with the given name is not present in the template,
        throws an exception.

        :param condition_name: the name of the Condition in the CloudFormation template file.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getCondition", [condition_name])

    @jsii.member(jsii_name="getParameter")
    def get_parameter(self, parameter_name: str) -> aws_cdk.core.CfnParameter:
        """Returns the CfnParameter object from the 'Parameters' section of the included template Any modifications performed on that object will be reflected in the resulting CDK template.

        If a Parameter with the given name is not present in the template,
        throws an exception.

        :param parameter_name: the name of the parameter to retrieve.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getParameter", [parameter_name])

    @jsii.member(jsii_name="getResource")
    def get_resource(self, logical_id: str) -> aws_cdk.core.CfnResource:
        """Returns the low-level CfnResource from the template with the given logical ID.

        Any modifications performed on that resource will be reflected in the resulting CDK template.

        The returned object will be of the proper underlying class;
        you can always cast it to the correct type in your code::

            // assume the template contains an AWS::S3::Bucket with logical ID 'Bucket'
            const cfnBucket = cfnTemplate.getResource('Bucket') as s3.CfnBucket;
            // cfnBucket is of type s3.CfnBucket

        If the template does not contain a resource with the given logical ID,
        an exception will be thrown.

        :param logical_id: the logical ID of the resource in the CloudFormation template file.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getResource", [logical_id])


@jsii.data_type(jsii_type="@aws-cdk/cloudformation-include.CfnIncludeProps", jsii_struct_bases=[], name_mapping={'template_file': 'templateFile'})
class CfnIncludeProps():
    def __init__(self, *, template_file: str) -> None:
        """Construction properties of {@link CfnInclude}.

        :param template_file: Path to the template file. Currently, only JSON templates are supported.

        stability
        :stability: experimental
        """
        self._values = {
            'template_file': template_file,
        }

    @builtins.property
    def template_file(self) -> str:
        """Path to the template file.

        Currently, only JSON templates are supported.

        stability
        :stability: experimental
        """
        return self._values.get('template_file')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnIncludeProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "CfnInclude",
    "CfnIncludeProps",
]

publication.publish()
