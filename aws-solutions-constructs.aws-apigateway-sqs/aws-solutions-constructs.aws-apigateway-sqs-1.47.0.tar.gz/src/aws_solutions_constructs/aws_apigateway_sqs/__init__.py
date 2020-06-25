"""
# aws-apigateway-sqs module

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
|![Python Logo](https://docs.aws.amazon.com/cdk/api/latest/img/python32.png) Python|`aws_solutions_constructs.aws_apigateway_sqs`|
|![Typescript Logo](https://docs.aws.amazon.com/cdk/api/latest/img/typescript32.png) Typescript|`@aws-solutions-constructs/aws-apigateway-sqs`|
|![Java Logo](https://docs.aws.amazon.com/cdk/api/latest/img/java32.png) Java|`software.amazon.awsconstructs.services.apigatewaysqs`|

## Overview

This AWS Solutions Construct implements an Amazon API Gateway connected to an Amazon SQS queue pattern.

Here is a minimal deployable pattern definition:

```javascript
const { ApiGatewayToSqs } = require('@aws-solutions-constructs/aws-apigateway-sqs');

new ApiGatewayToSqs(stack, 'ApiGatewayToSqsPattern', {
    apiGatewayProps: {},
    queueProps: {},
    deployDeadLetterQueue?: true,
    maxReceiveCount?: 3
});

```

## Initializer

```text
new ApiGatewayToSqs(scope: Construct, id: string, props: ApiGatewayToSqsProps);
```

*Parameters*

* scope [`Construct`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_core.Construct.html)
* id `string`
* props [`ApiGatewayToSqsProps`](#pattern-construct-props)

## Pattern Construct Props

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|apiGatewayProps?|[`api.RestApiProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-apigateway.RestApiProps.html)|Optional user-provided props to override the default props for the API Gateway.|
|queueProps?|[`sqs.QueueProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-sqs.QueueProps.html)|Optional user-provided props to override the default props for the queue.|
|deployDeadLetterQueue|`boolean`|Whether to deploy a secondary queue to be used as a dead letter queue.|
|maxReceiveCount|`number`|The number of times a message can be unsuccessfully dequeued before being moved to the dead-letter queue.|
|allowCreateOperation?|`boolean`|Whether to deploy an API Gateway Method for Create operations on the queue (i.e. sqs:SendMessage).|
|createRequestTemplate?|`string`|API Gateway Request template for Create method, required if allowCreateOperation set to true.|
|allowReadOperation?|`boolean`|Whether to deploy an API Gateway Method for Read operations on the queue (i.e. sqs:ReceiveMessage).|
|allowDeleteOperation?|`boolean`|Whether to deploy an API Gateway Method for Delete operations on the queue (i.e. sqs:DeleteMessage).|

## Pattern Properties

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|apiGateway|[`api.RestApi`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-apigateway.RestApi.html)|Returns an instance of the API Gateway REST API created by the pattern.|
|apiGatewayRole|[`iam.Role`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-iam.Role.html)|Returns an instance of the iam.Role created by the construct for API Gateway.|
|sqsQueue|[`sqs.Queue`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-sqs.Queue.html)|Returns an instance of the SQS queue created by the pattern.|

## Sample API Usage

| **Method** | **Request Path** | **Request Body** | **Queue Action** | **Description** |
|:-------------|:----------------|-----------------|-----------------|-----------------|
|GET|`/`| |`sqs::ReceiveMessage`|Retrieves a message from the queue.|
|POST|`/`| `{ "data": "Hello World!" }` |`sqs::SendMessage`|Delivers a message to the queue.|
|DELETE|`/message?receiptHandle=[value]`||`sqs::DeleteMessage`|Deletes a specified message from the queue|

## Default settings

Out of the box implementation of the Construct without any override will set the following defaults:

### Amazon API Gateway

* Deploy an edge-optimized API endpoint
* Enable CloudWatch logging for API Gateway
* Configure least privilege access IAM role for API Gateway
* Set the default authorizationType for all API methods to IAM

### Amazon SQS Queue

* Deploy SQS dead-letter queue for the source SQS Queue
* Enable server-side encryption for source SQS Queue using AWS Managed KMS Key

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

import aws_cdk.aws_apigateway
import aws_cdk.aws_iam
import aws_cdk.aws_sqs
import aws_cdk.core


class ApiGatewayToSqs(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-solutions-constructs/aws-apigateway-sqs.ApiGatewayToSqs"):
    """
    summary:
    :summary:: The ApiGatewayToSqs class.
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, allow_create_operation: typing.Optional[bool]=None, allow_delete_operation: typing.Optional[bool]=None, allow_read_operation: typing.Optional[bool]=None, api_gateway_props: typing.Any=None, create_request_template: typing.Optional[str]=None, deploy_dead_letter_queue: typing.Optional[bool]=None, max_receive_count: typing.Optional[jsii.Number]=None, queue_props: typing.Any=None) -> None:
        """
        :param scope: - represents the scope for all the resources.
        :param id: - this is a a scope-unique id.
        :param allow_create_operation: Whether to deploy an API Gateway Method for Create operations on the queue (i.e. sqs:SendMessage). Default: - false
        :param allow_delete_operation: Whether to deploy an API Gateway Method for Delete operations on the queue (i.e. sqs:DeleteMessage). Default: - false
        :param allow_read_operation: Whether to deploy an API Gateway Method for Read operations on the queue (i.e. sqs:ReceiveMessage). Default: - false
        :param api_gateway_props: Optional user-provided props to override the default props for the API Gateway. Default: - Default properties are used.
        :param create_request_template: API Gateway Request template for Create method, required if allowCreateOperation set to true. Default: - None
        :param deploy_dead_letter_queue: Whether to deploy a secondary queue to be used as a dead letter queue. Default: - required field.
        :param max_receive_count: The number of times a message can be unsuccessfully dequeued before being moved to the dead-letter queue. Default: - required only if deployDeadLetterQueue = true.
        :param queue_props: Optional user-provided props to override the default props for the queue. Default: - Default props are used

        access:
        :access:: public
        since:
        :since:: 0.8.0
        summary:
        :summary:: Constructs a new instance of the ApiGatewayToSqs class.
        """
        props = ApiGatewayToSqsProps(allow_create_operation=allow_create_operation, allow_delete_operation=allow_delete_operation, allow_read_operation=allow_read_operation, api_gateway_props=api_gateway_props, create_request_template=create_request_template, deploy_dead_letter_queue=deploy_dead_letter_queue, max_receive_count=max_receive_count, queue_props=queue_props)

        jsii.create(ApiGatewayToSqs, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="apiGateway")
    def api_gateway(self) -> aws_cdk.aws_apigateway.RestApi:
        return jsii.get(self, "apiGateway")

    @builtins.property
    @jsii.member(jsii_name="apiGatewayRole")
    def api_gateway_role(self) -> aws_cdk.aws_iam.Role:
        return jsii.get(self, "apiGatewayRole")

    @builtins.property
    @jsii.member(jsii_name="sqsQueue")
    def sqs_queue(self) -> aws_cdk.aws_sqs.Queue:
        return jsii.get(self, "sqsQueue")


@jsii.data_type(jsii_type="@aws-solutions-constructs/aws-apigateway-sqs.ApiGatewayToSqsProps", jsii_struct_bases=[], name_mapping={'allow_create_operation': 'allowCreateOperation', 'allow_delete_operation': 'allowDeleteOperation', 'allow_read_operation': 'allowReadOperation', 'api_gateway_props': 'apiGatewayProps', 'create_request_template': 'createRequestTemplate', 'deploy_dead_letter_queue': 'deployDeadLetterQueue', 'max_receive_count': 'maxReceiveCount', 'queue_props': 'queueProps'})
class ApiGatewayToSqsProps():
    def __init__(self, *, allow_create_operation: typing.Optional[bool]=None, allow_delete_operation: typing.Optional[bool]=None, allow_read_operation: typing.Optional[bool]=None, api_gateway_props: typing.Any=None, create_request_template: typing.Optional[str]=None, deploy_dead_letter_queue: typing.Optional[bool]=None, max_receive_count: typing.Optional[jsii.Number]=None, queue_props: typing.Any=None) -> None:
        """
        :param allow_create_operation: Whether to deploy an API Gateway Method for Create operations on the queue (i.e. sqs:SendMessage). Default: - false
        :param allow_delete_operation: Whether to deploy an API Gateway Method for Delete operations on the queue (i.e. sqs:DeleteMessage). Default: - false
        :param allow_read_operation: Whether to deploy an API Gateway Method for Read operations on the queue (i.e. sqs:ReceiveMessage). Default: - false
        :param api_gateway_props: Optional user-provided props to override the default props for the API Gateway. Default: - Default properties are used.
        :param create_request_template: API Gateway Request template for Create method, required if allowCreateOperation set to true. Default: - None
        :param deploy_dead_letter_queue: Whether to deploy a secondary queue to be used as a dead letter queue. Default: - required field.
        :param max_receive_count: The number of times a message can be unsuccessfully dequeued before being moved to the dead-letter queue. Default: - required only if deployDeadLetterQueue = true.
        :param queue_props: Optional user-provided props to override the default props for the queue. Default: - Default props are used

        summary:
        :summary:: The properties for the ApiGatewayToSqs class.
        """
        self._values = {
        }
        if allow_create_operation is not None: self._values["allow_create_operation"] = allow_create_operation
        if allow_delete_operation is not None: self._values["allow_delete_operation"] = allow_delete_operation
        if allow_read_operation is not None: self._values["allow_read_operation"] = allow_read_operation
        if api_gateway_props is not None: self._values["api_gateway_props"] = api_gateway_props
        if create_request_template is not None: self._values["create_request_template"] = create_request_template
        if deploy_dead_letter_queue is not None: self._values["deploy_dead_letter_queue"] = deploy_dead_letter_queue
        if max_receive_count is not None: self._values["max_receive_count"] = max_receive_count
        if queue_props is not None: self._values["queue_props"] = queue_props

    @builtins.property
    def allow_create_operation(self) -> typing.Optional[bool]:
        """Whether to deploy an API Gateway Method for Create operations on the queue (i.e. sqs:SendMessage).

        default
        :default: - false
        """
        return self._values.get('allow_create_operation')

    @builtins.property
    def allow_delete_operation(self) -> typing.Optional[bool]:
        """Whether to deploy an API Gateway Method for Delete operations on the queue (i.e. sqs:DeleteMessage).

        default
        :default: - false
        """
        return self._values.get('allow_delete_operation')

    @builtins.property
    def allow_read_operation(self) -> typing.Optional[bool]:
        """Whether to deploy an API Gateway Method for Read operations on the queue (i.e. sqs:ReceiveMessage).

        default
        :default: - false
        """
        return self._values.get('allow_read_operation')

    @builtins.property
    def api_gateway_props(self) -> typing.Any:
        """Optional user-provided props to override the default props for the API Gateway.

        default
        :default: - Default properties are used.
        """
        return self._values.get('api_gateway_props')

    @builtins.property
    def create_request_template(self) -> typing.Optional[str]:
        """API Gateway Request template for Create method, required if allowCreateOperation set to true.

        default
        :default: - None
        """
        return self._values.get('create_request_template')

    @builtins.property
    def deploy_dead_letter_queue(self) -> typing.Optional[bool]:
        """Whether to deploy a secondary queue to be used as a dead letter queue.

        default
        :default: - required field.
        """
        return self._values.get('deploy_dead_letter_queue')

    @builtins.property
    def max_receive_count(self) -> typing.Optional[jsii.Number]:
        """The number of times a message can be unsuccessfully dequeued before being moved to the dead-letter queue.

        default
        :default: - required only if deployDeadLetterQueue = true.
        """
        return self._values.get('max_receive_count')

    @builtins.property
    def queue_props(self) -> typing.Any:
        """Optional user-provided props to override the default props for the queue.

        default
        :default: - Default props are used
        """
        return self._values.get('queue_props')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ApiGatewayToSqsProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "ApiGatewayToSqs",
    "ApiGatewayToSqsProps",
]

publication.publish()
