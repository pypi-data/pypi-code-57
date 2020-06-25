"""
# aws-cloudfront-s3 module

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
|![Python Logo](https://docs.aws.amazon.com/cdk/api/latest/img/python32.png) Python|`aws_solutions_constructs.aws_cloudfront_s3`|
|![Typescript Logo](https://docs.aws.amazon.com/cdk/api/latest/img/typescript32.png) Typescript|`@aws-solutions-constructs/aws-cloudfront-s3`|
|![Java Logo](https://docs.aws.amazon.com/cdk/api/latest/img/java32.png) Java|`software.amazon.awsconstructs.services.cloudfronts3`|

This AWS Solutions Construct implements an AWS CloudFront fronting an AWS S3 Bucket.

Here is a minimal deployable pattern definition:

```javascript
const { CloudFrontToS3 } = require('@aws-solutions-constructs/aws-cloudfront-s3');

new CloudFrontToS3(stack, 'test-cloudfront-s3', {
    deployBucket: true
});

```

## Initializer

```text
new CloudFrontToS3(scope: Construct, id: string, props: CloudFrontToS3Props);
```

*Parameters*

* scope [`Construct`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_core.Construct.html)
* id `string`
* props [`CloudFrontToS3Props`](#pattern-construct-props)

## Pattern Construct Props

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|deployBucket|`boolean`|Whether to create a S3 Bucket or use an existing S3 Bucket|
|existingBucketObj?|[`s3.Bucket`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-s3.Bucket.html)|Existing instance of S3 Bucket object|
|bucketProps?|[`s3.BucketProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-s3.BucketProps.html)|Optional user provided props to override the default props for S3 Bucket|
|cloudFrontDistributionProps?|[`cloudfront.CloudFrontWebDistributionProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-cloudfront.CloudFrontWebDistributionProps.html)|Optional user provided props to override the default props for CloudFront Distribution|
|insertHttpSecurityHeaders?|`boolean`|Optional user provided props to turn on/off the automatic injection of best practice HTTP security headers in all responses from CloudFront|

## Pattern Properties

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|cloudFrontWebDistribution|[`cloudfront.CloudFrontWebDistribution`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-cloudfront.CloudFrontWebDistribution.html)|Returns an instance of cloudfront.CloudFrontWebDistribution created by the construct|
|s3Bucket|[`s3.Bucket`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-s3.Bucket.html)|Returns an instance of s3.Bucket created by the construct|

## Default settings

Out of the box implementation of the Construct without any override will set the following defaults:

### Amazon CloudFront

* Configure Access logging for CloudFront WebDistribution
* Enable automatic injection of best practice HTTP security headers in all responses from CloudFront WebDistribution

### Amazon S3 Bucket

* Configure Access logging for S3 Bucket
* Enable server-side encryption for S3 Bucket using AWS managed KMS Key
* Turn on the versioning for S3 Bucket
* Don't allow public access for S3 Bucket
* Retain the S3 Bucket when deleting the CloudFormation stack

## Architecture

![Architecture Diagram](architecture.png)

---


© Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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

import aws_cdk.aws_cloudfront
import aws_cdk.aws_s3
import aws_cdk.core


class CloudFrontToS3(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-solutions-constructs/aws-cloudfront-s3.CloudFrontToS3"):
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, bucket_props: typing.Optional[aws_cdk.aws_s3.BucketProps]=None, cloud_front_distribution_props: typing.Any=None, deploy_bucket: typing.Optional[bool]=None, existing_bucket_obj: typing.Optional[aws_cdk.aws_s3.Bucket]=None, insert_http_security_headers: typing.Optional[bool]=None) -> None:
        """
        :param scope: - represents the scope for all the resources.
        :param id: - this is a a scope-unique id.
        :param bucket_props: Optional user provided props to override the default props. If ``deploy`` is set to true only then this property is required Default: - Default props are used
        :param cloud_front_distribution_props: Optional user provided props to override the default props. Default: - Default props are used
        :param deploy_bucket: Whether to create a S3 Bucket or use an existing S3 Bucket. If set to false, you must provide S3 Bucket as ``existingBucketObj`` Default: - true
        :param existing_bucket_obj: Existing instance of S3 Bucket object. If ``deployBucket`` is set to false only then this property is required Default: - None
        :param insert_http_security_headers: Optional user provided props to turn on/off the automatic injection of best practice HTTP security headers in all responses from cloudfront. Default: - true

        access:
        :access:: public
        since:
        :since:: 0.8.0
        summary:
        :summary:: Constructs a new instance of the CloudFrontToS3 class.
        """
        props = CloudFrontToS3Props(bucket_props=bucket_props, cloud_front_distribution_props=cloud_front_distribution_props, deploy_bucket=deploy_bucket, existing_bucket_obj=existing_bucket_obj, insert_http_security_headers=insert_http_security_headers)

        jsii.create(CloudFrontToS3, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="cloudFrontWebDistribution")
    def cloud_front_web_distribution(self) -> aws_cdk.aws_cloudfront.CloudFrontWebDistribution:
        return jsii.get(self, "cloudFrontWebDistribution")

    @builtins.property
    @jsii.member(jsii_name="s3Bucket")
    def s3_bucket(self) -> aws_cdk.aws_s3.Bucket:
        return jsii.get(self, "s3Bucket")


@jsii.data_type(jsii_type="@aws-solutions-constructs/aws-cloudfront-s3.CloudFrontToS3Props", jsii_struct_bases=[], name_mapping={'bucket_props': 'bucketProps', 'cloud_front_distribution_props': 'cloudFrontDistributionProps', 'deploy_bucket': 'deployBucket', 'existing_bucket_obj': 'existingBucketObj', 'insert_http_security_headers': 'insertHttpSecurityHeaders'})
class CloudFrontToS3Props():
    def __init__(self, *, bucket_props: typing.Optional[aws_cdk.aws_s3.BucketProps]=None, cloud_front_distribution_props: typing.Any=None, deploy_bucket: typing.Optional[bool]=None, existing_bucket_obj: typing.Optional[aws_cdk.aws_s3.Bucket]=None, insert_http_security_headers: typing.Optional[bool]=None) -> None:
        """
        :param bucket_props: Optional user provided props to override the default props. If ``deploy`` is set to true only then this property is required Default: - Default props are used
        :param cloud_front_distribution_props: Optional user provided props to override the default props. Default: - Default props are used
        :param deploy_bucket: Whether to create a S3 Bucket or use an existing S3 Bucket. If set to false, you must provide S3 Bucket as ``existingBucketObj`` Default: - true
        :param existing_bucket_obj: Existing instance of S3 Bucket object. If ``deployBucket`` is set to false only then this property is required Default: - None
        :param insert_http_security_headers: Optional user provided props to turn on/off the automatic injection of best practice HTTP security headers in all responses from cloudfront. Default: - true

        summary:
        :summary:: The properties for the CloudFrontToS3 Construct
        """
        if isinstance(bucket_props, dict): bucket_props = aws_cdk.aws_s3.BucketProps(**bucket_props)
        self._values = {
        }
        if bucket_props is not None: self._values["bucket_props"] = bucket_props
        if cloud_front_distribution_props is not None: self._values["cloud_front_distribution_props"] = cloud_front_distribution_props
        if deploy_bucket is not None: self._values["deploy_bucket"] = deploy_bucket
        if existing_bucket_obj is not None: self._values["existing_bucket_obj"] = existing_bucket_obj
        if insert_http_security_headers is not None: self._values["insert_http_security_headers"] = insert_http_security_headers

    @builtins.property
    def bucket_props(self) -> typing.Optional[aws_cdk.aws_s3.BucketProps]:
        """Optional user provided props to override the default props.

        If ``deploy`` is set to true only then this property is required

        default
        :default: - Default props are used
        """
        return self._values.get('bucket_props')

    @builtins.property
    def cloud_front_distribution_props(self) -> typing.Any:
        """Optional user provided props to override the default props.

        default
        :default: - Default props are used
        """
        return self._values.get('cloud_front_distribution_props')

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
    def insert_http_security_headers(self) -> typing.Optional[bool]:
        """Optional user provided props to turn on/off the automatic injection of best practice HTTP security headers in all responses from cloudfront.

        default
        :default: - true
        """
        return self._values.get('insert_http_security_headers')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CloudFrontToS3Props(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "CloudFrontToS3",
    "CloudFrontToS3Props",
]

publication.publish()
