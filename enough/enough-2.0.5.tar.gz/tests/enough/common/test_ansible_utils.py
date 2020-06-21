import pytest
import shutil
import yaml

from enough import settings
from enough.common import ansible_utils


def test_get_variable_no_arg():
    defaults = yaml.load(open('playbooks/api/roles/api/defaults/main.yml'))
    variable = 'api_admin_password'
    ansible = ansible_utils.Ansible(settings.CONFIG_DIR, settings.SHARE_DIR)
    value = ansible.get_variable('api', variable, 'api-host')
    assert defaults[variable] == value


def test_get_variable_hosts():
    ansible = ansible_utils.Ansible(settings.CONFIG_DIR, settings.SHARE_DIR)
    d = ansible.get_variable_hosts('authorized_keys', 'production_domain',
                                   'bind-host', 'icinga-host')
    assert d == {'bind-host': 'enough.community', 'icinga-host': 'enough.community'}


def test_get_variable_inventory():
    test_inventory = 'tests/enough/common/test_ansible_utils/variables_inventory'
    expected = yaml.load(open(f'{test_inventory}/host_vars/api-host.yml'))
    variable = 'api_admin_password'
    ansible = ansible_utils.Ansible(settings.CONFIG_DIR, settings.SHARE_DIR)
    ansible.set_inventories([test_inventory])
    value = ansible.get_variable('api', variable, 'api-host')
    assert expected[variable] == value


def test_playbook_roles_path():
    p = ansible_utils.Playbook(settings.CONFIG_DIR, settings.SHARE_DIR)
    r = p.roles_path('.')
    assert '/infrastructure/' in r


def test_playbook_ensure_decrypted(tmpdir):
    p = ansible_utils.Playbook(settings.CONFIG_DIR, settings.SHARE_DIR)
    shutil.copytree('tests/enough/common/test_ansible_utils/domain.com',
                    f'{tmpdir}/domain.com')
    c = f'{tmpdir}/domain.com'
    p.config_dir = c

    #
    # decryption is needed but no password is found
    #
    with pytest.raises(ansible_utils.Playbook.NoPasswordException):
        assert p.ensure_decrypted() is False
    shutil.copyfile('tests/enough/common/test_ansible_utils/domain.com.pass',
                    f'{tmpdir}/domain.com.pass')

    #
    # all files are decrypted
    #
    for f in p.encrypted_files(c):
        if f.endswith('not-encrypted.key'):
            continue
        assert p.is_encrypted(f)
    assert p.ensure_decrypted() is True
    for f in p.encrypted_files(c):
        assert not p.is_encrypted(f)
    #
    # nothing to do
    #
    assert p.ensure_decrypted() is False


def test_playbook_run_with_args(caplog):
    p = ansible_utils.Playbook(settings.CONFIG_DIR, settings.SHARE_DIR)
    p.run('tests/enough/common/test_ansible_utils/playbook-ok.yml')
    assert 'OK_PLAYBOOK' in caplog.text
    assert 'OK_IMPORTED' in caplog.text


def test_playbook_run_no_args(mocker):
    called = {}

    def playbook():
        def run(*args):
            assert '--private-key' in args
            called['playbook'] = True
        return run
    mocker.patch('enough.common.ansible_utils.Playbook.bake',
                 side_effect=playbook)
    kwargs = {
        'args': [],
    }
    p = ansible_utils.Playbook(settings.CONFIG_DIR, settings.SHARE_DIR)
    p.run_from_cli(**kwargs)
    assert 'playbook' in called


def test_ansible_inventory():
    i = ansible_utils.Ansible(settings.CONFIG_DIR, settings.SHARE_DIR).ansible_inventory()
    assert '_meta' in i


def test_get_groups():
    i = ansible_utils.Ansible(settings.CONFIG_DIR, settings.SHARE_DIR).get_groups()
    assert 'all-hosts' in i


def test_flat_inventory():
    inventory = {
        'group1': {
            'children': ['group2', 'group3'],
            'hosts': ['host10', 'host11'],
        },
        'group2': {
            'hosts': ['host20'],
            'children': ['group4'],
        },
        'group3': {
            'hosts': ['host30', 'host31'],
        },
        'group4': {
            'children': ['group5', 'group6'],
        },
        'group5': {
            'hosts': ['host50', 'host51'],
        },
        'group6': {},
        'group7': {
            'hosts': ['host70', 'host71'],
        }
    }
    ansible = ansible_utils.Ansible(settings.CONFIG_DIR, settings.SHARE_DIR)
    expected = ['host10', 'host11', 'host20', 'host30', 'host31', 'host50', 'host51']
    assert sorted(ansible._flat_inventory(inventory, inventory['group1'])) == expected
    expected = ['host70', 'host71']
    assert sorted(ansible._flat_inventory(inventory, inventory['group7'])) == expected
