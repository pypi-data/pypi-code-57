import click
import logging
import os
import shutil
import odoopbx

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

ETC_PATH = '/etc/odoopbx'


@click.group()
def main():
    # Change working folder to Odoo PBX Salt package.
    os.chdir(os.path.join(odoopbx.__path__._path[0], 'salt'))
    # Check if symlink exists for etc and var dirs.
    for p in ['var', 'etc']:
        path = os.path.join(odoopbx.__path__._path[0], 'salt', p)
        if not os.path.islink(path):
            if os.path.isdir(path):
                shutil.rmtree(path)
            # Create a link to etc and var folders to store pki and caches.
            os.symlink('/' + p, path)
    # Check for /etc/odoopbx folder
    if not os.path.exists(ETC_PATH):
        os.mkdir('/etc/odoopbx')
    # Copy default files
    for f in ['odoo.conf', 'asterisk.conf']:
        if not os.path.exists(os.path.join(ETC_PATH, f)):
            open(os.path.join(ETC_PATH, f), 'w').write(
                open(os.path.join(
                    odoopbx.__path__._path[0], 'salt', 'minion.d', f)).read())


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


@main.group(help='Run the Agent from console.',
            invoke_without_command=True)
@click.argument('cmd', nargs=-1)
def run(cmd):
    """
    Execute a salt-call command passing all parameters.
    Example: odoopbx run -- -l info
    """
    cmd_l = ['salt-minion']
    cmd_l.extend(list(cmd))
    os.execvp('salt-minion', cmd_l)


@main.command(help='Enable a service.')
@click.argument('service', required=True)
def enable(service):
    os.execvp('salt-call', ['salt-call', 'state.apply', service])


if __name__ == '__main__':
    main()
