#!/usr/bin/env python
"""
The entrypoint of GitBuilding it is run when `gitbuilding` is run from the commandline.
"""

import argparse
import os
import logging
from colorama import Fore, Style
import pkg_resources
from gitbuilding import example, server
from gitbuilding.handler import GBHandler
from gitbuilding.output import MarkdownBuilder, StaticSiteBuilder

class GBParser():
    """
    The GitBuilding commandline (argparse) parser, it has a number of sub-parsers for
    the sub-commands such as `build` or `serve`
    """

    def __init__(self):
        gb_description = "Run git building to build your documentation"
        self._parser = argparse.ArgumentParser(description=gb_description,
                                               formatter_class=argparse.RawTextHelpFormatter)

        self._parser.add_argument("--version",
                                  action="store_true",
                                  dest="version",
                                  help="Print version information.")

        subparsers = self._parser.add_subparsers(help="Available commands",
                                                 metavar="<command>",
                                                 dest="command")

        self._parser_build = subparsers.add_parser("build", help="Build documentation")
        self._parser_new = subparsers.add_parser("new", help="New gitbuilding project")

        serve_help_str = "Start local server to view documentation"
        self._parser_serve = subparsers.add_parser("serve",
                                                   help=serve_help_str)

        dev_help_str = "Use npm dev server for live editor. Beware, here be dragons!"
        self._parser_serve.add_argument("--dev",
                                        action="store_true",
                                        dest="dev",
                                        help=dev_help_str)
        self._parser_html = subparsers.add_parser("build-html", help="Build static HTML site")

        help_help_str = "Run 'help <command>' for detailed help"
        self._parser_help = subparsers.add_parser("help",
                                                  help=help_help_str)

        self._parser_help.add_argument("h_command",
                                       metavar="<command>",
                                       nargs="?",
                                       type=str,
                                       help="Command to show help for")

    def parse_args(self, args=None, namespace=None):
        """
        Runs parse_args on the main argparse parser
        """
        return self._parser.parse_args(args=args, namespace=namespace)

    def print_help(self, command):
        """
        Can print help for `gitbuilding` or help for each gitbuilding command.
        """
        if command is None:
            self._parser.print_help()
        elif command == "build":
            print("\n`build` will build the documentation in the current folder,\n"
                  "make sure the current folder is a valid gitbuilding project.\n")
            print(self._parser_build.format_help())
        elif command == "build-html":
            print("\n`build-html` will create a static html website using the\n"
                  "build files produced from 'gitbuilding build'\n")
            print(self._parser_html.format_help())
        elif command == "serve":
            print("\n`serve` will create a local webserver to view your built\n"
                  "documentation rendered in HTML. You must run `build` before\n"
                  "running serve.\n")
            print(self._parser_serve.format_help())
        elif command == "new":
            print("\n`new` will create an empty gitbuilding project in the\n"
                  "current folder if empty. If the current folder is not\n"
                  "empty it will ask for a subfolder name for the project\n")
            print(self._parser_new.format_help())
        else:
            print(f"Invalid gitbuilding command {command}\n\n")
            self._parser.print_help()

def main(input_args=None):
    """This is what runs if you run `gitbuilding` from the terminal
    `input_args` can be used to run main from inside python, else sys.argv[1:]
    is used.
    """

    parser = GBParser()
    args = parser.parse_args(args=input_args)

    if args.version:
        print(pkg_resources.get_distribution("gitbuilding").version)
        return None

    if os.path.isfile("buildconf.yaml"):
        config_file = "buildconf.yaml"
    else:
        config_file = None

    handler = GBHandler()
    logger = logging.getLogger('BuildUp')
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    if args.command == "build":
        md_builder = MarkdownBuilder(config_file)
        md_builder.build()

    elif args.command == "new":
        example.output_example_project()

    elif args.command == "serve":

        if args.dev:
            gbs = server.DevServer(config_file, handler)
            print(Fore.RED+
                  "\n\n   WARNING! You are using the gitbuilding dev server."+
                  "\nHere be dragons!\n\n"+
                  Style.RESET_ALL)
            from flask_cors import CORS # pylint: disable=import-outside-toplevel

            CORS(gbs)
        else:
            gbs = server.GBServer(config_file, handler)
        gbs.run()

    elif args.command == "build-html":
        site_builder = StaticSiteBuilder(config_file)
        site_builder.build()

    elif args.command == "help":
        parser.print_help(args.h_command)
    else:
        print(f"Invalid gitbuilding command {args.command}")
    return None


if __name__ == "__main__":
    main()
