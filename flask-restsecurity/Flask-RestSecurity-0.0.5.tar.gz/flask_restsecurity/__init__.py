from flask import Response, current_app, request
from enum import Enum, auto

# Enums
class AuthenticationType(Enum):
    BASIC = 'basic'

class Environment(Enum):
    RESTFULL_BASIC_AUTORIZATION = auto()
    RESTFULL_AUTHENTICATION_REALM = auto()

# Main
class Security(object):
    def __init__(self, app=None):
        if app is not None:
            self.app = app
            self.init_app(app)
        else:
            self.app = None

    def init_app(self, app):
        app.config.setdefault(Environment.RESTFULL_AUTHENTICATION_REALM.value, '')

        @app.before_request
        def require_basic_auth():
            auth = Authentication()
            if not auth.valid():
                return self.challenge()

    def challenge(self):
        realm = current_app.config[Environment.RESTFULL_AUTHENTICATION_REALM.value]
        return Response(
            status=401,
            headers={'WWW-Authenticate': 'Basic realm="%s"' % realm}
        )

class AuthenticationException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class Authentication:
    def __init__(self):
        self.type = None

        basic_auth = current_app.config[Environment.RESTFULL_BASIC_AUTORIZATION]
        if basic_auth and basic_auth != {}:
            self.type = AuthenticationType.BASIC

    def valid(self):
        if not self.type:
            return True
        if self.type == AuthenticationType.BASIC:
            return self.basic_credentials()

    def basic_credentials(self):
        auth = request.authorization
        credentials = current_app.config[Environment.RESTFULL_BASIC_AUTORIZATION]
        return (auth and auth.type == AuthenticationType.BASIC.value and 
                auth.username in credentials and 
                credentials[auth.username] == auth.password)
