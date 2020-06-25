import os
import json

from .verbose import VERBOSE


class Person():
    def __init__(self, conn, data=None):
        self.conn = conn
        self.data = data
        if data:
            for key in data:
                setattr(self, key, data[key])

    def new_user(self, username, password, description=None):
        endpoint = '/usermgr/person/{}'.format(self.npid)
        body = {
            "username": username,
            "init_passwd": password,
            "memo": description,
        }
        resp = self.conn._post_request(endpoint, body)
        if resp.ok:
            user = self.conn.get_user(username)
            if VERBOSE:
                print("new user {} was successfully created".format(username))
            return user
        else:
            data = json.loads(resp.content.decode())
            raise ValueError(data['message'])
