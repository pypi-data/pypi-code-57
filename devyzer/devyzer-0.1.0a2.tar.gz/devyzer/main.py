#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import print_function
from __future__ import unicode_literals

import argparse
import logging
import os
import sys
from sys import exit

from devyzer import auth, terminal, __version__
from devyzer.config import Config
from devyzer.utils import print_devyzer
from devyzer.utils.logger import TerminalLogger

logger = logging.getLogger(__name__)


def create_argument_parser() -> argparse.ArgumentParser:
    """Parse all the command line arguments for the training script."""

    parser = argparse.ArgumentParser(
        prog="Bot Watcher Service",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="A Devyzer Bot Watcher Service that subscribes to devyzer pub-sub channels "
                    ", watch if a party needs to send actions or communicate something to Bot ",
    )

    parser.add_argument(
        "--version",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Print installed Bot Watcher version",
    )

    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parsers = [parent_parser]

    subparsers = parser.add_subparsers(help="Available commands")

    terminal.subparser(subparsers, parents=parent_parsers)
    auth.subparser(subparsers, parents=parent_parsers)

    return parser


def print_version() -> None:
    print_devyzer()
    print("Version : ", __version__)


def init():
    import devyzer

    config = Config()
    devyzer.config = config.read_configuration()
    devyzer.logger = TerminalLogger(__name__,
                                    devyzer.config[config.MAIN][config.LOG_FILE],
                                    devyzer.config[config.MAIN][config.LOG_LEVEL]).logger


def main():
    arg_parser = create_argument_parser()
    cmdline_arguments = arg_parser.parse_args()

    # insert current path in syspath so custom modules are found
    sys.path.insert(1, os.getcwd())

    init()

    if hasattr(cmdline_arguments, "func"):
        cmdline_arguments.func(cmdline_arguments)
    elif hasattr(cmdline_arguments, "version"):
        print_version()
    else:
        # user has not provided a subcommand, let's print the help
        logger.error("No command specified.")
        arg_parser.print_help()
        exit(1)


if __name__ == '__main__':
    main()
