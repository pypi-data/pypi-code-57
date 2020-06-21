# pylint: disable=C0103
import base64
import json
import os

import boto3
import requests

from wavelength_test.integration.util.aws_utils import get_api_key, get_cognito_id_token
from wavelength_test.integration.util.event_to_request import (check_headers,
                                                        VERB_GET,
                                                        VERB_POST, VERB_PUT,
                                                        VERB_PATCH, VERB_DELETE)
from wavelength_test.integration.util.invoker_base import RESPONSE_CONVERTERS, try_json
from wavelength_test.integration.util.event_to_request import event_to_request_url, event_to_request_headers, event_to_body

ENDPOINT_TYPE_LAMBDA = 'lambda'
ENDPOINT_TYPE_GATEWAY = 'apigateway'


class InvokerResponseAWS:
    """
    InvokerResponse for integration tests against AWS
    """

    def __init__(self, httpResponse):
        """
        InovkerAWS init, sets various attributes as follows:
        """
        self.response = httpResponse

        content_type = self.response.headers.get('Content-Type', 'undefined')
        converter = RESPONSE_CONVERTERS.get(content_type, try_json)

        self.response_body = converter(self.response.text)
        self.header = self.response.headers
        self.status_code = self.response.status_code

    def __getitem__(self, key):
        """
        This method ensures that the pre-existing contract stays working.
        it overwrites the bracket syntax.
        """
        return self.response_body[key]


class InvokerAWS:
    """
    Invoker for integration tests against AWS
    """
    _cognito_id_token_val = None

    def __init__(self, service_name, stage, api_version, **kwargs):
        """
        InvokerAWS init
        :param service_name:
        :param stage:
        :param api_version:
        :param endpoint_type: [lambda,apigateway]
        :param resource: path in addition to an expected base
        """
        self._service_name = service_name
        self._stage = stage
        self._api_version = api_version
        self._region = os.environ.get('region', 'us-east-1')
        self._ssm_client = boto3.client('ssm', self._region)
        self._gateway_client = boto3.client('apigateway', self._region)
        self._api_key = get_api_key(
            service_name, self._ssm_client, self._gateway_client)
        self._endpoint_type = kwargs.get('endpoint_type')
        self._resource = kwargs.get('resource')

        if self._resource:
            param_name = (
                f'/{self._endpoint_type}/{self._stage}/{service_name}/v{self._api_version}/{self._resource}')
        else:
            param_name = (
                f'/{self._endpoint_type}/{self._stage}/{service_name}/v{self._api_version}')
        response = self._ssm_client.get_parameter(Name=param_name)
        self._request_url = response['Parameter']['Value']

    def get_decrypted_cognito_profile_id(self, profile_num=1):
        """
        Decodes the cognito JWT, gets the IDToken at [1], and adds '-1' to the end
        :return: decrypted JWT IDToken with '-{profile_num}' on the end
        """
        tokens = self._cognito_id_token.split('.')
        decoded_token = json.loads(base64.b64decode(tokens[1]).decode('utf-8'))
        sub_from_token = decoded_token['sub'] + f'-{profile_num}'
        return sub_from_token

    def get_cognito_id_token(self):
        """
        Gets the cognito JWT
        """
        return self._cognito_id_token

    @property
    def _cognito_id_token(self):
        return None
        # TODO - use JWT service
        if not type(self)._cognito_id_token_val:
            type(self)._cognito_id_token_val = get_cognito_id_token(self._service_name,
                                                                    self._region,
                                                                    self._ssm_client)
        return type(self)._cognito_id_token_val

    def _get_url(self, resource):
        """
        Get request url
        :param resource:
        :return:
        """
        paths = self._request_url.split('/')
        if resource and resource != 'default' and resource not in paths:
            url = self._request_url + '/' + resource
        else:
            url = self._request_url
        return url

    def get(self, event, resource, **kwargs):
        """
        Get
        :param event:
        :param resource:
        :return:
        """
        url = self._get_url(resource)
        if self._endpoint_type == ENDPOINT_TYPE_LAMBDA:
            raise Exception(
                'Bad invocation type change invoker type to apigateway')
        return self._invoke_api(VERB_GET, url, self._api_key, event, **kwargs)

    def delete(self, event, resource, **kwargs):
        """
        Delete
        :param event:
        :param resource:
        :return:
        """
        url = self._get_url(resource)
        if self._endpoint_type == ENDPOINT_TYPE_LAMBDA:
            raise Exception(
                'Bad invocation type change invoker type to apigateway')
        return self._invoke_api(VERB_DELETE, url, self._api_key, event, **kwargs)

    def post(self, event, resource, **kwargs):
        """
        Post
        :param event:
        :param resource:
        :return:
        """
        url = self._get_url(resource)
        if self._endpoint_type == ENDPOINT_TYPE_LAMBDA:
            raise Exception(
                'Bad invocation type change invoker type to apigateway')
        return self._invoke_api(VERB_POST, url, self._api_key, event, **kwargs)

    def put(self, event, resource, **kwargs):
        """
        Put
        :param event:
        :param resource:
        :return:
        """
        url = self._get_url(resource)
        if self._endpoint_type == ENDPOINT_TYPE_LAMBDA:
            raise Exception(
                'Bad invocation type change invoker type to apigateway')
        return self._invoke_api(VERB_PUT, url, self._api_key, event, **kwargs)

    def patch(self, event, resource, **kwargs):
        """
        Put
        :param event:
        :param resource:
        :return:
        """
        url = self._get_url(resource)
        if self._endpoint_type == ENDPOINT_TYPE_LAMBDA:
            raise Exception(
                'Bad invocation type change invoker type to apigateway')
        return self._invoke_api(VERB_PATCH, url, self._api_key, event, **kwargs)

    def invoke(self, event):
        """
        Direct Lambda invocation
        """
        if self._endpoint_type == ENDPOINT_TYPE_GATEWAY:
            raise Exception(
                'Bad invocation type change invoker type to lambda')
        return self._invoke_lambda(self._request_url, event)

    def _invoke_api(self, verb, url, apikey, event, **kwargs):
        """
        Invokes API
        :param verb:
        :param url:
        :param apikey:
        :param event:
        :param content_type:
        :return: response
        """
        content_type = kwargs.get('content_type', 'application/json')
        request_url = event_to_request_url(url, event)
        body = event_to_body(event)
        should_redirect = kwargs.get('allow_redirect', True)
        if body:
            response = getattr(requests, verb)(request_url,
                                               headers=event_to_request_headers(event,
                                                                                content_type,
                                                                                apikey,
                                                                                self._cognito_id_token),
                                               json=body, allow_redirects=should_redirect)
        else:
            response = getattr(requests, verb)(request_url,
                                               headers=event_to_request_headers(event,
                                                                                content_type,
                                                                                apikey,
                                                                                self._cognito_id_token),
                                               allow_redirects=should_redirect)

        if response.status_code in range(200, 499) and not response.status_code == 400:
            # API Gateway does not return CORS headers on validation failure
            check_headers(response.headers)
        response.raise_for_status()
        return InvokerResponseAWS(response)

    @classmethod
    def _invoke_lambda(cls, arn, event):
        """
        Direct Lambda invocation
        :param arn:
        :param event:
        :return: payload
        """
        lambda_client = boto3.client(ENDPOINT_TYPE_LAMBDA)
        res = lambda_client.invoke(
            FunctionName=arn,
            InvocationType='RequestResponse',
            Payload=json.dumps(event),
        )
        return json.loads(res['Payload'].read().decode("utf-8"))
