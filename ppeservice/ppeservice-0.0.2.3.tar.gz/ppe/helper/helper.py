from flask import request
from ..database_util import User
from functools import wraps
import datetime

def get_user(username):
    """
    get_user will extract the corresponding user database object
    according to the unique userame
    param username: your username
    type: string
    """
    return User.query.filter_by(username=username).first()

def authorized(user, token):
    if user:
        return user.token == token and \
             user.token_generated_date.date() + datetime.timedelta(days=3) > datetime.date.today()
    else:
        return False

def auth_required(function):
    @wraps(function)
    def decorated(*args, **kwargs):
        """
            Method to verify user before making each request
            :return : returns successful route if success else
                        auth failed message
        """
        try:
            print("inside of try")
            token = request.headers['token']
            user = User.query.filter_by(token=token).first()
            if user is not None:
                return function(token=token, *args, **kwargs) if authorized(user, token) else "Auth failed, maybe you token is expired, try login again"
        except Exception as e:
            return "Auth error: " + str(e)
    return decorated
