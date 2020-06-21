import glob
import json
import logging
import os
import re
import sh
import tempfile
import textwrap

log = logging.getLogger(__name__)


class Ansible(object):

    def __init__(self, config_dir, share_dir, inventories=[]):
        self.config_dir = config_dir
        self.share_dir = share_dir
        self.set_inventories(inventories)

    def set_inventories(self, inventories):
        self.inventories = [
            '-i', 'inventory',
        ]
        if self.config_dir != '.':
            self.inventories.extend(['-i', f'{self.config_dir}/inventory'])
        if inventories:
            self.inventories.extend([f'-i{i}' for i in inventories])

    def bake_ansible_playbook(self, verbose=True):
        args = [
            '--extra-vars', f'enough_domain_config_directory={self.config_dir}',
        ] + self.inventories
        if self.vault_password_option():
            args.append(self.vault_password_option())
        kwargs = dict(
            _truncate_exc=False,
            _cwd=self.share_dir,
            _env={'ANSIBLE_NOCOLOR': 'true'},
        )

        if verbose:
            kwargs.update(dict(
                _tee=True,
                _out=lambda x: log.info(x.strip()),
                _err=lambda x: log.info(x.strip()),
            ))

        return sh.ansible_playbook.bake(
            *args,
            **kwargs,
        )

    def vault_password_option(self):
        password_file = f'{self.config_dir}.pass'
        if os.path.exists(password_file):
            return f'--vault-password-file={password_file}'
        else:
            log.info(f'no decryption because {password_file} does not exist')
            return None

    def ansible_inventory(self):
        args = [
            '--list',
        ] + self.inventories
        if self.vault_password_option():
            args.append(self.vault_password_option())
        i = sh.ansible_inventory(
            *args,
            _cwd=self.share_dir,
        )
        return json.loads(i.stdout.decode('utf-8'))

    def _flat_inventory(self, i, content):
        hosts = content.get('hosts', [])
        for child in content.get('children', []):
            hosts.extend(self._flat_inventory(i, i[child]))
        return hosts

    def get_groups(self):
        i = self.ansible_inventory()
        del i['_meta']
        groups = {}
        for name, content in i.items():
            groups[name] = self._flat_inventory(i, content)
        return groups

    def get_variable(self, role, variable, host):
        return self.get_variable_hosts(role, variable, host)[host]

    def get_variable_hosts(self, role, variable, *hosts):
        with tempfile.NamedTemporaryFile() as f:
            # the sourrounding "> <" are to prevent conversion to int, list or whatever
            playbook = textwrap.dedent("""
            ---
            - hosts: all
              gather_facts: false
              serial: 1

              roles:
                - role: "{{ rolevar }}"
                  when: false

              tasks:
                - name: print variable
                  debug:
                    msg: ">{{ ansible_play_batch[0] }}:{{ variable }}<"
            """)
            f.write(bytearray(playbook, 'utf-8'))
            f.flush()
            args = [
                '-e', f'rolevar={role}',
                '-e', 'variable={{ ' + variable + ' }}',
                '--limit', ','.join(hosts),
            ] + self.inventories + [
                f.name
            ]
            r = self.bake_ansible_playbook(verbose=False)(*args)
            return dict(re.findall(r'.*"msg": ">(.*?):(.*)<"$',
                                   r.stdout.decode('utf-8'),
                                   re.MULTILINE))


class Playbook(Ansible):

    class NoPasswordException(Exception):
        pass

    @staticmethod
    def is_encrypted(p):
        if not os.path.exists(p):
            return False
        c = open(p).read()
        return c.startswith('$ANSIBLE_VAULT')

    @staticmethod
    def encrypted_files(d):
        return [
            f'{d}/infrastructure_key',
            f'{d}/inventory/group_vars/all/clouds.yml',
        ] + glob.glob(f'{d}/certs/*.key')

    def ensure_decrypted(self):
        encrypted = [f for f in self.encrypted_files(self.config_dir)
                     if self.is_encrypted(f)]
        if len(encrypted) == 0:
            return False
        vault_password_option = self.vault_password_option()
        if not vault_password_option:
            raise Playbook.NoPasswordException(
                f'{encrypted} are encrypted but {self.config_dir}.pass does not exist')
        for f in encrypted:
            log.info(f'decrypt {f}')
            sh.ansible_vault.decrypt(
                vault_password_option,
                f,
                _tee=True,
                _out=lambda x: log.info(x.strip()),
                _err=lambda x: log.info(x.strip()),
                _truncate_exc=False,
                _env={
                    'ANSIBLE_NOCOLOR': 'true',
                }
            )
        return True

    @staticmethod
    def roles_path(d):
        r = glob.glob(f'{d}/playbooks/*/roles')
        r.append(f'{d}/playbooks/wazuh/wazuh-ansible/roles/wazuh')
        return ":".join(r)

    def bake(self):
        args = [
            '--extra-vars', f'enough_domain_config_directory={self.config_dir}',
            '-i', f'{self.share_dir}/inventory',
        ]
        if self.vault_password_option():
            args.append(self.vault_password_option())
        if self.share_dir != self.config_dir:
            args.extend(['-i', f'{self.config_dir}/inventory'])
        logger = logging.getLogger(__name__)
        return sh.ansible_playbook.bake(
            *args,
            _tee=True,
            _out=lambda x: logger.info(x.strip()),
            _err=lambda x: logger.info(x.strip()),
            _truncate_exc=False,
            _env={
                'SHARE_DIR': self.share_dir,
                'CONFIG_DIR': self.config_dir,
                'ANSIBLE_ROLES_PATH': self.roles_path(self.share_dir),
                'ANSIBLE_NOCOLOR': 'true',
            },
        )

    def run_from_cli(self, **kwargs):
        if not kwargs['args']:
            args = [
                '--private-key', f'{self.config_dir}/infrastructure_key',
                f'{self.config_dir}/enough-playbook.yml'
            ]
        else:
            args = kwargs['args'][1:]
        self.run(*args)

    def run(self, *args):
        self.ensure_decrypted()
        self.bake()(*args)
