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
class CfnServer(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_transfer.CfnServer"):
    """A CloudFormation ``AWS::Transfer::Server``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html
    cloudformationResource:
    :cloudformationResource:: AWS::Transfer::Server
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, certificate: typing.Optional[str]=None, endpoint_details: typing.Optional[typing.Union["EndpointDetailsProperty", _IResolvable_9ceae33e]]=None, endpoint_type: typing.Optional[str]=None, identity_provider_details: typing.Optional[typing.Union["IdentityProviderDetailsProperty", _IResolvable_9ceae33e]]=None, identity_provider_type: typing.Optional[str]=None, logging_role: typing.Optional[str]=None, protocols: typing.Optional[typing.List[str]]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None) -> None:
        """Create a new ``AWS::Transfer::Server``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param certificate: ``AWS::Transfer::Server.Certificate``.
        :param endpoint_details: ``AWS::Transfer::Server.EndpointDetails``.
        :param endpoint_type: ``AWS::Transfer::Server.EndpointType``.
        :param identity_provider_details: ``AWS::Transfer::Server.IdentityProviderDetails``.
        :param identity_provider_type: ``AWS::Transfer::Server.IdentityProviderType``.
        :param logging_role: ``AWS::Transfer::Server.LoggingRole``.
        :param protocols: ``AWS::Transfer::Server.Protocols``.
        :param tags: ``AWS::Transfer::Server.Tags``.
        """
        props = CfnServerProps(certificate=certificate, endpoint_details=endpoint_details, endpoint_type=endpoint_type, identity_provider_details=identity_provider_details, identity_provider_type=identity_provider_type, logging_role=logging_role, protocols=protocols, tags=tags)

        jsii.create(CfnServer, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnServer":
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
    @jsii.member(jsii_name="attrServerId")
    def attr_server_id(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: ServerId
        """
        return jsii.get(self, "attrServerId")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::Transfer::Server.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> typing.Optional[str]:
        """``AWS::Transfer::Server.Certificate``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-certificate
        """
        return jsii.get(self, "certificate")

    @certificate.setter
    def certificate(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "certificate", value)

    @builtins.property
    @jsii.member(jsii_name="endpointDetails")
    def endpoint_details(self) -> typing.Optional[typing.Union["EndpointDetailsProperty", _IResolvable_9ceae33e]]:
        """``AWS::Transfer::Server.EndpointDetails``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-endpointdetails
        """
        return jsii.get(self, "endpointDetails")

    @endpoint_details.setter
    def endpoint_details(self, value: typing.Optional[typing.Union["EndpointDetailsProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "endpointDetails", value)

    @builtins.property
    @jsii.member(jsii_name="endpointType")
    def endpoint_type(self) -> typing.Optional[str]:
        """``AWS::Transfer::Server.EndpointType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-endpointtype
        """
        return jsii.get(self, "endpointType")

    @endpoint_type.setter
    def endpoint_type(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "endpointType", value)

    @builtins.property
    @jsii.member(jsii_name="identityProviderDetails")
    def identity_provider_details(self) -> typing.Optional[typing.Union["IdentityProviderDetailsProperty", _IResolvable_9ceae33e]]:
        """``AWS::Transfer::Server.IdentityProviderDetails``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-identityproviderdetails
        """
        return jsii.get(self, "identityProviderDetails")

    @identity_provider_details.setter
    def identity_provider_details(self, value: typing.Optional[typing.Union["IdentityProviderDetailsProperty", _IResolvable_9ceae33e]]) -> None:
        jsii.set(self, "identityProviderDetails", value)

    @builtins.property
    @jsii.member(jsii_name="identityProviderType")
    def identity_provider_type(self) -> typing.Optional[str]:
        """``AWS::Transfer::Server.IdentityProviderType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-identityprovidertype
        """
        return jsii.get(self, "identityProviderType")

    @identity_provider_type.setter
    def identity_provider_type(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "identityProviderType", value)

    @builtins.property
    @jsii.member(jsii_name="loggingRole")
    def logging_role(self) -> typing.Optional[str]:
        """``AWS::Transfer::Server.LoggingRole``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-loggingrole
        """
        return jsii.get(self, "loggingRole")

    @logging_role.setter
    def logging_role(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "loggingRole", value)

    @builtins.property
    @jsii.member(jsii_name="protocols")
    def protocols(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Transfer::Server.Protocols``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-protocols
        """
        return jsii.get(self, "protocols")

    @protocols.setter
    def protocols(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "protocols", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_transfer.CfnServer.EndpointDetailsProperty", jsii_struct_bases=[], name_mapping={'address_allocation_ids': 'addressAllocationIds', 'subnet_ids': 'subnetIds', 'vpc_endpoint_id': 'vpcEndpointId', 'vpc_id': 'vpcId'})
    class EndpointDetailsProperty():
        def __init__(self, *, address_allocation_ids: typing.Optional[typing.List[str]]=None, subnet_ids: typing.Optional[typing.List[str]]=None, vpc_endpoint_id: typing.Optional[str]=None, vpc_id: typing.Optional[str]=None) -> None:
            """
            :param address_allocation_ids: ``CfnServer.EndpointDetailsProperty.AddressAllocationIds``.
            :param subnet_ids: ``CfnServer.EndpointDetailsProperty.SubnetIds``.
            :param vpc_endpoint_id: ``CfnServer.EndpointDetailsProperty.VpcEndpointId``.
            :param vpc_id: ``CfnServer.EndpointDetailsProperty.VpcId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-endpointdetails.html
            """
            self._values = {
            }
            if address_allocation_ids is not None: self._values["address_allocation_ids"] = address_allocation_ids
            if subnet_ids is not None: self._values["subnet_ids"] = subnet_ids
            if vpc_endpoint_id is not None: self._values["vpc_endpoint_id"] = vpc_endpoint_id
            if vpc_id is not None: self._values["vpc_id"] = vpc_id

        @builtins.property
        def address_allocation_ids(self) -> typing.Optional[typing.List[str]]:
            """``CfnServer.EndpointDetailsProperty.AddressAllocationIds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-endpointdetails.html#cfn-transfer-server-endpointdetails-addressallocationids
            """
            return self._values.get('address_allocation_ids')

        @builtins.property
        def subnet_ids(self) -> typing.Optional[typing.List[str]]:
            """``CfnServer.EndpointDetailsProperty.SubnetIds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-endpointdetails.html#cfn-transfer-server-endpointdetails-subnetids
            """
            return self._values.get('subnet_ids')

        @builtins.property
        def vpc_endpoint_id(self) -> typing.Optional[str]:
            """``CfnServer.EndpointDetailsProperty.VpcEndpointId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-endpointdetails.html#cfn-transfer-server-endpointdetails-vpcendpointid
            """
            return self._values.get('vpc_endpoint_id')

        @builtins.property
        def vpc_id(self) -> typing.Optional[str]:
            """``CfnServer.EndpointDetailsProperty.VpcId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-endpointdetails.html#cfn-transfer-server-endpointdetails-vpcid
            """
            return self._values.get('vpc_id')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'EndpointDetailsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="monocdk-experiment.aws_transfer.CfnServer.IdentityProviderDetailsProperty", jsii_struct_bases=[], name_mapping={'invocation_role': 'invocationRole', 'url': 'url'})
    class IdentityProviderDetailsProperty():
        def __init__(self, *, invocation_role: str, url: str) -> None:
            """
            :param invocation_role: ``CfnServer.IdentityProviderDetailsProperty.InvocationRole``.
            :param url: ``CfnServer.IdentityProviderDetailsProperty.Url``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-identityproviderdetails.html
            """
            self._values = {
                'invocation_role': invocation_role,
                'url': url,
            }

        @builtins.property
        def invocation_role(self) -> str:
            """``CfnServer.IdentityProviderDetailsProperty.InvocationRole``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-identityproviderdetails.html#cfn-transfer-server-identityproviderdetails-invocationrole
            """
            return self._values.get('invocation_role')

        @builtins.property
        def url(self) -> str:
            """``CfnServer.IdentityProviderDetailsProperty.Url``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-identityproviderdetails.html#cfn-transfer-server-identityproviderdetails-url
            """
            return self._values.get('url')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'IdentityProviderDetailsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_transfer.CfnServerProps", jsii_struct_bases=[], name_mapping={'certificate': 'certificate', 'endpoint_details': 'endpointDetails', 'endpoint_type': 'endpointType', 'identity_provider_details': 'identityProviderDetails', 'identity_provider_type': 'identityProviderType', 'logging_role': 'loggingRole', 'protocols': 'protocols', 'tags': 'tags'})
class CfnServerProps():
    def __init__(self, *, certificate: typing.Optional[str]=None, endpoint_details: typing.Optional[typing.Union["CfnServer.EndpointDetailsProperty", _IResolvable_9ceae33e]]=None, endpoint_type: typing.Optional[str]=None, identity_provider_details: typing.Optional[typing.Union["CfnServer.IdentityProviderDetailsProperty", _IResolvable_9ceae33e]]=None, identity_provider_type: typing.Optional[str]=None, logging_role: typing.Optional[str]=None, protocols: typing.Optional[typing.List[str]]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None) -> None:
        """Properties for defining a ``AWS::Transfer::Server``.

        :param certificate: ``AWS::Transfer::Server.Certificate``.
        :param endpoint_details: ``AWS::Transfer::Server.EndpointDetails``.
        :param endpoint_type: ``AWS::Transfer::Server.EndpointType``.
        :param identity_provider_details: ``AWS::Transfer::Server.IdentityProviderDetails``.
        :param identity_provider_type: ``AWS::Transfer::Server.IdentityProviderType``.
        :param logging_role: ``AWS::Transfer::Server.LoggingRole``.
        :param protocols: ``AWS::Transfer::Server.Protocols``.
        :param tags: ``AWS::Transfer::Server.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html
        """
        self._values = {
        }
        if certificate is not None: self._values["certificate"] = certificate
        if endpoint_details is not None: self._values["endpoint_details"] = endpoint_details
        if endpoint_type is not None: self._values["endpoint_type"] = endpoint_type
        if identity_provider_details is not None: self._values["identity_provider_details"] = identity_provider_details
        if identity_provider_type is not None: self._values["identity_provider_type"] = identity_provider_type
        if logging_role is not None: self._values["logging_role"] = logging_role
        if protocols is not None: self._values["protocols"] = protocols
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def certificate(self) -> typing.Optional[str]:
        """``AWS::Transfer::Server.Certificate``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-certificate
        """
        return self._values.get('certificate')

    @builtins.property
    def endpoint_details(self) -> typing.Optional[typing.Union["CfnServer.EndpointDetailsProperty", _IResolvable_9ceae33e]]:
        """``AWS::Transfer::Server.EndpointDetails``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-endpointdetails
        """
        return self._values.get('endpoint_details')

    @builtins.property
    def endpoint_type(self) -> typing.Optional[str]:
        """``AWS::Transfer::Server.EndpointType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-endpointtype
        """
        return self._values.get('endpoint_type')

    @builtins.property
    def identity_provider_details(self) -> typing.Optional[typing.Union["CfnServer.IdentityProviderDetailsProperty", _IResolvable_9ceae33e]]:
        """``AWS::Transfer::Server.IdentityProviderDetails``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-identityproviderdetails
        """
        return self._values.get('identity_provider_details')

    @builtins.property
    def identity_provider_type(self) -> typing.Optional[str]:
        """``AWS::Transfer::Server.IdentityProviderType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-identityprovidertype
        """
        return self._values.get('identity_provider_type')

    @builtins.property
    def logging_role(self) -> typing.Optional[str]:
        """``AWS::Transfer::Server.LoggingRole``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-loggingrole
        """
        return self._values.get('logging_role')

    @builtins.property
    def protocols(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Transfer::Server.Protocols``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-protocols
        """
        return self._values.get('protocols')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_b4661f1a]]:
        """``AWS::Transfer::Server.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnServerProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnUser(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_transfer.CfnUser"):
    """A CloudFormation ``AWS::Transfer::User``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html
    cloudformationResource:
    :cloudformationResource:: AWS::Transfer::User
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, role: str, server_id: str, user_name: str, home_directory: typing.Optional[str]=None, home_directory_mappings: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["HomeDirectoryMapEntryProperty", _IResolvable_9ceae33e]]]]=None, home_directory_type: typing.Optional[str]=None, policy: typing.Optional[str]=None, ssh_public_keys: typing.Optional[typing.List[str]]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None) -> None:
        """Create a new ``AWS::Transfer::User``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param role: ``AWS::Transfer::User.Role``.
        :param server_id: ``AWS::Transfer::User.ServerId``.
        :param user_name: ``AWS::Transfer::User.UserName``.
        :param home_directory: ``AWS::Transfer::User.HomeDirectory``.
        :param home_directory_mappings: ``AWS::Transfer::User.HomeDirectoryMappings``.
        :param home_directory_type: ``AWS::Transfer::User.HomeDirectoryType``.
        :param policy: ``AWS::Transfer::User.Policy``.
        :param ssh_public_keys: ``AWS::Transfer::User.SshPublicKeys``.
        :param tags: ``AWS::Transfer::User.Tags``.
        """
        props = CfnUserProps(role=role, server_id=server_id, user_name=user_name, home_directory=home_directory, home_directory_mappings=home_directory_mappings, home_directory_type=home_directory_type, policy=policy, ssh_public_keys=ssh_public_keys, tags=tags)

        jsii.create(CfnUser, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnUser":
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
    @jsii.member(jsii_name="attrServerId")
    def attr_server_id(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: ServerId
        """
        return jsii.get(self, "attrServerId")

    @builtins.property
    @jsii.member(jsii_name="attrUserName")
    def attr_user_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: UserName
        """
        return jsii.get(self, "attrUserName")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::Transfer::User.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> str:
        """``AWS::Transfer::User.Role``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-role
        """
        return jsii.get(self, "role")

    @role.setter
    def role(self, value: str) -> None:
        jsii.set(self, "role", value)

    @builtins.property
    @jsii.member(jsii_name="serverId")
    def server_id(self) -> str:
        """``AWS::Transfer::User.ServerId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-serverid
        """
        return jsii.get(self, "serverId")

    @server_id.setter
    def server_id(self, value: str) -> None:
        jsii.set(self, "serverId", value)

    @builtins.property
    @jsii.member(jsii_name="userName")
    def user_name(self) -> str:
        """``AWS::Transfer::User.UserName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-username
        """
        return jsii.get(self, "userName")

    @user_name.setter
    def user_name(self, value: str) -> None:
        jsii.set(self, "userName", value)

    @builtins.property
    @jsii.member(jsii_name="homeDirectory")
    def home_directory(self) -> typing.Optional[str]:
        """``AWS::Transfer::User.HomeDirectory``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-homedirectory
        """
        return jsii.get(self, "homeDirectory")

    @home_directory.setter
    def home_directory(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "homeDirectory", value)

    @builtins.property
    @jsii.member(jsii_name="homeDirectoryMappings")
    def home_directory_mappings(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["HomeDirectoryMapEntryProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::Transfer::User.HomeDirectoryMappings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-homedirectorymappings
        """
        return jsii.get(self, "homeDirectoryMappings")

    @home_directory_mappings.setter
    def home_directory_mappings(self, value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["HomeDirectoryMapEntryProperty", _IResolvable_9ceae33e]]]]) -> None:
        jsii.set(self, "homeDirectoryMappings", value)

    @builtins.property
    @jsii.member(jsii_name="homeDirectoryType")
    def home_directory_type(self) -> typing.Optional[str]:
        """``AWS::Transfer::User.HomeDirectoryType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-homedirectorytype
        """
        return jsii.get(self, "homeDirectoryType")

    @home_directory_type.setter
    def home_directory_type(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "homeDirectoryType", value)

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(self) -> typing.Optional[str]:
        """``AWS::Transfer::User.Policy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-policy
        """
        return jsii.get(self, "policy")

    @policy.setter
    def policy(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "policy", value)

    @builtins.property
    @jsii.member(jsii_name="sshPublicKeys")
    def ssh_public_keys(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Transfer::User.SshPublicKeys``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-sshpublickeys
        """
        return jsii.get(self, "sshPublicKeys")

    @ssh_public_keys.setter
    def ssh_public_keys(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "sshPublicKeys", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_transfer.CfnUser.HomeDirectoryMapEntryProperty", jsii_struct_bases=[], name_mapping={'entry': 'entry', 'target': 'target'})
    class HomeDirectoryMapEntryProperty():
        def __init__(self, *, entry: str, target: str) -> None:
            """
            :param entry: ``CfnUser.HomeDirectoryMapEntryProperty.Entry``.
            :param target: ``CfnUser.HomeDirectoryMapEntryProperty.Target``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-user-homedirectorymapentry.html
            """
            self._values = {
                'entry': entry,
                'target': target,
            }

        @builtins.property
        def entry(self) -> str:
            """``CfnUser.HomeDirectoryMapEntryProperty.Entry``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-user-homedirectorymapentry.html#cfn-transfer-user-homedirectorymapentry-entry
            """
            return self._values.get('entry')

        @builtins.property
        def target(self) -> str:
            """``CfnUser.HomeDirectoryMapEntryProperty.Target``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-user-homedirectorymapentry.html#cfn-transfer-user-homedirectorymapentry-target
            """
            return self._values.get('target')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'HomeDirectoryMapEntryProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_transfer.CfnUserProps", jsii_struct_bases=[], name_mapping={'role': 'role', 'server_id': 'serverId', 'user_name': 'userName', 'home_directory': 'homeDirectory', 'home_directory_mappings': 'homeDirectoryMappings', 'home_directory_type': 'homeDirectoryType', 'policy': 'policy', 'ssh_public_keys': 'sshPublicKeys', 'tags': 'tags'})
class CfnUserProps():
    def __init__(self, *, role: str, server_id: str, user_name: str, home_directory: typing.Optional[str]=None, home_directory_mappings: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnUser.HomeDirectoryMapEntryProperty", _IResolvable_9ceae33e]]]]=None, home_directory_type: typing.Optional[str]=None, policy: typing.Optional[str]=None, ssh_public_keys: typing.Optional[typing.List[str]]=None, tags: typing.Optional[typing.List[_CfnTag_b4661f1a]]=None) -> None:
        """Properties for defining a ``AWS::Transfer::User``.

        :param role: ``AWS::Transfer::User.Role``.
        :param server_id: ``AWS::Transfer::User.ServerId``.
        :param user_name: ``AWS::Transfer::User.UserName``.
        :param home_directory: ``AWS::Transfer::User.HomeDirectory``.
        :param home_directory_mappings: ``AWS::Transfer::User.HomeDirectoryMappings``.
        :param home_directory_type: ``AWS::Transfer::User.HomeDirectoryType``.
        :param policy: ``AWS::Transfer::User.Policy``.
        :param ssh_public_keys: ``AWS::Transfer::User.SshPublicKeys``.
        :param tags: ``AWS::Transfer::User.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html
        """
        self._values = {
            'role': role,
            'server_id': server_id,
            'user_name': user_name,
        }
        if home_directory is not None: self._values["home_directory"] = home_directory
        if home_directory_mappings is not None: self._values["home_directory_mappings"] = home_directory_mappings
        if home_directory_type is not None: self._values["home_directory_type"] = home_directory_type
        if policy is not None: self._values["policy"] = policy
        if ssh_public_keys is not None: self._values["ssh_public_keys"] = ssh_public_keys
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def role(self) -> str:
        """``AWS::Transfer::User.Role``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-role
        """
        return self._values.get('role')

    @builtins.property
    def server_id(self) -> str:
        """``AWS::Transfer::User.ServerId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-serverid
        """
        return self._values.get('server_id')

    @builtins.property
    def user_name(self) -> str:
        """``AWS::Transfer::User.UserName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-username
        """
        return self._values.get('user_name')

    @builtins.property
    def home_directory(self) -> typing.Optional[str]:
        """``AWS::Transfer::User.HomeDirectory``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-homedirectory
        """
        return self._values.get('home_directory')

    @builtins.property
    def home_directory_mappings(self) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnUser.HomeDirectoryMapEntryProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::Transfer::User.HomeDirectoryMappings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-homedirectorymappings
        """
        return self._values.get('home_directory_mappings')

    @builtins.property
    def home_directory_type(self) -> typing.Optional[str]:
        """``AWS::Transfer::User.HomeDirectoryType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-homedirectorytype
        """
        return self._values.get('home_directory_type')

    @builtins.property
    def policy(self) -> typing.Optional[str]:
        """``AWS::Transfer::User.Policy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-policy
        """
        return self._values.get('policy')

    @builtins.property
    def ssh_public_keys(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Transfer::User.SshPublicKeys``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-sshpublickeys
        """
        return self._values.get('ssh_public_keys')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_b4661f1a]]:
        """``AWS::Transfer::User.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnUserProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "CfnServer",
    "CfnServerProps",
    "CfnUser",
    "CfnUserProps",
]

publication.publish()
