from typing import List
import sys

from management_commands.command import Command
from management_commands.utils import initialize_argument_parser, run_command


def main(
        commands: List[Command],
        handler_argument_name='___handler',
        **kwargs,
) -> None:
    return run_command(
        parser=initialize_argument_parser(commands=commands, handler_argument_name=handler_argument_name, **kwargs),
        handler_argument_name=handler_argument_name,
        args=sys.argv[1:]
    )
