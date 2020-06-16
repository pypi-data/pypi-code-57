from flask import Blueprint, jsonify
from ..database_util import db, User
import uuid
from flask import request, make_response, abort, Response
from ..helper import get_user, authorized, auth_required

blue = Blueprint(__name__, import_name="blue")


@blue.route('/')
def index():
    return "Test Passed"

@blue.route('/initdb')
def db_operate():
    db.create_all()
    admin = User(token=str(uuid.uuid4()), username='admin',
                 password='admin@example.com')
    db.session.add(admin)
    db.session.commit()
    return "Operation done!"

@blue.route('/signup', methods=['POST'])
def signup():
    try:
        req_data = request.get_json(force=True)
        username = req_data['username']
        password = req_data['password']
        if get_user(username):
            return "Username already exists"
        token = str(uuid.uuid4())
        new_user = User(token=token, username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        ret = {"msg": "Signed up successfully", "token": token}
        return jsonify(ret)
    except Exception as e:
        return "Signup error: " + str(e)

@blue.route('/login', methods=['GET', 'POST'])
def login():
    try:
        req_data = request.get_json(force=True)
        username = req_data['username']
        password = req_data['password']
        # this is an database object
        user = get_user(username)

        if user.password == password:
            token = str(user.token)
            print(token)
            ret = jsonify({"msg": "Login success", "token": token})
            resp = make_response(ret)
            resp.set_cookie('token', token)
            # resp.set_cookie('username', username)
            # resp.set_cookie('password', password)
            return resp
        return "Login failed"
    except Exception as e:
        return "Login errod: " + str(e)

@blue.route('/logout', methods=['GET'])
@auth_required
def logout(user):
    try:
        resp = make_response("Logged out")
        resp.set_cookie('username', expires=0)
        resp.set_cookie('password', expires=0)
        return resp
    except Exception as e:
        return "Logour error: " + str(e)

@blue.route('/user', methods=['GET'])
@auth_required
def user(token):
    return "hello " + token

# @blue.route('/dropdb', methods=['GET'])
# @auth_required
# def drop(token):
#     return "hello " + token