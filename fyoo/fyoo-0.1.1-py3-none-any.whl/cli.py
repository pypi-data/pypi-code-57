import argparse
import os
import sys
from typing import Optional, List, Sequence, Text

from fyoo.parser import FyooParser


class CliSingleton:

    __instance = None

    PARSER_DESCRIPTION = '''
    This utility wraps around a command, and templates in context to
    the latter command's arguments. The child process will replace
    the fyoo/python process.
    '''.strip()
    PARSER_EXEC_HELP = '''
    Execute a subcommand. The subcommand will spawn a child process that
    will become a parent (implemented by ``os.execvp``).
    '''.strip()
    PARSER_EXEC_COMMAND_HELP = 'Enter any number of arguments as a command'

    def __init__(self):
        self.parser = FyooParser('fyoo', description=CliSingleton.PARSER_DESCRIPTION)
        subparsers = self.parser.add_subparsers(parser_class=argparse.ArgumentParser)
        subparsers.required = True
        exec_parser = subparsers.add_parser('--', help=CliSingleton.PARSER_EXEC_HELP)
        exec_parser.set_defaults(callback=self.exec)
        exec_parser.add_argument('command', nargs=argparse.REMAINDER, help=CliSingleton.PARSER_EXEC_COMMAND_HELP)

    # pylint: disable=no-self-use
    def exec(self, command: List[str]):
        os.execvp(command[0], command)

    def main(self, args: Sequence[Text]) -> None:
        try:
            arg_dict = vars(self.parser.parse_args(args))
        except TypeError as err:
            if err.args == ('sequence item 0: expected str instance, NoneType found', ):
                self.parser.error('Please provide a subcommand')
            raise
        callback = arg_dict.pop('callback')
        callback(**arg_dict)

    def __new__(cls, *args, **kwargs):
        if not kwargs.pop('_is_instance_call', False):
            raise ValueError("Can not instantiate, use .instance() instead")
        return super(CliSingleton, cls).__new__(cls, *args, **kwargs)

    @classmethod
    def instance(cls):
        if cls.__instance is None:
            cls.__instance = cls.__new__(cls, _is_instance_call=True)
            cls.__instance.__init__()
        return cls.__instance

    @classmethod
    def remove(cls):
        if cls.__instance is not None:
            CliSingleton.__instance = None


def get_parser() -> FyooParser:
    return CliSingleton.instance().parser


def main(args: Optional[Sequence[Text]] = None):
    if args is None:
        args = sys.argv[1:]

    cli = CliSingleton.instance()

    cli.main(args)


if __name__ == '__main__':
    main()
