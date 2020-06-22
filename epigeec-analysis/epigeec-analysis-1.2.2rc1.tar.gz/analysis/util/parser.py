from __future__ import absolute_import, division, print_function

import argparse
from .launcher import CatLaucher, GrepLauncher

class CatParser(object):
    @staticmethod
    def add_parser(subparsers):
        parser = subparsers.add_parser(
            'cat',
            description='UNIX cat like command for json metadata.',
            help='UNIX cat like command for json metadata.'
        )
        parser.set_defaults(func=CatLaucher.run)

        parser.add_argument(
            'input',
            nargs='+',
            help='The metadate file: metadata.json',
            type=str
        )
        parser.add_argument(
            '--md5sum',
            help="Set 'md5sum' as the unique identifier for files instead of file_names.",
            action='store_true')

class GrepParser(object):
    @staticmethod
    def add_parser(subparsers):
        parser = subparsers.add_parser(
            'grep',
            description='UNIX grep like command for json metadata.',
            help='UNIX grep like command for json metadata.'
        )
        parser.set_defaults(func=GrepLauncher.run)

        parser.add_argument('-v', action='store_true', help='Invert the match. Like not the pattern.')

        group = parser.add_mutually_exclusive_group()
        group.add_argument('-e', action='store_true', help='The pattern is a regex for the research.')
        group.add_argument('-f', action='store_true', help='The patterns are in a file.')

        parser.add_argument('pattern', help='The pattern for the research.', type=str)
        parser.add_argument('inputs', nargs='+', help='The raw metadate file: metadata.json', type=str)
        parser.add_argument(
            '--md5sum',
            help="Set 'md5sum' as the unique identifier for files instead of file_names.",
            action='store_true')
