from tests.icinga_helper import IcingaHelper

testinfra_hosts = ['ansible://icinga-host']


class TestChecks(IcingaHelper):

    def test_disk(self):
        assert self.is_service_ok('website-host!disk')
        assert self.is_service_ok('packages-host!disk')

    def test_icinga_ntp_time(self):
        assert self.is_service_ok('website-host!systemd-timesyncd is working')
