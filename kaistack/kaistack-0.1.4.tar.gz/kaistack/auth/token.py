import json
import os
import time

import click
from auth0.v3.authentication import GetToken

from kaistack.auth.exceptions import NoAuthContextException
from kaistack.config.context import load_context

_TOKEN_CACHE_FILE = '~/.kaistack/authtoken'


def load_from_cache():
    cache_file = os.path.expanduser(_TOKEN_CACHE_FILE)
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            token = f.read()
            result = json.loads(token)
            expires_in = result['expires_in']
            modify_time = os.path.getmtime(cache_file)
            # Keep 60 seconds buffer
            if (modify_time + expires_in - 60) > time.time():
                # Cached token hasn't expired
                return result, True
            else:
                # Token has expired
                return None, False
    return None, False


def save_to_cache(cred):
    cred = json.dumps(cred)
    with open(os.path.expanduser(_TOKEN_CACHE_FILE), 'w') as f:
        f.write(cred)


def get_access_token():
    '''Get access token'''
    token, is_cache_available = load_from_cache()
    if is_cache_available:
        return token
    ctx = load_context()
    auth0_domain = os.environ.get("AUTH_DOMAIN")
    if auth0_domain is None:
        auth0_domain = ctx.get('domain')

    non_interactive_client_id = os.environ.get("AUTH_CLIENT_ID")
    if non_interactive_client_id is None:
        non_interactive_client_id = ctx.get('client_id')

    non_interactive_client_secret = os.environ.get("AUTH_CLIENT_SECRET")
    if non_interactive_client_secret is None:
        non_interactive_client_secret = ctx.get('client_secret')

    auth_endpoint = os.environ.get("AUTH_ENDPOINT")
    if auth_endpoint is None:
        auth_endpoint = ctx.get('endpoint')

    if auth0_domain is None or non_interactive_client_id is None or non_interactive_client_secret is None or auth_endpoint is None:
        raise NoAuthContextException()
    get_token = GetToken(auth0_domain)
    cred = get_token.client_credentials(non_interactive_client_id,
                                        non_interactive_client_secret, auth_endpoint)
    save_to_cache(cred)
    return cred


@click.command(name="get-token")
def get_token():
    click.echo(get_access_token())
