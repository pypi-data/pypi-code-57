import argparse
from typing import List, Any, TYPE_CHECKING
import asyncio
import sys

if TYPE_CHECKING:
    from management_commands import Command


def underscore(s: str) -> str:
    return ''.join(['_' + c.lower() if c.isupper() else c for c in s]).lstrip('_')


def initialize_argument_parser(
    commands: List['Command'],
    handler_argument_name: str,
    **kwargs,
) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(**kwargs)
    subparsers = parser.add_subparsers(title='commands')

    for command_obj in commands:
        command_obj.add_subparser(subparsers, handler_argument_name=handler_argument_name)

    return parser


def run_command(parser: argparse.ArgumentParser, handler_argument_name: str, args: List[str]) -> Any:
    arguments = vars(parser.parse_args(args=args))

    if handler_argument_name not in arguments:
        parser.print_usage()
        sys.exit(1)

    handler = arguments.pop(handler_argument_name)

    if asyncio.iscoroutinefunction(handler):
        return asyncio.run(handler(**arguments))
    else:
        return handler(**arguments)
