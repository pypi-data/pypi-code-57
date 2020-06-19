import os

from polidoro_argument import Command
from polidoro_cli.clis.cli import CLI
from polidoro_cli.clis.cli_utils import set_environment_variables, CONFIG_FILE
from polidoro_cli.clis.docker.docker import Docker


class QueroBoot(Docker):
    help = 'QueroBoot CLI commands'

    @staticmethod
    @Command(
        help='Run "docker exec COMMAND"',
        aliases={'environment_vars': 'e'}
    )
    def exec(*args, environment_vars={}):
        Docker.exec(*args, environment_vars=environment_vars)

    @staticmethod
    @Command(
        help='Run "docker-compose up"'
    )
    def up(*args):
        compose_args = ' '.join(filter(lambda a: a.startswith('-'), args))
        other_args = ' '.join(filter(lambda a: not a.startswith('-'), args))
        qb_dir = os.environ.get('QUERO_BOOT_DIR', None)
        if qb_dir and not os.path.exists(qb_dir):
            print('%s is not a valid directory' % qb_dir)
            qb_dir = None
        if not qb_dir:
            qb_dir = set_environment_variables('QUERO_BOOT_DIR', input('QueroBoot dir: '), file_name=CONFIG_FILE,
                                               exit_on_complete=False)
        CLI.execute('docker-compose up %s %s %s' % (compose_args, Docker.get_container_name(), other_args),
                    dir=qb_dir)
