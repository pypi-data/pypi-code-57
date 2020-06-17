import json
from dataclasses import is_dataclass
import textwrap
from os import environ
import requests
import os
from .mapping import *
from enum import Enum
from .mapping_inputs import ARK_NAAN

__all__ = ['get_by_id', 'create_ark', 'update_ark', 'search_arks']

graphql_endpoint = {
    'dev': 'https://m752xzraej.execute-api.us-east-2.amazonaws.com/dev/graphql',
    'prod': 'https://o56dder9y3.execute-api.us-east-2.amazonaws.com/prod/graphql',
    'sandbox': 'http://0.0.0.0:5000/graphql',
}


def _indent(s):
    return textwrap.indent(s, '    ')


def __graphql_get_by_id(ark):
    """
    Produces GQL query for getting ARK by ID
    """
    return f"""
        query {{
              getARK(ark: "{ark}") {{
                ...arkFields
              }}
            }}
    {get_fragments()}
    """


def __graphql_authenticate(login, password):
    """
    Produces GQL query for basic auth
    """
    return f"""
       query {{
          authenticate(login: "{login}", password: "{password}") {{
            status
            errorMessage
            accessToken
          }}
        }}
    """


def __graphql_mutation(mutation_name, input_name, input):
    """
    Produces GQL Mutation for updating ARK
    """
    query = f"""
        mutation {{
          {mutation_name} (
            {input_name}: {{
                {__generate_gql_input(input)}
            }}
          ) 
          {{ 
            ark {{
                ...arkFields
            }}
          }}
    }}
    {get_fragments()}
    """
    return query


def __run_gql_query(query, access_token=None, attachments=None):
    """
    Runs query and return results.
    If attachments are specified, they are sent as binaries.
    """
    headers = {'Authorization': access_token} if access_token else None
    if attachments:
        files_map = {}
        for i, path in enumerate(attachments):
            filename, file_ext = os.path.splitext(path)
            files_map[f'attachment_{i}{file_ext}'] = open(path, 'rb')
        resp = requests.post(graphql_endpoint[environ['Environment']], data={'query': query},
                             files=files_map, headers=headers)
    else:
        resp = requests.post(graphql_endpoint[environ['Environment']], data={'query': query},
                             headers=headers)

    if resp.status_code != 200:
        message = f'Query failed with status code {resp.status_code}.'
        raise Exception(message)

    data = json.loads(resp.text)

    if 'errors' in data:
        message = f"Query returned errors {data['errors']}."
        raise Exception(message)

    return data


def __generate_gql_input(input_val):
    output = ''

    for key, val in input_val.__dict__.items():
        if val:
            output += '\n'

            output += f'{key}: '
            if is_dataclass(val):
                output += f'{{ {__generate_gql_input(val)} }}'
            elif isinstance(val, list):
                output += '['
                for i in val:
                    if is_dataclass(i):
                        output += f'{{ {__generate_gql_input(i)} }}'
                    else:
                        output += json.dumps(i)
                output += ']'
            elif isinstance(val, Enum):
                output += val.name
            else:
                output += json.dumps(val)

    return _indent(output)


def create_ark(ark_input, access_token):
    """
    Create new ARK record
    :param ark_input: CreateARKInput input object (see mapping_inputs.py)
    :return: newly created record
    """

    errors = ark_input.validate()
    if errors:
        raise Exception('Error in ARK input: {0}'.format(', '.join(errors)))

    if not access_token:
        raise Exception('Access Token is required')

    query = __graphql_mutation('createARK', 'arkInput', ark_input)
    data = __run_gql_query(query, access_token=access_token)
    return data['data']['createARK']['ark']


def update_ark(ark_input, access_token):
    """
    Update ARK record
    :param ark_input: UpdateARKInput object (see mapping_inputs.py)
    :return: updated ARK record
    """

    errors = ark_input.validate()
    if errors:
        raise Exception('Error in ARK input: {0}'.format(', '.join(errors)))

    # Remove prefix before generating query
    ark_input.ark = ark_input.ark.replace('ark:', '')

    query = __graphql_mutation('updateARK', 'arkInput', ark_input)
    data = __run_gql_query(query, access_token=access_token)
    return data['data']['updateARK']['ark']


def get_by_id(ark: str):
    """
    Returns all fields of ARK.
    """
    prefix = 'ark:' + ARK_NAAN + '/'
    if not ark.startswith(prefix) or not ark.replace(prefix, '').isalnum():
        raise Exception('Invalid ark format. Must be ark:45488/abcdef')

    # Remove prefix before generating query
    ark = ark.replace('ark:', '')

    data = __run_gql_query(__graphql_get_by_id(ark))
    return data['data']['getARK']


def authenticate_basic(login, password):
    """
    Authenticates user by login and password. Returns object: {status, accessToken, errorMessage}
    """
    if not login or not  password:
        raise Exception('Login and password required')

    query = __graphql_authenticate(login, password)
    data = __run_gql_query(query)
    return data['data']['authenticate']