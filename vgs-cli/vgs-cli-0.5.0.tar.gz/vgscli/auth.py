from vgscli.auth_server import AuthServer
from vgscli.keyring_token_util import KeyringTokenUtil

token_util = KeyringTokenUtil()
TOKEN_FILE_NAME = 'vgs_token'


def handshake(environment):
    try:
        auth_server = AuthServer(environment)
        token_util.validate_refresh_token()
        if not token_util.validate_access_token():
            auth_server.refresh_authentication()
    except Exception as e:
        raise AuthenticateException("Authentication error occurred:" + e.args[0])


def login(environment):
    try:
        auth_server = AuthServer(environment)
        return auth_server.authenticate(environment)
    except Exception as e:
        raise AuthenticateException("Authentication error occurred:" + e.args[0])


def logout():
    token_util.clear_tokens()
    token_util.remove_encryption_secret()


class AuthenticateException(Exception):
    def __init__(self, arg):
        self.message = arg
