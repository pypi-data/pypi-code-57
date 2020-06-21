import os
import pytest
import requests_mock as requests_mock_module
import shutil

from enough import settings
from enough.common import service


@pytest.mark.skipif('SKIP_OPENSTACK_INTEGRATION_TESTS' in os.environ,
                    reason='skip integration test')
def test_openstack_create_or_update(tmpdir, openstack_name, requests_mock):
    shutil.copy('infrastructure_key', f'{tmpdir}/infrastructure_key')
    shutil.copy('infrastructure_key.pub', f'{tmpdir}/infrastructure_key.pub')
    requests_mock.post(requests_mock_module.ANY, status_code=201)
    requests_mock.get(requests_mock_module.ANY, status_code=200)
    domain = f'enough.test'
    s = service.ServiceOpenStack(str(tmpdir), settings.SHARE_DIR, **{
        'driver': 'openstack',
        'playbook': os.path.abspath('tests/enough/common/test_common_service/enough-playbook.yml'),
        'domain': domain,
        'name': 'essential',
    })
    s.dotenough.set_certificate('ownca')
    s.dotenough.set_clouds_file('inventory/group_vars/all/clouds.yml')
    r = s.create_or_update()
    assert r['fqdn'] == f'essential.{domain}'
    # the second time around the hosts.yml are reused
    r = s.create_or_update()
    assert r['fqdn'] == f'essential.{domain}'


def test_service_from_host():
    s = service.Service(settings.CONFIG_DIR, settings.SHARE_DIR)
    assert s.service_from_host('icinga-host') in ('essential', 'openvpn', 'wekan')
    assert s.service_from_host('cloud-host') == 'cloud'
    assert s.service_from_host('unknown-host') is None


def test_update_vpn_dependencies():
    s = service.Service(settings.CONFIG_DIR, settings.SHARE_DIR)
    assert s.hosts_with_internal_network(['bind-host']) == []
    assert 'website-host' not in s.service2hosts['openvpn']
    assert 'website-host' not in s.service2hosts['weblate']
    s.ansible.set_inventories(['tests/enough/common/test_common_service/vpn_inventory'])
    s.set_service2hosts()
    assert 'website-host' in s.service2hosts['openvpn']
    assert s.hosts_with_internal_network(['icinga-host']) == ['icinga-host']
    s.update_vpn_dependencies()
    assert 'website-host' in s.service2hosts['weblate']
