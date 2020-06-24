"""
## AWS::APIGatewayv2 Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development. They are subject to non-backward compatible changes or removal in any future version. These are not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be announced in the release notes. This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

## Table of Contents

* [Introduction](#introduction)
* [HTTP API](#http-api)

  * [Defining HTTP APIs](#defining-http-apis)
  * [Cross Origin Resource Sharing (CORS)](#cross-origin-resource-sharing-cors)
  * [Publishing HTTP APIs](#publishing-http-apis)

## Introduction

Amazon API Gateway is an AWS service for creating, publishing, maintaining, monitoring, and securing REST, HTTP, and WebSocket
APIs at any scale. API developers can create APIs that access AWS or other web services, as well as data stored in the AWS Cloud.
As an API Gateway API developer, you can create APIs for use in your own client applications. Read the
[Amazon API Gateway Developer Guide](https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html).

This module supports features under [API Gateway v2](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ApiGatewayV2.html)
that lets users set up Websocket and HTTP APIs.
REST APIs can be created using the `@aws-cdk/aws-apigateway` module.

## HTTP API

HTTP APIs enable creation of RESTful APIs that integrate with AWS Lambda functions, known as Lambda proxy integration,
or to any routable HTTP endpoint, known as HTTP proxy integration.

### Defining HTTP APIs

HTTP APIs have two fundamental concepts - Routes and Integrations.

Routes direct incoming API requests to backend resources. Routes consist of two parts: an HTTP method and a resource
path, such as, `GET /books`. Learn more at [Working with
routes](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-routes.html). Use the `ANY` method
to match any methods for a route that are not explicitly defined.

Integrations define how the HTTP API responds when a client reaches a specific Route. HTTP APIs support two types of
integrations - Lambda proxy integration and HTTP proxy integration. Learn more at [Configuring
integrations](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations.html).

The code snippet below configures a route `GET /books` with an HTTP proxy integration and uses the `ANY` method to
proxy all other HTTP method calls to `/books` to a lambda proxy.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
get_books_integration = HttpProxyIntegration(
    url="https://get-books-proxy.myproxy.internal"
)

books_default_fn = lambda.Function(stack, "BooksDefaultFn", ...)
books_default_integration = LambdaProxyIntegration(
    handler=books_default_fn
)

http_api = HttpApi(stack, "HttpApi")

http_api.add_routes(
    path="/books",
    methods=[HttpMethod.GET],
    integration=get_books_integration
)
http_api.add_routes(
    path="/books",
    methods=[HttpMethod.ANY],
    integration=books_default_integration
)
```

The `defaultIntegration` option while defining HTTP APIs lets you create a default catch-all integration that is
matched when a client reaches a route that is not explicitly defined.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
HttpApi(stack, "HttpProxyApi",
    default_integration=HttpProxyIntegration(
        url="http://example.com"
    )
)
```

### Cross Origin Resource Sharing (CORS)

[Cross-origin resource sharing (CORS)](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) is a browser security
feature that restricts HTTP requests that are initiated from scripts running in the browser. Enabling CORS will allow
requests to your API from a web application hosted in a domain different from your API domain.

When configured CORS for an HTTP API, API Gateway automatically sends a response to preflight `OPTIONS` requests, even
if there isn't an `OPTIONS` route configured. Note that, when this option is used, API Gateway will ignore CORS headers
returned from your backend integration. Learn more about [Configuring CORS for an HTTP
API](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-cors.html).

The `corsPreflight` option lets you specify a CORS configuration for an API.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
HttpApi(stack, "HttpProxyApi",
    cors_preflight={
        "allow_credentials": True,
        "allow_headers": ["Authorization"],
        "allow_methods": [HttpMethod.GET, HttpMethod.HEAD, HttpMethod.OPTIONS, HttpMethod.POST],
        "allow_origins": ["*"],
        "max_age": Duration.days(10)
    }
)
```

### Publishing HTTP APIs

A Stage is a logical reference to a lifecycle state of your API (for example, `dev`, `prod`, `beta`, or `v2`). API
stages are identified by their stage name. Each stage is a named reference to a deployment of the API made available for
client applications to call.

Use `HttpStage` to create a Stage resource for HTTP APIs. The following code sets up a Stage, whose URL is available at
`https://{api_id}.execute-api.{region}.amazonaws.com/beta`.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
HttpStage(stack, "Stage",
    http_api=api,
    stage_name="beta"
)
```

If you omit the `stageName` will create a `$default` stage. A `$default` stage is one that is served from the base of
the API's URL - `https://{api_id}.execute-api.{region}.amazonaws.com/`.

Note that, `HttpApi` will always creates a `$default` stage, unless the `createDefaultStage` property is unset.
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
import aws_cdk.core


@jsii.data_type(jsii_type="@aws-cdk/aws-apigatewayv2.BatchHttpRouteOptions", jsii_struct_bases=[], name_mapping={'integration': 'integration'})
class BatchHttpRouteOptions():
    def __init__(self, *, integration: "IHttpRouteIntegration") -> None:
        """Options used when configuring multiple routes, at once.

        The options here are the ones that would be configured for all being set up.

        :param integration: The integration to be configured on this route.

        stability
        :stability: experimental
        """
        self._values = {
            'integration': integration,
        }

    @builtins.property
    def integration(self) -> "IHttpRouteIntegration":
        """The integration to be configured on this route.

        stability
        :stability: experimental
        """
        return self._values.get('integration')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BatchHttpRouteOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnApi(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigatewayv2.CfnApi"):
    """A CloudFormation ``AWS::ApiGatewayV2::Api``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html
    cloudformationResource:
    :cloudformationResource:: AWS::ApiGatewayV2::Api
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, api_key_selection_expression: typing.Optional[str]=None, base_path: typing.Optional[str]=None, body: typing.Any=None, body_s3_location: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "BodyS3LocationProperty"]]=None, cors_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CorsProperty"]]=None, credentials_arn: typing.Optional[str]=None, description: typing.Optional[str]=None, disable_schema_validation: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]=None, fail_on_warnings: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]=None, name: typing.Optional[str]=None, protocol_type: typing.Optional[str]=None, route_key: typing.Optional[str]=None, route_selection_expression: typing.Optional[str]=None, tags: typing.Any=None, target: typing.Optional[str]=None, version: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::ApiGatewayV2::Api``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_key_selection_expression: ``AWS::ApiGatewayV2::Api.ApiKeySelectionExpression``.
        :param base_path: ``AWS::ApiGatewayV2::Api.BasePath``.
        :param body: ``AWS::ApiGatewayV2::Api.Body``.
        :param body_s3_location: ``AWS::ApiGatewayV2::Api.BodyS3Location``.
        :param cors_configuration: ``AWS::ApiGatewayV2::Api.CorsConfiguration``.
        :param credentials_arn: ``AWS::ApiGatewayV2::Api.CredentialsArn``.
        :param description: ``AWS::ApiGatewayV2::Api.Description``.
        :param disable_schema_validation: ``AWS::ApiGatewayV2::Api.DisableSchemaValidation``.
        :param fail_on_warnings: ``AWS::ApiGatewayV2::Api.FailOnWarnings``.
        :param name: ``AWS::ApiGatewayV2::Api.Name``.
        :param protocol_type: ``AWS::ApiGatewayV2::Api.ProtocolType``.
        :param route_key: ``AWS::ApiGatewayV2::Api.RouteKey``.
        :param route_selection_expression: ``AWS::ApiGatewayV2::Api.RouteSelectionExpression``.
        :param tags: ``AWS::ApiGatewayV2::Api.Tags``.
        :param target: ``AWS::ApiGatewayV2::Api.Target``.
        :param version: ``AWS::ApiGatewayV2::Api.Version``.
        """
        props = CfnApiProps(api_key_selection_expression=api_key_selection_expression, base_path=base_path, body=body, body_s3_location=body_s3_location, cors_configuration=cors_configuration, credentials_arn=credentials_arn, description=description, disable_schema_validation=disable_schema_validation, fail_on_warnings=fail_on_warnings, name=name, protocol_type=protocol_type, route_key=route_key, route_selection_expression=route_selection_expression, tags=tags, target=target, version=version)

        jsii.create(CfnApi, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnApi":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::ApiGatewayV2::Api.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="body")
    def body(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Api.Body``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-body
        """
        return jsii.get(self, "body")

    @body.setter
    def body(self, value: typing.Any) -> None:
        jsii.set(self, "body", value)

    @builtins.property
    @jsii.member(jsii_name="apiKeySelectionExpression")
    def api_key_selection_expression(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Api.ApiKeySelectionExpression``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-apikeyselectionexpression
        """
        return jsii.get(self, "apiKeySelectionExpression")

    @api_key_selection_expression.setter
    def api_key_selection_expression(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "apiKeySelectionExpression", value)

    @builtins.property
    @jsii.member(jsii_name="basePath")
    def base_path(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Api.BasePath``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-basepath
        """
        return jsii.get(self, "basePath")

    @base_path.setter
    def base_path(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "basePath", value)

    @builtins.property
    @jsii.member(jsii_name="bodyS3Location")
    def body_s3_location(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "BodyS3LocationProperty"]]:
        """``AWS::ApiGatewayV2::Api.BodyS3Location``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-bodys3location
        """
        return jsii.get(self, "bodyS3Location")

    @body_s3_location.setter
    def body_s3_location(self, value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "BodyS3LocationProperty"]]) -> None:
        jsii.set(self, "bodyS3Location", value)

    @builtins.property
    @jsii.member(jsii_name="corsConfiguration")
    def cors_configuration(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CorsProperty"]]:
        """``AWS::ApiGatewayV2::Api.CorsConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-corsconfiguration
        """
        return jsii.get(self, "corsConfiguration")

    @cors_configuration.setter
    def cors_configuration(self, value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CorsProperty"]]) -> None:
        jsii.set(self, "corsConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="credentialsArn")
    def credentials_arn(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Api.CredentialsArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-credentialsarn
        """
        return jsii.get(self, "credentialsArn")

    @credentials_arn.setter
    def credentials_arn(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "credentialsArn", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Api.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="disableSchemaValidation")
    def disable_schema_validation(self) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
        """``AWS::ApiGatewayV2::Api.DisableSchemaValidation``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-disableschemavalidation
        """
        return jsii.get(self, "disableSchemaValidation")

    @disable_schema_validation.setter
    def disable_schema_validation(self, value: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]) -> None:
        jsii.set(self, "disableSchemaValidation", value)

    @builtins.property
    @jsii.member(jsii_name="failOnWarnings")
    def fail_on_warnings(self) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
        """``AWS::ApiGatewayV2::Api.FailOnWarnings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-failonwarnings
        """
        return jsii.get(self, "failOnWarnings")

    @fail_on_warnings.setter
    def fail_on_warnings(self, value: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]) -> None:
        jsii.set(self, "failOnWarnings", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Api.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="protocolType")
    def protocol_type(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Api.ProtocolType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-protocoltype
        """
        return jsii.get(self, "protocolType")

    @protocol_type.setter
    def protocol_type(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "protocolType", value)

    @builtins.property
    @jsii.member(jsii_name="routeKey")
    def route_key(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Api.RouteKey``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-routekey
        """
        return jsii.get(self, "routeKey")

    @route_key.setter
    def route_key(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "routeKey", value)

    @builtins.property
    @jsii.member(jsii_name="routeSelectionExpression")
    def route_selection_expression(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Api.RouteSelectionExpression``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-routeselectionexpression
        """
        return jsii.get(self, "routeSelectionExpression")

    @route_selection_expression.setter
    def route_selection_expression(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "routeSelectionExpression", value)

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Api.Target``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-target
        """
        return jsii.get(self, "target")

    @target.setter
    def target(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "target", value)

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Api.Version``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-version
        """
        return jsii.get(self, "version")

    @version.setter
    def version(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "version", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-apigatewayv2.CfnApi.BodyS3LocationProperty", jsii_struct_bases=[], name_mapping={'bucket': 'bucket', 'etag': 'etag', 'key': 'key', 'version': 'version'})
    class BodyS3LocationProperty():
        def __init__(self, *, bucket: typing.Optional[str]=None, etag: typing.Optional[str]=None, key: typing.Optional[str]=None, version: typing.Optional[str]=None) -> None:
            """
            :param bucket: ``CfnApi.BodyS3LocationProperty.Bucket``.
            :param etag: ``CfnApi.BodyS3LocationProperty.Etag``.
            :param key: ``CfnApi.BodyS3LocationProperty.Key``.
            :param version: ``CfnApi.BodyS3LocationProperty.Version``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-api-bodys3location.html
            """
            self._values = {
            }
            if bucket is not None: self._values["bucket"] = bucket
            if etag is not None: self._values["etag"] = etag
            if key is not None: self._values["key"] = key
            if version is not None: self._values["version"] = version

        @builtins.property
        def bucket(self) -> typing.Optional[str]:
            """``CfnApi.BodyS3LocationProperty.Bucket``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-api-bodys3location.html#cfn-apigatewayv2-api-bodys3location-bucket
            """
            return self._values.get('bucket')

        @builtins.property
        def etag(self) -> typing.Optional[str]:
            """``CfnApi.BodyS3LocationProperty.Etag``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-api-bodys3location.html#cfn-apigatewayv2-api-bodys3location-etag
            """
            return self._values.get('etag')

        @builtins.property
        def key(self) -> typing.Optional[str]:
            """``CfnApi.BodyS3LocationProperty.Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-api-bodys3location.html#cfn-apigatewayv2-api-bodys3location-key
            """
            return self._values.get('key')

        @builtins.property
        def version(self) -> typing.Optional[str]:
            """``CfnApi.BodyS3LocationProperty.Version``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-api-bodys3location.html#cfn-apigatewayv2-api-bodys3location-version
            """
            return self._values.get('version')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'BodyS3LocationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-apigatewayv2.CfnApi.CorsProperty", jsii_struct_bases=[], name_mapping={'allow_credentials': 'allowCredentials', 'allow_headers': 'allowHeaders', 'allow_methods': 'allowMethods', 'allow_origins': 'allowOrigins', 'expose_headers': 'exposeHeaders', 'max_age': 'maxAge'})
    class CorsProperty():
        def __init__(self, *, allow_credentials: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]=None, allow_headers: typing.Optional[typing.List[str]]=None, allow_methods: typing.Optional[typing.List[str]]=None, allow_origins: typing.Optional[typing.List[str]]=None, expose_headers: typing.Optional[typing.List[str]]=None, max_age: typing.Optional[jsii.Number]=None) -> None:
            """
            :param allow_credentials: ``CfnApi.CorsProperty.AllowCredentials``.
            :param allow_headers: ``CfnApi.CorsProperty.AllowHeaders``.
            :param allow_methods: ``CfnApi.CorsProperty.AllowMethods``.
            :param allow_origins: ``CfnApi.CorsProperty.AllowOrigins``.
            :param expose_headers: ``CfnApi.CorsProperty.ExposeHeaders``.
            :param max_age: ``CfnApi.CorsProperty.MaxAge``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-api-cors.html
            """
            self._values = {
            }
            if allow_credentials is not None: self._values["allow_credentials"] = allow_credentials
            if allow_headers is not None: self._values["allow_headers"] = allow_headers
            if allow_methods is not None: self._values["allow_methods"] = allow_methods
            if allow_origins is not None: self._values["allow_origins"] = allow_origins
            if expose_headers is not None: self._values["expose_headers"] = expose_headers
            if max_age is not None: self._values["max_age"] = max_age

        @builtins.property
        def allow_credentials(self) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
            """``CfnApi.CorsProperty.AllowCredentials``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-api-cors.html#cfn-apigatewayv2-api-cors-allowcredentials
            """
            return self._values.get('allow_credentials')

        @builtins.property
        def allow_headers(self) -> typing.Optional[typing.List[str]]:
            """``CfnApi.CorsProperty.AllowHeaders``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-api-cors.html#cfn-apigatewayv2-api-cors-allowheaders
            """
            return self._values.get('allow_headers')

        @builtins.property
        def allow_methods(self) -> typing.Optional[typing.List[str]]:
            """``CfnApi.CorsProperty.AllowMethods``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-api-cors.html#cfn-apigatewayv2-api-cors-allowmethods
            """
            return self._values.get('allow_methods')

        @builtins.property
        def allow_origins(self) -> typing.Optional[typing.List[str]]:
            """``CfnApi.CorsProperty.AllowOrigins``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-api-cors.html#cfn-apigatewayv2-api-cors-alloworigins
            """
            return self._values.get('allow_origins')

        @builtins.property
        def expose_headers(self) -> typing.Optional[typing.List[str]]:
            """``CfnApi.CorsProperty.ExposeHeaders``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-api-cors.html#cfn-apigatewayv2-api-cors-exposeheaders
            """
            return self._values.get('expose_headers')

        @builtins.property
        def max_age(self) -> typing.Optional[jsii.Number]:
            """``CfnApi.CorsProperty.MaxAge``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-api-cors.html#cfn-apigatewayv2-api-cors-maxage
            """
            return self._values.get('max_age')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'CorsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.implements(aws_cdk.core.IInspectable)
class CfnApiMapping(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigatewayv2.CfnApiMapping"):
    """A CloudFormation ``AWS::ApiGatewayV2::ApiMapping``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apimapping.html
    cloudformationResource:
    :cloudformationResource:: AWS::ApiGatewayV2::ApiMapping
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, api_id: str, domain_name: str, stage: str, api_mapping_key: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::ApiGatewayV2::ApiMapping``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_id: ``AWS::ApiGatewayV2::ApiMapping.ApiId``.
        :param domain_name: ``AWS::ApiGatewayV2::ApiMapping.DomainName``.
        :param stage: ``AWS::ApiGatewayV2::ApiMapping.Stage``.
        :param api_mapping_key: ``AWS::ApiGatewayV2::ApiMapping.ApiMappingKey``.
        """
        props = CfnApiMappingProps(api_id=api_id, domain_name=domain_name, stage=stage, api_mapping_key=api_mapping_key)

        jsii.create(CfnApiMapping, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnApiMapping":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> str:
        """``AWS::ApiGatewayV2::ApiMapping.ApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apimapping.html#cfn-apigatewayv2-apimapping-apiid
        """
        return jsii.get(self, "apiId")

    @api_id.setter
    def api_id(self, value: str) -> None:
        jsii.set(self, "apiId", value)

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> str:
        """``AWS::ApiGatewayV2::ApiMapping.DomainName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apimapping.html#cfn-apigatewayv2-apimapping-domainname
        """
        return jsii.get(self, "domainName")

    @domain_name.setter
    def domain_name(self, value: str) -> None:
        jsii.set(self, "domainName", value)

    @builtins.property
    @jsii.member(jsii_name="stage")
    def stage(self) -> str:
        """``AWS::ApiGatewayV2::ApiMapping.Stage``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apimapping.html#cfn-apigatewayv2-apimapping-stage
        """
        return jsii.get(self, "stage")

    @stage.setter
    def stage(self, value: str) -> None:
        jsii.set(self, "stage", value)

    @builtins.property
    @jsii.member(jsii_name="apiMappingKey")
    def api_mapping_key(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::ApiMapping.ApiMappingKey``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apimapping.html#cfn-apigatewayv2-apimapping-apimappingkey
        """
        return jsii.get(self, "apiMappingKey")

    @api_mapping_key.setter
    def api_mapping_key(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "apiMappingKey", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-apigatewayv2.CfnApiMappingProps", jsii_struct_bases=[], name_mapping={'api_id': 'apiId', 'domain_name': 'domainName', 'stage': 'stage', 'api_mapping_key': 'apiMappingKey'})
class CfnApiMappingProps():
    def __init__(self, *, api_id: str, domain_name: str, stage: str, api_mapping_key: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::ApiGatewayV2::ApiMapping``.

        :param api_id: ``AWS::ApiGatewayV2::ApiMapping.ApiId``.
        :param domain_name: ``AWS::ApiGatewayV2::ApiMapping.DomainName``.
        :param stage: ``AWS::ApiGatewayV2::ApiMapping.Stage``.
        :param api_mapping_key: ``AWS::ApiGatewayV2::ApiMapping.ApiMappingKey``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apimapping.html
        """
        self._values = {
            'api_id': api_id,
            'domain_name': domain_name,
            'stage': stage,
        }
        if api_mapping_key is not None: self._values["api_mapping_key"] = api_mapping_key

    @builtins.property
    def api_id(self) -> str:
        """``AWS::ApiGatewayV2::ApiMapping.ApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apimapping.html#cfn-apigatewayv2-apimapping-apiid
        """
        return self._values.get('api_id')

    @builtins.property
    def domain_name(self) -> str:
        """``AWS::ApiGatewayV2::ApiMapping.DomainName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apimapping.html#cfn-apigatewayv2-apimapping-domainname
        """
        return self._values.get('domain_name')

    @builtins.property
    def stage(self) -> str:
        """``AWS::ApiGatewayV2::ApiMapping.Stage``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apimapping.html#cfn-apigatewayv2-apimapping-stage
        """
        return self._values.get('stage')

    @builtins.property
    def api_mapping_key(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::ApiMapping.ApiMappingKey``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-apimapping.html#cfn-apigatewayv2-apimapping-apimappingkey
        """
        return self._values.get('api_mapping_key')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnApiMappingProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-apigatewayv2.CfnApiProps", jsii_struct_bases=[], name_mapping={'api_key_selection_expression': 'apiKeySelectionExpression', 'base_path': 'basePath', 'body': 'body', 'body_s3_location': 'bodyS3Location', 'cors_configuration': 'corsConfiguration', 'credentials_arn': 'credentialsArn', 'description': 'description', 'disable_schema_validation': 'disableSchemaValidation', 'fail_on_warnings': 'failOnWarnings', 'name': 'name', 'protocol_type': 'protocolType', 'route_key': 'routeKey', 'route_selection_expression': 'routeSelectionExpression', 'tags': 'tags', 'target': 'target', 'version': 'version'})
class CfnApiProps():
    def __init__(self, *, api_key_selection_expression: typing.Optional[str]=None, base_path: typing.Optional[str]=None, body: typing.Any=None, body_s3_location: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApi.BodyS3LocationProperty"]]=None, cors_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApi.CorsProperty"]]=None, credentials_arn: typing.Optional[str]=None, description: typing.Optional[str]=None, disable_schema_validation: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]=None, fail_on_warnings: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]=None, name: typing.Optional[str]=None, protocol_type: typing.Optional[str]=None, route_key: typing.Optional[str]=None, route_selection_expression: typing.Optional[str]=None, tags: typing.Any=None, target: typing.Optional[str]=None, version: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::ApiGatewayV2::Api``.

        :param api_key_selection_expression: ``AWS::ApiGatewayV2::Api.ApiKeySelectionExpression``.
        :param base_path: ``AWS::ApiGatewayV2::Api.BasePath``.
        :param body: ``AWS::ApiGatewayV2::Api.Body``.
        :param body_s3_location: ``AWS::ApiGatewayV2::Api.BodyS3Location``.
        :param cors_configuration: ``AWS::ApiGatewayV2::Api.CorsConfiguration``.
        :param credentials_arn: ``AWS::ApiGatewayV2::Api.CredentialsArn``.
        :param description: ``AWS::ApiGatewayV2::Api.Description``.
        :param disable_schema_validation: ``AWS::ApiGatewayV2::Api.DisableSchemaValidation``.
        :param fail_on_warnings: ``AWS::ApiGatewayV2::Api.FailOnWarnings``.
        :param name: ``AWS::ApiGatewayV2::Api.Name``.
        :param protocol_type: ``AWS::ApiGatewayV2::Api.ProtocolType``.
        :param route_key: ``AWS::ApiGatewayV2::Api.RouteKey``.
        :param route_selection_expression: ``AWS::ApiGatewayV2::Api.RouteSelectionExpression``.
        :param tags: ``AWS::ApiGatewayV2::Api.Tags``.
        :param target: ``AWS::ApiGatewayV2::Api.Target``.
        :param version: ``AWS::ApiGatewayV2::Api.Version``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html
        """
        self._values = {
        }
        if api_key_selection_expression is not None: self._values["api_key_selection_expression"] = api_key_selection_expression
        if base_path is not None: self._values["base_path"] = base_path
        if body is not None: self._values["body"] = body
        if body_s3_location is not None: self._values["body_s3_location"] = body_s3_location
        if cors_configuration is not None: self._values["cors_configuration"] = cors_configuration
        if credentials_arn is not None: self._values["credentials_arn"] = credentials_arn
        if description is not None: self._values["description"] = description
        if disable_schema_validation is not None: self._values["disable_schema_validation"] = disable_schema_validation
        if fail_on_warnings is not None: self._values["fail_on_warnings"] = fail_on_warnings
        if name is not None: self._values["name"] = name
        if protocol_type is not None: self._values["protocol_type"] = protocol_type
        if route_key is not None: self._values["route_key"] = route_key
        if route_selection_expression is not None: self._values["route_selection_expression"] = route_selection_expression
        if tags is not None: self._values["tags"] = tags
        if target is not None: self._values["target"] = target
        if version is not None: self._values["version"] = version

    @builtins.property
    def api_key_selection_expression(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Api.ApiKeySelectionExpression``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-apikeyselectionexpression
        """
        return self._values.get('api_key_selection_expression')

    @builtins.property
    def base_path(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Api.BasePath``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-basepath
        """
        return self._values.get('base_path')

    @builtins.property
    def body(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Api.Body``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-body
        """
        return self._values.get('body')

    @builtins.property
    def body_s3_location(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApi.BodyS3LocationProperty"]]:
        """``AWS::ApiGatewayV2::Api.BodyS3Location``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-bodys3location
        """
        return self._values.get('body_s3_location')

    @builtins.property
    def cors_configuration(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnApi.CorsProperty"]]:
        """``AWS::ApiGatewayV2::Api.CorsConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-corsconfiguration
        """
        return self._values.get('cors_configuration')

    @builtins.property
    def credentials_arn(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Api.CredentialsArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-credentialsarn
        """
        return self._values.get('credentials_arn')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Api.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-description
        """
        return self._values.get('description')

    @builtins.property
    def disable_schema_validation(self) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
        """``AWS::ApiGatewayV2::Api.DisableSchemaValidation``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-disableschemavalidation
        """
        return self._values.get('disable_schema_validation')

    @builtins.property
    def fail_on_warnings(self) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
        """``AWS::ApiGatewayV2::Api.FailOnWarnings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-failonwarnings
        """
        return self._values.get('fail_on_warnings')

    @builtins.property
    def name(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Api.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-name
        """
        return self._values.get('name')

    @builtins.property
    def protocol_type(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Api.ProtocolType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-protocoltype
        """
        return self._values.get('protocol_type')

    @builtins.property
    def route_key(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Api.RouteKey``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-routekey
        """
        return self._values.get('route_key')

    @builtins.property
    def route_selection_expression(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Api.RouteSelectionExpression``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-routeselectionexpression
        """
        return self._values.get('route_selection_expression')

    @builtins.property
    def tags(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Api.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-tags
        """
        return self._values.get('tags')

    @builtins.property
    def target(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Api.Target``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-target
        """
        return self._values.get('target')

    @builtins.property
    def version(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Api.Version``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-api.html#cfn-apigatewayv2-api-version
        """
        return self._values.get('version')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnApiProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnAuthorizer(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigatewayv2.CfnAuthorizer"):
    """A CloudFormation ``AWS::ApiGatewayV2::Authorizer``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html
    cloudformationResource:
    :cloudformationResource:: AWS::ApiGatewayV2::Authorizer
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, api_id: str, authorizer_type: str, identity_source: typing.List[str], name: str, authorizer_credentials_arn: typing.Optional[str]=None, authorizer_result_ttl_in_seconds: typing.Optional[jsii.Number]=None, authorizer_uri: typing.Optional[str]=None, identity_validation_expression: typing.Optional[str]=None, jwt_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "JWTConfigurationProperty"]]=None) -> None:
        """Create a new ``AWS::ApiGatewayV2::Authorizer``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_id: ``AWS::ApiGatewayV2::Authorizer.ApiId``.
        :param authorizer_type: ``AWS::ApiGatewayV2::Authorizer.AuthorizerType``.
        :param identity_source: ``AWS::ApiGatewayV2::Authorizer.IdentitySource``.
        :param name: ``AWS::ApiGatewayV2::Authorizer.Name``.
        :param authorizer_credentials_arn: ``AWS::ApiGatewayV2::Authorizer.AuthorizerCredentialsArn``.
        :param authorizer_result_ttl_in_seconds: ``AWS::ApiGatewayV2::Authorizer.AuthorizerResultTtlInSeconds``.
        :param authorizer_uri: ``AWS::ApiGatewayV2::Authorizer.AuthorizerUri``.
        :param identity_validation_expression: ``AWS::ApiGatewayV2::Authorizer.IdentityValidationExpression``.
        :param jwt_configuration: ``AWS::ApiGatewayV2::Authorizer.JwtConfiguration``.
        """
        props = CfnAuthorizerProps(api_id=api_id, authorizer_type=authorizer_type, identity_source=identity_source, name=name, authorizer_credentials_arn=authorizer_credentials_arn, authorizer_result_ttl_in_seconds=authorizer_result_ttl_in_seconds, authorizer_uri=authorizer_uri, identity_validation_expression=identity_validation_expression, jwt_configuration=jwt_configuration)

        jsii.create(CfnAuthorizer, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnAuthorizer":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> str:
        """``AWS::ApiGatewayV2::Authorizer.ApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-apiid
        """
        return jsii.get(self, "apiId")

    @api_id.setter
    def api_id(self, value: str) -> None:
        jsii.set(self, "apiId", value)

    @builtins.property
    @jsii.member(jsii_name="authorizerType")
    def authorizer_type(self) -> str:
        """``AWS::ApiGatewayV2::Authorizer.AuthorizerType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-authorizertype
        """
        return jsii.get(self, "authorizerType")

    @authorizer_type.setter
    def authorizer_type(self, value: str) -> None:
        jsii.set(self, "authorizerType", value)

    @builtins.property
    @jsii.member(jsii_name="identitySource")
    def identity_source(self) -> typing.List[str]:
        """``AWS::ApiGatewayV2::Authorizer.IdentitySource``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-identitysource
        """
        return jsii.get(self, "identitySource")

    @identity_source.setter
    def identity_source(self, value: typing.List[str]) -> None:
        jsii.set(self, "identitySource", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """``AWS::ApiGatewayV2::Authorizer.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="authorizerCredentialsArn")
    def authorizer_credentials_arn(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Authorizer.AuthorizerCredentialsArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-authorizercredentialsarn
        """
        return jsii.get(self, "authorizerCredentialsArn")

    @authorizer_credentials_arn.setter
    def authorizer_credentials_arn(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "authorizerCredentialsArn", value)

    @builtins.property
    @jsii.member(jsii_name="authorizerResultTtlInSeconds")
    def authorizer_result_ttl_in_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::ApiGatewayV2::Authorizer.AuthorizerResultTtlInSeconds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-authorizerresultttlinseconds
        """
        return jsii.get(self, "authorizerResultTtlInSeconds")

    @authorizer_result_ttl_in_seconds.setter
    def authorizer_result_ttl_in_seconds(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "authorizerResultTtlInSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="authorizerUri")
    def authorizer_uri(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Authorizer.AuthorizerUri``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-authorizeruri
        """
        return jsii.get(self, "authorizerUri")

    @authorizer_uri.setter
    def authorizer_uri(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "authorizerUri", value)

    @builtins.property
    @jsii.member(jsii_name="identityValidationExpression")
    def identity_validation_expression(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Authorizer.IdentityValidationExpression``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-identityvalidationexpression
        """
        return jsii.get(self, "identityValidationExpression")

    @identity_validation_expression.setter
    def identity_validation_expression(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "identityValidationExpression", value)

    @builtins.property
    @jsii.member(jsii_name="jwtConfiguration")
    def jwt_configuration(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "JWTConfigurationProperty"]]:
        """``AWS::ApiGatewayV2::Authorizer.JwtConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-jwtconfiguration
        """
        return jsii.get(self, "jwtConfiguration")

    @jwt_configuration.setter
    def jwt_configuration(self, value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "JWTConfigurationProperty"]]) -> None:
        jsii.set(self, "jwtConfiguration", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-apigatewayv2.CfnAuthorizer.JWTConfigurationProperty", jsii_struct_bases=[], name_mapping={'audience': 'audience', 'issuer': 'issuer'})
    class JWTConfigurationProperty():
        def __init__(self, *, audience: typing.Optional[typing.List[str]]=None, issuer: typing.Optional[str]=None) -> None:
            """
            :param audience: ``CfnAuthorizer.JWTConfigurationProperty.Audience``.
            :param issuer: ``CfnAuthorizer.JWTConfigurationProperty.Issuer``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-authorizer-jwtconfiguration.html
            """
            self._values = {
            }
            if audience is not None: self._values["audience"] = audience
            if issuer is not None: self._values["issuer"] = issuer

        @builtins.property
        def audience(self) -> typing.Optional[typing.List[str]]:
            """``CfnAuthorizer.JWTConfigurationProperty.Audience``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-authorizer-jwtconfiguration.html#cfn-apigatewayv2-authorizer-jwtconfiguration-audience
            """
            return self._values.get('audience')

        @builtins.property
        def issuer(self) -> typing.Optional[str]:
            """``CfnAuthorizer.JWTConfigurationProperty.Issuer``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-authorizer-jwtconfiguration.html#cfn-apigatewayv2-authorizer-jwtconfiguration-issuer
            """
            return self._values.get('issuer')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'JWTConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-apigatewayv2.CfnAuthorizerProps", jsii_struct_bases=[], name_mapping={'api_id': 'apiId', 'authorizer_type': 'authorizerType', 'identity_source': 'identitySource', 'name': 'name', 'authorizer_credentials_arn': 'authorizerCredentialsArn', 'authorizer_result_ttl_in_seconds': 'authorizerResultTtlInSeconds', 'authorizer_uri': 'authorizerUri', 'identity_validation_expression': 'identityValidationExpression', 'jwt_configuration': 'jwtConfiguration'})
class CfnAuthorizerProps():
    def __init__(self, *, api_id: str, authorizer_type: str, identity_source: typing.List[str], name: str, authorizer_credentials_arn: typing.Optional[str]=None, authorizer_result_ttl_in_seconds: typing.Optional[jsii.Number]=None, authorizer_uri: typing.Optional[str]=None, identity_validation_expression: typing.Optional[str]=None, jwt_configuration: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnAuthorizer.JWTConfigurationProperty"]]=None) -> None:
        """Properties for defining a ``AWS::ApiGatewayV2::Authorizer``.

        :param api_id: ``AWS::ApiGatewayV2::Authorizer.ApiId``.
        :param authorizer_type: ``AWS::ApiGatewayV2::Authorizer.AuthorizerType``.
        :param identity_source: ``AWS::ApiGatewayV2::Authorizer.IdentitySource``.
        :param name: ``AWS::ApiGatewayV2::Authorizer.Name``.
        :param authorizer_credentials_arn: ``AWS::ApiGatewayV2::Authorizer.AuthorizerCredentialsArn``.
        :param authorizer_result_ttl_in_seconds: ``AWS::ApiGatewayV2::Authorizer.AuthorizerResultTtlInSeconds``.
        :param authorizer_uri: ``AWS::ApiGatewayV2::Authorizer.AuthorizerUri``.
        :param identity_validation_expression: ``AWS::ApiGatewayV2::Authorizer.IdentityValidationExpression``.
        :param jwt_configuration: ``AWS::ApiGatewayV2::Authorizer.JwtConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html
        """
        self._values = {
            'api_id': api_id,
            'authorizer_type': authorizer_type,
            'identity_source': identity_source,
            'name': name,
        }
        if authorizer_credentials_arn is not None: self._values["authorizer_credentials_arn"] = authorizer_credentials_arn
        if authorizer_result_ttl_in_seconds is not None: self._values["authorizer_result_ttl_in_seconds"] = authorizer_result_ttl_in_seconds
        if authorizer_uri is not None: self._values["authorizer_uri"] = authorizer_uri
        if identity_validation_expression is not None: self._values["identity_validation_expression"] = identity_validation_expression
        if jwt_configuration is not None: self._values["jwt_configuration"] = jwt_configuration

    @builtins.property
    def api_id(self) -> str:
        """``AWS::ApiGatewayV2::Authorizer.ApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-apiid
        """
        return self._values.get('api_id')

    @builtins.property
    def authorizer_type(self) -> str:
        """``AWS::ApiGatewayV2::Authorizer.AuthorizerType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-authorizertype
        """
        return self._values.get('authorizer_type')

    @builtins.property
    def identity_source(self) -> typing.List[str]:
        """``AWS::ApiGatewayV2::Authorizer.IdentitySource``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-identitysource
        """
        return self._values.get('identity_source')

    @builtins.property
    def name(self) -> str:
        """``AWS::ApiGatewayV2::Authorizer.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-name
        """
        return self._values.get('name')

    @builtins.property
    def authorizer_credentials_arn(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Authorizer.AuthorizerCredentialsArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-authorizercredentialsarn
        """
        return self._values.get('authorizer_credentials_arn')

    @builtins.property
    def authorizer_result_ttl_in_seconds(self) -> typing.Optional[jsii.Number]:
        """``AWS::ApiGatewayV2::Authorizer.AuthorizerResultTtlInSeconds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-authorizerresultttlinseconds
        """
        return self._values.get('authorizer_result_ttl_in_seconds')

    @builtins.property
    def authorizer_uri(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Authorizer.AuthorizerUri``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-authorizeruri
        """
        return self._values.get('authorizer_uri')

    @builtins.property
    def identity_validation_expression(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Authorizer.IdentityValidationExpression``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-identityvalidationexpression
        """
        return self._values.get('identity_validation_expression')

    @builtins.property
    def jwt_configuration(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnAuthorizer.JWTConfigurationProperty"]]:
        """``AWS::ApiGatewayV2::Authorizer.JwtConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-authorizer.html#cfn-apigatewayv2-authorizer-jwtconfiguration
        """
        return self._values.get('jwt_configuration')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnAuthorizerProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnDeployment(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigatewayv2.CfnDeployment"):
    """A CloudFormation ``AWS::ApiGatewayV2::Deployment``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-deployment.html
    cloudformationResource:
    :cloudformationResource:: AWS::ApiGatewayV2::Deployment
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, api_id: str, description: typing.Optional[str]=None, stage_name: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::ApiGatewayV2::Deployment``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_id: ``AWS::ApiGatewayV2::Deployment.ApiId``.
        :param description: ``AWS::ApiGatewayV2::Deployment.Description``.
        :param stage_name: ``AWS::ApiGatewayV2::Deployment.StageName``.
        """
        props = CfnDeploymentProps(api_id=api_id, description=description, stage_name=stage_name)

        jsii.create(CfnDeployment, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnDeployment":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> str:
        """``AWS::ApiGatewayV2::Deployment.ApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-deployment.html#cfn-apigatewayv2-deployment-apiid
        """
        return jsii.get(self, "apiId")

    @api_id.setter
    def api_id(self, value: str) -> None:
        jsii.set(self, "apiId", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Deployment.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-deployment.html#cfn-apigatewayv2-deployment-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="stageName")
    def stage_name(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Deployment.StageName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-deployment.html#cfn-apigatewayv2-deployment-stagename
        """
        return jsii.get(self, "stageName")

    @stage_name.setter
    def stage_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "stageName", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-apigatewayv2.CfnDeploymentProps", jsii_struct_bases=[], name_mapping={'api_id': 'apiId', 'description': 'description', 'stage_name': 'stageName'})
class CfnDeploymentProps():
    def __init__(self, *, api_id: str, description: typing.Optional[str]=None, stage_name: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::ApiGatewayV2::Deployment``.

        :param api_id: ``AWS::ApiGatewayV2::Deployment.ApiId``.
        :param description: ``AWS::ApiGatewayV2::Deployment.Description``.
        :param stage_name: ``AWS::ApiGatewayV2::Deployment.StageName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-deployment.html
        """
        self._values = {
            'api_id': api_id,
        }
        if description is not None: self._values["description"] = description
        if stage_name is not None: self._values["stage_name"] = stage_name

    @builtins.property
    def api_id(self) -> str:
        """``AWS::ApiGatewayV2::Deployment.ApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-deployment.html#cfn-apigatewayv2-deployment-apiid
        """
        return self._values.get('api_id')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Deployment.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-deployment.html#cfn-apigatewayv2-deployment-description
        """
        return self._values.get('description')

    @builtins.property
    def stage_name(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Deployment.StageName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-deployment.html#cfn-apigatewayv2-deployment-stagename
        """
        return self._values.get('stage_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnDeploymentProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnDomainName(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigatewayv2.CfnDomainName"):
    """A CloudFormation ``AWS::ApiGatewayV2::DomainName``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-domainname.html
    cloudformationResource:
    :cloudformationResource:: AWS::ApiGatewayV2::DomainName
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, domain_name: str, domain_name_configurations: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["DomainNameConfigurationProperty", aws_cdk.core.IResolvable]]]]=None, tags: typing.Any=None) -> None:
        """Create a new ``AWS::ApiGatewayV2::DomainName``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param domain_name: ``AWS::ApiGatewayV2::DomainName.DomainName``.
        :param domain_name_configurations: ``AWS::ApiGatewayV2::DomainName.DomainNameConfigurations``.
        :param tags: ``AWS::ApiGatewayV2::DomainName.Tags``.
        """
        props = CfnDomainNameProps(domain_name=domain_name, domain_name_configurations=domain_name_configurations, tags=tags)

        jsii.create(CfnDomainName, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnDomainName":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="attrRegionalDomainName")
    def attr_regional_domain_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: RegionalDomainName
        """
        return jsii.get(self, "attrRegionalDomainName")

    @builtins.property
    @jsii.member(jsii_name="attrRegionalHostedZoneId")
    def attr_regional_hosted_zone_id(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: RegionalHostedZoneId
        """
        return jsii.get(self, "attrRegionalHostedZoneId")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::ApiGatewayV2::DomainName.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-domainname.html#cfn-apigatewayv2-domainname-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> str:
        """``AWS::ApiGatewayV2::DomainName.DomainName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-domainname.html#cfn-apigatewayv2-domainname-domainname
        """
        return jsii.get(self, "domainName")

    @domain_name.setter
    def domain_name(self, value: str) -> None:
        jsii.set(self, "domainName", value)

    @builtins.property
    @jsii.member(jsii_name="domainNameConfigurations")
    def domain_name_configurations(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["DomainNameConfigurationProperty", aws_cdk.core.IResolvable]]]]:
        """``AWS::ApiGatewayV2::DomainName.DomainNameConfigurations``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-domainname.html#cfn-apigatewayv2-domainname-domainnameconfigurations
        """
        return jsii.get(self, "domainNameConfigurations")

    @domain_name_configurations.setter
    def domain_name_configurations(self, value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["DomainNameConfigurationProperty", aws_cdk.core.IResolvable]]]]) -> None:
        jsii.set(self, "domainNameConfigurations", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-apigatewayv2.CfnDomainName.DomainNameConfigurationProperty", jsii_struct_bases=[], name_mapping={'certificate_arn': 'certificateArn', 'certificate_name': 'certificateName', 'endpoint_type': 'endpointType'})
    class DomainNameConfigurationProperty():
        def __init__(self, *, certificate_arn: typing.Optional[str]=None, certificate_name: typing.Optional[str]=None, endpoint_type: typing.Optional[str]=None) -> None:
            """
            :param certificate_arn: ``CfnDomainName.DomainNameConfigurationProperty.CertificateArn``.
            :param certificate_name: ``CfnDomainName.DomainNameConfigurationProperty.CertificateName``.
            :param endpoint_type: ``CfnDomainName.DomainNameConfigurationProperty.EndpointType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-domainname-domainnameconfiguration.html
            """
            self._values = {
            }
            if certificate_arn is not None: self._values["certificate_arn"] = certificate_arn
            if certificate_name is not None: self._values["certificate_name"] = certificate_name
            if endpoint_type is not None: self._values["endpoint_type"] = endpoint_type

        @builtins.property
        def certificate_arn(self) -> typing.Optional[str]:
            """``CfnDomainName.DomainNameConfigurationProperty.CertificateArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-domainname-domainnameconfiguration.html#cfn-apigatewayv2-domainname-domainnameconfiguration-certificatearn
            """
            return self._values.get('certificate_arn')

        @builtins.property
        def certificate_name(self) -> typing.Optional[str]:
            """``CfnDomainName.DomainNameConfigurationProperty.CertificateName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-domainname-domainnameconfiguration.html#cfn-apigatewayv2-domainname-domainnameconfiguration-certificatename
            """
            return self._values.get('certificate_name')

        @builtins.property
        def endpoint_type(self) -> typing.Optional[str]:
            """``CfnDomainName.DomainNameConfigurationProperty.EndpointType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-domainname-domainnameconfiguration.html#cfn-apigatewayv2-domainname-domainnameconfiguration-endpointtype
            """
            return self._values.get('endpoint_type')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'DomainNameConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-apigatewayv2.CfnDomainNameProps", jsii_struct_bases=[], name_mapping={'domain_name': 'domainName', 'domain_name_configurations': 'domainNameConfigurations', 'tags': 'tags'})
class CfnDomainNameProps():
    def __init__(self, *, domain_name: str, domain_name_configurations: typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnDomainName.DomainNameConfigurationProperty", aws_cdk.core.IResolvable]]]]=None, tags: typing.Any=None) -> None:
        """Properties for defining a ``AWS::ApiGatewayV2::DomainName``.

        :param domain_name: ``AWS::ApiGatewayV2::DomainName.DomainName``.
        :param domain_name_configurations: ``AWS::ApiGatewayV2::DomainName.DomainNameConfigurations``.
        :param tags: ``AWS::ApiGatewayV2::DomainName.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-domainname.html
        """
        self._values = {
            'domain_name': domain_name,
        }
        if domain_name_configurations is not None: self._values["domain_name_configurations"] = domain_name_configurations
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def domain_name(self) -> str:
        """``AWS::ApiGatewayV2::DomainName.DomainName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-domainname.html#cfn-apigatewayv2-domainname-domainname
        """
        return self._values.get('domain_name')

    @builtins.property
    def domain_name_configurations(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union["CfnDomainName.DomainNameConfigurationProperty", aws_cdk.core.IResolvable]]]]:
        """``AWS::ApiGatewayV2::DomainName.DomainNameConfigurations``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-domainname.html#cfn-apigatewayv2-domainname-domainnameconfigurations
        """
        return self._values.get('domain_name_configurations')

    @builtins.property
    def tags(self) -> typing.Any:
        """``AWS::ApiGatewayV2::DomainName.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-domainname.html#cfn-apigatewayv2-domainname-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnDomainNameProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnIntegration(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigatewayv2.CfnIntegration"):
    """A CloudFormation ``AWS::ApiGatewayV2::Integration``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html
    cloudformationResource:
    :cloudformationResource:: AWS::ApiGatewayV2::Integration
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, api_id: str, integration_type: str, connection_id: typing.Optional[str]=None, connection_type: typing.Optional[str]=None, content_handling_strategy: typing.Optional[str]=None, credentials_arn: typing.Optional[str]=None, description: typing.Optional[str]=None, integration_method: typing.Optional[str]=None, integration_uri: typing.Optional[str]=None, passthrough_behavior: typing.Optional[str]=None, payload_format_version: typing.Optional[str]=None, request_parameters: typing.Any=None, request_templates: typing.Any=None, template_selection_expression: typing.Optional[str]=None, timeout_in_millis: typing.Optional[jsii.Number]=None, tls_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "TlsConfigProperty"]]=None) -> None:
        """Create a new ``AWS::ApiGatewayV2::Integration``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_id: ``AWS::ApiGatewayV2::Integration.ApiId``.
        :param integration_type: ``AWS::ApiGatewayV2::Integration.IntegrationType``.
        :param connection_id: ``AWS::ApiGatewayV2::Integration.ConnectionId``.
        :param connection_type: ``AWS::ApiGatewayV2::Integration.ConnectionType``.
        :param content_handling_strategy: ``AWS::ApiGatewayV2::Integration.ContentHandlingStrategy``.
        :param credentials_arn: ``AWS::ApiGatewayV2::Integration.CredentialsArn``.
        :param description: ``AWS::ApiGatewayV2::Integration.Description``.
        :param integration_method: ``AWS::ApiGatewayV2::Integration.IntegrationMethod``.
        :param integration_uri: ``AWS::ApiGatewayV2::Integration.IntegrationUri``.
        :param passthrough_behavior: ``AWS::ApiGatewayV2::Integration.PassthroughBehavior``.
        :param payload_format_version: ``AWS::ApiGatewayV2::Integration.PayloadFormatVersion``.
        :param request_parameters: ``AWS::ApiGatewayV2::Integration.RequestParameters``.
        :param request_templates: ``AWS::ApiGatewayV2::Integration.RequestTemplates``.
        :param template_selection_expression: ``AWS::ApiGatewayV2::Integration.TemplateSelectionExpression``.
        :param timeout_in_millis: ``AWS::ApiGatewayV2::Integration.TimeoutInMillis``.
        :param tls_config: ``AWS::ApiGatewayV2::Integration.TlsConfig``.
        """
        props = CfnIntegrationProps(api_id=api_id, integration_type=integration_type, connection_id=connection_id, connection_type=connection_type, content_handling_strategy=content_handling_strategy, credentials_arn=credentials_arn, description=description, integration_method=integration_method, integration_uri=integration_uri, passthrough_behavior=passthrough_behavior, payload_format_version=payload_format_version, request_parameters=request_parameters, request_templates=request_templates, template_selection_expression=template_selection_expression, timeout_in_millis=timeout_in_millis, tls_config=tls_config)

        jsii.create(CfnIntegration, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnIntegration":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> str:
        """``AWS::ApiGatewayV2::Integration.ApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-apiid
        """
        return jsii.get(self, "apiId")

    @api_id.setter
    def api_id(self, value: str) -> None:
        jsii.set(self, "apiId", value)

    @builtins.property
    @jsii.member(jsii_name="integrationType")
    def integration_type(self) -> str:
        """``AWS::ApiGatewayV2::Integration.IntegrationType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-integrationtype
        """
        return jsii.get(self, "integrationType")

    @integration_type.setter
    def integration_type(self, value: str) -> None:
        jsii.set(self, "integrationType", value)

    @builtins.property
    @jsii.member(jsii_name="requestParameters")
    def request_parameters(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Integration.RequestParameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-requestparameters
        """
        return jsii.get(self, "requestParameters")

    @request_parameters.setter
    def request_parameters(self, value: typing.Any) -> None:
        jsii.set(self, "requestParameters", value)

    @builtins.property
    @jsii.member(jsii_name="requestTemplates")
    def request_templates(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Integration.RequestTemplates``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-requesttemplates
        """
        return jsii.get(self, "requestTemplates")

    @request_templates.setter
    def request_templates(self, value: typing.Any) -> None:
        jsii.set(self, "requestTemplates", value)

    @builtins.property
    @jsii.member(jsii_name="connectionId")
    def connection_id(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Integration.ConnectionId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-connectionid
        """
        return jsii.get(self, "connectionId")

    @connection_id.setter
    def connection_id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "connectionId", value)

    @builtins.property
    @jsii.member(jsii_name="connectionType")
    def connection_type(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Integration.ConnectionType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-connectiontype
        """
        return jsii.get(self, "connectionType")

    @connection_type.setter
    def connection_type(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "connectionType", value)

    @builtins.property
    @jsii.member(jsii_name="contentHandlingStrategy")
    def content_handling_strategy(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Integration.ContentHandlingStrategy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-contenthandlingstrategy
        """
        return jsii.get(self, "contentHandlingStrategy")

    @content_handling_strategy.setter
    def content_handling_strategy(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "contentHandlingStrategy", value)

    @builtins.property
    @jsii.member(jsii_name="credentialsArn")
    def credentials_arn(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Integration.CredentialsArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-credentialsarn
        """
        return jsii.get(self, "credentialsArn")

    @credentials_arn.setter
    def credentials_arn(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "credentialsArn", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Integration.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="integrationMethod")
    def integration_method(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Integration.IntegrationMethod``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-integrationmethod
        """
        return jsii.get(self, "integrationMethod")

    @integration_method.setter
    def integration_method(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "integrationMethod", value)

    @builtins.property
    @jsii.member(jsii_name="integrationUri")
    def integration_uri(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Integration.IntegrationUri``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-integrationuri
        """
        return jsii.get(self, "integrationUri")

    @integration_uri.setter
    def integration_uri(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "integrationUri", value)

    @builtins.property
    @jsii.member(jsii_name="passthroughBehavior")
    def passthrough_behavior(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Integration.PassthroughBehavior``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-passthroughbehavior
        """
        return jsii.get(self, "passthroughBehavior")

    @passthrough_behavior.setter
    def passthrough_behavior(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "passthroughBehavior", value)

    @builtins.property
    @jsii.member(jsii_name="payloadFormatVersion")
    def payload_format_version(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Integration.PayloadFormatVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-payloadformatversion
        """
        return jsii.get(self, "payloadFormatVersion")

    @payload_format_version.setter
    def payload_format_version(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "payloadFormatVersion", value)

    @builtins.property
    @jsii.member(jsii_name="templateSelectionExpression")
    def template_selection_expression(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Integration.TemplateSelectionExpression``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-templateselectionexpression
        """
        return jsii.get(self, "templateSelectionExpression")

    @template_selection_expression.setter
    def template_selection_expression(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "templateSelectionExpression", value)

    @builtins.property
    @jsii.member(jsii_name="timeoutInMillis")
    def timeout_in_millis(self) -> typing.Optional[jsii.Number]:
        """``AWS::ApiGatewayV2::Integration.TimeoutInMillis``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-timeoutinmillis
        """
        return jsii.get(self, "timeoutInMillis")

    @timeout_in_millis.setter
    def timeout_in_millis(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "timeoutInMillis", value)

    @builtins.property
    @jsii.member(jsii_name="tlsConfig")
    def tls_config(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "TlsConfigProperty"]]:
        """``AWS::ApiGatewayV2::Integration.TlsConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-tlsconfig
        """
        return jsii.get(self, "tlsConfig")

    @tls_config.setter
    def tls_config(self, value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "TlsConfigProperty"]]) -> None:
        jsii.set(self, "tlsConfig", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-apigatewayv2.CfnIntegration.TlsConfigProperty", jsii_struct_bases=[], name_mapping={'server_name_to_verify': 'serverNameToVerify'})
    class TlsConfigProperty():
        def __init__(self, *, server_name_to_verify: typing.Optional[str]=None) -> None:
            """
            :param server_name_to_verify: ``CfnIntegration.TlsConfigProperty.ServerNameToVerify``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-integration-tlsconfig.html
            """
            self._values = {
            }
            if server_name_to_verify is not None: self._values["server_name_to_verify"] = server_name_to_verify

        @builtins.property
        def server_name_to_verify(self) -> typing.Optional[str]:
            """``CfnIntegration.TlsConfigProperty.ServerNameToVerify``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-integration-tlsconfig.html#cfn-apigatewayv2-integration-tlsconfig-servernametoverify
            """
            return self._values.get('server_name_to_verify')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'TlsConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-apigatewayv2.CfnIntegrationProps", jsii_struct_bases=[], name_mapping={'api_id': 'apiId', 'integration_type': 'integrationType', 'connection_id': 'connectionId', 'connection_type': 'connectionType', 'content_handling_strategy': 'contentHandlingStrategy', 'credentials_arn': 'credentialsArn', 'description': 'description', 'integration_method': 'integrationMethod', 'integration_uri': 'integrationUri', 'passthrough_behavior': 'passthroughBehavior', 'payload_format_version': 'payloadFormatVersion', 'request_parameters': 'requestParameters', 'request_templates': 'requestTemplates', 'template_selection_expression': 'templateSelectionExpression', 'timeout_in_millis': 'timeoutInMillis', 'tls_config': 'tlsConfig'})
class CfnIntegrationProps():
    def __init__(self, *, api_id: str, integration_type: str, connection_id: typing.Optional[str]=None, connection_type: typing.Optional[str]=None, content_handling_strategy: typing.Optional[str]=None, credentials_arn: typing.Optional[str]=None, description: typing.Optional[str]=None, integration_method: typing.Optional[str]=None, integration_uri: typing.Optional[str]=None, passthrough_behavior: typing.Optional[str]=None, payload_format_version: typing.Optional[str]=None, request_parameters: typing.Any=None, request_templates: typing.Any=None, template_selection_expression: typing.Optional[str]=None, timeout_in_millis: typing.Optional[jsii.Number]=None, tls_config: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnIntegration.TlsConfigProperty"]]=None) -> None:
        """Properties for defining a ``AWS::ApiGatewayV2::Integration``.

        :param api_id: ``AWS::ApiGatewayV2::Integration.ApiId``.
        :param integration_type: ``AWS::ApiGatewayV2::Integration.IntegrationType``.
        :param connection_id: ``AWS::ApiGatewayV2::Integration.ConnectionId``.
        :param connection_type: ``AWS::ApiGatewayV2::Integration.ConnectionType``.
        :param content_handling_strategy: ``AWS::ApiGatewayV2::Integration.ContentHandlingStrategy``.
        :param credentials_arn: ``AWS::ApiGatewayV2::Integration.CredentialsArn``.
        :param description: ``AWS::ApiGatewayV2::Integration.Description``.
        :param integration_method: ``AWS::ApiGatewayV2::Integration.IntegrationMethod``.
        :param integration_uri: ``AWS::ApiGatewayV2::Integration.IntegrationUri``.
        :param passthrough_behavior: ``AWS::ApiGatewayV2::Integration.PassthroughBehavior``.
        :param payload_format_version: ``AWS::ApiGatewayV2::Integration.PayloadFormatVersion``.
        :param request_parameters: ``AWS::ApiGatewayV2::Integration.RequestParameters``.
        :param request_templates: ``AWS::ApiGatewayV2::Integration.RequestTemplates``.
        :param template_selection_expression: ``AWS::ApiGatewayV2::Integration.TemplateSelectionExpression``.
        :param timeout_in_millis: ``AWS::ApiGatewayV2::Integration.TimeoutInMillis``.
        :param tls_config: ``AWS::ApiGatewayV2::Integration.TlsConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html
        """
        self._values = {
            'api_id': api_id,
            'integration_type': integration_type,
        }
        if connection_id is not None: self._values["connection_id"] = connection_id
        if connection_type is not None: self._values["connection_type"] = connection_type
        if content_handling_strategy is not None: self._values["content_handling_strategy"] = content_handling_strategy
        if credentials_arn is not None: self._values["credentials_arn"] = credentials_arn
        if description is not None: self._values["description"] = description
        if integration_method is not None: self._values["integration_method"] = integration_method
        if integration_uri is not None: self._values["integration_uri"] = integration_uri
        if passthrough_behavior is not None: self._values["passthrough_behavior"] = passthrough_behavior
        if payload_format_version is not None: self._values["payload_format_version"] = payload_format_version
        if request_parameters is not None: self._values["request_parameters"] = request_parameters
        if request_templates is not None: self._values["request_templates"] = request_templates
        if template_selection_expression is not None: self._values["template_selection_expression"] = template_selection_expression
        if timeout_in_millis is not None: self._values["timeout_in_millis"] = timeout_in_millis
        if tls_config is not None: self._values["tls_config"] = tls_config

    @builtins.property
    def api_id(self) -> str:
        """``AWS::ApiGatewayV2::Integration.ApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-apiid
        """
        return self._values.get('api_id')

    @builtins.property
    def integration_type(self) -> str:
        """``AWS::ApiGatewayV2::Integration.IntegrationType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-integrationtype
        """
        return self._values.get('integration_type')

    @builtins.property
    def connection_id(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Integration.ConnectionId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-connectionid
        """
        return self._values.get('connection_id')

    @builtins.property
    def connection_type(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Integration.ConnectionType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-connectiontype
        """
        return self._values.get('connection_type')

    @builtins.property
    def content_handling_strategy(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Integration.ContentHandlingStrategy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-contenthandlingstrategy
        """
        return self._values.get('content_handling_strategy')

    @builtins.property
    def credentials_arn(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Integration.CredentialsArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-credentialsarn
        """
        return self._values.get('credentials_arn')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Integration.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-description
        """
        return self._values.get('description')

    @builtins.property
    def integration_method(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Integration.IntegrationMethod``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-integrationmethod
        """
        return self._values.get('integration_method')

    @builtins.property
    def integration_uri(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Integration.IntegrationUri``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-integrationuri
        """
        return self._values.get('integration_uri')

    @builtins.property
    def passthrough_behavior(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Integration.PassthroughBehavior``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-passthroughbehavior
        """
        return self._values.get('passthrough_behavior')

    @builtins.property
    def payload_format_version(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Integration.PayloadFormatVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-payloadformatversion
        """
        return self._values.get('payload_format_version')

    @builtins.property
    def request_parameters(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Integration.RequestParameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-requestparameters
        """
        return self._values.get('request_parameters')

    @builtins.property
    def request_templates(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Integration.RequestTemplates``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-requesttemplates
        """
        return self._values.get('request_templates')

    @builtins.property
    def template_selection_expression(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Integration.TemplateSelectionExpression``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-templateselectionexpression
        """
        return self._values.get('template_selection_expression')

    @builtins.property
    def timeout_in_millis(self) -> typing.Optional[jsii.Number]:
        """``AWS::ApiGatewayV2::Integration.TimeoutInMillis``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-timeoutinmillis
        """
        return self._values.get('timeout_in_millis')

    @builtins.property
    def tls_config(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnIntegration.TlsConfigProperty"]]:
        """``AWS::ApiGatewayV2::Integration.TlsConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integration.html#cfn-apigatewayv2-integration-tlsconfig
        """
        return self._values.get('tls_config')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnIntegrationProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnIntegrationResponse(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigatewayv2.CfnIntegrationResponse"):
    """A CloudFormation ``AWS::ApiGatewayV2::IntegrationResponse``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html
    cloudformationResource:
    :cloudformationResource:: AWS::ApiGatewayV2::IntegrationResponse
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, api_id: str, integration_id: str, integration_response_key: str, content_handling_strategy: typing.Optional[str]=None, response_parameters: typing.Any=None, response_templates: typing.Any=None, template_selection_expression: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::ApiGatewayV2::IntegrationResponse``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_id: ``AWS::ApiGatewayV2::IntegrationResponse.ApiId``.
        :param integration_id: ``AWS::ApiGatewayV2::IntegrationResponse.IntegrationId``.
        :param integration_response_key: ``AWS::ApiGatewayV2::IntegrationResponse.IntegrationResponseKey``.
        :param content_handling_strategy: ``AWS::ApiGatewayV2::IntegrationResponse.ContentHandlingStrategy``.
        :param response_parameters: ``AWS::ApiGatewayV2::IntegrationResponse.ResponseParameters``.
        :param response_templates: ``AWS::ApiGatewayV2::IntegrationResponse.ResponseTemplates``.
        :param template_selection_expression: ``AWS::ApiGatewayV2::IntegrationResponse.TemplateSelectionExpression``.
        """
        props = CfnIntegrationResponseProps(api_id=api_id, integration_id=integration_id, integration_response_key=integration_response_key, content_handling_strategy=content_handling_strategy, response_parameters=response_parameters, response_templates=response_templates, template_selection_expression=template_selection_expression)

        jsii.create(CfnIntegrationResponse, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnIntegrationResponse":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> str:
        """``AWS::ApiGatewayV2::IntegrationResponse.ApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-apiid
        """
        return jsii.get(self, "apiId")

    @api_id.setter
    def api_id(self, value: str) -> None:
        jsii.set(self, "apiId", value)

    @builtins.property
    @jsii.member(jsii_name="integrationId")
    def integration_id(self) -> str:
        """``AWS::ApiGatewayV2::IntegrationResponse.IntegrationId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-integrationid
        """
        return jsii.get(self, "integrationId")

    @integration_id.setter
    def integration_id(self, value: str) -> None:
        jsii.set(self, "integrationId", value)

    @builtins.property
    @jsii.member(jsii_name="integrationResponseKey")
    def integration_response_key(self) -> str:
        """``AWS::ApiGatewayV2::IntegrationResponse.IntegrationResponseKey``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-integrationresponsekey
        """
        return jsii.get(self, "integrationResponseKey")

    @integration_response_key.setter
    def integration_response_key(self, value: str) -> None:
        jsii.set(self, "integrationResponseKey", value)

    @builtins.property
    @jsii.member(jsii_name="responseParameters")
    def response_parameters(self) -> typing.Any:
        """``AWS::ApiGatewayV2::IntegrationResponse.ResponseParameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-responseparameters
        """
        return jsii.get(self, "responseParameters")

    @response_parameters.setter
    def response_parameters(self, value: typing.Any) -> None:
        jsii.set(self, "responseParameters", value)

    @builtins.property
    @jsii.member(jsii_name="responseTemplates")
    def response_templates(self) -> typing.Any:
        """``AWS::ApiGatewayV2::IntegrationResponse.ResponseTemplates``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-responsetemplates
        """
        return jsii.get(self, "responseTemplates")

    @response_templates.setter
    def response_templates(self, value: typing.Any) -> None:
        jsii.set(self, "responseTemplates", value)

    @builtins.property
    @jsii.member(jsii_name="contentHandlingStrategy")
    def content_handling_strategy(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::IntegrationResponse.ContentHandlingStrategy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-contenthandlingstrategy
        """
        return jsii.get(self, "contentHandlingStrategy")

    @content_handling_strategy.setter
    def content_handling_strategy(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "contentHandlingStrategy", value)

    @builtins.property
    @jsii.member(jsii_name="templateSelectionExpression")
    def template_selection_expression(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::IntegrationResponse.TemplateSelectionExpression``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-templateselectionexpression
        """
        return jsii.get(self, "templateSelectionExpression")

    @template_selection_expression.setter
    def template_selection_expression(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "templateSelectionExpression", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-apigatewayv2.CfnIntegrationResponseProps", jsii_struct_bases=[], name_mapping={'api_id': 'apiId', 'integration_id': 'integrationId', 'integration_response_key': 'integrationResponseKey', 'content_handling_strategy': 'contentHandlingStrategy', 'response_parameters': 'responseParameters', 'response_templates': 'responseTemplates', 'template_selection_expression': 'templateSelectionExpression'})
class CfnIntegrationResponseProps():
    def __init__(self, *, api_id: str, integration_id: str, integration_response_key: str, content_handling_strategy: typing.Optional[str]=None, response_parameters: typing.Any=None, response_templates: typing.Any=None, template_selection_expression: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::ApiGatewayV2::IntegrationResponse``.

        :param api_id: ``AWS::ApiGatewayV2::IntegrationResponse.ApiId``.
        :param integration_id: ``AWS::ApiGatewayV2::IntegrationResponse.IntegrationId``.
        :param integration_response_key: ``AWS::ApiGatewayV2::IntegrationResponse.IntegrationResponseKey``.
        :param content_handling_strategy: ``AWS::ApiGatewayV2::IntegrationResponse.ContentHandlingStrategy``.
        :param response_parameters: ``AWS::ApiGatewayV2::IntegrationResponse.ResponseParameters``.
        :param response_templates: ``AWS::ApiGatewayV2::IntegrationResponse.ResponseTemplates``.
        :param template_selection_expression: ``AWS::ApiGatewayV2::IntegrationResponse.TemplateSelectionExpression``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html
        """
        self._values = {
            'api_id': api_id,
            'integration_id': integration_id,
            'integration_response_key': integration_response_key,
        }
        if content_handling_strategy is not None: self._values["content_handling_strategy"] = content_handling_strategy
        if response_parameters is not None: self._values["response_parameters"] = response_parameters
        if response_templates is not None: self._values["response_templates"] = response_templates
        if template_selection_expression is not None: self._values["template_selection_expression"] = template_selection_expression

    @builtins.property
    def api_id(self) -> str:
        """``AWS::ApiGatewayV2::IntegrationResponse.ApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-apiid
        """
        return self._values.get('api_id')

    @builtins.property
    def integration_id(self) -> str:
        """``AWS::ApiGatewayV2::IntegrationResponse.IntegrationId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-integrationid
        """
        return self._values.get('integration_id')

    @builtins.property
    def integration_response_key(self) -> str:
        """``AWS::ApiGatewayV2::IntegrationResponse.IntegrationResponseKey``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-integrationresponsekey
        """
        return self._values.get('integration_response_key')

    @builtins.property
    def content_handling_strategy(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::IntegrationResponse.ContentHandlingStrategy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-contenthandlingstrategy
        """
        return self._values.get('content_handling_strategy')

    @builtins.property
    def response_parameters(self) -> typing.Any:
        """``AWS::ApiGatewayV2::IntegrationResponse.ResponseParameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-responseparameters
        """
        return self._values.get('response_parameters')

    @builtins.property
    def response_templates(self) -> typing.Any:
        """``AWS::ApiGatewayV2::IntegrationResponse.ResponseTemplates``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-responsetemplates
        """
        return self._values.get('response_templates')

    @builtins.property
    def template_selection_expression(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::IntegrationResponse.TemplateSelectionExpression``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-integrationresponse.html#cfn-apigatewayv2-integrationresponse-templateselectionexpression
        """
        return self._values.get('template_selection_expression')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnIntegrationResponseProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnModel(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigatewayv2.CfnModel"):
    """A CloudFormation ``AWS::ApiGatewayV2::Model``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-model.html
    cloudformationResource:
    :cloudformationResource:: AWS::ApiGatewayV2::Model
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, api_id: str, name: str, schema: typing.Any, content_type: typing.Optional[str]=None, description: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::ApiGatewayV2::Model``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_id: ``AWS::ApiGatewayV2::Model.ApiId``.
        :param name: ``AWS::ApiGatewayV2::Model.Name``.
        :param schema: ``AWS::ApiGatewayV2::Model.Schema``.
        :param content_type: ``AWS::ApiGatewayV2::Model.ContentType``.
        :param description: ``AWS::ApiGatewayV2::Model.Description``.
        """
        props = CfnModelProps(api_id=api_id, name=name, schema=schema, content_type=content_type, description=description)

        jsii.create(CfnModel, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnModel":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> str:
        """``AWS::ApiGatewayV2::Model.ApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-model.html#cfn-apigatewayv2-model-apiid
        """
        return jsii.get(self, "apiId")

    @api_id.setter
    def api_id(self, value: str) -> None:
        jsii.set(self, "apiId", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """``AWS::ApiGatewayV2::Model.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-model.html#cfn-apigatewayv2-model-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Model.Schema``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-model.html#cfn-apigatewayv2-model-schema
        """
        return jsii.get(self, "schema")

    @schema.setter
    def schema(self, value: typing.Any) -> None:
        jsii.set(self, "schema", value)

    @builtins.property
    @jsii.member(jsii_name="contentType")
    def content_type(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Model.ContentType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-model.html#cfn-apigatewayv2-model-contenttype
        """
        return jsii.get(self, "contentType")

    @content_type.setter
    def content_type(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "contentType", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Model.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-model.html#cfn-apigatewayv2-model-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-apigatewayv2.CfnModelProps", jsii_struct_bases=[], name_mapping={'api_id': 'apiId', 'name': 'name', 'schema': 'schema', 'content_type': 'contentType', 'description': 'description'})
class CfnModelProps():
    def __init__(self, *, api_id: str, name: str, schema: typing.Any, content_type: typing.Optional[str]=None, description: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::ApiGatewayV2::Model``.

        :param api_id: ``AWS::ApiGatewayV2::Model.ApiId``.
        :param name: ``AWS::ApiGatewayV2::Model.Name``.
        :param schema: ``AWS::ApiGatewayV2::Model.Schema``.
        :param content_type: ``AWS::ApiGatewayV2::Model.ContentType``.
        :param description: ``AWS::ApiGatewayV2::Model.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-model.html
        """
        self._values = {
            'api_id': api_id,
            'name': name,
            'schema': schema,
        }
        if content_type is not None: self._values["content_type"] = content_type
        if description is not None: self._values["description"] = description

    @builtins.property
    def api_id(self) -> str:
        """``AWS::ApiGatewayV2::Model.ApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-model.html#cfn-apigatewayv2-model-apiid
        """
        return self._values.get('api_id')

    @builtins.property
    def name(self) -> str:
        """``AWS::ApiGatewayV2::Model.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-model.html#cfn-apigatewayv2-model-name
        """
        return self._values.get('name')

    @builtins.property
    def schema(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Model.Schema``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-model.html#cfn-apigatewayv2-model-schema
        """
        return self._values.get('schema')

    @builtins.property
    def content_type(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Model.ContentType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-model.html#cfn-apigatewayv2-model-contenttype
        """
        return self._values.get('content_type')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Model.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-model.html#cfn-apigatewayv2-model-description
        """
        return self._values.get('description')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnModelProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnRoute(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigatewayv2.CfnRoute"):
    """A CloudFormation ``AWS::ApiGatewayV2::Route``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html
    cloudformationResource:
    :cloudformationResource:: AWS::ApiGatewayV2::Route
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, api_id: str, route_key: str, api_key_required: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]=None, authorization_scopes: typing.Optional[typing.List[str]]=None, authorization_type: typing.Optional[str]=None, authorizer_id: typing.Optional[str]=None, model_selection_expression: typing.Optional[str]=None, operation_name: typing.Optional[str]=None, request_models: typing.Any=None, request_parameters: typing.Any=None, route_response_selection_expression: typing.Optional[str]=None, target: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::ApiGatewayV2::Route``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_id: ``AWS::ApiGatewayV2::Route.ApiId``.
        :param route_key: ``AWS::ApiGatewayV2::Route.RouteKey``.
        :param api_key_required: ``AWS::ApiGatewayV2::Route.ApiKeyRequired``.
        :param authorization_scopes: ``AWS::ApiGatewayV2::Route.AuthorizationScopes``.
        :param authorization_type: ``AWS::ApiGatewayV2::Route.AuthorizationType``.
        :param authorizer_id: ``AWS::ApiGatewayV2::Route.AuthorizerId``.
        :param model_selection_expression: ``AWS::ApiGatewayV2::Route.ModelSelectionExpression``.
        :param operation_name: ``AWS::ApiGatewayV2::Route.OperationName``.
        :param request_models: ``AWS::ApiGatewayV2::Route.RequestModels``.
        :param request_parameters: ``AWS::ApiGatewayV2::Route.RequestParameters``.
        :param route_response_selection_expression: ``AWS::ApiGatewayV2::Route.RouteResponseSelectionExpression``.
        :param target: ``AWS::ApiGatewayV2::Route.Target``.
        """
        props = CfnRouteProps(api_id=api_id, route_key=route_key, api_key_required=api_key_required, authorization_scopes=authorization_scopes, authorization_type=authorization_type, authorizer_id=authorizer_id, model_selection_expression=model_selection_expression, operation_name=operation_name, request_models=request_models, request_parameters=request_parameters, route_response_selection_expression=route_response_selection_expression, target=target)

        jsii.create(CfnRoute, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnRoute":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> str:
        """``AWS::ApiGatewayV2::Route.ApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-apiid
        """
        return jsii.get(self, "apiId")

    @api_id.setter
    def api_id(self, value: str) -> None:
        jsii.set(self, "apiId", value)

    @builtins.property
    @jsii.member(jsii_name="requestModels")
    def request_models(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Route.RequestModels``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-requestmodels
        """
        return jsii.get(self, "requestModels")

    @request_models.setter
    def request_models(self, value: typing.Any) -> None:
        jsii.set(self, "requestModels", value)

    @builtins.property
    @jsii.member(jsii_name="requestParameters")
    def request_parameters(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Route.RequestParameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-requestparameters
        """
        return jsii.get(self, "requestParameters")

    @request_parameters.setter
    def request_parameters(self, value: typing.Any) -> None:
        jsii.set(self, "requestParameters", value)

    @builtins.property
    @jsii.member(jsii_name="routeKey")
    def route_key(self) -> str:
        """``AWS::ApiGatewayV2::Route.RouteKey``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-routekey
        """
        return jsii.get(self, "routeKey")

    @route_key.setter
    def route_key(self, value: str) -> None:
        jsii.set(self, "routeKey", value)

    @builtins.property
    @jsii.member(jsii_name="apiKeyRequired")
    def api_key_required(self) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
        """``AWS::ApiGatewayV2::Route.ApiKeyRequired``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-apikeyrequired
        """
        return jsii.get(self, "apiKeyRequired")

    @api_key_required.setter
    def api_key_required(self, value: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]) -> None:
        jsii.set(self, "apiKeyRequired", value)

    @builtins.property
    @jsii.member(jsii_name="authorizationScopes")
    def authorization_scopes(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ApiGatewayV2::Route.AuthorizationScopes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-authorizationscopes
        """
        return jsii.get(self, "authorizationScopes")

    @authorization_scopes.setter
    def authorization_scopes(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "authorizationScopes", value)

    @builtins.property
    @jsii.member(jsii_name="authorizationType")
    def authorization_type(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Route.AuthorizationType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-authorizationtype
        """
        return jsii.get(self, "authorizationType")

    @authorization_type.setter
    def authorization_type(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "authorizationType", value)

    @builtins.property
    @jsii.member(jsii_name="authorizerId")
    def authorizer_id(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Route.AuthorizerId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-authorizerid
        """
        return jsii.get(self, "authorizerId")

    @authorizer_id.setter
    def authorizer_id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "authorizerId", value)

    @builtins.property
    @jsii.member(jsii_name="modelSelectionExpression")
    def model_selection_expression(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Route.ModelSelectionExpression``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-modelselectionexpression
        """
        return jsii.get(self, "modelSelectionExpression")

    @model_selection_expression.setter
    def model_selection_expression(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "modelSelectionExpression", value)

    @builtins.property
    @jsii.member(jsii_name="operationName")
    def operation_name(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Route.OperationName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-operationname
        """
        return jsii.get(self, "operationName")

    @operation_name.setter
    def operation_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "operationName", value)

    @builtins.property
    @jsii.member(jsii_name="routeResponseSelectionExpression")
    def route_response_selection_expression(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Route.RouteResponseSelectionExpression``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-routeresponseselectionexpression
        """
        return jsii.get(self, "routeResponseSelectionExpression")

    @route_response_selection_expression.setter
    def route_response_selection_expression(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "routeResponseSelectionExpression", value)

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Route.Target``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-target
        """
        return jsii.get(self, "target")

    @target.setter
    def target(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "target", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-apigatewayv2.CfnRoute.ParameterConstraintsProperty", jsii_struct_bases=[], name_mapping={'required': 'required'})
    class ParameterConstraintsProperty():
        def __init__(self, *, required: typing.Union[bool, aws_cdk.core.IResolvable]) -> None:
            """
            :param required: ``CfnRoute.ParameterConstraintsProperty.Required``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-route-parameterconstraints.html
            """
            self._values = {
                'required': required,
            }

        @builtins.property
        def required(self) -> typing.Union[bool, aws_cdk.core.IResolvable]:
            """``CfnRoute.ParameterConstraintsProperty.Required``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-route-parameterconstraints.html#cfn-apigatewayv2-route-parameterconstraints-required
            """
            return self._values.get('required')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ParameterConstraintsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-apigatewayv2.CfnRouteProps", jsii_struct_bases=[], name_mapping={'api_id': 'apiId', 'route_key': 'routeKey', 'api_key_required': 'apiKeyRequired', 'authorization_scopes': 'authorizationScopes', 'authorization_type': 'authorizationType', 'authorizer_id': 'authorizerId', 'model_selection_expression': 'modelSelectionExpression', 'operation_name': 'operationName', 'request_models': 'requestModels', 'request_parameters': 'requestParameters', 'route_response_selection_expression': 'routeResponseSelectionExpression', 'target': 'target'})
class CfnRouteProps():
    def __init__(self, *, api_id: str, route_key: str, api_key_required: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]=None, authorization_scopes: typing.Optional[typing.List[str]]=None, authorization_type: typing.Optional[str]=None, authorizer_id: typing.Optional[str]=None, model_selection_expression: typing.Optional[str]=None, operation_name: typing.Optional[str]=None, request_models: typing.Any=None, request_parameters: typing.Any=None, route_response_selection_expression: typing.Optional[str]=None, target: typing.Optional[str]=None) -> None:
        """Properties for defining a ``AWS::ApiGatewayV2::Route``.

        :param api_id: ``AWS::ApiGatewayV2::Route.ApiId``.
        :param route_key: ``AWS::ApiGatewayV2::Route.RouteKey``.
        :param api_key_required: ``AWS::ApiGatewayV2::Route.ApiKeyRequired``.
        :param authorization_scopes: ``AWS::ApiGatewayV2::Route.AuthorizationScopes``.
        :param authorization_type: ``AWS::ApiGatewayV2::Route.AuthorizationType``.
        :param authorizer_id: ``AWS::ApiGatewayV2::Route.AuthorizerId``.
        :param model_selection_expression: ``AWS::ApiGatewayV2::Route.ModelSelectionExpression``.
        :param operation_name: ``AWS::ApiGatewayV2::Route.OperationName``.
        :param request_models: ``AWS::ApiGatewayV2::Route.RequestModels``.
        :param request_parameters: ``AWS::ApiGatewayV2::Route.RequestParameters``.
        :param route_response_selection_expression: ``AWS::ApiGatewayV2::Route.RouteResponseSelectionExpression``.
        :param target: ``AWS::ApiGatewayV2::Route.Target``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html
        """
        self._values = {
            'api_id': api_id,
            'route_key': route_key,
        }
        if api_key_required is not None: self._values["api_key_required"] = api_key_required
        if authorization_scopes is not None: self._values["authorization_scopes"] = authorization_scopes
        if authorization_type is not None: self._values["authorization_type"] = authorization_type
        if authorizer_id is not None: self._values["authorizer_id"] = authorizer_id
        if model_selection_expression is not None: self._values["model_selection_expression"] = model_selection_expression
        if operation_name is not None: self._values["operation_name"] = operation_name
        if request_models is not None: self._values["request_models"] = request_models
        if request_parameters is not None: self._values["request_parameters"] = request_parameters
        if route_response_selection_expression is not None: self._values["route_response_selection_expression"] = route_response_selection_expression
        if target is not None: self._values["target"] = target

    @builtins.property
    def api_id(self) -> str:
        """``AWS::ApiGatewayV2::Route.ApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-apiid
        """
        return self._values.get('api_id')

    @builtins.property
    def route_key(self) -> str:
        """``AWS::ApiGatewayV2::Route.RouteKey``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-routekey
        """
        return self._values.get('route_key')

    @builtins.property
    def api_key_required(self) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
        """``AWS::ApiGatewayV2::Route.ApiKeyRequired``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-apikeyrequired
        """
        return self._values.get('api_key_required')

    @builtins.property
    def authorization_scopes(self) -> typing.Optional[typing.List[str]]:
        """``AWS::ApiGatewayV2::Route.AuthorizationScopes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-authorizationscopes
        """
        return self._values.get('authorization_scopes')

    @builtins.property
    def authorization_type(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Route.AuthorizationType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-authorizationtype
        """
        return self._values.get('authorization_type')

    @builtins.property
    def authorizer_id(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Route.AuthorizerId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-authorizerid
        """
        return self._values.get('authorizer_id')

    @builtins.property
    def model_selection_expression(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Route.ModelSelectionExpression``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-modelselectionexpression
        """
        return self._values.get('model_selection_expression')

    @builtins.property
    def operation_name(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Route.OperationName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-operationname
        """
        return self._values.get('operation_name')

    @builtins.property
    def request_models(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Route.RequestModels``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-requestmodels
        """
        return self._values.get('request_models')

    @builtins.property
    def request_parameters(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Route.RequestParameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-requestparameters
        """
        return self._values.get('request_parameters')

    @builtins.property
    def route_response_selection_expression(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Route.RouteResponseSelectionExpression``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-routeresponseselectionexpression
        """
        return self._values.get('route_response_selection_expression')

    @builtins.property
    def target(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Route.Target``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-route.html#cfn-apigatewayv2-route-target
        """
        return self._values.get('target')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnRouteProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnRouteResponse(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigatewayv2.CfnRouteResponse"):
    """A CloudFormation ``AWS::ApiGatewayV2::RouteResponse``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html
    cloudformationResource:
    :cloudformationResource:: AWS::ApiGatewayV2::RouteResponse
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, api_id: str, route_id: str, route_response_key: str, model_selection_expression: typing.Optional[str]=None, response_models: typing.Any=None, response_parameters: typing.Any=None) -> None:
        """Create a new ``AWS::ApiGatewayV2::RouteResponse``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_id: ``AWS::ApiGatewayV2::RouteResponse.ApiId``.
        :param route_id: ``AWS::ApiGatewayV2::RouteResponse.RouteId``.
        :param route_response_key: ``AWS::ApiGatewayV2::RouteResponse.RouteResponseKey``.
        :param model_selection_expression: ``AWS::ApiGatewayV2::RouteResponse.ModelSelectionExpression``.
        :param response_models: ``AWS::ApiGatewayV2::RouteResponse.ResponseModels``.
        :param response_parameters: ``AWS::ApiGatewayV2::RouteResponse.ResponseParameters``.
        """
        props = CfnRouteResponseProps(api_id=api_id, route_id=route_id, route_response_key=route_response_key, model_selection_expression=model_selection_expression, response_models=response_models, response_parameters=response_parameters)

        jsii.create(CfnRouteResponse, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnRouteResponse":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> str:
        """``AWS::ApiGatewayV2::RouteResponse.ApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html#cfn-apigatewayv2-routeresponse-apiid
        """
        return jsii.get(self, "apiId")

    @api_id.setter
    def api_id(self, value: str) -> None:
        jsii.set(self, "apiId", value)

    @builtins.property
    @jsii.member(jsii_name="responseModels")
    def response_models(self) -> typing.Any:
        """``AWS::ApiGatewayV2::RouteResponse.ResponseModels``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html#cfn-apigatewayv2-routeresponse-responsemodels
        """
        return jsii.get(self, "responseModels")

    @response_models.setter
    def response_models(self, value: typing.Any) -> None:
        jsii.set(self, "responseModels", value)

    @builtins.property
    @jsii.member(jsii_name="responseParameters")
    def response_parameters(self) -> typing.Any:
        """``AWS::ApiGatewayV2::RouteResponse.ResponseParameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html#cfn-apigatewayv2-routeresponse-responseparameters
        """
        return jsii.get(self, "responseParameters")

    @response_parameters.setter
    def response_parameters(self, value: typing.Any) -> None:
        jsii.set(self, "responseParameters", value)

    @builtins.property
    @jsii.member(jsii_name="routeId")
    def route_id(self) -> str:
        """``AWS::ApiGatewayV2::RouteResponse.RouteId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html#cfn-apigatewayv2-routeresponse-routeid
        """
        return jsii.get(self, "routeId")

    @route_id.setter
    def route_id(self, value: str) -> None:
        jsii.set(self, "routeId", value)

    @builtins.property
    @jsii.member(jsii_name="routeResponseKey")
    def route_response_key(self) -> str:
        """``AWS::ApiGatewayV2::RouteResponse.RouteResponseKey``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html#cfn-apigatewayv2-routeresponse-routeresponsekey
        """
        return jsii.get(self, "routeResponseKey")

    @route_response_key.setter
    def route_response_key(self, value: str) -> None:
        jsii.set(self, "routeResponseKey", value)

    @builtins.property
    @jsii.member(jsii_name="modelSelectionExpression")
    def model_selection_expression(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::RouteResponse.ModelSelectionExpression``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html#cfn-apigatewayv2-routeresponse-modelselectionexpression
        """
        return jsii.get(self, "modelSelectionExpression")

    @model_selection_expression.setter
    def model_selection_expression(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "modelSelectionExpression", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-apigatewayv2.CfnRouteResponse.ParameterConstraintsProperty", jsii_struct_bases=[], name_mapping={'required': 'required'})
    class ParameterConstraintsProperty():
        def __init__(self, *, required: typing.Union[bool, aws_cdk.core.IResolvable]) -> None:
            """
            :param required: ``CfnRouteResponse.ParameterConstraintsProperty.Required``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-routeresponse-parameterconstraints.html
            """
            self._values = {
                'required': required,
            }

        @builtins.property
        def required(self) -> typing.Union[bool, aws_cdk.core.IResolvable]:
            """``CfnRouteResponse.ParameterConstraintsProperty.Required``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-routeresponse-parameterconstraints.html#cfn-apigatewayv2-routeresponse-parameterconstraints-required
            """
            return self._values.get('required')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ParameterConstraintsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-apigatewayv2.CfnRouteResponseProps", jsii_struct_bases=[], name_mapping={'api_id': 'apiId', 'route_id': 'routeId', 'route_response_key': 'routeResponseKey', 'model_selection_expression': 'modelSelectionExpression', 'response_models': 'responseModels', 'response_parameters': 'responseParameters'})
class CfnRouteResponseProps():
    def __init__(self, *, api_id: str, route_id: str, route_response_key: str, model_selection_expression: typing.Optional[str]=None, response_models: typing.Any=None, response_parameters: typing.Any=None) -> None:
        """Properties for defining a ``AWS::ApiGatewayV2::RouteResponse``.

        :param api_id: ``AWS::ApiGatewayV2::RouteResponse.ApiId``.
        :param route_id: ``AWS::ApiGatewayV2::RouteResponse.RouteId``.
        :param route_response_key: ``AWS::ApiGatewayV2::RouteResponse.RouteResponseKey``.
        :param model_selection_expression: ``AWS::ApiGatewayV2::RouteResponse.ModelSelectionExpression``.
        :param response_models: ``AWS::ApiGatewayV2::RouteResponse.ResponseModels``.
        :param response_parameters: ``AWS::ApiGatewayV2::RouteResponse.ResponseParameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html
        """
        self._values = {
            'api_id': api_id,
            'route_id': route_id,
            'route_response_key': route_response_key,
        }
        if model_selection_expression is not None: self._values["model_selection_expression"] = model_selection_expression
        if response_models is not None: self._values["response_models"] = response_models
        if response_parameters is not None: self._values["response_parameters"] = response_parameters

    @builtins.property
    def api_id(self) -> str:
        """``AWS::ApiGatewayV2::RouteResponse.ApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html#cfn-apigatewayv2-routeresponse-apiid
        """
        return self._values.get('api_id')

    @builtins.property
    def route_id(self) -> str:
        """``AWS::ApiGatewayV2::RouteResponse.RouteId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html#cfn-apigatewayv2-routeresponse-routeid
        """
        return self._values.get('route_id')

    @builtins.property
    def route_response_key(self) -> str:
        """``AWS::ApiGatewayV2::RouteResponse.RouteResponseKey``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html#cfn-apigatewayv2-routeresponse-routeresponsekey
        """
        return self._values.get('route_response_key')

    @builtins.property
    def model_selection_expression(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::RouteResponse.ModelSelectionExpression``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html#cfn-apigatewayv2-routeresponse-modelselectionexpression
        """
        return self._values.get('model_selection_expression')

    @builtins.property
    def response_models(self) -> typing.Any:
        """``AWS::ApiGatewayV2::RouteResponse.ResponseModels``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html#cfn-apigatewayv2-routeresponse-responsemodels
        """
        return self._values.get('response_models')

    @builtins.property
    def response_parameters(self) -> typing.Any:
        """``AWS::ApiGatewayV2::RouteResponse.ResponseParameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-routeresponse.html#cfn-apigatewayv2-routeresponse-responseparameters
        """
        return self._values.get('response_parameters')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnRouteResponseProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnStage(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigatewayv2.CfnStage"):
    """A CloudFormation ``AWS::ApiGatewayV2::Stage``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html
    cloudformationResource:
    :cloudformationResource:: AWS::ApiGatewayV2::Stage
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, api_id: str, stage_name: str, access_log_settings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "AccessLogSettingsProperty"]]=None, auto_deploy: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]=None, client_certificate_id: typing.Optional[str]=None, default_route_settings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "RouteSettingsProperty"]]=None, deployment_id: typing.Optional[str]=None, description: typing.Optional[str]=None, route_settings: typing.Any=None, stage_variables: typing.Any=None, tags: typing.Any=None) -> None:
        """Create a new ``AWS::ApiGatewayV2::Stage``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param api_id: ``AWS::ApiGatewayV2::Stage.ApiId``.
        :param stage_name: ``AWS::ApiGatewayV2::Stage.StageName``.
        :param access_log_settings: ``AWS::ApiGatewayV2::Stage.AccessLogSettings``.
        :param auto_deploy: ``AWS::ApiGatewayV2::Stage.AutoDeploy``.
        :param client_certificate_id: ``AWS::ApiGatewayV2::Stage.ClientCertificateId``.
        :param default_route_settings: ``AWS::ApiGatewayV2::Stage.DefaultRouteSettings``.
        :param deployment_id: ``AWS::ApiGatewayV2::Stage.DeploymentId``.
        :param description: ``AWS::ApiGatewayV2::Stage.Description``.
        :param route_settings: ``AWS::ApiGatewayV2::Stage.RouteSettings``.
        :param stage_variables: ``AWS::ApiGatewayV2::Stage.StageVariables``.
        :param tags: ``AWS::ApiGatewayV2::Stage.Tags``.
        """
        props = CfnStageProps(api_id=api_id, stage_name=stage_name, access_log_settings=access_log_settings, auto_deploy=auto_deploy, client_certificate_id=client_certificate_id, default_route_settings=default_route_settings, deployment_id=deployment_id, description=description, route_settings=route_settings, stage_variables=stage_variables, tags=tags)

        jsii.create(CfnStage, self, [scope, id, props])

    @jsii.member(jsii_name="fromCloudFormation")
    @builtins.classmethod
    def from_cloud_formation(cls, scope: aws_cdk.core.Construct, id: str, resource_attributes: typing.Any, *, finder: aws_cdk.core.ICfnFinder) -> "CfnStage":
        """A factory method that creates a new instance of this class from an object containing the CloudFormation properties of this resource.

        Used in the @aws-cdk/cloudformation-include module.

        :param scope: -
        :param id: -
        :param resource_attributes: -
        :param finder: The finder interface used to resolve references across the template.

        stability
        :stability: experimental
        """
        options = aws_cdk.core.FromCloudFormationOptions(finder=finder)

        return jsii.sinvoke(cls, "fromCloudFormation", [scope, id, resource_attributes, options])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str, typing.Any]) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::ApiGatewayV2::Stage.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="apiId")
    def api_id(self) -> str:
        """``AWS::ApiGatewayV2::Stage.ApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-apiid
        """
        return jsii.get(self, "apiId")

    @api_id.setter
    def api_id(self, value: str) -> None:
        jsii.set(self, "apiId", value)

    @builtins.property
    @jsii.member(jsii_name="routeSettings")
    def route_settings(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Stage.RouteSettings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-routesettings
        """
        return jsii.get(self, "routeSettings")

    @route_settings.setter
    def route_settings(self, value: typing.Any) -> None:
        jsii.set(self, "routeSettings", value)

    @builtins.property
    @jsii.member(jsii_name="stageName")
    def stage_name(self) -> str:
        """``AWS::ApiGatewayV2::Stage.StageName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-stagename
        """
        return jsii.get(self, "stageName")

    @stage_name.setter
    def stage_name(self, value: str) -> None:
        jsii.set(self, "stageName", value)

    @builtins.property
    @jsii.member(jsii_name="stageVariables")
    def stage_variables(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Stage.StageVariables``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-stagevariables
        """
        return jsii.get(self, "stageVariables")

    @stage_variables.setter
    def stage_variables(self, value: typing.Any) -> None:
        jsii.set(self, "stageVariables", value)

    @builtins.property
    @jsii.member(jsii_name="accessLogSettings")
    def access_log_settings(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "AccessLogSettingsProperty"]]:
        """``AWS::ApiGatewayV2::Stage.AccessLogSettings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-accesslogsettings
        """
        return jsii.get(self, "accessLogSettings")

    @access_log_settings.setter
    def access_log_settings(self, value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "AccessLogSettingsProperty"]]) -> None:
        jsii.set(self, "accessLogSettings", value)

    @builtins.property
    @jsii.member(jsii_name="autoDeploy")
    def auto_deploy(self) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
        """``AWS::ApiGatewayV2::Stage.AutoDeploy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-autodeploy
        """
        return jsii.get(self, "autoDeploy")

    @auto_deploy.setter
    def auto_deploy(self, value: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]) -> None:
        jsii.set(self, "autoDeploy", value)

    @builtins.property
    @jsii.member(jsii_name="clientCertificateId")
    def client_certificate_id(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Stage.ClientCertificateId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-clientcertificateid
        """
        return jsii.get(self, "clientCertificateId")

    @client_certificate_id.setter
    def client_certificate_id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "clientCertificateId", value)

    @builtins.property
    @jsii.member(jsii_name="defaultRouteSettings")
    def default_route_settings(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "RouteSettingsProperty"]]:
        """``AWS::ApiGatewayV2::Stage.DefaultRouteSettings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-defaultroutesettings
        """
        return jsii.get(self, "defaultRouteSettings")

    @default_route_settings.setter
    def default_route_settings(self, value: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "RouteSettingsProperty"]]) -> None:
        jsii.set(self, "defaultRouteSettings", value)

    @builtins.property
    @jsii.member(jsii_name="deploymentId")
    def deployment_id(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Stage.DeploymentId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-deploymentid
        """
        return jsii.get(self, "deploymentId")

    @deployment_id.setter
    def deployment_id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "deploymentId", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Stage.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-apigatewayv2.CfnStage.AccessLogSettingsProperty", jsii_struct_bases=[], name_mapping={'destination_arn': 'destinationArn', 'format': 'format'})
    class AccessLogSettingsProperty():
        def __init__(self, *, destination_arn: typing.Optional[str]=None, format: typing.Optional[str]=None) -> None:
            """
            :param destination_arn: ``CfnStage.AccessLogSettingsProperty.DestinationArn``.
            :param format: ``CfnStage.AccessLogSettingsProperty.Format``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-accesslogsettings.html
            """
            self._values = {
            }
            if destination_arn is not None: self._values["destination_arn"] = destination_arn
            if format is not None: self._values["format"] = format

        @builtins.property
        def destination_arn(self) -> typing.Optional[str]:
            """``CfnStage.AccessLogSettingsProperty.DestinationArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-accesslogsettings.html#cfn-apigatewayv2-stage-accesslogsettings-destinationarn
            """
            return self._values.get('destination_arn')

        @builtins.property
        def format(self) -> typing.Optional[str]:
            """``CfnStage.AccessLogSettingsProperty.Format``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-accesslogsettings.html#cfn-apigatewayv2-stage-accesslogsettings-format
            """
            return self._values.get('format')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AccessLogSettingsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-apigatewayv2.CfnStage.RouteSettingsProperty", jsii_struct_bases=[], name_mapping={'data_trace_enabled': 'dataTraceEnabled', 'detailed_metrics_enabled': 'detailedMetricsEnabled', 'logging_level': 'loggingLevel', 'throttling_burst_limit': 'throttlingBurstLimit', 'throttling_rate_limit': 'throttlingRateLimit'})
    class RouteSettingsProperty():
        def __init__(self, *, data_trace_enabled: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]=None, detailed_metrics_enabled: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]=None, logging_level: typing.Optional[str]=None, throttling_burst_limit: typing.Optional[jsii.Number]=None, throttling_rate_limit: typing.Optional[jsii.Number]=None) -> None:
            """
            :param data_trace_enabled: ``CfnStage.RouteSettingsProperty.DataTraceEnabled``.
            :param detailed_metrics_enabled: ``CfnStage.RouteSettingsProperty.DetailedMetricsEnabled``.
            :param logging_level: ``CfnStage.RouteSettingsProperty.LoggingLevel``.
            :param throttling_burst_limit: ``CfnStage.RouteSettingsProperty.ThrottlingBurstLimit``.
            :param throttling_rate_limit: ``CfnStage.RouteSettingsProperty.ThrottlingRateLimit``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-routesettings.html
            """
            self._values = {
            }
            if data_trace_enabled is not None: self._values["data_trace_enabled"] = data_trace_enabled
            if detailed_metrics_enabled is not None: self._values["detailed_metrics_enabled"] = detailed_metrics_enabled
            if logging_level is not None: self._values["logging_level"] = logging_level
            if throttling_burst_limit is not None: self._values["throttling_burst_limit"] = throttling_burst_limit
            if throttling_rate_limit is not None: self._values["throttling_rate_limit"] = throttling_rate_limit

        @builtins.property
        def data_trace_enabled(self) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
            """``CfnStage.RouteSettingsProperty.DataTraceEnabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-routesettings.html#cfn-apigatewayv2-stage-routesettings-datatraceenabled
            """
            return self._values.get('data_trace_enabled')

        @builtins.property
        def detailed_metrics_enabled(self) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
            """``CfnStage.RouteSettingsProperty.DetailedMetricsEnabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-routesettings.html#cfn-apigatewayv2-stage-routesettings-detailedmetricsenabled
            """
            return self._values.get('detailed_metrics_enabled')

        @builtins.property
        def logging_level(self) -> typing.Optional[str]:
            """``CfnStage.RouteSettingsProperty.LoggingLevel``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-routesettings.html#cfn-apigatewayv2-stage-routesettings-logginglevel
            """
            return self._values.get('logging_level')

        @builtins.property
        def throttling_burst_limit(self) -> typing.Optional[jsii.Number]:
            """``CfnStage.RouteSettingsProperty.ThrottlingBurstLimit``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-routesettings.html#cfn-apigatewayv2-stage-routesettings-throttlingburstlimit
            """
            return self._values.get('throttling_burst_limit')

        @builtins.property
        def throttling_rate_limit(self) -> typing.Optional[jsii.Number]:
            """``CfnStage.RouteSettingsProperty.ThrottlingRateLimit``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-stage-routesettings.html#cfn-apigatewayv2-stage-routesettings-throttlingratelimit
            """
            return self._values.get('throttling_rate_limit')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'RouteSettingsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-apigatewayv2.CfnStageProps", jsii_struct_bases=[], name_mapping={'api_id': 'apiId', 'stage_name': 'stageName', 'access_log_settings': 'accessLogSettings', 'auto_deploy': 'autoDeploy', 'client_certificate_id': 'clientCertificateId', 'default_route_settings': 'defaultRouteSettings', 'deployment_id': 'deploymentId', 'description': 'description', 'route_settings': 'routeSettings', 'stage_variables': 'stageVariables', 'tags': 'tags'})
class CfnStageProps():
    def __init__(self, *, api_id: str, stage_name: str, access_log_settings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnStage.AccessLogSettingsProperty"]]=None, auto_deploy: typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]=None, client_certificate_id: typing.Optional[str]=None, default_route_settings: typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnStage.RouteSettingsProperty"]]=None, deployment_id: typing.Optional[str]=None, description: typing.Optional[str]=None, route_settings: typing.Any=None, stage_variables: typing.Any=None, tags: typing.Any=None) -> None:
        """Properties for defining a ``AWS::ApiGatewayV2::Stage``.

        :param api_id: ``AWS::ApiGatewayV2::Stage.ApiId``.
        :param stage_name: ``AWS::ApiGatewayV2::Stage.StageName``.
        :param access_log_settings: ``AWS::ApiGatewayV2::Stage.AccessLogSettings``.
        :param auto_deploy: ``AWS::ApiGatewayV2::Stage.AutoDeploy``.
        :param client_certificate_id: ``AWS::ApiGatewayV2::Stage.ClientCertificateId``.
        :param default_route_settings: ``AWS::ApiGatewayV2::Stage.DefaultRouteSettings``.
        :param deployment_id: ``AWS::ApiGatewayV2::Stage.DeploymentId``.
        :param description: ``AWS::ApiGatewayV2::Stage.Description``.
        :param route_settings: ``AWS::ApiGatewayV2::Stage.RouteSettings``.
        :param stage_variables: ``AWS::ApiGatewayV2::Stage.StageVariables``.
        :param tags: ``AWS::ApiGatewayV2::Stage.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html
        """
        self._values = {
            'api_id': api_id,
            'stage_name': stage_name,
        }
        if access_log_settings is not None: self._values["access_log_settings"] = access_log_settings
        if auto_deploy is not None: self._values["auto_deploy"] = auto_deploy
        if client_certificate_id is not None: self._values["client_certificate_id"] = client_certificate_id
        if default_route_settings is not None: self._values["default_route_settings"] = default_route_settings
        if deployment_id is not None: self._values["deployment_id"] = deployment_id
        if description is not None: self._values["description"] = description
        if route_settings is not None: self._values["route_settings"] = route_settings
        if stage_variables is not None: self._values["stage_variables"] = stage_variables
        if tags is not None: self._values["tags"] = tags

    @builtins.property
    def api_id(self) -> str:
        """``AWS::ApiGatewayV2::Stage.ApiId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-apiid
        """
        return self._values.get('api_id')

    @builtins.property
    def stage_name(self) -> str:
        """``AWS::ApiGatewayV2::Stage.StageName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-stagename
        """
        return self._values.get('stage_name')

    @builtins.property
    def access_log_settings(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnStage.AccessLogSettingsProperty"]]:
        """``AWS::ApiGatewayV2::Stage.AccessLogSettings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-accesslogsettings
        """
        return self._values.get('access_log_settings')

    @builtins.property
    def auto_deploy(self) -> typing.Optional[typing.Union[bool, aws_cdk.core.IResolvable]]:
        """``AWS::ApiGatewayV2::Stage.AutoDeploy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-autodeploy
        """
        return self._values.get('auto_deploy')

    @builtins.property
    def client_certificate_id(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Stage.ClientCertificateId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-clientcertificateid
        """
        return self._values.get('client_certificate_id')

    @builtins.property
    def default_route_settings(self) -> typing.Optional[typing.Union[aws_cdk.core.IResolvable, "CfnStage.RouteSettingsProperty"]]:
        """``AWS::ApiGatewayV2::Stage.DefaultRouteSettings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-defaultroutesettings
        """
        return self._values.get('default_route_settings')

    @builtins.property
    def deployment_id(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Stage.DeploymentId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-deploymentid
        """
        return self._values.get('deployment_id')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """``AWS::ApiGatewayV2::Stage.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-description
        """
        return self._values.get('description')

    @builtins.property
    def route_settings(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Stage.RouteSettings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-routesettings
        """
        return self._values.get('route_settings')

    @builtins.property
    def stage_variables(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Stage.StageVariables``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-stagevariables
        """
        return self._values.get('stage_variables')

    @builtins.property
    def tags(self) -> typing.Any:
        """``AWS::ApiGatewayV2::Stage.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigatewayv2-stage.html#cfn-apigatewayv2-stage-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnStageProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-apigatewayv2.CommonStageOptions", jsii_struct_bases=[], name_mapping={'auto_deploy': 'autoDeploy', 'stage_name': 'stageName'})
class CommonStageOptions():
    def __init__(self, *, auto_deploy: typing.Optional[bool]=None, stage_name: typing.Optional[str]=None) -> None:
        """Options required to create a new stage.

        Options that are common between HTTP and Websocket APIs.

        :param auto_deploy: Whether updates to an API automatically trigger a new deployment. Default: false
        :param stage_name: The name of the stage. See ``StageName`` class for more details. Default: '$default' the default stage of the API. This stage will have the URL at the root of the API endpoint.

        stability
        :stability: experimental
        """
        self._values = {
        }
        if auto_deploy is not None: self._values["auto_deploy"] = auto_deploy
        if stage_name is not None: self._values["stage_name"] = stage_name

    @builtins.property
    def auto_deploy(self) -> typing.Optional[bool]:
        """Whether updates to an API automatically trigger a new deployment.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('auto_deploy')

    @builtins.property
    def stage_name(self) -> typing.Optional[str]:
        """The name of the stage.

        See ``StageName`` class for more details.

        default
        :default: '$default' the default stage of the API. This stage will have the URL at the root of the API endpoint.

        stability
        :stability: experimental
        """
        return self._values.get('stage_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CommonStageOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-apigatewayv2.CorsPreflightOptions", jsii_struct_bases=[], name_mapping={'allow_credentials': 'allowCredentials', 'allow_headers': 'allowHeaders', 'allow_methods': 'allowMethods', 'allow_origins': 'allowOrigins', 'expose_headers': 'exposeHeaders', 'max_age': 'maxAge'})
class CorsPreflightOptions():
    def __init__(self, *, allow_credentials: typing.Optional[bool]=None, allow_headers: typing.Optional[typing.List[str]]=None, allow_methods: typing.Optional[typing.List["HttpMethod"]]=None, allow_origins: typing.Optional[typing.List[str]]=None, expose_headers: typing.Optional[typing.List[str]]=None, max_age: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """Options for the CORS Configuration.

        :param allow_credentials: Specifies whether credentials are included in the CORS request. Default: false
        :param allow_headers: Represents a collection of allowed headers. Default: - No Headers are allowed.
        :param allow_methods: Represents a collection of allowed HTTP methods. Default: - No Methods are allowed.
        :param allow_origins: Represents a collection of allowed origins. Default: - No Origins are allowed.
        :param expose_headers: Represents a collection of exposed headers. Default: - No Expose Headers are allowed.
        :param max_age: The duration that the browser should cache preflight request results. Default: Duration.seconds(0)

        stability
        :stability: experimental
        """
        self._values = {
        }
        if allow_credentials is not None: self._values["allow_credentials"] = allow_credentials
        if allow_headers is not None: self._values["allow_headers"] = allow_headers
        if allow_methods is not None: self._values["allow_methods"] = allow_methods
        if allow_origins is not None: self._values["allow_origins"] = allow_origins
        if expose_headers is not None: self._values["expose_headers"] = expose_headers
        if max_age is not None: self._values["max_age"] = max_age

    @builtins.property
    def allow_credentials(self) -> typing.Optional[bool]:
        """Specifies whether credentials are included in the CORS request.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('allow_credentials')

    @builtins.property
    def allow_headers(self) -> typing.Optional[typing.List[str]]:
        """Represents a collection of allowed headers.

        default
        :default: - No Headers are allowed.

        stability
        :stability: experimental
        """
        return self._values.get('allow_headers')

    @builtins.property
    def allow_methods(self) -> typing.Optional[typing.List["HttpMethod"]]:
        """Represents a collection of allowed HTTP methods.

        default
        :default: - No Methods are allowed.

        stability
        :stability: experimental
        """
        return self._values.get('allow_methods')

    @builtins.property
    def allow_origins(self) -> typing.Optional[typing.List[str]]:
        """Represents a collection of allowed origins.

        default
        :default: - No Origins are allowed.

        stability
        :stability: experimental
        """
        return self._values.get('allow_origins')

    @builtins.property
    def expose_headers(self) -> typing.Optional[typing.List[str]]:
        """Represents a collection of exposed headers.

        default
        :default: - No Expose Headers are allowed.

        stability
        :stability: experimental
        """
        return self._values.get('expose_headers')

    @builtins.property
    def max_age(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The duration that the browser should cache preflight request results.

        default
        :default: Duration.seconds(0)

        stability
        :stability: experimental
        """
        return self._values.get('max_age')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CorsPreflightOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-apigatewayv2.HttpApiProps", jsii_struct_bases=[], name_mapping={'api_name': 'apiName', 'cors_preflight': 'corsPreflight', 'create_default_stage': 'createDefaultStage', 'default_integration': 'defaultIntegration'})
class HttpApiProps():
    def __init__(self, *, api_name: typing.Optional[str]=None, cors_preflight: typing.Optional["CorsPreflightOptions"]=None, create_default_stage: typing.Optional[bool]=None, default_integration: typing.Optional["IHttpRouteIntegration"]=None) -> None:
        """Properties to initialize an instance of ``HttpApi``.

        :param api_name: Name for the HTTP API resoruce. Default: - id of the HttpApi construct.
        :param cors_preflight: Specifies a CORS configuration for an API. Default: - CORS disabled.
        :param create_default_stage: Whether a default stage and deployment should be automatically created. Default: true
        :param default_integration: An integration that will be configured on the catch-all route ($default). Default: - none

        stability
        :stability: experimental
        """
        if isinstance(cors_preflight, dict): cors_preflight = CorsPreflightOptions(**cors_preflight)
        self._values = {
        }
        if api_name is not None: self._values["api_name"] = api_name
        if cors_preflight is not None: self._values["cors_preflight"] = cors_preflight
        if create_default_stage is not None: self._values["create_default_stage"] = create_default_stage
        if default_integration is not None: self._values["default_integration"] = default_integration

    @builtins.property
    def api_name(self) -> typing.Optional[str]:
        """Name for the HTTP API resoruce.

        default
        :default: - id of the HttpApi construct.

        stability
        :stability: experimental
        """
        return self._values.get('api_name')

    @builtins.property
    def cors_preflight(self) -> typing.Optional["CorsPreflightOptions"]:
        """Specifies a CORS configuration for an API.

        default
        :default: - CORS disabled.

        see
        :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-cors.html
        stability
        :stability: experimental
        """
        return self._values.get('cors_preflight')

    @builtins.property
    def create_default_stage(self) -> typing.Optional[bool]:
        """Whether a default stage and deployment should be automatically created.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get('create_default_stage')

    @builtins.property
    def default_integration(self) -> typing.Optional["IHttpRouteIntegration"]:
        """An integration that will be configured on the catch-all route ($default).

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get('default_integration')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'HttpApiProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-apigatewayv2.HttpIntegrationProps", jsii_struct_bases=[], name_mapping={'http_api': 'httpApi', 'integration_type': 'integrationType', 'integration_uri': 'integrationUri', 'method': 'method', 'payload_format_version': 'payloadFormatVersion'})
class HttpIntegrationProps():
    def __init__(self, *, http_api: "IHttpApi", integration_type: "HttpIntegrationType", integration_uri: str, method: typing.Optional["HttpMethod"]=None, payload_format_version: typing.Optional["PayloadFormatVersion"]=None) -> None:
        """The integration properties.

        :param http_api: The HTTP API to which this integration should be bound.
        :param integration_type: Integration type.
        :param integration_uri: Integration URI. This will be the function ARN in the case of ``HttpIntegrationType.LAMBDA_PROXY``, or HTTP URL in the case of ``HttpIntegrationType.HTTP_PROXY``.
        :param method: The HTTP method to use when calling the underlying HTTP proxy. Default: - none. required if the integration type is ``HttpIntegrationType.HTTP_PROXY``.
        :param payload_format_version: The version of the payload format. Default: - defaults to latest in the case of HttpIntegrationType.LAMBDA_PROXY`, irrelevant otherwise.

        stability
        :stability: experimental
        """
        self._values = {
            'http_api': http_api,
            'integration_type': integration_type,
            'integration_uri': integration_uri,
        }
        if method is not None: self._values["method"] = method
        if payload_format_version is not None: self._values["payload_format_version"] = payload_format_version

    @builtins.property
    def http_api(self) -> "IHttpApi":
        """The HTTP API to which this integration should be bound.

        stability
        :stability: experimental
        """
        return self._values.get('http_api')

    @builtins.property
    def integration_type(self) -> "HttpIntegrationType":
        """Integration type.

        stability
        :stability: experimental
        """
        return self._values.get('integration_type')

    @builtins.property
    def integration_uri(self) -> str:
        """Integration URI.

        This will be the function ARN in the case of ``HttpIntegrationType.LAMBDA_PROXY``,
        or HTTP URL in the case of ``HttpIntegrationType.HTTP_PROXY``.

        stability
        :stability: experimental
        """
        return self._values.get('integration_uri')

    @builtins.property
    def method(self) -> typing.Optional["HttpMethod"]:
        """The HTTP method to use when calling the underlying HTTP proxy.

        default
        :default: - none. required if the integration type is ``HttpIntegrationType.HTTP_PROXY``.

        stability
        :stability: experimental
        """
        return self._values.get('method')

    @builtins.property
    def payload_format_version(self) -> typing.Optional["PayloadFormatVersion"]:
        """The version of the payload format.

        default
        :default: - defaults to latest in the case of HttpIntegrationType.LAMBDA_PROXY`, irrelevant otherwise.

        see
        :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html
        stability
        :stability: experimental
        """
        return self._values.get('payload_format_version')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'HttpIntegrationProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-apigatewayv2.HttpIntegrationType")
class HttpIntegrationType(enum.Enum):
    """Supported integration types.

    stability
    :stability: experimental
    """
    LAMBDA_PROXY = "LAMBDA_PROXY"
    """Integration type is a Lambda proxy.

    see
    :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html
    stability
    :stability: experimental
    """
    HTTP_PROXY = "HTTP_PROXY"
    """Integration type is an HTTP proxy.

    see
    :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html
    stability
    :stability: experimental
    """

@jsii.enum(jsii_type="@aws-cdk/aws-apigatewayv2.HttpMethod")
class HttpMethod(enum.Enum):
    """Supported HTTP methods.

    stability
    :stability: experimental
    """
    ANY = "ANY"
    """HTTP ANY.

    stability
    :stability: experimental
    """
    DELETE = "DELETE"
    """HTTP DELETE.

    stability
    :stability: experimental
    """
    GET = "GET"
    """HTTP GET.

    stability
    :stability: experimental
    """
    HEAD = "HEAD"
    """HTTP HEAD.

    stability
    :stability: experimental
    """
    OPTIONS = "OPTIONS"
    """HTTP OPTIONS.

    stability
    :stability: experimental
    """
    PATCH = "PATCH"
    """HTTP PATCH.

    stability
    :stability: experimental
    """
    POST = "POST"
    """HTTP POST.

    stability
    :stability: experimental
    """
    PUT = "PUT"
    """HTTP PUT.

    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-apigatewayv2.HttpProxyIntegrationProps", jsii_struct_bases=[], name_mapping={'url': 'url', 'method': 'method'})
class HttpProxyIntegrationProps():
    def __init__(self, *, url: str, method: typing.Optional["HttpMethod"]=None) -> None:
        """Properties to initialize a new ``HttpProxyIntegration``.

        :param url: The full-qualified HTTP URL for the HTTP integration.
        :param method: The HTTP method that must be used to invoke the underlying HTTP proxy. Default: HttpMethod.ANY

        stability
        :stability: experimental
        """
        self._values = {
            'url': url,
        }
        if method is not None: self._values["method"] = method

    @builtins.property
    def url(self) -> str:
        """The full-qualified HTTP URL for the HTTP integration.

        stability
        :stability: experimental
        """
        return self._values.get('url')

    @builtins.property
    def method(self) -> typing.Optional["HttpMethod"]:
        """The HTTP method that must be used to invoke the underlying HTTP proxy.

        default
        :default: HttpMethod.ANY

        stability
        :stability: experimental
        """
        return self._values.get('method')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'HttpProxyIntegrationProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-apigatewayv2.HttpRouteIntegrationConfig", jsii_struct_bases=[], name_mapping={'payload_format_version': 'payloadFormatVersion', 'type': 'type', 'uri': 'uri', 'method': 'method'})
class HttpRouteIntegrationConfig():
    def __init__(self, *, payload_format_version: "PayloadFormatVersion", type: "HttpIntegrationType", uri: str, method: typing.Optional["HttpMethod"]=None) -> None:
        """Config returned back as a result of the bind.

        :param payload_format_version: Payload format version in the case of lambda proxy integration. Default: - undefined
        :param type: Integration type.
        :param uri: Integration URI.
        :param method: The HTTP method that must be used to invoke the underlying proxy. Required for ``HttpIntegrationType.HTTP_PROXY`` Default: - undefined

        stability
        :stability: experimental
        """
        self._values = {
            'payload_format_version': payload_format_version,
            'type': type,
            'uri': uri,
        }
        if method is not None: self._values["method"] = method

    @builtins.property
    def payload_format_version(self) -> "PayloadFormatVersion":
        """Payload format version in the case of lambda proxy integration.

        default
        :default: - undefined

        see
        :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html
        stability
        :stability: experimental
        """
        return self._values.get('payload_format_version')

    @builtins.property
    def type(self) -> "HttpIntegrationType":
        """Integration type.

        stability
        :stability: experimental
        """
        return self._values.get('type')

    @builtins.property
    def uri(self) -> str:
        """Integration URI.

        stability
        :stability: experimental
        """
        return self._values.get('uri')

    @builtins.property
    def method(self) -> typing.Optional["HttpMethod"]:
        """The HTTP method that must be used to invoke the underlying proxy.

        Required for ``HttpIntegrationType.HTTP_PROXY``

        default
        :default: - undefined

        stability
        :stability: experimental
        """
        return self._values.get('method')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'HttpRouteIntegrationConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class HttpRouteKey(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigatewayv2.HttpRouteKey"):
    """HTTP route in APIGateway is a combination of the HTTP method and the path component.

    This class models that combination.

    stability
    :stability: experimental
    """
    @jsii.member(jsii_name="with")
    @builtins.classmethod
    def with_(cls, path: str, method: typing.Optional["HttpMethod"]=None) -> "HttpRouteKey":
        """Create a route key with the combination of the path and the method.

        :param path: -
        :param method: default is 'ANY'.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "with", [path, method])

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT")
    def DEFAULT(cls) -> "HttpRouteKey":
        """The catch-all route of the API, i.e., when no other routes match.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "DEFAULT")

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> str:
        """The key to the RouteKey as recognized by APIGateway.

        stability
        :stability: experimental
        """
        return jsii.get(self, "key")

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> typing.Optional[str]:
        """The path part of this RouteKey.

        Returns ``undefined`` when ``RouteKey.DEFAULT`` is used.

        stability
        :stability: experimental
        """
        return jsii.get(self, "path")


@jsii.data_type(jsii_type="@aws-cdk/aws-apigatewayv2.HttpRouteProps", jsii_struct_bases=[BatchHttpRouteOptions], name_mapping={'integration': 'integration', 'http_api': 'httpApi', 'route_key': 'routeKey'})
class HttpRouteProps(BatchHttpRouteOptions):
    def __init__(self, *, integration: "IHttpRouteIntegration", http_api: "IHttpApi", route_key: "HttpRouteKey") -> None:
        """Properties to initialize a new Route.

        :param integration: The integration to be configured on this route.
        :param http_api: the API the route is associated with.
        :param route_key: The key to this route. This is a combination of an HTTP method and an HTTP path.

        stability
        :stability: experimental
        """
        self._values = {
            'integration': integration,
            'http_api': http_api,
            'route_key': route_key,
        }

    @builtins.property
    def integration(self) -> "IHttpRouteIntegration":
        """The integration to be configured on this route.

        stability
        :stability: experimental
        """
        return self._values.get('integration')

    @builtins.property
    def http_api(self) -> "IHttpApi":
        """the API the route is associated with.

        stability
        :stability: experimental
        """
        return self._values.get('http_api')

    @builtins.property
    def route_key(self) -> "HttpRouteKey":
        """The key to this route.

        This is a combination of an HTTP method and an HTTP path.

        stability
        :stability: experimental
        """
        return self._values.get('route_key')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'HttpRouteProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-apigatewayv2.HttpStageOptions", jsii_struct_bases=[CommonStageOptions], name_mapping={'auto_deploy': 'autoDeploy', 'stage_name': 'stageName'})
class HttpStageOptions(CommonStageOptions):
    def __init__(self, *, auto_deploy: typing.Optional[bool]=None, stage_name: typing.Optional[str]=None) -> None:
        """Options to create a new stage for an HTTP API.

        :param auto_deploy: Whether updates to an API automatically trigger a new deployment. Default: false
        :param stage_name: The name of the stage. See ``StageName`` class for more details. Default: '$default' the default stage of the API. This stage will have the URL at the root of the API endpoint.

        stability
        :stability: experimental
        """
        self._values = {
        }
        if auto_deploy is not None: self._values["auto_deploy"] = auto_deploy
        if stage_name is not None: self._values["stage_name"] = stage_name

    @builtins.property
    def auto_deploy(self) -> typing.Optional[bool]:
        """Whether updates to an API automatically trigger a new deployment.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('auto_deploy')

    @builtins.property
    def stage_name(self) -> typing.Optional[str]:
        """The name of the stage.

        See ``StageName`` class for more details.

        default
        :default: '$default' the default stage of the API. This stage will have the URL at the root of the API endpoint.

        stability
        :stability: experimental
        """
        return self._values.get('stage_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'HttpStageOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-apigatewayv2.HttpStageProps", jsii_struct_bases=[HttpStageOptions], name_mapping={'auto_deploy': 'autoDeploy', 'stage_name': 'stageName', 'http_api': 'httpApi'})
class HttpStageProps(HttpStageOptions):
    def __init__(self, *, auto_deploy: typing.Optional[bool]=None, stage_name: typing.Optional[str]=None, http_api: "IHttpApi") -> None:
        """Properties to initialize an instance of ``HttpStage``.

        :param auto_deploy: Whether updates to an API automatically trigger a new deployment. Default: false
        :param stage_name: The name of the stage. See ``StageName`` class for more details. Default: '$default' the default stage of the API. This stage will have the URL at the root of the API endpoint.
        :param http_api: The HTTP API to which this stage is associated.

        stability
        :stability: experimental
        """
        self._values = {
            'http_api': http_api,
        }
        if auto_deploy is not None: self._values["auto_deploy"] = auto_deploy
        if stage_name is not None: self._values["stage_name"] = stage_name

    @builtins.property
    def auto_deploy(self) -> typing.Optional[bool]:
        """Whether updates to an API automatically trigger a new deployment.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('auto_deploy')

    @builtins.property
    def stage_name(self) -> typing.Optional[str]:
        """The name of the stage.

        See ``StageName`` class for more details.

        default
        :default: '$default' the default stage of the API. This stage will have the URL at the root of the API endpoint.

        stability
        :stability: experimental
        """
        return self._values.get('stage_name')

    @builtins.property
    def http_api(self) -> "IHttpApi":
        """The HTTP API to which this stage is associated.

        stability
        :stability: experimental
        """
        return self._values.get('http_api')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'HttpStageProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.interface(jsii_type="@aws-cdk/aws-apigatewayv2.IHttpApi")
class IHttpApi(aws_cdk.core.IResource, jsii.compat.Protocol):
    """Represents an HTTP API.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IHttpApiProxy

    @builtins.property
    @jsii.member(jsii_name="httpApiId")
    def http_api_id(self) -> str:
        """The identifier of this API Gateway HTTP API.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...


class _IHttpApiProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    """Represents an HTTP API.

    stability
    :stability: experimental
    """
    __jsii_type__ = "@aws-cdk/aws-apigatewayv2.IHttpApi"
    @builtins.property
    @jsii.member(jsii_name="httpApiId")
    def http_api_id(self) -> str:
        """The identifier of this API Gateway HTTP API.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "httpApiId")


@jsii.interface(jsii_type="@aws-cdk/aws-apigatewayv2.IHttpRouteIntegration")
class IHttpRouteIntegration(jsii.compat.Protocol):
    """The interface that various route integration classes will inherit.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IHttpRouteIntegrationProxy

    @jsii.member(jsii_name="bind")
    def bind(self, route: "IHttpRoute") -> "HttpRouteIntegrationConfig":
        """Bind this integration to the route.

        :param route: -

        stability
        :stability: experimental
        """
        ...


class _IHttpRouteIntegrationProxy():
    """The interface that various route integration classes will inherit.

    stability
    :stability: experimental
    """
    __jsii_type__ = "@aws-cdk/aws-apigatewayv2.IHttpRouteIntegration"
    @jsii.member(jsii_name="bind")
    def bind(self, route: "IHttpRoute") -> "HttpRouteIntegrationConfig":
        """Bind this integration to the route.

        :param route: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [route])


@jsii.interface(jsii_type="@aws-cdk/aws-apigatewayv2.IIntegration")
class IIntegration(aws_cdk.core.IResource, jsii.compat.Protocol):
    """Represents an integration to an API Route.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IIntegrationProxy

    @builtins.property
    @jsii.member(jsii_name="integrationId")
    def integration_id(self) -> str:
        """Id of the integration.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...


class _IIntegrationProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    """Represents an integration to an API Route.

    stability
    :stability: experimental
    """
    __jsii_type__ = "@aws-cdk/aws-apigatewayv2.IIntegration"
    @builtins.property
    @jsii.member(jsii_name="integrationId")
    def integration_id(self) -> str:
        """Id of the integration.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "integrationId")


@jsii.interface(jsii_type="@aws-cdk/aws-apigatewayv2.IRoute")
class IRoute(aws_cdk.core.IResource, jsii.compat.Protocol):
    """Represents a route.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IRouteProxy

    @builtins.property
    @jsii.member(jsii_name="routeId")
    def route_id(self) -> str:
        """Id of the Route.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...


class _IRouteProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    """Represents a route.

    stability
    :stability: experimental
    """
    __jsii_type__ = "@aws-cdk/aws-apigatewayv2.IRoute"
    @builtins.property
    @jsii.member(jsii_name="routeId")
    def route_id(self) -> str:
        """Id of the Route.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "routeId")


@jsii.interface(jsii_type="@aws-cdk/aws-apigatewayv2.IStage")
class IStage(aws_cdk.core.IResource, jsii.compat.Protocol):
    """Represents a Stage.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IStageProxy

    @builtins.property
    @jsii.member(jsii_name="stageName")
    def stage_name(self) -> str:
        """The name of the stage;

        its primary identifier.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...


class _IStageProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    """Represents a Stage.

    stability
    :stability: experimental
    """
    __jsii_type__ = "@aws-cdk/aws-apigatewayv2.IStage"
    @builtins.property
    @jsii.member(jsii_name="stageName")
    def stage_name(self) -> str:
        """The name of the stage;

        its primary identifier.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "stageName")


@jsii.implements(IHttpRouteIntegration)
class LambdaProxyIntegration(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigatewayv2.LambdaProxyIntegration"):
    """The Lambda Proxy integration resource for HTTP API.

    stability
    :stability: experimental
    """
    def __init__(self, *, handler: aws_cdk.aws_lambda.IFunction, payload_format_version: typing.Optional["PayloadFormatVersion"]=None) -> None:
        """
        :param handler: The handler for this integration.
        :param payload_format_version: Version of the payload sent to the lambda handler. Default: PayloadFormatVersion.VERSION_2_0

        stability
        :stability: experimental
        """
        props = LambdaProxyIntegrationProps(handler=handler, payload_format_version=payload_format_version)

        jsii.create(LambdaProxyIntegration, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, route: "IHttpRoute") -> "HttpRouteIntegrationConfig":
        """Bind this integration to the route.

        :param route: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [route])


@jsii.data_type(jsii_type="@aws-cdk/aws-apigatewayv2.LambdaProxyIntegrationProps", jsii_struct_bases=[], name_mapping={'handler': 'handler', 'payload_format_version': 'payloadFormatVersion'})
class LambdaProxyIntegrationProps():
    def __init__(self, *, handler: aws_cdk.aws_lambda.IFunction, payload_format_version: typing.Optional["PayloadFormatVersion"]=None) -> None:
        """Lambda Proxy integration properties.

        :param handler: The handler for this integration.
        :param payload_format_version: Version of the payload sent to the lambda handler. Default: PayloadFormatVersion.VERSION_2_0

        stability
        :stability: experimental
        """
        self._values = {
            'handler': handler,
        }
        if payload_format_version is not None: self._values["payload_format_version"] = payload_format_version

    @builtins.property
    def handler(self) -> aws_cdk.aws_lambda.IFunction:
        """The handler for this integration.

        stability
        :stability: experimental
        """
        return self._values.get('handler')

    @builtins.property
    def payload_format_version(self) -> typing.Optional["PayloadFormatVersion"]:
        """Version of the payload sent to the lambda handler.

        default
        :default: PayloadFormatVersion.VERSION_2_0

        see
        :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html
        stability
        :stability: experimental
        """
        return self._values.get('payload_format_version')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LambdaProxyIntegrationProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class PayloadFormatVersion(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigatewayv2.PayloadFormatVersion"):
    """Payload format version for lambda proxy integration.

    see
    :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html
    stability
    :stability: experimental
    """
    @jsii.member(jsii_name="custom")
    @builtins.classmethod
    def custom(cls, version: str) -> "PayloadFormatVersion":
        """A custom payload version.

        Typically used if there is a version number that the CDK doesn't support yet

        :param version: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "custom", [version])

    @jsii.python.classproperty
    @jsii.member(jsii_name="VERSION_1_0")
    def VERSION_1_0(cls) -> "PayloadFormatVersion":
        """Version 1.0.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VERSION_1_0")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VERSION_2_0")
    def VERSION_2_0(cls) -> "PayloadFormatVersion":
        """Version 2.0.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VERSION_2_0")

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> str:
        """version as a string.

        stability
        :stability: experimental
        """
        return jsii.get(self, "version")


@jsii.data_type(jsii_type="@aws-cdk/aws-apigatewayv2.AddRoutesOptions", jsii_struct_bases=[BatchHttpRouteOptions], name_mapping={'integration': 'integration', 'path': 'path', 'methods': 'methods'})
class AddRoutesOptions(BatchHttpRouteOptions):
    def __init__(self, *, integration: "IHttpRouteIntegration", path: str, methods: typing.Optional[typing.List["HttpMethod"]]=None) -> None:
        """Options for the Route with Integration resoruce.

        :param integration: The integration to be configured on this route.
        :param path: The path at which all of these routes are configured.
        :param methods: The HTTP methods to be configured. Default: HttpMethod.ANY

        stability
        :stability: experimental
        """
        self._values = {
            'integration': integration,
            'path': path,
        }
        if methods is not None: self._values["methods"] = methods

    @builtins.property
    def integration(self) -> "IHttpRouteIntegration":
        """The integration to be configured on this route.

        stability
        :stability: experimental
        """
        return self._values.get('integration')

    @builtins.property
    def path(self) -> str:
        """The path at which all of these routes are configured.

        stability
        :stability: experimental
        """
        return self._values.get('path')

    @builtins.property
    def methods(self) -> typing.Optional[typing.List["HttpMethod"]]:
        """The HTTP methods to be configured.

        default
        :default: HttpMethod.ANY

        stability
        :stability: experimental
        """
        return self._values.get('methods')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AddRoutesOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(IHttpApi)
class HttpApi(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigatewayv2.HttpApi"):
    """Create a new API Gateway HTTP API endpoint.

    stability
    :stability: experimental
    resource:
    :resource:: AWS::ApiGatewayV2::Api
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, api_name: typing.Optional[str]=None, cors_preflight: typing.Optional["CorsPreflightOptions"]=None, create_default_stage: typing.Optional[bool]=None, default_integration: typing.Optional["IHttpRouteIntegration"]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param api_name: Name for the HTTP API resoruce. Default: - id of the HttpApi construct.
        :param cors_preflight: Specifies a CORS configuration for an API. Default: - CORS disabled.
        :param create_default_stage: Whether a default stage and deployment should be automatically created. Default: true
        :param default_integration: An integration that will be configured on the catch-all route ($default). Default: - none

        stability
        :stability: experimental
        """
        props = HttpApiProps(api_name=api_name, cors_preflight=cors_preflight, create_default_stage=create_default_stage, default_integration=default_integration)

        jsii.create(HttpApi, self, [scope, id, props])

    @jsii.member(jsii_name="fromApiId")
    @builtins.classmethod
    def from_api_id(cls, scope: aws_cdk.core.Construct, id: str, http_api_id: str) -> "IHttpApi":
        """Import an existing HTTP API into this CDK app.

        :param scope: -
        :param id: -
        :param http_api_id: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromApiId", [scope, id, http_api_id])

    @jsii.member(jsii_name="addRoutes")
    def add_routes(self, *, path: str, methods: typing.Optional[typing.List["HttpMethod"]]=None, integration: "IHttpRouteIntegration") -> typing.List["HttpRoute"]:
        """Add multiple routes that uses the same configuration.

        The routes all go to the same path, but for different
        methods.

        :param path: The path at which all of these routes are configured.
        :param methods: The HTTP methods to be configured. Default: HttpMethod.ANY
        :param integration: The integration to be configured on this route.

        stability
        :stability: experimental
        """
        options = AddRoutesOptions(path=path, methods=methods, integration=integration)

        return jsii.invoke(self, "addRoutes", [options])

    @jsii.member(jsii_name="addStage")
    def add_stage(self, id: str, *, auto_deploy: typing.Optional[bool]=None, stage_name: typing.Optional[str]=None) -> "HttpStage":
        """Add a new stage.

        :param id: -
        :param auto_deploy: Whether updates to an API automatically trigger a new deployment. Default: false
        :param stage_name: The name of the stage. See ``StageName`` class for more details. Default: '$default' the default stage of the API. This stage will have the URL at the root of the API endpoint.

        stability
        :stability: experimental
        """
        options = HttpStageOptions(auto_deploy=auto_deploy, stage_name=stage_name)

        return jsii.invoke(self, "addStage", [id, options])

    @builtins.property
    @jsii.member(jsii_name="httpApiId")
    def http_api_id(self) -> str:
        """The identifier of this API Gateway HTTP API.

        stability
        :stability: experimental
        """
        return jsii.get(self, "httpApiId")

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> typing.Optional[str]:
        """Get the URL to the default stage of this API.

        Returns ``undefined`` if ``createDefaultStage`` is unset.

        stability
        :stability: experimental
        """
        return jsii.get(self, "url")


@jsii.implements(IHttpRouteIntegration)
class HttpProxyIntegration(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigatewayv2.HttpProxyIntegration"):
    """The HTTP Proxy integration resource for HTTP API.

    stability
    :stability: experimental
    """
    def __init__(self, *, url: str, method: typing.Optional["HttpMethod"]=None) -> None:
        """
        :param url: The full-qualified HTTP URL for the HTTP integration.
        :param method: The HTTP method that must be used to invoke the underlying HTTP proxy. Default: HttpMethod.ANY

        stability
        :stability: experimental
        """
        props = HttpProxyIntegrationProps(url=url, method=method)

        jsii.create(HttpProxyIntegration, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _: "IHttpRoute") -> "HttpRouteIntegrationConfig":
        """Bind this integration to the route.

        :param _: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_])


@jsii.implements(IStage)
class HttpStage(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigatewayv2.HttpStage"):
    """Represents a stage where an instance of the API is deployed.

    stability
    :stability: experimental
    resource:
    :resource:: AWS::ApiGatewayV2::Stage
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, http_api: "IHttpApi", auto_deploy: typing.Optional[bool]=None, stage_name: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param http_api: The HTTP API to which this stage is associated.
        :param auto_deploy: Whether updates to an API automatically trigger a new deployment. Default: false
        :param stage_name: The name of the stage. See ``StageName`` class for more details. Default: '$default' the default stage of the API. This stage will have the URL at the root of the API endpoint.

        stability
        :stability: experimental
        """
        props = HttpStageProps(http_api=http_api, auto_deploy=auto_deploy, stage_name=stage_name)

        jsii.create(HttpStage, self, [scope, id, props])

    @jsii.member(jsii_name="fromStageName")
    @builtins.classmethod
    def from_stage_name(cls, scope: aws_cdk.core.Construct, id: str, stage_name: str) -> "IStage":
        """Import an existing stage into this CDK app.

        :param scope: -
        :param id: -
        :param stage_name: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromStageName", [scope, id, stage_name])

    @builtins.property
    @jsii.member(jsii_name="stageName")
    def stage_name(self) -> str:
        """The name of the stage;

        its primary identifier.

        stability
        :stability: experimental
        """
        return jsii.get(self, "stageName")

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> str:
        """The URL to this stage.

        stability
        :stability: experimental
        """
        return jsii.get(self, "url")


@jsii.interface(jsii_type="@aws-cdk/aws-apigatewayv2.IHttpIntegration")
class IHttpIntegration(IIntegration, jsii.compat.Protocol):
    """Represents an Integration for an HTTP API.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IHttpIntegrationProxy

    @builtins.property
    @jsii.member(jsii_name="httpApi")
    def http_api(self) -> "IHttpApi":
        """The HTTP API associated with this integration.

        stability
        :stability: experimental
        """
        ...


class _IHttpIntegrationProxy(jsii.proxy_for(IIntegration)):
    """Represents an Integration for an HTTP API.

    stability
    :stability: experimental
    """
    __jsii_type__ = "@aws-cdk/aws-apigatewayv2.IHttpIntegration"
    @builtins.property
    @jsii.member(jsii_name="httpApi")
    def http_api(self) -> "IHttpApi":
        """The HTTP API associated with this integration.

        stability
        :stability: experimental
        """
        return jsii.get(self, "httpApi")


@jsii.interface(jsii_type="@aws-cdk/aws-apigatewayv2.IHttpRoute")
class IHttpRoute(IRoute, jsii.compat.Protocol):
    """Represents a Route for an HTTP API.

    stability
    :stability: experimental
    """
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IHttpRouteProxy

    @builtins.property
    @jsii.member(jsii_name="httpApi")
    def http_api(self) -> "IHttpApi":
        """The HTTP API associated with this route.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> typing.Optional[str]:
        """Returns the path component of this HTTP route, ``undefined`` if the path is the catch-all route.

        stability
        :stability: experimental
        """
        ...


class _IHttpRouteProxy(jsii.proxy_for(IRoute)):
    """Represents a Route for an HTTP API.

    stability
    :stability: experimental
    """
    __jsii_type__ = "@aws-cdk/aws-apigatewayv2.IHttpRoute"
    @builtins.property
    @jsii.member(jsii_name="httpApi")
    def http_api(self) -> "IHttpApi":
        """The HTTP API associated with this route.

        stability
        :stability: experimental
        """
        return jsii.get(self, "httpApi")

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> typing.Optional[str]:
        """Returns the path component of this HTTP route, ``undefined`` if the path is the catch-all route.

        stability
        :stability: experimental
        """
        return jsii.get(self, "path")


@jsii.implements(IHttpIntegration)
class HttpIntegration(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigatewayv2.HttpIntegration"):
    """The integration for an API route.

    stability
    :stability: experimental
    resource:
    :resource:: AWS::ApiGatewayV2::Integration
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, http_api: "IHttpApi", integration_type: "HttpIntegrationType", integration_uri: str, method: typing.Optional["HttpMethod"]=None, payload_format_version: typing.Optional["PayloadFormatVersion"]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param http_api: The HTTP API to which this integration should be bound.
        :param integration_type: Integration type.
        :param integration_uri: Integration URI. This will be the function ARN in the case of ``HttpIntegrationType.LAMBDA_PROXY``, or HTTP URL in the case of ``HttpIntegrationType.HTTP_PROXY``.
        :param method: The HTTP method to use when calling the underlying HTTP proxy. Default: - none. required if the integration type is ``HttpIntegrationType.HTTP_PROXY``.
        :param payload_format_version: The version of the payload format. Default: - defaults to latest in the case of HttpIntegrationType.LAMBDA_PROXY`, irrelevant otherwise.

        stability
        :stability: experimental
        """
        props = HttpIntegrationProps(http_api=http_api, integration_type=integration_type, integration_uri=integration_uri, method=method, payload_format_version=payload_format_version)

        jsii.create(HttpIntegration, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="httpApi")
    def http_api(self) -> "IHttpApi":
        """The HTTP API associated with this integration.

        stability
        :stability: experimental
        """
        return jsii.get(self, "httpApi")

    @builtins.property
    @jsii.member(jsii_name="integrationId")
    def integration_id(self) -> str:
        """Id of the integration.

        stability
        :stability: experimental
        """
        return jsii.get(self, "integrationId")


@jsii.implements(IHttpRoute)
class HttpRoute(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-apigatewayv2.HttpRoute"):
    """Route class that creates the Route for API Gateway HTTP API.

    stability
    :stability: experimental
    resource:
    :resource:: AWS::ApiGatewayV2::Route
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, http_api: "IHttpApi", route_key: "HttpRouteKey", integration: "IHttpRouteIntegration") -> None:
        """
        :param scope: -
        :param id: -
        :param http_api: the API the route is associated with.
        :param route_key: The key to this route. This is a combination of an HTTP method and an HTTP path.
        :param integration: The integration to be configured on this route.

        stability
        :stability: experimental
        """
        props = HttpRouteProps(http_api=http_api, route_key=route_key, integration=integration)

        jsii.create(HttpRoute, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="httpApi")
    def http_api(self) -> "IHttpApi":
        """The HTTP API associated with this route.

        stability
        :stability: experimental
        """
        return jsii.get(self, "httpApi")

    @builtins.property
    @jsii.member(jsii_name="routeId")
    def route_id(self) -> str:
        """Id of the Route.

        stability
        :stability: experimental
        """
        return jsii.get(self, "routeId")

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> typing.Optional[str]:
        """Returns the path component of this HTTP route, ``undefined`` if the path is the catch-all route.

        stability
        :stability: experimental
        """
        return jsii.get(self, "path")


__all__ = [
    "AddRoutesOptions",
    "BatchHttpRouteOptions",
    "CfnApi",
    "CfnApiMapping",
    "CfnApiMappingProps",
    "CfnApiProps",
    "CfnAuthorizer",
    "CfnAuthorizerProps",
    "CfnDeployment",
    "CfnDeploymentProps",
    "CfnDomainName",
    "CfnDomainNameProps",
    "CfnIntegration",
    "CfnIntegrationProps",
    "CfnIntegrationResponse",
    "CfnIntegrationResponseProps",
    "CfnModel",
    "CfnModelProps",
    "CfnRoute",
    "CfnRouteProps",
    "CfnRouteResponse",
    "CfnRouteResponseProps",
    "CfnStage",
    "CfnStageProps",
    "CommonStageOptions",
    "CorsPreflightOptions",
    "HttpApi",
    "HttpApiProps",
    "HttpIntegration",
    "HttpIntegrationProps",
    "HttpIntegrationType",
    "HttpMethod",
    "HttpProxyIntegration",
    "HttpProxyIntegrationProps",
    "HttpRoute",
    "HttpRouteIntegrationConfig",
    "HttpRouteKey",
    "HttpRouteProps",
    "HttpStage",
    "HttpStageOptions",
    "HttpStageProps",
    "IHttpApi",
    "IHttpIntegration",
    "IHttpRoute",
    "IHttpRouteIntegration",
    "IIntegration",
    "IRoute",
    "IStage",
    "LambdaProxyIntegration",
    "LambdaProxyIntegrationProps",
    "PayloadFormatVersion",
]

publication.publish()
