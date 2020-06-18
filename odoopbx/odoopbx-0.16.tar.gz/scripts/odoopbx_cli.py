import click
import logging
import os
import shutil
import odoopbx

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


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
    if not os.exists('/etc/odoopbx'):
        os.mkdir('/etc/odoopbx')


@click.command(help='Call a command.')
@click.argument('cmd', nargs=-1)
def call(cmd):
    """
    Execute a salt-call command passing all parameters.
    To pass an option use -- e.g. odoopbx call -- --version
    """
    cmd_l = ['salt-call']
    cmd_l.extend(list(cmd))
    os.execvp('salt-call', cmd_l)


main.add_command(call)


@click.group(help='Run the Agent from console.',
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


main.add_command(run)


@run.command(help='Configure PBX services. Without parameters list PBX services.')
@click.option('--enable', help='Enable a service.')
def services(enable):
    click.echo('Enabled services:')
    click.echo('- Odoo')
    click.echo('- Asterisk')
    click.echo('- Agent')


if __name__ == '__main__':
    main()
