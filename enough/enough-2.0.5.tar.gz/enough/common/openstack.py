import base64
import datetime
import json
import logging
import os
import re
import requests
import sh
import socket
import textwrap
import time
import yaml

from enough import settings
from enough.common.retry import retry
from enough.common.dotenough import Hosts

log = logging.getLogger(__name__)


class OpenStackBase(object):

    INTERNAL_NETWORK = 'internal'
    INTERNAL_NETWORK_CIDR = '10.20.30.0/24'

    def __init__(self, config_dir, config_file, **kwargs):
        self.args = kwargs
        self.config_dir = config_dir
        self.config_file = config_file
        self.o = sh.openstack.bake(
            '--os-cloud=ovh',
            _tee=True,
            _out=lambda x: log.info(x.strip()),
            _err=lambda x: log.info(x.strip()),
            _env={'OS_CLIENT_CONFIG_FILE': self.config_file},
        )


class Stack(OpenStackBase):

    def __init__(self, config_dir, config_file, definition=None, **kwargs):
        super().__init__(config_dir, config_file, **kwargs)
        log.info(f'OS_CLIENT_CONFIG_FILE={self.config_file}')
        self.definition = definition

    def get_template(self):
        return f'{settings.SHARE_DIR}/playbooks/infrastructure/template-host.yaml'

    def set_public_key(self, path):
        self.public_key = open(path).read().strip()

    def _create_or_update(self, action, network):
        d = self.definition
        parameters = [
            f'--parameter=public_key={self.public_key}',
        ]
        if 'flavor' in d:
            parameters.append(f'--parameter=flavor={d["flavor"]}')
        if 'port' in d:
            parameters.append(f'--parameter=port={d["port"]}')
        if 'volumes' in d and int(d['volumes'][0]['size']) > 0:
            parameters.append(f"--parameter=volume_size={d['volumes'][0]['size']}")
            parameters.append(f"--parameter=volume_name={d['volumes'][0]['name']}")
        if 'network' in d:
            parameters.append(f'--parameter=network={network}')
        log.info(f'_create_or_update: {d["name"]} {parameters}')
        self.o.stack(action, d['name'],
                     '--wait', '--timeout=600',
                     '--template', self.get_template(),
                     *parameters)
        return self.get_output()

    def get_output(self):
        r = self.o.stack('output', 'show', '--format=value', '-c=output', '--all',
                         self.definition['name'])
        result = json.loads(r.stdout)
        assert 'output_error' not in result, result['output_error']
        return result['output_value']

    def list(self):
        return [
            s.strip() for s in
            self.o.stack.list('--format=value', '-c', 'Stack Name', _iter=True)
        ]

    @staticmethod
    @retry((socket.timeout, ConnectionRefusedError), 9)
    def wait_for_ssh(ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((ip, int(port)))
        line = s.makefile("rb").readline()
        assert line.startswith(b'SSH-')

    def create_or_update(self, return_on_create=False):
        if self.definition['name'] not in self.list():
            self.create()
            if return_on_create:
                return None
        info = self.update()
        if not self.only_internal() or self.args.get('route_to_internal', True):
            self.wait_for_ssh(info['ipv4'], info['port'])
        Hosts(self.config_dir).create_or_update(
            self.definition['name'], info['ipv4'], info['port'])
        return info

    def create_internal_network(self):
        network = self.definition.get('internal_network', OpenStackBase.INTERNAL_NETWORK)
        cidr = self.definition.get('internal_network_cidr', OpenStackBase.INTERNAL_NETWORK_CIDR)
        o = OpenStack(self.config_dir, self.config_file)
        o.network_and_subnet_create(network, cidr)

    def connect_internal_network(self):
        server = self.definition['name']
        network = self.definition.get('internal_network', OpenStackBase.INTERNAL_NETWORK)
        o = OpenStack(self.config_dir, self.config_file)
        if o.server_connected_to_network(server, network):
            return
        self.o.server.add.network(server, network)

    def update(self):
        self.create_internal_network()
        r = self._create_or_update('update', self.definition.get('network', 'Ext-Net'))
        self.connect_internal_network()
        return r

    def only_internal(self):
        return self.definition.get('network', 'Ext-Net') != 'Ext-Net'

    def create(self):
        try:
            log.info('create on network Ext-Net')
            info = self._create_or_update('create', 'Ext-Net')
        except sh.ErrorReturnCode_1:
            log.info('retry create on network Ext-Net')
            # retry once because there is no way to increase the timeout and create fails often
            info = self._create_or_update('update', 'Ext-Net')
        if self.only_internal():
            log.info(f'remove network Ext-Net')
            # wait for the interface to settle before removing it
            self.wait_for_ssh(info['ipv4'], info['port'])
            server = self.definition['name']
            self.o.server.remove.network(server, 'Ext-Net')

    def delete_no_wait(self):
        name = self.definition['name']
        if name not in self.list():
            return False

        self.o.stack.delete('--yes', name)
        return True

    def delete_wait(self):
        name = self.definition['name']

        @retry(AssertionError, 9)
        def wait_is_deleted():
            assert name not in self.list(), f'{name} deletion in progress'
        wait_is_deleted()

        Hosts(self.config_dir).delete(name)

        network = self.definition.get('internal_network', OpenStackBase.INTERNAL_NETWORK)
        o = OpenStack(self.config_dir, self.config_file)
        o.network_delete_if_not_used(network)

    def delete(self):
        if self.delete_no_wait():
            self.delete_wait()


class Heat(OpenStackBase):

    def get_stack_definitions(self, share_dir=settings.SHARE_DIR):
        args = ['-i', f'{share_dir}/inventory',
                '-i', f'{self.config_dir}/inventory']
        if self.args.get('inventory'):
            args.extend([f'--inventory={i}' for i in self.args['inventory']])
        args.extend(['--vars', '--list'])
        password_file = f'{self.config_dir}.pass'
        if os.path.exists(password_file):
            args.extend(['--vault-password-file', password_file])
        r = sh.ansible_inventory(*args)
        inventory = json.loads(r.stdout)
        return inventory['_meta']['hostvars']

    def get_stack_definition(self, host):
        h = self.get_stack_definitions()[host]
        definition = {
            'name': host,
            'port': h.get('ansible_port', '22'),
            'flavor': h.get('openstack_flavor', 's1-2'),
            'network': h.get('openstack_network', 'Ext-Net'),
            'internal_network': OpenStackBase.INTERNAL_NETWORK,
            'internal_network_cidr': h.get('openstack_internal_network_cidr',
                                           OpenStackBase.INTERNAL_NETWORK_CIDR),
        }
        if 'openstack_volumes' in h:
            definition['volumes'] = h['openstack_volumes']
        return definition

    def host_from_volume(self, name):
        for host, definition in self.get_stack_definitions().items():
            for v in definition.get('openstack_volumes', []):
                if v['name'] == name:
                    return host
        return None

    def is_working(self):
        # retry to verify the API is stable
        for _ in range(5):
            try:
                self.o.stack.list()
            except sh.ErrorReturnCode_1:
                return False
        return True

    def create_missings(self, names, public_key):
        return self.create_or_update(Hosts(self.config_dir).missings(names), public_key)

    def create_or_update(self, names, public_key):
        r = {}
        created = []
        #
        # Launch the creation of all stacks in // and do not wait for them to complete
        #
        for name in names:
            s = Stack(self.config_dir, self.config_file, self.get_stack_definition(name),
                      **self.args)
            s.set_public_key(public_key)
            info = s.create_or_update(return_on_create=True)
            if info:
                r[name] = info
            else:
                created.append(name)
        #
        # Verify all stacks previously launched complete as expected
        #
        for name in created:
            s = Stack(self.config_dir, self.config_file, self.get_stack_definition(name),
                      **self.args)
            s.set_public_key(public_key)
            info = s.create_or_update(return_on_create=True)
            r[name] = s.create_or_update()
        return r

    def create_test_subdomain(self, domain):
        d = f"{self.config_dir}/inventory/group_vars/all"
        assert os.path.exists(d)
        if 'bind-host' not in Stack(self.config_dir, self.config_file, **self.args).list():
            return None
        h = Heat(self.config_dir, self.config_file)
        s = Stack(self.config_dir, self.config_file, h.get_stack_definition('bind-host'),
                  **self.args)
        s.set_public_key(f'{self.config_dir}/infrastructure_key.pub')
        bind_host = s.create_or_update()

        # reverse so the leftmost part varies, for human readability
        s = str(int(time.time()))[::-1]
        subdomain = base64.b32encode(s.encode('ascii')).decode('ascii').lower()

        fqdn = f'{subdomain}.test.{domain}'
        log.info(f'creating test subdomain {fqdn}')

        token = os.environ['ENOUGH_API_TOKEN']

        r = requests.post(f'https://api.{domain}/delegate-test-dns/',
                          headers={'Authorization': f'Token {token}'},
                          json={
                              'name': subdomain,
                              'ip': bind_host['ipv4'],
                          })
        r.raise_for_status()
        open(f'{d}/domain.yml', 'w').write(textwrap.dedent(f"""\
        ---
        domain: {fqdn}
        """))
        return fqdn


class OpenStackLeftovers(Exception):
    pass


class OpenStackBackupCreate(Exception):
    pass


class OpenStack(OpenStackBase):

    def __init__(self, config_dir, config_file):
        super().__init__(config_dir, config_file)
        self.config = yaml.load(open(config_file))

    @retry(OpenStackLeftovers, tries=7)
    def destroy_everything(self, prefix):
        log.info('destroy_everything acting')
        leftovers = []

        def delete_snapshots():
            for snapshot in self.o.volume.snapshot.list('--format=value', '-c', 'Name', _iter=True):
                snapshot = snapshot.strip()
                if prefix is None or prefix in snapshot:
                    leftovers.append(f'snapshot({snapshot})')
                    self.o.volume.snapshot.delete(snapshot)

        def delete_stacks():
            r = self.o.stack.list('--format=json', '-c', 'Stack Name', '-c', 'Stack Status')
            for name, status in [(x["Stack Name"], x["Stack Status"])
                                 for x in json.loads(r.stdout)]:
                if prefix is None or prefix in name:
                    leftovers.append(f'stack({name})')
                    if status == 'DELETE_FAILED' or not status.startswith('DELETE'):
                        self.o.stack.delete('--yes', '--wait', name)

        def delete_images():
            for image in self.o.image.list('--private', '--format=value', '-c', 'Name', _iter=True):
                image = image.strip()
                if prefix is None or prefix in image:
                    leftovers.append(f'image({image})')
                    self.o.image.delete(image)

        def delete_volumes():
            for volume in self.o.volume.list('--format=value', '-c', 'Name', _iter=True):
                volume = volume.strip()
                if prefix is None or prefix in volume:
                    leftovers.append(f'volume({volume})')
                    self.o.volume.delete(volume)

        def delete_networks():
            for network in self.o.network.list('--format=value', '-c', 'Name', _iter=True):
                network = network.strip()
                if network == 'Ext-Net':
                    continue
                if prefix is None or prefix in network:
                    leftovers.append(f'network({network})')
                    self.o.network.delete(network)

        #
        # There may be complex interdependencies between resources and
        # no easy way to figure them out. For instance, say there
        # exists a volume created from a snapshot of a volume created
        # by a stack. The stack cannot be deleted befor the volume created
        # from the snapshot is deleted. Because the snapshot cannot be deleted
        # before all volumes created from it are deleted. And the volumes from
        # which the snapshot are created cannot be deleted before all their
        # snapshots are deleted.
        #
        for f in (delete_snapshots, delete_stacks, delete_images, delete_volumes, delete_networks):
            try:
                f()
            except sh.ErrorReturnCode_1:
                pass

        if leftovers:
            raise OpenStackLeftovers('scheduled removal of ' + ' '.join(leftovers))

    def run(self, *args):
        return self.o(*args)

    def network_exists(self, name):
        network = self.o.network.list('--format=value', '-c', 'Name', '--name', name)
        return network.strip() == name

    def network_create(self, name):
        if not self.network_exists(name):
            self.o.network.create(name)

    def network_delete_if_not_used(self, name):
        if not self.network_exists(name):
            return
        ports = self.o.port.list('--device-owner=compute:None',
                                 '--network', name, '--format=value', '-c', 'ID')
        if ports.strip() == '':
            self.o.network.delete(name)

    def subnet_exists(self, name):
        subnet = self.o.subnet.list('--format=value', '-c', 'Name', '--name', name)
        return subnet.strip() == name

    def subnet_create(self, name, cidr):
        if not self.subnet_exists(name):
            self.o.subnet.create('--subnet-range', cidr, '--network', name, name)

    def subnet_update_dns(self, name, *dns):
        args = [f'--dns-nameserver={ip}' for ip in dns]
        args.append(name)
        self.o.subnet.set('--no-dns-nameserver', *args)

    def network_and_subnet_create(self, name, cidr):
        self.network_create(name)
        self.subnet_create(name, cidr)

    def server_connected_to_network(self, server, network):
        return self.server_ip_in_network(server, network)

    def server_ip_in_network(self, server, network):
        info = self.o.port.list('--server', server, '--network', network,
                                '--format=value', '-c', 'Fixed IP Addresses')
        info = info.strip()
        if info == '':
            return None
        pattern = r"ip_address='(.*?)'"
        m = re.search(pattern, info)
        assert m, f're.search({pattern}, {info})'
        return m.group(1)

    def backup_date(self):
        return datetime.datetime.today().strftime('%Y-%m-%d')

    def backup_create(self, volumes):
        if len(volumes) == 0:
            volumes = [x.strip() for x in self.o.volume.list('--format=value', '-c', 'Name')]
        date = self.backup_date()
        snapshots = self._backup_map()
        count = 0
        for volume in volumes:
            s = f'{date}-{volume}'
            if s not in snapshots:
                self.o.volume.snapshot.create('--force', '--volume', volume, s)
                count += 1
        self._backup_available(volumes, date)
        return count

    def _backup_map(self):
        return dict(self._backup_list())

    def _backup_list(self):
        r = self.o.volume.snapshot.list('--format=json', '-c', 'Name', '-c', 'Status',
                                        '--limit', '5000')
        return [(x["Name"], x["Status"]) for x in json.loads(r.stdout)]

    @retry(OpenStackBackupCreate, tries=7)
    def _backup_available(self, volumes, date):
        available = []
        waiting = []
        for name, status in self._backup_list():
            if not name.startswith(date):
                continue
            if status == "available":
                available.append(name)
            else:
                waiting.append(f'{status} {name}')
        available = ",".join(available)
        waiting = ",".join(waiting)
        progress = f'WAITING on {waiting}\nAVAILABLE {available}'
        log.debug(progress)
        if len(waiting) > 0:
            raise OpenStackBackupCreate(progress)

    def backup_prune(self, days):
        before = (datetime.datetime.today() - datetime.timedelta(days)).strftime('%Y-%m-%d')
        count = 0
        for name, status in self._backup_list():
            if name[:10] > before:
                continue
            self.o.volume.snapshot.delete(name)
            count += 1
        return count

    def replace_volume(self, host, volume):
        self.o.server.stop(host)
        attached = self.o.server.show(
            '--format=value', '-c', 'volumes_attached', host).stdout.strip()
        current_volume_id = re.sub("id='(.*)'", "\\1", attached.decode('utf-8'))
        current_volume = self.o.volume.show(
            '--format=value', '-c', 'name', current_volume_id).strip()
        self.o.server.remove.volume(host, current_volume)
        self.o.volume.delete(current_volume)
        self.o.server.add.volume(host, volume)
        self.o.server.start(host)
        self.o.volume.set('--name', current_volume, volume)

    def region_empty(self):
        volumes = self.o.volume.list()
        servers = self.o.server.list()
        images = self.o.image.list('--private')
        return volumes.strip() == '' and servers.strip() == '' and images.strip() == ''
