"""
# aws-sqs-lambda module

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
|![Java Logo](https://docs.aws.amazon.com/cdk/api/latest/img/java32.png) Java|`software.amazon.awsconstructs.services.sqslambda`|

This AWS Solutions Construct implements an Amazon SQS queue connected to an AWS Lambda function.

Here is a minimal deployable pattern definition:

```javascript
const { SqsToLambda } = require('@aws-solutions-constructs/aws-sqs-lambda');

new SqsToLambda(stack, 'SqsToLambdaPattern', {
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
new SqsToLambda(scope: Construct, id: string, props: SqsToLambdaProps);
```

*Parameters*

* scope [`Construct`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_core.Construct.html)
* id `string`
* props [`SqsToLambdaProps`](#pattern-construct-props)

## Pattern Construct Props

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|deployLambda|`boolean`|Whether to create a new Lambda function or use an existing Lambda function.|
|existingLambdaObj?|[`lambda.Function`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-lambda.Function.html)|An optional, existing Lambda function.|
|lambdaFunctionProps?|[`lambda.FunctionProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-lambda.FunctionProps.html)|Optional user-provided props to override the default props for the Lambda function.|
|queueProps?|[`sqs.QueueProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-sqs.QueueProps.html)|Optional user-provided props to override the default props for the SQS queue.|
|deployDeadLetterQueue?|`boolean`|Whether to create a secondary queue to be used as a dead letter queue. Defaults to true.|
|maxReceiveCount?|`number`|The number of times a message can be unsuccessfully dequeued before being moved to the dead letter queue. Defaults to 15.|

## Pattern Properties

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|lambdaFunction|[`lambda.Function`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-lambda.Function.html)|Returns an instance of the Lambda function created by the pattern.|
|sqsQueue|[`sqs.Queue`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-sqs.Queue.html)|Returns an instance of the SQS queue created by the pattern.|

## Default settings

Out of the box implementation of the Construct without any override will set the following defaults:

### Amazon SQS Queue

* Deploy SQS dead-letter queue for the source SQS Queue
* Enable server-side encryption for source SQS Queue using AWS Managed KMS Key

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

import aws_cdk.aws_lambda
import aws_cdk.aws_sqs
import aws_cdk.core


class SqsToLambda(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-solutions-constructs/aws-sqs-lambda.SqsToLambda"):
    """
    summary:
    :summary:: The SqsToLambda class.
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, deploy_lambda: bool, deploy_dead_letter_queue: typing.Optional[bool]=None, existing_lambda_obj: typing.Optional[aws_cdk.aws_lambda.Function]=None, lambda_function_props: typing.Any=None, max_receive_count: typing.Optional[jsii.Number]=None, queue_props: typing.Any=None) -> None:
        """
        :param scope: - represents the scope for all the resources.
        :param id: - this is a a scope-unique id.
        :param deploy_lambda: Whether to create a new Lambda function or use an existing Lambda function. If set to false, you must provide an existing function for the ``existingLambdaObj`` property. Default: - true
        :param deploy_dead_letter_queue: Whether to deploy a secondary queue to be used as a dead letter queue. Default: - true.
        :param existing_lambda_obj: Existing instance of Lambda Function object. If ``deploy`` is set to false only then this property is required Default: - None
        :param lambda_function_props: Optional user provided properties to override the default properties for the Lambda function. If ``deploy`` is set to true only then this property is required. Default: - Default properties are used.
        :param max_receive_count: The number of times a message can be unsuccessfully dequeued before being moved to the dead-letter queue. Default: - required field if deployDeadLetterQueue=true.
        :param queue_props: Optional user provided properties. Default: - Default props are used

        access:
        :access:: public
        since:
        :since:: 0.8.0
        summary:
        :summary:: Constructs a new instance of the SqsToLambda class.
        """
        props = SqsToLambdaProps(deploy_lambda=deploy_lambda, deploy_dead_letter_queue=deploy_dead_letter_queue, existing_lambda_obj=existing_lambda_obj, lambda_function_props=lambda_function_props, max_receive_count=max_receive_count, queue_props=queue_props)

        jsii.create(SqsToLambda, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="lambdaFunction")
    def lambda_function(self) -> aws_cdk.aws_lambda.Function:
        return jsii.get(self, "lambdaFunction")

    @builtins.property
    @jsii.member(jsii_name="sqsQueue")
    def sqs_queue(self) -> aws_cdk.aws_sqs.Queue:
        return jsii.get(self, "sqsQueue")


@jsii.data_type(jsii_type="@aws-solutions-constructs/aws-sqs-lambda.SqsToLambdaProps", jsii_struct_bases=[], name_mapping={'deploy_lambda': 'deployLambda', 'deploy_dead_letter_queue': 'deployDeadLetterQueue', 'existing_lambda_obj': 'existingLambdaObj', 'lambda_function_props': 'lambdaFunctionProps', 'max_receive_count': 'maxReceiveCount', 'queue_props': 'queueProps'})
class SqsToLambdaProps():
    def __init__(self, *, deploy_lambda: bool, deploy_dead_letter_queue: typing.Optional[bool]=None, existing_lambda_obj: typing.Optional[aws_cdk.aws_lambda.Function]=None, lambda_function_props: typing.Any=None, max_receive_count: typing.Optional[jsii.Number]=None, queue_props: typing.Any=None) -> None:
        """
        :param deploy_lambda: Whether to create a new Lambda function or use an existing Lambda function. If set to false, you must provide an existing function for the ``existingLambdaObj`` property. Default: - true
        :param deploy_dead_letter_queue: Whether to deploy a secondary queue to be used as a dead letter queue. Default: - true.
        :param existing_lambda_obj: Existing instance of Lambda Function object. If ``deploy`` is set to false only then this property is required Default: - None
        :param lambda_function_props: Optional user provided properties to override the default properties for the Lambda function. If ``deploy`` is set to true only then this property is required. Default: - Default properties are used.
        :param max_receive_count: The number of times a message can be unsuccessfully dequeued before being moved to the dead-letter queue. Default: - required field if deployDeadLetterQueue=true.
        :param queue_props: Optional user provided properties. Default: - Default props are used

        summary:
        :summary:: The properties for the SqsToLambda class.
        """
        self._values = {
            'deploy_lambda': deploy_lambda,
        }
        if deploy_dead_letter_queue is not None: self._values["deploy_dead_letter_queue"] = deploy_dead_letter_queue
        if existing_lambda_obj is not None: self._values["existing_lambda_obj"] = existing_lambda_obj
        if lambda_function_props is not None: self._values["lambda_function_props"] = lambda_function_props
        if max_receive_count is not None: self._values["max_receive_count"] = max_receive_count
        if queue_props is not None: self._values["queue_props"] = queue_props

    @builtins.property
    def deploy_lambda(self) -> bool:
        """Whether to create a new Lambda function or use an existing Lambda function.

        If set to false, you must provide an existing function for the ``existingLambdaObj`` property.

        default
        :default: - true
        """
        return self._values.get('deploy_lambda')

    @builtins.property
    def deploy_dead_letter_queue(self) -> typing.Optional[bool]:
        """Whether to deploy a secondary queue to be used as a dead letter queue.

        default
        :default: - true.
        """
        return self._values.get('deploy_dead_letter_queue')

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
    def max_receive_count(self) -> typing.Optional[jsii.Number]:
        """The number of times a message can be unsuccessfully dequeued before being moved to the dead-letter queue.

        default
        :default: - required field if deployDeadLetterQueue=true.
        """
        return self._values.get('max_receive_count')

    @builtins.property
    def queue_props(self) -> typing.Any:
        """Optional user provided properties.

        default
        :default: - Default props are used
        """
        return self._values.get('queue_props')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SqsToLambdaProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "SqsToLambda",
    "SqsToLambdaProps",
]

publication.publish()
