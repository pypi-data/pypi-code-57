"""
# aws-iot-kinesisfirehose-s3 module

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
|![Python Logo](https://docs.aws.amazon.com/cdk/api/latest/img/python32.png) Python|`aws_solutions_constructs.aws_iot_kinesisfirehose_s3`|
|![Typescript Logo](https://docs.aws.amazon.com/cdk/api/latest/img/typescript32.png) Typescript|`@aws-solutions-constructs/aws-iot-kinesisfirehose-s3`|
|![Java Logo](https://docs.aws.amazon.com/cdk/api/latest/img/java32.png) Java|`software.amazon.awsconstructs.services.iotkinesisfirehoses3`|

This AWS Solutions Construct implements an AWS IoT MQTT topic rule to send data to an Amazon Kinesis Data Firehose delivery stream connected to an Amazon S3 bucket.

Here is a minimal deployable pattern definition:

```javascript
const { IotToKinesisFirehoseToS3Props, IotToKinesisFirehoseToS3 } = require('@aws-solutions-constructs/aws-iot-kinesisfirehose-s3');

const props: IotToKinesisFirehoseToS3Props = {
    iotTopicRuleProps: {
        topicRulePayload: {
            ruleDisabled: false,
            description: "Persistent storage of connected vehicle telematics data",
            sql: "SELECT * FROM 'connectedcar/telemetry/#'",
            actions: []
        }
    }
};

new IotToKinesisFirehoseToS3(stack, 'test-iot-firehose-s3', props);

```

## Initializer

```text
new IotToKinesisFirehoseToS3(scope: Construct, id: string, props: IotToKinesisFirehoseToS3Props);
```

*Parameters*

* scope [`Construct`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_core.Construct.html)
* id `string`
* props [`IotToKinesisFirehoseToS3Props`](#pattern-construct-props)

## Pattern Construct Props

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|iotTopicRuleProps|[`iot.CfnTopicRuleProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-iot.CfnTopicRuleProps.html)|User provided CfnTopicRuleProps to override the defaults|
|kinesisFirehoseProps?|[`kinesisfirehose.CfnDeliveryStreamProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-kinesisfirehose.CfnDeliveryStreamProps.html)|Optional user provided props to override the default props for Kinesis Firehose Delivery Stream|
|deployBucket?|`boolean`|Whether to create a S3 Bucket or use an existing S3 Bucket|
|existingBucketObj?|[`s3.Bucket`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-s3.Bucket.html)|Existing instance of S3 Bucket object|
|bucketProps?|[`s3.BucketProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-s3.BucketProps.html)|Optional user provided props to override the default props for S3 Bucket|

## Pattern Properties

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|kinesisFirehose|[`kinesisfirehose.CfnDeliveryStream`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-kinesisfirehose.CfnDeliveryStream.html)|Returns an instance of kinesisfirehose.CfnDeliveryStream created by the construct|
|s3Bucket|[`s3.Bucket`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-s3.Bucket.html)|Returns an instance of s3.Bucket created by the construct|
|iotTopicRule|[`iot.CfnTopicRule`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-iot.CfnTopicRule.html)|Returns an instance of iot.CfnTopicRule created by the construct|
|iotActionsRole|[`iam.Role`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-iam.Role.html)|Returns an instance of the iam.Role created by the construct for IoT Rule|
|kinesisFirehoseRole|[`iam.Role`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-iam.Role.html)|Returns an instance of the iam.Role created by the construct for Kinesis Data Firehose delivery stream|

## Default settings

Out of the box implementation of the Construct without any override will set the following defaults:

### Amazon IoT Rule

* Configure least privilege access IAM role for Amazon IoT

### Amazon Kinesis Firehose

* Enable CloudWatch logging for Kinesis Firehose
* Configure least privilege access IAM role for Amazon Kinesis Firehose

### Amazon S3 Bucket

* Configure Access logging for S3 Bucket
* Enable server-side encryption for S3 Bucket using AWS managed KMS Key
* Turn on the versioning for S3 Bucket
* Don't allow public access for S3 Bucket
* Retain the S3 Bucket when deleting the CloudFormation stack

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

import aws_cdk.aws_iam
import aws_cdk.aws_iot
import aws_cdk.aws_kinesisfirehose
import aws_cdk.aws_s3
import aws_cdk.core


class IotToKinesisFirehoseToS3(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-solutions-constructs/aws-iot-kinesisfirehose-s3.IotToKinesisFirehoseToS3"):
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, iot_topic_rule_props: aws_cdk.aws_iot.CfnTopicRuleProps, bucket_props: typing.Optional[aws_cdk.aws_s3.BucketProps]=None, deploy_bucket: typing.Optional[bool]=None, existing_bucket_obj: typing.Optional[aws_cdk.aws_s3.Bucket]=None, kinesis_firehose_props: typing.Any=None) -> None:
        """
        :param scope: - represents the scope for all the resources.
        :param id: - this is a a scope-unique id.
        :param iot_topic_rule_props: User provided CfnTopicRuleProps to override the defaults. Default: - Default props are used
        :param bucket_props: Optional user provided props to override the default props. If ``deploy`` is set to true only then this property is required Default: - Default props are used
        :param deploy_bucket: Whether to create a S3 Bucket or use an existing S3 Bucket. If set to false, you must provide S3 Bucket as ``existingBucketObj`` Default: - true
        :param existing_bucket_obj: Existing instance of S3 Bucket object. If ``deployBucket`` is set to false only then this property is required Default: - None
        :param kinesis_firehose_props: Optional user provided props to override the default props. Default: - Default props are used

        access:
        :access:: public
        since:
        :since:: 0.8.0
        summary:
        :summary:: Constructs a new instance of the IotToKinesisFirehoseToS3 class.
        """
        props = IotToKinesisFirehoseToS3Props(iot_topic_rule_props=iot_topic_rule_props, bucket_props=bucket_props, deploy_bucket=deploy_bucket, existing_bucket_obj=existing_bucket_obj, kinesis_firehose_props=kinesis_firehose_props)

        jsii.create(IotToKinesisFirehoseToS3, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="iotActionsRole")
    def iot_actions_role(self) -> aws_cdk.aws_iam.Role:
        return jsii.get(self, "iotActionsRole")

    @builtins.property
    @jsii.member(jsii_name="iotTopicRule")
    def iot_topic_rule(self) -> aws_cdk.aws_iot.CfnTopicRule:
        return jsii.get(self, "iotTopicRule")

    @builtins.property
    @jsii.member(jsii_name="kinesisFirehose")
    def kinesis_firehose(self) -> aws_cdk.aws_kinesisfirehose.CfnDeliveryStream:
        return jsii.get(self, "kinesisFirehose")

    @builtins.property
    @jsii.member(jsii_name="kinesisFirehoseRole")
    def kinesis_firehose_role(self) -> aws_cdk.aws_iam.Role:
        return jsii.get(self, "kinesisFirehoseRole")

    @builtins.property
    @jsii.member(jsii_name="s3Bucket")
    def s3_bucket(self) -> aws_cdk.aws_s3.Bucket:
        return jsii.get(self, "s3Bucket")


@jsii.data_type(jsii_type="@aws-solutions-constructs/aws-iot-kinesisfirehose-s3.IotToKinesisFirehoseToS3Props", jsii_struct_bases=[], name_mapping={'iot_topic_rule_props': 'iotTopicRuleProps', 'bucket_props': 'bucketProps', 'deploy_bucket': 'deployBucket', 'existing_bucket_obj': 'existingBucketObj', 'kinesis_firehose_props': 'kinesisFirehoseProps'})
class IotToKinesisFirehoseToS3Props():
    def __init__(self, *, iot_topic_rule_props: aws_cdk.aws_iot.CfnTopicRuleProps, bucket_props: typing.Optional[aws_cdk.aws_s3.BucketProps]=None, deploy_bucket: typing.Optional[bool]=None, existing_bucket_obj: typing.Optional[aws_cdk.aws_s3.Bucket]=None, kinesis_firehose_props: typing.Any=None) -> None:
        """
        :param iot_topic_rule_props: User provided CfnTopicRuleProps to override the defaults. Default: - Default props are used
        :param bucket_props: Optional user provided props to override the default props. If ``deploy`` is set to true only then this property is required Default: - Default props are used
        :param deploy_bucket: Whether to create a S3 Bucket or use an existing S3 Bucket. If set to false, you must provide S3 Bucket as ``existingBucketObj`` Default: - true
        :param existing_bucket_obj: Existing instance of S3 Bucket object. If ``deployBucket`` is set to false only then this property is required Default: - None
        :param kinesis_firehose_props: Optional user provided props to override the default props. Default: - Default props are used

        summary:
        :summary:: The properties for the IotToKinesisFirehoseToS3 Construct
        """
        if isinstance(iot_topic_rule_props, dict): iot_topic_rule_props = aws_cdk.aws_iot.CfnTopicRuleProps(**iot_topic_rule_props)
        if isinstance(bucket_props, dict): bucket_props = aws_cdk.aws_s3.BucketProps(**bucket_props)
        self._values = {
            'iot_topic_rule_props': iot_topic_rule_props,
        }
        if bucket_props is not None: self._values["bucket_props"] = bucket_props
        if deploy_bucket is not None: self._values["deploy_bucket"] = deploy_bucket
        if existing_bucket_obj is not None: self._values["existing_bucket_obj"] = existing_bucket_obj
        if kinesis_firehose_props is not None: self._values["kinesis_firehose_props"] = kinesis_firehose_props

    @builtins.property
    def iot_topic_rule_props(self) -> aws_cdk.aws_iot.CfnTopicRuleProps:
        """User provided CfnTopicRuleProps to override the defaults.

        default
        :default: - Default props are used
        """
        return self._values.get('iot_topic_rule_props')

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
    def existing_bucket_obj(self) -> typing.Optional[aws_cdk.aws_s3.Bucket]:
        """Existing instance of S3 Bucket object.

        If ``deployBucket`` is set to false only then this property is required

        default
        :default: - None
        """
        return self._values.get('existing_bucket_obj')

    @builtins.property
    def kinesis_firehose_props(self) -> typing.Any:
        """Optional user provided props to override the default props.

        default
        :default: - Default props are used
        """
        return self._values.get('kinesis_firehose_props')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'IotToKinesisFirehoseToS3Props(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "IotToKinesisFirehoseToS3",
    "IotToKinesisFirehoseToS3Props",
]

publication.publish()
