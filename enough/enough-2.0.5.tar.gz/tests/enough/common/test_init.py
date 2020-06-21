import os
import pytest
import sh
import shutil

from enough import settings
from enough.common import Enough
from enough.common.openstack import OpenStack, Stack


@pytest.mark.skipif('SKIP_OPENSTACK_INTEGRATION_TESTS' in os.environ,
                    reason='skip integration test')
def test_clone_and_destroy(tmpdir):
    clone_clouds = os.path.expanduser("~/.enough/dev/clone-clouds.yml")
    test_clouds = 'inventory/group_vars/all/clouds.yml'

    clone_override_dir = f'{tmpdir}/clone-override'
    shutil.copytree('tests/enough/common/test_init/clone-override',
                    clone_override_dir)
    original_domain = 'original.com'
    original_config_dir = f'{tmpdir}/{original_domain}'
    shutil.copytree('tests/enough/common/test_init/backup',
                    original_config_dir)
    password = 'PASSWORD'
    open(f'{original_config_dir}.pass', 'w').write(password)
    shutil.copy('infrastructure_key', f'{original_config_dir}/infrastructure_key')
    shutil.copy('infrastructure_key.pub', f'{original_config_dir}/infrastructure_key.pub')
    original_all_dir = f'{original_config_dir}/inventory/group_vars/all'
    os.makedirs(original_all_dir)
    original_clouds = f'{original_all_dir}/clouds.yml'
    shutil.copyfile(test_clouds, original_clouds)

    original = Enough(original_config_dir, settings.SHARE_DIR,
                      domain=original_domain,
                      driver='openstack')
    assert original.openstack.o.server.list().strip() == ''

    clone_domain = 'clone.com'
    clone = original.clone(clone_domain, clone_clouds)

    assert password == open(f'{clone.config_dir}.pass').read()
    assert 'REPLACED CONTENT' == open(
        f'{clone.config_dir}/inventory/host_vars/to-replace.yml').read().strip()
    assert clone.openstack.o.server.list().strip() == ''

    assert os.path.exists(clone.config_dir)
    clone.destroy()
    assert not os.path.exists(clone.config_dir)


def create_enough(tmpdir, clouds, dotenough, **kwargs):
    enough_domain = 'enough.com'
    enough_config_dir = f'{tmpdir}/{enough_domain}'
    shutil.copytree(f'tests/enough/common/test_init/{dotenough}',
                    enough_config_dir)
    shutil.copy('infrastructure_key', f'{enough_config_dir}/infrastructure_key')
    shutil.copy('infrastructure_key.pub', f'{enough_config_dir}/infrastructure_key.pub')
    enough_all_dir = f'{enough_config_dir}/inventory/group_vars/all'
    os.makedirs(enough_all_dir)
    enough_clouds = f'{enough_all_dir}/clouds.yml'
    shutil.copyfile(clouds, enough_clouds)

    enough = Enough(enough_config_dir, settings.SHARE_DIR,
                    domain=enough_domain,
                    driver='openstack',
                    **kwargs)
    return enough


def create_and_clone_server_and_volume(tmpdir, clone_clouds, test_clouds):
    original = create_enough(tmpdir, test_clouds, 'backup')
    original.set_args(name='sample', playbook='enough-playbook.yml')
    original.service.create_or_update()

    clone_domain = 'clone.com'
    clone = original.clone(clone_domain, clone_clouds)
    clone.set_args(name='sample', playbook='enough-playbook.yml')
    clone.service.create_or_update()

    return (original, clone)


@pytest.mark.skipif('SKIP_OPENSTACK_INTEGRATION_TESTS' in os.environ,
                    reason='skip integration test')
def test_clone_create_service(tmpdir):
    clone_clouds = os.path.expanduser("~/.enough/dev/clone-clouds.yml")
    test_clouds = 'inventory/group_vars/all/clouds.yml'

    try:
        (original, clone) = create_and_clone_server_and_volume(tmpdir, clone_clouds, test_clouds)
        assert 'sample-host' in original.openstack.o.server.list()
        assert 'sample-volume' in original.openstack.o.volume.list()
        assert 'sample-host' in clone.openstack.o.server.list()
        assert 'sample-volume' in clone.openstack.o.volume.list()
    finally:
        for clouds in (test_clouds, clone_clouds):
            o = OpenStack(settings.CONFIG_DIR, clouds)
            # comment out the following line to re-use the content of the regions and save time
            o.destroy_everything(None)


@pytest.mark.skipif('SKIP_OPENSTACK_INTEGRATION_TESTS' in os.environ,
                    reason='skip integration test')
def test_create_copy_host(tmpdir):
    clouds = 'inventory/group_vars/all/clouds.yml'

    try:
        enough = create_enough(tmpdir, clouds, 'copy')
        if 'copy-volume' not in enough.openstack.o.volume.list():
            enough.openstack.o.volume.create('--size', '1', 'copy-volume')
        ip = enough.create_copy_host('copy-from-host', 'some-volume', 'copy-volume')
        r = sh.ssh('-i', enough.dotenough.private_key(), f'root@{ip}', 'id')
        assert 'uid=0(root)' in r
        r = sh.ssh('-i', enough.dotenough.private_key(), f'root@{ip}', 'mountpoint', '/srv').strip()
        assert r == '/srv is a mountpoint'
    finally:
        o = OpenStack(settings.CONFIG_DIR, clouds)
        # comment out the following line to re-use the content of the regions and save time
        o.destroy_everything(None)


@pytest.mark.skipif('SKIP_OPENSTACK_INTEGRATION_TESTS' in os.environ,
                    reason='skip integration test')
def test_clone_volume_from_snapshot(tmpdir):
    clone_clouds = os.path.expanduser("~/.enough/dev/clone-clouds.yml")
    test_clouds = 'inventory/group_vars/all/clouds.yml'

    try:
        original = create_enough(tmpdir, test_clouds, 'backup')
        original.set_args(name='sample', playbook='enough-playbook.yml')
        original.service.create_or_update()
        ip = original.hosts.load().get_ip('sample-host')
        sh.ssh('-i', original.dotenough.private_key(), f'debian@{ip}', 'touch', '/srv/STONE')
        sh.ssh('-i', original.dotenough.private_key(), f'debian@{ip}', 'sync')
        original.openstack.backup_create(['sample-volume'])
        snapshot = f'{original.openstack.backup_date()}-sample-volume'
        assert snapshot in original.openstack.o.volume.snapshot.list()

        clone_domain = 'clone.com'
        clone = original.clone(clone_domain, clone_clouds)

        (from_ip, to_ip, from_volume, to_volume) = original._clone_volume_from_snapshot_body(
            clone, snapshot)

        assert sh.ssh('-i', original.dotenough.private_key(), f'root@{from_ip}',
                      'test', '-e', '/srv/STONE').exit_code == 0
        assert sh.ssh('-i', clone.dotenough.private_key(), f'root@{to_ip}',
                      'test', '!', '-e', '/srv/STONE').exit_code == 0
        original._rsync_copy_host(from_ip, to_ip)
        assert sh.ssh('-i', clone.dotenough.private_key(), f'root@{to_ip}',
                      'test', '-e', '/srv/STONE').exit_code == 0

        original._clone_volume_from_snapshot_cleanup(clone, from_volume)

    finally:
        for clouds in (test_clouds, clone_clouds):
            o = OpenStack(settings.CONFIG_DIR, clouds)
            # comment out the following line to re-use the content of the regions and save time
            o.destroy_everything(None)


@pytest.mark.skipif('SKIP_OPENSTACK_INTEGRATION_TESTS' in os.environ,
                    reason='skip integration test')
def test_create_service_matching_snapshot(tmpdir):
    test_clouds = 'inventory/group_vars/all/clouds.yml'

    try:
        enough = create_enough(tmpdir, test_clouds, 'backup')
        host = enough.create_service_matching_snapshot('2020-02-20-sample-volume')
        assert host == 'sample-host'
        assert 'sample-volume' in enough.openstack.o.volume.list()

    finally:
        o = OpenStack(settings.CONFIG_DIR, test_clouds)
        # comment out the following line to re-use the content of the regions and save time
        o.destroy_everything(None)


@pytest.mark.skipif('SKIP_OPENSTACK_INTEGRATION_TESTS' in os.environ,
                    reason='skip integration test')
def test_restore_remote(tmpdir):
    clone_clouds = os.path.expanduser("~/.enough/dev/clone-clouds.yml")
    test_clouds = 'inventory/group_vars/all/clouds.yml'

    try:
        original = create_enough(tmpdir, test_clouds, 'backup')
        original.set_args(name='sample', playbook='enough-playbook.yml')
        original.service.create_or_update()
        ip = original.hosts.load().get_ip('sample-host')

        sh.ssh('-i', original.dotenough.private_key(), f'debian@{ip}', 'touch', '/srv/STONE')
        original.openstack.backup_create(['sample-volume'])
        snapshot = f'{original.openstack.backup_date()}-sample-volume'
        assert snapshot in original.openstack.o.volume.snapshot.list()

        clone = original.restore_remote('test.com', clone_clouds, snapshot)
        assert 'sample-volume' in clone.openstack.o.volume.list()
        hosts = clone.hosts.load()
        Stack.wait_for_ssh(hosts.get_ip('sample-host'), hosts.get_port('sample-host'))
        assert sh.ssh('-i', clone.dotenough.private_key(), f'debian@{ip}',
                      'test', '-e', '/srv/STONE').exit_code == 0

    finally:
        for clouds in (test_clouds, clone_clouds):
            o = OpenStack(settings.CONFIG_DIR, clouds)
            # comment out the following line to re-use the content of the regions and save time
            o.destroy_everything(None)


@pytest.mark.skipif('SKIP_OPENSTACK_INTEGRATION_TESTS' in os.environ,
                    reason='skip integration test')
def test_create_missings(tmpdir):
    test_clouds = 'inventory/group_vars/all/clouds.yml'

    try:
        enough = create_enough(tmpdir, test_clouds, 'create-missings')
        r = enough.create_missings(['bind-host'])
        assert 'bind-host' in r
        internal_dns = enough.openstack.o.subnet.show(
            '--format=value', '-c', 'dns_nameservers', 'internal').strip()
        bind_internal_ip = enough.openstack.server_ip_in_network('bind-host', 'internal')
        assert bind_internal_ip == internal_dns
    finally:
        o = OpenStack(settings.CONFIG_DIR, test_clouds)
        # comment out the following line to re-use the content of the regions and save time
        o.destroy_everything(None)
