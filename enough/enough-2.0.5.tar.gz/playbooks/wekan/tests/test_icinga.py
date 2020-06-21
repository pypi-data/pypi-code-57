from tests.icinga_helper import IcingaHelper

testinfra_hosts = ['icinga-host']


class TestChecks(IcingaHelper):

    def test_host(self):
        r = self.get_client().objects.get('Host', 'wekan-host')
        assert r['attrs']['name'] == 'wekan-host'

    def test_service(self):
        assert self.is_service_ok('wekan-host!Wekan')
