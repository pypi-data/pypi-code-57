import argparse
import secrets
import time
from typing import List

import requests
from yaspin import yaspin

import devyzer
from devyzer.constants import AUTH_UI_ENDPOINT, AUTHORIZED_EXPIRY, AUTH_CREATE_ENDPOINT, \
    AUTH_ENDPOINT
from devyzer.utils.cli import print_with_color, bcolors, open_url


# noinspection PyProtectedMember
def subparser(
        subparsers: argparse._SubParsersAction, parents: List[argparse.ArgumentParser]
):
    auth_parser = subparsers.add_parser(
        "auth",
        parents=parents,
        conflict_handler="resolve",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        help="Starts the terminal.",
    )

    auth_parser.add_argument('-F', '--force',
                             action='store_true',
                             help='Force authenticate if a local token exists')

    auth_parser.set_defaults(func=auth)


def request_auth_token():
    cli_token = secrets.token_hex(16)

    # issue cli token in gateway
    issue_token_response = requests.post(AUTH_CREATE_ENDPOINT,
                                         headers={'Content-Type': 'application/json'},
                                         json={"cliToken": cli_token})

    if issue_token_response.status_code > 201:
        print_with_color("Failed to issue a cli token. please check your internet connection", bcolors.FAIL)
        return None

    print_with_color(f'Auth URL : {AUTH_UI_ENDPOINT(cli_token)} ', bcolors.OKGREEN)
    open_url(AUTH_UI_ENDPOINT(cli_token))

    t_end = time.time() + 60 * AUTHORIZED_EXPIRY
    with yaspin(text="Authenticating ...", color="green") as spinner:
        while time.time() < t_end:
            time.sleep(2)

            get_token_response = requests.post(AUTH_ENDPOINT(cli_token),
                                               headers={'Content-Type': 'application/json'},
                                               json={"cliToken": cli_token})

            if 300 > get_token_response.status_code >= 200:
                result = get_token_response.json()
                if "token" in result and result["token"]:
                    spinner.ok("✔")
                    return result["token"]
        spinner.fail("✘")
        print_with_color("Failed to Authenticate, Timeout ", bcolors.WARNING)
        return None


def store_auth_token(token):
    """
    store console token
    :param token:console token
    """
    devyzer.config['auth']['token'] = token
    devyzer.config.write()


def get_auth_token():
    """
    get console token
    :return: console token or None
    """
    try:
        return devyzer.config['auth']['token']
    except:
        return None


def auth(args: argparse.Namespace = None, force=False):
    """
    check user token stored or not
    :return:False or  user token
    """

    local_token = get_auth_token()
    token = local_token
    if token is None or not token or force or (args and args.force):
        token = request_auth_token()

    store_auth_token(token)

    return token is not None


