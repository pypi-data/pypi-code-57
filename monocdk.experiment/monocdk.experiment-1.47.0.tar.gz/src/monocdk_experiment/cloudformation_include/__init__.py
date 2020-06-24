import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *

from .. import (CfnElement as _CfnElement_54343cf1, Construct as _Construct_f50a3f53, CfnCondition as _CfnCondition_548166d0, CfnParameter as _CfnParameter_90f1d0df, CfnResource as _CfnResource_7760e8e4)


class CfnInclude(_CfnElement_54343cf1, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.cloudformation_include.CfnInclude"):
    """Construct to import an existing CloudFormation template file into a CDK application.

    All resources defined in the template file can be retrieved by calling the {@link getResource} method.
    Any modifications made on the returned resource objects will be reflected in the resulting CDK template.

    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, template_file: str) -> None:
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
    def get_condition(self, condition_name: str) -> _CfnCondition_548166d0:
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
    def get_parameter(self, parameter_name: str) -> _CfnParameter_90f1d0df:
        """Returns the CfnParameter object from the 'Parameters' section of the included template Any modifications performed on that object will be reflected in the resulting CDK template.

        If a Parameter with the given name is not present in the template,
        throws an exception.

        :param parameter_name: the name of the parameter to retrieve.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getParameter", [parameter_name])

    @jsii.member(jsii_name="getResource")
    def get_resource(self, logical_id: str) -> _CfnResource_7760e8e4:
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


@jsii.data_type(jsii_type="monocdk-experiment.cloudformation_include.CfnIncludeProps", jsii_struct_bases=[], name_mapping={'template_file': 'templateFile'})
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
