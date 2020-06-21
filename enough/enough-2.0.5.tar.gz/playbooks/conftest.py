import os
import pytest
import shutil
import textwrap

from enough.common import Enough


def pytest_addoption(parser):
    parser.addoption(
        "--enough-no-create",
        action="store_true",
        help="Do not run the create step"
    )
    parser.addoption(
        "--enough-no-tests",
        action="store_true",
        help="Do not run the tests step"
    )
    parser.addoption(
        "--enough-no-destroy",
        action="store_true",
        help="Do not run the destroy step"
    )


def pytest_configure(config):
    pass


def make_config_dir(domain, cache):
    d = cache.makedir('dotenough')
    os.environ['ENOUGH_DOT'] = str(d)
    config_dir = f'{d}/{domain}'
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    return config_dir


def prepare_config_dir(domain, cache):
    os.environ['ENOUGH_DOMAIN'] = domain
    config_dir = make_config_dir(domain, cache)
    shutil.copy('infrastructure_key', f'{config_dir}/infrastructure_key')
    shutil.copy('infrastructure_key.pub', f'{config_dir}/infrastructure_key.pub')
    all_dir = f'{config_dir}/inventory/group_vars/all'
    if not os.path.exists(all_dir):
        os.makedirs(all_dir)
    shutil.copyfile('inventory/group_vars/all/clouds.yml', f'{all_dir}/clouds.yml')
    shutil.copyfile('inventory/group_vars/all/provision.yml', f'{all_dir}/provision.yml')
    open(f'{all_dir}/certificate.yml', 'w').write(textwrap.dedent(f"""\
    ---
    certificate_authority: letsencrypt_staging
    """))
    return config_dir


def get_hosts(session, enough):
    hosts = session.config.getoption("--enough-hosts").split(',')
    updated = enough.service.add_vpn_hosts_if_needed(hosts)
    return (hosts != updated, updated)


def reboot_internal(enough, hosts):
    for host in enough.service.hosts_with_internal_network(hosts):
        #
        # The reboot cannot be done immediately after removing the interface
        # for some reason. Otherwise sshd does not bind to the interface.
        #
        # Hopefully doing it at this stage is late enough and does not cause this
        # problem.
        #
        enough.openstack.o.server.reboot('--hard', host)


def pytest_sessionstart(session):
    service_directory = session.config.getoption("--enough-service")
    domain = f'{service_directory}.test'
    config_dir = prepare_config_dir(domain, session.config.cache)

    if session.config.getoption("--enough-no-create"):
        return

    e = Enough(config_dir, '.',
               domain=domain,
               driver='openstack',
               inventory=[f'playbooks/{service_directory}/inventory'],
               route_to_internal=False)
    (needs_vpn, hosts) = get_hosts(session, e)
    r = e.create_missings(hosts)
    if len(r) > 0:
        e.heat.create_test_subdomain('enough.community')
    if needs_vpn:
        if not e.vpn_has_credentials():
            vpn_hosts = ','.join(e.service.service2hosts['openvpn'])
            reboot_internal(e, hosts)
            e.playbook.run([
                '--private-key', f'{e.config_dir}/infrastructure_key',
                '-i', f'playbooks/openvpn/inventory',
                f'--limit={vpn_hosts},localhost',
                'playbooks/openvpn/playbook.yml',
            ])
        e.vpn_connect()

    hosts = ','.join(hosts)
    e.playbook.run([
        '--private-key', f'{e.config_dir}/infrastructure_key',
        '-i', f'playbooks/{service_directory}/inventory',
        f'--limit={hosts},localhost',
        f'playbooks/{service_directory}/playbook.yml',
    ])
    if needs_vpn:
        e.vpn_disconnect()


def pytest_runtest_setup(item):
    if item.config.getoption("--enough-no-tests"):
        pytest.skip("--enough-no-tests specified, skipping all tests")


def pytest_sessionfinish(session, exitstatus):
    if session.config.getoption("--enough-no-destroy"):
        return

    if exitstatus != 0:
        return

    service_directory = session.config.getoption("--enough-service")
    domain = f'{service_directory}.test'
    config_dir = make_config_dir(domain, session.config.cache)
    e = Enough(config_dir, '.',
               domain=domain,
               driver='openstack',
               inventory=[f'playbooks/{service_directory}/inventory'])
    (_, hosts) = get_hosts(session, e)
    e.host.delete_hosts(hosts)

    credentials = f'{config_dir}/openvpn/localhost.tar.gz'
    if os.path.exists(credentials):
        os.unlink(credentials)


def pytest_unconfigure(config):
    pass
