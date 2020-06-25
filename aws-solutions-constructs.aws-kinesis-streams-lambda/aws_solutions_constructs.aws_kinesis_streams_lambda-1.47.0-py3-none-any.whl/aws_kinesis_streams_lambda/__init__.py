"""
# aws-kinesisstreams-lambda module

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
|![Python Logo](https://docs.aws.amazon.com/cdk/api/latest/img/python32.png) Python|`aws_solutions_constructs.aws_kinesisstreams_lambda`|
|![Typescript Logo](https://docs.aws.amazon.com/cdk/api/latest/img/typescript32.png) Typescript|`@aws-solutions-constructs/aws-kinesisstreams-lambda`|
|![Java Logo](https://docs.aws.amazon.com/cdk/api/latest/img/java32.png) Java|`software.amazon.awsconstructs.services.kinesisstreamslambda`|

This AWS Solutions Construct deploys a Kinesis Stream and Lambda function with the appropriate resources/properties for interaction and security.

Here is a minimal deployable pattern definition:

```javascript
const { KinesisStreamsToLambda } = require('@aws-solutions-constructs/aws-kinesisstreams-lambda');

new KinesisStreamsToLambda(stack, 'KinesisToLambdaPattern', {
    deployLambda: true,
    eventSourceProps: {
        startingPosition: lambda.StartingPosition.TRIM_HORIZON,
        batchSize: 1
    },
    lambdaFunctionProps: {
        runtime: lambda.Runtime.NODEJS_10_X,
        handler: 'index.handler',
        code: lambda.Code.asset(`${__dirname}/lambda`)
    }
});

```

## Initializer

```text
new KinesisStreamsToLambda(scope: Construct, id: string, props: KinesisStreamsToLambdaProps);
```

*Parameters*

* scope [`Construct`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_core.Construct.html)
* id `string`
* props [`KinesisStreamsToLambdaProps`](#pattern-construct-props)

## Pattern Construct Props

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|deployLambda|`boolean`|Whether to create a new Lambda function or use an existing Lambda function. If set to false, you must provide an existing function for the `existingLambdaObj` property.|
|existingLambdaObj?|[`lambda.Function`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-lambda.Function.html)|An optional, existing Lambda function. This property is required if `deployLambda` is set to false.|
|lambdaFunctionProps?|[`lambda.FunctionProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-lambda.FunctionProps.html)|Optional user-provided props to override the default props for the Lambda function. This property is only required if `deployLambda` is set to true.|
|kinesisStreamProps?|[`kinesis.StreamProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-kinesis.StreamProps.html)|Optional user-provided props to override the default props for the Kinesis stream.|
|eventSourceProps?|[`lambda.EventSourceMappingOptions`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-lambda.EventSourceMappingOptions.html)|Optional user-provided props to override the default props for the Lambda event source mapping.|

## Pattern Properties

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|kinesisStream|[`kinesis.Stream`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-kinesis.Stream.html)|Returns an instance of the Kinesis stream created by the pattern.|
|lambdaFunction|[`lambda.Function`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-lambda.Function.html)|Returns an instance of the Lambda function created by the pattern.|
|kinesisStreamRole|[`iam.Role`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-iam.Role.html)|Returns an instance of the iam.Role created by the construct for Kinesis stream.|

## Default settings

Out of the box implementation of the Construct without any override will set the following defaults:

### Amazon Kinesis Stream

* Configure least privilege access IAM role for Kinesis Stream
* Enable server-side encryption for Kinesis Stream using AWS Managed KMS Key

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

import aws_cdk.aws_iam
import aws_cdk.aws_kinesis
import aws_cdk.aws_lambda
import aws_cdk.core


class KinesisStreamsToLambda(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-solutions-constructs/aws-kinesisstreams-lambda.KinesisStreamsToLambda"):
    """
    summary:
    :summary:: The KinesisStreamsToLambda class.
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, deploy_lambda: bool, event_source_props: typing.Any=None, existing_lambda_obj: typing.Optional[aws_cdk.aws_lambda.Function]=None, kinesis_stream_props: typing.Any=None, lambda_function_props: typing.Any=None) -> None:
        """
        :param scope: - represents the scope for all the resources.
        :param id: - this is a a scope-unique id.
        :param deploy_lambda: Whether to create a new Lambda function or use an existing Lambda function. If set to false, you must provide an existing function for the ``existingLambdaObj`` property. Default: - true
        :param event_source_props: Optional user-provided props to override the default props for the Lambda event source mapping. Default: - Default props are used.
        :param existing_lambda_obj: An optional, existing Lambda function. This property is required if ``deployLambda`` is set to false. Default: - None
        :param kinesis_stream_props: Optional user-provided props to override the default props for the Kinesis stream. Default: - Default props are used.
        :param lambda_function_props: Optional user-provided props to override the default props for the Lambda function. This property is only required if ``deployLambda`` is set to true. Default: - Default props are used.

        access:
        :access:: public
        since:
        :since:: 0.8.0
        summary:
        :summary:: Constructs a new instance of the KinesisStreamsToLambda class.
        """
        props = KinesisStreamsToLambdaProps(deploy_lambda=deploy_lambda, event_source_props=event_source_props, existing_lambda_obj=existing_lambda_obj, kinesis_stream_props=kinesis_stream_props, lambda_function_props=lambda_function_props)

        jsii.create(KinesisStreamsToLambda, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="kinesisStream")
    def kinesis_stream(self) -> aws_cdk.aws_kinesis.Stream:
        return jsii.get(self, "kinesisStream")

    @builtins.property
    @jsii.member(jsii_name="kinesisStreamRole")
    def kinesis_stream_role(self) -> aws_cdk.aws_iam.Role:
        return jsii.get(self, "kinesisStreamRole")

    @builtins.property
    @jsii.member(jsii_name="lambdaFunction")
    def lambda_function(self) -> aws_cdk.aws_lambda.Function:
        return jsii.get(self, "lambdaFunction")


@jsii.data_type(jsii_type="@aws-solutions-constructs/aws-kinesisstreams-lambda.KinesisStreamsToLambdaProps", jsii_struct_bases=[], name_mapping={'deploy_lambda': 'deployLambda', 'event_source_props': 'eventSourceProps', 'existing_lambda_obj': 'existingLambdaObj', 'kinesis_stream_props': 'kinesisStreamProps', 'lambda_function_props': 'lambdaFunctionProps'})
class KinesisStreamsToLambdaProps():
    def __init__(self, *, deploy_lambda: bool, event_source_props: typing.Any=None, existing_lambda_obj: typing.Optional[aws_cdk.aws_lambda.Function]=None, kinesis_stream_props: typing.Any=None, lambda_function_props: typing.Any=None) -> None:
        """The properties for the KinesisStreamsToLambda class.

        :param deploy_lambda: Whether to create a new Lambda function or use an existing Lambda function. If set to false, you must provide an existing function for the ``existingLambdaObj`` property. Default: - true
        :param event_source_props: Optional user-provided props to override the default props for the Lambda event source mapping. Default: - Default props are used.
        :param existing_lambda_obj: An optional, existing Lambda function. This property is required if ``deployLambda`` is set to false. Default: - None
        :param kinesis_stream_props: Optional user-provided props to override the default props for the Kinesis stream. Default: - Default props are used.
        :param lambda_function_props: Optional user-provided props to override the default props for the Lambda function. This property is only required if ``deployLambda`` is set to true. Default: - Default props are used.
        """
        self._values = {
            'deploy_lambda': deploy_lambda,
        }
        if event_source_props is not None: self._values["event_source_props"] = event_source_props
        if existing_lambda_obj is not None: self._values["existing_lambda_obj"] = existing_lambda_obj
        if kinesis_stream_props is not None: self._values["kinesis_stream_props"] = kinesis_stream_props
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
    def event_source_props(self) -> typing.Any:
        """Optional user-provided props to override the default props for the Lambda event source mapping.

        default
        :default: - Default props are used.
        """
        return self._values.get('event_source_props')

    @builtins.property
    def existing_lambda_obj(self) -> typing.Optional[aws_cdk.aws_lambda.Function]:
        """An optional, existing Lambda function.

        This property is required if ``deployLambda`` is set to false.

        default
        :default: - None
        """
        return self._values.get('existing_lambda_obj')

    @builtins.property
    def kinesis_stream_props(self) -> typing.Any:
        """Optional user-provided props to override the default props for the Kinesis stream.

        default
        :default: - Default props are used.
        """
        return self._values.get('kinesis_stream_props')

    @builtins.property
    def lambda_function_props(self) -> typing.Any:
        """Optional user-provided props to override the default props for the Lambda function.

        This property is only required if ``deployLambda`` is set to true.

        default
        :default: - Default props are used.
        """
        return self._values.get('lambda_function_props')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'KinesisStreamsToLambdaProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "KinesisStreamsToLambda",
    "KinesisStreamsToLambdaProps",
]

publication.publish()
