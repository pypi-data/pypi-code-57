import click
import json
import logging
import os
import sys
import shutil
import subprocess
import yaml
import odoopbx

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

ETC_PATH = '/etc/odoopbx'
ODOOPBX_MODULE_PATH = odoopbx.__path__._path[0]


@click.group()
def main():
    # Check for a single installation
    if len(odoopbx.__path__._path) > 1:
        click.secho('Multiple installations detected:', fg='red')
        for p in odoopbx.__path__._path:
            click.echo('- {}'.format(p))
        click.secho('Please clean up.', fg='green')
        sys.exit(-1)
    # Change working folder to Odoo PBX Salt package.
    os.chdir(os.path.join(ODOOPBX_MODULE_PATH, 'salt'))
    # Check for /etc/odoopbx folder
    if not os.path.exists(ETC_PATH):
        os.mkdir(ETC_PATH)
    if not os.path.exists(os.path.join(ETC_PATH, 'local.conf')):
        # Copy default files
        conf_files_path = os.path.join(ODOOPBX_MODULE_PATH, 'salt', 'minion.d')        
        custom_conf = open('/etc/odoopbx/local.conf', 'w')
        for f in [k for k in os.listdir(conf_files_path) if k.endswith(
                '.conf') and not k.startswith('_')]:
            custom_conf.write(
                open(os.path.join(
                    ODOOPBX_MODULE_PATH, 'salt', 'minion.d', f)).read())
        custom_conf.close()


@main.command(help='Call a command.')
@click.argument('cmd', nargs=-1)
def call(cmd):
    """
    Execute a salt-call command passing all parameters.
    To pass an option use -- e.g. odoopbx call -- --version
    """
    cmd_l = ['salt-call']
    cmd_l.extend(list(cmd))
    os.execvp('salt-call', cmd_l)


@main.group(help='Configuration management.')
def config():
    pass


def _config_load():
    config_path = os.path.join(ETC_PATH, 'local.conf')
    config = yaml.load(open(config_path), yaml.SafeLoader)
    return config


def _config_save(config):
    config_path = os.path.join(ETC_PATH, 'local.conf')
    open(config_path, 'w').write(yaml.dump(config))


@config.command(help='Get a configuration option', name='get')
@click.argument('option')
def config_get(option):
    os.execvp('odoopbx', ['odoopbx', 'call', 'config.get', option])


@config.command(help='Set a configuration option', name='set')
@click.argument('option')
@click.argument('value')
def config_set(option, value):    
    try:
        value = json.loads(value)
    except json.decoder.JSONDecodeError:
        # String value
        pass
    config = _config_load()
    if option not in config:
        click.secho('Option {} not found, creating a new one.'.format(
                    option), fg='red')
    config[option] = value
    _config_save(config)


@main.group(help='Run service.',
            invoke_without_command=True)
@click.argument('service', nargs=-1, required=True)
def run(service):
    service = list(service)
    if 'agent' in service:
        service.remove('agent')
        service.insert(0, 'salt-minion')
        service.extend(['-l', 'info'])
        os.execvp('salt-minion', service)
    else:
        click.echo('Not yet implemented')


@main.command(help='Enable a service.')
@click.argument('service', required=True)
def enable(service):
    os.execvp('salt-call', ['salt-call', 'state.apply', service])


@main.command(help='Get configuration option value.')
@click.argument('option')
def get(option):
    os.execvp('salt-call', ['salt-call', 'config.get', option])


@main.command(help='Install a service / all services')
@click.argument('service')
def install(service):
    if service == 'all':
        os.execvp('salt-call', ['salt-call', '-l info', 'state.highstate'])
    else:
        os.execvp('salt-call', ['salt-call', '-l info', 'state.apply', service])


@main.command(help='Restart a service')
@click.argument('service')
def restart(service):
    if service == 'agent':
        service = 'odoopbx-agent'
    os.execvp('systemctl', ['systemctl', 'restart', service])


@main.group(help='Show information.')
def show():
    pass


@main.command(help='Start a service.')
@click.argument('service')
def start(service):
    # Little magic to save time.
    if service == 'agent':
        service = 'odoopbx-agent'
    os.execvp('systemctl', ['systemctl', 'start', service])


@main.command(help='Stop a service.')
@click.argument('service')
def stop(service):
    # Little magic to save time.
    if service == 'agent':
        service = 'odoopbx-agent'
    os.execvp('systemctl', ['systemctl', 'stop', service])


@show.command(help='Show system information.', name='system')
def show_system():
    click.echo('Python path: {}'.format(ODOOPBX_MODULE_PATH))


if __name__ == '__main__':
    main()
