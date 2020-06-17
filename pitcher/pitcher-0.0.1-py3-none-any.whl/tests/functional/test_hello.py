import pytest
import json
import logging
import os
from typing import Any, Mapping

from pitcher import Application, Request, Route
from pitcher.middleware import AllowedHostMiddleware, CORSMiddleware, Middleware


@pytest.mark.parametrize(
    "input,hosts,status,cors_options,headers",
    [
        (
            "world",
            ["api.example.com"],
            200,
            {
                "allow_origins": ["example.com"],
                "allow_methods": ["GET", "POST", "PUT"],
                "allow_credentials": True,
            },
            {
                "Access-Control-Allow-Origin": "example.com",
                "Access-Control-Allow-Methods": "GET, POST, PUT",
                "Access-Control-Allow-Credentials": "true",
                "content-type": "application/json",
                "Vary": "Origin",
            },
        ),
        (
            "example",
            ["*.example.com"],
            200,
            {
                "allow_origins": ["api.example.com", "example.org", "example.com",],
                "allow_headers": ["authorization", "content-type"],
                "allow_methods": ["GET"],
            },
            {
                "Access-Control-Allow-Origin": "example.com",
                "Access-Control-Allow-Methods": "GET",
                # "Access-Control-Allow-Headers": "authorization, content-type",
                "content-type": "application/json",
                "Vary": "Origin",
            },
        ),
        (
            "everyone",
            ["*"],
            200,
            {"allow_origins": ["*"], "allow_headers": ["*"]},
            {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET",
                "content-type": "application/json",
            },
        ),
        (
            "fail",
            ["*.example.org"],
            400,
            {"allow_origins": ["*"], "allow_headers": ["*"]},
            {"content-type": "text/plain"},
        ),
    ],
)
def test_hello(input, hosts, status, cors_options, headers, lambda_context):
    def hello_world(request: Request, app) -> dict:
        name = request.params["name"]
        app.logger.info("hello {}", name)
        data = {"message": f"hello {name}"}
        return data

    def configure_logs(event: Mapping[str, Any], context: Any, app: Application):
        logging.basicConfig(level=os.getenv("LOG_LEVEL", logging.INFO))

    app = Application(
        name="hello",
        routes=[Route("/hello/{name}", hello_world)],
        middleware=[
            Middleware(AllowedHostMiddleware, allowed_hosts=hosts),
            Middleware(CORSMiddleware, **cors_options),
        ],
        logger=logging.getLogger(),
        on_invocation=[configure_logs],
    )

    event = {
        "path": f"/hello/{input}",
        "headers": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, lzma, sdch, br",
            "Accept-Language": "en-US,en;q=0.8",
            "CloudFront-Forwarded-Proto": "https",
            "CloudFront-Is-Desktop-Viewer": "true",
            "CloudFront-Is-Mobile-Viewer": "false",
            "CloudFront-Is-SmartTV-Viewer": "false",
            "CloudFront-Is-Tablet-Viewer": "false",
            "CloudFront-Viewer-Country": "US",
            "Host": "api.example.com",
            "Origin": "example.com",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36 OPR/39.0.2256.48",
            "Via": "1.1 fb7cca60f0ecd82ce07790c9c5eef16c.cloudfront.net (CloudFront)",
            "X-Amz-Cf-Id": "nBsWBOrSHMgnaROZJK1wGCZ9PcRcSpq_oSXZNQwQ10OTZL4cimZo3g==",
            "X-Forwarded-For": "192.168.100.1, 192.168.1.1",
            "X-Forwarded-Port": "443",
            "X-Forwarded-Proto": "https",
        },
        "pathParameters": {"name": input},
        "requestContext": {
            "accountId": "123456789012",
            "resourceId": "us4z18",
            "stage": "test",
            "requestId": "41b45ea3-70b5-11e6-b7bd-69b5aaebc7d9",
            "identity": {
                "cognitoIdentityPoolId": "",
                "accountId": "",
                "cognitoIdentityId": "",
                "caller": "",
                "apiKey": "",
                "sourceIp": "192.168.100.1",
                "cognitoAuthenticationType": "",
                "cognitoAuthenticationProvider": "",
                "userArn": "",
                "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36 OPR/39.0.2256.48",
                "user": "",
            },
            "resourcePath": "/hello/{name}",
            "httpMethod": "GET",
            "apiId": "wt6mne2s9k",
        },
        "resource": "/hello/{name}",
        "httpMethod": "GET",
        "stageVariables": {"stageVarName": "stageVarValue"},
    }

    response = app(event, lambda_context)

    assert response["statusCode"] == status
    assert response["headers"] == headers

    if response["headers"]["content-type"] == "application/json":
        json_body = json.loads(response["body"])
        assert json_body["message"] == f"hello {input}"
