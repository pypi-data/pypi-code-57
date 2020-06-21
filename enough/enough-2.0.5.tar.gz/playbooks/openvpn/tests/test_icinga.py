from tests.icinga_helper import IcingaHelper

testinfra_hosts = ['ansible://icinga-host']


class TestChecks(IcingaHelper):

    def test_host(self):
        r = self.get_client().objects.get('Host', 'website-host')
        assert r['attrs']['name'] == 'website-host'

    def test_service_disk(self):
        assert self.is_service_ok('website-host!disk')

    def test_service_openvpn(self):
        assert self.is_service_ok('website-host!Check OpenVPN')
