import json
import re
import requests
from urllib.parse import urlparse, urljoin, quote
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from .group import Group
from .person import Person
from .user import User
from .verbose import VERBOSE
from .mailinglist import Mailinglist


class ETH_IAM_conn():
    def __init__(self, admin_username, admin_password, hostname, endpoint_base):
        self._admin_username = admin_username
        self._admin_password = admin_password
        self.hostname = hostname
        self.endpoint_base = endpoint_base
        self.verify_certificates = True
        self.timeout = 600

    def _delete_request(self, endpoint):
        full_url = urljoin(self.hostname, self.endpoint_base+endpoint)
        resp = requests.delete(
            full_url,
            headers={'Accept': 'application/json'},
            auth=(self._admin_username, self._admin_password),
            verify=self.verify_certificates,
            timeout=self.timeout,
        )
        return resp

    def _post_request(self, endpoint, body):
        full_url = urljoin(self.hostname, self.endpoint_base+endpoint)
        resp = requests.post(
            full_url,
            json.dumps(body),
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            auth=(self._admin_username, self._admin_password),
            verify=self.verify_certificates,
            timeout=self.timeout,
        )
        return resp

    def _put_request(self, endpoint, body):
        full_url = urljoin(self.hostname, self.endpoint_base+endpoint)
        resp = requests.put(
            full_url,
            json.dumps(body),
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            auth=(self._admin_username, self._admin_password),
            verify=self.verify_certificates,
            timeout=self.timeout,
        )
        return resp

    def _get_request(self, endpoint):
        full_url = urljoin(self.hostname, self.endpoint_base+endpoint)
        resp = requests.get(
            full_url,
            headers={'Accept': 'application/json'},
            auth=(self._admin_username, self._admin_password),
            verify=self.verify_certificates,
            timeout=self.timeout,
        )
        return resp

    def new_person(self, firstname, lastname):
        raise Exception("not implemented yet")
        return Person(conn=self, firstname=firstname, lastname=lastname)

    def get_person(self, identifier=None, **kwargs):
        if identifier is not None:
            endpoint = '/usermgr/person/{}'.format(identifier)
        elif kwargs:
            args = "&".join("{}={}".format(key, val)
                            for key, val in kwargs.items())
            endpoint = '/usermgr/person?{}'.format(args)
        else:
            raise ValueError("please provide an identifier")

        resp = self._get_request(endpoint)
        data = json.loads(resp.content.decode())
        if resp.ok:
            return Person(conn=self, data=data)
        else:
            raise ValueError(data['message'])

    def get_user(self, identifier):
        endpoint = '/usermgr/user/{}'.format(identifier)
        resp = self._get_request(endpoint)
        data = json.loads(resp.content.decode())
        if resp.ok:
            return User(conn=self, data=data)
        else:
            raise ValueError(data['message'])

    def new_group(self, name, description, admingroup, targets, members=None):
        """
        name=<Group Name>
        description=<what is the purpose of this group>
        admingroup=<Admin Group>
        targets=['AD', 'LDAPS'] -- specify at least one target system
        members=['username1', 'username2']
        """
        if members is None:
            members = []

        endpoint = '/groupmgr/group'
        body = {
            "name": name,
            "description": description,
            "admingroup": admingroup,
            "targets": targets,
            "members": members
        }
        resp = self._post_request(endpoint, body)
        if resp.ok:
            data = json.loads(resp.content.decode())
            if VERBOSE:
                print("new group {} was successfully created".format(name))
            return Group(conn=self, data=data)
        else:
            data = json.loads(resp.content.decode())
            raise ValueError(data['message'])

    def del_group(self, name):
        """Deletes a group and removes it from all its target systems.
        """
        endpoint = '/groupmgr/group/{}'.format(name)
        resp = self._delete_request(endpoint)
        if resp.ok:
            if VERBOSE:
                print("group {} was successfully deleted".format(name))
        else:
            data = json.loads(resp.content.decode())
            raise ValueError(data['message'])

    def get_groups(self, **kwargs):
        """
        agroup=<Admin Group>  -- Get all groups of a given admin group
        name=group_name*      -- all groups starting with «group_name*»
        """
        if kwargs:
            args = "&".join("{}={}".format(key, val)
                            for key, val in kwargs.items())
            endpoint = '/groupmgr/groups?{}'.format(args)
        else:
            raise ValueError(
                "please provide a name or agroup parameter (or both)")

        resp = self._get_request(endpoint)
        data = json.loads(resp.content.decode())
        if resp.ok:
            groups = []
            for item in data:
                groups.append(Group(conn=self, data=item))

            return groups
        else:
            raise ValueError(data['message'])

    def get_group(self, identifier=None):
        if identifier is not None:

            if re.search(r'^\d+$', identifier):
                # we searched for a gidNumber
                groups = self.get_groups(gidNumber=identifier)
                if len(groups) == 1:
                    return groups[0]
                else:
                    raise ValueError(
                        'No group found with gidNumber={}'.format(identifier))
            else:
                endpoint = '/groupmgr/group/{}'.format(identifier)
        else:
            raise ValueError("please provide an identifier")
        resp = self._get_request(endpoint)
        data = json.loads(resp.content.decode())
        if resp.ok:
            return Group(conn=self, data=data)
        else:
            raise ValueError(data['message'])

    def get_mailinglist(self, identifier=None, **kwargs):
        if identifier is not None:
            endpoint = '/mailinglists/{}'.format(identifier)
        elif kwargs:
            args = "&".join("{}={}".format(key, val)
                            for key, val in kwargs.items())
            endpoint = '/mailinglists/?{}'.format(args)
        else:
            raise ValueError("please provide an identifier")
        resp = self._get_request(endpoint)
        data = json.loads(resp.content.decode())
        if resp.ok:
            return Mailinglist(conn=self, data=data)
        else:
            raise ValueError(data['message'])
