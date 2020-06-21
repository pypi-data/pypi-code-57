import logging
import os
import re
import requests

from enough import settings
from enough.common import openstack
from enough.common import dotenough
from enough.common import ansible_utils

log = logging.getLogger(__name__)


class Service(object):

    def __init__(self, config_dir, share_dir, **kwargs):
        self.config_dir = config_dir
        self.share_dir = share_dir
        self.ansible = ansible_utils.Ansible(
            self.config_dir, self.share_dir, kwargs.get('inventory', []))
        self.set_service2hosts()
        self.update_vpn_dependencies()

    def set_service2hosts(self):
        suffix = '-service-hosts'
        groups = self.ansible.get_groups()
        self.service2hosts = {
            name.replace(suffix, ''): hosts for name, hosts in groups.items()
            if name.endswith(suffix)
        }

    def update_vpn_dependencies(self):
        hosts = self.ansible.ansible_inventory()['_meta']['hostvars'].keys()
        internal_hosts = set(self.hosts_with_internal_network(hosts))
        if not internal_hosts:
            return
        assert 'openvpn' in self.service2hosts
        openvpn_hosts = set(self.service2hosts['openvpn'])
        for service in self.service2hosts.keys():
            if service == 'openvpn':
                continue
            hosts = set(self.service2hosts[service])
            if internal_hosts & hosts:
                self.service2hosts[service] = list(internal_hosts | openvpn_hosts)

    def add_vpn_hosts_if_needed(self, hosts):
        internal_hosts = set(self.hosts_with_internal_network(hosts))
        if not internal_hosts:
            return hosts
        assert 'openvpn' in self.service2hosts
        openvpn_hosts = set(self.service2hosts['openvpn'])
        hosts = set(hosts)
        return list(hosts | openvpn_hosts)

    def hosts_with_internal_network(self, hosts):
        networks = self.ansible.get_variable_hosts('encrypted_device', 'openstack_network', *hosts)
        return [host for (host, network) in networks.items() if network == 'internal']

    def service_from_host(self, host):
        found = None
        hosts_count = 0
        for service, hosts in self.service2hosts.items():
            if host in hosts:
                if hosts_count > 0 and len(hosts) > hosts_count:
                    continue
                found = service
                hosts_count = len(hosts)
        return found


class ServiceDocker(Service):

    def create_or_update(self):
        pass


class ServiceOpenStack(Service):

    class PingException(Exception):
        pass

    def __init__(self, config_dir, share_dir, **kwargs):
        super().__init__(config_dir, share_dir, **kwargs)
        self.args = kwargs
        self.dotenough = dotenough.DotEnoughOpenStack(config_dir, self.args['domain'])
        self.dotenough.ensure()

    def maybe_delegate_dns(self):
        subdomain_regexp = r'(.*)\.d\.(.*)'
        m = re.match(subdomain_regexp, self.args['domain'])
        if not m:
            log.info(f'{self.args["domain"]} does not match "{subdomain_regexp}", '
                     'do not attempt to delegate the DNS')
            return False
        (subdomain, domain) = m.group(1, 2)
        api = f'api.{domain}'
        ping = f'https://{api}/ping/'
        r = requests.get(ping)
        if not r.ok:
            raise ServiceOpenStack.PingException(f'{ping} does not respond')

        h = openstack.Heat(self.config_dir, self.dotenough.clouds_file)
        s = openstack.Stack(self.config_dir,
                            self.dotenough.clouds_file,
                            h.get_stack_definition('bind-host'))
        s.set_public_key(self.dotenough.public_key())
        bind_host = s.create_or_update()
        r = requests.post(f'https://{api}/delegate-dns/',
                          json={
                              'name': subdomain,
                              'ip': bind_host['ipv4'],
                          })
        r.raise_for_status()
        return True

    def create_or_update(self):
        hosts = self.service2hosts[self.args['name']]
        h = openstack.Heat(self.config_dir, self.dotenough.clouds_file)
        h.create_missings(hosts, self.dotenough.public_key())
        self.maybe_delegate_dns()
        playbook = ansible_utils.Playbook(self.config_dir, self.share_dir)
        if os.path.isabs(self.args["playbook"]):
            playbook_file = self.args["playbook"]
        else:
            playbook_file = f'{self.config_dir}/{self.args["playbook"]}'
        playbook.run([
            f'--private-key={self.dotenough.private_key()}',
            '--limit', ','.join(hosts + ['localhost']),
            playbook_file,
        ])
        return {'fqdn': f'{self.args["name"]}.{self.args["domain"]}'}


def service_factory(config_dir=settings.CONFIG_DIR, share_dir=settings.SHARE_DIR, **kwargs):
    if kwargs['driver'] == 'openstack':
        return ServiceOpenStack(config_dir, share_dir, **kwargs)
    else:
        return ServiceDocker(config_dir, share_dir, **kwargs)
