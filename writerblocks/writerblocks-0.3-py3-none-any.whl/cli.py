#!/usr/bin/env python3
"""Command-line interface for the tool."""

import argparse

import os.path
from writerblocks.common import DEFAULT_OPTIONS
from writerblocks.backend import (parse_options, run)


def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="A toolkit for writing stories in a modular way.")

    parser.add_argument('-d', '--base-dir', type=os.path.abspath,
                        help="Directory in which project files are stored; if "
                             "not specified, current directory will be used")
    parser.add_argument('-f', '--out-fmt',
                        help="File format to export projects to (default: {})"
                        .format(DEFAULT_OPTIONS.out_fmt))
    parser.add_argument('-r', '--in-fmt', help="Text file format (default: {})"
                        .format(DEFAULT_OPTIONS.in_fmt))
    parser.add_argument('-o', '--out-file',
                        help='Output file name, including extension'
                             ' (default: "{}")'.format(DEFAULT_OPTIONS.out_file))
    parser.add_argument('-i', '--index-file',
                        help='Index file to use; if not provided, will attempt '
                             'to automatically locate in project directory')
    parser.add_argument('-t', '--tags', nargs='+',
                        help="Ignore text files that don't have these tags "
                             "(space- or comma-separated)")
    parser.add_argument('-a', '--all-tags', action='store_true',
                        help='Use only files that match *all* specified tags'
                             ' (overrides default behavior)')
    parser.add_argument('-b', '--blacklist-tags', nargs='+',
                        help='Ignore files with these tags (space- or '
                             'comma-separated)')
    parser.add_argument('-n', '--new-project', action='store_true',
                        help='Create a new project with default contents.')

    parser.epilog = ("""All other command-line options will be passed to pandoc 
                     when output is generated.
                     All options may be set in writerblocks.ini; command-line
                     options will override config file ones.""")
    return parser


def main():
    """Run the command-line writerblocks tool."""
    parser = setup_parser()
    parse_options(*parser.parse_known_args())
    return run(action_on_error=parser.print_help)


if __name__ == '__main__':
    main()
