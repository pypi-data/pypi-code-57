import re
import json
from .verbose import VERBOSE


class Mailinglist():
    def __init__(self, conn, data):
        self.conn = conn
        self.data = data
        if data:
            for key in data:
                setattr(self, key, data[key])

            self.name = data['listName']

            members = []
            self.members = members
            for member in data['members']:
                match = re.search(r'^cn=(?P<cn>.*?)\,', member, re.IGNORECASE)
                if match:
                    members.append(match.groupdict()['cn'])

    def set_members(self, *members):
        if isinstance(members[0], list):
            members = tuple(members[0])
        resp = self._to_from_group(
            members, action='', mess="Members for mailinglist {} set")
        try:
            text = resp['audit_trail']['granted']
            text = re.sub(r'[\[\]]', '', text)
            self.members = re.split(r'\,\s*', text)
        except Exception:
            pass

    def add_members(self, *members):
        if isinstance(members[0], list):
            members = tuple(members[0])
        try:
            resp = self._to_from_group(
                members, action='add', mess="Added members to mailinglist {}")
            text = resp['audit_trail']['granted']
            text = re.sub(r'[\[\]]', '', text)
            members_to_add = re.split(r'\,\s*', text)
            for member in members_to_add:
                if member:
                    self.members.append(member)
        except Exception:
            pass

    def del_members(self, *members):
        if isinstance(members[0], list):
            members = tuple(members[0])
        try:
            resp = self._to_from_group(
                members, action='del', mess="Removed members from mailinglist {}")
            text = resp['audit_trail']['revoked']
            text = re.sub(r'[\[\]]', '', text)
            members_to_revoke = re.split(r'\,\s*', text)
            for member in members_to_revoke:
                if member:
                    self.members.remove(member)

        except Exception:
            pass

    def _to_from_group(self, members, action='add', mess="{}"):
        endpoint = '/mailinglists/{}/members/{}'.format(self.name, action)
        resp = self.conn._put_request(endpoint, members)
        if resp.ok:
            if VERBOSE:
                print(mess.format(self.name))
            return json.loads(resp.content.decode())

        else:
            data = json.loads(resp.content.decode())
            raise ValueError(data['message'])

    def delete(self):
        endpoint = '/mailinglists/{}'.format(self.name)
        resp = self.conn._delete_request(endpoint)
        if resp.ok:
            if VERBOSE:
                print("Mailinglist {} deleted.".format(self.name))
        else:
            data = json.loads(resp.content.decode())
            raise ValueError(data['message'])
