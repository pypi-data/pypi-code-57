# pylint
# vim: tw=100 foldmethod=indent
# pylint: disable=bad-continuation, invalid-name, superfluous-parens
# pylint: disable=bad-whitespace, mixed-indentation
# pylint: disable=redefined-outer-name, logging-not-lazy, logging-format-interpolation
# pylint: disable=missing-docstring, trailing-whitespace, trailing-newlines, too-few-public-methods

import logging
import json
from regapp_tools.parse_args import args
from regapp_tools.bwidmtools import get_user_registrations_from_external_id

logger = logging.getLogger(__name__)

class User:
    def __init__(self, regapp_userinfo, extensive=False):
        if args.verbose:
            print(json.dumps(regapp_userinfo, sort_keys=True, indent=4, separators=(',', ': ')))

        self.userinfo      = regapp_userinfo

        try:
            self.username      = F"{self.userinfo['attributeStore']['http://bwidm.de/bwidmOrgId']}_"\
                                 F"{self.userinfo['attributeStore']['urn:oid:0.9.2342.19200300.100.1.1']}"
        except KeyError:
            self.username      = "Username is not set"

        try:
            self.sub           = self.userinfo['eppn'].split('@')[0]
            self.iss           = self.userinfo['eppn'].split('@')[1]
        except KeyError:
            self.sub           = "Eppn is not set, cannot find sub"
            self.iss           = "Eppn is not set, cannot find iss"

        try:
            self.ssh_key_type  = "json encoded"
            self.ssh_keys      = json.loads(self.userinfo['genericStore']['ssh_key'])
        except json.decoder.JSONDecodeError:
            self.ssh_key_type  = "string encoded"
            self.ssh_keys      = self.userinfo['genericStore']['ssh_key']
        except KeyError:
            self.ssh_key_type  = "None"
            self.ssh_keys      = {}

        try:
            self.primary_group = Group(regapp_userinfo['primaryGroup'], primary       = True)
        except KeyError:
            self.primary_group = None

        self.groups        = []
        for group in regapp_userinfo['secondaryGroups']:
            self.groups.append(Group(group))

        for key in ['email', 'uidNumber', 'userStatus', 'createdAt', 'updatedAt', 'externalId', 'eppn']:
            try:
                setattr(self, key, regapp_userinfo[key])
            except KeyError:
                setattr(self, key, "Not set")

        if extensive:
            self.add_registries()

    def add_registries(self):
        '''Get list of registries:'''
        reg_info = get_user_registrations_from_external_id(self.externalId)
        self.reg = []
        for reg in reg_info:
            self.reg.append(Registry(reg))

    def __repr__(self, info=True, groups=False, sshkeys=False, extensive=False):
        rv = ""
        if info:
            rv += F"Username:      {self.username}\n"
            rv += F"external_id:   {self.externalId}\n"
            if extensive:
                rv += F"eppn:          {self.eppn}\n"
            rv += F"sub @ iss:     {self.sub} @ {self.iss}\n"
            rv += F"Email:         {self.email}\n"
            rv += F"Unix UID:      {self.uidNumber}\n"
            rv += F"Status:        {self.userStatus}\n"
            if sshkeys:
                rv += F"SSH Keys/type  {len(self.ssh_keys)} / {self.ssh_key_type}\n"
                rv += F"SSH Keys:      \n"
                rv += json.dumps(self.ssh_keys, sort_keys=True, indent=4, separators=(',', ': '))
            if extensive:
                rv += F"Registry State {self.get_latest_registry_status()}\n"
                rv += F"Created:       {self.createdAt}\n"
                rv += F"Updated:       {self.updatedAt}\n"
                rv += "\n"

        if groups:
            # rv += F"Groups:\n"
            # rv += "+--------------------------------+----------+-----------+\n"
            # rv += "| Group Name                     | Unix GID | RegApp ID |\n"
            rv += "Group Name                         Unix GID   RegApp ID  \n"
            # rv += "+--------------------------------+----------+-----------+\n"

            rv += self.primary_group.__repr__()
            for g in self.groups:
                rv += g.__repr__()
            # rv += "+--------------------------------+----------+-----------+"
        return rv

    def info(self, info=True, groups=False, sshkeys=False, extensive=False):
        return self. __repr__(info, groups, sshkeys, extensive)

    def get_latest_registry_status(self):
        try:
            return self.reg[-1].registryStatus
        except AttributeError: # No registries stored
            return "n/a"
        except IndexError: # No registries stored
            return "n/a"

    def has_active_registry(self):
        try:
            for reg in self.reg:
                if reg.registryStatus == "ACTIVE":
                    return True
        except AttributeError: # No registries stored
            pass
        return False

class Group:
    def __init__(self, groupinfo, primary=False):
        self.info = groupinfo
        self.is_primary = primary
    def __repr__(self):
        rv = ""
        rv += F"  {self.info['name']:30}"\
                F" {self.info['gidNumber']:8}"\
                F"   {self.info['id']:9}  "
        if self.is_primary:
            rv += "   (primary)"
        rv += "\n"
        return rv

class Registry:
    def  __init__ (self, reg_info):
        self.reg_info = reg_info
        keys = [ "agreedTime" , "createdAt" , "id" , "lastAccessCheck" , "lastReconcile",\
                 "lastStatusChange" , "registryStatus" , "serviceShortName" , "updatedAt", \
                 "userEmailAddress" , "version", "registryValues"]

        # "registryValues": {
        #     "cn"
        #     "description"
        #     "gidNumber"
        #     "givenName"
        #     "groupName"
        #     "homeDir"
        #     "localUid"
        #     "mail"
        #     "sambaEnabled"
        #     "sn"
        #     "uidNumber"
        # },
        for key in keys:
            try:
                setattr(self, key, reg_info[key])
            except KeyError:
                setattr(self, key, "Not set")

    def __repr__(self, extensive=False):
        rv = ""
        rv += F"{self.id} - "
        rv += F"{self.registryStatus:13} - "
        if extensive:
            rv += F"{self.lastStatusChange:30}- "
            rv += F"{self.createdAt:30}- "
        rv += F"{self.serviceShortName:10}- "
        rv += F"{self.registryValues['localUid']}"
        return rv
    def info (self, extensive=False):
        return self.__repr__(extensive)
