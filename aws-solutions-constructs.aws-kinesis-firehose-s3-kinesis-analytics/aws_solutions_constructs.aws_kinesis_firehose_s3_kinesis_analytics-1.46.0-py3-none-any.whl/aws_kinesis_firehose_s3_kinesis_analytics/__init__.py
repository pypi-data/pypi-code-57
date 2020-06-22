"""
# aws-kinesisfirehose-s3-and-kinesisanalytics module

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
|![Python Logo](https://docs.aws.amazon.com/cdk/api/latest/img/python32.png) Python|`aws_solutions_constructs.aws_kinesisfirehose_s3_and_kinesisanalytics`|
|![Typescript Logo](https://docs.aws.amazon.com/cdk/api/latest/img/typescript32.png) Typescript|`@aws-solutions-constructs/aws-kinesisfirehose-s3-and-kinesisanalytics`|
|![Java Logo](https://docs.aws.amazon.com/cdk/api/latest/img/java32.png) Java|`software.amazon.awsconstructs.services.kinesisfirehoses3kinesisanalytics`|

This AWS Solutions Construct implements an Amazon Kinesis Firehose delivery stream connected to an Amazon S3 bucket, and an Amazon Kinesis Analytics application.

Here is a minimal deployable pattern definition:

```javascript
const { KinesisFirehoseToAnalyticsAndS3 } = require('@aws-solutions-constructs/aws-kinesisfirehose-s3-and-kinesisanalytics');

new KinesisFirehoseToAnalyticsAndS3(stack, 'FirehoseToS3AndAnalyticsPattern', {
    kinesisAnalyticsProps: {
        inputs: [{
            inputSchema: {
                recordColumns: [{
                    name: 'ticker_symbol',
                    sqlType: 'VARCHAR(4)',
                    mapping: '$.ticker_symbol'
                }, {
                    name: 'sector',
                    sqlType: 'VARCHAR(16)',
                    mapping: '$.sector'
                }, {
                    name: 'change',
                    sqlType: 'REAL',
                    mapping: '$.change'
                }, {
                    name: 'price',
                    sqlType: 'REAL',
                    mapping: '$.price'
                }],
                recordFormat: {
                    recordFormatType: 'JSON'
                },
                recordEncoding: 'UTF-8'
            },
            namePrefix: 'SOURCE_SQL_STREAM'
        }]
    }
});

```

## Initializer

```text
new KinesisFirehoseToAnalyticsAndS3(scope: Construct, id: string, props: KinesisFirehoseToAnalyticsAndS3Props);
```

*Parameters*

* scope [`Construct`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_core.Construct.html)
* id `string`
* props [`KinesisFirehoseToAnalyticsAndS3Props`](#pattern-construct-props)

## Pattern Construct Props

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|kinesisFirehoseProps?|[`kinesisFirehose.CfnDeliveryStreamProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-kinesisfirehose.CfnDeliveryStreamProps.html)|Optional user-provided props to override the default props for the Kinesis Firehose delivery stream.|
|kinesisAnalyticsProps?|[`kinesisAnalytics.CfnApplicationProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-kinesisanalytics.CfnApplicationProps.html)|Optional user-provided props to override the default props for the Kinesis Analytics application.|
|deployBucket?|`boolean`|Whether to create a S3 Bucket or use an existing S3 Bucket|
|existingBucketObj?|[`s3.Bucket`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-s3.Bucket.html)|Existing instance of S3 Bucket object|
|bucketProps?|[`s3.BucketProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-s3.BucketProps.html)|Optional user provided props to override the default props for S3 Bucket|

## Pattern Properties

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|kinesisAnalytics|[`kinesisAnalytics.CfnApplication`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-kinesisanalytics.CfnApplication.html)|Returns an instance of the Kinesis Analytics application created by the pattern.|
|kinesisFirehose|[`kinesisFirehose.CfnDeliveryStream`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-kinesisfirehose.CfnDeliveryStream.html)|Returns an instance of the Kinesis Firehose delivery stream created by the pattern.|
|s3Bucket|[`s3.Bucket`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-s3.Bucket.html)|Returns an instance of the S3 bucket created by the pattern.|

## Default settings

Out of the box implementation of the Construct without any override will set the following defaults:

### Amazon Kinesis Firehose

* Enable CloudWatch logging for Kinesis Firehose
* Configure least privilege access IAM role for Amazon Kinesis Firehose

### Amazon S3 Bucket

* Configure Access logging for S3 Bucket
* Enable server-side encryption for S3 Bucket using AWS managed KMS Key
* Turn on the versioning for S3 Bucket
* Don't allow public access for S3 Bucket
* Retain the S3 Bucket when deleting the CloudFormation stack

### Amazon Kinesis Data Analytics

* Configure least privilege access IAM role for Amazon Kinesis Analytics

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

import aws_cdk.aws_kinesisanalytics
import aws_cdk.aws_kinesisfirehose
import aws_cdk.aws_s3
import aws_cdk.core


class KinesisFirehoseToAnalyticsAndS3(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-solutions-constructs/aws-kinesisfirehose-s3-and-kinesisanalytics.KinesisFirehoseToAnalyticsAndS3"):
    """
    summary:
    :summary:: The KinesisFirehoseToAnalyticsAndS3 class.
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, bucket_props: typing.Optional[aws_cdk.aws_s3.BucketProps]=None, deploy_bucket: typing.Optional[bool]=None, existing_bucket_obj: typing.Optional[aws_cdk.aws_s3.Bucket]=None, kinesis_analytics_props: typing.Any=None, kinesis_firehose_props: typing.Any=None) -> None:
        """
        :param scope: - represents the scope for all the resources.
        :param id: - this is a a scope-unique id.
        :param bucket_props: Optional user provided props to override the default props. If ``deploy`` is set to true only then this property is required Default: - Default props are used
        :param deploy_bucket: Whether to create a S3 Bucket or use an existing S3 Bucket. If set to false, you must provide S3 Bucket as ``existingBucketObj`` Default: - true
        :param existing_bucket_obj: Existing instance of S3 Bucket object. If ``deployBucket`` is set to false only then this property is required Default: - None
        :param kinesis_analytics_props: Optional user-provided props to override the default props for the Kinesis Analytics application. Default: - Default props are used.
        :param kinesis_firehose_props: Optional user-provided props to override the default props for the Kinesis Firehose delivery stream. Default: - Default props are used.

        access:
        :access:: public
        since:
        :since:: 0.8.0
        summary:
        :summary:: Constructs a new instance of the KinesisFirehoseToAnalyticsAndS3 class.
        """
        props = KinesisFirehoseToAnalyticsAndS3Props(bucket_props=bucket_props, deploy_bucket=deploy_bucket, existing_bucket_obj=existing_bucket_obj, kinesis_analytics_props=kinesis_analytics_props, kinesis_firehose_props=kinesis_firehose_props)

        jsii.create(KinesisFirehoseToAnalyticsAndS3, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="kinesisAnalytics")
    def kinesis_analytics(self) -> aws_cdk.aws_kinesisanalytics.CfnApplication:
        return jsii.get(self, "kinesisAnalytics")

    @builtins.property
    @jsii.member(jsii_name="kinesisFirehose")
    def kinesis_firehose(self) -> aws_cdk.aws_kinesisfirehose.CfnDeliveryStream:
        return jsii.get(self, "kinesisFirehose")

    @builtins.property
    @jsii.member(jsii_name="s3Bucket")
    def s3_bucket(self) -> aws_cdk.aws_s3.Bucket:
        return jsii.get(self, "s3Bucket")


@jsii.data_type(jsii_type="@aws-solutions-constructs/aws-kinesisfirehose-s3-and-kinesisanalytics.KinesisFirehoseToAnalyticsAndS3Props", jsii_struct_bases=[], name_mapping={'bucket_props': 'bucketProps', 'deploy_bucket': 'deployBucket', 'existing_bucket_obj': 'existingBucketObj', 'kinesis_analytics_props': 'kinesisAnalyticsProps', 'kinesis_firehose_props': 'kinesisFirehoseProps'})
class KinesisFirehoseToAnalyticsAndS3Props():
    def __init__(self, *, bucket_props: typing.Optional[aws_cdk.aws_s3.BucketProps]=None, deploy_bucket: typing.Optional[bool]=None, existing_bucket_obj: typing.Optional[aws_cdk.aws_s3.Bucket]=None, kinesis_analytics_props: typing.Any=None, kinesis_firehose_props: typing.Any=None) -> None:
        """The properties for the KinesisFirehoseToAnalyticsAndS3 class.

        :param bucket_props: Optional user provided props to override the default props. If ``deploy`` is set to true only then this property is required Default: - Default props are used
        :param deploy_bucket: Whether to create a S3 Bucket or use an existing S3 Bucket. If set to false, you must provide S3 Bucket as ``existingBucketObj`` Default: - true
        :param existing_bucket_obj: Existing instance of S3 Bucket object. If ``deployBucket`` is set to false only then this property is required Default: - None
        :param kinesis_analytics_props: Optional user-provided props to override the default props for the Kinesis Analytics application. Default: - Default props are used.
        :param kinesis_firehose_props: Optional user-provided props to override the default props for the Kinesis Firehose delivery stream. Default: - Default props are used.
        """
        if isinstance(bucket_props, dict): bucket_props = aws_cdk.aws_s3.BucketProps(**bucket_props)
        self._values = {
        }
        if bucket_props is not None: self._values["bucket_props"] = bucket_props
        if deploy_bucket is not None: self._values["deploy_bucket"] = deploy_bucket
        if existing_bucket_obj is not None: self._values["existing_bucket_obj"] = existing_bucket_obj
        if kinesis_analytics_props is not None: self._values["kinesis_analytics_props"] = kinesis_analytics_props
        if kinesis_firehose_props is not None: self._values["kinesis_firehose_props"] = kinesis_firehose_props

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
    def kinesis_analytics_props(self) -> typing.Any:
        """Optional user-provided props to override the default props for the Kinesis Analytics application.

        default
        :default: - Default props are used.
        """
        return self._values.get('kinesis_analytics_props')

    @builtins.property
    def kinesis_firehose_props(self) -> typing.Any:
        """Optional user-provided props to override the default props for the Kinesis Firehose delivery stream.

        default
        :default: - Default props are used.
        """
        return self._values.get('kinesis_firehose_props')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'KinesisFirehoseToAnalyticsAndS3Props(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "KinesisFirehoseToAnalyticsAndS3",
    "KinesisFirehoseToAnalyticsAndS3Props",
]

publication.publish()
