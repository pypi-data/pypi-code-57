"""
## AWS::Synthetics Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_synthetics as synthetics
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
class CfnCanary(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-synthetics.CfnCanary"):
    """A CloudFormation ``AWS::Synthetics::Canary``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html
    cloudformationResource:
    :cloudformationResource:: AWS::Synthetics::Canary
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, artifact_s3_location: str, code: typing.Union["CodeProperty", aws_cdk.core.IResolvable], execution_role_arn: str, name: str, run_config: typing.Union[aws_cdk.core.IResolvable, "RunConfigProperty"], runtime_version: str, schedule: typing.Union[aws_cdk.core.IResolvable, "ScheduleProperty"], start_canary_after_creation: typing.Union[bool, aws_cdk.core.IResolvable], failure_retention_period: typing.Optional[jsii.Number]=None, success_retention_period: typing.Optional[jsii.Number]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, vpc_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "VPCConfigProperty"]]=None) -> None:
        """Create a new ``AWS::Synthetics::Canary``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param artifact_s3_location: ``AWS::Synthetics::Canary.ArtifactS3Location``.
        :param code: ``AWS::Synthetics::Canary.Code``.
        :param execution_role_arn: ``AWS::Synthetics::Canary.ExecutionRoleArn``.
        :param name: ``AWS::Synthetics::Canary.Name``.
        :param run_config: ``AWS::Synthetics::Canary.RunConfig``.
        :param runtime_version: ``AWS::Synthetics::Canary.RuntimeVersion``.
        :param schedule: ``AWS::Synthetics::Canary.Schedule``.
        :param start_canary_after_creation: ``AWS::Synthetics::Canary.StartCanaryAfterCreation``.
        :param failure_retention_period: ``AWS::Synthetics::Canary.FailureRetentionPeriod``.
        :param success_retention_period: ``AWS::Synthetics::Canary.SuccessRetentionPeriod``.
        :param tags: ``AWS::Synthetics::Canary.Tags``.
        :param vpc_config: ``AWS::Synthetics::Canary.VPCConfig``.
        """
        props = CfnCanaryProps(artifact_s3_location=artifact_s3_location, code=code, execution_role_arn=execution_role_arn, name=name, run_config=run_config, runtime_version=runtime_version, schedule=schedule, start_canary_after_creation=start_canary_after_creation, failure_retention_period=failure_retention_period, success_retention_period=success_retention_period, tags=tags, vpc_config=vpc_config)

        jsii.create(CfnCanary, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnCanary":
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
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Id
        """
        return jsii.get(self, "attrId")

    @builtins.property
    @jsii.member(jsii_name="attrState")
    def attr_state(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: State
        """
        return jsii.get(self, "attrState")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::Synthetics::Canary.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="artifactS3Location")
    def artifact_s3_location(self) -> str:
        """``AWS::Synthetics::Canary.ArtifactS3Location``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-artifacts3location
        """
        return jsii.get(self, "artifactS3Location")

    @artifact_s3_location.setter
    def artifact_s3_location(self, value: str) -> None:
        jsii.set(self, "artifactS3Location", value)

    @builtins.property
    @jsii.member(jsii_name="code")
    def code(self) -> typing.Union["CodeProperty", aws_cdk.core.IResolvable]:
        """``AWS::Synthetics::Canary.Code``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-code
        """
        return jsii.get(self, "code")

    @code.setter
    def code(self, value: typing.Union["CodeProperty", aws_cdk.core.IResolvable]) -> None:
        jsii.set(self, "code", value)

    @builtins.property
    @jsii.member(jsii_name="executionRoleArn")
    def execution_role_arn(self) -> str:
        """``AWS::Synthetics::Canary.ExecutionRoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-executionrolearn
        """
        return jsii.get(self, "executionRoleArn")

    @execution_role_arn.setter
    def execution_role_arn(self, value: str) -> None:
        jsii.set(self, "executionRoleArn", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """``AWS::Synthetics::Canary.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="runConfig")
    def run_config(self) -> typing.Union[aws_cdk.core.IResolvable, "RunConfigProperty"]:
        """``AWS::Synthetics::Canary.RunConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-runconfig
        """
        return jsii.get(self, "runConfig")

    @run_config.setter
    def run_config(self, value: typing.Union[aws_cdk.core.IResolvable, "RunConfigProperty"]) -> None:
        jsii.set(self, "runConfig", value)

    @builtins.property
    @jsii.member(jsii_name="runtimeVersion")
    def runtime_version(self) -> str:
        """``AWS::Synthetics::Canary.RuntimeVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-runtimeversion
        """
        return jsii.get(self, "runtimeVersion")

    @runtime_version.setter
    def runtime_version(self, value: str) -> None:
        jsii.set(self, "runtimeVersion", value)

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> typing.Union[aws_cdk.core.IResolvable, "ScheduleProperty"]:
        """``AWS::Synthetics::Canary.Schedule``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-schedule
        """
        return jsii.get(self, "schedule")

    @schedule.setter
    def schedule(self, value: typing.Union[aws_cdk.core.IResolvable, "ScheduleProperty"]) -> None:
        jsii.set(self, "schedule", value)

    @builtins.property
    @jsii.member(jsii_name="startCanaryAfterCreation")
    def start_canary_after_creation(self) -> typing.Union[bool, aws_cdk.core.IResolvable]:
        """``AWS::Synthetics::Canary.StartCanaryAfterCreation``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-startcanaryaftercreation
        """
        return jsii.get(self, "startCanaryAfterCreation")

    @start_canary_after_creation.setter
    def start_canary_after_creation(self, value: typing.Union[bool, aws_cdk.core.IResolvable]) -> None:
        jsii.set(self, "startCanaryAfterCreation", value)

    @builtins.property
    @jsii.member(jsii_name="failureRetentionPeriod")
    def failure_retention_period(self) -> typing.Optional[jsii.Number]:
        """``AWS::Synthetics::Canary.FailureRetentionPeriod``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-failureretentionperiod
        """
        return jsii.get(self, "failureRetentionPeriod")

    @failure_retention_period.setter
    def failure_retention_period(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "failureRetentionPeriod", value)

    @builtins.property
    @jsii.member(jsii_name="successRetentionPeriod")
    def success_retention_period(self) -> typing.Optional[jsii.Number]:
        """``AWS::Synthetics::Canary.SuccessRetentionPeriod``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-successretentionperiod
        """
        return jsii.get(self, "successRetentionPeriod")

    @success_retention_period.setter
    def success_retention_period(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "successRetentionPeriod", value)

    @builtins.property
    @jsii.member(jsii_name="vpcConfig")
    def vpc_config(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "VPCConfigProperty"]]:
        """``AWS::Synthetics::Canary.VPCConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-vpcconfig
        """
        return jsii.get(self, "vpcConfig")

    @vpc_config.setter
    def vpc_config(self, value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "VPCConfigProperty"]]) -> None:
        jsii.set(self, "vpcConfig", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-synthetics.CfnCanary.CodeProperty", jsii_struct_bases=[], name_mapping={'handler': 'handler', 's3_bucket': 's3Bucket', 's3_key': 's3Key', 's3_object_version': 's3ObjectVersion', 'script': 'script'})
    class CodeProperty():
        def __init__(self, *, handler: typing.Optional[str]=None, s3_bucket: typing.Optional[str]=None, s3_key: typing.Optional[str]=None, s3_object_version: typing.Optional[str]=None, script: typing.Optional[str]=None) -> None:
            """
            :param handler: ``CfnCanary.CodeProperty.Handler``.
            :param s3_bucket: ``CfnCanary.CodeProperty.S3Bucket``.
            :param s3_key: ``CfnCanary.CodeProperty.S3Key``.
            :param s3_object_version: ``CfnCanary.CodeProperty.S3ObjectVersion``.
            :param script: ``CfnCanary.CodeProperty.Script``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-code.html
            """
            self._values = {
            }
            if handler is not None: self._values["handler"] = handler
            if s3_bucket is not None: self._values["s3_bucket"] = s3_bucket
            if s3_key is not None: self._values["s3_key"] = s3_key
            if s3_object_version is not None: self._values["s3_object_version"] = s3_object_version
            if script is not None: self._values["script"] = script

        @builtins.property
        def handler(self) -> typing.Optional[str]:
            """``CfnCanary.CodeProperty.Handler``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-code.html#cfn-synthetics-canary-code-handler
            """
            return self._values.get('handler')

        @builtins.property
        def s3_bucket(self) -> typing.Optional[str]:
            """``CfnCanary.CodeProperty.S3Bucket``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-code.html#cfn-synthetics-canary-code-s3bucket
            """
            return self._values.get('s3_bucket')

        @builtins.property
        def s3_key(self) -> typing.Optional[str]:
            """``CfnCanary.CodeProperty.S3Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-code.html#cfn-synthetics-canary-code-s3key
            """
            return self._values.get('s3_key')

        @builtins.property
        def s3_object_version(self) -> typing.Optional[str]:
            """``CfnCanary.CodeProperty.S3ObjectVersion``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-code.html#cfn-synthetics-canary-code-s3objectversion
            """
            return self._values.get('s3_object_version')

        @builtins.property
        def script(self) -> typing.Optional[str]:
            """``CfnCanary.CodeProperty.Script``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-code.html#cfn-synthetics-canary-code-script
            """
            return self._values.get('script')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'CodeProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-synthetics.CfnCanary.RunConfigProperty", jsii_struct_bases=[], name_mapping={'timeout_in_seconds': 'timeoutInSeconds'})
    class RunConfigProperty():
        def __init__(self, *, timeout_in_seconds: jsii.Number) -> None:
            """
            :param timeout_in_seconds: ``CfnCanary.RunConfigProperty.TimeoutInSeconds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-runconfig.html
            """
            self._values = {
                'timeout_in_seconds': timeout_in_seconds,
            }

        @builtins.property
        def timeout_in_seconds(self) -> jsii.Number:
            """``CfnCanary.RunConfigProperty.TimeoutInSeconds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-runconfig.html#cfn-synthetics-canary-runconfig-timeoutinseconds
            """
            return self._values.get('timeout_in_seconds')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'RunConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-synthetics.CfnCanary.ScheduleProperty", jsii_struct_bases=[], name_mapping={'duration_in_seconds': 'durationInSeconds', 'expression': 'expression'})
    class ScheduleProperty():
        def __init__(self, *, duration_in_seconds: str, expression: str) -> None:
            """
            :param duration_in_seconds: ``CfnCanary.ScheduleProperty.DurationInSeconds``.
            :param expression: ``CfnCanary.ScheduleProperty.Expression``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-schedule.html
            """
            self._values = {
                'duration_in_seconds': duration_in_seconds,
                'expression': expression,
            }

        @builtins.property
        def duration_in_seconds(self) -> str:
            """``CfnCanary.ScheduleProperty.DurationInSeconds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-schedule.html#cfn-synthetics-canary-schedule-durationinseconds
            """
            return self._values.get('duration_in_seconds')

        @builtins.property
        def expression(self) -> str:
            """``CfnCanary.ScheduleProperty.Expression``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-schedule.html#cfn-synthetics-canary-schedule-expression
            """
            return self._values.get('expression')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ScheduleProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-synthetics.CfnCanary.VPCConfigProperty", jsii_struct_bases=[], name_mapping={'security_group_ids': 'securityGroupIds', 'subnet_ids': 'subnetIds', 'vpc_id': 'vpcId'})
    class VPCConfigProperty():
        def __init__(self, *, security_group_ids: typing.List[str], subnet_ids: typing.List[str], vpc_id: typing.Optional[str]=None) -> None:
            """
            :param security_group_ids: ``CfnCanary.VPCConfigProperty.SecurityGroupIds``.
            :param subnet_ids: ``CfnCanary.VPCConfigProperty.SubnetIds``.
            :param vpc_id: ``CfnCanary.VPCConfigProperty.VpcId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-vpcconfig.html
            """
            self._values = {
                'security_group_ids': security_group_ids,
                'subnet_ids': subnet_ids,
            }
            if vpc_id is not None: self._values["vpc_id"] = vpc_id

        @builtins.property
        def security_group_ids(self) -> typing.List[str]:
            """``CfnCanary.VPCConfigProperty.SecurityGroupIds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-vpcconfig.html#cfn-synthetics-canary-vpcconfig-securitygroupids
            """
            return self._values.get('security_group_ids')

        @builtins.property
        def subnet_ids(self) -> typing.List[str]:
            """``CfnCanary.VPCConfigProperty.SubnetIds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-vpcconfig.html#cfn-synthetics-canary-vpcconfig-subnetids
            """
            return self._values.get('subnet_ids')

        @builtins.property
        def vpc_id(self) -> typing.Optional[str]:
            """``CfnCanary.VPCConfigProperty.VpcId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-vpcconfig.html#cfn-synthetics-canary-vpcconfig-vpcid
            """
            return self._values.get('vpc_id')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'VPCConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-synthetics.CfnCanaryProps", jsii_struct_bases=[], name_mapping={'artifact_s3_location': 'artifactS3Location', 'code': 'code', 'execution_role_arn': 'executionRoleArn', 'name': 'name', 'run_config': 'runConfig', 'runtime_version': 'runtimeVersion', 'schedule': 'schedule', 'start_canary_after_creation': 'startCanaryAfterCreation', 'failure_retention_period': 'failureRetentionPeriod', 'success_retention_period': 'successRetentionPeriod', 'tags': 'tags', 'vpc_config': 'vpcConfig'})
class CfnCanaryProps():
    def __init__(self, *, artifact_s3_location: str, code: typing.Union["CfnCanary.CodeProperty", aws_cdk.core.IResolvable], execution_role_arn: str, name: str, run_config: typing.Union[aws_cdk.core.IResolvable, "CfnCanary.RunConfigProperty"], runtime_version: str, schedule: typing.Union[aws_cdk.core.IResolvable, "CfnCanary.ScheduleProperty"], start_canary_after_creation: typing.Union[bool, aws_cdk.core.IResolvable], failure_retention_period: typing.Optional[jsii.Number]=None, success_retention_period: typing.Optional[jsii.Number]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, vpc_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCanary.VPCConfigProperty"]]=None) -> None:
        """Properties for defining a ``AWS::Synthetics::Canary``.

        :param artifact_s3_location: ``AWS::Synthetics::Canary.ArtifactS3Location``.
        :param code: ``AWS::Synthetics::Canary.Code``.
        :param execution_role_arn: ``AWS::Synthetics::Canary.ExecutionRoleArn``.
        :param name: ``AWS::Synthetics::Canary.Name``.
        :param run_config: ``AWS::Synthetics::Canary.RunConfig``.
        :param runtime_version: ``AWS::Synthetics::Canary.RuntimeVersion``.
        :param schedule: ``AWS::Synthetics::Canary.Schedule``.
        :param start_canary_after_creation: ``AWS::Synthetics::Canary.StartCanaryAfterCreation``.
        :param failure_retention_period: ``AWS::Synthetics::Canary.FailureRetentionPeriod``.
        :param success_retention_period: ``AWS::Synthetics::Canary.SuccessRetentionPeriod``.
        :param tags: ``AWS::Synthetics::Canary.Tags``.
        :param vpc_config: ``AWS::Synthetics::Canary.VPCConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html
        """
        self._values = {
            'artifact_s3_location': artifact_s3_location,
            'code': code,
            'execution_role_arn': execution_role_arn,
            'name': name,
            'run_config': run_config,
            'runtime_version': runtime_version,
            'schedule': schedule,
            'start_canary_after_creation': start_canary_after_creation,
        }
        if failure_retention_period is not None: self._values["failure_retention_period"] = failure_retention_period
        if success_retention_period is not None: self._values["success_retention_period"] = success_retention_period
        if tags is not None: self._values["tags"] = tags
        if vpc_config is not None: self._values["vpc_config"] = vpc_config

    @builtins.property
    def artifact_s3_location(self) -> str:
        """``AWS::Synthetics::Canary.ArtifactS3Location``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-artifacts3location
        """
        return self._values.get('artifact_s3_location')

    @builtins.property
    def code(self) -> typing.Union["CfnCanary.CodeProperty", aws_cdk.core.IResolvable]:
        """``AWS::Synthetics::Canary.Code``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-code
        """
        return self._values.get('code')

    @builtins.property
    def execution_role_arn(self) -> str:
        """``AWS::Synthetics::Canary.ExecutionRoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-executionrolearn
        """
        return self._values.get('execution_role_arn')

    @builtins.property
    def name(self) -> str:
        """``AWS::Synthetics::Canary.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-name
        """
        return self._values.get('name')

    @builtins.property
    def run_config(self) -> typing.Union[aws_cdk.core.IResolvable, "CfnCanary.RunConfigProperty"]:
        """``AWS::Synthetics::Canary.RunConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-runconfig
        """
        return self._values.get('run_config')

    @builtins.property
    def runtime_version(self) -> str:
        """``AWS::Synthetics::Canary.RuntimeVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-runtimeversion
        """
        return self._values.get('runtime_version')

    @builtins.property
    def schedule(self) -> typing.Union[aws_cdk.core.IResolvable, "CfnCanary.ScheduleProperty"]:
        """``AWS::Synthetics::Canary.Schedule``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-schedule
        """
        return self._values.get('schedule')

    @builtins.property
    def start_canary_after_creation(self) -> typing.Union[bool, aws_cdk.core.IResolvable]:
        """``AWS::Synthetics::Canary.StartCanaryAfterCreation``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-startcanaryaftercreation
        """
        return self._values.get('start_canary_after_creation')

    @builtins.property
    def failure_retention_period(self) -> typing.Optional[jsii.Number]:
        """``AWS::Synthetics::Canary.FailureRetentionPeriod``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-failureretentionperiod
        """
        return self._values.get('failure_retention_period')

    @builtins.property
    def success_retention_period(self) -> typing.Optional[jsii.Number]:
        """``AWS::Synthetics::Canary.SuccessRetentionPeriod``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-successretentionperiod
        """
        return self._values.get('success_retention_period')

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::Synthetics::Canary.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-tags
        """
        return self._values.get('tags')

    @builtins.property
    def vpc_config(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnCanary.VPCConfigProperty"]]:
        """``AWS::Synthetics::Canary.VPCConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-vpcconfig
        """
        return self._values.get('vpc_config')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnCanaryProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "CfnCanary",
    "CfnCanaryProps",
]

publication.publish()
