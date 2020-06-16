from flask import request
from ..database_util import User
from functools import wraps

def get_user(username):
    """
    get_user will extract the corresponding user database object
    according to the unique userame
    param username: your username
    type: string
    """
    return User.query.filter_by(username=username).first()

def authorized(user, token):
    return user.token == token if user else False

def auth_required(function):
    @wraps(function)
    def decorated(*args, **kwargs):
        """
            Method to verify user before making each request
            :return : returns successful route if success else
                        auth failed message
        """
        try:
            # username = request.cookies.get('username')
            # password = request.cookies.get('password')
            token = request.cookies.get('token')
            print(token)
            user = User.query.filter_by(token=token).first()
            print(user)
            if user is not None:
                return function(token, *args, **kwargs) if authorized(user, token) else "Auth failed"
        except Exception as e:
            return "Auth error: " + str(e)
    return decorated
