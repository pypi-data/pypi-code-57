"""
Event conversion utils
"""
from urllib import parse

import re

from wavelength_test.integration.util.mock_constants import (
    MOCK_TOKEN, STANDARD_AUTHORIZER_CONTEXT)

EXPECTED_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Credentials": "true"
}
ALLOW_ORIGIN_OPEN_FIT_REGEX = r'.*wavelengthdev.biz'  # TODO make config
VERB_GET = 'get'
VERB_DELETE = 'delete'
VERB_POST = 'post'
VERB_PUT = 'put'
VERB_PATCH = 'patch'
VERB_INVOKE = 'invoke'

VERBS = [VERB_GET, VERB_DELETE, VERB_POST, VERB_PUT, VERB_PATCH, VERB_INVOKE]


def event_to_request_url(base_path, event):
    """
    Returns path from received event
    :param base_path:
    :param event:
    :return: path
    """

    path = base_path
    path_parameters = event.get('pathParameters')
    querystring_parameters = event.get('queryStringParameters')

    if path_parameters:
        for path_parameter in path_parameters:
            path = path.replace('{' + path_parameter + '}',
                                path_parameters.get(path_parameter))

    if querystring_parameters:
        path += '?' + parse.urlencode(querystring_parameters)

    return path


def event_to_body(event):
    """
    Gets the body from the event
    :param event:
    :return: body
    """

    body = event.get('body')
    return body


def update_request_event(event, cognito_id_token):
    """
    Updates an request event to have the request context populated with an authorization
    """
    if cognito_id_token == MOCK_TOKEN:
        # This a local call, update the event for the lambda
        if 'requestContext' not in event:
            # This mocks up the request to look like the authorizer has decomposed the id token
            event.update(STANDARD_AUTHORIZER_CONTEXT)
        elif 'authorizer' not in event['requestContext']:
            event['requestContext']['authorizer'] = STANDARD_AUTHORIZER_CONTEXT['requestContext']['authorizer']
        if 'headers' not in event:
            event['headers'] = {}
        if not event['headers'].get('Authorization'):
            event['headers']['Authorization'] = cognito_id_token

    return event


def event_to_request_headers(event, content_type, api_key, cognito_id_token):
    """
    Gets the headers from the event
    :param event:
    :param content_type:
    :param api_key:
    :param cognito_id_token: cognito jwt ('IdToken' not 'AccessToken')
    :return: headers
    """

    headers = event.get('headers', {})
    if 'Content-Type' not in headers:
        headers['Content-Type'] = content_type
    if 'x-api-key' not in headers:
        headers['x-api-key'] = api_key
    if 'Authorization' not in headers:
        headers['Authorization'] = cognito_id_token
    return headers


def check_headers(headers):
    """
    Checks for Access-Control headers
    :param headers:
    :return:
    """
    if headers:
        for expected_header_key in EXPECTED_HEADERS:
            returned_header = headers.get(expected_header_key)
            header = str(returned_header).lower()
            if header != EXPECTED_HEADERS.get(expected_header_key):
                if expected_header_key == 'Access-Control-Allow-Origin' and \
                        re.match(ALLOW_ORIGIN_OPEN_FIT_REGEX, header):
                    continue
                else:
                    raise Exception(
                        "Response does not contain expected CORS headers")
