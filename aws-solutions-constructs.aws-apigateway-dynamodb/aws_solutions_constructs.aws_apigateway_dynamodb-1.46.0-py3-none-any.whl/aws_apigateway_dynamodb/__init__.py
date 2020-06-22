"""
# aws-apigateway-dynamodb module

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
|![Python Logo](https://docs.aws.amazon.com/cdk/api/latest/img/python32.png) Python|`aws_solutions_constructs.aws_apigateway_dynamodb`|
|![Typescript Logo](https://docs.aws.amazon.com/cdk/api/latest/img/typescript32.png) Typescript|`@aws-solutions-constructs/aws-apigateway-dynamodb`|
|![Java Logo](https://docs.aws.amazon.com/cdk/api/latest/img/java32.png) Java|`software.amazon.awsconstructs.services.apigatewaydynamodb`|

## Overview

This AWS Solutions Construct implements an Amazon API Gateway REST API connected to Amazon DynamoDB table.

Here is a minimal deployable pattern definition:

```javascript
import { ApiGatewayToDynamoDBProps, ApiGatewayToDynamoDB } from "@aws-solutions-constructs/aws-apigateway-dynamodb";

const props: ApiGatewayToDynamoDBProps = {};

new ApiGatewayToDynamoDB(stack, 'test-api-gateway-dynamodb-default', props);

```

## Initializer

```text
new ApiGatewayToDynamoDB(scope: Construct, id: string, props: ApiGatewayToDynamoDBProps);
```

*Parameters*

* scope [`Construct`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_core.Construct.html)
* id `string`
* props [`ApiGatewayToDynamoDBProps`](#pattern-construct-props)

## Pattern Construct Props

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|dynamoTableProps|[`dynamodb.TableProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-dynamodb.TableProps.html)|Optional user provided props to override the default props for DynamoDB Table|
|apiGatewayProps?|[`api.RestApiProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-apigateway.RestApiProps.html)|Optional user-provided props to override the default props for the API Gateway.|
|allowCreateOperation|`boolean`|Whether to deploy API Gateway Method for Create operation on DynamoDB table.|
|createRequestTemplate|`string`|API Gateway Request template for Create method, required if allowCreateOperation set to true|
|allowReadOperation|`boolean`|Whether to deploy API Gateway Method for Read operation on DynamoDB table.|
|allowUpdateOperation|`boolean`|Whether to deploy API Gateway Method for Update operation on DynamoDB table.|
|updateRequestTemplate|`string`|API Gateway Request template for Update method, required if allowUpdateOperation set to true|
|allowDeleteOperation|`boolean`|Whether to deploy API Gateway Method for Delete operation on DynamoDB table.|

## Pattern Properties

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|apiGateway|[`api.RestApi`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-apigateway.RestApi.html)|Returns an instance of the api.RestApi created by the construct.|
|apiGatewayRole|[`iam.Role`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-iam.Role.html)|Returns an instance of the iam.Role created by the construct for API Gateway.|
|dynamoTable|[`dynamodb.Table`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-dynamodb.Table.html)|Returns an instance of dynamodb.Table created by the construct.|

## Default settings

Out of the box implementation of the Construct without any override will set the following defaults:

### Amazon API Gateway

* Deploy an edge-optimized API endpoint
* Enable CloudWatch logging for API Gateway
* Configure least privilege access IAM role for API Gateway
* Set the default authorizationType for all API methods to IAM

### Amazon DynamoDB Table

* Set the billing mode for DynamoDB Table to On-Demand (Pay per request)
* Enable server-side encryption for DynamoDB Table using AWS managed KMS Key
* Creates a partition key called 'id' for DynamoDB Table
* Retain the Table when deleting the CloudFormation stack

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
import aws_cdk.aws_dynamodb
import aws_cdk.aws_iam
import aws_cdk.core


class ApiGatewayToDynamoDB(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-solutions-constructs/aws-apigateway-dynamodb.ApiGatewayToDynamoDB"):
    """
    summary:
    :summary:: The ApiGatewayToDynamoDB class.
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, allow_create_operation: typing.Optional[bool]=None, allow_delete_operation: typing.Optional[bool]=None, allow_read_operation: typing.Optional[bool]=None, allow_update_operation: typing.Optional[bool]=None, api_gateway_props: typing.Any=None, create_request_template: typing.Optional[str]=None, dynamo_table_props: typing.Optional[aws_cdk.aws_dynamodb.TableProps]=None, update_request_template: typing.Optional[str]=None) -> None:
        """
        :param scope: - represents the scope for all the resources.
        :param id: - this is a a scope-unique id.
        :param allow_create_operation: Whether to deploy API Gateway Method for Create operation on DynamoDB table. Default: - false
        :param allow_delete_operation: Whether to deploy API Gateway Method for Delete operation on DynamoDB table. Default: - false
        :param allow_read_operation: Whether to deploy API Gateway Method for Read operation on DynamoDB table. Default: - true
        :param allow_update_operation: Whether to deploy API Gateway Method for Update operation on DynamoDB table. Default: - false
        :param api_gateway_props: Optional user-provided props to override the default props for the API Gateway. Default: - Default properties are used.
        :param create_request_template: API Gateway Request template for Create method, required if allowCreateOperation set to true. Default: - None
        :param dynamo_table_props: Optional user provided props to override the default props. Default: - Default props are used
        :param update_request_template: API Gateway Request template for Update method, required if allowUpdateOperation set to true. Default: - None

        access:
        :access:: public
        since:
        :since:: 0.8.0
        summary:
        :summary:: Constructs a new instance of the ApiGatewayToDynamoDB class.
        """
        props = ApiGatewayToDynamoDBProps(allow_create_operation=allow_create_operation, allow_delete_operation=allow_delete_operation, allow_read_operation=allow_read_operation, allow_update_operation=allow_update_operation, api_gateway_props=api_gateway_props, create_request_template=create_request_template, dynamo_table_props=dynamo_table_props, update_request_template=update_request_template)

        jsii.create(ApiGatewayToDynamoDB, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="apiGateway")
    def api_gateway(self) -> aws_cdk.aws_apigateway.RestApi:
        return jsii.get(self, "apiGateway")

    @builtins.property
    @jsii.member(jsii_name="apiGatewayRole")
    def api_gateway_role(self) -> aws_cdk.aws_iam.Role:
        return jsii.get(self, "apiGatewayRole")

    @builtins.property
    @jsii.member(jsii_name="dynamoTable")
    def dynamo_table(self) -> aws_cdk.aws_dynamodb.Table:
        return jsii.get(self, "dynamoTable")


@jsii.data_type(jsii_type="@aws-solutions-constructs/aws-apigateway-dynamodb.ApiGatewayToDynamoDBProps", jsii_struct_bases=[], name_mapping={'allow_create_operation': 'allowCreateOperation', 'allow_delete_operation': 'allowDeleteOperation', 'allow_read_operation': 'allowReadOperation', 'allow_update_operation': 'allowUpdateOperation', 'api_gateway_props': 'apiGatewayProps', 'create_request_template': 'createRequestTemplate', 'dynamo_table_props': 'dynamoTableProps', 'update_request_template': 'updateRequestTemplate'})
class ApiGatewayToDynamoDBProps():
    def __init__(self, *, allow_create_operation: typing.Optional[bool]=None, allow_delete_operation: typing.Optional[bool]=None, allow_read_operation: typing.Optional[bool]=None, allow_update_operation: typing.Optional[bool]=None, api_gateway_props: typing.Any=None, create_request_template: typing.Optional[str]=None, dynamo_table_props: typing.Optional[aws_cdk.aws_dynamodb.TableProps]=None, update_request_template: typing.Optional[str]=None) -> None:
        """
        :param allow_create_operation: Whether to deploy API Gateway Method for Create operation on DynamoDB table. Default: - false
        :param allow_delete_operation: Whether to deploy API Gateway Method for Delete operation on DynamoDB table. Default: - false
        :param allow_read_operation: Whether to deploy API Gateway Method for Read operation on DynamoDB table. Default: - true
        :param allow_update_operation: Whether to deploy API Gateway Method for Update operation on DynamoDB table. Default: - false
        :param api_gateway_props: Optional user-provided props to override the default props for the API Gateway. Default: - Default properties are used.
        :param create_request_template: API Gateway Request template for Create method, required if allowCreateOperation set to true. Default: - None
        :param dynamo_table_props: Optional user provided props to override the default props. Default: - Default props are used
        :param update_request_template: API Gateway Request template for Update method, required if allowUpdateOperation set to true. Default: - None

        summary:
        :summary:: The properties for the ApiGatewayToDynamoDB class.
        """
        if isinstance(dynamo_table_props, dict): dynamo_table_props = aws_cdk.aws_dynamodb.TableProps(**dynamo_table_props)
        self._values = {
        }
        if allow_create_operation is not None: self._values["allow_create_operation"] = allow_create_operation
        if allow_delete_operation is not None: self._values["allow_delete_operation"] = allow_delete_operation
        if allow_read_operation is not None: self._values["allow_read_operation"] = allow_read_operation
        if allow_update_operation is not None: self._values["allow_update_operation"] = allow_update_operation
        if api_gateway_props is not None: self._values["api_gateway_props"] = api_gateway_props
        if create_request_template is not None: self._values["create_request_template"] = create_request_template
        if dynamo_table_props is not None: self._values["dynamo_table_props"] = dynamo_table_props
        if update_request_template is not None: self._values["update_request_template"] = update_request_template

    @builtins.property
    def allow_create_operation(self) -> typing.Optional[bool]:
        """Whether to deploy API Gateway Method for Create operation on DynamoDB table.

        default
        :default: - false
        """
        return self._values.get('allow_create_operation')

    @builtins.property
    def allow_delete_operation(self) -> typing.Optional[bool]:
        """Whether to deploy API Gateway Method for Delete operation on DynamoDB table.

        default
        :default: - false
        """
        return self._values.get('allow_delete_operation')

    @builtins.property
    def allow_read_operation(self) -> typing.Optional[bool]:
        """Whether to deploy API Gateway Method for Read operation on DynamoDB table.

        default
        :default: - true
        """
        return self._values.get('allow_read_operation')

    @builtins.property
    def allow_update_operation(self) -> typing.Optional[bool]:
        """Whether to deploy API Gateway Method for Update operation on DynamoDB table.

        default
        :default: - false
        """
        return self._values.get('allow_update_operation')

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
    def dynamo_table_props(self) -> typing.Optional[aws_cdk.aws_dynamodb.TableProps]:
        """Optional user provided props to override the default props.

        default
        :default: - Default props are used
        """
        return self._values.get('dynamo_table_props')

    @builtins.property
    def update_request_template(self) -> typing.Optional[str]:
        """API Gateway Request template for Update method, required if allowUpdateOperation set to true.

        default
        :default: - None
        """
        return self._values.get('update_request_template')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ApiGatewayToDynamoDBProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "ApiGatewayToDynamoDB",
    "ApiGatewayToDynamoDBProps",
]

publication.publish()
