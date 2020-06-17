from flask import Blueprint, jsonify
from ..database_util import db, User
import uuid
from flask import request, make_response, abort, Response
from ..helper import get_user, authorized, auth_required
import datetime
blue = Blueprint(__name__, import_name="blue")


@blue.route('/')
def index():
    return "Test Passed"

@blue.route('/initdb')
def db_operate():
    db.create_all()
    today = datetime.date.today()
    admin = User(token=str(uuid.uuid4()), username='admin',
                 password='admin@example.com',token_generated_date=today)
    db.session.add(admin)
    db.session.commit()
    return "Operation done!"

@blue.route('/signup', methods=['POST'])
def signup():
    try:
        today = datetime.date.today()
        req_data = request.get_json(force=True)
        username = req_data['username']
        password = req_data['password']
        if get_user(username):
            return "Username already exists"
        token = str(uuid.uuid4())
        new_user = User(token=token, username=username, password=password, token_generated_date=today)
        db.session.add(new_user)
        db.session.commit()
        # param today is in type of date, but the date from database is in type of datetime
        # so need to do the convertion, we can convert the datetime to date to do the comparasion
        # print(today == User.query.filter_by(username=username).first().token_generated_date.date())

        ret = {"msg": "Signed up successfully, you can login now!"}
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
            today = datetime.date.today()
            user.token_generated_date = today
            db.session.commit()
            ret = jsonify({"msg": "Login success", "token":token})
            resp = make_response(ret)
            return resp
        return "Login failed"
    except Exception as e:
        return "Login errod: " + str(e)

@blue.route('/logout', methods=['GET'])
@auth_required
def logout(token):
    try:
        user = User.query.filter_by(token=token).first()
        resp = make_response("Logged out")
        today = datetime.date.today()
        user.token_generated_date = today - datetime.timedelta(days=5)
        db.session.commit()
        return resp
    except Exception as e:
        return "Logour error: " + str(e)

@blue.route('/user', methods=['POST', 'GET'])
@auth_required
def user(token):
    return "hello " + token

# @blue.route('/dropdb', methods=['GET'])
# @auth_required
# def drop(token):
#     return "hello " + token