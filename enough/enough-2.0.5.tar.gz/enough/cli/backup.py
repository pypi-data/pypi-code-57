from cliff.command import Command

from enough import settings
from enough.common import options
from enough.common import Enough


def set_common_options(parser):
    parser.add_argument(
        '--target-clouds',
        help='Path to the target clouds.yml file')
    return parser


class Restore(Command):
    "Restore a service from a backup"

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        options.set_options(parser)
        parser.add_argument('--target-domain', help='Domain name')
        parser.add_argument('name')
        return set_common_options(parser)

    def take_action(self, parsed_args):
        args = vars(self.app.options)
        args.update(vars(parsed_args))
        e = Enough(settings.CONFIG_DIR, settings.SHARE_DIR, **args)
        e.restore()
