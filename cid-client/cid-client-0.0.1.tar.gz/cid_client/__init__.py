import json
from dataclasses import is_dataclass
import textwrap
from os import environ
import requests
import os
from .mapping import *
from enum import Enum

__all__ = [
    'assign_identifier',
    'authenticate_basic',
    'create_cid',
    'find_by_artifact',
    'get_by_id',
    'get_cid_children',
    'get_cid_siblings',
    'update_cid',
    'remove_identifier',
]

graphql_endpoint = {
    'dev': 'https://m752xzraej.execute-api.us-east-2.amazonaws.com/dev/graphql',
    'prod': 'https://o56dder9y3.execute-api.us-east-2.amazonaws.com/prod/graphql',
    'sandbox': 'http://0.0.0.0:5000/graphql',
}


def _indent(s):
    return textwrap.indent(s, '    ')


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


def __graphql_find_by_artifact(artifact):
    """
    Produces GQL query for getting CID by artifact
    """
    return f"""
       query {{
          findByArtifact(artifact: "{artifact}") {{
            total
            results
          }}
        }}
    """

def __graphql_get_by_id(cid):
    """
    Produces GQL query for getting CID by ID
    """
    return f"""
        query {{
              getCID(cid: "{cid}") {{
                ...cidFields
              }}
            }}
    {get_fragments()}
    """


def __graphql_get_cid_children(cid, size=10):
    """
    Produces GQL query for getting the children of a CID
    """
    return f"""
       query {{
          searchCIDChildren(cid: "{cid}", size: {size}) {{
            total
            results
          }}
        }}
    """


def __graphql_get_cid_siblings(cid, size=10):
    """
    Produces GQL query for getting the siblings of a CID
    """
    return f"""
       query {{
          searchCIDSiblings(cid: "{cid}", size: {size}) {{
            total
            results
          }}
        }}
    """


def __graphql_mutation(mutation_name, input_name, input):
    """
    Produces GQL Mutation for updating CID
    """
    query = f"""
        mutation {{
          {mutation_name} (
            {input_name}: {{
                {__generate_gql_input(input)}
            }}
          ) 
          {{ 
            cid {{
                ...cidFields
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
        raise Exception(f'Query failed with status code {resp.status_code}.')

    data = json.loads(resp.text)

    if 'errors' in data:
        raise Exception(f"Query returned errors {data['errors']}.")

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


def authenticate_basic(login, password):
    """
    Authenticates user by login and password. Returns object: {status, accessToken, errorMessage}
    """
    if not login or not  password:
        raise Exception('Login and password required')

    query = __graphql_authenticate(login, password)
    data = __run_gql_query(query)
    return data['data']['authenticate']


def assign_identifier(assign_id_input, access_token):
    """
    Assign a related CID, DOI, ARK or MARC identifier.
    Data is pulled from corresponding sources and saved as CID event.
    :param assign_id_input: AssignIdentifierInput object (see mapping_inputs.py)
    :return: updated CID record
    """
    errors = assign_id_input.validate()
    if errors:
        raise Exception('Error in Assign ID input: {0}'.format(', '.join(errors)))

    query = __graphql_mutation('assignIdentifier', 'assignIdInput', assign_id_input)

    data = __run_gql_query(query, access_token=access_token)
    return data['data']['assignIdentifier']['cid']


def create_cid(cid_input, access_token):
    """
    Create new CID record
    :param cid_input: CreateCIDInput input object (see mapping_inputs.py)
    :return: newly created record
    """
    errors = cid_input.validate()
    if errors:
        raise Exception('Error in CID input: {0}'.format(', '.join(errors)))

    if not access_token:
        raise Exception('Access Token is required')

    query = __graphql_mutation('createCID', 'cidInput', cid_input)
    data = __run_gql_query(query, access_token=access_token)
    return data['data']['createCID']['cid']


def find_by_artifact(artifact: str):
    """
    Returns cids by artifact link
    :param artifact: link to artifact
    """
    data = __run_gql_query(__graphql_find_by_artifact(artifact))
    return data['data']['findByArtifact']


def get_by_id(cid: str):
    """
    Returns all fields of CID.
    """
    data = __run_gql_query(__graphql_get_by_id(cid))
    return data['data']['getCID']


def get_cid_children(cid: str, size: int = 10):
    """
    Returns cids which have the provided CID as a PARENT.
    :param cid: CID to obtain child list for
    :param size: Max number of CIDs to return.  Defaults to 10
    """
    data = __run_gql_query(__graphql_get_cid_children(cid, size))
    return data['data']['searchCIDChildren']


def get_cid_siblings(cid: str, size: int = 10):
    """
    Returns cids which have the same PARENT or WHERE.url of the provided CID.
    :param cid: CID to obtain sibling list for
    :param size: Max number of CIDs to return. Defaults to 10
    """
    data = __run_gql_query(__graphql_get_cid_siblings(cid, size))
    return data['data']['searchCIDSiblings']


def remove_identifier(remove_id_input, access_token):
    """
    Remove a related CID, DOI, ARK or MARC identifier.
    :param remove_id_input: RemoveIdentifierInput object (see mapping_inputs.py)
    :return: updated CID record
    """
    errors = remove_id_input.validate()
    if errors:
        raise Exception('Error in Remove ID input: {0}'.format(', '.join(errors)))

    query = __graphql_mutation('removeIdentifier', 'removeIdInput', remove_id_input)

    data = __run_gql_query(query, access_token=access_token)
    return data['data']['removeIdentifier']['cid']


def update_cid(cid_input, access_token):
    """
    Update CID record
    :param cid_input: UpdateCIDInput object (see mapping_inputs.py)
    :return: updated CID record
    """
    errors = cid_input.validate()
    if errors:
        raise Exception('Error in CID input: {0}'.format(', '.join(errors)))

    query = __graphql_mutation('updateCID', 'cidInput', cid_input)
    data = __run_gql_query(query, access_token=access_token)
    return data['data']['updateCID']['cid']
