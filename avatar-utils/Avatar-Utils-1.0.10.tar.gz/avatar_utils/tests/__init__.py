from unittest import TestCase

import requests
from flask import Response


class AbstractApp:
    client = None
    headers = {'Content-type': 'application/json'}

    def post(self, url, data=dict()):
        return self.client.post(url, json=data, headers=self.headers)

    def get(self, url, data=dict()):
        return self.client.get(url, json=data, headers=self.headers)

    def register(self, username, email, password, confirm):
        return self.post('/register', data=dict(username=username, email=email, password=password, confirm=confirm))

    def login(self, username, password):
        return self.post('/login', data=dict(username=username, password=password))

    def logout(self):
        return self.post('/logout')

    def delete(self, user_id, password):
        return self.post('/user/delete', data=dict(user_id=user_id, password=password))


class RemoteApp(AbstractApp):
    client = requests
    base_url = 'http://10.9.14.101:8000'

    def post(self, url, data=dict()):
        res = super().post(self.base_url + url, data)
        return self.convert_to_flask_response(res)

    def get(self, url, data=dict()):
        res = super().get(self.base_url + url, data)
        return self.convert_to_flask_response(res)

    # TODO transfer headers
    @staticmethod
    def convert_to_flask_response(response):
        res = Response(
            response=response.text,
            status=response.status_code,
            mimetype=response.headers['content-type']
        )

        return res


class UnitTest(TestCase, AbstractApp):
    app = None
    db = None

    def setUp(self):
        TestCase.setUp(self)
        try:
            print('SQLALCHEMY_DATABASE_URI: %s' % self.app.config['SQLALCHEMY_DATABASE_URI'])
        except KeyError:
            pass

        self.assertFalse(self.app is None)
        self.assertFalse(self.client is None)
        self.assertTrue(self.app.config['TESTING'])

        self.app_context = self.app.app_context()
        self.app_context.push()
        self.db.create_all()
        super().setUp()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()
        self.app_context.pop()
        TestCase.tearDown(self)


class BaseUnitTest(UnitTest):
    from app import create_app, db

    app = create_app('testing')
    client = app.test_client()
    db = db


class IntegrationTest(TestCase, RemoteApp):
    pass
