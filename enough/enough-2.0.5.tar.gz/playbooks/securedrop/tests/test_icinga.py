from tests.icinga_helper import IcingaHelper

testinfra_hosts = ['ansible://icinga-host']


class TestChecks(IcingaHelper):

    def test_service(self, host):
        assert self.is_service_ok('securedrop-host!securedrop-host over Tor')
