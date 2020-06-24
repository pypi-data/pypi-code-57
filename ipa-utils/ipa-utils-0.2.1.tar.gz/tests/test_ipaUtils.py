import unittest
import os
from ipa_utils import IpaService

def unquote(value):
    if value.startswith('"'):
        value = value[1:]
    if value.endswith('"'):
        value = value[:-1]
    return value

class TestIpaUtils(unittest.TestCase):

    def setUp(self):
        self.server = unquote(os.environ["LDAP_SERVER"])
        self.port = int(os.environ["LDAP_PORT"])
        self.username = unquote(os.environ["LDAP_USERNAME"])
        self.password = unquote(os.environ["LDAP_PASSWORD"])
        self.base_dn = unquote(os.environ["LDAP_BASE_DN"])
        self.test_user = unquote(os.environ["TEST_USER"])

        print("server info: [{}] [{}] [{}] [{}] [{}] [{}]".format(self.server, self.port, self.username, self.password, self.base_dn, self.test_user))
        self.service = IpaService(self.server, self.port, self.base_dn, self.username, self.password)

    def test01(self):
        assert self.service.base_dn
    
    def test02(self):
        user = self.service.get_user_detail(self.test_user)
        assert user["uid"] == self.test_user

    def test03(self):
        user = self.service.get_user_detail("not_exists_user_20200624211900")
        assert user is None

    def test04(self):
        users = self.service.get_user_entries()
        assert len(users)

