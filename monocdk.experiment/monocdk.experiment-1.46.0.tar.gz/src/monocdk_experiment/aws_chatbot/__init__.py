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
class CfnSlackChannelConfiguration(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_chatbot.CfnSlackChannelConfiguration"):
    """A CloudFormation ``AWS::Chatbot::SlackChannelConfiguration``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html
    cloudformationResource:
    :cloudformationResource:: AWS::Chatbot::SlackChannelConfiguration
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, configuration_name: str, iam_role_arn: str, slack_channel_id: str, slack_workspace_id: str, logging_level: typing.Optional[str]=None, sns_topic_arns: typing.Optional[typing.List[str]]=None) -> None:
        """Create a new ``AWS::Chatbot::SlackChannelConfiguration``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param configuration_name: ``AWS::Chatbot::SlackChannelConfiguration.ConfigurationName``.
        :param iam_role_arn: ``AWS::Chatbot::SlackChannelConfiguration.IamRoleArn``.
        :param slack_channel_id: ``AWS::Chatbot::SlackChannelConfiguration.SlackChannelId``.
        :param slack_workspace_id: ``AWS::Chatbot::SlackChannelConfiguration.SlackWorkspaceId``.
        :param logging_level: ``AWS::Chatbot::SlackChannelConfiguration.LoggingLevel``.
        :param sns_topic_arns: ``AWS::Chatbot::SlackChannelConfiguration.SnsTopicArns``.
        """
        props = CfnSlackChannelConfigurationProps(configuration_name=configuration_name, iam_role_arn=iam_role_arn, slack_channel_id=slack_channel_id, slack_workspace_id=slack_workspace_id, logging_level=logging_level, sns_topic_arns=sns_topic_arns)

        jsii.create(CfnSlackChannelConfiguration, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnSlackChannelConfiguration":
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
    @jsii.member(jsii_name="configurationName")
    def configuration_name(self) -> str:
        """``AWS::Chatbot::SlackChannelConfiguration.ConfigurationName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-configurationname
        """
        return jsii.get(self, "configurationName")

    @configuration_name.setter
    def configuration_name(self, value: str) -> None:
        jsii.set(self, "configurationName", value)

    @builtins.property
    @jsii.member(jsii_name="iamRoleArn")
    def iam_role_arn(self) -> str:
        """``AWS::Chatbot::SlackChannelConfiguration.IamRoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-iamrolearn
        """
        return jsii.get(self, "iamRoleArn")

    @iam_role_arn.setter
    def iam_role_arn(self, value: str) -> None:
        jsii.set(self, "iamRoleArn", value)

    @builtins.property
    @jsii.member(jsii_name="slackChannelId")
    def slack_channel_id(self) -> str:
        """``AWS::Chatbot::SlackChannelConfiguration.SlackChannelId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-slackchannelid
        """
        return jsii.get(self, "slackChannelId")

    @slack_channel_id.setter
    def slack_channel_id(self, value: str) -> None:
        jsii.set(self, "slackChannelId", value)

    @builtins.property
    @jsii.member(jsii_name="slackWorkspaceId")
    def slack_workspace_id(self) -> str:
        """``AWS::Chatbot::SlackChannelConfiguration.SlackWorkspaceId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-slackworkspaceid
        """
        return jsii.get(self, "slackWorkspaceId")

    @slack_workspace_id.setter
    def slack_workspace_id(self, value: str) -> None:
        jsii.set(self, "slackWorkspaceId", value)

    @builtins.property
    @jsii.member(jsii_name="loggingLevel")
    def logging_level(self) -> typing.Optional[str]:
        """``AWS::Chatbot::SlackChannelConfiguration.LoggingLevel``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-logginglevel
        """
        return jsii.get(self, "loggingLevel")

    @logging_level.setter
    def logging_level(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "loggingLevel", value)

    @builtins.property
    @jsii.member(jsii_name="snsTopicArns")
    def sns_topic_arns(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Chatbot::SlackChannelConfiguration.SnsTopicArns``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-snstopicarns
        """
        return jsii.get(self, "snsTopicArns")

    @sns_topic_arns.setter
    def sns_topic_arns(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "snsTopicArns", value)


@jsii.data_type(jsii_type="monocdk-experiment.aws_chatbot.CfnSlackChannelConfigurationProps", jsii_struct_bases=[], name_mapping={'configuration_name': 'configurationName', 'iam_role_arn': 'iamRoleArn', 'slack_channel_id': 'slackChannelId', 'slack_workspace_id': 'slackWorkspaceId', 'logging_level': 'loggingLevel', 'sns_topic_arns': 'snsTopicArns'})
class CfnSlackChannelConfigurationProps():
    def __init__(self, *, configuration_name: str, iam_role_arn: str, slack_channel_id: str, slack_workspace_id: str, logging_level: typing.Optional[str]=None, sns_topic_arns: typing.Optional[typing.List[str]]=None) -> None:
        """Properties for defining a ``AWS::Chatbot::SlackChannelConfiguration``.

        :param configuration_name: ``AWS::Chatbot::SlackChannelConfiguration.ConfigurationName``.
        :param iam_role_arn: ``AWS::Chatbot::SlackChannelConfiguration.IamRoleArn``.
        :param slack_channel_id: ``AWS::Chatbot::SlackChannelConfiguration.SlackChannelId``.
        :param slack_workspace_id: ``AWS::Chatbot::SlackChannelConfiguration.SlackWorkspaceId``.
        :param logging_level: ``AWS::Chatbot::SlackChannelConfiguration.LoggingLevel``.
        :param sns_topic_arns: ``AWS::Chatbot::SlackChannelConfiguration.SnsTopicArns``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html
        """
        self._values = {
            'configuration_name': configuration_name,
            'iam_role_arn': iam_role_arn,
            'slack_channel_id': slack_channel_id,
            'slack_workspace_id': slack_workspace_id,
        }
        if logging_level is not None: self._values["logging_level"] = logging_level
        if sns_topic_arns is not None: self._values["sns_topic_arns"] = sns_topic_arns

    @builtins.property
    def configuration_name(self) -> str:
        """``AWS::Chatbot::SlackChannelConfiguration.ConfigurationName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-configurationname
        """
        return self._values.get('configuration_name')

    @builtins.property
    def iam_role_arn(self) -> str:
        """``AWS::Chatbot::SlackChannelConfiguration.IamRoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-iamrolearn
        """
        return self._values.get('iam_role_arn')

    @builtins.property
    def slack_channel_id(self) -> str:
        """``AWS::Chatbot::SlackChannelConfiguration.SlackChannelId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-slackchannelid
        """
        return self._values.get('slack_channel_id')

    @builtins.property
    def slack_workspace_id(self) -> str:
        """``AWS::Chatbot::SlackChannelConfiguration.SlackWorkspaceId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-slackworkspaceid
        """
        return self._values.get('slack_workspace_id')

    @builtins.property
    def logging_level(self) -> typing.Optional[str]:
        """``AWS::Chatbot::SlackChannelConfiguration.LoggingLevel``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-logginglevel
        """
        return self._values.get('logging_level')

    @builtins.property
    def sns_topic_arns(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Chatbot::SlackChannelConfiguration.SnsTopicArns``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-snstopicarns
        """
        return self._values.get('sns_topic_arns')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnSlackChannelConfigurationProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "CfnSlackChannelConfiguration",
    "CfnSlackChannelConfigurationProps",
]

publication.publish()
