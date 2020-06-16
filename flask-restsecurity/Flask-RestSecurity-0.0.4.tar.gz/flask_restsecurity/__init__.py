from flask_restsecurity.model.authentication import Authentication
from flask_restsecurity.config.env import Environment
from flask import Response, current_app

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