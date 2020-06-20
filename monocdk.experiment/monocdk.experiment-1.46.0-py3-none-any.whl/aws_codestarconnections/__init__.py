import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *

from .. import (CfnResource as _CfnResource_7760e8e4, Construct as _Construct_f50a3f53, FromCloudFormationOptions as _FromCloudFormationOptions_5f49f6f1, TreeInspector as _TreeInspector_154f5999, TagManager as _TagManager_2508893f, IInspectable as _IInspectable_051e6ed8, CfnTag as _CfnTag_b4661f1a)


@jsii.implements(_IInspectable_051e6ed8)
class CfnConnection(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_codestarconnections.CfnConnection"):
    """A CloudFormation ``AWS::CodeStarConnections::Connection``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarconnections-connection.html
    cloudformationResource:
    :cloudformationResource:: AWS::CodeStarConnections::Connection
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, connection_name: str, provider_type: str, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None) -> None:
        """Create a new ``AWS::CodeStarConnections::Connection``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param connection_name: ``AWS::CodeStarConnections::Connection.ConnectionName``.
        :param provider_type: ``AWS::CodeStarConnections::Connection.ProviderType``.
        :param tags: ``AWS::CodeStarConnections::Connection.Tags``.
        """
        props = CfnConnectionProps(connection_name=connection_name, provider_type=provider_type, tags=tags)

        jsii.create(CfnConnection, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnConnection":
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
    @jsii.member(jsii_name="attrConnectionArn")
    def attr_connection_arn(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: ConnectionArn
        """
        return jsii.get(self, "attrConnectionArn")

    @builtins.property
    @jsii.member(jsii_name="attrConnectionStatus")
    def attr_connection_status(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: ConnectionStatus
        """
        return jsii.get(self, "attrConnectionStatus")

    @builtins.property
    @jsii.member(jsii_name="attrOwnerAccountId")
    def attr_owner_account_id(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: OwnerAccountId
        """
        return jsii.get(self, "attrOwnerAccountId")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::CodeStarConnections::Connection.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarconnections-connection.html#cfn-codestarconnections-connection-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="connectionName")
    def connection_name(self) -> str:
        """``AWS::CodeStarConnections::Connection.ConnectionName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarconnections-connection.html#cfn-codestarconnections-connection-connectionname
        """
        return jsii.get(self, "connectionName")

    @connection_name.setter
    def connection_name(self, value: str) -> None:
        jsii.set(self, "connectionName", value)

    @builtins.property
    @jsii.member(jsii_name="providerType")
    def provider_type(self) -> str:
        """``AWS::CodeStarConnections::Connection.ProviderType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarconnections-connection.html#cfn-codestarconnections-connection-providertype
        """
        return jsii.get(self, "providerType")

    @provider_type.setter
    def provider_type(self, value: str) -> None:
        jsii.set(self, "providerType", value)


@jsii.data_type(jsii_type="monocdk-experiment.aws_codestarconnections.CfnConnectionProps", jsii_struct_bases=[], name_mapping={'connection_name': 'connectionName', 'provider_type': 'providerType', 'tags': 'tags'})
class CfnConnectionProps():
    def __init__(self, *, connection_name: str, provider_type: str, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None) -> None:
        """Properties for defining a ``AWS::CodeStarConnections::Connection``.

        :param connection_name: ``AWS::CodeStarConnections::Connection.ConnectionName``.
        :param provider_type: ``AWS::CodeStarConnections::Connection.ProviderType``.
        :param tags: ``AWS::CodeStarConnections::Connection.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarconnections-connection.html
        """
        self._values = {
            'connection_name': connection_name,
            'provider_type': provider_type,
        }
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def connection_name(self) -> str:
        """``AWS::CodeStarConnections::Connection.ConnectionName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarconnections-connection.html#cfn-codestarconnections-connection-connectionname
        """
        return self._values.get('connection_name')

    @builtins.property
    def provider_type(self) -> str:
        """``AWS::CodeStarConnections::Connection.ProviderType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarconnections-connection.html#cfn-codestarconnections-connection-providertype
        """
        return self._values.get('provider_type')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_b4661f1a]]:
        """``AWS::CodeStarConnections::Connection.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestarconnections-connection.html#cfn-codestarconnections-connection-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnConnectionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "CfnConnection",
    "CfnConnectionProps",
]

publication.publish()
