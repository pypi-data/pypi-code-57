import os
import json

from .person import Person
from .verbose import VERBOSE

service_map = {
    "LDAP": "LDAP",
    "LDAPS": "LDAP",
    "MAILBOX": "Mailbox",
}


class User():
    def __init__(self, conn, data):
        self.conn = conn
        self.data = data
        if data:
            for key in data:
                setattr(self, key, data[key])

    def delete(self):
        endpoint = '/usermgr/person/{}'.format(self.username)
        resp = self.conn._delete_request(endpoint)
        if resp.ok:
            if VERBOSE:
                print("User {} deleted.".format(self.username))
        else:
            data = json.loads(resp.content.decode())
            raise ValueError(data['message'])

    def get_person(self):
        endpoint = '/usermgr/person/{}'.format(self.npid)
        resp = self.conn._get_request(endpoint)
        data = json.loads(resp.content.decode())
        if resp.ok:
            return Person(conn=self, data=data)
        else:
            raise ValueError(data['message'])

    def _to_from_group(self, group_name, action='add', mess="{} {}"):
        endpoint = '/groupmgr/group/{}/members/{}'.format(group_name, action)
        body = [self.username]
        resp = self.conn._put_request(endpoint, body)
        if resp.ok:
            if VERBOSE:
                print(mess.format(self.username, group_name))
        else:
            data = json.loads(resp.content.decode())
            raise ValueError(data['message'])

    def add_to_group(self, group_name):
        self._to_from_group(group_name, action='add_forgiving',
                            mess="Added user {} to group {}")

    def remove_from_group(self, group_name):
        self._to_from_group(group_name, 'del',
                            mess="Removed user {} from group {}")

    def grant_service(self, service_name):
        if service_name.upper() in service_map:
            service_name = service_map[service_name.upper()]
        endpoint = '/usermgr/user/{}/service/{}'.format(
            self.username, service_name)
        resp = self.conn._post_request(endpoint, {})
        if resp.ok:
            if VERBOSE:
                print("Service {} granted to {}".format(
                    service_name, self.username))
        else:
            data = json.loads(resp.content.decode())
            raise ValueError(data['message'])

    def revoke_service(self, service_name):
        if service_name.upper() in service_map:
            service_name = service_map[service_name.upper()]
        endpoint = '/usermgr/user/{}/service/{}'.format(
            self.username, service_name)
        resp = self.conn._delete_request(endpoint)
        if resp.ok:
            if VERBOSE:
                print("Service {} revoked from {}".format(
                    service_name, self.username))
        else:
            data = json.loads(resp.content.decode())
            raise ValueError(data['message'])

    def get_service(self, service_name):
        # TODO: API is not implemented yet
        endpoint = '/usermgr/user/{}/service/{}'.format(
            self.username, service_name)
        resp = self.conn._get_request(endpoint)
        data = json.loads(resp.content.decode())
        if resp.ok:
            return Service(conn=self.conn, data=data)
        else:
            raise ValueError(data['message'])

    def set_password(self, password, service_name="LDAPS"):
        """Sets a password for a given service
        """

        if service_name.upper() not in service_map:
            raise ValueError(
                f"Cannot set password for service: {service_name}. Sorry!")

        endpoint = '/usermgr/user/{}/service/{}/password'.format(
            self.username, service_map[service_name.upper()])
        body = {"password": password}
        resp = self.conn._put_request(endpoint, body)

        if resp.ok:
            if VERBOSE:
                print(
                    "password for user {} and service {} has been successfully changed.".format(
                        self.username, service_name
                    )
                )
        else:
            data = json.loads(resp.content.decode())
            raise ValueError(data['message'])
