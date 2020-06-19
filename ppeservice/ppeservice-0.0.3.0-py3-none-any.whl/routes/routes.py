from ..version import version_num
from flask import Blueprint, jsonify
from ..database_util import db, User
import uuid
from flask import request, make_response, abort, Response
from ..helper import get_user, authorized, auth_required
import datetime
blue = Blueprint(__name__, import_name="blue")


# This part below, initialize the api for the real route, the root route of / is still loaded by the default blueprint
from flask_restx import Api, Resource, Namespace, fields, reqparse
api = Api(title="PPEService RestApi Documentation",version=version_num,doc="/api/docs")
ns = Namespace('/',"PPEService RestApi Documentation")
def init_api(app):
    api.init_app(app=app)
    api.add_namespace(ns)
    
    
@blue.route('/')
def index():
    return "Test Passed"

@ns.route('/initdb')
class initdb(Resource):
    def post(self):
        """
        If you want to re create the database, you could run this, 
        this function shouldb't be exposed externally
        """
        db.create_all()
        today = datetime.date.today()
        admin = User(token=str(uuid.uuid4()), username='admin',
                    password='admin@example.com',token_generated_date=today)
        db.session.add(admin)
        db.session.commit()
        return "Operation done!"

# Below are the orm object structures
account = api.model('account_structure', {
    'username': fields.String(required=True, description='username'),
    'password': fields.String(required=True, description='password')
})

# token = api.model('token_structure', {
#     'token': fields.String(required=True, description='username'),
# })
def RequestParser():
    parser = reqparse.RequestParser()
    parser.add_argument('token', required=True, location='headers')
    return parser

@ns.route('/signup')
@ns.expect(account)
class signup(Resource):
    def post(self):
        """
        This api allows you to signup
        """
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

@ns.route('/login')
@ns.expect(account)
class login(Resource):
    def post(self):
        """
        This api allows you to login
        """
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

# This is the token structre, as it's from the header, so should be retrieved from parser
token_parser = RequestParser()


@ns.route('/logout')
@ns.expect(token_parser)
class logout(Resource):
    @auth_required
    def post(self, token):
        """
        This api allows you to logout
        """
        try:
            user = User.query.filter_by(token=token).first()
            resp = make_response("Logged out")
            today = datetime.date.today()
            user.token_generated_date = today - datetime.timedelta(days=5)
            db.session.commit()
            return resp
        except Exception as e:
            return "Logour error: " + str(e)

@ns.route('/user')
@ns.expect(token_parser)
class TestUser(Resource):
    @auth_required
    def get(self, token):
        """
        This is a testing function for the token based authentication, 
        all the function implemented later should be implemented this way"""
        return "hello " + token

# @blue.route('/dropdb', methods=['GET'])
# @auth_required
# def drop(token):
#     return "hello " + token