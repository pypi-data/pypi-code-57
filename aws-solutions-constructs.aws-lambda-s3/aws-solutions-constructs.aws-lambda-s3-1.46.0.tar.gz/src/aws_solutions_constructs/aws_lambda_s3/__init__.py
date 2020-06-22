"""
# aws-lambda-s3 module

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
|![Python Logo](https://docs.aws.amazon.com/cdk/api/latest/img/python32.png) Python|`aws_solutions_constructs.aws_lambda_s3`|
|![Typescript Logo](https://docs.aws.amazon.com/cdk/api/latest/img/typescript32.png) Typescript|`@aws-solutions-constructs/aws-lambda-s3`|
|![Java Logo](https://docs.aws.amazon.com/cdk/api/latest/img/java32.png) Java|`software.amazon.awsconstructs.services.lambdas3`|

This AWS Solutions Construct implements an AWS Lambda function connected to an Amazon S3 bucket.

Here is a minimal deployable pattern definition:

```javascript
const { LambdaToS3 } = require('@aws-solutions-constructs/aws-lambda-s3');

new LambdaToS3(stack, 'LambdaToS3Pattern', {
    deployLambda: true,
    lambdaFunctionProps: {
        runtime: lambda.Runtime.NODEJS_10_X,
        handler: 'index.handler',
        code: lambda.Code.asset(`${__dirname}/lambda`)
    }
});

```

## Initializer

```text
new LambdaToS3(scope: Construct, id: string, props: LambdaToS3Props);
```

*Parameters*

* scope [`Construct`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_core.Construct.html)
* id `string`
* props [`LambdaToS3Props`](#pattern-construct-props)

## Pattern Construct Props

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|deployLambda|`boolean`|Whether to create a new Lambda function or use an existing Lambda function.|
|existingLambdaObj?|[`lambda.Function`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-lambda.Function.html)|An optional, existing Lambda function.|
|lambdaFunctionProps?|[`lambda.FunctionProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-lambda.FunctionProps.html)|Optional user-provided props to override the default props for the Lambda function.|
|deployBucket?|`boolean`|Whether to create a S3 Bucket or use an existing S3 Bucket|
|existingBucketObj?|[`s3.Bucket`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-s3.Bucket.html)|Existing instance of S3 Bucket object|
|bucketProps?|[`s3.BucketProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-s3.BucketProps.html)|Optional user provided props to override the default props for S3 Bucket|
|bucketPermissions?|`string[]`|Optional bucket permissions to grant to the Lambda function. One or more of the following may be specified: `Delete`, `Put`, `Read`, `ReadWrite`, `Write`.|

## Pattern Properties

|lambdaFunction|[`lambda.Function`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-lambda.Function.html)|Returns an instance of the Lambda function created by the pattern.|
|s3Bucket|[`s3.Bucket`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-s3.Bucket.html)|Returns an instance of the S3 bucket created by the pattern.|

## Default settings

Out of the box implementation of the Construct without any override will set the following defaults:

### AWS Lambda Function

* Configure least privilege access IAM role for Lambda function
* Enable reusing connections with Keep-Alive for NodeJs Lambda function

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

import aws_cdk.aws_lambda
import aws_cdk.aws_s3
import aws_cdk.core


class LambdaToS3(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-solutions-constructs/aws-lambda-s3.LambdaToS3"):
    """
    summary:
    :summary:: The LambdaToS3 class.
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, deploy_lambda: bool, bucket_permissions: typing.Optional[typing.List[str]]=None, bucket_props: typing.Optional[aws_cdk.aws_s3.BucketProps]=None, deploy_bucket: typing.Optional[bool]=None, existing_bucket_obj: typing.Optional[aws_cdk.aws_s3.Bucket]=None, existing_lambda_obj: typing.Optional[aws_cdk.aws_lambda.Function]=None, lambda_function_props: typing.Any=None) -> None:
        """
        :param scope: - represents the scope for all the resources.
        :param id: - this is a a scope-unique id.
        :param deploy_lambda: Whether to create a new Lambda function or use an existing Lambda function. If set to false, you must provide an existing function for the ``existingLambdaObj`` property. Default: - true
        :param bucket_permissions: Optional bucket permissions to grant to the Lambda function. One or more of the following may be specified: "Delete", "Put", "Read", "ReadWrite", "Write". Default: - Read/write access is given to the Lambda function if no value is specified.
        :param bucket_props: Optional user provided props to override the default props. If ``deploy`` is set to true only then this property is required Default: - Default props are used
        :param deploy_bucket: Whether to create a S3 Bucket or use an existing S3 Bucket. If set to false, you must provide S3 Bucket as ``existingBucketObj`` Default: - true
        :param existing_bucket_obj: Existing instance of S3 Bucket object. If ``deployBucket`` is set to false only then this property is required Default: - None
        :param existing_lambda_obj: Existing instance of Lambda Function object. If ``deploy`` is set to false only then this property is required Default: - None
        :param lambda_function_props: Optional user provided properties to override the default properties for the Lambda function. If ``deploy`` is set to true only then this property is required. Default: - Default properties are used.

        access:
        :access:: public
        since:
        :since:: 0.8.0
        summary:
        :summary:: Constructs a new instance of the LambdaToS3 class.
        """
        props = LambdaToS3Props(deploy_lambda=deploy_lambda, bucket_permissions=bucket_permissions, bucket_props=bucket_props, deploy_bucket=deploy_bucket, existing_bucket_obj=existing_bucket_obj, existing_lambda_obj=existing_lambda_obj, lambda_function_props=lambda_function_props)

        jsii.create(LambdaToS3, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="lambdaFunction")
    def lambda_function(self) -> aws_cdk.aws_lambda.Function:
        return jsii.get(self, "lambdaFunction")

    @builtins.property
    @jsii.member(jsii_name="s3Bucket")
    def s3_bucket(self) -> aws_cdk.aws_s3.Bucket:
        return jsii.get(self, "s3Bucket")


@jsii.data_type(jsii_type="@aws-solutions-constructs/aws-lambda-s3.LambdaToS3Props", jsii_struct_bases=[], name_mapping={'deploy_lambda': 'deployLambda', 'bucket_permissions': 'bucketPermissions', 'bucket_props': 'bucketProps', 'deploy_bucket': 'deployBucket', 'existing_bucket_obj': 'existingBucketObj', 'existing_lambda_obj': 'existingLambdaObj', 'lambda_function_props': 'lambdaFunctionProps'})
class LambdaToS3Props():
    def __init__(self, *, deploy_lambda: bool, bucket_permissions: typing.Optional[typing.List[str]]=None, bucket_props: typing.Optional[aws_cdk.aws_s3.BucketProps]=None, deploy_bucket: typing.Optional[bool]=None, existing_bucket_obj: typing.Optional[aws_cdk.aws_s3.Bucket]=None, existing_lambda_obj: typing.Optional[aws_cdk.aws_lambda.Function]=None, lambda_function_props: typing.Any=None) -> None:
        """
        :param deploy_lambda: Whether to create a new Lambda function or use an existing Lambda function. If set to false, you must provide an existing function for the ``existingLambdaObj`` property. Default: - true
        :param bucket_permissions: Optional bucket permissions to grant to the Lambda function. One or more of the following may be specified: "Delete", "Put", "Read", "ReadWrite", "Write". Default: - Read/write access is given to the Lambda function if no value is specified.
        :param bucket_props: Optional user provided props to override the default props. If ``deploy`` is set to true only then this property is required Default: - Default props are used
        :param deploy_bucket: Whether to create a S3 Bucket or use an existing S3 Bucket. If set to false, you must provide S3 Bucket as ``existingBucketObj`` Default: - true
        :param existing_bucket_obj: Existing instance of S3 Bucket object. If ``deployBucket`` is set to false only then this property is required Default: - None
        :param existing_lambda_obj: Existing instance of Lambda Function object. If ``deploy`` is set to false only then this property is required Default: - None
        :param lambda_function_props: Optional user provided properties to override the default properties for the Lambda function. If ``deploy`` is set to true only then this property is required. Default: - Default properties are used.

        summary:
        :summary:: The properties for the LambdaToS3 class.
        """
        if isinstance(bucket_props, dict): bucket_props = aws_cdk.aws_s3.BucketProps(**bucket_props)
        self._values = {
            'deploy_lambda': deploy_lambda,
        }
        if bucket_permissions is not None: self._values["bucket_permissions"] = bucket_permissions
        if bucket_props is not None: self._values["bucket_props"] = bucket_props
        if deploy_bucket is not None: self._values["deploy_bucket"] = deploy_bucket
        if existing_bucket_obj is not None: self._values["existing_bucket_obj"] = existing_bucket_obj
        if existing_lambda_obj is not None: self._values["existing_lambda_obj"] = existing_lambda_obj
        if lambda_function_props is not None: self._values["lambda_function_props"] = lambda_function_props

    @builtins.property
    def deploy_lambda(self) -> bool:
        """Whether to create a new Lambda function or use an existing Lambda function.

        If set to false, you must provide an existing function for the ``existingLambdaObj`` property.

        default
        :default: - true
        """
        return self._values.get('deploy_lambda')

    @builtins.property
    def bucket_permissions(self) -> typing.Optional[typing.List[str]]:
        """Optional bucket permissions to grant to the Lambda function.

        One or more of the following may be specified: "Delete", "Put", "Read", "ReadWrite", "Write".

        default
        :default: - Read/write access is given to the Lambda function if no value is specified.
        """
        return self._values.get('bucket_permissions')

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
    def existing_lambda_obj(self) -> typing.Optional[aws_cdk.aws_lambda.Function]:
        """Existing instance of Lambda Function object.

        If ``deploy`` is set to false only then this property is required

        default
        :default: - None
        """
        return self._values.get('existing_lambda_obj')

    @builtins.property
    def lambda_function_props(self) -> typing.Any:
        """Optional user provided properties to override the default properties for the Lambda function.

        If ``deploy`` is set to true only then this property is required.

        default
        :default: - Default properties are used.
        """
        return self._values.get('lambda_function_props')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LambdaToS3Props(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "LambdaToS3",
    "LambdaToS3Props",
]

publication.publish()
