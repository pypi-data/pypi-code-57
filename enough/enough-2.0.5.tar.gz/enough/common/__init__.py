import logging
import os
import re
import sh
import shutil

from enough.common.dotenough import DotEnough, Hosts
from enough.common.host import host_factory
from enough.common.service import service_factory
from enough.common.openstack import OpenStack, Heat
from enough.common import retry
from enough.common import ansible_utils

log = logging.getLogger(__name__)


class Enough(object):

    def __init__(self, config_dir, share_dir, **kwargs):
        self.config_dir = config_dir
        self.share_dir = share_dir
        self.init_args = kwargs.copy()
        self.set_args(**kwargs)

    def set_args(self, **kwargs):
        self.args = self.init_args.copy()
        self.args.update(kwargs)

        if 'clouds' not in self.args:
            self.args['clouds'] = f'{self.config_dir}/inventory/group_vars/all/clouds.yml'
        self.dotenough = DotEnough(self.config_dir, self.args['domain'])
        self.hosts = Hosts(self.config_dir)
        self.host = host_factory(self.config_dir, self.share_dir, **self.args)
        self.service = service_factory(self.config_dir, self.share_dir, **self.args)
        if self.args.get('driver', 'openstack'):
            self.openstack = OpenStack(self.config_dir, self.args['clouds'])
            self.heat = Heat(self.config_dir, self.args['clouds'], **self.args)
        self.playbook = ansible_utils.Playbook(self.config_dir, self.share_dir)
        self.ansible = ansible_utils.Ansible(self.config_dir, self.share_dir)

    def create_missings(self, hosts):
        public_key = f'{self.config_dir}/infrastructure_key.pub'
        r = self.heat.create_missings(hosts, public_key)
        self.update_internal_subnet_dns()
        return r

    def update_internal_subnet_dns(self):
        if not self.hosts.get_ip('bind-host'):
            return
        dns = []
        for host in self.service.service2hosts['bind']:
            dns.append(self.openstack.server_ip_in_network(host, self.openstack.INTERNAL_NETWORK))
        self.openstack.subnet_update_dns(self.openstack.INTERNAL_NETWORK, *dns)

    def _vpn_credentials_path(self):
        return f'{self.config_dir}/openvpn/localhost.tar.gz'

    def vpn_has_credentials(self):
        return os.path.exists(self._vpn_credentials_path())

    def vpn_connect(self):
        sh.sudo.tar('-xf', self._vpn_credentials_path(),
                    _cwd='/etc/openvpn/client')

        network_prefix = self.ansible.get_variable('openvpn',
                                                   'openstack_internal_network_prefix',
                                                   'bind-host')
        sh.sudo.openvpn(
            '--config', 'localhost.conf',
            '--writepid', '/var/run/openvpn-localhost.pid',
            _cwd='/etc/openvpn/client', _bg=True, _truncate_exc=False)

        @retry.retry(AssertionError, tries=5)
        def check_route():
            output = sh.ip.route()
            assert network_prefix in output, f'{network_prefix} in {output}'

        check_route()

    def vpn_disconnect(self):
        if os.path.exists('/var/run/openvpn-localhost.pid'):
            pid = open('/var/run/openvpn-localhost.pid').read().strip()
            sh.sudo.kill(pid)
            sh.sudo.rm('/var/run/openvpn-localhost.pid')

    def clone(self, target_domain, target_clouds):
        config_base = os.path.dirname(self.config_dir)
        config_dir = f'{config_base}/{target_domain}'
        sh.rsync('-a', '--delete',
                 '--exclude=private-key.yml',
                 '--exclude=hosts.yml',
                 '--exclude=group_vars/all/domain.yml',
                 '--exclude=group_vars/all/clouds.yml',
                 '--exclude=group_vars/all/production_domain.yml',
                 f'{self.config_dir}/', f'{config_dir}/')
        clone_override_dir = f'{config_base}/clone-override'
        if os.path.exists(clone_override_dir):
            log.info(f'overriding with {clone_override_dir}')
            sh.rsync('-av', '--checksum', f'{clone_override_dir}/', f'{config_dir}/')
        if os.path.exists(f'{self.config_dir}.pass'):
            shutil.copyfile(f'{self.config_dir}.pass', f'{config_dir}.pass')
        all_dir = f'{config_dir}/inventory/group_vars/all'
        if not os.path.exists(all_dir):
            os.makedirs(all_dir)
        clouds = f'{all_dir}/clouds.yml'
        shutil.copyfile(target_clouds, clouds)
        kwargs = {
            'domain': target_domain,
            'driver': self.args['driver'],
        }
        clone = Enough(config_dir, self.share_dir, **kwargs)
        return clone

    def create_copy_host(self, name, original_volume, copy_volume):
        self.set_args(name=name)
        h = self.host.create_or_update()
        if self.openstack.o.volume.list(
                '-c', 'Status', '--format=value', '--name', copy_volume).strip() == 'available':
            self.openstack.o.server.add.volume(name, copy_volume)
        self.playbook.run([
            f'--private-key={self.dotenough.private_key()}',
            '--extra-vars', f'encrypted_volume_name={original_volume}',
            '--limit', f'localhost,{name}',
            f'{self.share_dir}/copy-playbook.yml',
        ])
        return h['ipv4']

    def delete_copy_host(self, name):
        self.set_args(name=[name])
        self.host.delete()

    def _rsync_copy_host(self, from_ip, to_ip):
        sh.ssh('-i', self.dotenough.private_key(),
               '-o', 'StrictHostKeyChecking=no',
               '-o', 'UserKnownHostsFile=/dev/null',
               f'root@{from_ip}',
               'rsync', '-avHS', '--numeric-ids', '--delete',
               '/srv/', f'root@{to_ip}:/srv/',
               _tee=True,
               _out=lambda x: log.info(x.strip()),
               _err=lambda x: log.info(x.strip()),
               _truncate_exc=False)

    def clone_volume_from_snapshot(self, clone, snapshot):
        (from_ip, to_ip, from_volume, to_volume) = self._clone_volume_from_snapshot_body(
            clone, snapshot)
        self._rsync_copy_host(from_ip, to_ip)
        self._clone_volume_from_snapshot_cleanup(clone, from_volume)
        return to_volume

    def _clone_volume_from_snapshot_body(self, clone, snapshot):
        #
        #         in the current region
        # Step 1: create volume from snapshot
        #
        volume_name = re.sub('^\d\d\d\d-\d\d-\d\d-', '', snapshot)
        from_volume = f'copy-from-{volume_name}'
        if not self.openstack.o.volume.list(
                '-c', 'Name', '--format=value',
                '--name', from_volume).strip() == from_volume:
            self.openstack.o.volume.create('--snapshot', snapshot, from_volume)
        size = self.openstack.o.volume.show(
            '-c', 'size', '--format=value', from_volume).strip()
        #
        #         in the current region
        # Step 2: attach the volume to a host dedicated to copying the content of the volume
        #
        from_ip = self.create_copy_host('copy-from-host', volume_name, from_volume)

        #
        #         in the clone region
        # Step 3: create an empty volume of the same size and attach it to a host dedicated
        #         to receive the copy
        #
        to_volume = f'copy-to-{volume_name}'
        if not clone.openstack.o.volume.list(
                '-c', 'Name', '--format=value',
                '--name', to_volume).strip() == to_volume:
            clone.openstack.o.volume.create('--size', size, to_volume)
        to_ip = clone.create_copy_host('copy-to-host', volume_name, to_volume)

        return (from_ip, to_ip, from_volume, to_volume)

    def _clone_volume_from_snapshot_cleanup(self, clone, copy_from_volume):
        self.delete_copy_host('copy-from-host')
        self.openstack.o.volume.delete(copy_from_volume)
        clone.delete_copy_host('copy-to-host')

    def destroy(self):
        self.openstack.destroy_everything(None)
        sh.rm('-r', self.config_dir)

    def restore(self):
        return self.restore_remote(self.args['target_domain'],
                                   self.args['target_clouds'],
                                   self.args['name'])

    def create_service_matching_snapshot(self, snapshot):
        volume_name = re.sub('^\d\d\d\d-\d\d-\d\d-', '', snapshot)
        host = self.heat.host_from_volume(volume_name)
        service = self.service.service_from_host(host)
        self.set_args(name=service, playbook='enough-playbook.yml')
        self.service.create_or_update()
        return host

    def restore_remote(self, domain, clouds, snapshot):
        clone = self.clone(domain, clouds)
        to_volume = self.clone_volume_from_snapshot(clone, snapshot)
        host = clone.create_service_matching_snapshot(snapshot)
        clone.openstack.replace_volume(host, to_volume)
        return clone
