import website
import testinfra
from tests.icinga_helper import IcingaHelper

testinfra_hosts = ['ansible://icinga-host']


class TestChecks(IcingaHelper):

    def test_host(self):
        r = self.get_client().objects.get('Host', 'website-host')
        assert r['attrs']['name'] == 'website-host'

    def test_service(self):
        website.update(testinfra.get_host('ansible://website-host',
                                          ssh_identity_file=self.ssh_identity_file,
                                          ansible_inventory=self.inventory))
        assert self.is_service_ok('website-host!Website')
