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
class CfnResourceShare(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_ram.CfnResourceShare"):
    """A CloudFormation ``AWS::RAM::ResourceShare``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html
    cloudformationResource:
    :cloudformationResource:: AWS::RAM::ResourceShare
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, name: str, allow_external_principals: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, principals: typing.Optional[typing.List[str]]=None, resource_arns: typing.Optional[typing.List[str]]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None) -> None:
        """Create a new ``AWS::RAM::ResourceShare``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: ``AWS::RAM::ResourceShare.Name``.
        :param allow_external_principals: ``AWS::RAM::ResourceShare.AllowExternalPrincipals``.
        :param principals: ``AWS::RAM::ResourceShare.Principals``.
        :param resource_arns: ``AWS::RAM::ResourceShare.ResourceArns``.
        :param tags: ``AWS::RAM::ResourceShare.Tags``.
        """
        props = CfnResourceShareProps(name=name, allow_external_principals=allow_external_principals, principals=principals, resource_arns=resource_arns, tags=tags)

        jsii.create(CfnResourceShare, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnResourceShare":
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
        """``AWS::RAM::ResourceShare.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """``AWS::RAM::ResourceShare.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="allowExternalPrincipals")
    def allow_external_principals(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::RAM::ResourceShare.AllowExternalPrincipals``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-allowexternalprincipals
        """
        return jsii.get(self, "allowExternalPrincipals")

    @allow_external_principals.setter
    def allow_external_principals(self, value: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "allowExternalPrincipals", value)

    @builtins.property
    @jsii.member(jsii_name="principals")
    def principals(self) -> typing.Optional[typing.List[str]]:
        """``AWS::RAM::ResourceShare.Principals``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-principals
        """
        return jsii.get(self, "principals")

    @principals.setter
    def principals(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "principals", value)

    @builtins.property
    @jsii.member(jsii_name="resourceArns")
    def resource_arns(self) -> typing.Optional[typing.List[str]]:
        """``AWS::RAM::ResourceShare.ResourceArns``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-resourcearns
        """
        return jsii.get(self, "resourceArns")

    @resource_arns.setter
    def resource_arns(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "resourceArns", value)


@jsii.data_type(jsii_type="monocdk-experiment.aws_ram.CfnResourceShareProps", jsii_struct_bases=[], name_mapping={'name': 'name', 'allow_external_principals': 'allowExternalPrincipals', 'principals': 'principals', 'resource_arns': 'resourceArns', 'tags': 'tags'})
class CfnResourceShareProps():
    def __init__(self, *, name: str, allow_external_principals: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]=None, principals: typing.Optional[typing.List[str]]=None, resource_arns: typing.Optional[typing.List[str]]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None) -> None:
        """Properties for defining a ``AWS::RAM::ResourceShare``.

        :param name: ``AWS::RAM::ResourceShare.Name``.
        :param allow_external_principals: ``AWS::RAM::ResourceShare.AllowExternalPrincipals``.
        :param principals: ``AWS::RAM::ResourceShare.Principals``.
        :param resource_arns: ``AWS::RAM::ResourceShare.ResourceArns``.
        :param tags: ``AWS::RAM::ResourceShare.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html
        """
        self._values = {
            'name': name,
        }
        if allow_external_principals is not None: self._values["allow_external_principals"] = allow_external_principals
        if principals is not None: self._values["principals"] = principals
        if resource_arns is not None: self._values["resource_arns"] = resource_arns
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def name(self) -> str:
        """``AWS::RAM::ResourceShare.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-name
        """
        return self._values.get('name')

    @builtins.property
    def allow_external_principals(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::RAM::ResourceShare.AllowExternalPrincipals``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-allowexternalprincipals
        """
        return self._values.get('allow_external_principals')

    @builtins.property
    def principals(self) -> typing.Optional[typing.List[str]]:
        """``AWS::RAM::ResourceShare.Principals``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-principals
        """
        return self._values.get('principals')

    @builtins.property
    def resource_arns(self) -> typing.Optional[typing.List[str]]:
        """``AWS::RAM::ResourceShare.ResourceArns``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-resourcearns
        """
        return self._values.get('resource_arns')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_b4661f1a]]:
        """``AWS::RAM::ResourceShare.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnResourceShareProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "CfnResourceShare",
    "CfnResourceShareProps",
]

publication.publish()
