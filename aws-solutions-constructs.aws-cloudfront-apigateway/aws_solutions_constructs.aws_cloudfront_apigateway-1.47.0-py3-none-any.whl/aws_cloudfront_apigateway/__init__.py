"""
# aws-cloudfront-apigateway module

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
|![Python Logo](https://docs.aws.amazon.com/cdk/api/latest/img/python32.png) Python|`aws_solutions_constructs.aws_cloudfront_apigateway`|
|![Typescript Logo](https://docs.aws.amazon.com/cdk/api/latest/img/typescript32.png) Typescript|`@aws-solutions-constructs/aws-cloudfront-apigateway`|
|![Java Logo](https://docs.aws.amazon.com/cdk/api/latest/img/java32.png) Java|`software.amazon.awsconstructs.services.cloudfrontapigateway`|

This AWS Solutions Construct implements an AWS CloudFront fronting an Amazon API Gateway REST API.

Here is a minimal deployable pattern definition:

```javascript
const { defaults } = require('@aws-solutions-constructs/core');
const { CloudFrontToApiGateway } = require('@aws-solutions-constructs/aws-cloudfront-apigateway');

const stack = new Stack();

const lambdaProps: lambda.FunctionProps = {
    code: lambda.Code.asset(`${__dirname}/lambda`),
    runtime: lambda.Runtime.NODEJS_12_X,
    handler: 'index.handler'
};

const func = defaults.deployLambdaFunction(stack, lambdaProps);

const _api = defaults.RegionalApiGateway(stack, func);

new CloudFrontToApiGateway(stack, 'test-cloudfront-apigateway', {
    existingApiGatewayObj: _api
});

```

## Initializer

```text
new CloudFrontToApiGateway(scope: Construct, id: string, props: CloudFrontToApiGatewayProps);
```

*Parameters*

* scope [`Construct`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_core.Construct.html)
* id `string`
* props [`CloudFrontToApiGatewayProps`](#pattern-construct-props)

## Pattern Construct Props

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|existingApiGatewayObj|[`api.RestApi`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-apigateway.RestApi.html)|The regional API Gateway that will be fronted with the CloudFront|
|cloudFrontDistributionProps?|[`cloudfront.CloudFrontWebDistributionProps | any`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-cloudfront.CloudFrontWebDistributionProps.html)|Optional user provided props to override the default props for CloudFront Distribution|
|insertHttpSecurityHeaders?|`boolean`|Optional user provided props to turn on/off the automatic injection of best practice HTTP security headers in all responses from CloudFront|

## Pattern Properties

| **Name**     | **Type**        | **Description** |
|:-------------|:----------------|-----------------|
|cloudFrontWebDistribution|[`cloudfront.CloudFrontWebDistribution`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-cloudfront.CloudFrontWebDistribution.html)|Returns an instance of cloudfront.CloudFrontWebDistribution created by the construct|
|apiGateway|[`api.RestApi`](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-apigateway.RestApi.html)|Returns an instance of the API Gateway REST API created by the pattern.|

## Default settings

Out of the box implementation of the Construct without any override will set the following defaults:

### Amazon CloudFront

* Configure Access logging for CloudFront WebDistribution
* Enable automatic injection of best practice HTTP security headers in all responses from CloudFront WebDistribution

### Amazon API Gateway

* User provided API Gateway object is used as-is

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
import aws_cdk.aws_cloudfront
import aws_cdk.core


class CloudFrontToApiGateway(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-solutions-constructs/aws-cloudfront-apigateway.CloudFrontToApiGateway"):
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, existing_api_gateway_obj: aws_cdk.aws_apigateway.RestApi, cloud_front_distribution_props: typing.Any=None, insert_http_security_headers: typing.Optional[bool]=None) -> None:
        """
        :param scope: - represents the scope for all the resources.
        :param id: - this is a a scope-unique id.
        :param existing_api_gateway_obj: Existing instance of api.RestApi object. Default: - None
        :param cloud_front_distribution_props: Optional user provided props to override the default props. Default: - Default props are used
        :param insert_http_security_headers: Optional user provided props to turn on/off the automatic injection of best practice HTTP security headers in all responses from cloudfront. Default: - true

        access:
        :access:: public
        since:
        :since:: 0.8.0
        summary:
        :summary:: Constructs a new instance of the CloudFrontToApiGateway class.
        """
        props = CloudFrontToApiGatewayProps(existing_api_gateway_obj=existing_api_gateway_obj, cloud_front_distribution_props=cloud_front_distribution_props, insert_http_security_headers=insert_http_security_headers)

        jsii.create(CloudFrontToApiGateway, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="apiGateway")
    def api_gateway(self) -> aws_cdk.aws_apigateway.RestApi:
        return jsii.get(self, "apiGateway")

    @builtins.property
    @jsii.member(jsii_name="cloudFrontWebDistribution")
    def cloud_front_web_distribution(self) -> aws_cdk.aws_cloudfront.CloudFrontWebDistribution:
        return jsii.get(self, "cloudFrontWebDistribution")


@jsii.data_type(jsii_type="@aws-solutions-constructs/aws-cloudfront-apigateway.CloudFrontToApiGatewayProps", jsii_struct_bases=[], name_mapping={'existing_api_gateway_obj': 'existingApiGatewayObj', 'cloud_front_distribution_props': 'cloudFrontDistributionProps', 'insert_http_security_headers': 'insertHttpSecurityHeaders'})
class CloudFrontToApiGatewayProps():
    def __init__(self, *, existing_api_gateway_obj: aws_cdk.aws_apigateway.RestApi, cloud_front_distribution_props: typing.Any=None, insert_http_security_headers: typing.Optional[bool]=None) -> None:
        """
        :param existing_api_gateway_obj: Existing instance of api.RestApi object. Default: - None
        :param cloud_front_distribution_props: Optional user provided props to override the default props. Default: - Default props are used
        :param insert_http_security_headers: Optional user provided props to turn on/off the automatic injection of best practice HTTP security headers in all responses from cloudfront. Default: - true

        summary:
        :summary:: The properties for the CloudFrontToApiGateway Construct
        """
        self._values = {
            'existing_api_gateway_obj': existing_api_gateway_obj,
        }
        if cloud_front_distribution_props is not None: self._values["cloud_front_distribution_props"] = cloud_front_distribution_props
        if insert_http_security_headers is not None: self._values["insert_http_security_headers"] = insert_http_security_headers

    @builtins.property
    def existing_api_gateway_obj(self) -> aws_cdk.aws_apigateway.RestApi:
        """Existing instance of api.RestApi object.

        default
        :default: - None
        """
        return self._values.get('existing_api_gateway_obj')

    @builtins.property
    def cloud_front_distribution_props(self) -> typing.Any:
        """Optional user provided props to override the default props.

        default
        :default: - Default props are used
        """
        return self._values.get('cloud_front_distribution_props')

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
        return 'CloudFrontToApiGatewayProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "CloudFrontToApiGateway",
    "CloudFrontToApiGatewayProps",
]

publication.publish()
