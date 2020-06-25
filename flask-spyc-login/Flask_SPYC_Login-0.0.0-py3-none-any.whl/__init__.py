__all__ = ['SPYCLogin']

import os
from flask import Flask, redirect, url_for, request, session,  Blueprint
from .tools import store_redirect, retrieve_redirect, verify


auth_blueprint = Blueprint('auth', __name__)


def set_user(identity=None):
    # the default session setter
    # must set session['login']
    # will be called with no parameter before_request
    if not identity:
        email = 'visitor@unknown.com'
        role = 'public'
    if identity:
        email = identity['email']
        role = identity['role']
    session['email'] = email
    session['role'] = role
    session['login'] = email.endswith('@school.pyc.edu.hk')


@auth_blueprint.route('/login')
def login():
    # the login route
    store_redirect()
    url = os.getenv('SPYC_LOGIN_URL') + '/signin?redirect=' + url_for('auth.auth', _external=True)
    return redirect(url)


@auth_blueprint.route('/auth')
def auth():
    # return route for login, only for program use
    token = request.values.get('token')
    identity = verify(token)
    if identity['verified']:
        set_user(identity)
    else:
        set_user()
    redirectURL = retrieve_redirect()
    return redirect(redirectURL)


class SPYCLogin:
    def __init__(self, app=None):
        # init app if given
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        app.register_blueprint(auth_blueprint)
        @app.before_request
        def session_init():
            if not session.get('login', False):
                set_user()

    @staticmethod
    def session_controller(func):
        # update set_user function, use as decorator
        global set_user
        set_user = func
