import os
import pytest
import requests_mock as requests_mock_module

from tests.modified_environ import modified_environ

from enough import settings
from enough.common.openstack import Stack, Heat, OpenStack


#
# Stack
#
@pytest.mark.skipif('SKIP_OPENSTACK_INTEGRATION_TESTS' in os.environ,
                    reason='skip integration test')
def test_stack_create_or_update_default(openstack_name):
    d = {
        'name': openstack_name,
        'flavor': 's1-2',
        'port': '22',
        'volumes': [
            {
                'size': '1',
                'name': openstack_name,
            },
        ],
    }
    s = Stack(settings.CONFIG_DIR, 'inventory/group_vars/all/clouds.yml', d)
    s.set_public_key('infrastructure_key.pub')
    r = s.create_or_update()
    assert r['port'] == '22'
    assert 'ipv4' in r
    assert r == s.create_or_update()
    s.delete()


@pytest.mark.skipif('SKIP_OPENSTACK_INTEGRATION_TESTS' in os.environ,
                    reason='skip integration test')
def test_stack_create_or_update_with_internal_network(openstack_name):
    name = openstack_name
    network = openstack_name
    class_c = '10.101.30'
    cidr = f'{class_c}.0/24'
    d = {
        'name': name,
        'flavor': 's1-2',
        'port': '22',
        'internal_network': network,
        'internal_network_cidr': cidr,
    }
    s = Stack(settings.CONFIG_DIR, 'inventory/group_vars/all/clouds.yml', d)
    s.set_public_key('infrastructure_key.pub')
    r = s.create_or_update()
    assert r['port'] == '22'
    ipv4 = r['ipv4']
    o = OpenStack(settings.CONFIG_DIR, 'inventory/group_vars/all/clouds.yml')
    assert o.server_connected_to_network(name, network)
    assert r == s.create_or_update()
    assert o.server_connected_to_network(name, network)
    assert r['ipv4'] == ipv4
    s.delete()
    assert not o.network_exists(network)


@pytest.mark.skipif('SKIP_OPENSTACK_INTEGRATION_TESTS' in os.environ,
                    reason='skip integration test')
@pytest.mark.skipif('SKIP_NETWORK_OPENSTACK_INTEGRATION_TESTS' in os.environ,
                    reason='skip network integration test')
def test_stack_create_or_update_network(openstack_name):
    o = OpenStack(settings.CONFIG_DIR, 'inventory/group_vars/all/clouds.yml')
    if 'internal' not in o.o.network.list('-f=value', '-c=Name'):
        pytest.skip('no internal network')
    d = {
        'name': openstack_name,
        'flavor': 's1-2',
        'port': '22',
        'network': 'internal',
        'volumes': [
            {
                'size': '1',
                'name': openstack_name,
            },
        ],
    }
    s = Stack(settings.CONFIG_DIR, 'inventory/group_vars/all/clouds.yml', d)
    s.set_public_key('infrastructure_key.pub')
    r = s.create_or_update()
    assert r['port'] == '22'
    assert 'ipv4' in r
    assert r['ipv4'].startswith('10.')
    assert r == s.create_or_update()
    s.delete()


#
# Heat
#
def test_heat_definition():
    h = Heat(settings.CONFIG_DIR, 'inventory/group_vars/all/clouds.yml')
    definitions = h.get_stack_definitions()
    assert 'bind-host' in definitions
    definition = h.get_stack_definition('bind-host')
    assert definition['name'] == 'bind-host'


def test_host_from_volume():
    h = Heat(settings.CONFIG_DIR, 'inventory/group_vars/all/clouds.yml')
    assert h.host_from_volume('cloud-volume') == 'cloud-host'
    assert h.host_from_volume('unknown-volume') is None


def test_heat_definition_encrypted():
    d = 'tests/enough/common/test_openstack/config_dir'
    h = Heat(d, 'inventory/group_vars/all/clouds.yml')
    definitions = h.get_stack_definitions(share_dir=d)
    assert 'my-host' in definitions
    assert definitions['my-host']['myvariable'] == 'myvalue'


def test_create_test_subdomain_no_bind(mocker):
    mocker.patch('os.path.exists', return_value=True)
    mocker.patch('enough.common.openstack.Stack.list', return_value=[])
    h = Heat(settings.CONFIG_DIR, 'inventory/group_vars/all/clouds.yml')
    assert h.create_test_subdomain('my.tld') is None


def test_create_test_subdomain_with_bind(tmpdir, mocker, requests_mock):
    mocker.patch('enough.settings.CONFIG_DIR', str(tmpdir))
    d = f'{tmpdir}/inventory/group_vars/all'
    os.makedirs(d)
    assert not os.path.exists(f'{d}/domain.yml')
    mocker.patch('os.path.exists', return_value=True)
    mocker.patch('enough.common.openstack.Stack.list', return_value=['bind-host'])
    mocker.patch('enough.common.openstack.Stack.set_public_key')
    mocker.patch('enough.common.openstack.Stack.create_or_update', return_value={
        'ipv4': '1.2.3.4',
    })
    mocker.patch('enough.common.openstack.Heat.get_stack_definition')
    requests_mock.post(requests_mock_module.ANY, status_code=201)
    h = Heat(settings.CONFIG_DIR, 'inventory/group_vars/all/clouds.yml')
    with modified_environ(ENOUGH_API_TOKEN="TOKEN"):
        fqdn = h.create_test_subdomain('my.tld')
    assert '.test.my.tld' in fqdn
    assert os.path.exists(f'{d}/domain.yml')


#
# OpenStack
#
@pytest.mark.skipif('SKIP_OPENSTACK_INTEGRATION_TESTS' in os.environ,
                    reason='skip integration test')
def test_network(openstack_name):
    o = OpenStack(settings.CONFIG_DIR, 'inventory/group_vars/all/clouds.yml')
    o.network_and_subnet_create(openstack_name, '10.11.12.0/24')
    assert o.network_exists(openstack_name)
    assert o.subnet_exists(openstack_name)

    dns_ip = '1.2.3.4'
    o.subnet_update_dns(openstack_name, dns_ip)
    r = o.o.subnet.show('--format=value', '-c', 'dns_nameservers', openstack_name)
    assert r.strip() == dns_ip


@pytest.mark.skipif('SKIP_OPENSTACK_INTEGRATION_TESTS' in os.environ,
                    reason='skip integration test')
def test_backup_create_with_name(openstack_name, caplog):
    o = OpenStack(settings.CONFIG_DIR, 'inventory/group_vars/all/clouds.yml')
    o.o.volume.create('--size=1', openstack_name)
    assert o.backup_create([openstack_name]) == 1
    assert o.backup_create([openstack_name]) == 0
    available_snapshot = f'AVAILABLE {o.backup_date()}-{openstack_name}'
    assert available_snapshot in caplog.text
    assert o.backup_prune(0) == 1
    assert o.backup_prune(0) == 0


@pytest.mark.skipif('SKIP_OPENSTACK_INTEGRATION_TESTS' in os.environ,
                    reason='skip integration test')
def test_backup_create_no_names(openstack_name, caplog):
    o = OpenStack(settings.CONFIG_DIR, 'inventory/group_vars/all/clouds.yml')
    o.o.volume.create('--size=1', openstack_name)
    o.backup_create([])
    available_snapshot = f'AVAILABLE {o.backup_date()}-{openstack_name}'
    assert available_snapshot in caplog.text


@pytest.mark.skipif('SKIP_OPENSTACK_INTEGRATION_TESTS' in os.environ,
                    reason='skip integration test')
def test_openstack_replace_volume(openstack_name):
    d = {
        'name': openstack_name,
        'flavor': 's1-2',
        'port': '22',
        'volumes': [
            {
                'size': '1',
                'name': openstack_name,
            },
        ],
    }
    s = Stack(settings.CONFIG_DIR, 'inventory/group_vars/all/clouds.yml', d)
    s.set_public_key('infrastructure_key.pub')
    s.create_or_update()
    other_volume = f'{openstack_name}_other'
    o = OpenStack(settings.CONFIG_DIR, 'inventory/group_vars/all/clouds.yml')
    o.o.volume.create('--size=1', other_volume)
    assert openstack_name in o.o.volume.list('--name', openstack_name)
    o.replace_volume(openstack_name, other_volume)
    assert o.o.volume.list('--name', other_volume).strip() == ''
    assert openstack_name in o.o.volume.list('--name', openstack_name)
