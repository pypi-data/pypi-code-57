"""
# aws-cognito-apigateway-lambda module

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
|![Python Logo](https://docs.aws.amazon.com/cdk/api/latest/img/python32.png) Python|`aws_solutions_constructs.aws_cognito_apigateway_lambda`|
|![Typescript Logo](https://docs.aws.amazon.com/cdk/api/latest/img/typescript32.png) Typescript|`@aws-solutions-constructs/aws-cognito-apigateway-lambda`|
|![Java Logo](https://docs.aws.amazon.com/cdk/api/latest/img/java32.png) Java|`software.amazon.awsconstructs.services.cognitoapigatewaylambda`|

This AWS Solutions Construct implements an Amazon Cognito securing an Amazon API Gateway Lambda backed REST APIs pattern.

Here is a minimal deployable pattern definition:

```javascript
const { CognitoToApiGatewayToLambda } = require('@aws-solutions-constructs/aws-cognito-apigateway-lambda');

const stack = new Stack(app, 'test-cognito-apigateway-lambda-stack');

const lambdaProps: lambda.FunctionProps = {
    code: lambda.Code.asset(`${__dirname}/lambda`),
    runtime: lambda.Runtime.NODEJS_12_X,
    handler: 'index.handler'
};

new CognitoToApiGatewayToLambda(stack, 'test-cognito-apigateway-lambda', {
    lambdaFunctionProps: lambdaProps,
    deployLambda: true
});
```

## Initializer

```text
new CognitoToApiGatewayToLambda(scope: Construct, id: string, props: CognitoToApiGatewayToLambdaProps);
```

*Parameters*

* scope [`Construct`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_core.Construct.html)
* id `string`
* props [`CognitoToApiGatewayToLambdaProps`](#pattern-construct-props)

## Pattern Construct Props

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|deployLambda|`boolean`|Whether to create a new Lambda function or use an existing Lambda function|
|existingLambdaObj?|[`lambda.Function`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-lambda.Function.html)|Existing instance of Lambda Function object|
|lambdaFunctionProps?|[`lambda.FunctionProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-lambda.FunctionProps.html)|Optional user provided props to override the default props for Lambda function|
|apiGatewayProps?|[`api.LambdaRestApiProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-apigateway.LambdaRestApi.html)|Optional user provided props to override the default props for API Gateway|
|cognitoUserPoolProps?|[`cognito.UserPoolProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-cognito.UserPoolProps.html)|Optional user provided props to override the default props for Cognito User Pool|
|cognitoUserPoolClientProps?|[`cognito.UserPoolClientProps`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-cognito.UserPoolClientProps.html)|Optional user provided props to override the default props for Cognito User Pool Client|

## Pattern Properties

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|apiGateway|[`api.RestApi`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-apigateway.RestApi.html)|Returns an instance of api.RestApi created by the construct|
|lambdaFunction|[`lambda.Function`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-lambda.Function.html)|Returns an instance of lambda.Function created by the construct|
|userPool|[`cognito.UserPool`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-cognito.UserPool.html)|Returns an instance of cognito.UserPool created by the construct|
|userPoolClient|[`cognito.UserPoolClient`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-cognito.UserPoolClient.html)|Returns an instance of cognito.UserPoolClient created by the construct|

## Default settings

Out of the box implementation of the Construct without any override will set the following defaults:

### Amazon Cognito

* Set password policy for User Pools
* Enforce the advanced security mode for User Pools

### Amazon API Gateway

* Deploy an edge-optimized API endpoint
* Enable CloudWatch logging for API Gateway
* Configure least privilege access IAM role for API Gateway
* Set the default authorizationType for all API methods to IAM

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

import aws_cdk.aws_apigateway
import aws_cdk.aws_cognito
import aws_cdk.aws_lambda
import aws_cdk.core


class CognitoToApiGatewayToLambda(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-solutions-constructs/aws-cognito-apigateway-lambda.CognitoToApiGatewayToLambda"):
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, deploy_lambda: bool, api_gateway_props: typing.Any=None, cognito_user_pool_client_props: typing.Optional[aws_cdk.aws_cognito.UserPoolClientProps]=None, cognito_user_pool_props: typing.Optional[aws_cdk.aws_cognito.UserPoolProps]=None, existing_lambda_obj: typing.Optional[aws_cdk.aws_lambda.Function]=None, lambda_function_props: typing.Optional[aws_cdk.aws_lambda.FunctionProps]=None) -> None:
        """
        :param scope: - represents the scope for all the resources.
        :param id: - this is a a scope-unique id.
        :param deploy_lambda: Whether to create a new Lambda function or use an existing Lambda function. If set to false, you must provide a lambda function object as ``existingLambdaObj`` Default: - true
        :param api_gateway_props: Optional user provided props to override the default props for the API Gateway. Default: - Default props are used
        :param cognito_user_pool_client_props: Optional user provided props to override the default props. Default: - Default props are used
        :param cognito_user_pool_props: Optional user provided props to override the default props. Default: - Default props are used
        :param existing_lambda_obj: Existing instance of Lambda Function object. If ``deploy`` is set to false only then this property is required Default: - None
        :param lambda_function_props: Optional user provided props to override the default props for the Lambda function. If ``deploy`` is set to true only then this property is required Default: - Default props are used

        access:
        :access:: public
        since:
        :since:: 0.8.0
        summary:
        :summary:: Constructs a new instance of the CognitoToApiGatewayToLambda class.
        """
        props = CognitoToApiGatewayToLambdaProps(deploy_lambda=deploy_lambda, api_gateway_props=api_gateway_props, cognito_user_pool_client_props=cognito_user_pool_client_props, cognito_user_pool_props=cognito_user_pool_props, existing_lambda_obj=existing_lambda_obj, lambda_function_props=lambda_function_props)

        jsii.create(CognitoToApiGatewayToLambda, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="apiGateway")
    def api_gateway(self) -> aws_cdk.aws_apigateway.RestApi:
        return jsii.get(self, "apiGateway")

    @builtins.property
    @jsii.member(jsii_name="lambdaFunction")
    def lambda_function(self) -> aws_cdk.aws_lambda.Function:
        return jsii.get(self, "lambdaFunction")

    @builtins.property
    @jsii.member(jsii_name="userPool")
    def user_pool(self) -> aws_cdk.aws_cognito.UserPool:
        return jsii.get(self, "userPool")

    @builtins.property
    @jsii.member(jsii_name="userPoolClient")
    def user_pool_client(self) -> aws_cdk.aws_cognito.UserPoolClient:
        return jsii.get(self, "userPoolClient")


@jsii.data_type(jsii_type="@aws-solutions-constructs/aws-cognito-apigateway-lambda.CognitoToApiGatewayToLambdaProps", jsii_struct_bases=[], name_mapping={'deploy_lambda': 'deployLambda', 'api_gateway_props': 'apiGatewayProps', 'cognito_user_pool_client_props': 'cognitoUserPoolClientProps', 'cognito_user_pool_props': 'cognitoUserPoolProps', 'existing_lambda_obj': 'existingLambdaObj', 'lambda_function_props': 'lambdaFunctionProps'})
class CognitoToApiGatewayToLambdaProps():
    def __init__(self, *, deploy_lambda: bool, api_gateway_props: typing.Any=None, cognito_user_pool_client_props: typing.Optional[aws_cdk.aws_cognito.UserPoolClientProps]=None, cognito_user_pool_props: typing.Optional[aws_cdk.aws_cognito.UserPoolProps]=None, existing_lambda_obj: typing.Optional[aws_cdk.aws_lambda.Function]=None, lambda_function_props: typing.Optional[aws_cdk.aws_lambda.FunctionProps]=None) -> None:
        """
        :param deploy_lambda: Whether to create a new Lambda function or use an existing Lambda function. If set to false, you must provide a lambda function object as ``existingLambdaObj`` Default: - true
        :param api_gateway_props: Optional user provided props to override the default props for the API Gateway. Default: - Default props are used
        :param cognito_user_pool_client_props: Optional user provided props to override the default props. Default: - Default props are used
        :param cognito_user_pool_props: Optional user provided props to override the default props. Default: - Default props are used
        :param existing_lambda_obj: Existing instance of Lambda Function object. If ``deploy`` is set to false only then this property is required Default: - None
        :param lambda_function_props: Optional user provided props to override the default props for the Lambda function. If ``deploy`` is set to true only then this property is required Default: - Default props are used

        summary:
        :summary:: The properties for the CognitoToApiGatewayToLambda Construct
        """
        if isinstance(cognito_user_pool_client_props, dict): cognito_user_pool_client_props = aws_cdk.aws_cognito.UserPoolClientProps(**cognito_user_pool_client_props)
        if isinstance(cognito_user_pool_props, dict): cognito_user_pool_props = aws_cdk.aws_cognito.UserPoolProps(**cognito_user_pool_props)
        if isinstance(lambda_function_props, dict): lambda_function_props = aws_cdk.aws_lambda.FunctionProps(**lambda_function_props)
        self._values = {
            'deploy_lambda': deploy_lambda,
        }
        if api_gateway_props is not None: self._values["api_gateway_props"] = api_gateway_props
        if cognito_user_pool_client_props is not None: self._values["cognito_user_pool_client_props"] = cognito_user_pool_client_props
        if cognito_user_pool_props is not None: self._values["cognito_user_pool_props"] = cognito_user_pool_props
        if existing_lambda_obj is not None: self._values["existing_lambda_obj"] = existing_lambda_obj
        if lambda_function_props is not None: self._values["lambda_function_props"] = lambda_function_props

    @builtins.property
    def deploy_lambda(self) -> bool:
        """Whether to create a new Lambda function or use an existing Lambda function.

        If set to false, you must provide a lambda function object as ``existingLambdaObj``

        default
        :default: - true
        """
        return self._values.get('deploy_lambda')

    @builtins.property
    def api_gateway_props(self) -> typing.Any:
        """Optional user provided props to override the default props for the API Gateway.

        default
        :default: - Default props are used
        """
        return self._values.get('api_gateway_props')

    @builtins.property
    def cognito_user_pool_client_props(self) -> typing.Optional[aws_cdk.aws_cognito.UserPoolClientProps]:
        """Optional user provided props to override the default props.

        default
        :default: - Default props are used
        """
        return self._values.get('cognito_user_pool_client_props')

    @builtins.property
    def cognito_user_pool_props(self) -> typing.Optional[aws_cdk.aws_cognito.UserPoolProps]:
        """Optional user provided props to override the default props.

        default
        :default: - Default props are used
        """
        return self._values.get('cognito_user_pool_props')

    @builtins.property
    def existing_lambda_obj(self) -> typing.Optional[aws_cdk.aws_lambda.Function]:
        """Existing instance of Lambda Function object.

        If ``deploy`` is set to false only then this property is required

        default
        :default: - None
        """
        return self._values.get('existing_lambda_obj')

    @builtins.property
    def lambda_function_props(self) -> typing.Optional[aws_cdk.aws_lambda.FunctionProps]:
        """Optional user provided props to override the default props for the Lambda function.

        If ``deploy`` is set to true only then this property is required

        default
        :default: - Default props are used
        """
        return self._values.get('lambda_function_props')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CognitoToApiGatewayToLambdaProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "CognitoToApiGatewayToLambda",
    "CognitoToApiGatewayToLambdaProps",
]

publication.publish()
