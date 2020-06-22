"""
# aws-s3-step-function module

<!--BEGIN STABILITY BANNER-->---


![Stability: Experimental](https://img.shields.io/badge/stability-Experimental-important.svg?style=for-the-badge)

> All classes are under active development and subject to non-backward compatible changes or removal in any
> future version. These are not subject to the [Semantic Versioning](https://semver.org/) model.
> This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

| **Reference Documentation**:| <span style="font-weight: normal">https://docs.aws.amazon.com/solutions/latest/constructs/</span>|
|:-------------|:-------------|

<div style="height:8px"></div>

| **Language**     | **Package**        |
|:-------------|-----------------|
|![Python Logo](https://docs.aws.amazon.com/cdk/api/latest/img/python32.png) Python|`aws_solutions_constructs.aws_s3_step_function`|
|![Typescript Logo](https://docs.aws.amazon.com/cdk/api/latest/img/typescript32.png) Typescript|`@aws-solutions-constructs/aws-s3-step-function`|
|![Java Logo](https://docs.aws.amazon.com/cdk/api/latest/img/java32.png) Java|`software.amazon.awsconstructs.services.s3stepfunction`|

This AWS Solutions Construct implements an Amazon S3 bucket connected to an AWS Step Function.

Here is a minimal deployable pattern definition:

```javascript
const { S3ToStepFunction, S3ToStepFunctionProps } = require('@aws-solutions-constructs/aws-s3-step-function');

const startState = new stepfunctions.Pass(stack, 'StartState');

const props: S3ToStepFunctionProps = {
    stateMachineProps: {
      definition: startState
    }
};

new S3ToStepFunction(stack, 'test-s3-step-function-stack', props);
```

## Initializer

```text
new S3ToStepFunction(scope: Construct, id: string, props: S3ToStepFunctionProps);
```

*Parameters*

* scope [`Construct`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_core.Construct.html)
* id `string`
* props [`S3ToStepFunctionProps`](#pattern-construct-props)

## Pattern Construct Props

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|deployBucket?|`boolean`|Whether to create a S3 Bucket or use an existing S3 Bucket|
|existingBucketObj?|[`s3.Bucket`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-s3.Bucket.html)|Existing instance of S3 Bucket object|
|bucketProps?|[`s3.BucketProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-s3.BucketProps.html)|Optional user provided props to override the default props for S3 Bucket|
|stateMachineProps|[`sfn.StateMachineProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-stepfunctions.StateMachineProps.html)|Optional user provided props to override the default props for sfn.StateMachine|
|eventRuleProps?|[`events.RuleProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-events.RuleProps.html)|Optional user provided eventRuleProps to override the defaults|
|deployCloudTrail?|`boolean`|Whether to deploy a Trail in AWS CloudTrail to log API events in Amazon S3|

## Pattern Properties

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|stateMachine|[`sfn.StateMachine`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-stepfunctions.StateMachine.html)|Returns an instance of sfn.StateMachine created by the construct|
|cloudwatchAlarms|[`cloudwatch.Alarm[]`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-cloudwatch.Alarm.html)|Returns a list of cloudwatch.Alarm created by the construct|
|s3Bucket|[`s3.Bucket`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-s3.Bucket.html)|Returns an instance of the s3.Bucket created by the construct|
|cloudtrail|[`cloudtrail.Trail`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-cloudtrail.Trail.html)|Returns an instance of the cloudtrail.Trail created by the construct|

## Default settings

Out of the box implementation of the Construct without any override will set the following defaults:

### Amazon S3 Bucket

* Configure Access logging for S3 Bucket
* Enable server-side encryption for S3 Bucket using AWS managed KMS Key
* Turn on the versioning for S3 Bucket
* Don't allow public access for S3 Bucket
* Retain the S3 Bucket when deleting the CloudFormation stack

### AWS CloudTrail

* Configure a Trail in AWS CloudTrail to log API events in Amazon S3 related to the Bucket created by the Construct

### Amazon CloudWatch Events Rule

* Grant least privilege permissions to CloudWatch Events to trigger the Lambda Function

### AWS Step Function

* Enable CloudWatch logging for API Gateway
* Deploy best practices CloudWatch Alarms for the Step Function

## Architecture

![Architecture Diagram](architecture.png)

---


© Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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

import aws_cdk.aws_cloudtrail
import aws_cdk.aws_cloudwatch
import aws_cdk.aws_events
import aws_cdk.aws_s3
import aws_cdk.aws_stepfunctions
import aws_cdk.core


class S3ToStepFunction(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-solutions-constructs/aws-s3-step-function.S3ToStepFunction"):
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, state_machine_props: aws_cdk.aws_stepfunctions.StateMachineProps, bucket_props: typing.Optional[aws_cdk.aws_s3.BucketProps]=None, deploy_bucket: typing.Optional[bool]=None, deploy_cloud_trail: typing.Optional[bool]=None, event_rule_props: typing.Optional[aws_cdk.aws_events.RuleProps]=None, existing_bucket_obj: typing.Optional[aws_cdk.aws_s3.Bucket]=None) -> None:
        """
        :param scope: - represents the scope for all the resources.
        :param id: - this is a a scope-unique id.
        :param state_machine_props: User provided StateMachineProps to override the defaults. Default: - None
        :param bucket_props: Optional user provided props to override the default props. If ``deploy`` is set to true only then this property is required Default: - Default props are used
        :param deploy_bucket: Whether to create a S3 Bucket or use an existing S3 Bucket. If set to false, you must provide S3 Bucket as ``existingBucketObj`` Default: - true
        :param deploy_cloud_trail: Whether to deploy a Trail in AWS CloudTrail to log API events in Amazon S3. Default: - true
        :param event_rule_props: User provided eventRuleProps to override the defaults. Default: - None
        :param existing_bucket_obj: Existing instance of S3 Bucket object. If ``deployBucket`` is set to false only then this property is required Default: - None

        access:
        :access:: public
        since:
        :since:: 0.9.0
        summary:
        :summary:: Constructs a new instance of the S3ToStepFunction class.
        """
        props = S3ToStepFunctionProps(state_machine_props=state_machine_props, bucket_props=bucket_props, deploy_bucket=deploy_bucket, deploy_cloud_trail=deploy_cloud_trail, event_rule_props=event_rule_props, existing_bucket_obj=existing_bucket_obj)

        jsii.create(S3ToStepFunction, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="cloudwatchAlarms")
    def cloudwatch_alarms(self) -> typing.List[aws_cdk.aws_cloudwatch.Alarm]:
        return jsii.get(self, "cloudwatchAlarms")

    @builtins.property
    @jsii.member(jsii_name="s3Bucket")
    def s3_bucket(self) -> aws_cdk.aws_s3.Bucket:
        return jsii.get(self, "s3Bucket")

    @builtins.property
    @jsii.member(jsii_name="stateMachine")
    def state_machine(self) -> aws_cdk.aws_stepfunctions.StateMachine:
        return jsii.get(self, "stateMachine")

    @builtins.property
    @jsii.member(jsii_name="cloudtrail")
    def cloudtrail(self) -> typing.Optional[aws_cdk.aws_cloudtrail.Trail]:
        return jsii.get(self, "cloudtrail")


@jsii.data_type(jsii_type="@aws-solutions-constructs/aws-s3-step-function.S3ToStepFunctionProps", jsii_struct_bases=[], name_mapping={'state_machine_props': 'stateMachineProps', 'bucket_props': 'bucketProps', 'deploy_bucket': 'deployBucket', 'deploy_cloud_trail': 'deployCloudTrail', 'event_rule_props': 'eventRuleProps', 'existing_bucket_obj': 'existingBucketObj'})
class S3ToStepFunctionProps():
    def __init__(self, *, state_machine_props: aws_cdk.aws_stepfunctions.StateMachineProps, bucket_props: typing.Optional[aws_cdk.aws_s3.BucketProps]=None, deploy_bucket: typing.Optional[bool]=None, deploy_cloud_trail: typing.Optional[bool]=None, event_rule_props: typing.Optional[aws_cdk.aws_events.RuleProps]=None, existing_bucket_obj: typing.Optional[aws_cdk.aws_s3.Bucket]=None) -> None:
        """
        :param state_machine_props: User provided StateMachineProps to override the defaults. Default: - None
        :param bucket_props: Optional user provided props to override the default props. If ``deploy`` is set to true only then this property is required Default: - Default props are used
        :param deploy_bucket: Whether to create a S3 Bucket or use an existing S3 Bucket. If set to false, you must provide S3 Bucket as ``existingBucketObj`` Default: - true
        :param deploy_cloud_trail: Whether to deploy a Trail in AWS CloudTrail to log API events in Amazon S3. Default: - true
        :param event_rule_props: User provided eventRuleProps to override the defaults. Default: - None
        :param existing_bucket_obj: Existing instance of S3 Bucket object. If ``deployBucket`` is set to false only then this property is required Default: - None

        summary:
        :summary:: The properties for the S3ToStepFunction Construct
        """
        if isinstance(state_machine_props, dict): state_machine_props = aws_cdk.aws_stepfunctions.StateMachineProps(**state_machine_props)
        if isinstance(bucket_props, dict): bucket_props = aws_cdk.aws_s3.BucketProps(**bucket_props)
        if isinstance(event_rule_props, dict): event_rule_props = aws_cdk.aws_events.RuleProps(**event_rule_props)
        self._values = {
            'state_machine_props': state_machine_props,
        }
        if bucket_props is not None: self._values["bucket_props"] = bucket_props
        if deploy_bucket is not None: self._values["deploy_bucket"] = deploy_bucket
        if deploy_cloud_trail is not None: self._values["deploy_cloud_trail"] = deploy_cloud_trail
        if event_rule_props is not None: self._values["event_rule_props"] = event_rule_props
        if existing_bucket_obj is not None: self._values["existing_bucket_obj"] = existing_bucket_obj

    @builtins.property
    def state_machine_props(self) -> aws_cdk.aws_stepfunctions.StateMachineProps:
        """User provided StateMachineProps to override the defaults.

        default
        :default: - None
        """
        return self._values.get('state_machine_props')

    @builtins.property
    def bucket_props(self) -> typing.Optional[aws_cdk.aws_s3.BucketProps]:
        """Optional user provided props to override the default props.

        If ``deploy`` is set to true only then this property is required

        default
        :default: - Default props are used
        """
        return self._values.get('bucket_props')

    @builtins.property
    def deploy_bucket(self) -> typing.Optional[bool]:
        """Whether to create a S3 Bucket or use an existing S3 Bucket.

        If set to false, you must provide S3 Bucket as ``existingBucketObj``

        default
        :default: - true
        """
        return self._values.get('deploy_bucket')

    @builtins.property
    def deploy_cloud_trail(self) -> typing.Optional[bool]:
        """Whether to deploy a Trail in AWS CloudTrail to log API events in Amazon S3.

        default
        :default: - true
        """
        return self._values.get('deploy_cloud_trail')

    @builtins.property
    def event_rule_props(self) -> typing.Optional[aws_cdk.aws_events.RuleProps]:
        """User provided eventRuleProps to override the defaults.

        default
        :default: - None
        """
        return self._values.get('event_rule_props')

    @builtins.property
    def existing_bucket_obj(self) -> typing.Optional[aws_cdk.aws_s3.Bucket]:
        """Existing instance of S3 Bucket object.

        If ``deployBucket`` is set to false only then this property is required

        default
        :default: - None
        """
        return self._values.get('existing_bucket_obj')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'S3ToStepFunctionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "S3ToStepFunction",
    "S3ToStepFunctionProps",
]

publication.publish()
