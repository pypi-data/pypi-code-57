"""
# aws-sns-lambda module

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
|![Python Logo](https://docs.aws.amazon.com/cdk/api/latest/img/python32.png) Python|`aws_solutions_constructs.aws_sns_lambda`|
|![Typescript Logo](https://docs.aws.amazon.com/cdk/api/latest/img/typescript32.png) Typescript|`@aws-solutions-constructs/aws-sns-lambda`|
|![Java Logo](https://docs.aws.amazon.com/cdk/api/latest/img/java32.png) Java|`software.amazon.awsconstructs.services.snslambda`|

This AWS Solutions Construct implements an Amazon SNS connected to an AWS Lambda function.

Here is a minimal deployable pattern definition:

```javascript
const { SnsToLambdaProps, SnsToLambda } = require('@aws-solutions-constructs/aws-sns-lambda');

const stack = new Stack(app, 'test-sns-lambda');

// Definitions
const props: SnsToLambdaProps = {
    deployLambda: true,
    lambdaFunctionProps: {
        runtime: lambda.Runtime.NODEJS_12_X,
        handler: 'index.handler',
        code: lambda.Code.asset(`${__dirname}/lambda`)
    }
};

new SnsToLambda(stack, 'test-sns-lambda', props);

```

## Initializer

```text
new SnsToLambda(scope: Construct, id: string, props: SnsToLambdaProps);
```

*Parameters*

* scope [`Construct`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_core.Construct.html)
* id `string`
* props [`S3ToLambdaProps`](#pattern-construct-props)

## Pattern Construct Props

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|deployLambda|`boolean`|Whether to create a new Lambda function or use an existing Lambda function. If set to false, you must provide an existing function for the `existingLambdaObj` property.|
|existingLambdaObj?|[`lambda.Function`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-lambda.Function.html)|An optional, existing Lambda function. This property is required if `deployLambda` is set to false.|
|lambdaFunctionProps?|[`lambda.FunctionProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-lambda.FunctionProps.html)|Optional user-provided props to override the default props for the lambda function|
|topicProps?|[`sns.TopicProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-sns.TopicProps.html)|Optional user provided properties to override the default properties for the SNS topic.|
|enableEncryption?|`boolean`|Use a KMS Key, either managed by this CDK app, or imported. If importing an encryption key, it must be specified in the encryptionKey property for this construct.|
|encryptionKey?|[`kms.Key`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-kms.Key.html)|An optional, imported encryption key to encrypt the SNS topic with.|

## Pattern Properties

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|lambdaFunction|[`lambda.Function`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-lambda.Function.html)|Returns an instance of the Lambda function created by the pattern.|
|snsTopic|[`sns.Topic`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-sns.Topic.html)|Returns an instance of the SNS topic created by the pattern.|

## Default settings

Out of the box implementation of the Construct without any override will set the following defaults:

### Amazon SNS Topic

* Configure least privilege access permissions for SNS Topic
* Enable server-side encryption forSNS Topic using Customer managed KMS Key

### AWS Lambda Function

* Configure least privilege access IAM role for Lambda function
* Enable reusing connections with Keep-Alive for NodeJs Lambda function

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

import aws_cdk.aws_kms
import aws_cdk.aws_lambda
import aws_cdk.aws_sns
import aws_cdk.core


class SnsToLambda(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-solutions-constructs/aws-sns-lambda.SnsToLambda"):
    """
    summary:
    :summary:: The SnsToLambda class.
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, deploy_lambda: bool, enable_encryption: typing.Optional[bool]=None, encryption_key: typing.Optional[aws_cdk.aws_kms.Key]=None, existing_lambda_obj: typing.Optional[aws_cdk.aws_lambda.Function]=None, lambda_function_props: typing.Any=None, topic_props: typing.Any=None) -> None:
        """
        :param scope: - represents the scope for all the resources.
        :param id: - this is a a scope-unique id.
        :param deploy_lambda: Whether to create a new Lambda function or use an existing Lambda function. If set to false, you must provide an existing function for the ``existingLambdaObj`` property. Default: - true
        :param enable_encryption: Use a KMS Key, either managed by this CDK app, or imported. If importing an encryption key, it must be specified in the encryptionKey property for this construct. Default: - true (encryption enabled, managed by this CDK app).
        :param encryption_key: An optional, imported encryption key to encrypt the SNS topic with. Default: - not specified.
        :param existing_lambda_obj: Existing instance of Lambda Function object. If ``deploy`` is set to false only then this property is required Default: - None
        :param lambda_function_props: Optional user provided properties to override the default properties for the Lambda function. If ``deploy`` is set to true only then this property is required. Default: - Default properties are used.
        :param topic_props: Optional user provided properties to override the default properties for the SNS topic. Default: - Default properties are used.

        access:
        :access:: public
        since:
        :since:: 0.8.0
        summary:
        :summary:: Constructs a new instance of the LambdaToSns class.
        """
        props = SnsToLambdaProps(deploy_lambda=deploy_lambda, enable_encryption=enable_encryption, encryption_key=encryption_key, existing_lambda_obj=existing_lambda_obj, lambda_function_props=lambda_function_props, topic_props=topic_props)

        jsii.create(SnsToLambda, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="lambdaFunction")
    def lambda_function(self) -> aws_cdk.aws_lambda.Function:
        return jsii.get(self, "lambdaFunction")

    @builtins.property
    @jsii.member(jsii_name="snsTopic")
    def sns_topic(self) -> aws_cdk.aws_sns.Topic:
        return jsii.get(self, "snsTopic")


@jsii.data_type(jsii_type="@aws-solutions-constructs/aws-sns-lambda.SnsToLambdaProps", jsii_struct_bases=[], name_mapping={'deploy_lambda': 'deployLambda', 'enable_encryption': 'enableEncryption', 'encryption_key': 'encryptionKey', 'existing_lambda_obj': 'existingLambdaObj', 'lambda_function_props': 'lambdaFunctionProps', 'topic_props': 'topicProps'})
class SnsToLambdaProps():
    def __init__(self, *, deploy_lambda: bool, enable_encryption: typing.Optional[bool]=None, encryption_key: typing.Optional[aws_cdk.aws_kms.Key]=None, existing_lambda_obj: typing.Optional[aws_cdk.aws_lambda.Function]=None, lambda_function_props: typing.Any=None, topic_props: typing.Any=None) -> None:
        """
        :param deploy_lambda: Whether to create a new Lambda function or use an existing Lambda function. If set to false, you must provide an existing function for the ``existingLambdaObj`` property. Default: - true
        :param enable_encryption: Use a KMS Key, either managed by this CDK app, or imported. If importing an encryption key, it must be specified in the encryptionKey property for this construct. Default: - true (encryption enabled, managed by this CDK app).
        :param encryption_key: An optional, imported encryption key to encrypt the SNS topic with. Default: - not specified.
        :param existing_lambda_obj: Existing instance of Lambda Function object. If ``deploy`` is set to false only then this property is required Default: - None
        :param lambda_function_props: Optional user provided properties to override the default properties for the Lambda function. If ``deploy`` is set to true only then this property is required. Default: - Default properties are used.
        :param topic_props: Optional user provided properties to override the default properties for the SNS topic. Default: - Default properties are used.

        summary:
        :summary:: The properties for the SnsToLambda class.
        """
        self._values = {
            'deploy_lambda': deploy_lambda,
        }
        if enable_encryption is not None: self._values["enable_encryption"] = enable_encryption
        if encryption_key is not None: self._values["encryption_key"] = encryption_key
        if existing_lambda_obj is not None: self._values["existing_lambda_obj"] = existing_lambda_obj
        if lambda_function_props is not None: self._values["lambda_function_props"] = lambda_function_props
        if topic_props is not None: self._values["topic_props"] = topic_props

    @builtins.property
    def deploy_lambda(self) -> bool:
        """Whether to create a new Lambda function or use an existing Lambda function.

        If set to false, you must provide an existing function for the ``existingLambdaObj`` property.

        default
        :default: - true
        """
        return self._values.get('deploy_lambda')

    @builtins.property
    def enable_encryption(self) -> typing.Optional[bool]:
        """Use a KMS Key, either managed by this CDK app, or imported.

        If importing an encryption key, it must be specified in
        the encryptionKey property for this construct.

        default
        :default: - true (encryption enabled, managed by this CDK app).
        """
        return self._values.get('enable_encryption')

    @builtins.property
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.Key]:
        """An optional, imported encryption key to encrypt the SNS topic with.

        default
        :default: - not specified.
        """
        return self._values.get('encryption_key')

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

    @builtins.property
    def topic_props(self) -> typing.Any:
        """Optional user provided properties to override the default properties for the SNS topic.

        default
        :default: - Default properties are used.
        """
        return self._values.get('topic_props')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SnsToLambdaProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "SnsToLambda",
    "SnsToLambdaProps",
]

publication.publish()
