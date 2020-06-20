import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *

from .. import (CfnResource as _CfnResource_7760e8e4, Construct as _Construct_f50a3f53, FromCloudFormationOptions as _FromCloudFormationOptions_5f49f6f1, TreeInspector as _TreeInspector_154f5999, IInspectable as _IInspectable_051e6ed8, IResolvable as _IResolvable_9ceae33e, Resource as _Resource_884d0774, IResource as _IResource_72f7ee7e, RemovalPolicy as _RemovalPolicy_5986e9f3)
from ..aws_cloudwatch import (Metric as _Metric_53e89548, MetricOptions as _MetricOptions_ad2c4d5d)
from ..aws_iam import (PolicyStatement as _PolicyStatement_f75dc775, PolicyDocument as _PolicyDocument_1d1bca11, IRole as _IRole_e69bbae4, Grant as _Grant_96af6d2d, IGrantable as _IGrantable_0fcfc53a)


@jsii.implements(_IInspectable_051e6ed8)
class CfnDestination(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_logs.CfnDestination"):
    """A CloudFormation ``AWS::Logs::Destination``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html
    cloudformationResource:
    :cloudformationResource:: AWS::Logs::Destination
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, destination_name: str, destination_policy: str, role_arn: str, target_arn: str) -> None:
        """Create a new ``AWS::Logs::Destination``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param destination_name: ``AWS::Logs::Destination.DestinationName``.
        :param destination_policy: ``AWS::Logs::Destination.DestinationPolicy``.
        :param role_arn: ``AWS::Logs::Destination.RoleArn``.
        :param target_arn: ``AWS::Logs::Destination.TargetArn``.
        """
        props = CfnDestinationProps(destination_name=destination_name, destination_policy=destination_policy, role_arn=role_arn, target_arn=target_arn)

        jsii.create(CfnDestination, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnDestination":
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
    @jsii.member(jsii_name="destinationName")
    def destination_name(self) -> str:
        """``AWS::Logs::Destination.DestinationName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html#cfn-logs-destination-destinationname
        """
        return jsii.get(self, "destinationName")

    @destination_name.setter
    def destination_name(self, value: str) -> None:
        jsii.set(self, "destinationName", value)

    @builtins.property
    @jsii.member(jsii_name="destinationPolicy")
    def destination_policy(self) -> str:
        """``AWS::Logs::Destination.DestinationPolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html#cfn-logs-destination-destinationpolicy
        """
        return jsii.get(self, "destinationPolicy")

    @destination_policy.setter
    def destination_policy(self, value: str) -> None:
        jsii.set(self, "destinationPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> str:
        """``AWS::Logs::Destination.RoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html#cfn-logs-destination-rolearn
        """
        return jsii.get(self, "roleArn")

    @role_arn.setter
    def role_arn(self, value: str) -> None:
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="targetArn")
    def target_arn(self) -> str:
        """``AWS::Logs::Destination.TargetArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html#cfn-logs-destination-targetarn
        """
        return jsii.get(self, "targetArn")

    @target_arn.setter
    def target_arn(self, value: str) -> None:
        jsii.set(self, "targetArn", value)


@jsii.data_type(jsii_type="monocdk-experiment.aws_logs.CfnDestinationProps", jsii_struct_bases=[], name_mapping={'destination_name': 'destinationName', 'destination_policy': 'destinationPolicy', 'role_arn': 'roleArn', 'target_arn': 'targetArn'})
class CfnDestinationProps():
    def __init__(self, *, destination_name: str, destination_policy: str, role_arn: str, target_arn: str) -> None:
        """Properties for defining a ``AWS::Logs::Destination``.

        :param destination_name: ``AWS::Logs::Destination.DestinationName``.
        :param destination_policy: ``AWS::Logs::Destination.DestinationPolicy``.
        :param role_arn: ``AWS::Logs::Destination.RoleArn``.
        :param target_arn: ``AWS::Logs::Destination.TargetArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html
        """
        self._values = {
            'destination_name': destination_name,
            'destination_policy': destination_policy,
            'role_arn': role_arn,
            'target_arn': target_arn,
        }

    @builtins.property
    def destination_name(self) -> str:
        """``AWS::Logs::Destination.DestinationName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html#cfn-logs-destination-destinationname
        """
        return self._values.get('destination_name')

    @builtins.property
    def destination_policy(self) -> str:
        """``AWS::Logs::Destination.DestinationPolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html#cfn-logs-destination-destinationpolicy
        """
        return self._values.get('destination_policy')

    @builtins.property
    def role_arn(self) -> str:
        """``AWS::Logs::Destination.RoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html#cfn-logs-destination-rolearn
        """
        return self._values.get('role_arn')

    @builtins.property
    def target_arn(self) -> str:
        """``AWS::Logs::Destination.TargetArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html#cfn-logs-destination-targetarn
        """
        return self._values.get('target_arn')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnDestinationProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnLogGroup(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_logs.CfnLogGroup"):
    """A CloudFormation ``AWS::Logs::LogGroup``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html
    cloudformationResource:
    :cloudformationResource:: AWS::Logs::LogGroup
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, log_group_name: typing.Optional[str]=None, retention_in_days: typing.Optional[jsii.Number]=None) -> None:
        """Create a new ``AWS::Logs::LogGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param log_group_name: ``AWS::Logs::LogGroup.LogGroupName``.
        :param retention_in_days: ``AWS::Logs::LogGroup.RetentionInDays``.
        """
        props = CfnLogGroupProps(log_group_name=log_group_name, retention_in_days=retention_in_days)

        jsii.create(CfnLogGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnLogGroup":
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
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> typing.Optional[str]:
        """``AWS::Logs::LogGroup.LogGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html#cfn-cwl-loggroup-loggroupname
        """
        return jsii.get(self, "logGroupName")

    @log_group_name.setter
    def log_group_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "logGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="retentionInDays")
    def retention_in_days(self) -> typing.Optional[jsii.Number]:
        """``AWS::Logs::LogGroup.RetentionInDays``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html#cfn-cwl-loggroup-retentionindays
        """
        return jsii.get(self, "retentionInDays")

    @retention_in_days.setter
    def retention_in_days(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "retentionInDays", value)


@jsii.data_type(jsii_type="monocdk-experiment.aws_logs.CfnLogGroupProps", jsii_struct_bases=[], name_mapping={'log_group_name': 'logGroupName', 'retention_in_days': 'retentionInDays'})
class CfnLogGroupProps():
    def __init__(self, *, log_group_name: typing.Optional[str]=None, retention_in_days: typing.Optional[jsii.Number]=None) -> None:
        """Properties for defining a ``AWS::Logs::LogGroup``.

        :param log_group_name: ``AWS::Logs::LogGroup.LogGroupName``.
        :param retention_in_days: ``AWS::Logs::LogGroup.RetentionInDays``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html
        """
        self._values = {
        }
        if log_group_name is not None: self._values["log_group_name"] = log_group_name
        if retention_in_days is not None: self._values["retention_in_days"] = retention_in_days

    @builtins.property
    def log_group_name(self) -> typing.Optional[str]:
        """``AWS::Logs::LogGroup.LogGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html#cfn-cwl-loggroup-loggroupname
        """
        return self._values.get('log_group_name')

    @builtins.property
    def retention_in_days(self) -> typing.Optional[jsii.Number]:
        """``AWS::Logs::LogGroup.RetentionInDays``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html#cfn-cwl-loggroup-retentionindays
        """
        return self._values.get('retention_in_days')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnLogGroupProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnLogStream(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_logs.CfnLogStream"):
    """A CloudFormation ``AWS::Logs::LogStream``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-logstream.html
    cloudformationResource:
    :cloudformationResource:: AWS::Logs::LogStream
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, log_group_name: str, log_stream_name: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::Logs::LogStream``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param log_group_name: ``AWS::Logs::LogStream.LogGroupName``.
        :param log_stream_name: ``AWS::Logs::LogStream.LogStreamName``.
        """
        props = CfnLogStreamProps(log_group_name=log_group_name, log_stream_name=log_stream_name)

        jsii.create(CfnLogStream, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnLogStream":
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
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> str:
        """``AWS::Logs::LogStream.LogGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-logstream.html#cfn-logs-logstream-loggroupname
        """
        return jsii.get(self, "logGroupName")

    @log_group_name.setter
    def log_group_name(self, value: str) -> None:
        jsii.set(self, "logGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="logStreamName")
    def log_stream_name(self) -> typing.Optional[str]:
        """``AWS::Logs::LogStream.LogStreamName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-logstream.html#cfn-logs-logstream-logstreamname
        """
        return jsii.get(self, "logStreamName")

    @log_stream_name.setter
    def log_stream_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "logStreamName", value)


@jsii.data_type(jsii_type="monocdk-experiment.aws_logs.CfnLogStreamProps", jsii_struct_bases=[], name_mapping={'log_group_name': 'logGroupName', 'log_stream_name': 'logStreamName'})
class CfnLogStreamProps():
    def __init__(self, *, log_group_name: str, log_stream_name: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::Logs::LogStream``.

        :param log_group_name: ``AWS::Logs::LogStream.LogGroupName``.
        :param log_stream_name: ``AWS::Logs::LogStream.LogStreamName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-logstream.html
        """
        self._values = {
            'log_group_name': log_group_name,
        }
        if log_stream_name is not None: self._values["log_stream_name"] = log_stream_name

    @builtins.property
    def log_group_name(self) -> str:
        """``AWS::Logs::LogStream.LogGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-logstream.html#cfn-logs-logstream-loggroupname
        """
        return self._values.get('log_group_name')

    @builtins.property
    def log_stream_name(self) -> typing.Optional[str]:
        """``AWS::Logs::LogStream.LogStreamName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-logstream.html#cfn-logs-logstream-logstreamname
        """
        return self._values.get('log_stream_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnLogStreamProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnMetricFilter(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_logs.CfnMetricFilter"):
    """A CloudFormation ``AWS::Logs::MetricFilter``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html
    cloudformationResource:
    :cloudformationResource:: AWS::Logs::MetricFilter
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, filter_pattern: str, log_group_name: str, metric_transformations: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["MetricTransformationProperty", _IResolvable_9ceae33e]]]) -> None:
        """Create a new ``AWS::Logs::MetricFilter``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param filter_pattern: ``AWS::Logs::MetricFilter.FilterPattern``.
        :param log_group_name: ``AWS::Logs::MetricFilter.LogGroupName``.
        :param metric_transformations: ``AWS::Logs::MetricFilter.MetricTransformations``.
        """
        props = CfnMetricFilterProps(filter_pattern=filter_pattern, log_group_name=log_group_name, metric_transformations=metric_transformations)

        jsii.create(CfnMetricFilter, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnMetricFilter":
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
    @jsii.member(jsii_name="filterPattern")
    def filter_pattern(self) -> str:
        """``AWS::Logs::MetricFilter.FilterPattern``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html#cfn-cwl-metricfilter-filterpattern
        """
        return jsii.get(self, "filterPattern")

    @filter_pattern.setter
    def filter_pattern(self, value: str) -> None:
        jsii.set(self, "filterPattern", value)

    @builtins.property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> str:
        """``AWS::Logs::MetricFilter.LogGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html#cfn-cwl-metricfilter-loggroupname
        """
        return jsii.get(self, "logGroupName")

    @log_group_name.setter
    def log_group_name(self, value: str) -> None:
        jsii.set(self, "logGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="metricTransformations")
    def metric_transformations(self) -> typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["MetricTransformationProperty", _IResolvable_9ceae33e]]]:
        """``AWS::Logs::MetricFilter.MetricTransformations``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html#cfn-cwl-metricfilter-metrictransformations
        """
        return jsii.get(self, "metricTransformations")

    @metric_transformations.setter
    def metric_transformations(self, value: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["MetricTransformationProperty", _IResolvable_9ceae33e]]]) -> None:
        jsii.set(self, "metricTransformations", value)

    @jsii.data_type(jsii_type="monocdk-experiment.aws_logs.CfnMetricFilter.MetricTransformationProperty", jsii_struct_bases=[], name_mapping={'metric_name': 'metricName', 'metric_namespace': 'metricNamespace', 'metric_value': 'metricValue', 'default_value': 'defaultValue'})
    class MetricTransformationProperty():
        def __init__(self, *, metric_name: str, metric_namespace: str, metric_value: str, default_value: typing.Optional[jsii.Number]=None) -> None:
            """
            :param metric_name: ``CfnMetricFilter.MetricTransformationProperty.MetricName``.
            :param metric_namespace: ``CfnMetricFilter.MetricTransformationProperty.MetricNamespace``.
            :param metric_value: ``CfnMetricFilter.MetricTransformationProperty.MetricValue``.
            :param default_value: ``CfnMetricFilter.MetricTransformationProperty.DefaultValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-metricfilter-metrictransformation.html
            """
            self._values = {
                'metric_name': metric_name,
                'metric_namespace': metric_namespace,
                'metric_value': metric_value,
            }
            if default_value is not None: self._values["default_value"] = default_value

        @builtins.property
        def metric_name(self) -> str:
            """``CfnMetricFilter.MetricTransformationProperty.MetricName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-metricfilter-metrictransformation.html#cfn-cwl-metricfilter-metrictransformation-metricname
            """
            return self._values.get('metric_name')

        @builtins.property
        def metric_namespace(self) -> str:
            """``CfnMetricFilter.MetricTransformationProperty.MetricNamespace``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-metricfilter-metrictransformation.html#cfn-cwl-metricfilter-metrictransformation-metricnamespace
            """
            return self._values.get('metric_namespace')

        @builtins.property
        def metric_value(self) -> str:
            """``CfnMetricFilter.MetricTransformationProperty.MetricValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-metricfilter-metrictransformation.html#cfn-cwl-metricfilter-metrictransformation-metricvalue
            """
            return self._values.get('metric_value')

        @builtins.property
        def default_value(self) -> typing.Optional[jsii.Number]:
            """``CfnMetricFilter.MetricTransformationProperty.DefaultValue``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-metricfilter-metrictransformation.html#cfn-cwl-metricfilter-metrictransformation-defaultvalue
            """
            return self._values.get('default_value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'MetricTransformationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="monocdk-experiment.aws_logs.CfnMetricFilterProps", jsii_struct_bases=[], name_mapping={'filter_pattern': 'filterPattern', 'log_group_name': 'logGroupName', 'metric_transformations': 'metricTransformations'})
class CfnMetricFilterProps():
    def __init__(self, *, filter_pattern: str, log_group_name: str, metric_transformations: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnMetricFilter.MetricTransformationProperty", _IResolvable_9ceae33e]]]) -> None:
        """Properties for defining a ``AWS::Logs::MetricFilter``.

        :param filter_pattern: ``AWS::Logs::MetricFilter.FilterPattern``.
        :param log_group_name: ``AWS::Logs::MetricFilter.LogGroupName``.
        :param metric_transformations: ``AWS::Logs::MetricFilter.MetricTransformations``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html
        """
        self._values = {
            'filter_pattern': filter_pattern,
            'log_group_name': log_group_name,
            'metric_transformations': metric_transformations,
        }

    @builtins.property
    def filter_pattern(self) -> str:
        """``AWS::Logs::MetricFilter.FilterPattern``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html#cfn-cwl-metricfilter-filterpattern
        """
        return self._values.get('filter_pattern')

    @builtins.property
    def log_group_name(self) -> str:
        """``AWS::Logs::MetricFilter.LogGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html#cfn-cwl-metricfilter-loggroupname
        """
        return self._values.get('log_group_name')

    @builtins.property
    def metric_transformations(self) -> typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnMetricFilter.MetricTransformationProperty", _IResolvable_9ceae33e]]]:
        """``AWS::Logs::MetricFilter.MetricTransformations``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html#cfn-cwl-metricfilter-metrictransformations
        """
        return self._values.get('metric_transformations')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnMetricFilterProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(_IInspectable_051e6ed8)
class CfnSubscriptionFilter(_CfnResource_7760e8e4, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_logs.CfnSubscriptionFilter"):
    """A CloudFormation ``AWS::Logs::SubscriptionFilter``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html
    cloudformationResource:
    :cloudformationResource:: AWS::Logs::SubscriptionFilter
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, destination_arn: str, filter_pattern: str, log_group_name: str, role_arn: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::Logs::SubscriptionFilter``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param destination_arn: ``AWS::Logs::SubscriptionFilter.DestinationArn``.
        :param filter_pattern: ``AWS::Logs::SubscriptionFilter.FilterPattern``.
        :param log_group_name: ``AWS::Logs::SubscriptionFilter.LogGroupName``.
        :param role_arn: ``AWS::Logs::SubscriptionFilter.RoleArn``.
        """
        props = CfnSubscriptionFilterProps(destination_arn=destination_arn, filter_pattern=filter_pattern, log_group_name=log_group_name, role_arn=role_arn)

        jsii.create(CfnSubscriptionFilter, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: _Construct_f50a3f53, id: str, resource_attributes: typing.Any, *, finder: _ICfnFinder_3b168f30) -> "CfnSubscriptionFilter":
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
    @jsii.member(jsii_name="destinationArn")
    def destination_arn(self) -> str:
        """``AWS::Logs::SubscriptionFilter.DestinationArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-cwl-subscriptionfilter-destinationarn
        """
        return jsii.get(self, "destinationArn")

    @destination_arn.setter
    def destination_arn(self, value: str) -> None:
        jsii.set(self, "destinationArn", value)

    @builtins.property
    @jsii.member(jsii_name="filterPattern")
    def filter_pattern(self) -> str:
        """``AWS::Logs::SubscriptionFilter.FilterPattern``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-cwl-subscriptionfilter-filterpattern
        """
        return jsii.get(self, "filterPattern")

    @filter_pattern.setter
    def filter_pattern(self, value: str) -> None:
        jsii.set(self, "filterPattern", value)

    @builtins.property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> str:
        """``AWS::Logs::SubscriptionFilter.LogGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-cwl-subscriptionfilter-loggroupname
        """
        return jsii.get(self, "logGroupName")

    @log_group_name.setter
    def log_group_name(self, value: str) -> None:
        jsii.set(self, "logGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> typing.Optional[str]:
        """``AWS::Logs::SubscriptionFilter.RoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-cwl-subscriptionfilter-rolearn
        """
        return jsii.get(self, "roleArn")

    @role_arn.setter
    def role_arn(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "roleArn", value)


@jsii.data_type(jsii_type="monocdk-experiment.aws_logs.CfnSubscriptionFilterProps", jsii_struct_bases=[], name_mapping={'destination_arn': 'destinationArn', 'filter_pattern': 'filterPattern', 'log_group_name': 'logGroupName', 'role_arn': 'roleArn'})
class CfnSubscriptionFilterProps():
    def __init__(self, *, destination_arn: str, filter_pattern: str, log_group_name: str, role_arn: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::Logs::SubscriptionFilter``.

        :param destination_arn: ``AWS::Logs::SubscriptionFilter.DestinationArn``.
        :param filter_pattern: ``AWS::Logs::SubscriptionFilter.FilterPattern``.
        :param log_group_name: ``AWS::Logs::SubscriptionFilter.LogGroupName``.
        :param role_arn: ``AWS::Logs::SubscriptionFilter.RoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html
        """
        self._values = {
            'destination_arn': destination_arn,
            'filter_pattern': filter_pattern,
            'log_group_name': log_group_name,
        }
        if role_arn is not None: self._values["role_arn"] = role_arn

    @builtins.property
    def destination_arn(self) -> str:
        """``AWS::Logs::SubscriptionFilter.DestinationArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-cwl-subscriptionfilter-destinationarn
        """
        return self._values.get('destination_arn')

    @builtins.property
    def filter_pattern(self) -> str:
        """``AWS::Logs::SubscriptionFilter.FilterPattern``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-cwl-subscriptionfilter-filterpattern
        """
        return self._values.get('filter_pattern')

    @builtins.property
    def log_group_name(self) -> str:
        """``AWS::Logs::SubscriptionFilter.LogGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-cwl-subscriptionfilter-loggroupname
        """
        return self._values.get('log_group_name')

    @builtins.property
    def role_arn(self) -> typing.Optional[str]:
        """``AWS::Logs::SubscriptionFilter.RoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-cwl-subscriptionfilter-rolearn
        """
        return self._values.get('role_arn')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnSubscriptionFilterProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_logs.ColumnRestriction", jsii_struct_bases=[], name_mapping={'comparison': 'comparison', 'number_value': 'numberValue', 'string_value': 'stringValue'})
class ColumnRestriction():
    def __init__(self, *, comparison: str, number_value: typing.Optional[jsii.Number]=None, string_value: typing.Optional[str]=None) -> None:
        """
        :param comparison: Comparison operator to use.
        :param number_value: Number value to compare to. Exactly one of 'stringValue' and 'numberValue' must be set.
        :param string_value: String value to compare to. Exactly one of 'stringValue' and 'numberValue' must be set.

        stability
        :stability: experimental
        """
        self._values = {
            'comparison': comparison,
        }
        if number_value is not None: self._values["number_value"] = number_value
        if string_value is not None: self._values["string_value"] = string_value

    @builtins.property
    def comparison(self) -> str:
        """Comparison operator to use.

        stability
        :stability: experimental
        """
        return self._values.get('comparison')

    @builtins.property
    def number_value(self) -> typing.Optional[jsii.Number]:
        """Number value to compare to.

        Exactly one of 'stringValue' and 'numberValue' must be set.

        stability
        :stability: experimental
        """
        return self._values.get('number_value')

    @builtins.property
    def string_value(self) -> typing.Optional[str]:
        """String value to compare to.

        Exactly one of 'stringValue' and 'numberValue' must be set.

        stability
        :stability: experimental
        """
        return self._values.get('string_value')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ColumnRestriction(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_logs.CrossAccountDestinationProps", jsii_struct_bases=[], name_mapping={'role': 'role', 'target_arn': 'targetArn', 'destination_name': 'destinationName'})
class CrossAccountDestinationProps():
    def __init__(self, *, role: _IRole_e69bbae4, target_arn: str, destination_name: typing.Optional[str]=None) -> None:
        """Properties for a CrossAccountDestination.

        :param role: The role to assume that grants permissions to write to 'target'. The role must be assumable by 'logs.{REGION}.amazonaws.com'.
        :param target_arn: The log destination target's ARN.
        :param destination_name: The name of the log destination. Default: Automatically generated

        stability
        :stability: experimental
        """
        self._values = {
            'role': role,
            'target_arn': target_arn,
        }
        if destination_name is not None: self._values["destination_name"] = destination_name

    @builtins.property
    def role(self) -> _IRole_e69bbae4:
        """The role to assume that grants permissions to write to 'target'.

        The role must be assumable by 'logs.{REGION}.amazonaws.com'.

        stability
        :stability: experimental
        """
        return self._values.get('role')

    @builtins.property
    def target_arn(self) -> str:
        """The log destination target's ARN.

        stability
        :stability: experimental
        """
        return self._values.get('target_arn')

    @builtins.property
    def destination_name(self) -> typing.Optional[str]:
        """The name of the log destination.

        default
        :default: Automatically generated

        stability
        :stability: experimental
        """
        return self._values.get('destination_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CrossAccountDestinationProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class FilterPattern(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_logs.FilterPattern"):
    """A collection of static methods to generate appropriate ILogPatterns.

    stability
    :stability: experimental
    """
    def __init__(self) -> None:
        jsii.create(FilterPattern, self, [])

    @jsii.member(jsii_name="all")
    @builtins.classmethod
    def all(cls, *patterns: "JsonPattern") -> "JsonPattern":
        """A JSON log pattern that matches if all given JSON log patterns match.

        :param patterns: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "all", [*patterns])

    @jsii.member(jsii_name="allEvents")
    @builtins.classmethod
    def all_events(cls) -> "IFilterPattern":
        """A log pattern that matches all events.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "allEvents", [])

    @jsii.member(jsii_name="allTerms")
    @builtins.classmethod
    def all_terms(cls, *terms: str) -> "IFilterPattern":
        """A log pattern that matches if all the strings given appear in the event.

        :param terms: The words to search for. All terms must match.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "allTerms", [*terms])

    @jsii.member(jsii_name="any")
    @builtins.classmethod
    def any(cls, *patterns: "JsonPattern") -> "JsonPattern":
        """A JSON log pattern that matches if any of the given JSON log patterns match.

        :param patterns: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "any", [*patterns])

    @jsii.member(jsii_name="anyTerm")
    @builtins.classmethod
    def any_term(cls, *terms: str) -> "IFilterPattern":
        """A log pattern that matches if any of the strings given appear in the event.

        :param terms: The words to search for. Any terms must match.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "anyTerm", [*terms])

    @jsii.member(jsii_name="anyTermGroup")
    @builtins.classmethod
    def any_term_group(cls, *term_groups: typing.List[str]) -> "IFilterPattern":
        """A log pattern that matches if any of the given term groups matches the event.

        A term group matches an event if all the terms in it appear in the event string.

        :param term_groups: A list of term groups to search for. Any one of the clauses must match.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "anyTermGroup", [*term_groups])

    @jsii.member(jsii_name="booleanValue")
    @builtins.classmethod
    def boolean_value(cls, json_field: str, value: bool) -> "JsonPattern":
        """A JSON log pattern that matches if the field exists and equals the boolean value.

        :param json_field: Field inside JSON. Example: "$.myField"
        :param value: The value to match.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "booleanValue", [json_field, value])

    @jsii.member(jsii_name="exists")
    @builtins.classmethod
    def exists(cls, json_field: str) -> "JsonPattern":
        """A JSON log patter that matches if the field exists.

        This is a readable convenience wrapper over 'field = *'

        :param json_field: Field inside JSON. Example: "$.myField"

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "exists", [json_field])

    @jsii.member(jsii_name="isNull")
    @builtins.classmethod
    def is_null(cls, json_field: str) -> "JsonPattern":
        """A JSON log pattern that matches if the field exists and has the special value 'null'.

        :param json_field: Field inside JSON. Example: "$.myField"

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "isNull", [json_field])

    @jsii.member(jsii_name="literal")
    @builtins.classmethod
    def literal(cls, log_pattern_string: str) -> "IFilterPattern":
        """Use the given string as log pattern.

        See https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html
        for information on writing log patterns.

        :param log_pattern_string: The pattern string to use.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "literal", [log_pattern_string])

    @jsii.member(jsii_name="notExists")
    @builtins.classmethod
    def not_exists(cls, json_field: str) -> "JsonPattern":
        """A JSON log pattern that matches if the field does not exist.

        :param json_field: Field inside JSON. Example: "$.myField"

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "notExists", [json_field])

    @jsii.member(jsii_name="numberValue")
    @builtins.classmethod
    def number_value(cls, json_field: str, comparison: str, value: jsii.Number) -> "JsonPattern":
        """A JSON log pattern that compares numerical values.

        This pattern only matches if the event is a JSON event, and the indicated field inside
        compares with the value in the indicated way.

        Use '$' to indicate the root of the JSON structure. The comparison operator can only
        compare equality or inequality. The '*' wildcard may appear in the value may at the
        start or at the end.

        For more information, see:

        https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html

        :param json_field: Field inside JSON. Example: "$.myField"
        :param comparison: Comparison to carry out. One of =, !=, <, <=, >, >=.
        :param value: The numerical value to compare to.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "numberValue", [json_field, comparison, value])

    @jsii.member(jsii_name="spaceDelimited")
    @builtins.classmethod
    def space_delimited(cls, *columns: str) -> "SpaceDelimitedTextPattern":
        """A space delimited log pattern matcher.

        The log event is divided into space-delimited columns (optionally
        enclosed by "" or [] to capture spaces into column values), and names
        are given to each column.

        '...' may be specified once to match any number of columns.

        Afterwards, conditions may be added to individual columns.

        :param columns: The columns in the space-delimited log stream.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "spaceDelimited", [*columns])

    @jsii.member(jsii_name="stringValue")
    @builtins.classmethod
    def string_value(cls, json_field: str, comparison: str, value: str) -> "JsonPattern":
        """A JSON log pattern that compares string values.

        This pattern only matches if the event is a JSON event, and the indicated field inside
        compares with the string value.

        Use '$' to indicate the root of the JSON structure. The comparison operator can only
        compare equality or inequality. The '*' wildcard may appear in the value may at the
        start or at the end.

        For more information, see:

        https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html

        :param json_field: Field inside JSON. Example: "$.myField"
        :param comparison: Comparison to carry out. Either = or !=.
        :param value: The string value to compare to. May use '*' as wildcard at start or end of string.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "stringValue", [json_field, comparison, value])


@jsii.interface(jsii_type="monocdk-experiment.aws_logs.IFilterPattern")
class IFilterPattern(jsii.compat.Protocol):
    """Interface for objects that can render themselves to log patterns.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IFilterPatternProxy

    @builtins.property
    @jsii.member(jsii_name="logPatternString")
    def log_pattern_string(self) -> str:
        """
        stability
        :stability: experimental
        """
        ...


class _IFilterPatternProxy():
    """Interface for objects that can render themselves to log patterns.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_logs.IFilterPattern"
    @builtins.property
    @jsii.member(jsii_name="logPatternString")
    def log_pattern_string(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "logPatternString")


@jsii.interface(jsii_type="monocdk-experiment.aws_logs.ILogGroup")
class ILogGroup(_IResource_72f7ee7e, jsii.compat.Protocol):
    """
    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ILogGroupProxy

    @builtins.property
    @jsii.member(jsii_name="logGroupArn")
    def log_group_arn(self) -> str:
        """The ARN of this log group, with ':*' appended.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> str:
        """The name of this log group.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @jsii.member(jsii_name="addMetricFilter")
    def add_metric_filter(self, id: str, *, filter_pattern: "IFilterPattern", metric_name: str, metric_namespace: str, default_value: typing.Optional[jsii.Number]=None, metric_value: typing.Optional[str]=None) -> "MetricFilter":
        """Create a new Metric Filter on this Log Group.

        :param id: Unique identifier for the construct in its parent.
        :param filter_pattern: Pattern to search for log events.
        :param metric_name: The name of the metric to emit.
        :param metric_namespace: The namespace of the metric to emit.
        :param default_value: The value to emit if the pattern does not match a particular event. Default: No metric emitted.
        :param metric_value: The value to emit for the metric. Can either be a literal number (typically "1"), or the name of a field in the structure to take the value from the matched event. If you are using a field value, the field value must have been matched using the pattern. If you want to specify a field from a matched JSON structure, use '$.fieldName', and make sure the field is in the pattern (if only as '$.fieldName = *'). If you want to specify a field from a matched space-delimited structure, use '$fieldName'. Default: "1"

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="addStream")
    def add_stream(self, id: str, *, log_stream_name: typing.Optional[str]=None) -> "LogStream":
        """Create a new Log Stream for this Log Group.

        :param id: Unique identifier for the construct in its parent.
        :param log_stream_name: The name of the log stream to create. The name must be unique within the log group. Default: Automatically generated

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="addSubscriptionFilter")
    def add_subscription_filter(self, id: str, *, destination: "ILogSubscriptionDestination", filter_pattern: "IFilterPattern") -> "SubscriptionFilter":
        """Create a new Subscription Filter on this Log Group.

        :param id: Unique identifier for the construct in its parent.
        :param destination: The destination to send the filtered events to. For example, a Kinesis stream or a Lambda function.
        :param filter_pattern: Log events matching this pattern will be sent to the destination.

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="extractMetric")
    def extract_metric(self, json_field: str, metric_namespace: str, metric_name: str) -> _Metric_53e89548:
        """Extract a metric from structured log events in the LogGroup.

        Creates a MetricFilter on this LogGroup that will extract the value
        of the indicated JSON field in all records where it occurs.

        The metric will be available in CloudWatch Metrics under the
        indicated namespace and name.

        :param json_field: JSON field to extract (example: '$.myfield').
        :param metric_namespace: Namespace to emit the metric under.
        :param metric_name: Name to emit the metric under.

        return
        :return: A Metric object representing the extracted metric

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="grant")
    def grant(self, grantee: _IGrantable_0fcfc53a, *actions: str) -> _Grant_96af6d2d:
        """Give the indicated permissions on this log group and all streams.

        :param grantee: -
        :param actions: -

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: _IGrantable_0fcfc53a) -> _Grant_96af6d2d:
        """Give permissions to write to create and write to streams in this log group.

        :param grantee: -

        stability
        :stability: experimental
        """
        ...


class _ILogGroupProxy(jsii.proxy_for(_IResource_72f7ee7e)):
    """
    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_logs.ILogGroup"
    @builtins.property
    @jsii.member(jsii_name="logGroupArn")
    def log_group_arn(self) -> str:
        """The ARN of this log group, with ':*' appended.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "logGroupArn")

    @builtins.property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> str:
        """The name of this log group.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "logGroupName")

    @jsii.member(jsii_name="addMetricFilter")
    def add_metric_filter(self, id: str, *, filter_pattern: "IFilterPattern", metric_name: str, metric_namespace: str, default_value: typing.Optional[jsii.Number]=None, metric_value: typing.Optional[str]=None) -> "MetricFilter":
        """Create a new Metric Filter on this Log Group.

        :param id: Unique identifier for the construct in its parent.
        :param filter_pattern: Pattern to search for log events.
        :param metric_name: The name of the metric to emit.
        :param metric_namespace: The namespace of the metric to emit.
        :param default_value: The value to emit if the pattern does not match a particular event. Default: No metric emitted.
        :param metric_value: The value to emit for the metric. Can either be a literal number (typically "1"), or the name of a field in the structure to take the value from the matched event. If you are using a field value, the field value must have been matched using the pattern. If you want to specify a field from a matched JSON structure, use '$.fieldName', and make sure the field is in the pattern (if only as '$.fieldName = *'). If you want to specify a field from a matched space-delimited structure, use '$fieldName'. Default: "1"

        stability
        :stability: experimental
        """
        props = MetricFilterOptions(filter_pattern=filter_pattern, metric_name=metric_name, metric_namespace=metric_namespace, default_value=default_value, metric_value=metric_value)

        return jsii.invoke(self, "addMetricFilter", [id, props])

    @jsii.member(jsii_name="addStream")
    def add_stream(self, id: str, *, log_stream_name: typing.Optional[str]=None) -> "LogStream":
        """Create a new Log Stream for this Log Group.

        :param id: Unique identifier for the construct in its parent.
        :param log_stream_name: The name of the log stream to create. The name must be unique within the log group. Default: Automatically generated

        stability
        :stability: experimental
        """
        props = StreamOptions(log_stream_name=log_stream_name)

        return jsii.invoke(self, "addStream", [id, props])

    @jsii.member(jsii_name="addSubscriptionFilter")
    def add_subscription_filter(self, id: str, *, destination: "ILogSubscriptionDestination", filter_pattern: "IFilterPattern") -> "SubscriptionFilter":
        """Create a new Subscription Filter on this Log Group.

        :param id: Unique identifier for the construct in its parent.
        :param destination: The destination to send the filtered events to. For example, a Kinesis stream or a Lambda function.
        :param filter_pattern: Log events matching this pattern will be sent to the destination.

        stability
        :stability: experimental
        """
        props = SubscriptionFilterOptions(destination=destination, filter_pattern=filter_pattern)

        return jsii.invoke(self, "addSubscriptionFilter", [id, props])

    @jsii.member(jsii_name="extractMetric")
    def extract_metric(self, json_field: str, metric_namespace: str, metric_name: str) -> _Metric_53e89548:
        """Extract a metric from structured log events in the LogGroup.

        Creates a MetricFilter on this LogGroup that will extract the value
        of the indicated JSON field in all records where it occurs.

        The metric will be available in CloudWatch Metrics under the
        indicated namespace and name.

        :param json_field: JSON field to extract (example: '$.myfield').
        :param metric_namespace: Namespace to emit the metric under.
        :param metric_name: Name to emit the metric under.

        return
        :return: A Metric object representing the extracted metric

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "extractMetric", [json_field, metric_namespace, metric_name])

    @jsii.member(jsii_name="grant")
    def grant(self, grantee: _IGrantable_0fcfc53a, *actions: str) -> _Grant_96af6d2d:
        """Give the indicated permissions on this log group and all streams.

        :param grantee: -
        :param actions: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "grant", [grantee, *actions])

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: _IGrantable_0fcfc53a) -> _Grant_96af6d2d:
        """Give permissions to write to create and write to streams in this log group.

        :param grantee: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "grantWrite", [grantee])


@jsii.interface(jsii_type="monocdk-experiment.aws_logs.ILogStream")
class ILogStream(_IResource_72f7ee7e, jsii.compat.Protocol):
    """
    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ILogStreamProxy

    @builtins.property
    @jsii.member(jsii_name="logStreamName")
    def log_stream_name(self) -> str:
        """The name of this log stream.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...


class _ILogStreamProxy(jsii.proxy_for(_IResource_72f7ee7e)):
    """
    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_logs.ILogStream"
    @builtins.property
    @jsii.member(jsii_name="logStreamName")
    def log_stream_name(self) -> str:
        """The name of this log stream.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "logStreamName")


@jsii.interface(jsii_type="monocdk-experiment.aws_logs.ILogSubscriptionDestination")
class ILogSubscriptionDestination(jsii.compat.Protocol):
    """Interface for classes that can be the destination of a log Subscription.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ILogSubscriptionDestinationProxy

    @jsii.member(jsii_name="bind")
    def bind(self, scope: _Construct_f50a3f53, source_log_group: "ILogGroup") -> "LogSubscriptionDestinationConfig":
        """Return the properties required to send subscription events to this destination.

        If necessary, the destination can use the properties of the SubscriptionFilter
        object itself to configure its permissions to allow the subscription to write
        to it.

        The destination may reconfigure its own permissions in response to this
        function call.

        :param scope: -
        :param source_log_group: -

        stability
        :stability: experimental
        """
        ...


class _ILogSubscriptionDestinationProxy():
    """Interface for classes that can be the destination of a log Subscription.

    stability
    :stability: experimental
    """
    __jsii_type__ = "monocdk-experiment.aws_logs.ILogSubscriptionDestination"
    @jsii.member(jsii_name="bind")
    def bind(self, scope: _Construct_f50a3f53, source_log_group: "ILogGroup") -> "LogSubscriptionDestinationConfig":
        """Return the properties required to send subscription events to this destination.

        If necessary, the destination can use the properties of the SubscriptionFilter
        object itself to configure its permissions to allow the subscription to write
        to it.

        The destination may reconfigure its own permissions in response to this
        function call.

        :param scope: -
        :param source_log_group: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [scope, source_log_group])


@jsii.implements(IFilterPattern)
class JsonPattern(metaclass=jsii.JSIIAbstractClass, jsii_type="monocdk-experiment.aws_logs.JsonPattern"):
    """Base class for patterns that only match JSON log events.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _JsonPatternProxy

    def __init__(self, json_pattern_string: str) -> None:
        """
        :param json_pattern_string: -

        stability
        :stability: experimental
        """
        jsii.create(JsonPattern, self, [json_pattern_string])

    @builtins.property
    @jsii.member(jsii_name="jsonPatternString")
    def json_pattern_string(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "jsonPatternString")

    @builtins.property
    @jsii.member(jsii_name="logPatternString")
    def log_pattern_string(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "logPatternString")


class _JsonPatternProxy(JsonPattern):
    pass

@jsii.implements(ILogGroup)
class LogGroup(_Resource_884d0774, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_logs.LogGroup"):
    """Define a CloudWatch Log Group.

    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, log_group_name: typing.Optional[str]=None, removal_policy: typing.Optional[_RemovalPolicy_5986e9f3]=None, retention: typing.Optional["RetentionDays"]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param log_group_name: Name of the log group. Default: Automatically generated
        :param removal_policy: Determine the removal policy of this log group. Normally you want to retain the log group so you can diagnose issues from logs even after a deployment that no longer includes the log group. In that case, use the normal date-based retention policy to age out your logs. Default: RemovalPolicy.Retain
        :param retention: How long, in days, the log contents will be retained. To retain all logs, set this value to RetentionDays.INFINITE. Default: RetentionDays.TWO_YEARS

        stability
        :stability: experimental
        """
        props = LogGroupProps(log_group_name=log_group_name, removal_policy=removal_policy, retention=retention)

        jsii.create(LogGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromLogGroupArn")
    @builtins.classmethod
    def from_log_group_arn(cls, scope: _Construct_f50a3f53, id: str, log_group_arn: str) -> "ILogGroup":
        """Import an existing LogGroup given its ARN.

        :param scope: -
        :param id: -
        :param log_group_arn: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromLogGroupArn", [scope, id, log_group_arn])

    @jsii.member(jsii_name="fromLogGroupName")
    @builtins.classmethod
    def from_log_group_name(cls, scope: _Construct_f50a3f53, id: str, log_group_name: str) -> "ILogGroup":
        """Import an existing LogGroup given its name.

        :param scope: -
        :param id: -
        :param log_group_name: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromLogGroupName", [scope, id, log_group_name])

    @jsii.member(jsii_name="addMetricFilter")
    def add_metric_filter(self, id: str, *, filter_pattern: "IFilterPattern", metric_name: str, metric_namespace: str, default_value: typing.Optional[jsii.Number]=None, metric_value: typing.Optional[str]=None) -> "MetricFilter":
        """Create a new Metric Filter on this Log Group.

        :param id: Unique identifier for the construct in its parent.
        :param filter_pattern: Pattern to search for log events.
        :param metric_name: The name of the metric to emit.
        :param metric_namespace: The namespace of the metric to emit.
        :param default_value: The value to emit if the pattern does not match a particular event. Default: No metric emitted.
        :param metric_value: The value to emit for the metric. Can either be a literal number (typically "1"), or the name of a field in the structure to take the value from the matched event. If you are using a field value, the field value must have been matched using the pattern. If you want to specify a field from a matched JSON structure, use '$.fieldName', and make sure the field is in the pattern (if only as '$.fieldName = *'). If you want to specify a field from a matched space-delimited structure, use '$fieldName'. Default: "1"

        stability
        :stability: experimental
        """
        props = MetricFilterOptions(filter_pattern=filter_pattern, metric_name=metric_name, metric_namespace=metric_namespace, default_value=default_value, metric_value=metric_value)

        return jsii.invoke(self, "addMetricFilter", [id, props])

    @jsii.member(jsii_name="addStream")
    def add_stream(self, id: str, *, log_stream_name: typing.Optional[str]=None) -> "LogStream":
        """Create a new Log Stream for this Log Group.

        :param id: Unique identifier for the construct in its parent.
        :param log_stream_name: The name of the log stream to create. The name must be unique within the log group. Default: Automatically generated

        stability
        :stability: experimental
        """
        props = StreamOptions(log_stream_name=log_stream_name)

        return jsii.invoke(self, "addStream", [id, props])

    @jsii.member(jsii_name="addSubscriptionFilter")
    def add_subscription_filter(self, id: str, *, destination: "ILogSubscriptionDestination", filter_pattern: "IFilterPattern") -> "SubscriptionFilter":
        """Create a new Subscription Filter on this Log Group.

        :param id: Unique identifier for the construct in its parent.
        :param destination: The destination to send the filtered events to. For example, a Kinesis stream or a Lambda function.
        :param filter_pattern: Log events matching this pattern will be sent to the destination.

        stability
        :stability: experimental
        """
        props = SubscriptionFilterOptions(destination=destination, filter_pattern=filter_pattern)

        return jsii.invoke(self, "addSubscriptionFilter", [id, props])

    @jsii.member(jsii_name="extractMetric")
    def extract_metric(self, json_field: str, metric_namespace: str, metric_name: str) -> _Metric_53e89548:
        """Extract a metric from structured log events in the LogGroup.

        Creates a MetricFilter on this LogGroup that will extract the value
        of the indicated JSON field in all records where it occurs.

        The metric will be available in CloudWatch Metrics under the
        indicated namespace and name.

        :param json_field: JSON field to extract (example: '$.myfield').
        :param metric_namespace: Namespace to emit the metric under.
        :param metric_name: Name to emit the metric under.

        return
        :return: A Metric object representing the extracted metric

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "extractMetric", [json_field, metric_namespace, metric_name])

    @jsii.member(jsii_name="grant")
    def grant(self, grantee: _IGrantable_0fcfc53a, *actions: str) -> _Grant_96af6d2d:
        """Give the indicated permissions on this log group and all streams.

        :param grantee: -
        :param actions: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "grant", [grantee, *actions])

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: _IGrantable_0fcfc53a) -> _Grant_96af6d2d:
        """Give permissions to write to create and write to streams in this log group.

        :param grantee: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "grantWrite", [grantee])

    @builtins.property
    @jsii.member(jsii_name="logGroupArn")
    def log_group_arn(self) -> str:
        """The ARN of this log group.

        stability
        :stability: experimental
        """
        return jsii.get(self, "logGroupArn")

    @builtins.property
    @jsii.member(jsii_name="logGroupName")
    def log_group_name(self) -> str:
        """The name of this log group.

        stability
        :stability: experimental
        """
        return jsii.get(self, "logGroupName")


@jsii.data_type(jsii_type="monocdk-experiment.aws_logs.LogGroupProps", jsii_struct_bases=[], name_mapping={'log_group_name': 'logGroupName', 'removal_policy': 'removalPolicy', 'retention': 'retention'})
class LogGroupProps():
    def __init__(self, *, log_group_name: typing.Optional[str]=None, removal_policy: typing.Optional[_RemovalPolicy_5986e9f3]=None, retention: typing.Optional["RetentionDays"]=None) -> None:
        """Properties for a LogGroup.

        :param log_group_name: Name of the log group. Default: Automatically generated
        :param removal_policy: Determine the removal policy of this log group. Normally you want to retain the log group so you can diagnose issues from logs even after a deployment that no longer includes the log group. In that case, use the normal date-based retention policy to age out your logs. Default: RemovalPolicy.Retain
        :param retention: How long, in days, the log contents will be retained. To retain all logs, set this value to RetentionDays.INFINITE. Default: RetentionDays.TWO_YEARS

        stability
        :stability: experimental
        """
        self._values = {
        }
        if log_group_name is not None: self._values["log_group_name"] = log_group_name
        if removal_policy is not None: self._values["removal_policy"] = removal_policy
        if retention is not None: self._values["retention"] = retention

    @builtins.property
    def log_group_name(self) -> typing.Optional[str]:
        """Name of the log group.

        default
        :default: Automatically generated

        stability
        :stability: experimental
        """
        return self._values.get('log_group_name')

    @builtins.property
    def removal_policy(self) -> typing.Optional[_RemovalPolicy_5986e9f3]:
        """Determine the removal policy of this log group.

        Normally you want to retain the log group so you can diagnose issues
        from logs even after a deployment that no longer includes the log group.
        In that case, use the normal date-based retention policy to age out your
        logs.

        default
        :default: RemovalPolicy.Retain

        stability
        :stability: experimental
        """
        return self._values.get('removal_policy')

    @builtins.property
    def retention(self) -> typing.Optional["RetentionDays"]:
        """How long, in days, the log contents will be retained.

        To retain all logs, set this value to RetentionDays.INFINITE.

        default
        :default: RetentionDays.TWO_YEARS

        stability
        :stability: experimental
        """
        return self._values.get('retention')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LogGroupProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(ILogStream)
class LogStream(_Resource_884d0774, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_logs.LogStream"):
    """Define a Log Stream in a Log Group.

    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, log_group: "ILogGroup", log_stream_name: typing.Optional[str]=None, removal_policy: typing.Optional[_RemovalPolicy_5986e9f3]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param log_group: The log group to create a log stream for.
        :param log_stream_name: The name of the log stream to create. The name must be unique within the log group. Default: Automatically generated
        :param removal_policy: Determine what happens when the log stream resource is removed from the app. Normally you want to retain the log stream so you can diagnose issues from logs even after a deployment that no longer includes the log stream. The date-based retention policy of your log group will age out the logs after a certain time. Default: RemovalPolicy.Retain

        stability
        :stability: experimental
        """
        props = LogStreamProps(log_group=log_group, log_stream_name=log_stream_name, removal_policy=removal_policy)

        jsii.create(LogStream, self, [scope, id, props])

    @jsii.member(jsii_name="fromLogStreamName")
    @builtins.classmethod
    def from_log_stream_name(cls, scope: _Construct_f50a3f53, id: str, log_stream_name: str) -> "ILogStream":
        """Import an existing LogGroup.

        :param scope: -
        :param id: -
        :param log_stream_name: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromLogStreamName", [scope, id, log_stream_name])

    @builtins.property
    @jsii.member(jsii_name="logStreamName")
    def log_stream_name(self) -> str:
        """The name of this log stream.

        stability
        :stability: experimental
        """
        return jsii.get(self, "logStreamName")


@jsii.data_type(jsii_type="monocdk-experiment.aws_logs.LogStreamProps", jsii_struct_bases=[], name_mapping={'log_group': 'logGroup', 'log_stream_name': 'logStreamName', 'removal_policy': 'removalPolicy'})
class LogStreamProps():
    def __init__(self, *, log_group: "ILogGroup", log_stream_name: typing.Optional[str]=None, removal_policy: typing.Optional[_RemovalPolicy_5986e9f3]=None) -> None:
        """Properties for a LogStream.

        :param log_group: The log group to create a log stream for.
        :param log_stream_name: The name of the log stream to create. The name must be unique within the log group. Default: Automatically generated
        :param removal_policy: Determine what happens when the log stream resource is removed from the app. Normally you want to retain the log stream so you can diagnose issues from logs even after a deployment that no longer includes the log stream. The date-based retention policy of your log group will age out the logs after a certain time. Default: RemovalPolicy.Retain

        stability
        :stability: experimental
        """
        self._values = {
            'log_group': log_group,
        }
        if log_stream_name is not None: self._values["log_stream_name"] = log_stream_name
        if removal_policy is not None: self._values["removal_policy"] = removal_policy

    @builtins.property
    def log_group(self) -> "ILogGroup":
        """The log group to create a log stream for.

        stability
        :stability: experimental
        """
        return self._values.get('log_group')

    @builtins.property
    def log_stream_name(self) -> typing.Optional[str]:
        """The name of the log stream to create.

        The name must be unique within the log group.

        default
        :default: Automatically generated

        stability
        :stability: experimental
        """
        return self._values.get('log_stream_name')

    @builtins.property
    def removal_policy(self) -> typing.Optional[_RemovalPolicy_5986e9f3]:
        """Determine what happens when the log stream resource is removed from the app.

        Normally you want to retain the log stream so you can diagnose issues from
        logs even after a deployment that no longer includes the log stream.

        The date-based retention policy of your log group will age out the logs
        after a certain time.

        default
        :default: RemovalPolicy.Retain

        stability
        :stability: experimental
        """
        return self._values.get('removal_policy')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LogStreamProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_logs.LogSubscriptionDestinationConfig", jsii_struct_bases=[], name_mapping={'arn': 'arn', 'role': 'role'})
class LogSubscriptionDestinationConfig():
    def __init__(self, *, arn: str, role: typing.Optional[_IRole_e69bbae4]=None) -> None:
        """Properties returned by a Subscription destination.

        :param arn: The ARN of the subscription's destination.
        :param role: The role to assume to write log events to the destination. Default: No role assumed

        stability
        :stability: experimental
        """
        self._values = {
            'arn': arn,
        }
        if role is not None: self._values["role"] = role

    @builtins.property
    def arn(self) -> str:
        """The ARN of the subscription's destination.

        stability
        :stability: experimental
        """
        return self._values.get('arn')

    @builtins.property
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The role to assume to write log events to the destination.

        default
        :default: No role assumed

        stability
        :stability: experimental
        """
        return self._values.get('role')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LogSubscriptionDestinationConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class MetricFilter(_Resource_884d0774, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_logs.MetricFilter"):
    """A filter that extracts information from CloudWatch Logs and emits to CloudWatch Metrics.

    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, log_group: "ILogGroup", filter_pattern: "IFilterPattern", metric_name: str, metric_namespace: str, default_value: typing.Optional[jsii.Number]=None, metric_value: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param log_group: The log group to create the filter on.
        :param filter_pattern: Pattern to search for log events.
        :param metric_name: The name of the metric to emit.
        :param metric_namespace: The namespace of the metric to emit.
        :param default_value: The value to emit if the pattern does not match a particular event. Default: No metric emitted.
        :param metric_value: The value to emit for the metric. Can either be a literal number (typically "1"), or the name of a field in the structure to take the value from the matched event. If you are using a field value, the field value must have been matched using the pattern. If you want to specify a field from a matched JSON structure, use '$.fieldName', and make sure the field is in the pattern (if only as '$.fieldName = *'). If you want to specify a field from a matched space-delimited structure, use '$fieldName'. Default: "1"

        stability
        :stability: experimental
        """
        props = MetricFilterProps(log_group=log_group, filter_pattern=filter_pattern, metric_name=metric_name, metric_namespace=metric_namespace, default_value=default_value, metric_value=metric_value)

        jsii.create(MetricFilter, self, [scope, id, props])

    @jsii.member(jsii_name="metric")
    def metric(self, *, account: typing.Optional[str]=None, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str, typing.Any]]=None, label: typing.Optional[str]=None, period: typing.Optional[_Duration_5170c158]=None, region: typing.Optional[str]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[_Unit_e1b74f3c]=None) -> _Metric_53e89548:
        """Return the given named metric for this Metric Filter.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: avg over 5 minutes

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(account=account, color=color, dimensions=dimensions, label=label, period=period, region=region, statistic=statistic, unit=unit)

        return jsii.invoke(self, "metric", [props])


@jsii.data_type(jsii_type="monocdk-experiment.aws_logs.MetricFilterOptions", jsii_struct_bases=[], name_mapping={'filter_pattern': 'filterPattern', 'metric_name': 'metricName', 'metric_namespace': 'metricNamespace', 'default_value': 'defaultValue', 'metric_value': 'metricValue'})
class MetricFilterOptions():
    def __init__(self, *, filter_pattern: "IFilterPattern", metric_name: str, metric_namespace: str, default_value: typing.Optional[jsii.Number]=None, metric_value: typing.Optional[str]=None) -> None:
        """Properties for a MetricFilter created from a LogGroup.

        :param filter_pattern: Pattern to search for log events.
        :param metric_name: The name of the metric to emit.
        :param metric_namespace: The namespace of the metric to emit.
        :param default_value: The value to emit if the pattern does not match a particular event. Default: No metric emitted.
        :param metric_value: The value to emit for the metric. Can either be a literal number (typically "1"), or the name of a field in the structure to take the value from the matched event. If you are using a field value, the field value must have been matched using the pattern. If you want to specify a field from a matched JSON structure, use '$.fieldName', and make sure the field is in the pattern (if only as '$.fieldName = *'). If you want to specify a field from a matched space-delimited structure, use '$fieldName'. Default: "1"

        stability
        :stability: experimental
        """
        self._values = {
            'filter_pattern': filter_pattern,
            'metric_name': metric_name,
            'metric_namespace': metric_namespace,
        }
        if default_value is not None: self._values["default_value"] = default_value
        if metric_value is not None: self._values["metric_value"] = metric_value

    @builtins.property
    def filter_pattern(self) -> "IFilterPattern":
        """Pattern to search for log events.

        stability
        :stability: experimental
        """
        return self._values.get('filter_pattern')

    @builtins.property
    def metric_name(self) -> str:
        """The name of the metric to emit.

        stability
        :stability: experimental
        """
        return self._values.get('metric_name')

    @builtins.property
    def metric_namespace(self) -> str:
        """The namespace of the metric to emit.

        stability
        :stability: experimental
        """
        return self._values.get('metric_namespace')

    @builtins.property
    def default_value(self) -> typing.Optional[jsii.Number]:
        """The value to emit if the pattern does not match a particular event.

        default
        :default: No metric emitted.

        stability
        :stability: experimental
        """
        return self._values.get('default_value')

    @builtins.property
    def metric_value(self) -> typing.Optional[str]:
        """The value to emit for the metric.

        Can either be a literal number (typically "1"), or the name of a field in the structure
        to take the value from the matched event. If you are using a field value, the field
        value must have been matched using the pattern.

        If you want to specify a field from a matched JSON structure, use '$.fieldName',
        and make sure the field is in the pattern (if only as '$.fieldName = *').

        If you want to specify a field from a matched space-delimited structure,
        use '$fieldName'.

        default
        :default: "1"

        stability
        :stability: experimental
        """
        return self._values.get('metric_value')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'MetricFilterOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_logs.MetricFilterProps", jsii_struct_bases=[MetricFilterOptions], name_mapping={'filter_pattern': 'filterPattern', 'metric_name': 'metricName', 'metric_namespace': 'metricNamespace', 'default_value': 'defaultValue', 'metric_value': 'metricValue', 'log_group': 'logGroup'})
class MetricFilterProps(MetricFilterOptions):
    def __init__(self, *, filter_pattern: "IFilterPattern", metric_name: str, metric_namespace: str, default_value: typing.Optional[jsii.Number]=None, metric_value: typing.Optional[str]=None, log_group: "ILogGroup") -> None:
        """Properties for a MetricFilter.

        :param filter_pattern: Pattern to search for log events.
        :param metric_name: The name of the metric to emit.
        :param metric_namespace: The namespace of the metric to emit.
        :param default_value: The value to emit if the pattern does not match a particular event. Default: No metric emitted.
        :param metric_value: The value to emit for the metric. Can either be a literal number (typically "1"), or the name of a field in the structure to take the value from the matched event. If you are using a field value, the field value must have been matched using the pattern. If you want to specify a field from a matched JSON structure, use '$.fieldName', and make sure the field is in the pattern (if only as '$.fieldName = *'). If you want to specify a field from a matched space-delimited structure, use '$fieldName'. Default: "1"
        :param log_group: The log group to create the filter on.

        stability
        :stability: experimental
        """
        self._values = {
            'filter_pattern': filter_pattern,
            'metric_name': metric_name,
            'metric_namespace': metric_namespace,
            'log_group': log_group,
        }
        if default_value is not None: self._values["default_value"] = default_value
        if metric_value is not None: self._values["metric_value"] = metric_value

    @builtins.property
    def filter_pattern(self) -> "IFilterPattern":
        """Pattern to search for log events.

        stability
        :stability: experimental
        """
        return self._values.get('filter_pattern')

    @builtins.property
    def metric_name(self) -> str:
        """The name of the metric to emit.

        stability
        :stability: experimental
        """
        return self._values.get('metric_name')

    @builtins.property
    def metric_namespace(self) -> str:
        """The namespace of the metric to emit.

        stability
        :stability: experimental
        """
        return self._values.get('metric_namespace')

    @builtins.property
    def default_value(self) -> typing.Optional[jsii.Number]:
        """The value to emit if the pattern does not match a particular event.

        default
        :default: No metric emitted.

        stability
        :stability: experimental
        """
        return self._values.get('default_value')

    @builtins.property
    def metric_value(self) -> typing.Optional[str]:
        """The value to emit for the metric.

        Can either be a literal number (typically "1"), or the name of a field in the structure
        to take the value from the matched event. If you are using a field value, the field
        value must have been matched using the pattern.

        If you want to specify a field from a matched JSON structure, use '$.fieldName',
        and make sure the field is in the pattern (if only as '$.fieldName = *').

        If you want to specify a field from a matched space-delimited structure,
        use '$fieldName'.

        default
        :default: "1"

        stability
        :stability: experimental
        """
        return self._values.get('metric_value')

    @builtins.property
    def log_group(self) -> "ILogGroup":
        """The log group to create the filter on.

        stability
        :stability: experimental
        """
        return self._values.get('log_group')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'MetricFilterProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="monocdk-experiment.aws_logs.RetentionDays")
class RetentionDays(enum.Enum):
    """How long, in days, the log contents will be retained.

    stability
    :stability: experimental
    """
    ONE_DAY = "ONE_DAY"
    """1 day.

    stability
    :stability: experimental
    """
    THREE_DAYS = "THREE_DAYS"
    """3 days.

    stability
    :stability: experimental
    """
    FIVE_DAYS = "FIVE_DAYS"
    """5 days.

    stability
    :stability: experimental
    """
    ONE_WEEK = "ONE_WEEK"
    """1 week.

    stability
    :stability: experimental
    """
    TWO_WEEKS = "TWO_WEEKS"
    """2 weeks.

    stability
    :stability: experimental
    """
    ONE_MONTH = "ONE_MONTH"
    """1 month.

    stability
    :stability: experimental
    """
    TWO_MONTHS = "TWO_MONTHS"
    """2 months.

    stability
    :stability: experimental
    """
    THREE_MONTHS = "THREE_MONTHS"
    """3 months.

    stability
    :stability: experimental
    """
    FOUR_MONTHS = "FOUR_MONTHS"
    """4 months.

    stability
    :stability: experimental
    """
    FIVE_MONTHS = "FIVE_MONTHS"
    """5 months.

    stability
    :stability: experimental
    """
    SIX_MONTHS = "SIX_MONTHS"
    """6 months.

    stability
    :stability: experimental
    """
    ONE_YEAR = "ONE_YEAR"
    """1 year.

    stability
    :stability: experimental
    """
    THIRTEEN_MONTHS = "THIRTEEN_MONTHS"
    """13 months.

    stability
    :stability: experimental
    """
    EIGHTEEN_MONTHS = "EIGHTEEN_MONTHS"
    """18 months.

    stability
    :stability: experimental
    """
    TWO_YEARS = "TWO_YEARS"
    """2 years.

    stability
    :stability: experimental
    """
    FIVE_YEARS = "FIVE_YEARS"
    """5 years.

    stability
    :stability: experimental
    """
    TEN_YEARS = "TEN_YEARS"
    """10 years.

    stability
    :stability: experimental
    """
    INFINITE = "INFINITE"
    """Retain logs forever.

    stability
    :stability: experimental
    """

@jsii.implements(IFilterPattern)
class SpaceDelimitedTextPattern(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_logs.SpaceDelimitedTextPattern"):
    """Space delimited text pattern.

    stability
    :stability: experimental
    """
    def __init__(self, columns: typing.List[str], restrictions: typing.Mapping[str, typing.List["ColumnRestriction"]]) -> None:
        """
        :param columns: -
        :param restrictions: -

        stability
        :stability: experimental
        """
        jsii.create(SpaceDelimitedTextPattern, self, [columns, restrictions])

    @jsii.member(jsii_name="construct")
    @builtins.classmethod
    def construct(cls, columns: typing.List[str]) -> "SpaceDelimitedTextPattern":
        """Construct a new instance of a space delimited text pattern.

        Since this class must be public, we can't rely on the user only creating it through
        the ``LogPattern.spaceDelimited()`` factory function. We must therefore validate the
        argument in the constructor. Since we're returning a copy on every mutation, and we
        don't want to re-validate the same things on every construction, we provide a limited
        set of mutator functions and only validate the new data every time.

        :param columns: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "construct", [columns])

    @jsii.member(jsii_name="whereNumber")
    def where_number(self, column_name: str, comparison: str, value: jsii.Number) -> "SpaceDelimitedTextPattern":
        """Restrict where the pattern applies.

        :param column_name: -
        :param comparison: -
        :param value: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "whereNumber", [column_name, comparison, value])

    @jsii.member(jsii_name="whereString")
    def where_string(self, column_name: str, comparison: str, value: str) -> "SpaceDelimitedTextPattern":
        """Restrict where the pattern applies.

        :param column_name: -
        :param comparison: -
        :param value: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "whereString", [column_name, comparison, value])

    @builtins.property
    @jsii.member(jsii_name="logPatternString")
    def log_pattern_string(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "logPatternString")


@jsii.data_type(jsii_type="monocdk-experiment.aws_logs.StreamOptions", jsii_struct_bases=[], name_mapping={'log_stream_name': 'logStreamName'})
class StreamOptions():
    def __init__(self, *, log_stream_name: typing.Optional[str]=None) -> None:
        """Properties for a new LogStream created from a LogGroup.

        :param log_stream_name: The name of the log stream to create. The name must be unique within the log group. Default: Automatically generated

        stability
        :stability: experimental
        """
        self._values = {
        }
        if log_stream_name is not None: self._values["log_stream_name"] = log_stream_name

    @builtins.property
    def log_stream_name(self) -> typing.Optional[str]:
        """The name of the log stream to create.

        The name must be unique within the log group.

        default
        :default: Automatically generated

        stability
        :stability: experimental
        """
        return self._values.get('log_stream_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'StreamOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class SubscriptionFilter(_Resource_884d0774, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_logs.SubscriptionFilter"):
    """A new Subscription on a CloudWatch log group.

    stability
    :stability: experimental
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, log_group: "ILogGroup", destination: "ILogSubscriptionDestination", filter_pattern: "IFilterPattern") -> None:
        """
        :param scope: -
        :param id: -
        :param log_group: The log group to create the subscription on.
        :param destination: The destination to send the filtered events to. For example, a Kinesis stream or a Lambda function.
        :param filter_pattern: Log events matching this pattern will be sent to the destination.

        stability
        :stability: experimental
        """
        props = SubscriptionFilterProps(log_group=log_group, destination=destination, filter_pattern=filter_pattern)

        jsii.create(SubscriptionFilter, self, [scope, id, props])


@jsii.data_type(jsii_type="monocdk-experiment.aws_logs.SubscriptionFilterOptions", jsii_struct_bases=[], name_mapping={'destination': 'destination', 'filter_pattern': 'filterPattern'})
class SubscriptionFilterOptions():
    def __init__(self, *, destination: "ILogSubscriptionDestination", filter_pattern: "IFilterPattern") -> None:
        """Properties for a new SubscriptionFilter created from a LogGroup.

        :param destination: The destination to send the filtered events to. For example, a Kinesis stream or a Lambda function.
        :param filter_pattern: Log events matching this pattern will be sent to the destination.

        stability
        :stability: experimental
        """
        self._values = {
            'destination': destination,
            'filter_pattern': filter_pattern,
        }

    @builtins.property
    def destination(self) -> "ILogSubscriptionDestination":
        """The destination to send the filtered events to.

        For example, a Kinesis stream or a Lambda function.

        stability
        :stability: experimental
        """
        return self._values.get('destination')

    @builtins.property
    def filter_pattern(self) -> "IFilterPattern":
        """Log events matching this pattern will be sent to the destination.

        stability
        :stability: experimental
        """
        return self._values.get('filter_pattern')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SubscriptionFilterOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="monocdk-experiment.aws_logs.SubscriptionFilterProps", jsii_struct_bases=[SubscriptionFilterOptions], name_mapping={'destination': 'destination', 'filter_pattern': 'filterPattern', 'log_group': 'logGroup'})
class SubscriptionFilterProps(SubscriptionFilterOptions):
    def __init__(self, *, destination: "ILogSubscriptionDestination", filter_pattern: "IFilterPattern", log_group: "ILogGroup") -> None:
        """Properties for a SubscriptionFilter.

        :param destination: The destination to send the filtered events to. For example, a Kinesis stream or a Lambda function.
        :param filter_pattern: Log events matching this pattern will be sent to the destination.
        :param log_group: The log group to create the subscription on.

        stability
        :stability: experimental
        """
        self._values = {
            'destination': destination,
            'filter_pattern': filter_pattern,
            'log_group': log_group,
        }

    @builtins.property
    def destination(self) -> "ILogSubscriptionDestination":
        """The destination to send the filtered events to.

        For example, a Kinesis stream or a Lambda function.

        stability
        :stability: experimental
        """
        return self._values.get('destination')

    @builtins.property
    def filter_pattern(self) -> "IFilterPattern":
        """Log events matching this pattern will be sent to the destination.

        stability
        :stability: experimental
        """
        return self._values.get('filter_pattern')

    @builtins.property
    def log_group(self) -> "ILogGroup":
        """The log group to create the subscription on.

        stability
        :stability: experimental
        """
        return self._values.get('log_group')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SubscriptionFilterProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(ILogSubscriptionDestination)
class CrossAccountDestination(_Resource_884d0774, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_logs.CrossAccountDestination"):
    """A new CloudWatch Logs Destination for use in cross-account scenarios.

    CrossAccountDestinations are used to subscribe a Kinesis stream in a
    different account to a CloudWatch Subscription.

    Consumers will hardly ever need to use this class. Instead, directly
    subscribe a Kinesis stream using the integration class in the
    ``@aws-cdk/aws-logs-destinations`` package; if necessary, a
    ``CrossAccountDestination`` will be created automatically.

    stability
    :stability: experimental
    resource:
    :resource:: AWS::Logs::Destination
    """
    def __init__(self, scope: _Construct_f50a3f53, id: str, *, role: _IRole_e69bbae4, target_arn: str, destination_name: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param role: The role to assume that grants permissions to write to 'target'. The role must be assumable by 'logs.{REGION}.amazonaws.com'.
        :param target_arn: The log destination target's ARN.
        :param destination_name: The name of the log destination. Default: Automatically generated

        stability
        :stability: experimental
        """
        props = CrossAccountDestinationProps(role=role, target_arn=target_arn, destination_name=destination_name)

        jsii.create(CrossAccountDestination, self, [scope, id, props])

    @jsii.member(jsii_name="addToPolicy")
    def add_to_policy(self, statement: _PolicyStatement_f75dc775) -> None:
        """
        :param statement: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addToPolicy", [statement])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: _Construct_f50a3f53, _source_log_group: "ILogGroup") -> "LogSubscriptionDestinationConfig":
        """Return the properties required to send subscription events to this destination.

        If necessary, the destination can use the properties of the SubscriptionFilter
        object itself to configure its permissions to allow the subscription to write
        to it.

        The destination may reconfigure its own permissions in response to this
        function call.

        :param _scope: -
        :param _source_log_group: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_scope, _source_log_group])

    @builtins.property
    @jsii.member(jsii_name="destinationArn")
    def destination_arn(self) -> str:
        """The ARN of this CrossAccountDestination object.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "destinationArn")

    @builtins.property
    @jsii.member(jsii_name="destinationName")
    def destination_name(self) -> str:
        """The name of this CrossAccountDestination object.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "destinationName")

    @builtins.property
    @jsii.member(jsii_name="policyDocument")
    def policy_document(self) -> _PolicyDocument_1d1bca11:
        """Policy object of this CrossAccountDestination object.

        stability
        :stability: experimental
        """
        return jsii.get(self, "policyDocument")


__all__ = [
    "CfnDestination",
    "CfnDestinationProps",
    "CfnLogGroup",
    "CfnLogGroupProps",
    "CfnLogStream",
    "CfnLogStreamProps",
    "CfnMetricFilter",
    "CfnMetricFilterProps",
    "CfnSubscriptionFilter",
    "CfnSubscriptionFilterProps",
    "ColumnRestriction",
    "CrossAccountDestination",
    "CrossAccountDestinationProps",
    "FilterPattern",
    "IFilterPattern",
    "ILogGroup",
    "ILogStream",
    "ILogSubscriptionDestination",
    "JsonPattern",
    "LogGroup",
    "LogGroupProps",
    "LogStream",
    "LogStreamProps",
    "LogSubscriptionDestinationConfig",
    "MetricFilter",
    "MetricFilterOptions",
    "MetricFilterProps",
    "RetentionDays",
    "SpaceDelimitedTextPattern",
    "StreamOptions",
    "SubscriptionFilter",
    "SubscriptionFilterOptions",
    "SubscriptionFilterProps",
]

publication.publish()
