import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *

from .. import (CfnResource as _CfnResource_7760e8e4, Construct as _Construct_f50a3f53, FromCloudFormationOptions as _FromCloudFormationOptions_5f49f6f1, TreeInspector as _TreeInspector_154f5999, IInspectable as _IInspectable_051e6ed8)


@jsii.implements(_IInspectable_051e6ed8)
class CfnGraph(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_detective.CfnGraph"):
    """A CloudFormation ``AWS::Detective::Graph``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-graph.html
    cloudformationResource:
    :cloudformationResource:: AWS::Detective::Graph
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str) -> None:
        """Create a new ``AWS::Detective::Graph``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        """
        jsii.create(CfnGraph, self, [scope, id])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnGraph":
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


@jsii.implements(_IInspectable_051e6ed8)
class CfnMemberInvitation(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_detective.CfnMemberInvitation"):
    """A CloudFormation ``AWS::Detective::MemberInvitation``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-memberinvitation.html
    cloudformationResource:
    :cloudformationResource:: AWS::Detective::MemberInvitation
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, graph_arn: str, member_email_address: str, member_id: str, message: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::Detective::MemberInvitation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param graph_arn: ``AWS::Detective::MemberInvitation.GraphArn``.
        :param member_email_address: ``AWS::Detective::MemberInvitation.MemberEmailAddress``.
        :param member_id: ``AWS::Detective::MemberInvitation.MemberId``.
        :param message: ``AWS::Detective::MemberInvitation.Message``.
        """
        props = CfnMemberInvitationProps(graph_arn=graph_arn, member_email_address=member_email_address, member_id=member_id, message=message)

        jsii.create(CfnMemberInvitation, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnMemberInvitation":
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
    @jsii.member(jsii_name="graphArn")
    def graph_arn(self) -> str:
        """``AWS::Detective::MemberInvitation.GraphArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-memberinvitation.html#cfn-detective-memberinvitation-grapharn
        """
        return jsii.get(self, "graphArn")

    @graph_arn.setter
    def graph_arn(self, value: str) -> None:
        jsii.set(self, "graphArn", value)

    @builtins.property
    @jsii.member(jsii_name="memberEmailAddress")
    def member_email_address(self) -> str:
        """``AWS::Detective::MemberInvitation.MemberEmailAddress``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-memberinvitation.html#cfn-detective-memberinvitation-memberemailaddress
        """
        return jsii.get(self, "memberEmailAddress")

    @member_email_address.setter
    def member_email_address(self, value: str) -> None:
        jsii.set(self, "memberEmailAddress", value)

    @builtins.property
    @jsii.member(jsii_name="memberId")
    def member_id(self) -> str:
        """``AWS::Detective::MemberInvitation.MemberId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-memberinvitation.html#cfn-detective-memberinvitation-memberid
        """
        return jsii.get(self, "memberId")

    @member_id.setter
    def member_id(self, value: str) -> None:
        jsii.set(self, "memberId", value)

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> typing.Optional[str]:
        """``AWS::Detective::MemberInvitation.Message``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-memberinvitation.html#cfn-detective-memberinvitation-message
        """
        return jsii.get(self, "message")

    @message.setter
    def message(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "message", value)


@jsii.data_type(jsii_type="monocdk-experiment.aws_detective.CfnMemberInvitationProps", jsii_struct_bases=[], name_mapping={'graph_arn': 'graphArn', 'member_email_address': 'memberEmailAddress', 'member_id': 'memberId', 'message': 'message'})
class CfnMemberInvitationProps():
    def __init__(self, *, graph_arn: str, member_email_address: str, member_id: str, message: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::Detective::MemberInvitation``.

        :param graph_arn: ``AWS::Detective::MemberInvitation.GraphArn``.
        :param member_email_address: ``AWS::Detective::MemberInvitation.MemberEmailAddress``.
        :param member_id: ``AWS::Detective::MemberInvitation.MemberId``.
        :param message: ``AWS::Detective::MemberInvitation.Message``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-memberinvitation.html
        """
        self._values = {
            'graph_arn': graph_arn,
            'member_email_address': member_email_address,
            'member_id': member_id,
        }
        if message is not None: self._values["message"] = message

    @builtins.property
    def graph_arn(self) -> str:
        """``AWS::Detective::MemberInvitation.GraphArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-memberinvitation.html#cfn-detective-memberinvitation-grapharn
        """
        return self._values.get('graph_arn')

    @builtins.property
    def member_email_address(self) -> str:
        """``AWS::Detective::MemberInvitation.MemberEmailAddress``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-memberinvitation.html#cfn-detective-memberinvitation-memberemailaddress
        """
        return self._values.get('member_email_address')

    @builtins.property
    def member_id(self) -> str:
        """``AWS::Detective::MemberInvitation.MemberId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-memberinvitation.html#cfn-detective-memberinvitation-memberid
        """
        return self._values.get('member_id')

    @builtins.property
    def message(self) -> typing.Optional[str]:
        """``AWS::Detective::MemberInvitation.Message``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-memberinvitation.html#cfn-detective-memberinvitation-message
        """
        return self._values.get('message')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnMemberInvitationProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "CfnGraph",
    "CfnMemberInvitation",
    "CfnMemberInvitationProps",
]

publication.publish()
