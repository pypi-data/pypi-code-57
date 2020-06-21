# pylint: disable=W0212
# pylint: disable=C0103
# pylint: disable=W0603
# pylint: disable=C0411
from http.client import responses

import requests

from wavelength_test.integration.util.event_to_request import (VERB_GET,
                                                        VERB_POST, VERB_PUT,
                                                        VERB_PATCH, VERB_DELETE)
from wavelength_test.integration.util.event_to_request import (update_request_event,
                                                        check_headers, VERB_INVOKE)
from wavelength_test.integration.util.invoker_base import RESPONSE_CONVERTERS, try_json
from wavelength_test.integration.util.mock_constants import (MOCK_TOKEN,
                                                      MOCK_ACCOUNT_ID)


class InvokerResponseLocal:
    """
    InvokerResponse for integration tests against local
    """

    def __init__(self, httpResponse):
        """
        InvokerResponseLocal init, sets various attributes as follows:
        """
        self.response = httpResponse

        body = self.response['body']
        content_type = self.response['headers'].get('Content-Type', 'undefined')
        # Default to try_json otherwise we could break many tests since most responses aren't
        # returning Content-Type header from the lib's get_standard_response (but they should -BM)
        converter = RESPONSE_CONVERTERS.get(content_type, try_json)

        self.response_body = converter(body)
        self.header = self.response['headers']
        self.status_code = self.response['statusCode']

    def __getitem__(self, key):
        """
        This method ensures that the pre-existing contract stays working.
        it overwrites the bracket syntax.
        """
        return self.response_body[key]


class InvokerLocal:
    """
    Invoker for local integration testing
    """

    def __init__(self, local_invoke_mapper, ctx):
        """
        Initializes InvokerLocal
        :param local_invoke_mapper:
        """
        self._ctx = ctx
        self._local_invoke_mapper = local_invoke_mapper
        self._cognito_id_token = MOCK_TOKEN

    @staticmethod
    def get_decrypted_cognito_profile_id(profile_num=1):
        """
        Gets the cognito Account ID
        """
        return f'{MOCK_ACCOUNT_ID}-{profile_num}'

    def get_cognito_id_token(self, entitlements: [str]):
        """
        Gets the cognito JWT, ignores entitlements for now
        """
        return self._cognito_id_token

    def get(self, event, resource, **kwargs):
        """
        Get request
        """
        event = update_request_event(event, self._cognito_id_token)
        result = self._local_invoke_mapper[resource][VERB_GET](
            event, self._ctx)
        return self._process_response(result, **kwargs)

    def delete(self, event, resource, **kwargs):
        """
        Delete request
        """
        event = update_request_event(event, self._cognito_id_token)
        result = self._local_invoke_mapper[resource][VERB_DELETE](
            event, self._ctx)
        return self._process_response(result, **kwargs)

    def post(self, event, resource, **kwargs):
        """
        Post request
        """
        event = update_request_event(event, self._cognito_id_token)
        result = self._local_invoke_mapper[resource][VERB_POST](
            event, self._ctx)
        return self._process_response(result, **kwargs)

    def put(self, event, resource, **kwargs):
        """
        Put request
        """
        event = update_request_event(event, self._cognito_id_token)
        result = self._local_invoke_mapper[resource][VERB_PUT](
            event, self._ctx)
        return self._process_response(result, **kwargs)

    def patch(self, event, resource, **kwargs):
        """
        Put request
        """
        event = update_request_event(event, self._cognito_id_token)
        result = self._local_invoke_mapper[resource][VERB_PATCH](
            event, self._ctx)
        return self._process_response(result, **kwargs)

    def invoke(self, event):
        """
        Direct Lambda invocation
        """
        return self._local_invoke_mapper['default'][VERB_INVOKE](event, self._ctx)

    @classmethod
    def _process_response(cls, response, **kwargs):
        """
        Process the response (get, delete, post, put, etc)
        :param response:
        :return:
        """
        if not response:
            return response
        if response['statusCode'] in range(200, 499):
            check_headers(response['headers'])
            if response['statusCode'] in range(200, 399):
                return InvokerResponseLocal(response)
        response_model = requests.models.Response()
        response_model.code = responses.get(response['statusCode'])
        response_model.error_type = "HTTP Exception"
        response_model.status_code = response['statusCode']
        response_model._content = response['body'].encode()
        raise requests.exceptions.HTTPError(
            'LocalInvoker HTTP Error', response=response_model)
