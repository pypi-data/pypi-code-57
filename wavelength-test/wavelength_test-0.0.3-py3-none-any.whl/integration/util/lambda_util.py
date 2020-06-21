# pylint: disable=C0103

import os

from botocore.exceptions import ClientError
from typing import List

from wavelength_test.integration.util.event_to_request import VERBS
from wavelength_test.integration.util.lambda_invoker_aws import InvokerAWS
from wavelength_test.integration.util.lambda_invoker_local import InvokerLocal

EXPECTED_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Credentials": "true"
}
SERVERLESS = None


class ServerlessYMLInjector:
    """
    Used to inject the serverless.yml file into this file for the Invoker __init__'s service_name attribute
    !Important: the serverless.yml file must be opened and injected BEFORE using the Invoker.
    This should be done in the setUp() of the subclassed integration_test_base.py in each project as follows:
    with open('./serverless.yml', "r") as f:
        serverless_yaml = yaml.load(f)
    ServerlessYMLInjector(serverless_yaml)
    """

    def __init__(self, serverless_yaml):
        global SERVERLESS  # pylint: disable=global-statement
        SERVERLESS = serverless_yaml


class Context:
    """
    Creates Mock Context object
    """

    def __init__(self):
        self.function_name = 'stage-func_name'
        self.aws_request_id = 'test'
        self.invoked_function_arn = 'test_url'


class LocalInvokeMapper:
    """
    Mapper for Local Invoker
    """

    def __init__(self, verb, func, resource=None):
        if verb.lower() not in VERBS:
            raise Exception('Invalid verb must be one of {}'.format(VERBS))
        self._resource = resource
        self._func = func
        self._verb = verb.lower()

    def get_resource(self):
        """
        Gets resource
        """
        return self._resource

    def get_verb(self):
        """
        Gets verb
        """
        return self._verb

    def get_function(self):
        """
        Gets function
        """
        return self._func


class Invoker:
    """
    Invoker determines which resources to use if local or AWS
    """

    def __init__(self, mappers: List[LocalInvokeMapper], endpoint_type='apigateway', resource=None):
        """
        Create an invoker per endpoint

        service name - this project is stdemo
        mappers - map an optional resource (multiple endpoint paths) and verbs to a local 'lambda' function
        endpoint_type - is the method to call api gateway or lambda
        resource - optional extra path parameter for when reading ssm parameters for endpoints off of the base
        """
        if SERVERLESS is not None:
            self._service_name = SERVERLESS['custom']['service_name']
        else:
            raise Exception(
                'You must inject serverless.yml file using ServerlessYMLInjector before using the Invoker')

        self._stage = os.environ.get('stageName')
        self._api_version = os.environ.get('api_version', 1)
        self._endpoint_type = endpoint_type
        self._local_invoke_mapper = dict()
        for mapper in mappers:
            self._local_invoke_mapper.setdefault(mapper.get_resource() if mapper.get_resource(
            ) else 'default', {}).update({mapper.get_verb(): mapper.get_function()})
        try:
            self.invoker = InvokerAWS(self._service_name,
                                      self._stage,
                                      self._api_version,
                                      endpoint_type=self._endpoint_type,
                                      resource=resource) \
                if self._stage else InvokerLocal(self._local_invoke_mapper, Context())
        except ClientError as error:
            boto_error = _get_boto3_error(error)
            if boto_error.get('aws', {}).get('code', '') == 'ParameterNotFound':
                raise Exception(
                    f'One or more SSM parameters are missing for stage {self._stage}') from error
            if 'The security token included in the request is expired' in boto_error.get('message', ''):
                raise Exception(f'Failed to execute AWS operation, your session has expired, '
                                'please use get keys to refresh your session') from error
            raise error

    def is_local(self):
        """
        Checks if stage exists
        """
        return not self._stage

    def get_decrypted_cognito_profile_id(self, profile_num=1):
        """
        Gets the cognito Account ID
        """
        return self.invoker.get_decrypted_cognito_profile_id(profile_num)

    def get_cognito_id_token(self):
        """
        Gets the cognito JWT
        """
        return self.invoker.get_cognito_id_token()

    def delete(self, event, resource='default', **kwargs):
        """
        Delete request
        """
        return self.invoker.delete(event, resource, **kwargs)

    def get(self, event, resource='default', **kwargs):
        """
        Get request
        """
        return self.invoker.get(event, resource, **kwargs)

    def post(self, event, resource='default', **kwargs):
        """
        Post request
        """
        return self.invoker.post(event, resource, **kwargs)

    def put(self, event, resource='default', **kwargs):
        """
        Put request
        """
        return self.invoker.put(event, resource, **kwargs)

    def patch(self, event, resource='default', **kwargs):
        """
        Patch request
        """
        return self.invoker.patch(event, resource, **kwargs)

    def invoke(self, event):
        """
        Direct Lambda invocation
        """
        return self.invoker.invoke(event)


def _get_boto3_error(error):
    """
    must be an instance of botocore.exceptions ClientError.
    """
    aws = {}
    message = ''

    # boto3 response
    if hasattr(error, 'response'):
        meta = error.response.get('ResponseMetadata')
        if meta:
            aws['status'] = meta['HTTPStatusCode']
        error = error.response.get('Error')
        if error:
            aws['code'] = error['Code']
            aws['message'] = error['Message']

    if hasattr(error, 'operation_name'):
        aws['op'] = error.operation_name

    if hasattr(error, 'message') or hasattr(error, 'Message'):
        message = error.message
    elif aws.get('message') or aws.get('Message'):
        message = aws['message']

    return {'message': message, 'aws': aws}
